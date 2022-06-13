# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (
    QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMenuBar, QPushButton, QStatusBar,
    QTableWidget, QVBoxLayout, QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(678, 416)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.point_info_box = QGroupBox(self.groupBox_2)
        self.point_info_box.setObjectName(u"point_info_box")
        self.horizontalLayout = QHBoxLayout(self.point_info_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.point_info_box)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.point_name_edit = QLineEdit(self.point_info_box)
        self.point_name_edit.setObjectName(u"point_name_edit")

        self.horizontalLayout.addWidget(self.point_name_edit)

        self.distance_lbl = QLabel(self.point_info_box)
        self.distance_lbl.setObjectName(u"distance_lbl")

        self.horizontalLayout.addWidget(self.distance_lbl)

        self.point_append_btn = QPushButton(self.point_info_box)
        self.point_append_btn.setObjectName(u"point_append_btn")

        self.horizontalLayout.addWidget(self.point_append_btn)

        self.verticalLayout.addWidget(self.point_info_box)

        self.points_table = QTableWidget(self.groupBox_2)
        self.points_table.setObjectName(u"points_table")
        self.points_table.horizontalHeader().setCascadingSectionResizes(False)
        self.points_table.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout.addWidget(self.points_table)

        self.calculate_distance_btn = QPushButton(self.groupBox_2)
        self.calculate_distance_btn.setObjectName(u"calculate_distance_btn")

        self.verticalLayout.addWidget(self.calculate_distance_btn)

        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 678, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", "Ввод точек", None))
        self.point_info_box.setTitle("")
        self.label.setText(QCoreApplication.translate("MainWindow", "Точка", None))
        self.distance_lbl.setText("")
        self.point_append_btn.setText(QCoreApplication.translate("MainWindow", "добавить", None))
        self.calculate_distance_btn.setText(QCoreApplication.translate("MainWindow", "Рассчитать", None))
    # retranslateUi
