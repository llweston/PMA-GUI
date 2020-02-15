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
        #self.setMinimumSize(1000, 1000)
        pass

class Window(QtWidgets.QMainWindow):
    #only way I found to get keypressed working
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
    #wasd control not working currently, leaving it here
    def keyPressEvent(self, e):
        print("key press")
        if e.key() == QtCore.Qt.Key_W:
            print('+y')
            reply = self.ydev.move_rel(self.cm)
        elif e.key() == QtCore.Qt.Key_S:
            print('-y')
            reply = self.ydev.move_rel(-self.cm)
        elif e.key() == QtCore.Qt.Key_A:
            print('+x')
            reply = self.xdev.move_rel(self.cm)
        elif e.key() == QtCore.Qt.Key_D:
            print('-x')
            reply = self.xdev.move_rel(-self.cm)
        elif e.key() == QtCore.Qt.Key_Up:
            print('-x')
            reply = self.zdev.move_rel(self.cm)
        elif e.key() == QtCore.Qt.Key_Down:
            print('-x')
            reply = self.zdev.move_rel(-self.cm)
    def keyReleaseEvent(self, e):
        print("key release")
        if e.key() == QtCore.Qt.Key_W:
            print('0y')
        elif e.key() == QtCore.Qt.Key_S:
            print('0y')
        elif e.key() == QtCore.Qt.Key_A:
            print('0x')
        elif e.key() == QtCore.Qt.Key_D:
            print('0x')
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
