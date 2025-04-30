import asyncio
from bleak import BleakClient, BleakError
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field

# Constants from your scripts
DEVICE_ADDRESS = "BE:27:08:00:32:5F" # Make sure this is correct
CHAR_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

# Payloads
def build_rgb_payload(r: int, g: int, b: int) -> bytearray:
    # Clamp values to 0-255
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return bytearray([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x00, 0xef])

def build_off_payload() -> bytearray:
    return bytearray([0x7e, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0xef]) # Corrected based on common patterns, adjust if needed

app = FastAPI()

class ColorRequest(BaseModel):
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)

async def send_payload(payload: bytearray):
    """Connects to the device and sends the given payload."""
    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            if client.is_connected:
                print(f"Connected to {DEVICE_ADDRESS}")
                await client.write_gatt_char(CHAR_UUID, payload, response=False) # Often response=False is needed
                print(f"Sent payload: {payload.hex()}")
            else:
                print(f"Failed to connect to {DEVICE_ADDRESS}")
                raise HTTPException(status_code=503, detail="Could not connect to the Bluetooth device.")
    except BleakError as e:
        print(f"BleakError: {e}")
        raise HTTPException(status_code=500, detail=f"Bluetooth error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")


@app.post("/set_color")
async def set_color_endpoint(color: ColorRequest):
    """Sets the color of the LED device."""
    payload = build_rgb_payload(color.r, color.g, color.b)
    await send_payload(payload)
    return {"message": f"Color set to R={color.r}, G={color.g}, B={color.b}"}

@app.post("/turn_off")
async def turn_off_endpoint():
    """Turns off the LED device."""
    payload = build_off_payload()
    await send_payload(payload)
    return {"message": "Device turned off"}

if __name__ == "__main__":
    print("Starting server...")
    # Consider adding host="0.0.0.0" to make it accessible on your network
    uvicorn.run(app, host="127.0.0.1", port=8000) 