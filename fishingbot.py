"""
(c) 2021 yy4n (https://github.com/yy4n)
This code is licensed under the MIT license (see LICENSE file for details)

This program automates the task of fishing in the video game 'Terraria' by clicking on the screen and reeling in the fishing pole as soon as movement is detected.
It can also accomplish several other tasks related to fishing.
For more information and a detailed guide, see https://github.com/yy4n/Terraria-Fishing-Bot
"""

import time
import threading
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PIL import ImageGrab
from PIL.ImageQt import ImageQt

import pyautogui
import keyboard

icon_path = "icon.png"

class Ui_Instructions_dialog(object):
    """The dialog for instructions. Opened from 'Ui_MainWindow'"""
    def __init__(self, quickstack, crates):
        self.q = quickstack
        self.c = crates
    
    def setupUi(self, Instructions_dialog):
        Instructions_dialog.setObjectName("Instructions_dialog")
        Instructions_dialog.resize(450, 340)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Instructions_dialog.sizePolicy().hasHeightForWidth())
        Instructions_dialog.setSizePolicy(sizePolicy)
        Instructions_dialog.setMinimumSize(QtCore.QSize(450, 340))
        Instructions_dialog.setMaximumSize(QtCore.QSize(450, 340))
        icon = QtGui.QIcon(icon_path)
        Instructions_dialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Instructions_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 300, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Instructions_dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 431, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout_instructions = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.layout_instructions.setContentsMargins(0, 0, 0, 0)
        self.layout_instructions.setObjectName("layout_instructions")
        self.text_general = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.text_general.setWordWrap(True)
        self.text_general.setIndent(-1)
        self.text_general.setObjectName("text_general")
        self.layout_instructions.addWidget(self.text_general)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layout_instructions.addWidget(self.line)
        self.text_quickstacking = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.text_quickstacking.setWordWrap(True)
        self.text_quickstacking.setObjectName("text_quickstacking")
        self.layout_instructions.addWidget(self.text_quickstacking)
        self.text_crates = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.text_crates.setEnabled(True)
        self.text_crates.setWordWrap(True)
        self.text_crates.setObjectName("text_crates")
        self.layout_instructions.addWidget(self.text_crates)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.layout_instructions.addWidget(self.line_2)
        self.text_alt = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.text_alt.setWordWrap(True)
        self.text_alt.setObjectName("text_alt")
        self.layout_instructions.addWidget(self.text_alt)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_instructions.addItem(spacerItem)

        self.text_quickstacking.setHidden(not self.q or self.c)
        self.text_crates.setHidden(not self.c)
        self.line_2.setHidden(not self.c and not self.q)

        self.retranslateUi(Instructions_dialog)
        self.buttonBox.accepted.connect(Instructions_dialog.accept)
        self.buttonBox.rejected.connect(Instructions_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Instructions_dialog)

    def retranslateUi(self, Instructions_dialog):
        _translate = QtCore.QCoreApplication.translate
        Instructions_dialog.setWindowTitle(_translate("Instructions_dialog", "Terraria Fishing Bot - Instructions"))
        self.buttonBox.setToolTip(_translate("Instructions_dialog", "Have you read everything yet?"))
        self.text_general.setText(_translate("Instructions_dialog", "Open Terraria in fullscreen mode. Position yourself above a fishing lake and take out your fishing pole. Do not throw it. The bot will do that for you. For the best auto-fishing experience, go to Settings>Video>Waves Quality and turn off waves."))
        self.text_quickstacking.setText(_translate("Instructions_dialog", "<html><head/><body><p>You have enabled <span style=\" font-weight:600;\">quickstacking</span>. Let your inventory open while fishing. It is recommended that you have at least one chest for every obtainable item near you.</p></body></html>"))
        self.text_crates.setText(_translate("Instructions_dialog", "<html><head/><body><p>You have enabled <span style=\" font-weight:600;\">opening crates</span>. Let your inventory open while fishing and clear the bottom right spot and as much space as possible. The hotbar has to be filled.</p><p>It is adviced that you have at least one chest for every fish and every item you can obtain from crates near you. Otherwise, you will soon run out of space in your inventory and you might loose items and fishing time.</p><p>You can get bait from crates that will prolong your fishing time. Just be sure to not have any chests with bait or crates in them around you, as the bot will quickstack them otherwise.</p></body></html>"))
        self.text_alt.setText(_translate("Instructions_dialog", "<html><head/><body><p><span style=\" font-weight:600;\">As soon as you are ready, press OK. After that, position your mouse cursor with the tip at the surface of the liquid, then press ALT.</span></p></body></html>"))



class Ui_MainWindow(object):
    """The Main UI

    Also contains the bot logic and the settings
    """
    def setupUi(self, MainWindow):
        """Setup UI

        made using PyQt5 Designer (Created by: PyQt5 UI code generator 5.15.4)
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(500, 330)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(500, 330))
        MainWindow.setMaximumSize(QtCore.QSize(500, 330))
        icon = QtGui.QIcon(icon_path)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip("")
        MainWindow.setToolTipDuration(-1)
        MainWindow.setAnimated(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 241, 146))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout_settings = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.layout_settings.setContentsMargins(0, 0, 0, 0)
        self.layout_settings.setObjectName("layout_settings")
        self.text_settings = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_settings.sizePolicy().hasHeightForWidth())
        self.text_settings.setSizePolicy(sizePolicy)
        self.text_settings.setTextFormat(QtCore.Qt.MarkdownText)
        self.text_settings.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.text_settings.setIndent(-1)
        self.text_settings.setObjectName("text_settings")
        self.layout_settings.addWidget(self.text_settings)
        self.checkBox_bloodmoon = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_bloodmoon.setEnabled(True)
        self.checkBox_bloodmoon.setToolTipDuration(-1)
        self.checkBox_bloodmoon.setChecked(True)
        self.checkBox_bloodmoon.setObjectName("checkBox_bloodmoon")
        self.layout_settings.addWidget(self.checkBox_bloodmoon)
        self.layout_buffs = QtWidgets.QHBoxLayout()
        self.layout_buffs.setContentsMargins(-1, 0, -1, -1)
        self.layout_buffs.setObjectName("layout_buffs")
        self.checkBox_buffs = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_buffs.setObjectName("checkBox_buffs")
        self.layout_buffs.addWidget(self.checkBox_buffs)
        self.spinBox_buffs = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_buffs.setMinimum(1)
        self.spinBox_buffs.setMaximum(60)
        self.spinBox_buffs.setProperty("value", 3)
        self.spinBox_buffs.setObjectName("spinBox_buffs")
        self.layout_buffs.addWidget(self.spinBox_buffs)
        self.text_buffs = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_buffs.sizePolicy().hasHeightForWidth())
        self.text_buffs.setSizePolicy(sizePolicy)
        self.text_buffs.setObjectName("text_buffs")
        self.layout_buffs.addWidget(self.text_buffs)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_buffs.addItem(spacerItem)
        self.layout_settings.addLayout(self.layout_buffs)
        self.checkBox_quickstack = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_quickstack.setObjectName("checkBox_quickstack")
        self.layout_settings.addWidget(self.checkBox_quickstack)
        self.checkBox_crates = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_crates.setObjectName("checkBox_crates")
        self.layout_settings.addWidget(self.checkBox_crates)
        self.layout_contrast = QtWidgets.QHBoxLayout()
        self.layout_contrast.setObjectName("layout_contrast")
        self.text_contrast = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_contrast.sizePolicy().hasHeightForWidth())
        self.text_contrast.setSizePolicy(sizePolicy)
        self.text_contrast.setScaledContents(False)
        self.text_contrast.setIndent(18)
        self.text_contrast.setObjectName("text_contrast")
        self.layout_contrast.addWidget(self.text_contrast)
        self.spinBox_contrast = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_contrast.sizePolicy().hasHeightForWidth())
        self.spinBox_contrast.setSizePolicy(sizePolicy)
        self.spinBox_contrast.setMinimum(50)
        self.spinBox_contrast.setMaximum(2000)
        self.spinBox_contrast.setSingleStep(5)
        self.spinBox_contrast.setProperty("value", 400)
        self.spinBox_contrast.setObjectName("spinBox_contrast")
        self.layout_contrast.addWidget(self.spinBox_contrast)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_contrast.addItem(spacerItem1)
        self.layout_settings.addLayout(self.layout_contrast)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_settings.addItem(spacerItem2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(270, 10, 61, 90))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.layout_liquid = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.layout_liquid.setContentsMargins(0, 0, 0, 0)
        self.layout_liquid.setObjectName("layout_liquid")
        self.text_liquid = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_liquid.sizePolicy().hasHeightForWidth())
        self.text_liquid.setSizePolicy(sizePolicy)
        self.text_liquid.setTextFormat(QtCore.Qt.MarkdownText)
        self.text_liquid.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.text_liquid.setObjectName("text_liquid")
        self.layout_liquid.addWidget(self.text_liquid)
        self.radioButton_water = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.radioButton_water.setChecked(True)
        self.radioButton_water.setObjectName("radioButton_water")
        self.layout_liquid.addWidget(self.radioButton_water)
        self.radioButton_lava = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.radioButton_lava.setObjectName("radioButton_lava")
        self.layout_liquid.addWidget(self.radioButton_lava)
        self.radioButton_honey = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.radioButton_honey.setObjectName("radioButton_honey")
        self.layout_liquid.addWidget(self.radioButton_honey)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_liquid.addItem(spacerItem3)
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(280, 250, 201, 41))
        self.button_start.setObjectName("button_start")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 193, 241, 114))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.layout_screen_settings = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.layout_screen_settings.setContentsMargins(0, 0, 0, 0)
        self.layout_screen_settings.setObjectName("layout_screen_settings")
        self.text_screen_settings = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_screen_settings.sizePolicy().hasHeightForWidth())
        self.text_screen_settings.setSizePolicy(sizePolicy)
        self.text_screen_settings.setTextFormat(QtCore.Qt.MarkdownText)
        self.text_screen_settings.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.text_screen_settings.setObjectName("text_screen_settings")
        self.layout_screen_settings.addWidget(self.text_screen_settings)
        self.layout_quickstack_position = QtWidgets.QHBoxLayout()
        self.layout_quickstack_position.setObjectName("layout_quickstack_position")
        self.text_quickstack_position = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_quickstack_position.sizePolicy().hasHeightForWidth())
        self.text_quickstack_position.setSizePolicy(sizePolicy)
        self.text_quickstack_position.setMinimumSize(QtCore.QSize(125, 0))
        self.text_quickstack_position.setObjectName("text_quickstack_position")
        self.layout_quickstack_position.addWidget(self.text_quickstack_position)
        self.label_quickstack_position = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_quickstack_position.sizePolicy().hasHeightForWidth())
        self.label_quickstack_position.setSizePolicy(sizePolicy)
        self.label_quickstack_position.setObjectName("label_quickstack_position")
        self.layout_quickstack_position.addWidget(self.label_quickstack_position)
        self.button_quickstack_position = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_quickstack_position.sizePolicy().hasHeightForWidth())
        self.button_quickstack_position.setSizePolicy(sizePolicy)
        self.button_quickstack_position.setObjectName("button_quickstack_position")
        self.layout_quickstack_position.addWidget(self.button_quickstack_position)
        self.layout_screen_settings.addLayout(self.layout_quickstack_position)
        self.layout_sort_position = QtWidgets.QHBoxLayout()
        self.layout_sort_position.setObjectName("layout_sort_position")
        self.text_sort_position = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_sort_position.sizePolicy().hasHeightForWidth())
        self.text_sort_position.setSizePolicy(sizePolicy)
        self.text_sort_position.setMinimumSize(QtCore.QSize(125, 0))
        self.text_sort_position.setObjectName("text_sort_position")
        self.layout_sort_position.addWidget(self.text_sort_position)
        self.label_sort_position = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_sort_position.setObjectName("label_sort_position")
        self.layout_sort_position.addWidget(self.label_sort_position)
        self.button_sort_position = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.button_sort_position.setObjectName("button_sort_position")
        self.layout_sort_position.addWidget(self.button_sort_position)
        self.layout_screen_settings.addLayout(self.layout_sort_position)
        self.layout_slot_position = QtWidgets.QHBoxLayout()
        self.layout_slot_position.setObjectName("layout_slot_position")
        self.text_slot_position = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_slot_position.sizePolicy().hasHeightForWidth())
        self.text_slot_position.setSizePolicy(sizePolicy)
        self.text_slot_position.setMinimumSize(QtCore.QSize(125, 0))
        self.text_slot_position.setObjectName("text_slot_position")
        self.layout_slot_position.addWidget(self.text_slot_position)
        self.label_slot_position = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_slot_position.setObjectName("label_slot_position")
        self.layout_slot_position.addWidget(self.label_slot_position)
        self.button_slot_position = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.button_slot_position.setObjectName("button_slot_position")
        self.layout_slot_position.addWidget(self.button_slot_position)
        self.layout_screen_settings.addLayout(self.layout_slot_position)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout_screen_settings.addItem(spacerItem4)
        self.debug_image = QtWidgets.QLabel(self.centralwidget)
        self.debug_image.setGeometry(QtCore.QRect(280, 130, 200, 100))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.debug_image.sizePolicy().hasHeightForWidth())
        self.debug_image.setSizePolicy(sizePolicy)
        self.debug_image.setMinimumSize(QtCore.QSize(200, 100))
        self.debug_image.setMaximumSize(QtCore.QSize(200, 100))
        self.debug_image.setText("")
        self.debug_image.setObjectName("debug_image")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(280, 170, 201, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.text_info = QtWidgets.QLabel(self.centralwidget)
        self.text_info.setGeometry(QtCore.QRect(350, 10, 140, 91))
        self.text_info.setTextFormat(QtCore.Qt.AutoText)
        self.text_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.text_info.setWordWrap(True)
        self.text_info.setObjectName("text_info")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(250, 10, 21, 301))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(10, 160, 251, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(330, 10, 20, 101))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(260, 100, 231, 21))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.text_stop = QtWidgets.QLabel(self.centralwidget)
        self.text_stop.setGeometry(QtCore.QRect(280, 290, 201, 16))
        self.text_stop.setAlignment(QtCore.Qt.AlignCenter)
        self.text_stop.setIndent(-1)
        self.text_stop.setObjectName("text_stop")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.text_stop.setHidden(True)
        self.text_info.setOpenExternalLinks(True)
        
        # events
        self.button_quickstack_position.clicked.connect(self.on_quickstack_position_clicked)
        self.button_sort_position.clicked.connect(self.on_sort_position_clicked)
        self.button_slot_position.clicked.connect(self.on_slot_position_clicked)
        self.button_start.clicked.connect(self.on_start_clicked)
        
        self.checkBox_bloodmoon.stateChanged.connect(self.on_setting_changed)
        self.checkBox_buffs.stateChanged.connect(self.on_setting_changed)
        self.spinBox_buffs.valueChanged.connect(self.on_setting_changed)
        self.checkBox_quickstack.stateChanged.connect(self.on_setting_changed)
        self.checkBox_crates.stateChanged.connect(self.on_setting_changed)

        self.radioButton_water.toggled.connect(self.on_setting_changed)
        self.radioButton_lava.toggled.connect(self.on_setting_changed)
        self.radioButton_honey.toggled.connect(self.on_setting_changed)

        # settings setup
        self.get_settings()
        self.settings_set_enabled(True)
        
        self.pos_quickstack = (565, 280)
        self.pos_sort = (600, 280)
        self.pos_slot = (520, 250)
        self.refresh_positions()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Terraria Fishing Bot"))
        self.text_settings.setText(_translate("MainWindow", "**Settings**"))
        self.checkBox_bloodmoon.setToolTip(_translate("MainWindow", "The bot stops fishing on bloodmoon to avoid blood moon enemies."))
        self.checkBox_bloodmoon.setText(_translate("MainWindow", "Stop fishing on blood moon"))
        self.checkBox_buffs.setToolTip(_translate("MainWindow", "The bot will press \'b\' periodically as specified. This can be used to automatically consume fishing potions."))
        self.checkBox_buffs.setText(_translate("MainWindow", "Take buffs every"))
        self.spinBox_buffs.setToolTip(_translate("MainWindow", "The bot will press \'b\' periodically as specified. This can be used to automatically consume fishing potions."))
        self.text_buffs.setToolTip(_translate("MainWindow", "The bot will press \'b\' periodically as specified. This can be used to automatically consume fishing potions."))
        self.text_buffs.setText(_translate("MainWindow", "minutes"))
        self.checkBox_quickstack.setToolTip(_translate("MainWindow", "<html><head/><body><p>The bot will press the \'Quickstack to nearby chests\' button in the inventory after each catch. Make sure to open your inventory when using this.</p></body></html>"))
        self.checkBox_quickstack.setText(_translate("MainWindow", "Quickstack"))
        self.checkBox_crates.setToolTip(_translate("MainWindow", "The bot will attempt to open crates by pressing the last inventory slot after each catch. Then it will sort the inventory and quickstack to nearby chests. Make sure to have your inventory open when using this."))
        self.checkBox_crates.setText(_translate("MainWindow", "Open crates"))
        self.text_contrast.setToolTip(_translate("MainWindow", "Lower the contrast if the bot does not catch every fish, raise it if it reels in the pole when there is no fish on the pole."))
        self.text_contrast.setText(_translate("MainWindow", "Contrast: "))
        self.spinBox_contrast.setToolTip(_translate("MainWindow", "Lower the contrast if the bot does not catch every fish, raise it if it reels in the pole when there is no fish on the pole."))
        self.text_liquid.setToolTip(_translate("MainWindow", "The liquid to fish in"))
        self.text_liquid.setText(_translate("MainWindow", "**Liquid**"))
        self.radioButton_water.setText(_translate("MainWindow", "Water"))
        self.radioButton_lava.setToolTip(_translate("MainWindow", "You need special items to fish in lava."))
        self.radioButton_lava.setText(_translate("MainWindow", "Lava"))
        self.radioButton_honey.setText(_translate("MainWindow", "Honey"))
        self.button_start.setText(_translate("MainWindow", "Start"))
        self.text_screen_settings.setToolTip(_translate("MainWindow", "Only change these if your screen resolution is not 1920x1080px or if the bot does not click on the right spot for some reason."))
        self.text_screen_settings.setText(_translate("MainWindow", "**Screen settings**"))
        self.text_quickstack_position.setText(_translate("MainWindow", "Quickstack button: "))
        self.label_quickstack_position.setText(_translate("MainWindow", "(0,0)"))
        self.button_quickstack_position.setText(_translate("MainWindow", "Change"))
        self.text_sort_position.setText(_translate("MainWindow", "Sort Inventory button: "))
        self.label_sort_position.setText(_translate("MainWindow", "(0,0)"))
        self.button_sort_position.setText(_translate("MainWindow", "Change"))
        self.text_slot_position.setText(_translate("MainWindow", "Last inventory slot:"))
        self.label_slot_position.setText(_translate("MainWindow", "(0,0)"))
        self.button_slot_position.setText(_translate("MainWindow", "Change"))
        self.text_info.setText(_translate("MainWindow", "<html><head/><body><p style='margin: 0px; padding: 5px;'><span style=\" font-weight:600;\">Info</span></p><p style='margin: 3px; padding: 0px;'>This program automates fishing in Terraria.</p><p style='margin: 3px; padding: 0px;'> Click <a href='https://github.com/yy4n/Terraria-Fishing-Bot'>here</a> for more info.</p> <p style='margin: 3px; padding: 0px;'>Written by yy4n</p></body></html>"))
        self.text_stop.setText(_translate("MainWindow", "Hold ALT to stop"))

        

    def get_settings(self, exclude_disabled=False):
        """Gets the settings from the checkboxes of the UI

        Does not look at disabled checkboxes if exclude_disabled is True.
        """
        if (not exclude_disabled) or self.checkBox_bloodmoon.isEnabled():
            self.s_bmoon = self.checkBox_bloodmoon.isChecked()
        self.s_autobuff  = self.checkBox_buffs.isChecked()
        self.s_buff_interval = self.spinBox_buffs.value()
        self.s_autocrate = self.checkBox_crates.isChecked()
        if (not exclude_disabled) or self.checkBox_quickstack.isEnabled():
            self.s_quickstack = self.checkBox_quickstack.isChecked()
        self.s_contrast = self.spinBox_contrast.value()
        if self.radioButton_lava.isChecked():
            self.liquid = 'l'
        elif self.radioButton_honey.isChecked():
            self.liquid = 'h'
        else:
            self.liquid = 'w'

    def settings_set_enabled(self, enabled):
        """Enables or disables all checkboxes for settings

        enabled - whether to enable or disable the checkboxes
        """
        self.checkBox_bloodmoon.setEnabled(enabled)
        self.checkBox_buffs.setEnabled(enabled)
        self.spinBox_buffs.setEnabled(enabled)
        self.checkBox_crates.setEnabled(enabled)
        self.checkBox_quickstack.setEnabled(enabled)
        self.spinBox_contrast.setEnabled(enabled)
        
        self.radioButton_water.setEnabled(enabled)
        self.radioButton_lava.setEnabled(enabled)
        self.radioButton_honey.setEnabled(enabled)

        self.button_quickstack_position.setEnabled(enabled)
        self.button_sort_position.setEnabled(enabled)
        self.button_slot_position.setEnabled(enabled)

        if enabled:
            self.refresh_settings_disabling()

    def refresh_settings_disabling(self):
        """Disables not to be used checkboxes, given the settings"""
        if not self.radioButton_water.isChecked():
            self.checkBox_bloodmoon.setEnabled(False)
            self.checkBox_bloodmoon.setChecked(False)
        else:
            if not self.checkBox_bloodmoon.isEnabled():
                self.checkBox_bloodmoon.setEnabled(True)
                self.checkBox_bloodmoon.setChecked(self.s_bmoon)
        if self.checkBox_crates.isChecked():
            self.checkBox_quickstack.setEnabled(False)
            self.checkBox_quickstack.setChecked(True)
        else:
            if not self.checkBox_quickstack.isEnabled():
                self.checkBox_quickstack.setEnabled(True)
                self.checkBox_quickstack.setChecked(self.s_quickstack)

    def refresh_positions(self):
        """Refreshes the displayed position settings"""
        self.label_quickstack_position.setText(str(self.pos_quickstack))
        self.label_sort_position.setText(str(self.pos_sort))
        self.label_slot_position.setText(str(self.pos_slot))
    
    def instruction_dialog(self):
        """Opens the instructions dialog

        Stops the thread until an option is selected.
        Returns 1 if 'OK' is pressed and 0 if 'Cancel' is pressed.
        """
        Instructions_dialog = QtWidgets.QDialog()
        ui = Ui_Instructions_dialog(self.s_quickstack, self.s_autocrate)
        ui.setupUi(Instructions_dialog)
        Instructions_dialog.setModal(True)
        Instructions_dialog.show()
        return Instructions_dialog.exec()

    def position_dialog(self, position_char):
        """Opens the position change dialog

        Stops the thread until 'Reset' or 'Cancel' is pressed, or until a new position is set.
        Opens a new thread of the function 'position_setting'
        """
        self.position_dialog_window = QtWidgets.QMessageBox(MainWindow)
        self.position_dialog_window.setWindowTitle("Set a screen position")
        self.position_dialog_window.setText("Place your mouse cursor over the desired part of the screen, then press ALT. This should only be required if your screen resolution is not 1920x1080px. Press 'Reset' to reset to the default position.")
        self.position_dialog_window.setStandardButtons(QtWidgets.QMessageBox.Reset | QtWidgets.QMessageBox.Cancel)

        self.position_char = position_char
        thread = threading.Thread(target=self.position_setting, daemon=True)
        thread.start()
        if self.position_dialog_window.exec() == QtWidgets.QMessageBox.Reset:
            if position_char == 'q':
                self.pos_quickstack = (565, 280)
            elif position_char == 's':
                self.pos_sort = (600, 280)
            else:
                self.pos_slot = (520, 250)
        self.refresh_positions()
        self.position_char = ''

    def position_setting(self):
        """Handles setting a new position

        Stops the current thread until ALT is pressed or the position char is set to an empty string in the main thread
        """
        time.sleep(0.2)
        while True:
            if self.position_char == '':
                return
            if keyboard.is_pressed('alt'):
                break
        pos = pyautogui.position()
        if self.position_char == 'q':
            self.pos_quickstack = (pos.x, pos.y)
        elif self.position_char == 's':
            self.pos_sort = (pos.x, pos.y)
        else:
            self.pos_slot = (pos.x, pos.y)
        self.position_dialog_window.close()
        self.refresh_positions()

    def update_debug_image(self, screen, resolution, sight_y):
        """Sets the debug image to a 80x40px screenshot from the middle of the screen"""
        qim = ImageQt(screen).copy(resolution.width//2-40, sight_y-20, 80, 40)
        pix = QtGui.QPixmap.fromImage(qim)
        self.debug_image.setPixmap(pix)
        self.debug_image.setScaledContents(True)

    # events
    
    def on_start_clicked(self):
        if self.instruction_dialog():
            self.get_settings()
            self.start_bot()

    def on_quickstack_position_clicked(self):
        self.position_dialog('q')

    def on_sort_position_clicked(self):
        self.position_dialog('s')

    def on_slot_position_clicked(self):
        self.position_dialog('l')

    def on_setting_changed(self):
        self.get_settings(True)
        self.refresh_settings_disabling()


    # bot functions
    
    def fish(self):
        self.fishing = not self.fishing
        self.click()
    
    def click(self):
        pyautogui.mouseDown()
        time.sleep(0.01)  # terraria does not register much shorter clicks
        pyautogui.mouseUp()
        time.sleep(0.01)

    def right_click(self):
        pyautogui.mouseDown(button='right')
        time.sleep(0.01)
        pyautogui.mouseUp(button='right')
        time.sleep(0.01)

    def take_buffs(self):
        pyautogui.keyDown('b')
        time.sleep(0.01)
        pyautogui.keyUp('b')
        time.sleep(0.01)

    def open_crates(self):
        self.quickstack()
        pyautogui.moveTo(self.pos_slot[0], self.pos_slot[1])
        self.right_click()
        self.quickstack()
        pyautogui.moveTo(self.pos_slot[0], self.pos_slot[1])
        self.right_click()
        self.sort_inventory()
        pyautogui.moveTo(self.pos_slot[0], self.pos_slot[1])
        self.click()
        self.sort_inventory()
        pyautogui.moveTo(self.pos_slot[0], self.pos_slot[1])
        self.click()
        self.reset_cursor()
        self.right_click()
        
    def quickstack(self):
        pyautogui.moveTo(self.pos_quickstack[0], self.pos_quickstack[1])
        self.click()

    def sort_inventory(self):
        pyautogui.moveTo(self.pos_sort[0], self.pos_sort[1])
        self.click()

    def reset_cursor(self):
        resolution = pyautogui.size()
        mouse_pos = (resolution.width//2, resolution.height-5)
        pyautogui.moveTo(mouse_pos[0], mouse_pos[1])



    def start_bot(self):
        """Starts the bot in a new thread"""
        self.settings_set_enabled(False)
        
        self.fishing = False

        self.button_start.setText("Waiting for liquid level...")
        self.button_start.setEnabled(False)
        
        thread = threading.Thread(target=self.bot, daemon=True)
        thread.start()

    def bot(self):
        """The bot logic

        Not to be called on its own. Use 'start_bot()' instead
        """
        # get liquid surface
        keyboard.wait('alt')
        water_surface = pyautogui.position().y

        self.button_start.setText("Running...")
        self.text_stop.setHidden(False)
        
        # Setup
        resolution = pyautogui.size()
        self.reset_cursor()
        self.fish()

        # Final prep before starting
        sight_y = water_surface - 7
        blood_moon = False
        last_buff_time = time.time()

        screen = ImageGrab.grab()
        self.update_debug_image(screen, resolution, sight_y)
        last_frame = 0
        for x in range(resolution.width//2-20, resolution.width//2+20):
                pixel = screen.getpixel((x, sight_y))
                last_frame += pixel[0] + pixel[1] + pixel[2]

        if self.s_autobuff:
            self.take_buffs()

        # Fishing loop
        while not keyboard.is_pressed("alt"):
            # screenshot
            screen = ImageGrab.grab()
            self.update_debug_image(screen, resolution, sight_y)
            mouse_point = pyautogui.position()

            # determine if there is a blood moon
            if self.liquid == 'w' and self.s_bmoon:
                pixel = screen.getpixel((screen.width//2, water_surface + 30))
                if  pixel[0]/pixel[2] > 1.75:
                    blood_moon = True
                elif blood_moon:
                    if not self.fishing:
                        self.fish()
                    blood_moon = False

            # calculate the value of the current screenshot
            frame = 0
            for x in range(resolution.width//2-10, resolution.width//2+10):
                pixel = screen.getpixel((x, sight_y))
                frame += pixel[0] + pixel[1] + pixel[2]

            # see if there was change at the bobber
            if abs(frame - last_frame) > self.s_contrast:
                if self.s_bmoon and blood_moon:
                    continue
                
                # catch the fish
                print("Fish detected.")
                self.fish()
                time.sleep(0.15)
                
                # quickstack
                if self.s_quickstack and not self.s_autocrate:
                    self.quickstack()
                    self.reset_cursor()

                # autocrate
                if self.s_autocrate:
                    self.open_crates()
                    self.reset_cursor()

                # catch more fish
                time.sleep(0.15)
                self.fish();
                time.sleep(0.8)

                # refresh the screenshot value
                screen = ImageGrab.grab()
                frame = 0
                for x in range(resolution.width//2-10, resolution.width//2+10):
                    pixel = screen.getpixel((x, sight_y))
                    frame += pixel[0] + pixel[1] + pixel[2]
            elif self.liquid == 'w' and self.s_bmoon and blood_moon:
                # reel in the pole for blood moon
                if self.fishing:
                    self.fish()
                print("Blood Moon. Not Fishing.")
                time.sleep(3)

            # Autobuff
            if self.s_autobuff:
                current_time = time.time()
                if (current_time - last_buff_time) >= 60 * self.s_buff_interval:
                    self.take_buffs()
                    last_buff_time = current_time
                    
            # set the last frame to compare with next time
            last_frame = frame

        self.button_start.setText("Start")
        self.button_start.setEnabled(True)
        self.text_stop.setHidden(True)
        self.settings_set_enabled(True)


# redirect the exceptions to the console (only relevant for debugging)
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    sys.excepthook = except_hook

    # scale properly
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    # icon path
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    icon_path = os.path.join(base_path, "icon.png")
    
    # launch program
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    
    

    
