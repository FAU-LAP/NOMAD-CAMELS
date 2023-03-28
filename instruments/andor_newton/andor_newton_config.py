# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\andor_newton_config.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_andor_newton_config(object):
    def setupUi(self, andor_newton_config):
        andor_newton_config.setObjectName("andor_newton_config")
        andor_newton_config.resize(381, 479)
        self.gridLayout = QtWidgets.QGridLayout(andor_newton_config)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_5 = QtWidgets.QFrame(andor_newton_config)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_15 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 0, 0, 1, 1)
        self.set_temperature = QtWidgets.QSpinBox(self.frame_5)
        self.set_temperature.setMinimum(-99)
        self.set_temperature.setProperty("value", -60)
        self.set_temperature.setObjectName("set_temperature")
        self.gridLayout_5.addWidget(self.set_temperature, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_5, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(andor_newton_config)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox_shutter_mode = QtWidgets.QComboBox(self.frame)
        self.comboBox_shutter_mode.setObjectName("comboBox_shutter_mode")
        self.comboBox_shutter_mode.addItem("")
        self.comboBox_shutter_mode.addItem("")
        self.comboBox_shutter_mode.addItem("")
        self.comboBox_shutter_mode.addItem("")
        self.comboBox_shutter_mode.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_shutter_mode, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.exposure_time = QtWidgets.QDoubleSpinBox(self.frame)
        self.exposure_time.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.exposure_time.setDecimals(3)
        self.exposure_time.setSingleStep(0.1)
        self.exposure_time.setObjectName("exposure_time")
        self.gridLayout_2.addWidget(self.exposure_time, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(andor_newton_config)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.preamp_gain = QtWidgets.QSpinBox(self.frame_3)
        self.preamp_gain.setProperty("value", 4)
        self.preamp_gain.setObjectName("preamp_gain")
        self.gridLayout_4.addWidget(self.preamp_gain, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        self.comboBox_readout_mode = QtWidgets.QComboBox(self.frame_3)
        self.comboBox_readout_mode.setObjectName("comboBox_readout_mode")
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.addItem("")
        self.comboBox_readout_mode.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_readout_mode, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.horizontal_binning = QtWidgets.QSpinBox(self.frame_3)
        self.horizontal_binning.setSingleStep(2)
        self.horizontal_binning.setProperty("value", 4)
        self.horizontal_binning.setObjectName("horizontal_binning")
        self.gridLayout_4.addWidget(self.horizontal_binning, 6, 0, 1, 1)
        self.hs_speed = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.hs_speed.setProperty("value", 0.05)
        self.hs_speed.setObjectName("hs_speed")
        self.gridLayout_4.addWidget(self.hs_speed, 8, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 7, 0, 1, 1)
        self.vs_speed = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.vs_speed.setProperty("value", 25.7)
        self.vs_speed.setObjectName("vs_speed")
        self.gridLayout_4.addWidget(self.vs_speed, 10, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 11, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.frame_3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 9, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(andor_newton_config)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.start_row = QtWidgets.QSpinBox(self.frame_2)
        self.start_row.setMaximum(999)
        self.start_row.setProperty("value", 95)
        self.start_row.setObjectName("start_row")
        self.gridLayout_3.addWidget(self.start_row, 7, 0, 1, 1)
        self.track_height = QtWidgets.QSpinBox(self.frame_2)
        self.track_height.setObjectName("track_height")
        self.gridLayout_3.addWidget(self.track_height, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.frame_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 6, 0, 1, 1)
        self.number_of_tracks = QtWidgets.QSpinBox(self.frame_2)
        self.number_of_tracks.setObjectName("number_of_tracks")
        self.gridLayout_3.addWidget(self.number_of_tracks, 2, 0, 1, 1)
        self.pushButton_create_tracks = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_create_tracks.setObjectName("pushButton_create_tracks")
        self.gridLayout_3.addWidget(self.pushButton_create_tracks, 5, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.frame_2)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 8, 0, 1, 1)
        self.end_row = QtWidgets.QSpinBox(self.frame_2)
        self.end_row.setMaximum(999)
        self.end_row.setProperty("value", 120)
        self.end_row.setObjectName("end_row")
        self.gridLayout_3.addWidget(self.end_row, 9, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 10, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 1, 2, 1)
        self.frame_4 = QtWidgets.QFrame(andor_newton_config)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_16 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.gridLayout_6.addWidget(self.label_16, 0, 0, 1, 1)
        self.serial_number = QtWidgets.QSpinBox(self.frame_4)
        self.serial_number.setMaximum(99999999)
        self.serial_number.setObjectName("serial_number")
        self.gridLayout_6.addWidget(self.serial_number, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 0, 1, 1, 1)

        self.retranslateUi(andor_newton_config)
        QtCore.QMetaObject.connectSlotsByName(andor_newton_config)
        andor_newton_config.setTabOrder(self.set_temperature, self.exposure_time)
        andor_newton_config.setTabOrder(self.exposure_time, self.preamp_gain)
        andor_newton_config.setTabOrder(self.preamp_gain, self.horizontal_binning)
        andor_newton_config.setTabOrder(self.horizontal_binning, self.hs_speed)
        andor_newton_config.setTabOrder(self.hs_speed, self.vs_speed)
        andor_newton_config.setTabOrder(self.vs_speed, self.number_of_tracks)
        andor_newton_config.setTabOrder(self.number_of_tracks, self.track_height)
        andor_newton_config.setTabOrder(self.track_height, self.start_row)
        andor_newton_config.setTabOrder(self.start_row, self.end_row)
        andor_newton_config.setTabOrder(self.end_row, self.serial_number)
        andor_newton_config.setTabOrder(self.serial_number, self.comboBox_shutter_mode)
        andor_newton_config.setTabOrder(self.comboBox_shutter_mode, self.comboBox_readout_mode)
        andor_newton_config.setTabOrder(self.comboBox_readout_mode, self.pushButton_create_tracks)

    def retranslateUi(self, andor_newton_config):
        _translate = QtCore.QCoreApplication.translate
        andor_newton_config.setWindowTitle(_translate("andor_newton_config", "Form"))
        self.label_15.setText(_translate("andor_newton_config", "Temperature (┬░C)"))
        self.label.setText(_translate("andor_newton_config", "Exposure"))
        self.comboBox_shutter_mode.setItemText(0, _translate("andor_newton_config", "Open for any series"))
        self.comboBox_shutter_mode.setItemText(1, _translate("andor_newton_config", "Open for FVB series"))
        self.comboBox_shutter_mode.setItemText(2, _translate("andor_newton_config", "Permanently closed"))
        self.comboBox_shutter_mode.setItemText(3, _translate("andor_newton_config", "Permanently open"))
        self.comboBox_shutter_mode.setItemText(4, _translate("andor_newton_config", "Fully Auto"))
        self.label_5.setText(_translate("andor_newton_config", "Exposure Time (s)"))
        self.label_4.setText(_translate("andor_newton_config", "Shutter Mode"))
        self.label_8.setText(_translate("andor_newton_config", "Readout Mode"))
        self.comboBox_readout_mode.setItemText(0, _translate("andor_newton_config", "FVB - Full Vertical Binning"))
        self.comboBox_readout_mode.setItemText(1, _translate("andor_newton_config", "Multi Track"))
        self.comboBox_readout_mode.setItemText(2, _translate("andor_newton_config", "Random Track"))
        self.comboBox_readout_mode.setItemText(3, _translate("andor_newton_config", "Single Track"))
        self.comboBox_readout_mode.setItemText(4, _translate("andor_newton_config", "Image"))
        self.label_9.setText(_translate("andor_newton_config", "Preamp Gain"))
        self.label_3.setText(_translate("andor_newton_config", "Readout"))
        self.label_11.setText(_translate("andor_newton_config", "HS Speed (MHz)"))
        self.label_12.setText(_translate("andor_newton_config", "VS Speed (┬Ás/shift)"))
        self.label_10.setText(_translate("andor_newton_config", "Horizontal Binning"))
        self.label_6.setText(_translate("andor_newton_config", "Number of Tracks"))
        self.label_7.setText(_translate("andor_newton_config", "Track Height"))
        self.label_13.setText(_translate("andor_newton_config", "Start Row"))
        self.pushButton_create_tracks.setText(_translate("andor_newton_config", "Create Tracks"))
        self.label_14.setText(_translate("andor_newton_config", "End Row"))
        self.label_2.setText(_translate("andor_newton_config", "Tracks"))
        self.label_16.setText(_translate("andor_newton_config", "Serial Number"))
