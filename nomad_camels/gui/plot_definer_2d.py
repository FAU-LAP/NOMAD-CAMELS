# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_definer_2d.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QWidget)

from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box

class Ui_Plot_Definer_2D(object):
    def setupUi(self, Plot_Definer_2D):
        if not Plot_Definer_2D.objectName():
            Plot_Definer_2D.setObjectName(u"Plot_Definer_2D")
        Plot_Definer_2D.resize(400, 222)
        self.gridLayout = QGridLayout(Plot_Definer_2D)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(Plot_Definer_2D)
        self.label_7.setObjectName(u"label_7")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.label_6 = QLabel(Plot_Definer_2D)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_8 = QLabel(Plot_Definer_2D)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)

        self.lineEdit_ylabel = QLineEdit(Plot_Definer_2D)
        self.lineEdit_ylabel.setObjectName(u"lineEdit_ylabel")

        self.gridLayout.addWidget(self.lineEdit_ylabel, 3, 3, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

        self.label_10 = QLabel(Plot_Definer_2D)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 4, 2, 1, 1)

        self.label_9 = QLabel(Plot_Definer_2D)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.label_5 = QLabel(Plot_Definer_2D)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.lineEdit_title = QLineEdit(Plot_Definer_2D)
        self.lineEdit_title.setObjectName(u"lineEdit_title")

        self.gridLayout.addWidget(self.lineEdit_title, 0, 1, 1, 3)

        self.label_11 = QLabel(Plot_Definer_2D)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 1, 1, 1)

        self.lineEdit_y_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_y_axis.setObjectName(u"lineEdit_y_axis")

        self.gridLayout.addWidget(self.lineEdit_y_axis, 3, 1, 1, 1)

        self.lineEdit_z_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_z_axis.setObjectName(u"lineEdit_z_axis")

        self.gridLayout.addWidget(self.lineEdit_z_axis, 4, 1, 1, 1)

        self.lineEdit_xlabel = QLineEdit(Plot_Definer_2D)
        self.lineEdit_xlabel.setObjectName(u"lineEdit_xlabel")

        self.gridLayout.addWidget(self.lineEdit_xlabel, 2, 3, 1, 1)

        self.lineEdit_x_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_x_axis.setObjectName(u"lineEdit_x_axis")

        self.gridLayout.addWidget(self.lineEdit_x_axis, 2, 1, 1, 1)

        self.lineEdit_zlabel = QLineEdit(Plot_Definer_2D)
        self.lineEdit_zlabel.setObjectName(u"lineEdit_zlabel")

        self.gridLayout.addWidget(self.lineEdit_zlabel, 4, 3, 1, 1)

        self.label_12 = QLabel(Plot_Definer_2D)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 6, 0, 1, 2)

        self.lineEdit_n_data_points = QLineEdit(Plot_Definer_2D)
        self.lineEdit_n_data_points.setObjectName(u"lineEdit_n_data_points")

        self.gridLayout.addWidget(self.lineEdit_n_data_points, 6, 2, 1, 2)

        QWidget.setTabOrder(self.lineEdit_title, self.lineEdit_x_axis)
        QWidget.setTabOrder(self.lineEdit_x_axis, self.lineEdit_y_axis)
        QWidget.setTabOrder(self.lineEdit_y_axis, self.lineEdit_z_axis)
        QWidget.setTabOrder(self.lineEdit_z_axis, self.lineEdit_xlabel)
        QWidget.setTabOrder(self.lineEdit_xlabel, self.lineEdit_ylabel)
        QWidget.setTabOrder(self.lineEdit_ylabel, self.lineEdit_zlabel)

        self.retranslateUi(Plot_Definer_2D)

        QMetaObject.connectSlotsByName(Plot_Definer_2D)
    # setupUi

    def retranslateUi(self, Plot_Definer_2D):
        Plot_Definer_2D.setWindowTitle(QCoreApplication.translate("Plot_Definer_2D", u"Form", None))
        self.label_7.setText(QCoreApplication.translate("Plot_Definer_2D", u"z-axis:", None))
        self.label_6.setText(QCoreApplication.translate("Plot_Definer_2D", u"y-axis:", None))
        self.label_8.setText(QCoreApplication.translate("Plot_Definer_2D", u"y-label:", None))
        self.label_10.setText(QCoreApplication.translate("Plot_Definer_2D", u"z-label:", None))
        self.label_9.setText(QCoreApplication.translate("Plot_Definer_2D", u"x-label:", None))
        self.label_5.setText(QCoreApplication.translate("Plot_Definer_2D", u"x-axis:", None))
        self.label_11.setText(QCoreApplication.translate("Plot_Definer_2D", u"title:", None))
        self.label_12.setText(QCoreApplication.translate("Plot_Definer_2D", u"# data points:", None))
        self.lineEdit_n_data_points.setText(QCoreApplication.translate("Plot_Definer_2D", u"inf", None))
    # retranslateUi

