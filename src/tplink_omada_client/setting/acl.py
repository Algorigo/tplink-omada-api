from typing import Any, Dict, Optional, List
from .policy import *


class AclType(Enum):
    gateway = 0
    switch = 1
    eap = 2


class Protocol(Enum):
    tcp = 6
    udp = 17
    icmp = 1
    ggp = 3
    ah = 51
    ax_25 = 93
    dccp = 33
    egp = 8
    eigrp = 88
    encap = 98
    esp = 50
    ether_ip = 97
    fc = 133
    gre = 47
    hmp = 20
    idrp_cmtp = 38
    idrp = 45
    igp = 9
    ip_ipencap = 4
    ip_comp = 108
    ipip = 94
    is_is = 124
    iso_tp4 = 29
    l2tp = 115
    mobility_header = 135
    mpls_in_ip = 137
    ospf = 89
    pim = 103
    pup = 12
    rdp = 27
    rsvp = 46
    sctp = 132
    skip = 57
    st = 5
    udp_lite = 136
    vmtp = 81
    vrrp = 112
    xns_idp = 22
    xtp = 36
    manet = 138
    hip = 139
    shim6 = 140
    wesp = 141
    rohc = 142
    icmpv6 = 58

    def from_values(values: List[int]) -> List["Protocol"]:
        if len(values) == 1 and values[0] == 256:
            return [protocol for protocol in Protocol]

        return [Protocol(value) for value in values]

    def to_values(protocols: List["Protocol"]) -> List[int]:
        print(
            "protocols:",
            protocols,
            len(protocols),
            len([protocol for protocol in Protocol]),
            len(Protocol),
        )
        return (
            [256]
            if len(protocols) >= len(Protocol)
            else [protocol.value for protocol in protocols]
        )


class AclSourceType(Enum):
    network = 0
    ip_group = 1
    ip_port_group = 2
    ssid = 4
    ip_v6_group = 6
    ip_v6_port_group = 7


class AclDestinationType(Enum):
    network = 0
    ip_group = 1
    ip_port_group = 2
    ip_v6_group = 6
    ip_v6_port_group = 7


class Acl:
    @staticmethod
    def new_acl(
        type: AclType,
        name: str,
        status: bool,
        policy: Policy | str,
        protocols: List[Protocol] | List[str],
        source_type: AclSourceType | str,
        source_ids: List[str],
        destination_type: AclDestinationType | str,
        destination_ids: List[str],
    ) -> "Acl":
        map: Dict[str, Any] = {
            "type": type.value,
            "name": name,
            "status": status,
            "policy": policy.value if isinstance(policy, Policy) else policy,
            "protocols": [p.value if isinstance(p, Protocol) else p for p in protocols],
            "sourceType": (
                source_type.value
                if isinstance(source_type, AclSourceType)
                else source_type
            ),
            "sourceIds": source_ids,
            "destinationType": (
                destination_type.value
                if isinstance(destination_type, AclDestinationType)
                else destination_type
            ),
            "destinationIds": destination_ids,
        }
        return Acl(map)

    def __init__(self, map: Dict[str, Any]):
        self.id: Optional[str] = map.get("id")
        self.type: AclType = AclType(map["type"])
        self.index: Optional[int] = map.get("index")
        self.site_id: Optional[str] = map.get("siteId")
        self.name: str = map["name"]
        self.status: bool = map["status"]
        self.policy: Policy = (
            Policy(map["policy"])
            if not isinstance(map["policy"], Policy)
            else map["policy"]
        )
        self.protocols: List[Protocol] = (
            map["protocols"]
            if len(map["protocols"]) > 0 and isinstance(map["protocols"], Protocol)
            else Protocol.from_values(map["protocols"])
        )
        self.source_type: AclSourceType = (
            AclSourceType(map["sourceType"])
            if not isinstance(map["sourceType"], AclSourceType)
            else map["sourceType"]
        )
        self.source_ids: List[str] = map["sourceIds"]
        self.destination_type: AclDestinationType = (
            AclDestinationType(map["destinationType"])
            if not isinstance(map["destinationType"], AclDestinationType)
            else map["destinationType"]
        )
        self.destination_ids: List[str] = map["destinationIds"]

    def to_map(self) -> Dict[str, Any]:
        map: Dict[str, Any] = {
            "type": self.type.value,
            "name": self.name,
            "status": self.status,
            "policy": self.policy.value,
            "protocols": Protocol.to_values(self.protocols),
            "sourceType": self.source_type.value,
            "sourceIds": self.source_ids,
            "destinationType": self.destination_type.value,
            "destinationIds": self.destination_ids,
        }
        if self.id is not None:
            map["id"] = self.id
        if self.index is not None:
            map["index"] = self.index
        if self.site_id is not None:
            map["siteId"] = self.site_id

        return map

    def __repr__(self) -> str:
        return f"Acl(id={self.id}, index={self.index}, type={self.type}, source_ids={self.source_ids}, destination_ids={self.destination_ids}, protocols={self.protocols})"
