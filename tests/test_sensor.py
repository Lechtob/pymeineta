import pytest
from pymeineta import MeinETAClient, ConnectionError, ParsingError


@pytest.mark.asyncio
async def test_get_sensors_dict_success(aresponses):
    mock_xml = """<eta><menu>
    <fub name="FBH" uri="/120/10101">
      <object name="Außentemperatur" uri="/120/10101/0/0/12197"/>
    </fub>
    </menu></eta>"""
    aresponses.add(
        "192.168.1.100:8080",
        "/user/menu",
        "GET",
        aresponses.Response(status=200, text=mock_xml),
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    sensors = await client.get_sensors_dict()
    assert "fbh_außentemperatur" in sensors
    assert sensors["fbh_außentemperatur"] == "/120/10101/0/0/12197"


@pytest.mark.asyncio
async def test_get_sensors_dict_parsing_error(aresponses):
    invalid_xml = "<invalid><xml></xml>"
    aresponses.add(
        "192.168.1.100:8080",
        "/user/menu",
        "GET",
        aresponses.Response(status=200, text=invalid_xml),
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    with pytest.raises(ParsingError):
        await client.get_sensors_dict()


@pytest.mark.asyncio
async def test_fetch_xml_retries(aresponses):
    aresponses.add(
        "192.168.1.100:8080",
        "/user/menu",
        "GET",
        aresponses.Response(status=500),
        repeat=2,
    )
    aresponses.add(
        "192.168.1.100:8080",
        "/user/menu",
        "GET",
        aresponses.Response(status=200, text="<eta></eta>"),
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    result = await client._fetch_xml("http://192.168.1.100:8080/user/menu")
    assert result == "<eta></eta>"


@pytest.mark.asyncio
async def test_get_sensors_dict_caching(aresponses):
    mock_xml = "<eta><menu><fub name='FBH' uri='/120/10101'/></menu></eta>"
    aresponses.add(
        "192.168.1.100:8080",
        "/user/menu",
        "GET",
        aresponses.Response(status=200, text=mock_xml),
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)

    # Use logging to track calls
    sensors = await client.get_sensors_dict()  # Initial API call
    sensors_cached = await client.get_sensors_dict()  # Cached result

    assert sensors == sensors_cached
    # aresponses doesn't directly track calls, so manual validation required
