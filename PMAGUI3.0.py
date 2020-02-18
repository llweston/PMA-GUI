import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtProperty, QObject, pyqtSignal, QThread, QPointF, QRectF, QLineF, QObject
from PyQt5.QtWidgets import QWidget, QApplication, QStyleFactory, QMainWindow, QGridLayout
from PyQt5.QtGui import QPainter
from JoyEx import Direction, Joystick
from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
from time import sleep

class Ui_MainWindow(object):
    #UI Setup
    def setupUi(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        #self.setMinimumSize(1000, 1000) #How I tested which window accepted qt methods
        pass

class Window(QtWidgets.QMainWindow):
    #only way I found to get keypressed working
    def __init__(self):
        super(Window, self).__init__()
        #self.setMinimumSize(1000, 1000) #How I tested which window accepted qt methods
        #PMA Setup, mostly copied from the file-based motion control
        try:
            USB_DEVICE = 'COM6'
            ZABER_ASCII_PORT = AsciiSerial(USB_DEVICE)
            print("NUTS!")
            self.torch_output = 1
            self.wire_output = 2
            self.iodev = AsciiDevice(ZABER_ASCII_PORT, 1) #additional xy dev created to deal w/ io
            self.xdev = AsciiDevice(ZABER_ASCII_PORT, 1).axis(1)
            self.ydev = AsciiDevice(ZABER_ASCII_PORT, 1).axis(2)
            self.zdev = AsciiDevice(ZABER_ASCII_PORT, 2)
            self.number_devices = 2
            self.xdev.home()
            self.ydev.home()
            self.zdev.home()
            self.cm = 2016
        except:
            print("No Connection!!")
        #UI Setup
        self.setObjectName("MainWindow")
        self.resize(691, 876)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.verticalSlider.setMaximum(143)
        self.verticalSlider.valueChanged.connect(self.updateLCD)
        self.gridLayout_5.addWidget(self.verticalSlider, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, QtGui.QBrush(QtGui.QColor('red')))
        self.lcdNumber.setPalette(palette)
        self.verticalLayout.addWidget(self.lcdNumber)
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 3, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout_3.addWidget(self.plainTextEdit, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 5, 1, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.lcdNumber_2.setMinimumHeight(75)
        self.lcdNumber_2.setPalette(palette)
        self.gridLayout_4.addWidget(self.lcdNumber_2, 1, 1, 1, 1)
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.lcdNumber_3.setPalette(palette)
        self.gridLayout_4.addWidget(self.lcdNumber_3, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_4, 4, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.ButtAdjYUp)
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.ButtAdjYDn)
        self.gridLayout_2.addWidget(self.pushButton_4, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.ButtAdjXUp)
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setMinimumSize(200, 200)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)
        self.joystick = Joystick(self.frame)
        #need to find a way to connect joystick to handler to use successfully
        #print(self.joystick.property("clicked"))
        #self.joystick.clicked.connect(self.JoyWrangler)
        self.horizontalLayout.addWidget(self.joystick)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.ButtAdjXDn)
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.ButtAdjZDn)
        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.ButtAdjZUp)
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 7, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setCheckable(True)
        self.pushButton_8.clicked[bool].connect(self.FIRE)
        self.gridLayout.addWidget(self.pushButton_8, 5, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 8, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_2.setReadOnly(True)
        self.horizontalLayout_2.addWidget(self.plainTextEdit_2)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.plainTextEdit_3.setReadOnly(True)
        self.horizontalLayout_3.addWidget(self.plainTextEdit_3)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_3.addWidget(self.label_13)
        self.gridLayout.addLayout(self.horizontalLayout_3, 7, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_4.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.plainTextEdit_4.setReadOnly(True)
        self.horizontalLayout_4.addWidget(self.plainTextEdit_4)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_4.addWidget(self.label_14)
        self.gridLayout.addLayout(self.horizontalLayout_4, 8, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 691, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
    def ButtAdjZUp(self):
        self.verticalSlider.setValue(self.verticalSlider.value() + 1)
        print("+1cm Z")
    #individual handlers for each button is inefficient, fix later
    def ButtAdjZDn(self):
        self.verticalSlider.setValue(self.verticalSlider.value() - 1)
        print("-1cm Z")
    def ButtAdjXUp(self):
        try:
            self.x = self.x + 1
        except:
            self.x = 1
        self.lcdNumber_3.display(self.x)
        print("+1cm X")
        self.updateLCD3()
    def ButtAdjXDn(self):
        try:
            if self.x > 0:
                self.x = self.x - 1
                print("-1cm X")
        except:
            self.x = 0
        self.lcdNumber_3.display(self.x)
        self.updateLCD3()
    def ButtAdjYUp(self):
        try:
            self.y = self.y + 1
        except:
            self.y = 1
        self.lcdNumber_2.display(self.y)
        print("+1cm Y")
        self.updateLCD2()
    def ButtAdjYDn(self):
        try:
            if self.y > 0:
                self.y = self.y - 1
                print("-1cm Y")
        except:
            self.y = 0
        self.lcdNumber_2.display(self.y)
        self.updateLCD2()

    def JoyWrangler(self):
        #dysfunctional joystick handler
        print("I'm in")

    def FIRE(self, pressed):
        if pressed:
            print("ZAP!")
            switch1 = self.iodev.send("io set do 1 1")
            switch2 = self.iodev.send("io set do 2 1")
            state = self.iodev.send("io get do")
        else:
            print("no zap")
            switch1 = self.iodev.send("io set do 1 0")
            switch2 = self.iodev.send("io set do 2 0")
            state = self.iodev.send("io get do")

    def updateLCD(self, event):
        print(event)
        self.lcdNumber.display(event)
        #sleep(1) #delaying didn't seem to help the refresh lag
        reply = self.zdev.move_abs(self.cm*self.lcdNumber.intValue())
    def updateLCD3(self):
        print('x beep beep')
        reply = self.xdev.move_abs(self.cm*self.x)
    def updateLCD2(self):
        print('y beep beep')
        reply = self.ydev.move_abs(self.cm*self.y)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_8.setText(_translate("MainWindow", "Z pos (cm)"))
        self.label_4.setText(_translate("MainWindow", "Wire Length"))
        self.label_5.setText(_translate("MainWindow", "cm"))
        self.label_6.setText(_translate("MainWindow", "Y pos (cm)"))
        self.label_7.setText(_translate("MainWindow", "X pos (cm)"))
        self.pushButton_3.setText(_translate("MainWindow", "+y (1cm)"))
        self.pushButton_4.setText(_translate("MainWindow", "-y (1cm)"))
        self.pushButton_6.setText(_translate("MainWindow", "+x (1cm)"))
        self.pushButton_5.setText(_translate("MainWindow", "-x (1cm)"))
        self.label_2.setText(_translate("MainWindow", "XY Control"))
        self.pushButton_2.setText(_translate("MainWindow", "-z (1cm)"))
        self.label.setText(_translate("MainWindow", "Z Control"))
        self.label_3.setText(_translate("MainWindow", "Welcome to the PMA GUI!1!"))
        self.pushButton.setText(_translate("MainWindow", "+z (1cm)"))
        self.label_9.setText(_translate("MainWindow", "Wire Feed Delay"))
        self.label_10.setText(_translate("MainWindow", "Arc Delay"))
        self.pushButton_8.setText(_translate("MainWindow", "TEST FIRE"))
        self.label_11.setText(_translate("MainWindow", "Velocity"))
        self.label_12.setText(_translate("MainWindow", "Sec"))
        self.label_13.setText(_translate("MainWindow", "Sec"))
        self.label_14.setText(_translate("MainWindow", "fast"))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    #wasd control not working currently, leaving it here
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_W:
            print("+0.388455cm Y")
            try:
                self.y = self.y + 0.388455
            except:
                self.y = 0.388455
            self.lcdNumber_2.display(self.y)
            reply = self.ydev.move_vel(20*self.cm)
        elif e.key() == QtCore.Qt.Key_S:
            try:
                if self.y > 0:
                    self.y = self.y - 0.388455
                    print("-0.388455cm Y")
            except:
                self.y = 0
            self.lcdNumber_2.display(self.y)
            reply = self.ydev.move_vel(-(20*self.cm))
        elif e.key() == QtCore.Qt.Key_A:
            print("+0.377799cm X")
            try:
                self.x = self.x + 0.377799
            except:
                self.x = 0.377799
            self.lcdNumber_3.display(self.x)
            reply = self.xdev.move_vel(20*self.cm)
        elif e.key() == QtCore.Qt.Key_D:
            try:
                if self.x > 0:
                    self.x = self.x - 0.377799
                    print("-0.377799cm X")
            except:
                self.x = 0
            self.lcdNumber_3.display(self.x)
            reply = self.xdev.move_vel(-(20*self.cm))
        elif e.key() == QtCore.Qt.Key_Up:
            #Z keyboard control isn't very useful compared to GUI so might remove
            self.verticalSlider.setValue(self.verticalSlider.value() + 1)
            print("+1cm Z")
        elif e.key() == QtCore.Qt.Key_Down:
            self.verticalSlider.setValue(self.verticalSlider.value() - 1)
            print("-1cm Z")
    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_W:
            print('0y')
            reply = self.ydev.move_vel(0)
        elif e.key() == QtCore.Qt.Key_S:
            print('0y')
            reply = self.ydev.move_vel(0)
        elif e.key() == QtCore.Qt.Key_A:
            print('0x')
            reply = self.xdev.move_vel(0)
        elif e.key() == QtCore.Qt.Key_D:
            print('0x')
            reply = self.xdev.move_vel(0)
        elif e.key() == QtCore.Qt.Key_Up:
            print('0z')
        elif e.key() == QtCore.Qt.Key_Down:
            print('0z')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    MainWindow.show()
    sys.exit(app.exec_())
