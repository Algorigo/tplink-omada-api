from enum import IntEnum
from ..definitions import OmadaApiData


class InterfaceType(IntEnum):
    """Known types of interface."""

    WAN = 0
    LAN = 1


class IpMacBinding(OmadaApiData):
    """IP/MAC binding."""

    @property
    def id(self) -> str:
        """ID."""
        return self._data.get("id")

    @property
    def description(self) -> str:
        """Description."""
        return self._data.get("description")

    @property
    def mac(self) -> str:
        """MAC address."""
        return self._data.get("mac")

    @property
    def ip(self) -> str:
        """IP address."""
        return self._data.get("ip")

    @property
    def status(self) -> bool:
        """Status."""
        return self._data.get("status")

    @property
    def interface_type(self) -> InterfaceType:
        """Interface type."""
        return InterfaceType(self._data.get("interfaceType"))

    @property
    def interface_id(self) -> str:
        """Interface ID."""
        return self._data.get("interfaceId")
