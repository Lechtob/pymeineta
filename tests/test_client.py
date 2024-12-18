import pytest
import aresponses
from pymeineta import MeinETAClient, ParsingError

@pytest.mark.asyncio
async def test_connection_success(aresponses):
    aresponses.add(
        "192.168.1.100:8080", "/user/menu", "GET",
        aresponses.Response(status=200, text="<eta><menu></menu></eta>")
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    result = await client.test_connection()
    assert result is True

@pytest.mark.asyncio
async def test_connection_failure(aresponses):
    aresponses.add(
    "192.168.1.100:8080",
    "/user/menu",
    "GET",
    aresponses.Response(status=404),
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    with pytest.raises(ConnectionError):
        await client.test_connection()

@pytest.mark.asyncio
async def test_get_sensors_dict_success(aresponses):
    mock_xml = """<eta><menu>
    <fub name="FBH" uri="/120/10101">
      <object name="Außentemperatur" uri="/120/10101/0/0/12197"/>
    </fub>
    </menu></eta>"""
    aresponses.add(
        "192.168.1.100:8080", "/user/menu", "GET",
        aresponses.Response(status=200, text=mock_xml)
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    sensors = await client.get_sensors_dict()
    assert "fbh_außentemperatur" in sensors
    assert sensors["fbh_außentemperatur"] == "/120/10101/0/0/12197"

@pytest.mark.asyncio
async def test_get_sensors_dict_parsing_error(aresponses):
    invalid_xml = "<invalid><xml></xml>"
    aresponses.add(
        "192.168.1.100:8080", "/user/menu", "GET",
        aresponses.Response(status=200, text=invalid_xml),
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    with pytest.raises(ParsingError):
        await client.get_sensors_dict()

@pytest.mark.asyncio
async def test_get_data_success(aresponses):
    mock_xml = """<eta>
      <value unit="°C" decPlaces="1" scaleFactor="10" strValue="15.0">150</value>
    </eta>"""
    aresponses.add(
        "192.168.1.100:8080", "/user/var/120/10101/0/0/12197", "GET",
        aresponses.Response(status=200, text=mock_xml)
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    value, unit = await client.get_data("120/10101/0/0/12197")
    assert value == 15.0
    assert unit == "°C"

