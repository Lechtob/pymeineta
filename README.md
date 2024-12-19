# pymeineta

[![Python Version](https://img.shields.io/pypi/pyversions/pymeineta)](https://pypi.org/project/pymeineta/)
[![Coverage Status](https://coveralls.io/repos/github/lechtob/pymeineta/badge.svg?branch=main)](https://coveralls.io/github/lechtob/pymeineta?branch=main)
[![Build Status](https://github.com/lechtob/pymeineta/actions/workflows/ci.yml/badge.svg)](https://github.com/lechtob/pymeineta/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Basic Example](#basic-example)
  - [Advanced Features](#advanced-features)
- [Features](#features)
- [Supported Python Versions](#supported-python-versions)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Testing](#testing)
- [License](#license)
- [Links](#links)
- [Support](#support)

---

## Overview

**pymeineta** is an asynchronous Python library designed to seamlessly interact with the MeinETA REST API. It provides functionalities such as reading sensor values from the boiler and setting various parameters, making it a robust tool for managing and monitoring MeinETA devices within your Python projects.

---

## Installation

### Official Release

To install the latest stable version of `pymeineta` from PyPI:

```bash
pip install pymeineta
```

### Test Installation

For testing purposes, you can install the library from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps pymeineta
```

---

## Quick Start

Get up and running with **pymeineta** in just a few steps:

1. **Install** the library (see [Installation](#installation)).
2. **Obtain** your API key from MeinETA.
3. **Initialize** the client and start interacting with your MeinETA devices.

---

## Usage

### Basic Example

Here's a simple example to demonstrate how to use `pymeineta` to connect to a MeinETA device, check connectivity, retrieve sensor data, and set parameters.

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

### Advanced Features

#### Asynchronous Communication

`pymeineta` leverages `aiohttp` for non-blocking interactions, ensuring efficient communication in asynchronous applications.

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

#### Error Handling

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

---

## Features

- **Asynchronous Communication**: Built with `aiohttp` for efficient, non-blocking interactions.
- **Error Handling**: Custom exceptions for robust error management.
- **Retry Mechanism**: Automatically retries transient failures such as network issues.
- **Caching**: Caches sensor mappings for faster data retrieval.
- **Parameter Management**: Easily set and manage device parameters.
- **Easy Integration**: Simple to integrate into existing Python projects.

---

## Supported Python Versions

`pymeineta` supports Python 3.8 and above.

---

## Configuration

**pymeineta** uses environment variables to manage sensitive information like API keys. You can set them up as follows:

```bash
export MEINETA_API_KEY='your_api_key_here'
export MEINETA_HOST='192.168.1.100'
export MEINETA_PORT=8080
```

Alternatively, you can create a `.env` file in your project root:

```plaintext
# .env
MEINETA_API_KEY=your_api_key_here
MEINETA_HOST=192.168.1.100
MEINETA_PORT=8080
```

Then, use a library like `python-dotenv` to load these variables:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('MEINETA_API_KEY')
host = os.getenv('MEINETA_HOST')
port = os.getenv('MEINETA_PORT')
```

---

## Documentation

Comprehensive documentation and guides are available in the [docs/](docs/) directory or online at [pymeineta Documentation](https://github.com/Lechtob/pymeineta/docs/).

- **API Reference**: Detailed descriptions of all available classes and methods.
- **Example Applications**: Practical code examples demonstrating library usage.
- **FAQ**: Frequently asked questions and their answers.

---

## Contributing

Contributions are welcome! Please follow these steps to contribute to `pymeineta`:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Implement your changes** and add corresponding tests.
4. **Ensure all tests pass** and the code is formatted:

    ```bash
    pre-commit run --all-files
    ```

5. **Commit and push** your changes:

    ```bash
    git commit -m "Add feature: Your feature description"
    git push origin feature/your-feature-name
    ```

6. **Create a Pull Request** on GitHub.

For more details, refer to our [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Testing

The project uses `pytest` for testing. To run the tests:

```bash
pytest tests/
```

Ensure all development dependencies are installed:

```bash
pip install -r requirements-dev.txt
```

Automated tests are executed on every push and pull request via GitHub Actions.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Links

- [pymeineta Documentation](https://github.com/lechtob/pymeineta/docs/)
- [TestPyPI Package](https://test.pypi.org/project/pymeineta/)
- [GitHub Repository](https://github.com/lechtob/pymeineta)
- [PyPI Package](https://pypi.org/project/pymeineta/)

---

## Support

If you have any questions or encounter issues, please open an [Issue](https://github.com/lechtob/pymeineta/issues) on GitHub or contact us directly at [tobiaslechenauer@gmail.com](mailto:tobiaslechenauer@gmail.com).

---
