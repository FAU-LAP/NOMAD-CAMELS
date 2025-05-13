# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_definer.ui'
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

class Ui_Plot_Definer(object):
    def setupUi(self, Plot_Definer):
        if not Plot_Definer.objectName():
            Plot_Definer.setObjectName(u"Plot_Definer")
        Plot_Definer.resize(470, 435)
        self.gridLayout = QGridLayout(Plot_Definer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_x_axis = Variable_Box(Plot_Definer)
        self.lineEdit_x_axis.setObjectName(u"lineEdit_x_axis")

        self.gridLayout.addWidget(self.lineEdit_x_axis, 0, 1, 1, 3)

        self.label_5 = QLabel(Plot_Definer)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.line = QFrame(Plot_Definer)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 3, 0, 1, 4)

        self.fit_definer = QLabel(Plot_Definer)
        self.fit_definer.setObjectName(u"fit_definer")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        self.fit_definer.setFont(font1)

        self.gridLayout.addWidget(self.fit_definer, 5, 3, 4, 1)

        self.checkBox_same_fit = QCheckBox(Plot_Definer)
        self.checkBox_same_fit.setObjectName(u"checkBox_same_fit")

        self.gridLayout.addWidget(self.checkBox_same_fit, 4, 3, 1, 1)

        self.y_axes = QWidget(Plot_Definer)
        self.y_axes.setObjectName(u"y_axes")

        self.gridLayout.addWidget(self.y_axes, 1, 0, 1, 4)

        self.line_2 = QFrame(Plot_Definer)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 4, 2, 5, 1)

        self.plotting_group = QWidget(Plot_Definer)
        self.plotting_group.setObjectName(u"plotting_group")
        self.gridLayout_2 = QGridLayout(self.plotting_group)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_ylabel2 = Variable_Box(self.plotting_group)
        self.lineEdit_ylabel2.setObjectName(u"lineEdit_ylabel2")

        self.gridLayout_2.addWidget(self.lineEdit_ylabel2, 4, 3, 1, 1)

        self.checkBox_xlog = QCheckBox(self.plotting_group)
        self.checkBox_xlog.setObjectName(u"checkBox_xlog")

        self.gridLayout_2.addWidget(self.checkBox_xlog, 3, 0, 1, 4)

        self.label_6 = QLabel(self.plotting_group)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_3 = QLabel(self.plotting_group)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_top_left_x = QLabel(self.plotting_group)
        self.label_top_left_x.setObjectName(u"label_top_left_x")

        self.gridLayout_2.addWidget(self.label_top_left_x, 9, 0, 1, 1)

        self.lineEdit_top_left_x = QLineEdit(self.plotting_group)
        self.lineEdit_top_left_x.setObjectName(u"lineEdit_top_left_x")

        self.gridLayout_2.addWidget(self.lineEdit_top_left_x, 9, 1, 1, 1)

        self.lineEdit_plot_width = QLineEdit(self.plotting_group)
        self.lineEdit_plot_width.setObjectName(u"lineEdit_plot_width")

        self.gridLayout_2.addWidget(self.lineEdit_plot_width, 9, 3, 1, 1)

        self.label_top_left_y = QLabel(self.plotting_group)
        self.label_top_left_y.setObjectName(u"label_top_left_y")

        self.gridLayout_2.addWidget(self.label_top_left_y, 10, 0, 1, 1)

        self.lineEdit_plot_height = QLineEdit(self.plotting_group)
        self.lineEdit_plot_height.setObjectName(u"lineEdit_plot_height")

        self.gridLayout_2.addWidget(self.lineEdit_plot_height, 10, 3, 1, 1)

        self.checkBox_ylog = QCheckBox(self.plotting_group)
        self.checkBox_ylog.setObjectName(u"checkBox_ylog")

        self.gridLayout_2.addWidget(self.checkBox_ylog, 6, 0, 1, 2)

        self.label_plot_height = QLabel(self.plotting_group)
        self.label_plot_height.setObjectName(u"label_plot_height")

        self.gridLayout_2.addWidget(self.label_plot_height, 10, 2, 1, 1)

        self.lineEdit_nPoints = QLineEdit(self.plotting_group)
        self.lineEdit_nPoints.setObjectName(u"lineEdit_nPoints")

        self.gridLayout_2.addWidget(self.lineEdit_nPoints, 0, 1, 1, 3)

        self.line_3 = QFrame(self.plotting_group)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 7, 0, 1, 4)

        self.lineEdit_xlabel = Variable_Box(self.plotting_group)
        self.lineEdit_xlabel.setObjectName(u"lineEdit_xlabel")

        self.gridLayout_2.addWidget(self.lineEdit_xlabel, 2, 1, 1, 3)

        self.lineEdit_title = Variable_Box(self.plotting_group)
        self.lineEdit_title.setObjectName(u"lineEdit_title")

        self.gridLayout_2.addWidget(self.lineEdit_title, 1, 1, 1, 3)

        self.lineEdit_ylabel = Variable_Box(self.plotting_group)
        self.lineEdit_ylabel.setObjectName(u"lineEdit_ylabel")

        self.gridLayout_2.addWidget(self.lineEdit_ylabel, 4, 1, 1, 1)

        self.lineEdit_top_left_y = QLineEdit(self.plotting_group)
        self.lineEdit_top_left_y.setObjectName(u"lineEdit_top_left_y")

        self.gridLayout_2.addWidget(self.lineEdit_top_left_y, 10, 1, 1, 1)

        self.label_2 = QLabel(self.plotting_group)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.checkBox_show_in_browser = QCheckBox(self.plotting_group)
        self.checkBox_show_in_browser.setObjectName(u"checkBox_show_in_browser")

        self.gridLayout_2.addWidget(self.checkBox_show_in_browser, 11, 0, 1, 1)

        self.label_plot_width = QLabel(self.plotting_group)
        self.label_plot_width.setObjectName(u"label_plot_width")

        self.gridLayout_2.addWidget(self.label_plot_width, 9, 2, 1, 1)

        self.checkBox_ylog2 = QCheckBox(self.plotting_group)
        self.checkBox_ylog2.setObjectName(u"checkBox_ylog2")

        self.gridLayout_2.addWidget(self.checkBox_ylog2, 6, 2, 1, 2)

        self.label = QLabel(self.plotting_group)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.label_4 = QLabel(self.plotting_group)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 4, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 13, 0, 1, 4)

        self.checkBox_manual_plot_position = QCheckBox(self.plotting_group)
        self.checkBox_manual_plot_position.setObjectName(u"checkBox_manual_plot_position")

        self.gridLayout_2.addWidget(self.checkBox_manual_plot_position, 8, 0, 1, 1)

        self.label_port = QLabel(self.plotting_group)
        self.label_port.setObjectName(u"label_port")

        self.gridLayout_2.addWidget(self.label_port, 12, 0, 1, 1)

        self.spinBox_port = QSpinBox(self.plotting_group)
        self.spinBox_port.setObjectName(u"spinBox_port")
        self.spinBox_port.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_port.setMaximum(65536)
        self.spinBox_port.setValue(8050)

        self.gridLayout_2.addWidget(self.spinBox_port, 12, 1, 1, 1)


        self.gridLayout.addWidget(self.plotting_group, 4, 0, 5, 2)

        QWidget.setTabOrder(self.lineEdit_x_axis, self.lineEdit_nPoints)
        QWidget.setTabOrder(self.lineEdit_nPoints, self.lineEdit_title)
        QWidget.setTabOrder(self.lineEdit_title, self.lineEdit_xlabel)
        QWidget.setTabOrder(self.lineEdit_xlabel, self.lineEdit_ylabel)
        QWidget.setTabOrder(self.lineEdit_ylabel, self.lineEdit_ylabel2)
        QWidget.setTabOrder(self.lineEdit_ylabel2, self.lineEdit_top_left_x)
        QWidget.setTabOrder(self.lineEdit_top_left_x, self.lineEdit_top_left_y)
        QWidget.setTabOrder(self.lineEdit_top_left_y, self.lineEdit_plot_width)
        QWidget.setTabOrder(self.lineEdit_plot_width, self.lineEdit_plot_height)
        QWidget.setTabOrder(self.lineEdit_plot_height, self.checkBox_xlog)
        QWidget.setTabOrder(self.checkBox_xlog, self.checkBox_ylog)
        QWidget.setTabOrder(self.checkBox_ylog, self.checkBox_ylog2)
        QWidget.setTabOrder(self.checkBox_ylog2, self.checkBox_same_fit)

        self.retranslateUi(Plot_Definer)

        QMetaObject.connectSlotsByName(Plot_Definer)
    # setupUi

    def retranslateUi(self, Plot_Definer):
        Plot_Definer.setWindowTitle(QCoreApplication.translate("Plot_Definer", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("Plot_Definer", u"x-axis:", None))
        self.fit_definer.setText(QCoreApplication.translate("Plot_Definer", u"No y-axis selected", None))
        self.checkBox_same_fit.setText(QCoreApplication.translate("Plot_Definer", u"same fit for all ", None))
        self.checkBox_xlog.setText(QCoreApplication.translate("Plot_Definer", u"x logarithmic?", None))
        self.label_6.setText(QCoreApplication.translate("Plot_Definer", u"# points:", None))
        self.label_3.setText(QCoreApplication.translate("Plot_Definer", u"y-label:", None))
#if QT_CONFIG(tooltip)
        self.label_top_left_x.setToolTip(QCoreApplication.translate("Plot_Definer", u"Set the exact x coordinate of the top left corner of the plot window in pixels (min 0)", None))
#endif // QT_CONFIG(tooltip)
        self.label_top_left_x.setText(QCoreApplication.translate("Plot_Definer", u"Top Left X", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_top_left_x.setToolTip(QCoreApplication.translate("Plot_Definer", u"Minimum is 0 pixels", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lineEdit_plot_width.setToolTip(QCoreApplication.translate("Plot_Definer", u"Minimum is 430 pixels", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_top_left_y.setToolTip(QCoreApplication.translate("Plot_Definer", u"Set the exact y coordinate of the top left corner of the plot window in pixels (min 0)", None))
#endif // QT_CONFIG(tooltip)
        self.label_top_left_y.setText(QCoreApplication.translate("Plot_Definer", u"Top  Left Y", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_plot_height.setToolTip(QCoreApplication.translate("Plot_Definer", u"Minimum is 126 pixels", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_ylog.setText(QCoreApplication.translate("Plot_Definer", u"y logarithmic?", None))
#if QT_CONFIG(tooltip)
        self.label_plot_height.setToolTip(QCoreApplication.translate("Plot_Definer", u"Set the height of the plot window in pixels (min 126)", None))
#endif // QT_CONFIG(tooltip)
        self.label_plot_height.setText(QCoreApplication.translate("Plot_Definer", u"Plot Height", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_top_left_y.setToolTip(QCoreApplication.translate("Plot_Definer", u"Minimum is 0 pixels", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Plot_Definer", u"x-label:", None))
#if QT_CONFIG(tooltip)
        self.checkBox_show_in_browser.setToolTip(QCoreApplication.translate("Plot_Definer", u"Check this to make the plot available via the browser.\n"
"This will significantly increase the protocol startup time!\n"
"Reachable under 127.0.0.1:Port", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_show_in_browser.setText(QCoreApplication.translate("Plot_Definer", u"Show plot in browser", None))
#if QT_CONFIG(tooltip)
        self.label_plot_width.setToolTip(QCoreApplication.translate("Plot_Definer", u"Set the width of the plot window in pixels (min 430)", None))
#endif // QT_CONFIG(tooltip)
        self.label_plot_width.setText(QCoreApplication.translate("Plot_Definer", u"Plot Width", None))
        self.checkBox_ylog2.setText(QCoreApplication.translate("Plot_Definer", u"y2 logarithmic?", None))
        self.label.setText(QCoreApplication.translate("Plot_Definer", u"title:", None))
        self.label_4.setText(QCoreApplication.translate("Plot_Definer", u"y-label 2", None))
#if QT_CONFIG(tooltip)
        self.checkBox_manual_plot_position.setToolTip(QCoreApplication.translate("Plot_Definer", u"Check this to set the manual x&y coordinates and the size of the plot window.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_manual_plot_position.setText(QCoreApplication.translate("Plot_Definer", u"Manual plot position", None))
#if QT_CONFIG(tooltip)
        self.label_port.setToolTip(QCoreApplication.translate("Plot_Definer", u"Port of the localhost to display the plot", None))
#endif // QT_CONFIG(tooltip)
        self.label_port.setText(QCoreApplication.translate("Plot_Definer", u"Port", None))
    # retranslateUi

