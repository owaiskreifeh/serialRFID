/*
  RFID Reader/Writer with Serial Communication
  Modified to support START_CARD-UUID_CARRIED-DATA format and write mode
  Based on Random Nerd Tutorials RFID example
*/

#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
#include <MFRC522DriverPinSimple.h>
#include <MFRC522Debug.h>

// Pin configuration
MFRC522DriverPinSimple ss_pin(5);
MFRC522DriverSPI driver{ss_pin};
MFRC522 mfrc522{driver};

// RFID key and block configuration
MFRC522::MIFARE_Key key;
byte blockAddress = 2;
byte bufferblocksize = 18;
byte blockDataRead[18];

// Mode control
enum Mode {
  READ_MODE,
  WRITE_MODE
};

Mode currentMode = READ_MODE;
unsigned long lastWriteIndicator = 0;
const unsigned long WRITE_INDICATOR_INTERVAL = 1000; // 1 second
String dataToWrite = ""; // Data to write when in write mode
bool dataReceived = false;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  
  mfrc522.PCD_Init();
  MFRC522Debug::PCD_DumpVersionToSerial(mfrc522, Serial);
  
  // Prepare key - all keys are set to FFFFFFFFFFFF at chip delivery from the factory
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
  
  Serial.println(F("RFID Reader ready. Send 'START_WRITE' to enter write mode."));
}

void loop() {
  // Check for serial commands
  checkSerialCommands();
  
  // Handle write mode indicator
  if (currentMode == WRITE_MODE) {
    unsigned long currentTime = millis();
    if (currentTime - lastWriteIndicator >= WRITE_INDICATOR_INTERVAL) {
      Serial.println("__WRITE__");
      lastWriteIndicator = currentTime;
    }
  }
  
  // Check if a new card is present
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  // Handle card based on current mode
  if (currentMode == READ_MODE) {
    handleCardRead();
  } else if (currentMode == WRITE_MODE && dataReceived) {
    handleCardWrite();
  }

  delay(1000); // Prevent rapid re-reads
}

void checkSerialCommands() {
  if (Serial.available()) {
    String command = Serial.readString();
    command.trim();
    
    if (command == "START_WRITE") {
      currentMode = WRITE_MODE;
      dataReceived = false;
      dataToWrite = "";
      Serial.println("Entering write mode. Send data to write, then present card.");
      lastWriteIndicator = millis();
    } else if (currentMode == WRITE_MODE && !dataReceived) {
      // In write mode, store the data to write
      dataToWrite = command;
      dataReceived = true;
      Serial.println("Data received. Present card to write: " + dataToWrite);
    }
  }
}

void handleCardRead() {
  // Get card UID as hex string
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (uid.length() > 0) uid += ":";
    if (mfrc522.uid.uidByte[i] < 16) uid += "0"; // Add leading zero for single digit hex
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();
  
  // Read data from card
  String cardData = readDataFromCard();
  
  // Send in specified format: START_CARD-UUID_CARRIED-DATA
  Serial.println("START_CARD-" + uid + "_CARRIED-" + cardData);
  
  // Halt communication with the card
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

void handleCardWrite() {
  // Write data to card
  if (writeDataToCard(dataToWrite)) {
    Serial.println("Data written successfully to card");
  } else {
    Serial.println("Failed to write data to card");
  }
  
  // Return to read mode
  currentMode = READ_MODE;
  dataReceived = false;
  dataToWrite = "";
  Serial.println("Returning to read mode");
  
  // Halt communication with the card
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

String readDataFromCard() {
  // Authenticate the specified block using KEY_A = 0x60
  if (mfrc522.PCD_Authenticate(0x60, blockAddress, &key, &(mfrc522.uid)) != 0) {
    return "AUTH_ERROR";
  }

  // Read data from the specified block
  if (mfrc522.MIFARE_Read(blockAddress, blockDataRead, &bufferblocksize) != 0) {
    return "READ_ERROR";
  }

  // Convert to string (remove null terminators and non-printable chars)
  String data = "";
  for (byte i = 0; i < 16; i++) {
    if (blockDataRead[i] >= 32 && blockDataRead[i] <= 126) { // Printable ASCII
      data += char(blockDataRead[i]);
    } else if (blockDataRead[i] == 0) {
      break; // Stop at null terminator
    }
  }
  
  return data.length() > 0 ? data : "EMPTY";
}

bool writeDataToCard(String data) {
  // Prepare data buffer (16 bytes for MIFARE Classic)
  byte newBlockData[16];
  memset(newBlockData, 0, sizeof(newBlockData)); // Clear buffer with zeros
  
  // Copy data to buffer (max 16 characters)
  for (int i = 0; i < data.length() && i < 16; i++) {
    newBlockData[i] = data[i];
  }
  
  // Authenticate the specified block using KEY_A = 0x60
  if (mfrc522.PCD_Authenticate(0x60, blockAddress, &key, &(mfrc522.uid)) != 0) {
    return false;
  }
  
  // Write data to the specified block
  if (mfrc522.MIFARE_Write(blockAddress, newBlockData, 16) != 0) {
    return false;
  }
  
  return true;
}