# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rugo2024Jfkhtf.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)
import icono_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(310, 304)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u"../../../../.designer/LogoInversiones.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        MainWindow.setIconSize(QSize(36, 36))
        self.MenuL = QAction(MainWindow)
        self.MenuL.setObjectName(u"MenuL")
        font1 = QFont()
        font1.setBold(True)
        self.MenuL.setFont(font1)
        self.MenuB = QAction(MainWindow)
        self.MenuB.setObjectName(u"MenuB")
        self.MenuR = QAction(MainWindow)
        self.MenuR.setObjectName(u"MenuR")
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName(u"actionSalir")
        self.MenuS = QAction(MainWindow)
        self.MenuS.setObjectName(u"MenuS")
        self.MenuA = QAction(MainWindow)
        self.MenuA.setObjectName(u"MenuA")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.PuertoS = QComboBox(self.centralwidget)
        self.PuertoS.setObjectName(u"PuertoS")
        self.PuertoS.setGeometry(QRect(150, 40, 141, 22))
        self.Selec = QLabel(self.centralwidget)
        self.Selec.setObjectName(u"Selec")
        self.Selec.setGeometry(QRect(140, 20, 151, 16))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(False)
        self.Selec.setFont(font2)
        self.Selec.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(23, 120, 123, 112))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.BLeer = QPushButton(self.verticalLayoutWidget)
        self.BLeer.setObjectName(u"BLeer")
        font3 = QFont()
        font3.setPointSize(9)
        font3.setBold(True)
        font3.setItalic(False)
        self.BLeer.setFont(font3)

        self.verticalLayout.addWidget(self.BLeer)

        self.BBorrar = QPushButton(self.verticalLayoutWidget)
        self.BBorrar.setObjectName(u"BBorrar")
        self.BBorrar.setFont(font3)

        self.verticalLayout.addWidget(self.BBorrar)

        self.BSalir = QPushButton(self.verticalLayoutWidget)
        self.BSalir.setObjectName(u"BSalir")
        self.BSalir.setFont(font3)

        self.verticalLayout.addWidget(self.BSalir)

        self.Icono = QLabel(self.centralwidget)
        self.Icono.setObjectName(u"Icono")
        self.Icono.setGeometry(QRect(30, 10, 101, 101))
        self.Icono.setStyleSheet(u"image: url(:/images/usb2.png);")
        self.Icono.setFrameShape(QFrame.Shape.StyledPanel)
        self.Icono.setFrameShadow(QFrame.Shadow.Raised)
        self.Icono.setLineWidth(0)
        self.Icono.setMidLineWidth(0)
        self.Icono.setTextFormat(Qt.TextFormat.AutoText)
        self.Icono.setScaledContents(True)
        self.Icono.setWordWrap(False)
        self.Icono.setMargin(0)
        self.Estado = QLabel(self.centralwidget)
        self.Estado.setObjectName(u"Estado")
        self.Estado.setGeometry(QRect(20, 230, 271, 21))
        self.Estado.setFrameShape(QFrame.Shape.Panel)
        self.Estado.setFrameShadow(QFrame.Shadow.Raised)
        self.Estado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ListB = QListWidget(self.centralwidget)
        self.ListB.setObjectName(u"ListB")
        self.ListB.setEnabled(True)
        self.ListB.setGeometry(QRect(150, 70, 141, 151))
        self.ListB.setStyleSheet(u"")
        self.ListB.setFrameShape(QFrame.Shape.StyledPanel)
        self.ListB.setFrameShadow(QFrame.Shadow.Raised)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 310, 21))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuArchivo.setFont(font)
        self.menuAcerca_de = QMenu(self.menubar)
        self.menuAcerca_de.setObjectName(u"menuAcerca_de")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuAcerca_de.menuAction())
        self.menuArchivo.addAction(self.MenuL)
        self.menuArchivo.addAction(self.MenuB)
        self.menuArchivo.addAction(self.MenuR)
        self.menuArchivo.addSeparator()
        self.menuArchivo.addAction(self.MenuS)
        self.menuAcerca_de.addAction(self.MenuA)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bump Integrator 2026", None))
        self.MenuL.setText(QCoreApplication.translate("MainWindow", u"Leer memoria", None))
        self.MenuB.setText(QCoreApplication.translate("MainWindow", u"Borrar Memoria", None))
        self.MenuR.setText(QCoreApplication.translate("MainWindow", u"Recuperar", None))
        self.actionSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.MenuS.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.MenuA.setText(QCoreApplication.translate("MainWindow", u"Acerca de ...", None))
        self.Selec.setText(QCoreApplication.translate("MainWindow", u"Seleccion Puerto", None))
        self.BLeer.setText(QCoreApplication.translate("MainWindow", u"Leer Memoria", None))
        self.BBorrar.setText(QCoreApplication.translate("MainWindow", u"Borrar Memoria", None))
        self.BSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.Icono.setText("")
        self.Estado.setText("")
        self.menuArchivo.setTitle(QCoreApplication.translate("MainWindow", u"Archivo", None))
        self.menuAcerca_de.setTitle(QCoreApplication.translate("MainWindow", u"Ayuda", None))
    # retranslateUi

