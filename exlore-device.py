import asyncio
from bleak import BleakScanner, BleakClient

async def explore_device(address, name):
    print(f"\n🔎 Connecting to {name or '(Unknown)'} [{address}]...")
    try:
        async with BleakClient(address, timeout=10.0) as client:
            services = await client.get_services()
            for service in services:
                print(f"  📦 Service: {service.uuid}")
                for char in service.characteristics:
                    props = ', '.join(char.properties)
                    if "write" in char.properties or "write-without-response" in char.properties:
                        print(f"    ✨ Writable Characteristic: {char.uuid} | Properties: [{props}]")
                    else:
                        print(f"    └─ Characteristic: {char.uuid} | Properties: [{props}]")
    except Exception as e:
        print(f"  ❌ Failed to connect: {e}")

asyncio.run(explore_device("BE:27:08:00:32:5F", "Lotus LED"))
