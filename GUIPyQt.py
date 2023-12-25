import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class VentanaPrincipal(QMainWindow): #Crea la ventana usando QDialog
    def __init__(self):
        super().__init__()
        # Cargar el archivo de interfaz UI
        loadUi("GUI/Preguntas y respuestas.ui", self)
        self.setWindowTitle("Preguntas y Respuestas")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

    def eventoXD(self):
        self.lbl_cicloWhile.setPixmap(QPixmap("Imagenes/arbol.jpg").scaled(self.lbl_cicloWhile.size(), aspectRatioMode=True))
        self.lbl_cicloWhile.setStyleSheet("border: 2px solid blue;")
            
        

        

if __name__ == "__main__": #Se ejecuta si el archivo se ejecuta directamente y no se importa como un modulo
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())


