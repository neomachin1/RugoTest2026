from ui_rugo2024 import Ui_MainWindow
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QFileDialog, QMessageBox
import serial.tools.list_ports
import os
from time import sleep
import icono_rc
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import * #pyqtSignal, QObject
from PySide6.QtGui import QPixmap

from serial import Serial
from serial import SerialException
from time import sleep


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.setWindowIcon(QtGui.QIcon('usb.png'))
        pixmap = QPixmap('usb2.png')
        self.ui.Icono.setPixmap(pixmap)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)#FramelessWindowHint
        
        self.ui.BLeer.clicked.connect(self.LeerM)#LeerM)#CSVfile)#LeerM)
        self.ui.BBorrar.clicked.connect(self.BorraM)#Recupera)
        self.ui.BSalir.clicked.connect(self.SalirM)
        
        self.ui.MenuL.triggered.connect(self.LeerM)
        self.ui.MenuB.triggered.connect(self.BorraM)
        self.ui.MenuR.triggered.connect(self.Recupera)
        self.ui.MenuS.triggered.connect(self.SalirM)
        
        self.ui.ListB.itemDoubleClicked.connect(self.Ejecutar)
        self.serie = self.Escanear()
        self.carpeta = []
 
        
        self.ruta=""
        if (self.serie):
            self.ui.PuertoS.addItem(None)
            for x in self.serie:
                self.ui.PuertoS.addItem(x)


    def cabezera(self, nData, nFile):
        with open(nFile, 'w') as Grabar:        
            Grabar.write('VIA\t\t:\t' + nData[9:14].decode('utf-8') + '\n')
            Grabar.write('KM \t\t:\t' + str((nData[5]*256)+nData[4]) + '.' + str(nData[6]) + '\n')
            Grabar.write('LONG\t\t:\t' + str(nData[7]*10) + '\n')
            Grabar.write('SENTIDO\t\t:\t' + chr(nData[8]) + '\n')
            Grabar.write('HORA\t\t:\t' + str(nData[14])+':'+str(nData[15])+':'+str(nData[16]) + '\n')
            Grabar.write('FECHA\t\t:\t'+str(nData[17])+'/'+str(nData[18])+'/'+ str(nData[19]) + '\n')
            Grabar.write('LATITUD\t\t:\t' + str(nData[20])+str(nData[21])+"."+str(nData[22])+str(nData[23])+' '+chr(nData[24]) + '\n')
            Grabar.write('LONGITUD\t:\t' + str(nData[25])+str(nData[26])+"."+str(nData[27])+str(nData[28])+' '+chr(nData[29]) + '\n')
            Grabar.write('----------------------------------------------------\n')
            Grabar.write('BUMP1\t\tBUMP2\t\tHORA\t\tLATITUD\t\tLONGITUD\n')

    def data(self, nData, nFile):
        with open(nFile, 'a') as Grabar:
            Grabar.write(str(nData[0] + (nData[1]*256)) + '\t\t' + str(nData[2] + (nData[3]*256)) + '\t\t') #BUMP
            Grabar.write(str(nData[4]).zfill(2)+':'+str(nData[5]).zfill(2)+':'+str(nData[6]).zfill(2) + '\t')                        #HORA
            Grabar.write(str(nData[7]) + str(nData[8])+"." + str(nData[9]) + str(nData[10]) + ' S' + '\t')        #LATITUD
            Grabar.write(str(nData[11]) + str(nData[12]) + "." + str(nData[13]) + str(nData[14]) + ' W' + '\n')       #LONGITUD

    def LeerM(self):
        puerto = self.ui.PuertoS.currentText()
        
        if puerto != "":
            DirArchivo, _ = QFileDialog.getSaveFileName(self, "File", "RugoBump.dat")
            
            if DirArchivo != '':
                Archivo = os.path.basename(DirArchivo)
                self.carpeta.append(os.path.dirname(DirArchivo))
                #print(Archivo, self.carpeta[0])
                 
                try:
                    with Serial(puerto, baudrate=115200, timeout=1) as ser:  #57600
                        ser.write(b'US10')
                        RData = ser.read(8)
                        TData = (RData[2]*256)+RData[1]
                        PData = (TData) // 32#128
                        if ((PData%32) != 0):#128
                            PData+=1

                        if TData > 0:
                            f = open(Archivo, 'wb')
                            f.write(RData[1:4])     #Cabecera de Datos Nuevo

                            for paginas in range(PData):
                                ser.write(b'US11')
                                RData = bytes(ser.read(32))#128
                                f.write(RData)
                            f.close()

                        else:
                            self.ui.Estado.setText("Lectura Memoria Vacia")

                        ser.write(b'US13')
                        
                except SerialException as e:
                    print(e)
                    return
                
                fuente = open(Archivo, 'rb')
                fuente.seek(0, os.SEEK_END)
                TotalFile = fuente.tell()-3
                fuente.seek(0)
                patron = Archivo[:-4]
                
                ListaFile = []
                self.ui.ListB.clear()
                
                datos = fuente.read(3)
                TotalMem = (datos[0]+(datos[1]*256))
                cabeza = bytes([85, 170, 85, 170])
                #print("Total Mem ", TotalMem, TData, datos[:4], len(datos[:4]), cabeza)
                nFile = 0

                if (TotalFile >= TotalMem):
                    while(TotalMem):
                        datos = fuente.read(16)
                        TotalMem-=16
                        if (datos[:4]  == bytes(cabeza)):
                            nFile+=1
                            Archivo = patron
                            Archivo+=str(nFile)+".txt"
                            ListaFile.append(Archivo)
                            datos += fuente.read(16)
                            TotalMem-=16
                            #print(Archivo, TotalMem)
                            print(datos, TotalMem)
                            self.cabezera(datos, Archivo)
                        else:
                            print(TotalMem, datos)
                            self.data(datos, Archivo)
                fuente.close()                 
                
                self.ui.statusbar.showMessage("Data Convertida")
                self.ui.ListB.addItems(ListaFile)
                self.ui.Estado.setText('Archivos Recuperados ' + str(self.ui.ListB.count()))
            else:
                self.ui.statusbar.showMessage("Proceso No Realizado")
                self.ui.Estado.setText('Datos no descargados')

        else:
            QMessageBox.about(self, "Error Puerto "" Hardware", "Equipo no conectado")
    
    def BorraM(self):
        self.ui.statusbar.showMessage("Borrar Memoria")
        puerto = self.ui.PuertoS.currentText()
        
        if puerto != "":
            print(puerto, "Conectado")
            try:
                with Serial(puerto, baudrate=115200, timeout=1) as ser:#57600
                    ser.write(b'US12')
                    sleep(1)
                    QMessageBox.information(self, "Borrar Memoria", "Memoria Libre")
            except:
                QMessageBox.about(self, "no enviado u2", "no enviado u2")
        else:
            QMessageBox.about(self, "Equipo no conectado", "Seleccione Puerto")
        
    def SalirM(self):
        print('Exit')
        self.ui.statusbar.showMessage("Salir")
        self.close()

    def Recupera(self):
        ruta, data = QFileDialog.getOpenFileName(self, 'Recuperar Archivo Rugosimetro', '', 'Roughness File (*.dat *.rbd)')
        if ruta != "":
            self.carpeta.append(os.path.dirname(ruta))
            print(self.carpeta)
            ruta = os.path.basename(ruta)
            total = os.path.getsize(ruta)
            print('Tamaño de datos leido Recupera', total)

            fuente = open(ruta, 'rb')
            fuente.seek(0, os.SEEK_END)
            TotalFile = fuente.tell()-3
            fuente.seek(0)
            
            patron = ruta[:-4]
            ListaFile = []
            self.ui.ListB.clear()
            
            datos = fuente.read(3)
            TotalMem = (datos[0]+(datos[1]*256))
            cabeza = bytes([85, 170, 85, 170])
            #print("Total Mem ", TotalMem, TData, datos[:4], len(datos[:4]), cabeza)
            nFile = 0

            if (TotalFile >= TotalMem):
                while(TotalMem):
                    datos = fuente.read(16)
                    TotalMem-=16
                    if (datos[:4]  == bytes(cabeza)):
                        nFile+=1
                        Archivo = patron
                        Archivo+=str(nFile)+".txt"
                        ListaFile.append(Archivo)
                        datos += fuente.read(16)
                        TotalMem-=16
                        #print(Archivo, TotalMem)
                        self.cabezera(datos, Archivo)
                    else:
                        self.data(datos, Archivo)
            fuente.close()                 










            

            
            
            self.ui.statusbar.showMessage("Data Recuperada")
            self.ui.ListB.addItems(ListaFile)
            self.ui.Estado.setText('Archivos Recuperados ' + str(self.ui.ListB.count()))

    def Escanear(self):
        try:
            ports = serial.tools.list_ports.comports()
            puertos = []
            for port, desc, hwid in sorted(ports):
                puerto = port
                puertos.append(puerto)
                #self.ui.statusbar.shooswMessage("Puerto serie detectados")
        except:
            self.ui.statusbar.showMessage("Error scan puerto serie")
        return puertos

    def Ejecutar(self):
        ejecuta = self.carpeta[0]+'/'+ self.ui.ListB.currentItem().text()
        os.startfile(ejecuta)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())