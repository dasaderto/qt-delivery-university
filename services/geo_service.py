import math
from dataclasses import dataclass
from typing import Optional

from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from furl import furl

from config.current_config import Config


@dataclass
class Point:
    lng: float
    lat: float

    def to_rad(self) -> 'Point':
        return Point(lng=RadConverter(self.lng).convert(), lat=RadConverter(self.lat).convert())

    def __str__(self):
        return f"({self.lng}, {self.lat})"

    def __eq__(self, other: 'Point'):
        if not isinstance(other, Point):
            return False

        return self.lng == other.lng and self.lat == other.lat


class RadConverter:
    def __init__(self, value: float):
        self.value = value

    def convert(self) -> float:
        return self.value * math.pi / 180


class GeoService:
    geocode_base_url = f"https://geocode-maps.yandex.ru/1.x?apikey={Config.YA_MAPS_API_KEY}&format=json"

    def start_point_coords_search(self, network_manager: QNetworkAccessManager, point_data: str):
        url = furl(self.geocode_base_url)
        url.args.add("geocode", point_data)
        request = QNetworkRequest(QUrl(url.url))
        network_manager.get(request)

    def coords_found(self, response: dict) -> Optional[Point]:
        feature_members = response.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
        if not feature_members:
            return

        need_member = feature_members[0]
        coords = need_member.get('GeoObject', {}).get("Point", {}).get('pos', "")
        if not coords:
            return

        split_coords = coords.split()
        return Point(lng=float(split_coords[0]), lat=float(split_coords[1]))

    def points_distance(self, first_point: Point, second_point: Point) -> float:
        int_r = 6371
        d_lng = RadConverter(value=second_point.lng - first_point.lng).convert()
        d_lat = RadConverter(value=second_point.lat - first_point.lat).convert()
        rad_first_point = first_point.to_rad()
        rad_second_point = second_point.to_rad()
        int_a = (math.sin(d_lat / 2) ** 2 + math.sin(d_lng / 2) ** 2
                 * math.cos(rad_first_point.lat) * math.cos(rad_second_point.lat))
        int_c = 2 * math.atan2(math.sqrt(int_a), math.sqrt(1 - int_a))
        int_d = int_r * int_c

        return round(int_d, 3)