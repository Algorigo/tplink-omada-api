from ..definitions import OmadaApiData
from enum import Enum, IntEnum


class NetworkPurpose(Enum):
    """Known network purposes for Omada devices."""

    INTERFACE = "interface"
    VLAN = "vlan"

    def from_str(value: str):
        """Convert a string to a NetworkPurpose."""
        for network_purpose in NetworkPurpose:
            if network_purpose.value == value:
                return network_purpose
        raise ValueError(f"Unknown network purpose: {value}")


class VLanType(IntEnum):
    """Known VLAN types for Omada devices."""

    SINGLE = 0
    MULTIPLE = 1


class OmadaNetwork(OmadaApiData):
    """Network settings of an Omada device."""

    @property
    def id(self) -> str:
        """Network ID."""
        return self._data.get("id")

    @property
    def site(self) -> str:
        """Site ID."""
        return self._data.get("site")

    @property
    def name(self) -> str:
        """Network name."""
        return self._data.get("name")

    @property
    def purpose(self) -> NetworkPurpose:
        """Network purpose."""
        return NetworkPurpose.from_str(self._data.get("purpose"))

    @property
    def interface_id(self) -> list:
        """Interface ID."""
        return self._data.get("interfaceId")

    @property
    def vlan_type(self) -> VLanType:
        """VLAN type."""
        return VLanType(self._data.get("vlanType"))

    @property
    def vlan(self) -> int:
        """VLAN ID."""
        return self._data.get("vlan")

    @property
    def gateway_subnet(self) -> str:
        """Gateway subnet."""
        return self._data.get("gatewaySubnet")

    @property
    def dhcp_settings(self) -> dict:
        """DHCP settings."""
        return self._data.get("dhcpSettings")

    @property
    def dhcp_guard(self) -> dict:
        """DHCP guard."""
        return self._data.get("dhcpGuard")

    @property
    def portal(self) -> bool:
        """Portal."""
        return self._data.get("portal")

    @property
    def access_control_rule(self) -> bool:
        """Access control rule."""
        return self._data.get("accessControlRule")

    @property
    def rate_limit(self) -> bool:
        """Rate limit."""
        return self._data.get("rateLimit")

    @property
    def all_lan(self) -> bool:
        """All LAN."""
        return self._data.get("allLan")

    @property
    def orig_name(self) -> str:
        """Original name."""
        return self._data.get("origName")

    @property
    def interface(self) -> bool:
        """Interface."""
        return self._data.get("interface")

    @property
    def primary(self) -> bool:
        """Primary."""
        return self._data.get("primary")
