import math
import random
from dataclasses import dataclass
from typing import Optional, NamedTuple, List

from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from furl import furl

from config.current_config import Config

ANTS_COUNT = 50
TRIALS_COUNT = 100
EVAPORATING_RATE = 0.1


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


class SavedPointType(NamedTuple):
    point: Point
    address: str


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


class Ant:

    def __init__(self, pheromones: List[List[int]], nodes: List[SavedPointType], geo_service: GeoService):
        self.geo_service = geo_service
        self.pheromones = pheromones
        self.nodes = nodes
        self.path = []
        self.path_len = math.inf

    def run(self):
        self.path = []
        pheromone_map = [self.pheromones[row][:] for row in range(len(self.pheromones))]
        current_node = random.choice(range(len(self.nodes)))
        self.path.append(current_node)
        for row in range(len(pheromone_map)):
            pheromone_map[row][current_node] = 0
        for i in range(len(self.nodes) - 1):
            current_node = random.choices(range(len(self.nodes)), weights=pheromone_map[self.path[-1]])[0]
            self.path.append(current_node)
            for row in range(len(pheromone_map)):
                pheromone_map[row][current_node] = 0

        distance = 0
        for i in range(len(self.path) - 1):
            distance += self.geo_service.points_distance(self.nodes[i].point, self.nodes[i + 1].point)
        self.path_len = distance


class TSPMap:

    def __init__(self, nodes: List[SavedPointType]):
        self.geo_service = GeoService()
        self.nodes = nodes
        self.pheromones = [[1 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
        for i in range(len(self.pheromones)):
            self.pheromones[i][i] = 0
        self.evaporating_rate = EVAPORATING_RATE
        self.optimal_path = []
        self.optimal_length = math.inf

    def run(self):
        for trial in range(TRIALS_COUNT):
            ants = [Ant(pheromones=self.pheromones, nodes=self.nodes, geo_service=self.geo_service)
                    for _ in range(ANTS_COUNT)]
            for ant in ants:
                ant.run()
            optimal_ant = min(ants, key=lambda x: x.path_len)
            self.update_pheromones(optimal_ant)
            self.optimal_path = optimal_ant.path
            self.optimal_length = optimal_ant.path_len

    def update_pheromones(self, optimal_ant: Ant):
        self.pheromones = [[self.pheromones[i][j] * (1 - self.evaporating_rate)
                            for j in range(len(self.pheromones))] for i in range(len(self.pheromones))]
        path = optimal_ant.path
        for i in range(len(path) - 1):
            self.pheromones[path[i]][path[i + 1]] += 1 / optimal_ant.path_len
            self.pheromones[path[i + 1]][path[i]] += 1 / optimal_ant.path_len
        if len(path) and path[0] != path[-1]:
            self.pheromones[path[0]][path[-1]] += 1 / optimal_ant.path_len
            self.pheromones[path[-1]][path[0]] += 1 / optimal_ant.path_len

    def get_optimal_path(self):
        return [self.nodes[i] for i in self.optimal_path]
