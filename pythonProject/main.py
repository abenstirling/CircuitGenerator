import serial

port = '/dev/cu.usbserial-0001'  # Update with the correct USB serial port name
baud_rate = 115200


def receiveList():
    received_data = []

    # Read the size of the list
    list_size = 1024
    print("List size:", list_size)

    # Read the list elements one by one
    for _ in range(list_size):
        # Read a floating-point number from the serial port
        data_str = ser.readline().decode().strip()

        # Safely convert the string to a float
        try:
            received_value = float(data_str)
            received_data.append(received_value)
        except ValueError:
            print("Failed to parse received data as a float:", data_str)

    return received_data


ser = serial.Serial(port, baud_rate)
received_list = receiveList()
print("Received list:", received_list)

ser.close()
