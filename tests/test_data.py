import pytest
from pymeineta import MeinETAClient, ConnectionError, ParsingError


@pytest.mark.asyncio
async def test_get_data_success(aresponses):
    mock_xml = """<eta>
      <value unit="°C" decPlaces="1" scaleFactor="10" strValue="15.0">150</value>
    </eta>"""
    aresponses.add(
        "192.168.1.100:8080",
        "/user/var/120/10101/0/0/12197",
        "GET",
        aresponses.Response(status=200, text=mock_xml),
    )
    client = MeinETAClient(host="192.168.1.100", port=8080)
    value, unit = await client.get_data("120/10101/0/0/12197")
    assert value == 15.0
    assert unit == "°C"
