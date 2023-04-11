# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'for_loop.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QWidget)

from CAMELS.ui_widgets.path_button_edit import Path_Button_Edit
from CAMELS.ui_widgets.variable_tool_tip_box import Variable_Box

class Ui_for_loop_config(object):
    def setupUi(self, for_loop_config):
        if not for_loop_config.objectName():
            for_loop_config.setObjectName(u"for_loop_config")
        for_loop_config.resize(380, 476)
        self.gridLayout = QGridLayout(for_loop_config)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_point = QPushButton(for_loop_config)
        self.pushButton_add_point.setObjectName(u"pushButton_add_point")
        self.pushButton_add_point.setMinimumSize(QSize(30, 23))
        self.pushButton_add_point.setMaximumSize(QSize(30, 16777215))

        self.gridLayout.addWidget(self.pushButton_add_point, 1, 3, 1, 1)

        self.label_9 = QLabel(for_loop_config)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(80, 16777215))

        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)

        self.pushButton_del_point = QPushButton(for_loop_config)
        self.pushButton_del_point.setObjectName(u"pushButton_del_point")
        self.pushButton_del_point.setMinimumSize(QSize(30, 23))
        self.pushButton_del_point.setMaximumSize(QSize(30, 16777215))

        self.gridLayout.addWidget(self.pushButton_del_point, 1, 4, 1, 1)

        self.comboBox_loop_type = QComboBox(for_loop_config)
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.setObjectName(u"comboBox_loop_type")
        self.comboBox_loop_type.setMinimumSize(QSize(135, 0))

        self.gridLayout.addWidget(self.comboBox_loop_type, 1, 1, 1, 1)

        self.label = QLabel(for_loop_config)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.path_line_button = Path_Button_Edit(for_loop_config)
        self.path_line_button.setObjectName(u"path_line_button")
        self.path_line_button.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.path_line_button, 5, 0, 1, 2)

        self.sweep_widget = QWidget(for_loop_config)
        self.sweep_widget.setObjectName(u"sweep_widget")
        self.gridLayout_2 = QGridLayout(self.sweep_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_max = QLabel(self.sweep_widget)
        self.label_max.setObjectName(u"label_max")

        self.gridLayout_2.addWidget(self.label_max, 5, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 0, 0, 1, 1)

        self.lineEdit_max = Variable_Box(self.sweep_widget)
        self.lineEdit_max.setObjectName(u"lineEdit_max")

        self.gridLayout_2.addWidget(self.lineEdit_max, 6, 1, 1, 1)

        self.lineEdit_point_distance = Variable_Box(self.sweep_widget)
        self.lineEdit_point_distance.setObjectName(u"lineEdit_point_distance")

        self.gridLayout_2.addWidget(self.lineEdit_point_distance, 9, 1, 1, 1)

        self.label_3 = QLabel(self.sweep_widget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 3, 1, 1, 1)

        self.lineEdit_stop = Variable_Box(self.sweep_widget)
        self.lineEdit_stop.setObjectName(u"lineEdit_stop")

        self.gridLayout_2.addWidget(self.lineEdit_stop, 4, 1, 1, 1)

        self.label_min = QLabel(self.sweep_widget)
        self.label_min.setObjectName(u"label_min")

        self.gridLayout_2.addWidget(self.label_min, 5, 0, 1, 1)

        self.label_6 = QLabel(self.sweep_widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_2 = QLabel(self.sweep_widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)

        self.lineEdit_start = Variable_Box(self.sweep_widget)
        self.lineEdit_start.setObjectName(u"lineEdit_start")

        self.gridLayout_2.addWidget(self.lineEdit_start, 4, 0, 1, 1)

        self.label_8 = QLabel(self.sweep_widget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 7, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 11, 0, 1, 1)

        self.label_7 = QLabel(self.sweep_widget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 7, 0, 1, 1)

        self.comboBox_sweep_mode = QComboBox(self.sweep_widget)
        self.comboBox_sweep_mode.addItem("")
        self.comboBox_sweep_mode.addItem("")
        self.comboBox_sweep_mode.addItem("")
        self.comboBox_sweep_mode.addItem("")
        self.comboBox_sweep_mode.setObjectName(u"comboBox_sweep_mode")

        self.gridLayout_2.addWidget(self.comboBox_sweep_mode, 1, 1, 1, 1)

        self.lineEdit_min = Variable_Box(self.sweep_widget)
        self.lineEdit_min.setObjectName(u"lineEdit_min")

        self.gridLayout_2.addWidget(self.lineEdit_min, 6, 0, 1, 1)

        self.lineEdit_n_points = Variable_Box(self.sweep_widget)
        self.lineEdit_n_points.setObjectName(u"lineEdit_n_points")

        self.gridLayout_2.addWidget(self.lineEdit_n_points, 9, 0, 1, 1)

        self.checkBox_include_endpoints = QCheckBox(self.sweep_widget)
        self.checkBox_include_endpoints.setObjectName(u"checkBox_include_endpoints")
        self.checkBox_include_endpoints.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_include_endpoints, 10, 0, 1, 2)


        self.gridLayout.addWidget(self.sweep_widget, 3, 0, 1, 2)

        self.verticalSpacer_4 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_4, 6, 1, 1, 1)

        self.tableWidget_points = QTableWidget(for_loop_config)
        self.tableWidget_points.setObjectName(u"tableWidget_points")
        self.tableWidget_points.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.tableWidget_points, 2, 2, 5, 3)

        QWidget.setTabOrder(self.comboBox_loop_type, self.pushButton_add_point)
        QWidget.setTabOrder(self.pushButton_add_point, self.pushButton_del_point)
        QWidget.setTabOrder(self.pushButton_del_point, self.comboBox_sweep_mode)
        QWidget.setTabOrder(self.comboBox_sweep_mode, self.lineEdit_start)
        QWidget.setTabOrder(self.lineEdit_start, self.lineEdit_stop)
        QWidget.setTabOrder(self.lineEdit_stop, self.lineEdit_min)
        QWidget.setTabOrder(self.lineEdit_min, self.lineEdit_max)
        QWidget.setTabOrder(self.lineEdit_max, self.lineEdit_n_points)
        QWidget.setTabOrder(self.lineEdit_n_points, self.lineEdit_point_distance)
        QWidget.setTabOrder(self.lineEdit_point_distance, self.checkBox_include_endpoints)
        QWidget.setTabOrder(self.checkBox_include_endpoints, self.tableWidget_points)

        self.retranslateUi(for_loop_config)

        QMetaObject.connectSlotsByName(for_loop_config)
    # setupUi

    def retranslateUi(self, for_loop_config):
        for_loop_config.setWindowTitle(QCoreApplication.translate("for_loop_config", u"Form", None))
        self.pushButton_add_point.setText(QCoreApplication.translate("for_loop_config", u"+", None))
        self.label_9.setText(QCoreApplication.translate("for_loop_config", u"Points:", None))
        self.pushButton_del_point.setText(QCoreApplication.translate("for_loop_config", u"-", None))
        self.comboBox_loop_type.setItemText(0, QCoreApplication.translate("for_loop_config", u"start - stop", None))
        self.comboBox_loop_type.setItemText(1, QCoreApplication.translate("for_loop_config", u"start - min - max - stop", None))
        self.comboBox_loop_type.setItemText(2, QCoreApplication.translate("for_loop_config", u"start - max - min - stop", None))
        self.comboBox_loop_type.setItemText(3, QCoreApplication.translate("for_loop_config", u"Value-List", None))
        self.comboBox_loop_type.setItemText(4, QCoreApplication.translate("for_loop_config", u"Text-File", None))

        self.label.setText(QCoreApplication.translate("for_loop_config", u"Loop-Type:", None))
        self.label_max.setText(QCoreApplication.translate("for_loop_config", u"Max", None))
        self.label_3.setText(QCoreApplication.translate("for_loop_config", u"Stop", None))
        self.label_min.setText(QCoreApplication.translate("for_loop_config", u"Min", None))
        self.label_6.setText(QCoreApplication.translate("for_loop_config", u"Sweep mode", None))
        self.label_2.setText(QCoreApplication.translate("for_loop_config", u"Start", None))
        self.label_8.setText(QCoreApplication.translate("for_loop_config", u"point-distance", None))
        self.label_7.setText(QCoreApplication.translate("for_loop_config", u"# points", None))
        self.comboBox_sweep_mode.setItemText(0, QCoreApplication.translate("for_loop_config", u"linear", None))
        self.comboBox_sweep_mode.setItemText(1, QCoreApplication.translate("for_loop_config", u"logarithmic", None))
        self.comboBox_sweep_mode.setItemText(2, QCoreApplication.translate("for_loop_config", u"exponential", None))
        self.comboBox_sweep_mode.setItemText(3, QCoreApplication.translate("for_loop_config", u"1/x", None))

        self.checkBox_include_endpoints.setText(QCoreApplication.translate("for_loop_config", u"Include end-points", None))
    # retranslateUi

