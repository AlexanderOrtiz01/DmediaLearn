import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import cv2


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

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)




# Crea una ventana con un nombre específico
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Establece la propiedad de la ventana en pantalla completa
cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)






# Create a gesture recognizer instance with the live stream mode:
gestos = None
lateralidad = None
yI = None
xI = None


def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):

  #print(type(result.gestures))
  global gestos, lateralidad, yI, xI
  if (len(result.gestures) != 0):
    gestos = str(result.gestures[0][0].category_name)
    lateralidad = result.handedness[0][0].category_name

    puntoMuñecaIzquierda = result.hand_landmarks[0][0]
    yI= puntoMuñecaIzquierda.y

    puntoMuñecaIzquierda = result.hand_landmarks[0][0]
    xI= puntoMuñecaIzquierda.x

    print(xI)
  else:
    gestos = None
    lateralidad = None
    print("Vacio")

  



imagen_superpuesta = cv2.imread('Imagenes\GestosEmojisMinijuego\Mano_Levantada_Layout.png')





options = GestureRecognizerOptions(
    base_options,
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=print_result)
with GestureRecognizer.create_from_options(options) as recognizer:
  # The detector is initialized. Use it here.

  frame_timestamp_ms = 0
  while True:
    ret, frame = cap.read()
    if ret == False:
      break



    # Asegurarse de que la imagen superpuesta tenga el mismo tamaño que el frame
    imagen_superpuesta = cv2.resize(imagen_superpuesta, (frame.shape[1], frame.shape[0]))
    




    height, width, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

  

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    #Reconocedor de gestos para el live stream
    recognizer.recognize_async(mp_image, frame_timestamp_ms)
    frame_timestamp_ms += 1
    
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, str(xI),(100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)





     # Combinar el frame y la imagen superpuesta
    alpha = 0.0  # Peso de la imagen superpuesta
    beta = 1 - alpha  # Peso del frame original
    frame = cv2.addWeighted(frame, alpha, imagen_superpuesta, beta, 0)





    

    #cv2.putText(frame, str(gestos),(100, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()

