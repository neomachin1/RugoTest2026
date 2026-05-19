from rugo2024 import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import serial.tools.list_ports
import os
from time import sleep
import icono_rc
#import hashlib
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap

from serial import Serial
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
        
        self.ui.BLeer.clicked.connect(self.LeerM)#CSVfile)#LeerM)
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

    def LeerM(self):
        puerto = self.ui.PuertoS.currentText()
        
        if puerto != "":
            print(puerto)
            DirArchivo, _ = QFileDialog.getSaveFileName(self, "File", "DataBump.bin")
            
            if DirArchivo != '':
                Archivo = os.path.basename(DirArchivo)
                self.carpeta.append(os.path.dirname(DirArchivo))
                print(Archivo, self.carpeta[0])
                 
                try:
                    with Serial(puerto, baudrate=57600, timeout=1) as ser:
                        ser.write(b'U0')
                        sleep(0.1)
                        RData = ser.read(8)
                        TData = (RData[2]*256)+RData[1]
                        PData = (TData//128) + 1
                        print('Mensaje U0', RData)
                        print('Numero de Datos: ', TData)
                        print('Numero de paginas: ', PData)
                        print('3 datos', RData[1:4])

                        sleep(0.1)
                        if TData > 0:
                            f = open(Archivo, 'wb')
                            f.write(RData[1:4])     #Cabecera de Datos Nuevo
                            print('cabezera nueva', RData[1:4])
                            for paginas in range(PData):
                                print(paginas)
                                ser.write(b'U1')
                                sleep(0.1)
                                RData = bytes(ser.read(128))
                                print(paginas, RData)
                                f.write(RData)
                            f.close()
                            
                        self.ui.statusbar.showMessage("Lectura Memoria Completa")
                        print('Fin file base')
                except:
                    QMessageBox.about(self, "Error Hardware", "serial with")
                    return
                
                patron = Archivo[:-4]
                fuente = open(Archivo, 'rb')
                print(os.path.getsize(Archivo))
                
                a = fuente.read(3)
                total = TData
                print('cabezera insertada', a)
                print('total descargado', total)
                
                counter = 0
                ListaFile = []
                self.ui.ListB.clear()

                while (total > 0):
                    a = fuente.read(4)#iniciamos lectura datos
                    total-=4

                    if (a[0] == 85) & (a[1] == 170) & (a[2] == 85) & (a[3] == 170):
                        archivo = patron+str(counter)+'.txt'
                        ListaFile.append(archivo)
                        
                        counter+=1
                        a = fuente.read(28)
                        total-=28

                        archivos = open(archivo, 'w')
                        archivos.write('VIA  : \t')
                        archivos.write(a[5:10].decode('utf-8'))
                        archivos.write('\n')
                        archivos.write('KM   : \t')
                        archivos.write(str((a[0]*256)+a[1]))
                        archivos.write('\n')
                        archivos.write('LONG : \t'+str(a[3]*100))
                        archivos.write('\n')
                        archivos.write('HORA : \t'+str(a[10])+':'+str(a[11])+':'+str(a[12]))
                        archivos.write('\n')
                        archivos.write('FECHA: \t'+str(a[13])+'/'+str(a[14])+'/'+ str(a[15]))
                        archivos.write('\n')
                        archivos.write('LATITUD : \t')
                        #archivos.write(str(a[16])+str(a[17])+"."+str(a[18])+str(a[19])+' '+chr(a[20]))
                        lati = float(a[16]) + float("{:.6f}".format(float(str(a[17]) + "." + str(a[18]) + str(a[19])) /60 ))
                        archivos.write("-" + str(lati) + '\t')
                        archivos.write('\n')
                        archivos.write('LONGITUD : \t')
                        #archivos.write(str(a[21])+str(a[22])+"."+str(a[23])+str(a[24])+' '+chr(a[25]))
                        longi = float(a[21]) + float("{:.6f}".format(float(str(a[22]) + "." + str(a[23]) + str(a[24])) /60 ))
                        archivos.write("-" + str(longi) + '\n') 
                        archivos.write('\n')
                        archivos.write('----------------------------------------------------\n')
                        archivos.write('BUMP1\tBUMP2\tHORA\t\tLATITUD\tLONGITUD\n')
                        archivos.close()
       
                    elif (a[0] != 255) & (a[1] != 255) & (a[2] != 255) & (a[3] != 255):
                        a += fuente.read(12)
                        total-=12
     
                        archivos = open(archivo, 'a')
                        archivos.write(str((a[0]*256)+a[1])+'\t')
                        archivos.write(str((a[2]*256)+a[3])+'\t')
                        archivos.write(str(a[4])+':'+str(a[5])+':'+str(a[6])+'\t')
                        #archivos.write(str(a[7])+str(a[8])+"."+str(a[9])+str(a[10])+' S'+'\t')
                        lati = float(a[7]) + float("{:.6f}".format(float(str(a[8]) + "." + str(a[9]) + str(a[10])) /60 ))
                        archivos.write("-" + str(lati) + '\t')
                        #archivos.write(str(a[11])+str(a[12])+"."+str(a[13])+str(a[14])+' W'+'\n')
                        longi = float(a[11]) + float("{:.6f}".format(float(str(a[12]) + "." + str(a[13]) + str(a[14])) /60 ))
                        archivos.write("-" + str(longi) + '\n')
                        archivos.close()
                        
                fuente.close()
                self.ui.statusbar.showMessage("Data Convertida")
                self.ui.ListB.addItems(ListaFile)
                self.ui.Estado.setText('Archivos Recuperados ' + str(self.ui.ListB.count()))
            else:
                self.ui.statusbar.showMessage("Proceso No Realizado")
                self.ui.Estado.setText('Datos no descargados')

        else:
            QMessageBox.about(self, "Error Puerto "" Hardware", "Equipo no conectado")
        
        #self.ui.statusbar.showMessage("Boton Leer Memoria")
    
    def BorraM(self):
        self.ui.statusbar.showMessage("Borrar Memoria")
        puerto = self.ui.PuertoS.currentText()
        
        if puerto != "":
            print(puerto, "Conectado")
            try:
                with Serial(puerto, baudrate=57600, timeout=1) as ser:
                    ser.write(b'U2')
                    sleep(2)
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
        ruta, data = QFileDialog.getOpenFileName(self, 'Recuperar Archivo Rugosimetro', '', 'Roughness File (*.bin *.rbd)')
        if ruta != "":
            self.carpeta.append(os.path.dirname(ruta))
            print(self.carpeta)
            ruta = os.path.basename(ruta)
            total = os.path.getsize(ruta)
            print('Tamaño de datos leido Recupera', total)

            patron = ruta[:-4]
            fuente = open(ruta, 'rb')
            a = fuente.read(3)
            
            total = a[2]+(a[1]*256)+a[0]
            print('valor de archivo Recupera:', total, patron, ruta)
            counter = 0
            self.ui.ListB.clear()
            ListaFile = []

            while (total > 0) & (total>=12):
                a = fuente.read(4)#iniciamos lectura datos
                total-=4
                print(total, a)

                if ((a[0] == 85) & (a[1] == 170) & (a[2] == 85) & (a[3] == 170)):
                    archivo = patron+str(counter)+'.txt'
                    ListaFile.append(archivo)
                    
                    counter+=1
                    a = fuente.read(28)
                    print(a)
                    total-=28

                    archivos = open(archivo, 'w')
                    archivos.write('VIA  : \t')
                    archivos.write(a[5:10].decode('utf-8'))
                    archivos.write('\n')
                    archivos.write('KM   : \t')
                    archivos.write(str((a[0]*256)+a[1]))
                    archivos.write('\n')
                    archivos.write('LONG : \t'+str(a[3]*100))
                    archivos.write('\n')
                    archivos.write('HORA : \t'+str(a[10])+':'+str(a[11])+':'+str(a[12]))
                    archivos.write('\n')
                    archivos.write('FECHA: \t'+str(a[13])+'/'+ str(a[14])+'/'+str(a[15]))
                    archivos.write('\n')
                    archivos.write('LATITUD : \t')
                    #archivos.write(str(a[16])+str(a[17])+"."+str(a[18])+str(a[19])+chr(a[20]))
                    lati = float(a[16]) + float("{:.6f}".format(float(str(a[17]) + "." + str(a[18]) + str(a[19])) /60 ))
                    archivos.write("-" + str(lati) + '\t')
                    archivos.write('\n')
                    archivos.write('LONGITUD : \t')
                    #archivos.write(str(a[21])+str(a[22])+"."+str(a[23])+str(a[24])+' '+chr(a[25]))
                    longi = float(a[21]) + float("{:.6f}".format(float(str(a[22]) + "." + str(a[23]) + str(a[24])) /60 ))
                    archivos.write("-" + str(longi) + '\n')                   
                    
                    archivos.write('\n')
                    archivos.write('----------------------------------------------------\n')
                    archivos.write('BUMP1\tBUMP2\tHORA\t\tLATITUD\tLONGITUD\n')
                    archivos.close()
   
                elif (a[0] != 255):# & (a[1] != 255):# & (a[2] != 255):# & (a[3] != 255):
                    a += fuente.read(12)
                    print(a)
                    total-=12
 
                    archivos = open(archivo, 'a')
                    archivos.write(str((a[0]*256)+a[1])+'\t')
                    archivos.write(str((a[2]*256)+a[3])+'\t')
                    archivos.write(str(a[4])+':'+str(a[5])+':'+str(a[6])+'\t')
                    #archivos.write(str(a[7])+str(a[8])+"."+str(a[9])+str(a[10])+' S'+'\t')
                    lati = float(a[7]) + float("{:.6f}".format(float(str(a[8]) + "." + str(a[9]) + str(a[10])) /60 ))
                    archivos.write("-" + str(lati) + '\t')
                    #archivos.write(str(a[11])+str(a[12])+"."+str(a[13])+str(a[14])+' W'+'\n')
                    longi = float(a[11]) + float("{:.6f}".format(float(str(a[12]) + "." + str(a[13]) + str(a[14])) /60 ))
                    archivos.write("-" + str(longi) + '\n')
                    #print(str(a[7]), str(a[8]), str(a[9]), str(a[10]))
                    archivos.close()

                else:
                    self.ui.statusbar.showMessage("Error en Data")
                    break
            
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