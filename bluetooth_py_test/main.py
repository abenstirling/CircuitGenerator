import asyncio
from bleak import BleakScanner

async def receive_data():
    async with BleakScanner() as scanner:
        while True:
            await scanner.start()
            scanner.register_detection_callback(discovered_device)
            await asyncio.sleep(5)
            await scanner.stop()

def discovered_device(device, advertisement_data):
    print(f"Discovered device {device.address}: {device.name} @ RSSI: {device.rssi} (Advertisement Data: {advertisement_data})")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(receive_data())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()