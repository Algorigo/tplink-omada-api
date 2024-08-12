from abc import ABC
from typing import Any
from enum import Enum, IntEnum
import re


class PortType(Enum):
    """Known port types for Omada devices."""

    SFP_PLUS_WAN = "SFP+ WAN"
    SFP_PLUS_WAN_LAN = "SFP+ WAN/LAN"
    SFP_WAN_LAN = "SFP WAN/LAN"
    WAN_LAN = "WAN/LAN"
    WAN = "WAN"
    LAN = "LAN"

    def from_str(value: str):
        """Convert a string to a PortType."""
        for port_type in PortType:
            if port_type.value == value:
                return port_type
        raise ValueError(f"Unknown port type: {value}")


class ConnectionType(IntEnum):
    DYNAMIC_IP = 0
    STATIC_IP = 1
    PPPOE = 2
    L2TP = 3
    PPTP = 4


class WanLanPort(ABC):
    """Base representation of WAN/LAN port data."""

    def __init__(self, port_uuid: str, port_name: str):
        self._port_uuid = port_uuid
        self._port_name = port_name
        print("port_name:", port_name)
        match = re.match(r"([^0-9]+)([0-9]+)$", self.port_name)
        if match is not None:
            self._port_type = PortType.from_str(match[1])
            self._port_number = int(re.match(r"([^0-9]+)([0-9]+)$", self.port_name)[2])
        else:
            self._port_type = PortType.from_str(port_name)
            self._port_number = 0

    def __repr__(self) -> str:
        repr_str = self.__class__.__name__
        repr_str += "{"
        for name in self.__dir__():
            if not name.startswith("_") and name != "raw_data":
                repr_str += f"{name}={getattr(self, name)},"
        repr_str += "}"
        return repr_str

    @property
    def port_uuid(self) -> str:
        """Port UUID."""
        return self._port_uuid

    @property
    def port_name(self) -> str:
        """Port name."""
        return self._port_name

    @property
    def port_type(self) -> PortType:
        """Port type."""
        return self._port_type

    @property
    def port_number(self) -> int:
        """Port number."""
        return self._port_number


class WanPort(WanLanPort):
    """Details of a WAN port."""

    def __init__(self, data: dict[str, Any]):
        super().__init__(data["portUuid"], data["portName"])
        self._data = data

    @property
    def ip_v6_enable(self) -> int:
        """Indicates if the port is enabled."""
        return self._data.get("enable")

    @property
    def prefix(self) -> str:
        """Prefix of the port."""
        return self._data.get("prefix")

    @property
    def connection_type(self) -> ConnectionType:
        """Type of the port."""
        return ConnectionType(self._data.get("type"))
