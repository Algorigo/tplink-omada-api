from typing import Any, Dict, Optional


class Ssid:
    def __init__(
        self,
        map: Dict[str, Any],
    ):
        self.ssid_id: str = map["ssidId"]
        self.ssid_name: str = map["ssidName"]

    def __repr__(self) -> str:
        return f"Ssid(ssid_id={self.ssid_id}, ssid_name={self.ssid_name})"


class Ssids:
    def __init__(
        self,
        map: Dict[str, Any],
    ):
        self.wlan_id: str = map["wlanId"]
        self.wlan_name: str = map["wlanName"]
        self.ssid_list = [Ssid(ssid_map) for ssid_map in map.get("ssidList", [])]
