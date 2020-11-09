from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from functools import partial

import utils.config_parser as ConfigParser
import utils.rc_resources

import re
import time
import sqlite3
import sys

# Worker Thread
class WorkerThread(QThread):
    def __init__(self):
        super(WorkerThread, self).__init__()
        self.cfgparse = ConfigParser.TaskScheduler()
        self.FLAG = True

    def run(self):
        while self.FLAG:
            self.cfgparse.start()
            time.sleep(1)

    def stop(self):
        print("thread stopping...")
        self.FLAG = False
        self.exit()
        self.wait()
        print("stopped")
        sys.exit()


# Remove Course GUI
class Ui_Remove(QWidget):

    confirmed = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(400, 300))
        self.setStyleSheet("background-color: rgb(255,255,255)")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        # Label
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.label.setStyleSheet("""
        background-color: rgb(245,245,245);
        border-radius: 10px;
        font: 19pt "Segoe UI Light";
        """)
        self.label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        self.frame.setMinimumSize(QSize(0, 50))
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Push Button
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("""
        QPushButton {
            font: 12pt "Segoe UI Semilight";
            background-color: rgb(245,245,245);
            border: 2px solid rgb(150,150,150);
            border-radius: 10px;
        }
        QPushButton#pushButton:hover {
            background-color: rgb(235,235,235);
        }
        QPushButton#pushButton:pressed {
            background-color: rgb(225,225,225);
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton)

        # Push Button 2
        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("""
        QPushButton {
            font: 12pt "Segoe UI Semilight";
            background-color: rgb(245,245,245);
            border: 2px solid rgb(150,150,150);
            border-radius: 10px;
        }
        QPushButton#pushButton_2:hover {
            background-color: rgb(235,235,235);
        }
        QPushButton#pushButton_2:pressed {
            background-color: rgb(225,225,225);
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

### Event Handling ###
        # Button Events
        self.pushButton.clicked.connect(self.on_accepted)
        self.pushButton_2.clicked.connect(self.on_rejected)

### Button Functions ###
    def on_accepted(self):
        self.confirmed.emit()
        self.close()

    def on_rejected(self):
        self.close()

### Translate UI ###
    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Form", "Confirmation", None))
        self.label.setText(QCoreApplication.translate(
            "Form", 
            "Are you sure you want to delete:",
            None))
        self.pushButton.setText(QCoreApplication.translate("Form", "Yes", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", "No", None))



# Add Course GUI
class Ui_AddCourse(QWidget):

    added = Signal(int, str, str, str, str, str)

    def __init__(self):
        super().__init__()

        self.line_edit_qss = """
        QLineEdit {
            background-color: rgb(255,255,255);
            border: 2px solid rgb(150,150,150);
            border-radius: 10px;
        }
        QLineEdit:hover {
            border: 2px solid rgb(200,200,200);
        }
        QLineEdit:focus {
            border: 2px solid rgb(85, 170, 255);
        }
        """

        self.setupUi()
        self.show()
        
    def setupUi(self):
        self.resize(800, 600)
        self.setWindowModality(Qt.ApplicationModal)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(800, 600))
        self.setMaximumSize(QSize(800, 600))
        self.setStyleSheet("background-color: rgb(255,255,255);")

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_4 = QFrame(self)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setStyleSheet("background-color: transparent;")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Push Button
        self.pushButton = QPushButton(self.frame_4)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(100, 30))
        self.pushButton.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        font.setStyleStrategy(QFont.PreferDefault)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("""
        QPushButton {
            font: 25 12pt "Segoe UI Semilight";
            background-color: rgb(245,245,245);
            border: 2px solid rgb(150,150,150);
            border-radius: 10px;
        }
        QPushButton#pushButton:hover {
            background-color: rgb(235,235,235);
        }
        QPushButton#pushButton:pressed {
            background-color: rgb(225,225,225);
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton)

        # Push Button 2
        self.pushButton_2 = QPushButton(self.frame_4)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(100, 30))
        self.pushButton_2.setMaximumSize(QSize(100, 16777215))
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("""
        QPushButton {
            font: 25 12pt "Segoe UI Semilight";
            background-color: rgb(245,245,245);
            border: 2px solid rgb(150,150,150);
            border-radius: 10px;
        }
        QPushButton#pushButton_2:hover {
            background-color: rgb(235,235,235);
        }
        QPushButton#pushButton_2:pressed {
            background-color: rgb(225,225,225);
        }
        """)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addWidget(self.frame_4, 5, 0, 1, 3, Qt.AlignRight|Qt.AlignBottom)

        self.frame = QFrame(self)
        self.frame.setObjectName("frame")
        self.frame.setMinimumSize(QSize(460, 0))
        self.frame.setMaximumSize(QSize(476, 100000))
        font1 = QFont()
        font1.setFamily("Segoe UI Light")
        self.frame.setFont(font1)
        self.frame.setStyleSheet("border-radius: 20px; padding: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")

        # Label 1
        self.label = QLabel(self.frame)
        self.label.setObjectName("label")
        font2 = QFont()
        font2.setFamily("Segoe UI Semilight")
        font2.setPointSize(28)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(3)
        self.label.setFont(font2)
        self.label.setStyleSheet("font: 25 28pt \"Segoe UI Semilight\";")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        # Line Edit 1
        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setMinimumSize(QSize(200, 25))
        self.lineEdit.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamily("Segoe UI Light")
        font3.setPointSize(12)
        self.lineEdit.setFont(font3)
        self.lineEdit.setStyleSheet(self.line_edit_qss)
        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.lineEdit)

        self.verticalSpacer = QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(2, QFormLayout.SpanningRole, self.verticalSpacer)

        # Label 2
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("font: 25 14pt \"Segoe UI Light\";")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        # Line Edit 2
        self.lineEdit_2 = QLineEdit(self.frame)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFont(font3)
        self.lineEdit_2.setStyleSheet(self.line_edit_qss)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_2)

        self.verticalSpacer_2 = QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(5, QFormLayout.SpanningRole, self.verticalSpacer_2)

        # Label 3
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("font: 25 14pt \"Segoe UI Light\";")
        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_3)

        # Line Edit 3
        self.lineEdit_3 = QLineEdit(self.frame)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setFont(font3)
        self.lineEdit_3.setStyleSheet(self.line_edit_qss)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lineEdit_3)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.formLayout.setItem(7, QFormLayout.SpanningRole, self.verticalSpacer_3)

        self.gridLayout.addWidget(self.frame, 0, 0, 3, 1)

        self.frame_2 = QFrame(self)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setMinimumSize(QSize(300, 300))
        self.frame_2.setStyleSheet("border-radius: 20px; padding: 5px; padding-top: 0px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName("label_5")
        self.label_5.setMaximumSize(QSize(200, 60))
        self.label_5.setStyleSheet("font: 25 28pt \"Segoe UI Semilight\";")
        self.label_5.setFrameShape(QFrame.NoFrame)
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.label_5)

        # Checkbox 1
        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName("checkBox")
        font4 = QFont()
        font4.setFamily("Segoe UI Light")
        font4.setPointSize(12)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setWeight(3)
        self.checkBox.setFont(font4)
        self.checkBox.setStyleSheet("font: 25 12pt \"Segoe UI Light\";")
        self.verticalLayout.addWidget(self.checkBox)

        # Checkbox 2
        self.checkBox_2 = QCheckBox(self.frame_2)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setStyleSheet("font: 25 12pt \"Segoe UI Light\";")
        self.verticalLayout.addWidget(self.checkBox_2)

        # Checkbox 3
        self.checkBox_3 = QCheckBox(self.frame_2)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setStyleSheet("font: 25 12pt \"Segoe UI Light\";")
        self.verticalLayout.addWidget(self.checkBox_3)

        # Checkbox 4
        self.checkBox_4 = QCheckBox(self.frame_2)
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.setStyleSheet("font: 25 12pt \"Segoe UI Light\";")
        self.verticalLayout.addWidget(self.checkBox_4)

        # Checkbox 5
        self.checkBox_5 = QCheckBox(self.frame_2)
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.setStyleSheet("font: 25 12pt \"Segoe UI Light\";")
        self.verticalLayout.addWidget(self.checkBox_5)

        # Checkbox 6
        self.checkBox_6 = QCheckBox(self.frame_2)
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_6.setStyleSheet("font: 25 12pt \"Segoe UI Light\";")
        self.verticalLayout.addWidget(self.checkBox_6)

        # Checkbox 7
        self.checkBox_7 = QCheckBox(self.frame_2)
        self.checkBox_7.setObjectName("checkBox_7")
        self.checkBox_7.setStyleSheet("font: 25 12pt \"Segoe UI Light\";")
        self.verticalLayout.addWidget(self.checkBox_7)

        self.gridLayout.addWidget(self.frame_2, 0, 2, 5, 1)

        self.frame_3 = QFrame(self)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setStyleSheet("border-radius: 20px; padding: 5px;")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Label 4
        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName("label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setStyleSheet("font: 25 28pt \"Segoe UI Semilight\";")
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout_2.addWidget(self.label_4)

        # Time Edit
        self.timeEdit = QTimeEdit(self.frame_3)
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit.setCursor(QCursor(Qt.PointingHandCursor))
        self.timeEdit.setStyleSheet("""
        QTimeEdit {
            font: 25 20pt "Segoe UI Light";
            background-color: rgb(255,255,255);
            border: 2px solid rgb(150,150,150);
            border-radius: 10px;
        }
        QTimeEdit:hover {
            border: 2px solid rgb(200,200,200);
        }
        QTimeEdit:focus {
            border: 2px solid rgb(85, 170, 255)
        }
        QTimeEdit#timeEdit:up-buttn {
            background-color: transparent;
            border: 2px solid rgb(150,150,150);
            border-radius: 10px;
        };
        """)
        self.timeEdit.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.timeEdit.setProperty("showGroupSeparator", False)
        self.verticalLayout_2.addWidget(self.timeEdit)
        self.time = self.timeEdit.time().toString("hh:mm")
        self.timeEdit.timeChanged.connect(self.timeUpdate)

        self.gridLayout.addWidget(self.frame_3, 4, 0, 1, 1)

        # LINE
        self.line = QFrame(self)
        self.line.setObjectName("line")
        self.line.setStyleSheet("color: rgb(180,180,180)")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.VLine)
        self.gridLayout.addWidget(self.line, 0, 1, 5, 1)

        # LINE 2
        self.line_2 = QFrame(self)
        self.line_2.setObjectName("line_2")
        self.line_2.setStyleSheet("color: rgb(180,180,180)")
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setFrameShape(QFrame.HLine)
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 1)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

# Event Handling
        # Button Events
        self.pushButton.clicked.connect(self.yes)
        self.pushButton_2.clicked.connect(self.no)

        # Checkbox Events
        self.weekday = set()
        self.week = self.checkBox.toggled.connect(lambda: self.buttonState(self.checkBox, self.weekday))
        self.week = self.checkBox_2.toggled.connect(lambda: self.buttonState(self.checkBox_2, self.weekday))
        self.week = self.checkBox_3.toggled.connect(lambda: self.buttonState(self.checkBox_3, self.weekday))
        self.week = self.checkBox_4.toggled.connect(lambda: self.buttonState(self.checkBox_4, self.weekday))
        self.week = self.checkBox_5.toggled.connect(lambda: self.buttonState(self.checkBox_5, self.weekday))
        self.week = self.checkBox_6.toggled.connect(lambda: self.buttonState(self.checkBox_6, self.weekday))
        self.week = self.checkBox_7.toggled.connect(lambda: self.buttonState(self.checkBox_7, self.weekday))

# Button Functions
    def yes(self, week):
        print("ACCEPTED!")

        course, meetingID, password = self.txt()
        weekStr = ",".join(self.weekday)
        time = self.time

        self.added.emit(self.id, course, meetingID, password, weekStr, time)
        self.id = None
        self.close()
    
    def yes_add(self):
        self.id = -1

    def yes_edited(self, id):
        self.id = id
    
    def no(self):
        print("DENIED!")
        self.close()

# Data Processing
    def timeUpdate(self):
        self.time = self.timeEdit.time().toString("hh:mm")
        print("changed! " + self.time)

    def txt(self):
        line1 = self.lineEdit.text()
        line2 = self.lineEdit_2.text()
        line3 = self.lineEdit_3.text()
        return(line1, line2, line3)
    
    def buttonState(self, button, weekday):
        caption = button.text()
        # Monday
        if caption == "Monday":
            if button.isChecked():
                weekday.add("monday")
                print("1 is checked!")
            else:
                weekday.remove("monday")
                print("1 is not checked...")
        # Tuesday
        elif caption == "Tuesday":
            if button.isChecked():
                weekday.add("tuesday")
                print("2 is checked!")
            else:
                weekday.remove("tuesday")
                print("2 is not checked...")
        # Wednesday
        elif caption == "Wednesday":
            if button.isChecked():
                weekday.add("wednesday")
                print("3 is checked!")
            else:
                weekday.remove("wednesday")
                print("3 is not checked...")
        # Thursday
        elif caption == "Thursday":
            if button.isChecked():
                weekday.add("thursday")
                print("4 is checked!")
            else:
                weekday.remove("thursday")
                print("4 is not checked...")
        # Friday
        elif caption == "Friday":
            if button.isChecked():
                weekday.add("friday")
                print("5 is checked!")
            else:
                weekday.remove("friday")
                print("5 is not checked...")
        # Saturday
        elif caption == "Saturday":
            if button.isChecked():
                weekday.add("saturday")
                print("6 is checked!")
            else:
                weekday.remove("saturday")
                print("6 is not checked...")
        # Sunday
        elif caption == "Sunday":
            if button.isChecked():
                weekday.add("sunday")
                print("7 is checked!")
            else:
                weekday.remove("sunday")
                print("7 is not checked...")
        print(weekday)

# Translate UI
    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Form", "Add Course", None))
        self.pushButton.setText(QCoreApplication.translate("Form", "Save", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", "Discard", None))
        self.label.setText(QCoreApplication.translate("Form", "Course", None))
        self.lineEdit.setInputMask("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Form", "Course Name", None))
        self.label_2.setText(QCoreApplication.translate("Form", "Meeting ID", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Form", "Meeting ID", None))
        self.label_3.setText(QCoreApplication.translate("Form", "Password", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("Form", "Password", None))
        self.label_5.setText(QCoreApplication.translate("Form", "Weekday", None))
        self.checkBox.setText(QCoreApplication.translate("Form", "Monday", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", "Tuesday", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", "Wednesday", None))
        self.checkBox_4.setText(QCoreApplication.translate("Form", "Thursday", None))
        self.checkBox_5.setText(QCoreApplication.translate("Form", "Friday", None))
        self.checkBox_6.setText(QCoreApplication.translate("Form", "Saturday", None))
        self.checkBox_7.setText(QCoreApplication.translate("Form", "Sunday", None))
        self.label_4.setText(QCoreApplication.translate("Form", "Time", None))



# Main Window GUI
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__(None)

        # Load Scheduler
        self.cfgparse = ConfigParser.TaskScheduler()
        self.cfgparse.load()

        # Start Worker Thread
        self.worker = WorkerThread()
        self.worker.start()

        self.setObjectName("MainWindow")
        self.base()
        self.show()

    def base(self):
        self.resize(1024, 768)
        self.setWindowIcon(QIcon("./resources/icon.ico"))
        self.setMinimumSize(QSize(1024, 768))
        self.setWindowOpacity(1)
        self.setWindowTitle("Zoom Automation")
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.rightFrame = QFrame(self.centralwidget)
        self.rightFrame.setObjectName("rightFrame")
        self.rightFrame.setMinimumSize(QSize(100, 0))
        self.rightFrame.setMaximumSize(QSize(100, 16777215))
        self.rightFrame.setStyleSheet("background-color: transparent;")
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout.addWidget(self.rightFrame, 4, 2, 1, 1)

        self.leftFrame = QFrame(self.centralwidget)
        self.leftFrame.setObjectName("leftFrame")
        self.leftFrame.setMinimumSize(QSize(100, 0))
        self.leftFrame.setMaximumSize(QSize(100, 16777215))
        self.leftFrame.setStyleSheet("background-color: transparent;")
        self.leftFrame.setFrameShape(QFrame.StyledPanel)
        self.leftFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout.addWidget(self.leftFrame, 4, 0, 1, 1)

        self.LowFrame = QFrame(self.centralwidget)
        self.LowFrame.setObjectName("LowFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LowFrame.sizePolicy().hasHeightForWidth())
        self.LowFrame.setSizePolicy(sizePolicy)
        self.LowFrame.setMinimumSize(QSize(1006, 100))
        self.LowFrame.setStyleSheet("background-color: transparent;")
        self.LowFrame.setFrameShape(QFrame.StyledPanel)
        self.LowFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.LowFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Push Button 1
        self.pushButton = QPushButton(self.LowFrame)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(70, 70))
        self.pushButton.setMaximumSize(QSize(70, 70))
        self.pushButton.setStyleSheet("""
        QPushButton {
            background-image: url(:/resources/addButton.png);
            border-radius: 20px;
        }

        QPushButton#pushButton:hover {
            background-image: url(:/resources/addButton.png);
            background-color: rgb(247,249,254);
            border-radius: 20px;
        }

        QPushButton#pushButton:pressed {
            background-color: rgb(85, 255, 255);
            background-color: rgb(237,243,255);
            border-radius: 20px;
        }
        """)
        self.pushButton.setText("")
        self.horizontalLayout.addWidget(self.pushButton)

        # Push Button 2
        self.pushButton_2 = QPushButton(self.LowFrame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(70, 70))
        self.pushButton_2.setMaximumSize(QSize(70, 70))
        self.pushButton_2.setStyleSheet("""
        QPushButton {
            background-image: url(:/resources/refreshButton.png);
            border-radius: 20px;
        }

        QPushButton#pushButton_2:hover {
            background-image: url(:/resources/refreshButton.png);
            background-color: rgb(247,249,254);
            border-radius: 20px;
        }

        QPushButton#pushButton_2:pressed {
            background-image: url(:/resources/refreshButton.png);
            background-color: rgb(237,243,255);
            border-radius: 20px;
        }
        """)
        self.pushButton_2.setText("")
        self.horizontalLayout.addWidget(self.pushButton_2)

        # Push Button 3
        self.pushButton_3 = QPushButton(self.LowFrame)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(70, 70))
        self.pushButton_3.setMaximumSize(QSize(70, 70))
        self.pushButton_3.setStyleSheet("""
        QPushButton {
            background-image: url(:/resources/editButton.png);
            border-radius: 20px;
        }

        QPushButton#pushButton_3:hover {
            background-image: url(:/resources/editButton.png);
            background-color: rgb(247,249,254);
            border-radius: 20px;
        }

        QPushButton#pushButton_3:pressed {
            background-image: url(:/resources/editButton.png);
            background-color: rgb(237,243,255);
            border-radius: 20px;
        }
        """)
        self.pushButton_3.setText("")
        self.horizontalLayout.addWidget(self.pushButton_3)

        # Push Button 4
        self.pushButton_4 = QPushButton(self.LowFrame)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(70, 70))
        self.pushButton_4.setMaximumSize(QSize(70, 70))
        self.pushButton_4.setStyleSheet("""
        QPushButton {
            background-image: url(:/resources/removeButton.png);
            border-radius: 20px;
        }

        QPushButton#pushButton_4:hover {
            background-image: url(:/resources/removeButton.png);
            background-color: rgb(247,249,254);
            border-radius: 20px;
        }

        QPushButton#pushButton_4:pressed {
            background-image: url(:/resources/removeButton.png);
            background-color: rgb(237,243,255);
            border-radius: 20px;
        }
        """)
        self.pushButton_4.setText("")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.gridLayout.addWidget(self.LowFrame, 3, 0, 1, 3)

        self.TopFrame = QFrame(self.centralwidget)
        self.TopFrame.setObjectName("TopFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.TopFrame.sizePolicy().hasHeightForWidth())
        self.TopFrame.setSizePolicy(sizePolicy1)
        self.TopFrame.setMinimumSize(QSize(1006, 150))
        self.TopFrame.setMaximumSize(QSize(16777215, 150))
        self.TopFrame.setStyleSheet("background-color: transparent;")
        self.TopFrame.setFrameShape(QFrame.StyledPanel)
        self.TopFrame.setFrameShadow(QFrame.Raised)

        # TIME Label
        self.label = QLabel(self.TopFrame)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(40, 32, 191, 71))
        font = QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(64)
        self.label.setFont(font)

        # DATE Label
        self.label_2 = QLabel(self.TopFrame)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(275, 28, 587, 91))
        self.label_2.setMinimumSize(QSize(471, 51))
        font1 = QFont()
        font1.setFamily("Segoe UI Light")
        font1.setPointSize(36)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet("background-color: rgb(245, 245, 245); border-radius: 20px;")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.gridLayout.addWidget(self.TopFrame, 2, 0, 1, 3, Qt.AlignHCenter|Qt.AlignVCenter)


        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        self.frame.setMinimumSize(QSize(0, 20))
        self.frame.setStyleSheet("background-color: transparent;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout.addWidget(self.frame, 5, 1, 1, 1)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setStyleSheet("background-color: rgb(245, 245, 245); border-radius: 5px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Table Widget
        self.tableWidget = QTableWidget(self.frame_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setStyleSheet("""
        QTableWidget {	
            background-color: rgb(255, 255, 255);
            padding: 10px;
            border-radius: 5px;
            gridline-color: rgb(192, 192, 192);
        }

        QTableWidget::item{
            border-color: rgb(44, 49, 60);
            padding-left: 3px;
            padding-right: 3px;
            gridline-color: rgb(192, 192, 192);
        }

        QTableWidget::item:selected{
            background-color: rgb(85, 170, 255, 200);
        }

        QTableWidget::horizontalHeader {	
            background-color: rgb(245, 245, 245);
        }

        QHeaderView::section:horizontal {
            border: 1px solid rgb(192, 192, 192);
            background-color: rgb(235, 235, 235);
            alternate-background-color: transparent;
            padding: 3px;
        }

        QHeaderView::section:vertical {
            border: 1px solid rgb(192, 192, 192);
            background-color: rgb(235, 235, 235);
            alternate-background-color: transparent;
            padding: 3px;
        }
        """)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setFrameShape(QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QFrame.Plain)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.tableWidget.setHorizontalHeaderLabels([
            "Course",
            "Meeting ID",
            "Password",
            "Time",
            "Weekday",
            "Run"
            ])
        self.gridLayout.addWidget(self.frame_2, 4, 1, 1, 1)

        # Initilize Table
        self.loadTable()
        self.runButton()
        
        # Time and Date
        self.timeDateConnect()
        Timer = QTimer(self)
        Timer.timeout.connect(self.timeDateConnect)
        Timer.start(1000)

        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)

# Event handling
        # Button Events
        self.pushButton.clicked.connect(self.button_add)
        self.pushButton_2.clicked.connect(self.button_refresh)
        self.pushButton_3.clicked.connect(self.button_edit)
        self.pushButton_4.clicked.connect(self.button_remove)

### Close Event (system tray) ###
        # Tray Icon MENU
        self.menu = QMenu()
        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.worker.stop)
        self.menu.addAction(self.quit)

        # Tray Icon
        self.tray_icon = QSystemTrayIcon(QIcon("./resources/icon.ico"), self)
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_menu)

    # Override Close Event
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    # Close Event
    def tray_menu(self, reason):
        print(str(reason))
        if (reason != QSystemTrayIcon.ActivationReason.Context):
            self.showNormal()

### Time and Date Functions ###
    # Time
    def timeDateConnect(self):
        curTime = QTime.currentTime()
        labelTime = curTime.toString("hh:mm")
        self.label.setText(labelTime)

        curDate = QDate.currentDate()
        labelDate = curDate.toString("MMMM d, dddd")
        self.label_2.setText(labelDate)

### Table Functions ###
    # Load Table From Database 
    def loadTable(self):
        query = "SELECT * FROM courseTable"
        data = self.db_search_multiple(query)

        self.tableWidget.setRowCount(0)
        self.CIDcache = []
        for rows, value in enumerate(data):
            self.tableWidget.insertRow(rows)
            for columns, item in enumerate(value):
                if columns == 0:
                    self.CIDcache.append(item)
                else:
                    newColumns = columns - 1
                    self.tableWidget.setItem(rows, newColumns, QTableWidgetItem(str(item)))

    # Run button SLOT
    @Slot(int)
    def runClicked(self, row):
        cid = str(self.CIDcache[row])
        query = "SELECT * FROM courseTable WHERE CID=" + cid
        dataList = self.db_search_multiple(query)
        dataSet = dataList[0]
        CID = dataSet[0]
        self.cfgparse.run(CID)

    # Run Button
    def runButton(self):
        for i in range(self.tableWidget.rowCount()):
            row = i
            self.pushButton_table = QPushButton(str(i))
            self.pushButton_table.setObjectName(u"pushbutton")
            self.pushButton_table.setFixedSize(QSize(50,30))
            self.pushButton_table.setText("")

            self.pushButton_table.setStyleSheet("""
            QPushButton {
                border: 2px solid rgb(122, 122, 122);
                border-radius: 15px;
                background-color: rgb(235,235,235);
                background-image: url(:/resources/runButton.png);
            }
            QPushButton#pushbutton:hover {
                border: 2px solid rgb(122, 122, 122);
                border-radius: 15px;
                background-color: rgb(224,224,224);
                background-image: url(:/resources/runButton.png);
            }
            QPushButton#pushbutton:pressed {
                border: 2px solid rgb(122, 122, 122);
                border-radius: 15px;
                background-color: rgb(214,214,214);
                background-image: url(:/resources/runButton.png);
            }
            """)
            self.pushButton_table.clicked.connect(partial(self.runClicked, row))
            box = QWidget()
            Vbox = QHBoxLayout()
            Vbox.setAlignment(Qt.AlignCenter)
            Vbox.addWidget(self.pushButton_table)
            Vbox.setContentsMargins(0,0,0,0)
            box.setStyleSheet("background-color: transparent;")
            box.setLayout(Vbox)
            self.tableWidget.setCellWidget(i, 5, box)

### Button Functions ###
    # Add Button
    def button_add(self):
        self.addWindow = Ui_AddCourse()
        self.addWindow.yes_add()
        self.addWindow.show()
        self.addWindow.added.connect(self.addCourse)

    @Slot(int, str, str, str, str, str)
    def addCourse(self, cid, course, meeting, password, weekday, time):
        self.cid = str(cid)
        self.course = course
        self.meeting = meeting
        self.password = password
        self.weekday = weekday
        self.time_ = time
        
        if self.cid == "-1":
            self.db_insert_courseTable()
        else:
            self.db_update_courseTable()

        self.button_refresh()

    # Refresh Button
    ## Refresh table and scheduler
    def button_refresh(self):
        self.cfgparse.clear()
        self.cfgparse.load()
        self.loadTable()
        self.runButton()

    # Edit Button
    def button_edit(self):
        try:
            row = self.tableWidget.currentRow()
            if row >= 0:
                cid = str(self.CIDcache[row])
                query = "SELECT * FROM courseTable WHERE CID=" + cid
                dataList = self.db_search_multiple(query)
                dataSet = dataList[0]
                
                CID = dataSet[0]
                course = dataSet[1]
                meetID = dataSet[2]
                pwd = dataSet[3]
                date = dataSet[4]
                dateSplit = re.split(",", date)
                time = dataSet[5]
                timeSplit = re.split(":", time)
                hour = int(timeSplit[0])
                minute = int(timeSplit[1])

                self.editWindow = Ui_AddCourse()

                self.editWindow.yes_edited(CID)
                self.editWindow.lineEdit.setText(course)
                self.editWindow.lineEdit_2.setText(meetID)
                self.editWindow.lineEdit_3.setText(pwd)
                self.editWindow.timeEdit.setTime(QTime(hour, minute))

                for weekday in dateSplit:
                    print(weekday)
                    if weekday == "monday":
                        self.editWindow.checkBox.setCheckState(Qt.Checked)
                    elif weekday == "tuesday":
                        self.editWindow.checkBox_2.setCheckState(Qt.Checked)
                    elif weekday == "wednesday":
                        self.editWindow.checkBox_3.setCheckState(Qt.Checked)
                    elif weekday == "thursday":
                        self.editWindow.checkBox_4.setCheckState(Qt.Checked)
                    elif weekday == "friday":
                        self.editWindow.checkBox_5.setCheckState(Qt.Checked)
                    elif weekday == "saturday":
                        self.editWindow.checkBox_6.setCheckState(Qt.Checked)
                    elif weekday == "sunday":
                        self.editWindow.checkBox_7.setCheckState(Qt.Checked)

                self.editWindow.show()
                self.editWindow.added.connect(self.addCourse)
        except Exception as e:
            print(e)

        
    # Remove Button
    def button_remove(self):
        try:
            row = self.tableWidget.currentRow()
            if row >= 0:
                cid = str(self.CIDcache[row])
                query = "SELECT course FROM courseTable WHERE CID=" + cid
                deleteCourse = self.db_search_singular(query)
                print(deleteCourse[0])

                self.removeWindow = Ui_Remove()
                self.removeWindow.show()
                self.removeWindow.label.setText(
                    "Are you sure you want to delete:\n{}".format(deleteCourse[0])
                    )
                self.removeWindow.confirmed.connect(lambda: self.confirmRemove(cid))
            elif row < 0:
                print("error, no selection has been made")
        except Exception as e:
            print(e)

    def confirmRemove(self, cid):
        query = "DELETE FROM courseTable WHERE CID=" + cid
        self.db_delete_courseTable(query)
        self.button_refresh()




### Database Functions ###
### REMEMBER TO HANDLE EXCEPTIONS ###
    def db_search_multiple(self, query):
        connection = sqlite3.connect("./resources/courselist.db")
        cursor = connection.cursor()
        cache = cursor.execute(query)
        data = cache.fetchall()
        connection.close()
        return(data)

    def db_search_singular(self, query):
        connection = sqlite3.connect("./resources/courselist.db")
        cursor = connection.cursor()
        cache = cursor.execute(query)
        data = cache.fetchall()
        connection.close()
        return([x[0] for x in data])
        
    def db_delete_courseTable(self, query):
        connection = sqlite3.connect("./resources/courselist.db")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def db_insert_courseTable(self):
        connection = sqlite3.connect("./resources/courselist.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO courseTable(course, meetingID, password, weekday, time) VALUES (?,?,?,?,?)",
            (self.course, self.meeting, self.password, self.weekday, self.time_)
            )
        connection.commit()
        print("Successfully added!")

        cursor.execute("SELECT * FROM courseTable")
        r = cursor.fetchall()
        print(r)
        connection.close()

        print("---------------------")
        print(self.course)
        print(self.meeting)
        print(self.password)
        print(self.weekday)
        print(self.time_)
    
    def db_update_courseTable(self):
        connection = sqlite3.connect("./resources/courselist.db")
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE courseTable SET course=?, meetingID=?, password=?, weekday=?, time=? WHERE CID=?
        """, (self.course, self.meeting, self.password, self.weekday, self.time_, self.cid)
        )
        connection.commit()
        print("Successfully added!")

        cursor.execute("SELECT * FROM courseTable")
        r = cursor.fetchall()
        print(r)
        connection.close()

        print("---------------------")
        print(self.course)
        print(self.meeting)
        print(self.password)
        print(self.weekday)
        print(self.time_)



def start():
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec_())
