import cv2
import mediapipe as mp
import math

import sys
from PyQt5.QtWidgets import QApplication, QDialog,QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from ventanas import preguntas
import random




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

    distancia = math.sqrt(((x2-x1)**2 + (y2-y1)**2) + (abs(z1 * 4)))  # <----------(abs(z1 * 2))) Distacia 
    return distancia
    #-------------------------------------------------------------------------------

class VentanaPrincipal(QMainWindow): #Crea la ventana usando QDialog
    def __init__(self):
        super().__init__()
        # Cargar el archivo de interfaz UI
        loadUi("GUI/Preguntas y respuestas.ui", self)
        self.setWindowTitle("Preguntas y Respuestas")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.funcion_Mediapipe()
        self.labelImagenDVar = self.findChild(QLabel, "lblimagen2")
        self.labelImagenIVar = self.findChild(QLabel, "lblimagen1")


    def funcion_Mediapipe(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic

        puntoYDerecha, puntoYIzquierda, manoDerechaCerrada, manoIzquierdaCerrada = 0, 0, 0, 0

        #instaciaPreguntas = preguntas.parametros_construc(puntoYDerecha, puntoYIzquierda, manoDerechaCerrada, manoIzquierdaCerrada)
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

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
                

                # Mano izquieda (azul)
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
                

                # Mano derecha (verde)
                mp_drawing.draw_landmarks(
                    frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))
                


                dedos = 0
                manoDerechaCerrada = False
                manoIzquierdaCerrada = False
                #Deteccion puntos manos
                if results.left_hand_landmarks or results.right_hand_landmarks:
                    if results.left_hand_landmarks:
                        dedos += deteccion_puntos_manos(results.left_hand_landmarks.landmark)
                        if dedos <= 1:
                            manoIzquierdaCerrada = True

                    if results.right_hand_landmarks:
                        dedos += deteccion_puntos_manos(results.right_hand_landmarks.landmark)
                        if dedos <= 1:
                            manoDerechaCerrada = True

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
                    if yI <= 0.3:
                        puntoYIzquierda = True

                    if yD <= 0.3:
                        puntoYDerecha = True


                

                frame = cv2.flip(frame, 1) #Invierte la imagen

                #Texto en pantalla
                cv2.putText(frame, "Numero de dedos: "+ str(dedos), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(frame, "Eje Y: "+ str(yD),(100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                

                #Texto en pantalla de manos cerradas
                if manoIzquierdaCerrada == True:
                    cv2.putText(frame, "Mano izquierda cerrada", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if manoDerechaCerrada == True:
                    cv2.putText(frame, "Mano derecha cerrada", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)




                #Preguntas
                #instaciaPreguntas = preguntas.parametros_construc(puntoYDerecha, puntoYIzquierda, manoDerechaCerrada, manoIzquierdaCerrada)
                #texto en pantalla de puntos Y
                if puntoYDerecha == True:
                    cv2.putText(frame, "Derecha Activado", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    self.lblimagen2.setStyleSheet("border: 30px solid red; border-radius: 50px;")
                    #instaciaPreguntas.preg_1()
                    #self.lbl_cicloWhile.setText("Arriba")
                    #self.close()
                    QApplication.processEvents()
                else:
                    #self.lbl_cicloWhile.setText("Abajo")
                    self.lblimagen2.setStyleSheet("border: none;")
                    QApplication.processEvents()
                    
                if puntoYIzquierda == True:
                    cv2.putText(frame, "Izquierda Activado", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    self.lblimagen1.setStyleSheet("border: 30px solid red; border-radius: 50px;")
                    #instaciaPreguntas.preg_2()
                    QApplication.processEvents()
                else:
                    #self.lbl_cicloWhile.setText("Abajo")
                    self.lblimagen1.setStyleSheet("border: none;")
                    QApplication.processEvents()
                






                #texto de puntos x, y, z en pantalla punto [8]
                cv2.putText(frame, f"Punto x: {puntoXDedoStr}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Punto y: {puntoYDedoStr}", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Punto Z: {puntoZDedoStr}", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                #texto de puntos x, y, z en pantalla punto [0]
                cv2.putText(frame, f"Punto x: {puntoXDedoStr2}", (800, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"Punto y: {puntoYDedoStr2}", (800, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(frame, f"Punto Z: {puntoZDedoStr2}", (800, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                

                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        cap.release() #Libera los recursos de cv2.VideoCapture()
        cv2.destroyAllWindows()
    
if __name__ == "__main__": #Se ejecuta si el archivo se ejecuta directamente y no se importa como un modulo
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())