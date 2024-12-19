# MeinETA Python Client

[![TestPyPI - Python Version](https://img.shields.io/pypi/pyversions/meineta)](https://pypi.org/project/meineta/)
[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/username/meineta/actions)
[![Build Status](https://github.com/username/meineta/actions/workflows/ci.yml/badge.svg)](https://github.com/username/meineta/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/MIT)

## Overview

`meinETA` is an asynchronous Python client for interacting with the MeinETA local REST API. This library enables users to:

- Check the connectivity of MeinETA devices.
- Retrieve and parse sensor data.
- Access and manage the menu structure of available sensors.

The library is designed to be lightweight, efficient, and easy to integrate into your Python projects.

---

## Installation

To install the library from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps meineta
```

Once the package is officially released, use:

```bash
pip install meineta
```

---

## Usage

### Basic Example

```python
import asyncio
from meineta import MeinETAClient

async def main():
    client = MeinETAClient(host="192.168.1.100", port=8080)

    # Test connection
    if await client.test_connection():
        print("Connection successful!")

    # Get sensor dictionary
    sensors = await client.get_sensors_dict()
    print(sensors)

    # Fetch sensor data
    value, unit = await client.get_data("120/10101/0/0/12197")
    print(f"Sensor value: {value} {unit}")

asyncio.run(main())
```

---

## Features

- **Asynchronous Communication**: Built with `aiohttp` for non-blocking interactions.
- **Error Handling**: Custom exceptions for robust error management.
- **Retry Mechanism**: Retries for transient failures (e.g., network issues).
- **Caching**: Caches sensor mappings for faster data retrieval.

---

## Development

### Running Tests

The project uses `pytest` for testing. To run the tests:

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed explanation of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Links

- [MeinETA Documentation](https://www.example.com/docs)
- [TestPyPI Package](https://test.pypi.org/project/meineta/)
- [GitHub Repository](https://github.com/username/meineta)

---

## Acknowledgements

Special thanks to the MeinETA team for their support and documentation.

