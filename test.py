import bluetooth

# UUID for the service and characteristic (must match the ESP32 server)
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

def receive_array():
    # Create a Bluetooth socket
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    print("Waiting for connection...")
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    # Search for the ESP32 service by UUID
    service_matches = bluetooth.find_service(uuid=SERVICE_UUID)
    if len(service_matches) == 0:
        print("No service found with the UUID", SERVICE_UUID)
        return

    # Connect to the ESP32 service
    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]
    print("Connecting to", name, "at", host, "on port", port)
    client_sock.connect((host, port))

    # Receive the data from the ESP32
    data = client_sock.recv(1024)
    received_array = list(map(int, data.decode().split(',')))

    print("Received array:", received_array)

    # Close the connection
    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    receive_array()
