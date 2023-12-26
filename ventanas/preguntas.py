import sys
from PyQt5.QtWidgets import QApplication, QDialog,QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import random

#Constructor
class parametros_construc:
    #Atributos
    def __init__(self, puntoYDerecha, puntoYIzquierda, manoDerechaCerrada, manoIzquierdaCerrada) -> None:
        self.varPuntoYDer = puntoYDerecha
        self.varPuntoYIzq = puntoYIzquierda
        self.varManoDCerrada = manoDerechaCerrada
        self.varManoICerrada = manoIzquierdaCerrada

    #Preguntas/eventos
    def preg_1(self):
        pass

    def preg_2(self):
        tituloPregunta = "¿Cuál es el animal más grande del mundo?"
        tamañoFuente = "72px"
        imagen1 = "Imagenes/ballena.jpg"
        imagen2 = "Imagenes/leon.jpeg"
        return imagen1, imagen2, tituloPregunta, tamañoFuente
        
        
    def preg_3(self):
        tituloPregunta = "¿Cuál es el país más grande del mundo?"
        tamañoFuente = "72px"
        imagen1 = "Imagenes\El salvador.jpg"
        imagen2 = "Imagenes\Rusia.jpg"
        return imagen1, imagen2, tituloPregunta, tamañoFuente
        