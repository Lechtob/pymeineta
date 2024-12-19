# API Reference

## `MeinETAClient` Class

### Initialization

```python
MeinETAClient(host: str, port: int)
```

**Parameters**:

- `host`(str): The hostname or IP address of the ETA Touch device.
- `port`(int): The port number for the REST API.

### Methods

`test_connection()`

```python
async def test_connection(self) -> bool
```

Tests the connectivity to the ETA Touch device.

**Returns**:

- `bool`:`True` if the connection is successful, `False` otherwise.

`get_sensor_dict()`

```python
async def get_sensors_dict(self) -> dict
```

Retrieves a dictionary of available sensors from the MeinETA device.

**Returns**:

- `dict`: A dictionary containing sensor information.

`get_data(sensor_id: str)`

```python
async def get_data(self, sensor_id: str) -> Tuple[Any, str]
```

Fetches the data for a specific sensor.

**Parameters**:

- `sensor_id`(str): The identifier for the sensor.

**Returns**:

- `Tuple[Any, str]`: A tuple containing the sensor value and its unit.

`set_parameter(parameter_name: str, value: Any)`

```python
async def set_parameter(self, parameter_name: str, value: Any) -> bool
```

Sets a parameter on the ETA Touch device.

**Parameters**:

- `parameter_name`(str): The name of the parameter to set.
- `value` (Any): The value to set for the parameter.

**Returns**:

- `bool`: `True` if the parameter was set successfully, `False` otherwise.
