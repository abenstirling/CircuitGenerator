import serial
import ast
import time

port = '/dev/cu.usbserial-0001'  # Update with the correct USB serial port name
baud_rate = 115200


def receiveList():
    received_data = []

    # Read the size of the list
    list_size = 1024
    print("List size:", list_size)

    # Read the list as a string
    data_str = ser.readline().decode().strip()
    print("Received data:", data_str)

    # Safely evaluate the string as a list
    try:
        received_data = ast.literal_eval(data_str)
    except (SyntaxError, ValueError):
        print("Failed to parse received data as a list.")

    return received_data




message = "true"

ser = serial.Serial(port, baud_rate)
ser.write(message.encode())
received_list = receiveList()
print("Received list:", received_list)

ser.close()
