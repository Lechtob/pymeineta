# Usage

## Quick Start

Get up and running with **pymeineta** in just a few steps:

1. **Install** the library (see [Installation](../README.md#installation)).
2. **Obtain** your API key from MeinETA.
3. **Initialize** the client and start interacting with your MeinETA devices.

## Basic Example

```python
import asyncio
from pymeineta import MeinETAClient

async def main():
    client = MeinETAClient(host="192.168.1.100", port=8080, api_key="YOUR_API_KEY")

    # Test connection
    if await client.test_connection():
        print("Connection successful!")

    # Retrieve sensor data
    sensors = await client.get_sensors_dict()
    print("Available Sensors:", sensors)

    # Fetch sensor value
    value, unit = await client.get_data("120/10101/0/0/12197")
    print(f"Sensor Value: {value} {unit}")

    # Set a parameter (example)
    success = await client.set_parameter("temperature_threshold", 75)
    if success:
        print("Parameter set successfully!")

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Features

### Asynchronous Communication

pymeineta leverages `aiohttp` for non-blocking interactions, ensuring efficient communication in asynchronous applications.

```python
import asyncio
from pymeineta import MeinETAClient

async def fetch_sensor_data():
    client = MeinETAClient(host="192.168.1.100", port=8080, api_key="YOUR_API_KEY")
    await client.connect()

    data = await client.get_data("sensor_id")
    await client.disconnect()
    return data

async def main():
    sensor_data = await fetch_sensor_data()
    print(sensor_data)

if __name__ == "__main__":
    asyncio.run(main())
```

### Error Handling

Utilize custom exceptions for robust error management, ensuring your application can gracefully handle issues.

```python
from pymeineta import MeinETAClient, ConnectionError, DataError

async def safe_fetch():
    client = MeinETAClient(host="192.168.1.100", port=8080, api_key="YOUR_API_KEY")
    try:
        await client.connect()
        data = await client.get_data("sensor_id")
    except ConnectionError:
        print("Failed to connect to MeinETA device!")
    except DataError:
        print("Error retrieving sensor data!")
    finally:
        await client.disconnect()

asyncio.run(safe_fetch())
```
