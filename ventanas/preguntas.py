import sys
from PyQt5.QtWidgets import QApplication, QDialog,QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import random
from MediapipeArchivo import VentanaPrincipal

#Constructor
class parametros_construc():
    # contador = 0
    # if contador <= 0:
    #     random.choice()
    #     contador += 1

    #Atributos
    def __init__(self, puntoYDerecha, puntoYIzquierda, manoDerechaCerrada, manoIzquierdaCerrada) -> None:
        self.varPuntoYDer = puntoYDerecha
        self.varPuntoYIzq = puntoYIzquierda
        self.varManoDCerrada = manoDerechaCerrada
        self.varManoICerrada = manoIzquierdaCerrada
        self.preg_1()
        self.preg_2()


    #Preguntas/eventos
    def preg_1(self):
        imagen = self.lblimagen2.setSt7yleSheet("border: 30px solid red; border-radius: 50px;")
        return imagen
        #self.lblimagen1.setPixmap(QPixmap("Imagenes/Rusia.jpg").scaled(self.lbl_cicloWhile.size(), aspectRatioMode=True))
        # self.lblimagen2.setPixmap(QPixmap("Imagenes/Rusia.jpg").scaled(self.lbl_cicloWhile.size(), aspectRatioMode=True))

        # #bloqueador = False
        # if self.varPuntoYDer == True:
        #     self.lblimagen2.setStyleSheet("border: 10px solid blue;")

        # if self.varPuntoYIzq == True:
        #     self.lblimagen1.setStyleSheet("border: 10px solid blue;")

    def preg_2(self):
        #self.lblimagen1.setPixmap(QPixmap("Imagenes/Rusia.jpg").scaled(self.lbl_cicloWhile.size(), aspectRatioMode=True))
        imagen = VentanaPrincipal.lblimagen1.setStyleSheet("border: 30px solid red; border-radius: 50px;")
        return imagen
        


#Por hacer:
#-crear las preguntas en un modulo