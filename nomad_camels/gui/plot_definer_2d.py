# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_definer_2d.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QFrame,
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box

class Ui_Plot_Definer_2D(object):
    def setupUi(self, Plot_Definer_2D):
        if not Plot_Definer_2D.objectName():
            Plot_Definer_2D.setObjectName(u"Plot_Definer_2D")
        Plot_Definer_2D.resize(400, 305)
        self.gridLayout = QGridLayout(Plot_Definer_2D)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_top_left_x = QLabel(Plot_Definer_2D)
        self.label_top_left_x.setObjectName(u"label_top_left_x")

        self.gridLayout.addWidget(self.label_top_left_x, 9, 0, 1, 1)

        self.label_9 = QLabel(Plot_Definer_2D)
        self.label_9.setObjectName(u"label_9")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.lineEdit_plot_height = QLineEdit(Plot_Definer_2D)
        self.lineEdit_plot_height.setObjectName(u"lineEdit_plot_height")

        self.gridLayout.addWidget(self.lineEdit_plot_height, 10, 3, 1, 1)

        self.label_10 = QLabel(Plot_Definer_2D)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 4, 2, 1, 1)

        self.label_6 = QLabel(Plot_Definer_2D)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.lineEdit_zlabel = Variable_Box(Plot_Definer_2D)
        self.lineEdit_zlabel.setObjectName(u"lineEdit_zlabel")

        self.gridLayout.addWidget(self.lineEdit_zlabel, 4, 3, 1, 1)

        self.lineEdit_top_left_x = QLineEdit(Plot_Definer_2D)
        self.lineEdit_top_left_x.setObjectName(u"lineEdit_top_left_x")

        self.gridLayout.addWidget(self.lineEdit_top_left_x, 9, 1, 1, 1)

        self.checkBox_manual_plot_position_2d = QCheckBox(Plot_Definer_2D)
        self.checkBox_manual_plot_position_2d.setObjectName(u"checkBox_manual_plot_position_2d")

        self.gridLayout.addWidget(self.checkBox_manual_plot_position_2d, 7, 0, 1, 1)

        self.label_plot_width = QLabel(Plot_Definer_2D)
        self.label_plot_width.setObjectName(u"label_plot_width")

        self.gridLayout.addWidget(self.label_plot_width, 9, 2, 1, 1)

        self.spinBox_port = QSpinBox(Plot_Definer_2D)
        self.spinBox_port.setObjectName(u"spinBox_port")
        self.spinBox_port.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_port.setMaximum(65536)
        self.spinBox_port.setValue(8050)

        self.gridLayout.addWidget(self.spinBox_port, 12, 1, 1, 1)

        self.label_8 = QLabel(Plot_Definer_2D)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)

        self.label_plot_height = QLabel(Plot_Definer_2D)
        self.label_plot_height.setObjectName(u"label_plot_height")

        self.gridLayout.addWidget(self.label_plot_height, 10, 2, 1, 1)

        self.label_11 = QLabel(Plot_Definer_2D)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)

        self.label_7 = QLabel(Plot_Definer_2D)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.lineEdit_x_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_x_axis.setObjectName(u"lineEdit_x_axis")

        self.gridLayout.addWidget(self.lineEdit_x_axis, 2, 1, 1, 1)

        self.lineEdit_plot_width = QLineEdit(Plot_Definer_2D)
        self.lineEdit_plot_width.setObjectName(u"lineEdit_plot_width")

        self.gridLayout.addWidget(self.lineEdit_plot_width, 9, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 13, 0, 1, 1)

        self.label_5 = QLabel(Plot_Definer_2D)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_top_left_y = QLabel(Plot_Definer_2D)
        self.label_top_left_y.setObjectName(u"label_top_left_y")

        self.gridLayout.addWidget(self.label_top_left_y, 10, 0, 1, 1)

        self.lineEdit_n_data_points = QLineEdit(Plot_Definer_2D)
        self.lineEdit_n_data_points.setObjectName(u"lineEdit_n_data_points")

        self.gridLayout.addWidget(self.lineEdit_n_data_points, 5, 2, 1, 2)

        self.lineEdit_y_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_y_axis.setObjectName(u"lineEdit_y_axis")

        self.gridLayout.addWidget(self.lineEdit_y_axis, 3, 1, 1, 1)

        self.lineEdit_z_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_z_axis.setObjectName(u"lineEdit_z_axis")

        self.gridLayout.addWidget(self.lineEdit_z_axis, 4, 1, 1, 1)

        self.checkBox_show_in_browser = QCheckBox(Plot_Definer_2D)
        self.checkBox_show_in_browser.setObjectName(u"checkBox_show_in_browser")

        self.gridLayout.addWidget(self.checkBox_show_in_browser, 11, 0, 1, 1)

        self.lineEdit_title = Variable_Box(Plot_Definer_2D)
        self.lineEdit_title.setObjectName(u"lineEdit_title")

        self.gridLayout.addWidget(self.lineEdit_title, 0, 1, 1, 3)

        self.lineEdit_xlabel = Variable_Box(Plot_Definer_2D)
        self.lineEdit_xlabel.setObjectName(u"lineEdit_xlabel")

        self.gridLayout.addWidget(self.lineEdit_xlabel, 2, 3, 1, 1)

        self.label_12 = QLabel(Plot_Definer_2D)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 5, 0, 1, 2)

        self.line = QFrame(Plot_Definer_2D)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 6, 0, 1, 4)

        self.lineEdit_top_left_y = QLineEdit(Plot_Definer_2D)
        self.lineEdit_top_left_y.setObjectName(u"lineEdit_top_left_y")

        self.gridLayout.addWidget(self.lineEdit_top_left_y, 10, 1, 1, 1)

        self.label_port = QLabel(Plot_Definer_2D)
        self.label_port.setObjectName(u"label_port")

        self.gridLayout.addWidget(self.label_port, 12, 0, 1, 1)

        self.lineEdit_ylabel = Variable_Box(Plot_Definer_2D)
        self.lineEdit_ylabel.setObjectName(u"lineEdit_ylabel")

        self.gridLayout.addWidget(self.lineEdit_ylabel, 3, 3, 1, 1)

        QWidget.setTabOrder(self.lineEdit_title, self.lineEdit_x_axis)
        QWidget.setTabOrder(self.lineEdit_x_axis, self.lineEdit_y_axis)
        QWidget.setTabOrder(self.lineEdit_y_axis, self.lineEdit_z_axis)
        QWidget.setTabOrder(self.lineEdit_z_axis, self.lineEdit_xlabel)
        QWidget.setTabOrder(self.lineEdit_xlabel, self.lineEdit_ylabel)
        QWidget.setTabOrder(self.lineEdit_ylabel, self.lineEdit_zlabel)
        QWidget.setTabOrder(self.lineEdit_zlabel, self.lineEdit_n_data_points)
        QWidget.setTabOrder(self.lineEdit_n_data_points, self.lineEdit_top_left_x)
        QWidget.setTabOrder(self.lineEdit_top_left_x, self.lineEdit_top_left_y)
        QWidget.setTabOrder(self.lineEdit_top_left_y, self.lineEdit_plot_width)
        QWidget.setTabOrder(self.lineEdit_plot_width, self.lineEdit_plot_height)

        self.retranslateUi(Plot_Definer_2D)

        QMetaObject.connectSlotsByName(Plot_Definer_2D)
    # setupUi

    def retranslateUi(self, Plot_Definer_2D):
        Plot_Definer_2D.setWindowTitle(QCoreApplication.translate("Plot_Definer_2D", u"Form", None))
#if QT_CONFIG(tooltip)
        self.label_top_left_x.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Set the exact x coordinate of the top left corner of the plot window in pixels (min 0)", None))
#endif // QT_CONFIG(tooltip)
        self.label_top_left_x.setText(QCoreApplication.translate("Plot_Definer_2D", u"Top Left X", None))
        self.label_9.setText(QCoreApplication.translate("Plot_Definer_2D", u"x-label:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_plot_height.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Minimum is 126 pixels", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("Plot_Definer_2D", u"z-label:", None))
        self.label_6.setText(QCoreApplication.translate("Plot_Definer_2D", u"y-axis:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_top_left_x.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Minimum is 0 pixels", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkBox_manual_plot_position_2d.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Check this to set the manual x&y coordinates and the size of the plot window.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_manual_plot_position_2d.setText(QCoreApplication.translate("Plot_Definer_2D", u"Manual plot position", None))
#if QT_CONFIG(tooltip)
        self.label_plot_width.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Set the width of the plot window in pixels (min 430)", None))
#endif // QT_CONFIG(tooltip)
        self.label_plot_width.setText(QCoreApplication.translate("Plot_Definer_2D", u"Plot Width", None))
        self.label_8.setText(QCoreApplication.translate("Plot_Definer_2D", u"y-label:", None))
#if QT_CONFIG(tooltip)
        self.label_plot_height.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Set the height of the plot window in pixels (min 126)", None))
#endif // QT_CONFIG(tooltip)
        self.label_plot_height.setText(QCoreApplication.translate("Plot_Definer_2D", u"Plot Height", None))
        self.label_11.setText(QCoreApplication.translate("Plot_Definer_2D", u"title:", None))
        self.label_7.setText(QCoreApplication.translate("Plot_Definer_2D", u"z-axis:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_plot_width.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Minimum is 430 pixels", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Plot_Definer_2D", u"x-axis:", None))
#if QT_CONFIG(tooltip)
        self.label_top_left_y.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Set the exact y coordinate of the top left corner of the plot window in pixels (min 0)", None))
#endif // QT_CONFIG(tooltip)
        self.label_top_left_y.setText(QCoreApplication.translate("Plot_Definer_2D", u"Top Left Y", None))
        self.lineEdit_n_data_points.setText(QCoreApplication.translate("Plot_Definer_2D", u"inf", None))
#if QT_CONFIG(tooltip)
        self.checkBox_show_in_browser.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Check this to make the plot available via the browser.\n"
"This will significantly increase the protocol startup time!\n"
"Reachable under 127.0.0.1:Port", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_show_in_browser.setText(QCoreApplication.translate("Plot_Definer_2D", u"Show plot in browser", None))
        self.label_12.setText(QCoreApplication.translate("Plot_Definer_2D", u"# data points:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_top_left_y.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Minimum is 0 pixels", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_port.setToolTip(QCoreApplication.translate("Plot_Definer_2D", u"Port of the localhost to display the plot. ", None))
#endif // QT_CONFIG(tooltip)
        self.label_port.setText(QCoreApplication.translate("Plot_Definer_2D", u"Port", None))
    # retranslateUi

