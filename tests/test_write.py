#!/usr/bin/env python3
"""
Test script for RFID write operations with enhanced debugging
"""

import serial
import time
import sys

def test_write_operation(port, data="TEST_DATA"):
    """Test write operation with detailed debugging"""
    print(f"Testing write operation on {port}")
    print(f"Data to write: {data}")
    print("-" * 50)
    
    try:
        # Connect to Arduino
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(3)  # Wait for Arduino to fully initialize
        
        print("Connected to Arduino")
        print("Waiting for Arduino to be ready...")
        
        # Clear any existing data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Wait for Arduino ready message
        start_time = time.time()
        while time.time() - start_time < 10:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                print(f"Arduino: {line}")
                if "RFID Reader ready" in line:
                    print("Arduino is ready!")
                    break
            time.sleep(0.1)
        
        # Send write command
        print("\nSending START_WRITE command...")
        ser.write(b"START_WRITE\n")
        ser.flush()
        time.sleep(1)
        
        # Check for write mode confirmation
        start_time = time.time()
        write_mode_confirmed = False
        while time.time() - start_time < 5:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                print(f"Arduino: {line}")
                if "Entering write mode" in line:
                    write_mode_confirmed = True
                    break
            time.sleep(0.1)
        
        if not write_mode_confirmed:
            print("ERROR: Arduino did not enter write mode")
            ser.close()
            return False
        
        # Send data
        print(f"\nSending data: {data}")
        ser.write(f"{data}\n".encode())
        ser.flush()
        time.sleep(1)
        
        # Check for data confirmation
        start_time = time.time()
        data_confirmed = False
        while time.time() - start_time < 5:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                print(f"Arduino: {line}")
                if "Data received" in line:
                    data_confirmed = True
                    break
            time.sleep(0.1)
        
        if not data_confirmed:
            print("ERROR: Arduino did not confirm data reception")
            ser.close()
            return False
        
        print("\nData confirmed. Now present a card to write...")
        print("Waiting for card detection and write operation...")
        
        # Monitor for write results
        start_time = time.time()
        while time.time() - start_time < 30:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                print(f"Arduino: {line}")
                
                # Check for various outcomes
                if "Data written successfully" in line:
                    print("SUCCESS: Data written successfully!")
                    ser.close()
                    return True
                elif "Failed to write" in line:
                    print("ERROR: Write operation failed")
                    ser.close()
                    return False
                elif "Authentication failed" in line:
                    print("ERROR: Authentication failed")
                    ser.close()
                    return False
                elif "Write operation failed" in line:
                    print("ERROR: Write operation failed")
                    ser.close()
                    return False
                elif "Returning to read mode" in line:
                    print("INFO: Returning to read mode")
                    break
                elif "ets" in line or "rst:" in line:
                    print("ERROR: Arduino reset detected!")
                    ser.close()
                    return False
            
            time.sleep(0.1)
        
        print("TIMEOUT: No write result received within 30 seconds")
        ser.close()
        return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_write.py <port> [data]")
        print("Example: python test_write.py COM10 TEST123")
        return
    
    port = sys.argv[1]
    data = sys.argv[2] if len(sys.argv) > 2 else "TEST_DATA"
    
    success = test_write_operation(port, data)
    
    if success:
        print("\n[SUCCESS] Write test completed successfully!")
    else:
        print("\n[ERROR] Write test failed!")
        print("\nTroubleshooting tips:")
        print("1. Check power supply - RFID writing requires stable power")
        print("2. Ensure card is properly positioned on the reader")
        print("3. Try a different card if available")
        print("4. Check serial connection and baudrate")
        print("5. Verify Arduino code is uploaded correctly")

if __name__ == "__main__":
    main()
