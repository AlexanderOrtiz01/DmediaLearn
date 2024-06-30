import cv2
import mediapipe as mp
import math

import sys
from PyQt5.QtWidgets import QApplication, QDialog,QLabel, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt,QFile
from PyQt5.QtGui import QPixmap, QMovie
import random

from ventanas import preguntas
from ventanas import gifs
from pynput import keyboard

import time

from PIL import Image
import numpy as np


#Todo esto pertenece a MediaPiepe Gestures
#Descarga del modelo y guardado en directorio local
model_path = 'Modelo\gesture_recognizer.task'

#Construimos las tareas
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

#Especificamos la ruta del modelo dentro del parámetro Nombre del modelo
base_options = BaseOptions(model_asset_path=model_path)

    #--------------------Funciones------------------------------------------
#Variables controladoras de mediapipe gestures
gestos = None
puntoYDerecha = False
puntoYIzquierda = False
manoDerechaCerrada = False
manoIzquierdaCerrada = False

#Variables del minijuego
imagenSuperpuestaPath = "Imagenes\GestosEmojisMinijuego\Fondo.png"
            


#Detecta el gesto y la lateralidad de las manos...
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
  #print(type(result.gestures))
  global gestos, puntoYDerecha, puntoYIzquierda, manoDerechaCerrada, manoIzquierdaCerrada
  if (len(result.gestures) != 0):
    gestos = str(result.gestures[0][0].category_name)
    puntoY = result.hand_landmarks[0][0]
    puntoY = puntoY.y
    puntoX = result.hand_landmarks[0][0]
    puntoX = puntoX.x


    #Estas variables se colocan en False para que la seleccion de la opcion se deseleccione al bajar la mano
    puntoYIzquierda = False
    puntoYDerecha = False
    #Punto Y derecha
    if puntoY <= 0.4 and puntoX <= 0.5:
        puntoYDerecha = True
    #Punto Y izquierda
    if puntoY <= 0.4 and puntoX >= 0.5:
        puntoYIzquierda = True


    #Estas variables se colocan en False para que no se guarde la mano cerrada
    manoDerechaCerrada = False
    manoIzquierdaCerrada = False
    #Detecta mano cerrada derecha
    if str(gestos) == "Closed_Fist" and puntoYDerecha == True:
        manoDerechaCerrada =True
    #Detecta mano cerrada izquierda
    if str(gestos) == "Closed_Fist" and puntoYIzquierda == True:
        manoIzquierdaCerrada =True
    print(gestos)



    #------------------Minijuego------------------------
    if str(gestos) == "Closed_Fist" and puntoYDerecha == True:
        manoDerechaCerrada =True






  else:
    gestos = None
    print("Vacio")




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

    distancia = math.sqrt(((x2-x1)**2 + (y2-y1)**2) + (abs(z1 * 5)))  # <----------(abs(z1 * 2))) Distacia  50 = 4 metros aproximadamente
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
        self.listenerMinijuego = keyboard.Listener(on_press=self.minijuego)
        self.listenerIniciarJuego = keyboard.Listener(on_press=self.iniciar_juego)
        self.listenerfinalizarMinijuego = keyboard.Listener(on_press=self.finalizar_Minijuego)
        self.listenerSigPregunta.start()
        self.listenerReinPregunta.start()
        self.listenerMinijuego.start()
        self.listenerIniciarJuego.start()
        self.listenerfinalizarMinijuego.start()

        #Asigna el numero a la pregunta
        self.numeroPregunta = 1
        self.lblNumPregunta.setText(str(self.numeroPregunta))
        self.lblNumPregunta.setStyleSheet(open(estiloCss).read())

        self.controladorDePausa = False #<--- Hace que la opcion de eleccion de preguntas se detecta a pesar de continuar el bucle de la funcion de mediapipe
        
        #Variables de evento iniciar_juego
        self.cuenta3Seg = ""
        self.listaEsquinas = []

        self.rompeCiclo = None
        
        #Variables de funcion_minijuego
        self.activadorEsquina = ""
        self.congelaEsquina1 = self.congelaEsquina2 = self.congelaEsquina3 = self.congelaEsquina4 = False
        self.congelaEsquina1Comparacion = self.congelaEsquina2Comparacion = self.congelaEsquina3Comparacion = self.congelaEsquina4Comparacion = None
        self.congelaEsquina1ComparacionI = self.congelaEsquina2ComparacionI = self.congelaEsquina3ComparacionI = self.congelaEsquina4ComparacionI = False

        self.variableComparar = ""
        self.controladorIniciar_Detener = None

        #Inicia la funcion principal (Ventana principal)
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



    def minijuego(self, key):
        if key == keyboard.KeyCode.from_char('m'):
            self.rompeCiclo = True



    def iniciar_juego(self, key):
        global imagenSuperpuestaPath
        if key == keyboard.KeyCode.from_char('i'):

            #Lista de gestos de las manos
            listaGestos = {"Thumb_Up":"Imagenes\GestosEmojisMinijuego\Pulgar_Hacia_Arriba_Layout.png", 
                            "Thumb_Down":"Imagenes\GestosEmojisMinijuego\PulgarHaciaAbajo.png",
                            "Open_Palm":"Imagenes\GestosEmojisMinijuego\Mano_Levantada_Layout.png",
                            "Closed_Fist":"Imagenes\GestosEmojisMinijuego\ManoCerrada.png"}
            
            imagenSuperpuestaPath = random.choice(list(listaGestos.values()))
            

            





            # #variable acumulativa para los indeces de la lista self.listaEsquinas
            # self.inidiceListaEsquinas = 0

            # #Lista con todas las esquinas de la pantalla
            # self.listaEsquinas = ["esq1","esq2","esq3","esq4"]
            
            # #Cuando se presiona la tecla los cuadros de las esquinas desaparecen
            # self.congelaEsquina1Comparacion = self.congelaEsquina2Comparacion = self.congelaEsquina3Comparacion = self.congelaEsquina4Comparacion = None

            # #lista de las esquinas a activarse en orden aleatorio
            # random.shuffle(self.listaEsquinas)

            # # Cuenta regresiva del 3 al 1
            # i = int
            # for i in range(3, 0, -1):
            #     self.cuenta3Seg = str(i)
            #     time.sleep(1)
            # self.cuenta3Seg = ""
            # self.controladorIniciar_Detener = True

            # #manda las variables para que se pongan en pantalla los cuadros de las esquinas con 1 seg de timing
            # for j in self.listaEsquinas:
            #     self.activadorEsquina = j
            #     time.sleep(1)
            # self.activadorEsquina = ""
            # self.congelaEsquina1 = self.congelaEsquina2 = self.congelaEsquina3 = self.congelaEsquina4 = False


    def finalizar_Minijuego(self, key):
        if key == keyboard.KeyCode.from_char('f'):
            self.rompeCiclo = False

            #Cuando se presiona la tecla los cuadros de las esquinas desaparecen
            self.congelaEsquina1Comparacion = self.congelaEsquina2Comparacion = self.congelaEsquina3Comparacion = self.congelaEsquina4Comparacion = None

        

    def funcion_Mediapipe(self):
        global gestos, puntoYDerecha, puntoYIzquierda, manoDerechaCerrada, manoIzquierdaCerrada

        #Variable de gestos
        global imagenSuperpuestaPath

        #Se crea la ventana
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        
        # Crea una ventana con un nombre específico
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        # Establece la propiedad de la ventana en pantalla completa
        cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        #Inicializador del detector de gestos
        options = GestureRecognizerOptions(
            base_options,
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=1,
            result_callback=print_result)
        with GestureRecognizer.create_from_options(options) as recognizer:
            
            frame_timestamp_ms = 0
            while True:
                ret, frame = cap.read()
                if ret == False:
                    break
                height, width, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                #Imagen Superpuesta (directorio)
                imagen_superpuesta = cv2.imread(imagenSuperpuestaPath)

                # Asegura que la imagen superpuesta tenga el mismo tamaño que el framei
                try:
                    imagen_superpuesta = cv2.resize(imagen_superpuesta, (frame.shape[1], frame.shape[0]))
                except cv2.error as e:
                    print("Error al redimensionar la imagen: ", e)

                

                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

                #Reconocedor de gestos para el live stream
                recognizer.recognize_async(mp_image, frame_timestamp_ms)
                frame_timestamp_ms += 1
                
                #Invierte la imagen
                frame = cv2.flip(frame, 1)
                
                #Texto en pantalla de manos cerradas
                if str(gestos) == "Closed_Fist":
                    cv2.putText(frame, "Mano izquierda cerrada", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if str(gestos) == "Closed_Fist":
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

                
                if self.rompeCiclo == True:
                    break

                # Combinar el frame y la imagen superpuesta
                alpha = 0.0  # Opacidad 0 maximo 1 minimo
                beta = 1 - alpha  # Peso del frame original
                frame = cv2.addWeighted(frame, alpha, imagen_superpuesta, beta, 0)

                cv2.imshow("Frame", frame)
        cap.release() #Libera los recursos de cv2.VideoCapture()
        cv2.destroyAllWindows()
        self.funcion_minijuego()
                




#-------------------------------------------------------------------------------------------------------------------------
    def funcion_minijuego(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Crea una ventana con un nombre específico
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

        # Establece la propiedad de la ventana en pantalla completa
        cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        #Estilo de font para la cuenta regresiva7
        font = cv2.FONT_HERSHEY_DUPLEX
        escala = 5
        espesor = 9


        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0,
            smooth_landmarks=True
            ) as pose:

            while True:
                ret, frame = cap.read()
                if ret == False:
                    break
                frame = cv2.flip(frame, 1)
                height, width, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks is not None:
                    mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(128, 0, 250), thickness=2, circle_radius=3),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))
                    

                    #Deteccion de esquinas
                    puntoMuñecaIzquierda = results.pose_landmarks.landmark[20]
                    puntoMuñecaDerecha = results.pose_landmarks.landmark[19]

                    xI = puntoMuñecaIzquierda.x
                    xD = puntoMuñecaDerecha.x

                    yI= puntoMuñecaIzquierda.y
                    yD = puntoMuñecaDerecha.y

                    #Si este if pasa a ser False no se continuaran detectando las esquinas
                    if self.controladorIniciar_Detener == True:
                        #Esquina 1
                        if ((xI <= 0.3 and yI <= 0.3) or (xD <= 0.3 and yD <= 0.3)) and self.congelaEsquina1Comparacion == None:
                            self.variableComparar = "esq1"
                            if self.listaEsquinas[self.inidiceListaEsquinas] == self.variableComparar:
                                self.inidiceListaEsquinas += 1
                                self.congelaEsquina1Comparacion = True

                            elif self.listaEsquinas[self.inidiceListaEsquinas] != self.variableComparar:
                                self.congelaEsquina1Comparacion = False
                    

                        #Esquina 2
                        if ((xI >= 0.7 and yI <= 0.3) or (xD >= 0.7 and yD <= 0.3)) and self.congelaEsquina2Comparacion == None:
                            self.variableComparar = "esq2"
                            if self.listaEsquinas[self.inidiceListaEsquinas] == self.variableComparar:
                                self.inidiceListaEsquinas += 1
                                self.congelaEsquina2Comparacion = True  

                            elif self.listaEsquinas[self.inidiceListaEsquinas] != self.variableComparar:
                                self.congelaEsquina2Comparacion = False
                        

                        #Esquina 3
                        if ((xI <= 0.3 and yI >= 0.7) or (xD <= 0.3 and yD >= 0.7)) and self.congelaEsquina3Comparacion == None:
                            self.variableComparar = "esq3"
                            if self.listaEsquinas[self.inidiceListaEsquinas] == self.variableComparar:
                                self.inidiceListaEsquinas += 1
                                self.congelaEsquina3Comparacion = True

                            elif self.listaEsquinas[self.inidiceListaEsquinas] != self.variableComparar:
                                self.congelaEsquina3Comparacion = False
                        

                        #Esquina 4
                        if ((xI >= 0.7 and yI >= 0.7) or (xD >= 0.7 and yD >= 0.7)) and self.congelaEsquina4Comparacion == None:
                            self.variableComparar = "esq4"
                            if self.listaEsquinas[self.inidiceListaEsquinas] == self.variableComparar:
                                self.inidiceListaEsquinas += 1
                                self.congelaEsquina4Comparacion = True

                            elif self.listaEsquinas[self.inidiceListaEsquinas] != self.variableComparar:
                                self.congelaEsquina4Comparacion = False
                    

                    cv2.putText(frame, f"Punto x: {str(xD)}", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, f"Punto y: {str(yD)}", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)



                #Pertenece a la esquina 1 (Coloca los cuadros verde y rojo respectivamente)
                if self.congelaEsquina1Comparacion == True:
                    cv2.rectangle(frame, (0, 0), (200, 200), (99, 191, 0), -1)
                    

                elif self.congelaEsquina1Comparacion == False:
                    cv2.rectangle(frame, (0, 0), (200, 200), (49, 49, 255), -1)
                    self.controladorIniciar_Detener = False


                #Pertenece a la esquina 2 (Coloca los cuadros verde y rojo respectivamente)
                if self.congelaEsquina2Comparacion == True:
                    cv2.rectangle(frame, (width-200, 0), (width, 200), (99, 191, 0), -1)
                    

                elif self.congelaEsquina2Comparacion == False:
                    cv2.rectangle(frame, (width-200, 0), (width, 200), (49, 49, 255), -1)
                    self.controladorIniciar_Detener = False                

                #Pertenece a la esquina 3 (Coloca los cuadros verde y rojo respectivamente)
                if self.congelaEsquina3Comparacion == True:
                    cv2.rectangle(frame, (0, height-200), (200, height), (99, 191, 0), -1)
                    

                elif self.congelaEsquina3Comparacion == False:
                    cv2.rectangle(frame, (0, height-200), (200, height), (49, 49, 255), -1)
                    self.controladorIniciar_Detener = False
                

                #Pertenece a la esquina 4 (Coloca los cuadros verde y rojo respectivamente)
                if self.congelaEsquina4Comparacion == True:
                    cv2.rectangle(frame, (width-200, height-200), (width, height), (99, 191, 0), -1)
                    

                elif self.congelaEsquina4Comparacion == False:
                    cv2.rectangle(frame, (width-200, height-200), (width, height), (49, 49, 255), -1)
                    self.controladorIniciar_Detener = False
                    
                






                #Pone la cuenta regresiva en el centro de la pantalla
                texto = f"{self.cuenta3Seg}"

                # Obtener el tamaño del texto
                tamano_texto, _ = cv2.getTextSize(texto, font, escala, espesor)

                # Obtener las dimensiones de la imagen/frame
                alto_frame, ancho_frame, _ = frame.shape

                # Calcular las coordenadas del texto para que esté centrado
                x = int((ancho_frame - tamano_texto[0]) / 2)
                y = int((alto_frame + tamano_texto[1]) / 2)

                # Dibujar el texto centrado en el frame
                cv2.putText(frame, texto, (x, y), font, escala, (255, 255, 255), espesor)





                #Muestra en pantalla las esquinas a memorizar
                if self.activadorEsquina == "esq1" or self.congelaEsquina1 == True:
                    cv2.rectangle(frame, (0, 0), (200, 200), (255, 158, 72), -1)  # Esquina superior izquierda
                    self.congelaEsquina1 = True
                
                if self.activadorEsquina == "esq2" or self.congelaEsquina2 == True:
                    cv2.rectangle(frame, (width-200, 0), (width, 200), (255, 158, 72), -1)  # Esquina superior derecha
                    self.congelaEsquina2 = True

                if self.activadorEsquina == "esq3" or self.congelaEsquina3 == True:
                    cv2.rectangle(frame, (0, height-200), (200, height), (255, 158, 72), -1)  # Esquina inferior izquierda
                    self.congelaEsquina3 = True

                if self.activadorEsquina == "esq4" or self.congelaEsquina4 == True:
                    cv2.rectangle(frame, (width-200, height-200), (width, height), (255, 158, 72), -1)  # Esquina inferior derecha
                    self.congelaEsquina4 = True


                
                cv2.imshow("Frame", frame)  
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                if self.rompeCiclo == False:
                    break
                
        cap.release() #Libera los recursos de cv2.VideoCapture()
        cv2.destroyAllWindows()
        self.funcion_Mediapipe()
#-------------------------------------------------------------------------------------------------------------------------


#Se ejecuta si el archivo se ejecuta directamente y no se importa como un modulo  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())