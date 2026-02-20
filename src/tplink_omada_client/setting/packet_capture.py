from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, List
from ..devices import OmadaAccessPoint
from ..setting.ssid import Ssid


class DeviceType(Enum):
    EAP = "ap"


class PacketCaptureSource(ABC):

    @abstractmethod
    def get_device_type_str(self) -> str:
        pass


class PacketCaptureSourceEap(PacketCaptureSource):

    def __init__(self, ap: OmadaAccessPoint):
        self.ap = ap

    def get_device_type_str(self) -> str:
        return f"{DeviceType.EAP.value}/{self.ap.mac}"


class InterfaceType(Enum):
    WIRED = 0
    WIRELESS = 1


class WirelessChannel(Enum):
    GHZ_2_4 = 0
    GHZ_5 = 1
    GHZ_6 = 2


class PacketCaptureInterface(ABC):

    @abstractmethod
    def update_payload(self, payload: Dict) -> Dict:
        pass


class PacketCaptureInterfaceWired(PacketCaptureInterface):

    def update_payload(self, payload: Dict) -> Dict:
        payload["interfaceType"] = InterfaceType.WIRED.value
        payload["interfaceName"] = "ETH(PoE)"
        return payload


class PacketCaptureInterfaceWireless(PacketCaptureInterface):

    def __init__(self, ssid: Ssid, channel: WirelessChannel):
        self.ssid = ssid
        self.channel = channel

    def update_payload(self, payload: Dict) -> Dict:
        payload["interfaceType"] = InterfaceType.WIRELESS.value
        payload["interfaceName"] = self.ssid.ssid_name
        payload["channel"] = self.channel.value
        return payload


class Filter(ABC):
    @abstractmethod
    def get_filter_str(self) -> str:
        pass


class GroupFilter(Filter, ABC):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    @abstractmethod
    def get_splitter(self) -> str:
        pass

    def get_filter_str(self) -> str:
        return self.get_splitter().join(
            [
                (
                    f"({f.get_filter_str()})"
                    if isinstance(f, GroupFilter)
                    else f.get_filter_str()
                )
                for f in self.filters
            ]
        )


class AndFilter(GroupFilter):

    def get_splitter(self) -> str:
        return " and "


class OrFilter(GroupFilter):

    def get_splitter(self) -> str:
        return " or "


class SourceIpFilter(Filter):

    def __init__(self, ip: str):
        self.ip = ip

    def get_filter_str(self) -> str:
        return f"src {self.ip}"


class DestinationIpFilter(Filter):

    def __init__(self, ip: str):
        self.ip = ip

    def get_filter_str(self) -> str:
        return f"dst {self.ip}"


class Protocols(Enum):
    TCP = "tcp"
    UDP = "udp"


class SourcePortFilter(Filter):

    def __init__(self, protocol: Protocols, port: int):
        self.protocol = protocol
        self.port = port

    def get_filter_str(self) -> str:
        return f"{self.protocol.value} src port {self.port}"


class DestinationPortFilter(Filter):

    def __init__(self, protocol: Protocols, port: int):
        self.protocol = protocol
        self.port = port

    def get_filter_str(self) -> str:
        return f"{self.protocol.value} dst port {self.port}"
