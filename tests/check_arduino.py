#!/usr/bin/env python3
"""
Simple script to check Arduino state and test basic communication
"""

import serial
import time

def check_arduino(port):
    """Check Arduino state and test communication"""
    print(f"Checking Arduino on {port}")
    print("-" * 40)
    
    try:
        # Connect to Arduino
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(3)
        
        print("Connected to Arduino")
        print("Reading Arduino output for 10 seconds...")
        print()
        
        # Read Arduino output for 10 seconds
        start_time = time.time()
        while time.time() - start_time < 10:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                if line:
                    print(f"Arduino: {line}")
            time.sleep(0.1)
        
        print("\nSending START_WRITE command...")
        ser.write(b"START_WRITE\n")
        ser.flush()
        
        print("Reading response for 5 seconds...")
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                if line:
                    print(f"Arduino: {line}")
            time.sleep(0.1)
        
        print("\nSending test data...")
        ser.write(b"TEST_DATA\n")
        ser.flush()
        
        print("Reading response for 5 seconds...")
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                if line:
                    print(f"Arduino: {line}")
            time.sleep(0.1)
        
        ser.close()
        print("\nCheck completed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "COM10"
    check_arduino(port)
