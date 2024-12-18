import asyncio
import logging
from typing import Dict, Tuple, Any, Optional
import aiohttp
import xmltodict
from xml.parsers.expat import ExpatError

from .exceptions import MeinETAError, ConnectionError, ParsingError, InvalidResponseError

logger = logging.getLogger(__name__)

class MeinETAClient:
    """Asynchronous client for the meinETA local REST API.
    
    This client provides the core functionality to:
    - Check connectivity to the meinETA device.
    - Retrieve available sensors (URIs) from the menu structure.
    - Fetch individual sensor data points by URI.
    """

    def __init__(self, host: str, port: int = 80, timeout: int = 10) -> None:
        """
        Initialize the meinETA client.

        :param host: Hostname or IP address of the meinETA device.
        :param port: Port number where the meinETA API is accessible (default 80).
        :param timeout: Request timeout in seconds.
        """
        self._host = host
        self._port = port
        self._timeout = timeout

        # Base URLs:
        self._menu_url = f"http://{self._host}:{self._port}/user/menu"
        self._var_url = f"http://{self._host}:{self._port}/user/var/"

        # Caching for sensors
        self._sensors_cache: Optional[Dict[str, str]] = None

    async def test_connection(self) -> bool:
        """Check if the device is reachable and responsive.

        :return: True if connection succeeds, False otherwise.
        :raises ConnectionError: If request fails or returns a non-200 status.
        """
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self._timeout)) as session:
                async with session.get(self._menu_url) as resp:
                    if resp.status == 200:
                        logger.info("Connection test successful.")
                        return True
                    else:
                        raise ConnectionError(f"Connection test failed with status {resp.status}", error_code=resp.status)
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            logger.error(f"Connection test failed due to network error: {err}")
            raise ConnectionError(f"Connection test failed due to network error: {err}") from err

    async def get_sensors_dict(self) -> Dict[str, str]:
        """Retrieve a dictionary of all available sensors mapped to their URIs."""
        if self._sensors_cache:
            logger.debug("Returning cached sensors.")
            return self._sensors_cache

        xml_data = await self._fetch_xml(self._menu_url)

        try:
            root = xmltodict.parse(xml_data)
            raw_dict = root["eta"]["menu"]["fub"]
        except (KeyError, ValueError, ExpatError) as err:
            logger.error(f"Failed to parse menu structure: {err}")
            raise ParsingError("Failed to parse menu structure", details=xml_data) from err

        uri_dict = {}
        self._evaluate_xml_dict(raw_dict, uri_dict)
        self._sensors_cache = uri_dict
        return uri_dict

    async def get_data(self, uri: str) -> Tuple[Any, Optional[str]]:
        """Fetch data for a given sensor URI."""
        xml_data = await self._fetch_xml(self._var_url + uri)
        try:
            root = xmltodict.parse(xml_data)
            data = root["eta"]["value"]
            return self._parse_data(data)
        except (KeyError, ValueError, ExpatError) as err:
            logger.error(f"Failed to parse data for URI {uri}: {err}")
            raise ParsingError("Failed to parse data", details=xml_data) from err


    async def _fetch_xml(self, url: str) -> str:
        """Fetch XML data from a given URL."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self._timeout)) as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            return await resp.text()
                        else:
                            logger.warning(f"Attempt {attempt + 1}: Failed with status {resp.status}")
                            raise InvalidResponseError(
                                f"Failed request with status {resp.status}", error_code=resp.status
                            )
            except (aiohttp.ClientError, asyncio.TimeoutError) as err:
                logger.warning(f"Attempt {attempt + 1}: Network error: {err}")
                if attempt == max_retries - 1:
                    raise ConnectionError(f"Request to {url} failed after {max_retries} attempts.") from err


    def _evaluate_xml_dict(self, xml_dict: Any, uri_dict: Dict[str, str], prefix: str = "") -> None:
        """Evaluate XML recursively to build URI mappings."""
        if isinstance(xml_dict, list):
            for child in xml_dict:
                self._evaluate_xml_dict(child, uri_dict, prefix)
        elif isinstance(xml_dict, dict):
            name = xml_dict.get("@name", "unknown").lower().replace(" ", "_")
            new_prefix = f"{prefix}_{name}".strip("_")
            uri = xml_dict.get("@uri")
            if uri:
                uri_dict[new_prefix] = uri
            if "object" in xml_dict:
                self._evaluate_xml_dict(xml_dict["object"], uri_dict, new_prefix)


    def _parse_data(self, data: Dict[str, Any]) -> Tuple[Any, Optional[str]]:
        """Parse a single data value from the meinETA API response.

        :param data: The dict representing <value> from the parsed XML.
        :return: (value, unit)
        """
        unit = data.get("@unit")
        text_value = data.get("#text")

        float_units = {
            "%", "A", "Hz", "Ohm", "Pa", "U/min", "V", "W", "W/m²", "bar",
            "kW", "kWh", "kg", "l", "l/min", "mV", "m²", "s", "°C"
        }

        if unit in float_units and text_value is not None:
            try:
                scale_factor = int(data.get("@scaleFactor", "1"))
                decimal_places = int(data.get("@decPlaces", "0"))
                raw_value = float(text_value)
                value = round(raw_value / scale_factor, decimal_places)
                return value, unit
            except (ValueError, TypeError):
                logger.warning(f"Failed to parse value for data: {data}")

        # Fallback for non-float or parsing failure
        return data.get("@strValue"), unit