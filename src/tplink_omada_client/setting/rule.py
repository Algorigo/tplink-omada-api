from typing import Dict, Any, List, Optional
from enum import Enum
from .policy import Policy


class RuleType(Enum):
    gateway = "gateway"
    eap = "ap"


class RuleSourceType(Enum):
    network = 0
    ip_group = 1
    ssid = 2


class Rule:
    @staticmethod
    def new_eap(
        type: RuleType,
        name: str,
        status: bool,
        policy: Policy,
        source_type: RuleSourceType,
        source_ids: List[str],
        urls: List[str],
    ) -> "Rule":
        map: Dict[str, Any] = {
            "type": type.value,
            "name": name,
            "status": status,
            "policy": policy.value,
            "sourceType": source_type.value,
            "sourceIds": source_ids,
            "urls": urls,
        }
        return Rule(map)

    def __init__(self, map: Dict[str, Any]):
        self.id: Optional[str] = map.get("id")
        self.index: Optional[int] = map.get("index")
        self.site_id: Optional[str] = map.get("siteId")
        self.type: RuleType = RuleType(map["type"])
        self.entry_id: Optional[int] = map.get("entryId")
        self.name: str = map["name"]
        self.status: bool = map["status"]
        self.policy: Policy = Policy(map["policy"])
        self.source_type: RuleSourceType = RuleSourceType(map["sourceType"])
        self.source_ids: List[str] = map["sourceIds"]
        self.mode: int = map.get("mode", 0)
        self.urls: List[str] = map["urls"]
        self.resource: Optional[int] = map.get("resource")

    def to_map(self) -> Dict[str, Any]:
        map: Dict[str, Any] = {
            "type": self.type.value,
            "entryId": self.entry_id,
            "name": self.name,
            "status": self.status,
            "policy": self.policy.value,
            "sourceType": self.source_type.value,
            "sourceIds": self.source_ids,
            "urls": self.urls,
        }
        if self.id is not None:
            map["id"] = self.id
        if self.index is not None:
            map["index"] = self.index
        if self.site_id is not None:
            map["siteId"] = self.site_id
        if self.mode is not None:
            map["mode"] = self.mode
        if self.resource is not None:
            map["resource"] = self.resource
        return map

    def __repr__(self):
        return f"Rule(id={self.id}, index={self.index}, type={self.type}, source_ids={self.source_ids})"
