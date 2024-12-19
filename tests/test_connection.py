import pytest
import asyncio
from pymeineta import MeinETAClient, ConnectionError, ParsingError


@pytest.mark.asyncio
async def test_connection_success(aresponses):
    aresponses.add(
        "192.168.1.100:8080",
        "/user/menu",
        "GET",
        aresponses.Response(status=200),
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
async def test_request_timeout(aresponses):
    async def delayed_response(*args, **kwargs):
        await asyncio.sleep(15)  # Simulate delay
        return aresponses.Response(status=200)

    aresponses.add(
        "192.168.1.100:8080",
        "/user/menu",
        "GET",
        delayed_response,
    )
    client = MeinETAClient(host="192.168.1.100", port=8080, timeout=5)
    with pytest.raises(ConnectionError):
        await client.test_connection()
