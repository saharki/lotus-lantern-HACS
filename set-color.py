import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = "BE:27:08:00:32:5F"
CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

def build_rgb_payload(r, g, b):
    return bytearray([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x00, 0xef])

async def set_color(r, g, b):
    async with BleakClient(DEVICE_ADDRESS) as client:
        print("Connected")
        await client.write_gatt_char(CHAR_UUID, build_rgb_payload(r, g, b))

# get rgb from parameters
r, g, b = sys.argv[1], sys.argv[2], sys.argv[3]

asyncio.run(set_color(r, g, b))