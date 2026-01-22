from typing import Dict, Any, List, Optional
from enum import Enum


class GroupType(Enum):
    ip_group = 0
    ip_port_group = 1
    ipv6_port_group = 2
    ipv6_group = 3
    mac_group = 4
    location_group = 5
    domain_group = 7


class PortType(Enum):
    ip_port_range = 0
    ip_port_mask = 1


class IpListItem:
    @staticmethod
    def new(ip: str, mask: int, description: Optional[str] = None) -> "IpListItem":
        map: Dict[str, Any] = {
            "ip": ip,
            "mask": str(mask),
        }
        if description is not None:
            map["description"] = description
        return IpListItem(map)

    def __init__(self, map: Dict[str, Any]):
        self.ip: str = map["ip"]
        self.mask: int = int(map["mask"])
        self.description: Optional[str] = map.get("description")

    def to_map(self) -> Dict[str, Any]:
        return {"ip": self.ip, "mask": str(self.mask), "description": self.description}


class IpV6ListItem:
    @staticmethod
    def new(
        ipv6: str, prefix: str, description: Optional[str] = None
    ) -> "IpV6ListItem":
        map: Dict[str, Any] = {
            "ip": ipv6,
            "prefix": prefix,
        }
        if description is not None:
            map["description"] = description
        return IpV6ListItem(map)

    def __init__(self, map: Dict[str, Any]):
        self.ipv6: str = map["ip"]
        self.prefix: int = int(map["prefix"])
        self.description: Optional[str] = map.get("description")

    def to_map(self) -> Dict[str, Any]:
        return {
            "ip": self.ipv6,
            "prefix": str(self.prefix),
            "description": self.description,
        }


class PortType(Enum):
    ip_port_range = 0
    ip_port_mask = 1


class PortRangeItem:
    def __init__(self, port_str: str):
        parts = port_str.split("-")
        self.start_port: int = int(parts[0])
        self.end_port: int = int(parts[1]) if len(parts) > 1 else self.start_port

    def __str__(self):
        return (
            f"{self.start_port}-{self.end_port}"
            if self.start_port != self.end_port
            else f"{self.start_port}"
        )


class PortMaskItem:
    @staticmethod
    def new(port: int, mask: int) -> "PortMaskItem":
        map: Dict[str, Any] = {
            "port": port,
            "mask": hex(mask),
        }
        return PortMaskItem(map)

    def __init__(self, map: Dict[str, Any]):
        self.port: int = int(map["port"])
        self.mask: int = int(map["mask"], 16)

    def to_map(self) -> Dict[str, Any]:
        return {"port": self.port, "mask": hex(self.mask)}


class Group:
    def __init__(self, map: Dict[str, Any], group_type: Optional[GroupType] = None):
        self.group_id: Optional[str] = map.get("groupId")
        self.site_id: Optional[str] = map.get("site")
        self.name: str = map["name"]
        self.built_in: bool = map.get("buildIn", False)
        self.count: int = map["count"]
        self.type: GroupType = (
            group_type if group_type is not None else GroupType(map["type"])
        )
        self.resource: Optional[int] = map.get("resource")

    def to_map(self) -> Dict[str, Any]:
        return {
            "groupId": self.group_id,
            "site": self.site_id,
            "name": self.name,
            "buildIn": self.built_in,
            "count": self.count,
            "type": self.type.value,
            "resource": self.resource,
        }

    def __repr__(self) -> str:
        return self.name

    def __str__(self):
        return self.__repr__()


class IpGroup(Group):
    @staticmethod
    def new(name: str, ip_list: List[IpListItem] | List[Dict[str, Any]]) -> "IpGroup":
        map: Dict[str, Any] = {
            "name": name,
            "ipList": ip_list,
            "count": len(ip_list),
        }
        return IpGroup(map)

    def __init__(self, map: Dict[str, Any]):
        super().__init__(map, GroupType.ip_group)
        self.ip_list: List[IpListItem] = [
            item if isinstance(item, IpListItem) else IpListItem(item)
            for item in map.get("ipList", [])
        ]

    def to_map(self) -> Dict[str, Any]:
        return super().to_map() | {"ipList": [item.to_map() for item in self.ip_list]}

    def __eq__(self, value):
        return isinstance(value, IpGroup) and self.to_map() == value.to_map()

    def __repr__(self):
        return f"IpGroup(name={self.name}, ip_list={self.ip_list})"

    def __str__(self):
        return self.__repr__()


class IpV6Group(Group):
    @staticmethod
    def new(
        name: str,
        ipv6_list: List[IpV6ListItem] | List[Dict[str, Any]],
    ) -> "IpV6Group":
        map: Dict[str, Any] = {
            "name": name,
            "ipv6List": ipv6_list,
            "count": len(ipv6_list),
        }
        return IpV6Group(map)

    def __init__(self, map: Dict[str, Any]):
        super().__init__(map, GroupType.ipv6_group)
        self.ipv6_list: List[IpV6ListItem] = [
            item if isinstance(item, IpV6ListItem) else IpV6ListItem(item)
            for item in map.get("ipv6List", [])
        ]

    def to_map(self) -> Dict[str, Any]:
        return super().to_map() | {
            "ipv6List": [item.to_map() for item in self.ipv6_list]
        }

    def __eq__(self, value):
        return isinstance(value, IpV6Group) and self.to_map() == value.to_map()

    def __repr__(self):
        return f"IpV6Group(name={self.name}, ipv6_list={self.ipv6_list})"

    def __str__(self):
        return self.__repr__()


class IpPortGroup(Group):
    @staticmethod
    def new(
        name: str,
        ip_list: List[IpListItem] | List[Dict[str, Any]],
        port_type: PortType,
        port_list: List[PortRangeItem] | List[str] = [],
        port_mask_list: List[PortMaskItem] | List[Dict[str, Any]] = [],
    ) -> "IpPortGroup":
        if len(port_list) == 0 and len(port_mask_list) == 0:
            raise ValueError("Either port_list or port_mask_list must be provided")

        map: Dict[str, Any] = {
            "name": name,
            "ipList": ip_list,
            "count": max(len(ip_list), len(port_list), len(port_mask_list)),
            "portType": port_type.value,
            "portList": port_list,
            "portMaskList": port_mask_list,
        }
        return IpPortGroup(map)

    def __init__(self, map: Dict[str, Any]):
        super().__init__(map, GroupType.ip_port_group)
        self.ip_list: List[IpListItem] = [
            item if isinstance(item, IpListItem) else IpListItem(item)
            for item in map.get("ipList", [])
        ]
        self.port_type: PortType = PortType(map.get("portType", 0))
        self.port_list: List[PortRangeItem] = [
            item if isinstance(item, PortRangeItem) else PortRangeItem(item)
            for item in map.get("portList", [])
        ]
        self.port_mask_list: List[PortMaskItem] = [
            item if isinstance(item, PortMaskItem) else PortMaskItem(item)
            for item in map.get("portMaskList", [])
        ]

    def to_map(self) -> Dict[str, Any]:
        return super().to_map() | {
            "ipList": [item.to_map() for item in self.ip_list],
            "portType": self.port_type.value,
            "portList": [item.__str__() for item in self.port_list],
            "portMaskList": [item.to_map() for item in self.port_mask_list],
        }

    def __eq__(self, value):
        return isinstance(value, IpPortGroup) and self.to_map() == value.to_map()

    def __repr__(self):
        return f"IpPortGroup(name={self.name}, ip_list={self.ip_list}, port_type={self.port_type}, port_list={self.port_list}, port_mask_list={self.port_mask_list})"

    def __str__(self):
        return self.__repr__()


class IpV6PortGroup(Group):
    @staticmethod
    def new(
        name: str,
        ipv6_list: List[IpV6ListItem] | List[Dict[str, Any]],
        port_type: PortType,
        port_list: List[PortRangeItem] | List[str] = [],
        port_mask_list: List[PortMaskItem] | List[Dict[str, Any]] = [],
    ) -> "IpV6PortGroup":
        if len(port_list) == 0 and len(port_mask_list) == 0:
            raise ValueError("Either port_list or port_mask_list must be provided")

        map: Dict[str, Any] = {
            "name": name,
            "ipv6List": ipv6_list,
            "count": max(len(ipv6_list), len(port_list), len(port_mask_list)),
            "portType": port_type.value,
            "portList": port_list,
            "portMaskList": port_mask_list,
        }
        return IpV6PortGroup(map)

    def __init__(self, map: Dict[str, Any]):
        super().__init__(map, GroupType.ipv6_port_group)
        self.ipv6_list: List[IpV6ListItem] = [
            item if isinstance(item, IpV6ListItem) else IpV6ListItem(item)
            for item in map.get("ipv6List", [])
        ]
        self.port_type: PortType = PortType(map.get("portType", 0))
        self.port_list: List[PortRangeItem] = [
            item if isinstance(item, PortRangeItem) else PortRangeItem(item)
            for item in map.get("portList", [])
        ]
        self.port_mask_list: List[PortMaskItem] = [
            item if isinstance(item, PortMaskItem) else PortMaskItem(item)
            for item in map.get("portMaskList", [])
        ]

    def to_map(self) -> Dict[str, Any]:
        return super().to_map() | {
            "ipv6List": [item.to_map() for item in self.ipv6_list],
            "portType": self.port_type.value,
            "portList": [item.__str__() for item in self.port_list],
            "portMaskList": [item.to_map() for item in self.port_mask_list],
        }

    def __eq__(self, value):
        return isinstance(value, IpV6PortGroup) and self.to_map() == value.to_map()

    def __repr__(self):
        return f"IpV6PortGroup(name={self.name}, ipv6_list={self.ipv6_list}, port_type={self.port_type}, port_list={self.port_list}, port_mask_list={self.port_mask_list})"

    def __str__(self):
        return self.__repr__()


class MacGroup(Group):
    @staticmethod
    def new(name: str, mac_list: List[Dict[str, Any]]) -> "MacGroup":
        map: Dict[str, Any] = {
            "name": name,
            "macList": mac_list,
            "count": len(mac_list),
        }
        return MacGroup(map)

    def __init__(self, map: Dict[str, Any]):
        super().__init__(map, GroupType.mac_group)
        self.mac_list: List[Dict[str, Any]] = map.get("macList", [])

    def to_map(self) -> Dict[str, Any]:
        return super().to_map() | {"macList": self.mac_list}

    def __eq__(self, value):
        return isinstance(value, MacGroup) and self.to_map() == value.to_map()

    def __repr__(self):
        return f"MacGroup(name={self.name}, mac_list={self.mac_list})"

    def __str__(self):
        return self.__repr__()


class LocationGroup(Group):
    @staticmethod
    def new(name: str, location_list: List[Dict[str, Any]]) -> "LocationGroup":
        map: Dict[str, Any] = {
            "name": name,
            "locationList": location_list,
            "count": len(location_list),
        }
        return LocationGroup(map)

    def __init__(self, map: Dict[str, Any]):
        super().__init__(map, GroupType.location_group)
        self.location_list: List[Dict[str, Any]] = map.get("locationList", [])

    def to_map(self) -> Dict[str, Any]:
        return super().to_map() | {"locationList": self.location_list}

    def __eq__(self, value):
        return isinstance(value, LocationGroup) and self.to_map() == value.to_map()

    def __repr__(self):
        return f"LocationGroup(name={self.name}, location_list={self.location_list})"

    def __str__(self):
        return self.__repr__()


class DomainGroup(Group):
    @staticmethod
    def new(
        name: str, domain_name: List[str], domain_name_port: List[Dict[str, str]]
    ) -> "DomainGroup":
        map: Dict[str, Any] = {
            "name": name,
            "domainName": domain_name,
            "domainNamePort": domain_name_port,
            "count": 1,
        }
        return DomainGroup(map)

    def __init__(self, map: Dict[str, Any]):
        super().__init__(map, GroupType.domain_group)
        self.domain_name: List[str] = map.get("domainName", [])
        self.domain_name_port: List[Dict[str, str]] = map.get("domainNamePort", [])

    def to_map(self) -> Dict[str, Any]:
        return super().to_map() | {
            "domainName": self.domain_name,
            "domainNamePort": self.domain_name_port,
        }

    def __eq__(self, value):
        return isinstance(value, DomainGroup) and self.to_map() == value.to_map()

    def __repr__(self):
        return f"DomainGroup(name={self.name}, domain_name={self.domain_name}, domain_name_port={self.domain_name_port})"

    def __str__(self):
        return self.__repr__()


def create_group_from_map(map: Dict[str, Any]) -> Group:
    group_type = GroupType(map["type"])
    if group_type == GroupType.ip_group:
        return IpGroup(map)
    elif group_type == GroupType.ipv6_group:
        return IpV6Group(map)
    elif group_type == GroupType.ip_port_group:
        return IpPortGroup(map)
    elif group_type == GroupType.ipv6_port_group:
        return IpV6PortGroup(map)
    elif group_type == GroupType.mac_group:
        return MacGroup(map)
    elif group_type == GroupType.location_group:
        return LocationGroup(map)
    elif group_type == GroupType.domain_group:
        return DomainGroup(map)
    else:
        return Group(map)
