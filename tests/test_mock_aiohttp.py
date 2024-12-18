from unittest.mock import AsyncMock, patch
import pytest
from pymeineta import MeinETAClient, ConnectionError


@pytest.mark.asyncio
async def test_connection_success():
    # Mock für die Antwort
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.text = AsyncMock(return_value="<eta><menu></menu></eta>")

    # Mock für ClientSession
    mock_session = AsyncMock()
    mock_session.get.return_value.__aenter__.return_value = mock_resp

    with patch("aiohttp.ClientSession", return_value=mock_session):
        client = MeinETAClient(host="192.168.1.100", port=8080)
        result = await client.test_connection()
        assert result is True

