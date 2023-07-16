from bluepy import btle

# UUID for the service and characteristic (must match the ESP32 server)
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        # Convert the received bytes to integers
        received_array = []
        for i in range(len(data) // 4):  # Assuming 4 bytes per integer
            value = int.from_bytes(data[i * 4 : (i + 1) * 4], byteorder="little", signed=True)
            received_array.append(value)

        print("Received array:", received_array)

def receive_array():
    # Create a BLE scanner and start scanning
    scanner = btle.Scanner()
    devices = scanner.scan(5.0)  # Scan for 5 seconds

    # Search for the ESP32 service by UUID
    esp32_device = None
    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Complete 128b Services" and value == SERVICE_UUID:
                esp32_device = dev
                break

    if not esp32_device:
        print("No device found with the service UUID", SERVICE_UUID)
        return

    # Connect to the ESP32 device
    peripheral = btle.Peripheral(esp32_device)
    peripheral.setDelegate(MyDelegate())

    # Find the characteristic by UUID
    service = peripheral.getServiceByUUID(SERVICE_UUID)
    characteristic = service.getCharacteristics(CHARACTERISTIC_UUID)[0]

    # Enable notifications for the characteristic
    peripheral.writeCharacteristic(characteristic.valHandle + 1, b"\x01\x00", True)

    # Wait for notifications
    while True:
        if peripheral.waitForNotifications(1.0):
            continue

    # Disconnect from the ESP32 device
    peripheral.disconnect()

if __name__ == "__main__":
    receive_array()
