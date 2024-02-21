# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_options.ui'
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
    QGridLayout,
    QHeaderView,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)


class Ui_Plot_Options(object):
    """ """

    def setupUi(self, Plot_Options):
        """

        Parameters
        ----------
        Plot_Options :


        Returns
        -------

        """
        if not Plot_Options.objectName():
            Plot_Options.setObjectName("Plot_Options")
        Plot_Options.resize(400, 283)
        self.gridLayout = QGridLayout(Plot_Options)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_log_y2 = QCheckBox(Plot_Options)
        self.checkBox_log_y2.setObjectName("checkBox_log_y2")

        self.gridLayout.addWidget(self.checkBox_log_y2, 2, 0, 1, 1)

        self.checkBox_use_abs_x = QCheckBox(Plot_Options)
        self.checkBox_use_abs_x.setObjectName("checkBox_use_abs_x")
        self.checkBox_use_abs_x.setEnabled(False)

        self.gridLayout.addWidget(self.checkBox_use_abs_x, 0, 1, 1, 1)

        self.checkBox_log_x = QCheckBox(Plot_Options)
        self.checkBox_log_x.setObjectName("checkBox_log_x")

        self.gridLayout.addWidget(self.checkBox_log_x, 0, 0, 1, 1)

        self.checkBox_use_abs_y = QCheckBox(Plot_Options)
        self.checkBox_use_abs_y.setObjectName("checkBox_use_abs_y")
        self.checkBox_use_abs_y.setEnabled(False)

        self.gridLayout.addWidget(self.checkBox_use_abs_y, 1, 1, 1, 1)

        self.checkBox_log_y = QCheckBox(Plot_Options)
        self.checkBox_log_y.setObjectName("checkBox_log_y")

        self.gridLayout.addWidget(self.checkBox_log_y, 1, 0, 1, 1)

        self.checkBox_use_abs_y2 = QCheckBox(Plot_Options)
        self.checkBox_use_abs_y2.setObjectName("checkBox_use_abs_y2")
        self.checkBox_use_abs_y2.setEnabled(False)

        self.gridLayout.addWidget(self.checkBox_use_abs_y2, 2, 1, 1, 1)

        self.tableWidget = QTableWidget(Plot_Options)
        self.tableWidget.setObjectName("tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 2)

        self.retranslateUi(Plot_Options)

        QMetaObject.connectSlotsByName(Plot_Options)

    # setupUi

    def retranslateUi(self, Plot_Options):
        """

        Parameters
        ----------
        Plot_Options :


        Returns
        -------

        """
        Plot_Options.setWindowTitle(
            QCoreApplication.translate("Plot_Options", "Form", None)
        )
        self.checkBox_log_y2.setText(
            QCoreApplication.translate("Plot_Options", "Y-Axis 2 logarithmic", None)
        )
        self.checkBox_use_abs_x.setText(
            QCoreApplication.translate("Plot_Options", "Use Absolute", None)
        )
        self.checkBox_log_x.setText(
            QCoreApplication.translate("Plot_Options", "X-Axis logarithmic", None)
        )
        self.checkBox_use_abs_y.setText(
            QCoreApplication.translate("Plot_Options", "Use Absolute", None)
        )
        self.checkBox_log_y.setText(
            QCoreApplication.translate("Plot_Options", "Y-Axis logarithmic", None)
        )
        self.checkBox_use_abs_y2.setText(
            QCoreApplication.translate("Plot_Options", "Use Absolute", None)
        )

    # retranslateUi
