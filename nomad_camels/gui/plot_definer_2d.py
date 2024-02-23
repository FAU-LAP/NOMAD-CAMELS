# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_definer_2d.ui'
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
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)

from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box


class Ui_Plot_Definer_2D(object):
    """ """

    def setupUi(self, Plot_Definer_2D):
        """

        Parameters
        ----------
        Plot_Definer_2D :


        Returns
        -------

        """
        if not Plot_Definer_2D.objectName():
            Plot_Definer_2D.setObjectName("Plot_Definer_2D")
        Plot_Definer_2D.resize(400, 222)
        self.gridLayout = QGridLayout(Plot_Definer_2D)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QLabel(Plot_Definer_2D)
        self.label_5.setObjectName("label_5")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_6 = QLabel(Plot_Definer_2D)
        self.label_6.setObjectName("label_6")
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_7 = QLabel(Plot_Definer_2D)
        self.label_7.setObjectName("label_7")
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.lineEdit_x_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_x_axis.setObjectName("lineEdit_x_axis")

        self.gridLayout.addWidget(self.lineEdit_x_axis, 2, 1, 1, 1)

        self.lineEdit_y_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_y_axis.setObjectName("lineEdit_y_axis")

        self.gridLayout.addWidget(self.lineEdit_y_axis, 3, 1, 1, 1)

        self.lineEdit_z_axis = Variable_Box(Plot_Definer_2D)
        self.lineEdit_z_axis.setObjectName("lineEdit_z_axis")

        self.gridLayout.addWidget(self.lineEdit_z_axis, 4, 1, 1, 1)

        self.lineEdit_xlabel = QLineEdit(Plot_Definer_2D)
        self.lineEdit_xlabel.setObjectName("lineEdit_xlabel")

        self.gridLayout.addWidget(self.lineEdit_xlabel, 2, 3, 1, 1)

        self.label_11 = QLabel(Plot_Definer_2D)
        self.label_11.setObjectName("label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 1, 1, 1, 1)

        self.label_10 = QLabel(Plot_Definer_2D)
        self.label_10.setObjectName("label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 4, 2, 1, 1)

        self.lineEdit_zlabel = QLineEdit(Plot_Definer_2D)
        self.lineEdit_zlabel.setObjectName("lineEdit_zlabel")

        self.gridLayout.addWidget(self.lineEdit_zlabel, 4, 3, 1, 1)

        self.label_8 = QLabel(Plot_Definer_2D)
        self.label_8.setObjectName("label_8")
        self.label_8.setFont(font)

        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)

        self.lineEdit_ylabel = QLineEdit(Plot_Definer_2D)
        self.lineEdit_ylabel.setObjectName("lineEdit_ylabel")

        self.gridLayout.addWidget(self.lineEdit_ylabel, 3, 3, 1, 1)

        self.lineEdit_title = QLineEdit(Plot_Definer_2D)
        self.lineEdit_title.setObjectName("lineEdit_title")

        self.gridLayout.addWidget(self.lineEdit_title, 0, 1, 1, 3)

        self.label_9 = QLabel(Plot_Definer_2D)
        self.label_9.setObjectName("label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

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
        """

        Parameters
        ----------
        Plot_Definer_2D :


        Returns
        -------

        """
        Plot_Definer_2D.setWindowTitle(
            QCoreApplication.translate("Plot_Definer_2D", "Form", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("Plot_Definer_2D", "x-axis:", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("Plot_Definer_2D", "y-axis:", None)
        )
        self.label_7.setText(
            QCoreApplication.translate("Plot_Definer_2D", "z-axis:", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("Plot_Definer_2D", "title:", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("Plot_Definer_2D", "z-label:", None)
        )
        self.label_8.setText(
            QCoreApplication.translate("Plot_Definer_2D", "y-label:", None)
        )
        self.label_9.setText(
            QCoreApplication.translate("Plot_Definer_2D", "x-label:", None)
        )

    # retranslateUi
