# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_definer.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box


class Ui_Plot_Definer(object):
    def setupUi(self, Plot_Definer):
        if not Plot_Definer.objectName():
            Plot_Definer.setObjectName("Plot_Definer")
        Plot_Definer.resize(470, 350)
        self.gridLayout = QGridLayout(Plot_Definer)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_x_axis = Variable_Box(Plot_Definer)
        self.lineEdit_x_axis.setObjectName("lineEdit_x_axis")

        self.gridLayout.addWidget(self.lineEdit_x_axis, 0, 1, 1, 3)

        self.label_5 = QLabel(Plot_Definer)
        self.label_5.setObjectName("label_5")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.line = QFrame(Plot_Definer)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 3, 0, 1, 4)

        self.fit_definer = QLabel(Plot_Definer)
        self.fit_definer.setObjectName("fit_definer")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        self.fit_definer.setFont(font1)

        self.gridLayout.addWidget(self.fit_definer, 5, 3, 4, 1)

        self.checkBox_same_fit = QCheckBox(Plot_Definer)
        self.checkBox_same_fit.setObjectName("checkBox_same_fit")

        self.gridLayout.addWidget(self.checkBox_same_fit, 4, 3, 1, 1)

        self.y_axes = QWidget(Plot_Definer)
        self.y_axes.setObjectName("y_axes")

        self.gridLayout.addWidget(self.y_axes, 1, 0, 1, 4)

        self.line_2 = QFrame(Plot_Definer)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 4, 2, 5, 1)

        self.plotting_group = QWidget(Plot_Definer)
        self.plotting_group.setObjectName("plotting_group")
        self.gridLayout_2 = QGridLayout(self.plotting_group)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_title = QLineEdit(self.plotting_group)
        self.lineEdit_title.setObjectName("lineEdit_title")

        self.gridLayout_2.addWidget(self.lineEdit_title, 1, 1, 1, 3)

        self.verticalSpacer = QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_2.addItem(self.verticalSpacer, 7, 0, 1, 4)

        self.label_2 = QLabel(self.plotting_group)
        self.label_2.setObjectName("label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.checkBox_xlog = QCheckBox(self.plotting_group)
        self.checkBox_xlog.setObjectName("checkBox_xlog")

        self.gridLayout_2.addWidget(self.checkBox_xlog, 3, 0, 1, 4)

        self.checkBox_ylog = QCheckBox(self.plotting_group)
        self.checkBox_ylog.setObjectName("checkBox_ylog")

        self.gridLayout_2.addWidget(self.checkBox_ylog, 6, 0, 1, 2)

        self.label_4 = QLabel(self.plotting_group)
        self.label_4.setObjectName("label_4")

        self.gridLayout_2.addWidget(self.label_4, 4, 2, 1, 1)

        self.checkBox_ylog2 = QCheckBox(self.plotting_group)
        self.checkBox_ylog2.setObjectName("checkBox_ylog2")

        self.gridLayout_2.addWidget(self.checkBox_ylog2, 6, 2, 1, 2)

        self.label = QLabel(self.plotting_group)
        self.label.setObjectName("label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.label_3 = QLabel(self.plotting_group)
        self.label_3.setObjectName("label_3")

        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)

        self.lineEdit_ylabel2 = QLineEdit(self.plotting_group)
        self.lineEdit_ylabel2.setObjectName("lineEdit_ylabel2")

        self.gridLayout_2.addWidget(self.lineEdit_ylabel2, 4, 3, 1, 1)

        self.lineEdit_xlabel = QLineEdit(self.plotting_group)
        self.lineEdit_xlabel.setObjectName("lineEdit_xlabel")

        self.gridLayout_2.addWidget(self.lineEdit_xlabel, 2, 1, 1, 3)

        self.lineEdit_ylabel = QLineEdit(self.plotting_group)
        self.lineEdit_ylabel.setObjectName("lineEdit_ylabel")

        self.gridLayout_2.addWidget(self.lineEdit_ylabel, 4, 1, 1, 1)

        self.label_6 = QLabel(self.plotting_group)
        self.label_6.setObjectName("label_6")

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.lineEdit_nPoints = QLineEdit(self.plotting_group)
        self.lineEdit_nPoints.setObjectName("lineEdit_nPoints")

        self.gridLayout_2.addWidget(self.lineEdit_nPoints, 0, 1, 1, 3)

        self.gridLayout.addWidget(self.plotting_group, 4, 0, 5, 2)

        self.retranslateUi(Plot_Definer)

        QMetaObject.connectSlotsByName(Plot_Definer)

    # setupUi

    def retranslateUi(self, Plot_Definer):
        Plot_Definer.setWindowTitle(
            QCoreApplication.translate("Plot_Definer", "Form", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("Plot_Definer", "x-axis:", None)
        )
        self.fit_definer.setText(
            QCoreApplication.translate("Plot_Definer", "No y-axis selected", None)
        )
        self.checkBox_same_fit.setText(
            QCoreApplication.translate("Plot_Definer", "same fit for all ", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("Plot_Definer", "x-label:", None)
        )
        self.checkBox_xlog.setText(
            QCoreApplication.translate("Plot_Definer", "x logarithmic?", None)
        )
        self.checkBox_ylog.setText(
            QCoreApplication.translate("Plot_Definer", "y logarithmic?", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("Plot_Definer", "y-label 2", None)
        )
        self.checkBox_ylog2.setText(
            QCoreApplication.translate("Plot_Definer", "y2 logarithmic?", None)
        )
        self.label.setText(QCoreApplication.translate("Plot_Definer", "title:", None))
        self.label_3.setText(
            QCoreApplication.translate("Plot_Definer", "y-label:", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("Plot_Definer", "# points:", None)
        )

    # retranslateUi
