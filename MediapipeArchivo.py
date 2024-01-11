import cv2
import mediapipe as mp
import math

#import keyboard
import sys
from PyQt5.QtWidgets import QApplication, QDialog,QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt,QFile
from PyQt5.QtGui import QPixmap, QMovie
import random

from ventanas import preguntas
from ventanas import gifs
from pynput import keyboard



    #--------------------Funciones------------------------------------------
    #Calcula los puntos de los dedos
def deteccion_puntos_manos(manoLandmark):
    puntos = [8, 12, 16, 20]
    muñecaLandmark = manoLandmark[0]
    dedosCount = 0

    dedoPulgarDistancia = calcularDistanciaDedos(manoLandmark[4], muñecaLandmark)
    if dedoPulgarDistancia > 0.2: #0.00001
            dedosCount += 1

    for puntosIndice in puntos:
        dedoLandmark = manoLandmark[puntosIndice]
        dedoMuñecaDistancia = calcularDistanciaDedos(dedoLandmark, muñecaLandmark)

        if dedoMuñecaDistancia > 0.3: #0.1
            dedosCount += 1
    return dedosCount

    #Calcula la distacia de los puntos de los dedos con la muñeca
def calcularDistanciaDedos(dedo, muñeca):
    x1, y1, z1 = dedo.x, dedo.y, dedo.z
    x2, y2, z2 = muñeca.x, muñeca.y, muñeca.z

    distancia = math.sqrt(((x2-x1)**2 + (y2-y1)**2) + (abs(z1 * 2)))  # <----------(abs(z1 * 2))) Distacia 
    return distancia
    #-------------------------------------------------------------------------------

#Instancias de los modulos y estilo
instaciaPreguntas = preguntas
instanciaGiftsCorrectos = gifs.gifts_correctos
instanciaGiftsIncorrectos = gifs.gifts_incorrectos
estiloCss = "style/style.css"

#Numero de la pregunta en pantalla
class VentanaPrincipal(QMainWindow): #Crea la ventana usando QDialog
    def __init__(self):
        super().__init__()
        # Cargar el archivo de interfaz UI
        loadUi("GUI/Preguntas y respuestas.ui", self)
        self.setWindowTitle("Preguntas y Respuestas")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        #Elige una pregunta al azar
        self.preguntasRandomLista = [getattr(instaciaPreguntas, nombre) for nombre in dir(instaciaPreguntas) if callable(getattr(instaciaPreguntas, nombre))]
        #self.preguntasRandom = [instaciaPreguntas.preg_2, instaciaPreguntas.preg_3]
        self.preguntasRandom = random.choice(self.preguntasRandomLista)

        #Establece la pregunta en ventana
        self.lblTitulo.setText(self.preguntasRandom()[2])
        self.lblTitulo.setStyleSheet(f"color: white; font-size: {self.preguntasRandom()[3]}; font-family: Comic Sans MS;")

        #Establece las imagenes en ventana
        self.lblimagen1.setPixmap(QPixmap(self.preguntasRandom()[0]).scaled(self.lblimagen1.size(), aspectRatioMode=True))
        self.lblimagen2.setPixmap(QPixmap(self.preguntasRandom()[1]).scaled(self.lblimagen2.size(), aspectRatioMode=True))

        #Permite que no se repitan las preguntas
        self.preguntasRandomLista.remove(self.preguntasRandom)

        #Detecta ciertas teclas para dar paso a eventos
        self.listenerSigPregunta = keyboard.Listener(on_press=self.siguiente_pregunta)
        self.listenerReinPregunta = keyboard.Listener(on_press=self.reiniciar_pregunta)
        self.listenerSigPregunta.start()
        self.listenerReinPregunta.start()

        #Asigna el numero a la pregunta
        self.numeroPregunta = 1
        self.lblNumPregunta.setText(str(self.numeroPregunta))
        self.lblNumPregunta.setStyleSheet(open(estiloCss).read())

        self.controladorDePausa = False #<--- Hace que la opcion de eleccion de preguntas se detecta a pesar de continuar el bucle de la funcion de mediapipe
        self.funcion_Mediapipe()





    #Funcion que da paso a la siguiente pregunta, usando teclas "enter" o "espacio"
    def siguiente_pregunta(self, key):
        if key == keyboard.Key.enter or key == keyboard.Key.space:
            #Elige una pregunta al azar
            self.preguntasRandom = random.choice(self.preguntasRandomLista)

            #Quita el gif del label
            self.lblimgReaccion.clear()

            #Suma el numero de la pregunta
            self.numeroPregunta += 1

            #Numero de la pregunta en pantalla
            self.lblNumPregunta.setText(str(self.numeroPregunta))
            self.lblNumPregunta.setStyleSheet(open(estiloCss).read())

            #Establece la pregunta en ventana
            self.lblTitulo.setText(self.preguntasRandom()[2])
            self.lblTitulo.setStyleSheet(f"color: white; font-size: {self.preguntasRandom()[3]}; font-family: Comic Sans MS;")

            #Establece las imagenes en ventana
            self.lblimagen1.setPixmap(QPixmap(self.preguntasRandom()[0]).scaled(self.lblimagen1.size(), aspectRatioMode=True))
            self.lblimagen2.setPixmap(QPixmap(self.preguntasRandom()[1]).scaled(self.lblimagen2.size(), aspectRatioMode=True))
            
            #Si es True permite que los recuadros amarillos, rojo o verde se mantengan estaticos en pantalla y si es False, no los mantiene estaticos
            self.controladorDePausa = False

            #Quita la pregunta de la lista para que no se vuelva a repetir
            self.preguntasRandomLista.remove(self.preguntasRandom)
            
            #Actualiza el evento en ventana
            QApplication.processEvents()





    #Permite reiniciar la pregunta cuando se presiona la tecla "R" del teclado
    def reiniciar_pregunta(self, key):
        if key == keyboard.KeyCode.from_char('r'):

            #Quita el gif del label
            self.lblimgReaccion.clear()

            #Si es True permite que los recuadros amarillos, rojo o verde se mantengan estaticos en pantalla y si es False, no los mantiene estaticos
            self.controladorDePausa = False


        

    def funcion_Mediapipe(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        with mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=0,
            smooth_landmarks=True) as holistic:

            while True:
                ret, frame = cap.read()
                if ret == False:
                    break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                

                results = holistic.process(frame_rgb)
                

                # Mano izquieda
                mp_drawing.draw_landmarks(
                    frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))
                #-------------------------- Primer punto------------------------
                puntoZDedoStr = str
                if results.right_hand_landmarks is not None:
                    puntoZDedo= results.right_hand_landmarks.landmark[8] #________________________________________ Punto z indice
                    puntoZDedo = puntoZDedo.z
                    puntoZDedoStr = str(puntoZDedo)

                puntoXDedoStr = str
                if results.right_hand_landmarks is not None:
                    puntoXDedo= results.right_hand_landmarks.landmark[8] #________________________________________ Punto x indice
                    puntoXDedo = puntoXDedo.x
                    puntoXDedoStr = str(puntoXDedo)

                puntoYDedoStr = str
                if results.right_hand_landmarks is not None:
                    puntoYDedo= results.right_hand_landmarks.landmark[8] #________________________________________ Punto y indice
                    puntoYDedo = puntoYDedo.y
                    puntoYDedoStr = str(puntoYDedo)

                    #-------------------------- Segundo punto------------------------
                puntoZDedoStr2 = str
                if results.right_hand_landmarks is not None:
                    puntoZDedo2= results.right_hand_landmarks.landmark[0] #________________________________________ Punto z indice
                    puntoZDedo2 = puntoZDedo2.z
                    puntoZDedoStr2 = str(puntoZDedo2)

                puntoXDedoStr2 = str
                if results.right_hand_landmarks is not None:
                    puntoXDedo2= results.right_hand_landmarks.landmark[0] #________________________________________ Punto x indice
                    puntoXDedo2 = puntoXDedo2.x
                    puntoXDedoStr2 = str(puntoXDedo2)

                puntoYDedoStr2 = str
                if results.right_hand_landmarks is not None:
                    puntoYDedo2= results.right_hand_landmarks.landmark[0] #________________________________________ Punto y indice
                    puntoYDedo2 = puntoYDedo2.y
                    puntoYDedoStr2 = str(puntoYDedo2)
                

                # Mano derecha
                mp_drawing.draw_landmarks(
                    frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))
                


                dedosDerecha = 0
                dedosIzquierda = 0
                manoDerechaCerrada = False
                manoIzquierdaCerrada = False
                #Deteccion puntos manos
                if results.right_hand_landmarks:
                    dedosDerecha += deteccion_puntos_manos(results.right_hand_landmarks.landmark)
                    if dedosDerecha <= 1:
                        manoDerechaCerrada = True

                if results.left_hand_landmarks:
                    dedosIzquierda += deteccion_puntos_manos(results.left_hand_landmarks.landmark)
                    if dedosIzquierda <= 1:
                        manoIzquierdaCerrada = True

                    

                # Postura
                mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))
                
                xI, yI = 0.0, 0.0
                xD, yD = 0.0, 0.0
                puntoYIzquierda = False
                puntoYDerecha = False
                #Deteccion de puntos postura
                if results.pose_landmarks is not None:
                    puntoMuñecaIzquierda = results.pose_landmarks.landmark[15]
                    puntoMuñecaDerecha = results.pose_landmarks.landmark[16]
                    
                    yI= puntoMuñecaIzquierda.y
                    yD = puntoMuñecaDerecha.y
                    if yI <= 0.4:
                        puntoYIzquierda = True

                    if yD <= 0.4:
                        puntoYDerecha = True


                
                #Invierte la imagen
                frame = cv2.flip(frame, 1)

                #Texto en pantalla
                cv2.putText(frame, "Numero de dedos: "+ str(dedosIzquierda), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(frame, "Eje Y: "+ str(yD),(100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                

                #Texto en pantalla de manos cerradas
                if manoIzquierdaCerrada == True:
                    cv2.putText(frame, "Mano izquierda cerrada", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if manoDerechaCerrada == True:
                    cv2.putText(frame, "Mano derecha cerrada", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)




                #Logica de las preguntas
                opcionCorrectaVar = None
                if puntoYDerecha == True and self.controladorDePausa == False:
                    cv2.putText(frame, "Derecha Activado", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    self.lblimagen2.setStyleSheet("border: 30px solid #ffbe0b; border-radius: 50px;")
                    if manoDerechaCerrada == True:
                        self.lblimagen2.setStyleSheet("border: 30px solid #d59e09; border-radius: 50px;")
                        opcionCorrectaVar = self.preguntasRandom()[5]

                    QApplication.processEvents()
                elif self.controladorDePausa == False:
                    self.lblimagen2.setStyleSheet("border: none;")
                    QApplication.processEvents()
                    
                if puntoYIzquierda == True and self.controladorDePausa == False:
                    cv2.putText(frame, "Izquierda Activado", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    self.lblimagen1.setStyleSheet("border: 30px solid #ffbe0b; border-radius: 50px;")
                    if manoIzquierdaCerrada == True:
                        self.lblimagen1.setStyleSheet("border: 30px solid #d59e09; border-radius: 50px;")
                        opcionCorrectaVar = self.preguntasRandom()[4]
                    QApplication.processEvents()
                    
                elif self.controladorDePausa == False:
                    self.lblimagen1.setStyleSheet("border: none;")
                    QApplication.processEvents()





                #se activa se la respuesta es correcta
                if opcionCorrectaVar == True and self.controladorDePausa == False:
                    if manoDerechaCerrada == True:
                        self.lblimagen2.setStyleSheet("border: 30px solid #00bf63; border-radius: 50px;")
                    
                    if manoIzquierdaCerrada == True:
                        self.lblimagen1.setStyleSheet("border: 30px solid #00bf63; border-radius: 50px;")

                    self.controladorDePausa = True

                    #Coloca el gif en pantalla
                    self.cargaGift = QMovie(instanciaGiftsCorrectos())
                    self.lblimgReaccion.setMovie(self.cargaGift)
                    self.cargaGift.start()
                    QApplication.processEvents()

                #se activa se la respuesta es incorrecta
                if opcionCorrectaVar == False and self.controladorDePausa == False:
                    if manoDerechaCerrada == True:
                        self.lblimagen2.setStyleSheet("border: 30px solid #ff3131; border-radius: 50px;")
                        self.lblimagen1.setStyleSheet("border: 30px solid #00bf63; border-radius: 50px;")
                    
                    if manoIzquierdaCerrada == True:
                        self.lblimagen1.setStyleSheet("border: 30px solid #ff3131; border-radius: 50px;")
                        self.lblimagen2.setStyleSheet("border: 30px solid #00bf63; border-radius: 50px;")
                    
                    self.controladorDePausa = True

                    #Coloca el gif en pantalla
                    self.cargaGift = QMovie(instanciaGiftsIncorrectos())
                    self.lblimgReaccion.setMovie(self.cargaGift)
                    self.cargaGift.start()
                    QApplication.processEvents()
                
                QApplication.processEvents()



                #texto de puntos x, y, z en pantalla punto [8]
                cv2.putText(frame, f"Punto x: {puntoXDedoStr}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Punto y: {puntoYDedoStr}", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Punto Z: {puntoZDedoStr}", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                #texto de puntos x, y, z en pantalla punto [0]
                cv2.putText(frame, f"Punto x: {puntoXDedoStr2}", (800, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Punto y: {puntoYDedoStr2}", (800, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(frame, f"Punto Z: {puntoZDedoStr2}", (800, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        #cap.release() #Libera los recursos de cv2.VideoCapture()
        #cv2.destroyAllWindows()
                cv2.imshow("Frame", frame)

#Se ejecuta si el archivo se ejecuta directamente y no se importa como un modulo  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())