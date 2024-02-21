# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gradient_descent_step.ui'
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
    QComboBox,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box


class Ui_Grad_Desc(object):
    """ """

    def setupUi(self, Grad_Desc):
        """

        Parameters
        ----------
        Grad_Desc :


        Returns
        -------

        """
        if not Grad_Desc.objectName():
            Grad_Desc.setObjectName("Grad_Desc")
        Grad_Desc.resize(400, 300)
        self.gridLayout = QGridLayout(Grad_Desc)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(Grad_Desc)
        self.label_12.setObjectName("label_12")

        self.gridLayout.addWidget(self.label_12, 8, 2, 1, 1)

        self.lineEdit_learning_rate = Variable_Box(Grad_Desc)
        self.lineEdit_learning_rate.setObjectName("lineEdit_learning_rate")

        self.gridLayout.addWidget(self.lineEdit_learning_rate, 7, 0, 1, 1)

        self.label_5 = QLabel(Grad_Desc)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)

        self.label = QLabel(Grad_Desc)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_9 = QLabel(Grad_Desc)
        self.label_9.setObjectName("label_9")

        self.gridLayout.addWidget(self.label_9, 6, 2, 1, 1)

        self.label_3 = QLabel(Grad_Desc)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_10 = QLabel(Grad_Desc)
        self.label_10.setObjectName("label_10")

        self.gridLayout.addWidget(self.label_10, 8, 0, 1, 1)

        self.label_11 = QLabel(Grad_Desc)
        self.label_11.setObjectName("label_11")

        self.gridLayout.addWidget(self.label_11, 8, 1, 1, 1)

        self.label_2 = QLabel(Grad_Desc)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_opt_func = Variable_Box(Grad_Desc)
        self.lineEdit_opt_func.setObjectName("lineEdit_opt_func")

        self.gridLayout.addWidget(self.lineEdit_opt_func, 2, 1, 1, 2)

        self.lineEdit_max_val = Variable_Box(Grad_Desc)
        self.lineEdit_max_val.setObjectName("lineEdit_max_val")

        self.gridLayout.addWidget(self.lineEdit_max_val, 5, 2, 1, 1)

        self.label_6 = QLabel(Grad_Desc)
        self.label_6.setObjectName("label_6")

        self.gridLayout.addWidget(self.label_6, 4, 2, 1, 1)

        self.checkBox_plot_steps = QCheckBox(Grad_Desc)
        self.checkBox_plot_steps.setObjectName("checkBox_plot_steps")

        self.gridLayout.addWidget(self.checkBox_plot_steps, 3, 0, 1, 3)

        self.lineEdit_min_val = Variable_Box(Grad_Desc)
        self.lineEdit_min_val.setObjectName("lineEdit_min_val")

        self.gridLayout.addWidget(self.lineEdit_min_val, 5, 1, 1, 1)

        self.lineEdit_starting_val = Variable_Box(Grad_Desc)
        self.lineEdit_starting_val.setObjectName("lineEdit_starting_val")

        self.gridLayout.addWidget(self.lineEdit_starting_val, 5, 0, 1, 1)

        self.lineEdit_momentum = Variable_Box(Grad_Desc)
        self.lineEdit_momentum.setObjectName("lineEdit_momentum")

        self.gridLayout.addWidget(self.lineEdit_momentum, 7, 2, 1, 1)

        self.lineEdit_largest_step = Variable_Box(Grad_Desc)
        self.lineEdit_largest_step.setObjectName("lineEdit_largest_step")

        self.gridLayout.addWidget(self.lineEdit_largest_step, 9, 1, 1, 1)

        self.label_8 = QLabel(Grad_Desc)
        self.label_8.setObjectName("label_8")

        self.gridLayout.addWidget(self.label_8, 6, 1, 1, 1)

        self.lineEdit_threshold = Variable_Box(Grad_Desc)
        self.lineEdit_threshold.setObjectName("lineEdit_threshold")

        self.gridLayout.addWidget(self.lineEdit_threshold, 7, 1, 1, 1)

        self.comboBox_output_channel = QComboBox(Grad_Desc)
        self.comboBox_output_channel.setObjectName("comboBox_output_channel")

        self.gridLayout.addWidget(self.comboBox_output_channel, 1, 1, 1, 2)

        self.lineEdit_smallest_step = Variable_Box(Grad_Desc)
        self.lineEdit_smallest_step.setObjectName("lineEdit_smallest_step")

        self.gridLayout.addWidget(self.lineEdit_smallest_step, 9, 0, 1, 1)

        self.comboBox_extremum_type = QComboBox(Grad_Desc)
        self.comboBox_extremum_type.setObjectName("comboBox_extremum_type")

        self.gridLayout.addWidget(self.comboBox_extremum_type, 0, 1, 1, 2)

        self.lineEdit_max_n_steps = Variable_Box(Grad_Desc)
        self.lineEdit_max_n_steps.setObjectName("lineEdit_max_n_steps")

        self.gridLayout.addWidget(self.lineEdit_max_n_steps, 9, 2, 1, 1)

        self.label_4 = QLabel(Grad_Desc)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_7 = QLabel(Grad_Desc)
        self.label_7.setObjectName("label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        QWidget.setTabOrder(self.comboBox_extremum_type, self.comboBox_output_channel)
        QWidget.setTabOrder(self.comboBox_output_channel, self.lineEdit_opt_func)
        QWidget.setTabOrder(self.lineEdit_opt_func, self.checkBox_plot_steps)
        QWidget.setTabOrder(self.checkBox_plot_steps, self.lineEdit_starting_val)
        QWidget.setTabOrder(self.lineEdit_starting_val, self.lineEdit_min_val)
        QWidget.setTabOrder(self.lineEdit_min_val, self.lineEdit_max_val)
        QWidget.setTabOrder(self.lineEdit_max_val, self.lineEdit_learning_rate)
        QWidget.setTabOrder(self.lineEdit_learning_rate, self.lineEdit_threshold)
        QWidget.setTabOrder(self.lineEdit_threshold, self.lineEdit_momentum)
        QWidget.setTabOrder(self.lineEdit_momentum, self.lineEdit_smallest_step)
        QWidget.setTabOrder(self.lineEdit_smallest_step, self.lineEdit_largest_step)
        QWidget.setTabOrder(self.lineEdit_largest_step, self.lineEdit_max_n_steps)

        self.retranslateUi(Grad_Desc)

        QMetaObject.connectSlotsByName(Grad_Desc)

    # setupUi

    def retranslateUi(self, Grad_Desc):
        """

        Parameters
        ----------
        Grad_Desc :


        Returns
        -------

        """
        Grad_Desc.setWindowTitle(QCoreApplication.translate("Grad_Desc", "Form", None))
        self.label_12.setText(
            QCoreApplication.translate("Grad_Desc", "Max Number of Steps", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("Grad_Desc", "Minimum Value", None)
        )
        self.label.setText(
            QCoreApplication.translate("Grad_Desc", "Extremum-Type:", None)
        )
        self.label_9.setText(QCoreApplication.translate("Grad_Desc", "Momentum", None))
        self.label_3.setText(
            QCoreApplication.translate("Grad_Desc", "Optimization Function:", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("Grad_Desc", "Smallest Step", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("Grad_Desc", "Largest Step", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("Grad_Desc", "Output-Channel:", None)
        )
        self.label_6.setText(
            QCoreApplication.translate("Grad_Desc", "Maximum Value", None)
        )
        self.checkBox_plot_steps.setText(
            QCoreApplication.translate("Grad_Desc", "Plot Steps", None)
        )
        self.label_8.setText(QCoreApplication.translate("Grad_Desc", "Threshold", None))
        self.label_4.setText(
            QCoreApplication.translate("Grad_Desc", "Starting Value", None)
        )
        self.label_7.setText(
            QCoreApplication.translate("Grad_Desc", "Learning Rate", None)
        )

    # retranslateUi
