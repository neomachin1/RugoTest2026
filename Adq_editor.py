from ui_editor import Ui_MainWindow
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QFileDialog, QMessageBox
import serial.tools.list_ports
import os
from time import sleep
import icono_rc
#import hashlib
import sys

from PySide2.QtCore import QCoreApplication



from serial import Serial
from time import sleep


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.setWindowIcon(QtGui.QIcon('usb.png'))
        
        self.ui.Cabezera.clicked.connect(self.Cabezera)
        self.ui.Datos.clicked.connect(self.Datos)
        self.ui.Agregar.clicked.connect(self.Agregar)
        self.ui.Archivo.clicked.connect(self.Archivo)
        self.carpeta = []

    def Archivo(self):
        ruta, data = QFileDialog.getOpenFileName(self, 'Recuperar Archivo Rugosimetro', '', 'Roughness File (*.bin *.rbd)')
        if ruta != "":
            self.carpeta.append(os.path.dirname(ruta))
            self.ruta = os.path.basename(ruta)
            self.fuente = open(ruta, 'rb')
            a = self.fuente.read(3)
            self.datos = a[2]+(a[1]*256)+a[0]
            self.total = os.path.getsize(ruta)
            
            self.ui.label_13.setText(self.ruta)
            self.ui.label_14.setText(str(os.path.getsize(ruta)))
            self.ui.label_15.setText(str(self.datos))
            self.ui.Cabezera.setEnabled(True)
            self.ui.Archivo.setEnabled(False)
            

    def Cabezera(self):
        datos = self.fuente.read(32)
        print(datos)
        print(datos[9:14].decode('utf-8'), (datos[4]*256)+datos[5])
        


    def Datos(self):
        pass
    def Agregar(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())