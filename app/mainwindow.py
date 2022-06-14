# This Python file uses the following encoding: utf-8
import json
from typing import List

from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem

from app.ui_mainwindow import Ui_MainWindow
from services.geo_service import GeoService, Point, SavedPointType, TSPMap
from utils.alerts import error_alert, alert


class MainWindow(QMainWindow):
    geo_service = GeoService()
    _points: List[SavedPointType] = None
    _points_matrix: List[List[float]] = None

    def __init__(self):
        super().__init__()
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.point_append_btn.clicked.connect(self.create_point)
        self.ui.calculate_distance_btn.clicked.connect(self.calculate_distance)
        self.geo_network_manager = QNetworkAccessManager(self)
        self.geo_network_manager.finished.connect(self.process_found_coords)
        self._points = []
        self._points_matrix = []

    def on_point_find_start(self):
        self.ui.point_append_btn.setDisabled(True)
        self.ui.point_name_edit.setDisabled(True)

    def on_point_find_end(self):
        self.ui.point_append_btn.setDisabled(False)
        self.ui.point_name_edit.setDisabled(False)
        self.ui.point_name_edit.setText("")

    def create_point(self):
        self.on_point_find_start()
        point_name = self.ui.point_name_edit.text()
        if not point_name:
            self.on_point_find_end()
            return
        self.geo_service.start_point_coords_search(network_manager=self.geo_network_manager, point_data=point_name)

    def update_points_matrix(self):
        self._points_matrix = [row + [0] for row in self._points_matrix]
        self._points_matrix.append([0] * len(self._points))
        for row_idx, row in enumerate(self._points_matrix):
            for col_idx, col in enumerate(row):
                if col_idx == row_idx or col:
                    continue
                points_distance = self.geo_service.points_distance(first_point=self._points[row_idx].point,
                                                                   second_point=self._points[col_idx].point)
                self._points_matrix[row_idx][col_idx] = points_distance

    def append_coords_to_table(self, point: Point):
        point_name = self.ui.point_name_edit.text()

        self.ui.points_table.insertRow(self.ui.points_table.rowCount())
        self.ui.points_table.insertColumn(self.ui.points_table.columnCount())
        header_name = f"{point_name} {point}"
        header_pos = self.ui.points_table.rowCount() - 1
        self.ui.points_table.setVerticalHeaderItem(header_pos, QTableWidgetItem(header_name))
        self.ui.points_table.setHorizontalHeaderItem(header_pos, QTableWidgetItem(header_name))

        for idx, row in enumerate(self._points_matrix):
            self.ui.points_table.setItem(idx, header_pos, QTableWidgetItem(str(self._points_matrix[idx][header_pos])))
            self.ui.points_table.setItem(header_pos, idx, QTableWidgetItem(str(self._points_matrix[idx][header_pos])))

        self.ui.points_table.resizeColumnToContents(header_pos)

    def process_found_coords(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            reply_content = reply.readAll()
            parsed_content = json.loads(str(reply_content, "utf-8"))
            point = self.geo_service.coords_found(response=parsed_content)
            if not point:
                error_alert(widget=self, message="Точка не найдена")
                self.on_point_find_end()
                return
            if point in [i.point for i in self._points]:
                error_alert(widget=self, message="Точка уже добавлена")
                self.on_point_find_end()
                return
            self._points.append(SavedPointType(point=point, address=self.ui.point_name_edit.text()))
            self.update_points_matrix()
            self.append_coords_to_table(point=point)
        else:
            error_alert(widget=self, message=reply.errorString())
        self.on_point_find_end()

    def calculate_distance(self):
        if len(self._points) <= 1:
            error_alert(widget=self, message="Недостаточное количество точек для рассчета")
            return
        if len(self._points) == 2:
            alert(widget=self, title="Маршрут", message="\n".join([
                "Оптимальный маршрут " + " - ".join([self._points[0].address,
                                                     self._points[1].address,
                                                     self._points[0].address]),
                "Протяженность маршрута " + str(
                    self.geo_service.points_distance(first_point=self._points[0].point,
                                                     second_point=self._points[1].point) * 2
                )
            ]))
            return
        map = TSPMap(nodes=self._points)
        map.run()
        alert(widget=self, title="Маршрут", message="\n".join([
            "Оптимальный маршрут " + " - ".join([self._points[0].address,
                                                 *[self._points[i].address for i in map.optimal_path],
                                                 self._points[0].address]),
            f"Протяженность маршрута {map.optimal_length}"
        ]))
