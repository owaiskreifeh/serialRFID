#!/usr/bin/env python3
"""
RFID CLI Tool - Interface for Arduino RFID Reader/Writer
Features:
- Read and save card data
- Write data to cards
- Associate UUIDs with custom text
- Output card data or associated text as keyboard input
"""

import serial
import json
import os
import time
import threading
import argparse
from datetime import datetime
try:
    import pynput.keyboard as keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Warning: pynput not installed. Keyboard output disabled.")
    print("Install with: pip install pynput")

class RFIDTool:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.running = False
        self.cards_db = "config/rfid_cards.json"
        self.associations_db = "config/rfid_associations.json"
        self.cards = self.load_cards()
        self.associations = self.load_associations()
        
    def load_cards(self):
        """Load saved cards from JSON file"""
        if os.path.exists(self.cards_db):
            try:
                with open(self.cards_db, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cards(self):
        """Save cards to JSON file"""
        with open(self.cards_db, 'w') as f:
            json.dump(self.cards, f, indent=2)
    
    def load_associations(self):
        """Load UUID-text associations from JSON file"""
        if os.path.exists(self.associations_db):
            try:
                with open(self.associations_db, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_associations(self):
        """Save UUID-text associations to JSON file"""
        with open(self.associations_db, 'w') as f:
            json.dump(self.associations, f, indent=2)
    
    def connect(self):
        """Connect to Arduino via serial"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"Connected to {self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Arduino"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("Disconnected")
    
    def send_command(self, command):
        """Send command to Arduino"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write((command + '\n').encode())
            return True
        return False
    
    def read_line(self):
        """Read line from Arduino"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                line = self.serial_conn.readline().decode().strip()
                return line
            except:
                return ""
        return ""
    
    def write_to_card(self, data):
        """Write data to RFID card"""
        if len(data) > 16:
            print("Warning: Data truncated to 16 characters")
            data = data[:16]
        
        print("Entering write mode...")
        self.send_command("START_WRITE")
        time.sleep(1)  # Increased delay to ensure Arduino is ready
        
        print(f"Sending data: {data}")
        self.send_command(data)
        time.sleep(0.5)  # Wait for data to be processed
        
        print("Present card to write data...")
        print("Waiting for card...")
        
        # Clear any existing serial buffer
        if self.serial_conn and self.serial_conn.in_waiting:
            self.serial_conn.reset_input_buffer()
        
        start_time = time.time()
        while time.time() - start_time < 30:  # 30 second timeout
            line = self.read_line()
            if line:
                print(f"Arduino: {line}")
                if "Data written successfully" in line:
                    print("Write successful!")
                    return True
                elif "Failed to write" in line:
                    print("Write failed!")
                    return False
                elif "Authentication failed" in line:
                    print("Authentication failed!")
                    return False
                elif "Write operation failed" in line:
                    print("Write operation failed!")
                    return False
                elif "Returning to read mode" in line:
                    print("Write operation completed, returning to read mode")
                    return True  # Consider this a success since we got to this point
                elif "ets" in line or "rst:" in line:
                    print("Arduino reset detected! This may indicate power issues or communication problems.")
                    return False
        
        print("Write timeout")
        return False
    
    def monitor_cards(self, keyboard_output=False):
        """Monitor for card reads and handle them"""
        print("Monitoring for cards... (Press Ctrl+C to stop)")
        print(f"Keyboard output: {'Enabled' if keyboard_output and KEYBOARD_AVAILABLE else 'Disabled'}")
        
        self.running = True
        try:
            while self.running:
                line = self.read_line()
                if line and line.startswith("START_CARD-"):
                    self.handle_card_read(line, keyboard_output)
                elif line and line.strip():
                    print(f"Arduino: {line}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            print("\nStopping monitor...")
    
    def handle_card_read(self, line, keyboard_output=False):
        """Handle a card read event"""
        try:
            # Parse: START_CARD-UUID_CARRIED-DATA
            parts = line.replace("START_CARD-", "").split("_CARRIED-")
            if len(parts) != 2:
                print(f"Invalid card format: {line}")
                return
            
            uuid, data = parts
            timestamp = datetime.now().isoformat()
            
            # Save card data
            self.cards[uuid] = {
                'data': data,
                'last_seen': timestamp,
                'read_count': self.cards.get(uuid, {}).get('read_count', 0) + 1
            }
            self.save_cards()
            
            print(f"\n--- Card Read ---")
            print(f"UUID: {uuid}")
            print(f"Data: {data}")
            print(f"Read count: {self.cards[uuid]['read_count']}")
            
            # Check for associations
            output_text = None
            if uuid in self.associations:
                output_text = self.associations[uuid]
                print(f"Associated text: {output_text}")
            elif data and data != "EMPTY":
                output_text = data
                print(f"Using card data for output")
            
            # Keyboard output
            if keyboard_output and KEYBOARD_AVAILABLE and output_text:
                self.type_text(output_text)
            
            print("--- End ---\n")
            
        except Exception as e:
            print(f"Error handling card read: {e}")
    
    def type_text(self, text):
        """Type text using keyboard simulation"""
        if not KEYBOARD_AVAILABLE:
            print("Keyboard output not available")
            return
        
        try:
            print(f"Typing: {text}")
            # Small delay before typing
            time.sleep(0.5)
            
            # Use pynput to type the text
            kb = keyboard.Controller()
            kb.type(text)
            
        except Exception as e:
            print(f"Error typing text: {e}")
    
    def associate_uuid_text(self, uuid, text):
        """Associate a UUID with custom text"""
        self.associations[uuid] = text
        self.save_associations()
        print(f"Associated UUID {uuid} with text: {text}")
    
    def list_cards(self):
        """List all saved cards"""
        if not self.cards:
            print("No cards saved")
            return
        
        print("\n--- Saved Cards ---")
        for uuid, info in self.cards.items():
            print(f"UUID: {uuid}")
            print(f"  Data: {info['data']}")
            print(f"  Last seen: {info['last_seen']}")
            print(f"  Read count: {info['read_count']}")
            if uuid in self.associations:
                print(f"  Associated text: {self.associations[uuid]}")
            print()
    
    def list_associations(self):
        """List all UUID-text associations"""
        if not self.associations:
            print("No associations saved")
            return
        
        print("\n--- UUID Associations ---")
        for uuid, text in self.associations.items():
            print(f"{uuid} -> {text}")
        print()
    
    def delete_card(self, uuid):
        """Delete a saved card"""
        if uuid in self.cards:
            del self.cards[uuid]
            self.save_cards()
            print(f"Deleted card: {uuid}")
        else:
            print(f"Card not found: {uuid}")
    
    def delete_association(self, uuid):
        """Delete a UUID association"""
        if uuid in self.associations:
            del self.associations[uuid]
            self.save_associations()
            print(f"Deleted association: {uuid}")
        else:
            print(f"Association not found: {uuid}")

def main():
    parser = argparse.ArgumentParser(description='RFID CLI Tool')
    parser.add_argument('--port', '-p', required=True, help='Serial port (e.g., COM3 or /dev/ttyUSB0)')
    parser.add_argument('--baudrate', '-b', type=int, default=115200, help='Baudrate (default: 115200)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor for card reads')
    monitor_parser.add_argument('--keyboard', '-k', action='store_true', 
                               help='Enable keyboard output for card data/associations')
    
    # Write command
    write_parser = subparsers.add_parser('write', help='Write data to card')
    write_parser.add_argument('data', help='Data to write (max 16 characters)')
    
    # List commands
    subparsers.add_parser('list-cards', help='List all saved cards')
    subparsers.add_parser('list-associations', help='List all UUID associations')
    
    # Associate command
    assoc_parser = subparsers.add_parser('associate', help='Associate UUID with text')
    assoc_parser.add_argument('uuid', help='Card UUID')
    assoc_parser.add_argument('text', help='Text to associate')
    
    # Delete commands
    del_card_parser = subparsers.add_parser('delete-card', help='Delete saved card')
    del_card_parser.add_argument('uuid', help='Card UUID to delete')
    
    del_assoc_parser = subparsers.add_parser('delete-association', help='Delete UUID association')
    del_assoc_parser.add_argument('uuid', help='UUID association to delete')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Commands that don't need serial connection
    if args.command in ['list-cards', 'list-associations']:
        tool = RFIDTool(args.port, args.baudrate)
        if args.command == 'list-cards':
            tool.list_cards()
        elif args.command == 'list-associations':
            tool.list_associations()
        return
    
    # Commands that need serial connection
    tool = RFIDTool(args.port, args.baudrate)
    
    if not tool.connect():
        return
    
    try:
        if args.command == 'monitor':
            tool.monitor_cards(keyboard_output=args.keyboard)
        elif args.command == 'write':
            tool.write_to_card(args.data)
        elif args.command == 'associate':
            tool.associate_uuid_text(args.uuid, args.text)
        elif args.command == 'delete-card':
            tool.delete_card(args.uuid)
        elif args.command == 'delete-association':
            tool.delete_association(args.uuid)
    
    finally:
        tool.disconnect()

if __name__ == "__main__":
    main()