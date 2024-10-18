import cv2
import numpy as np
import math
import time
import signal
import sys

# Función para manejar señales del sistema (Ctrl + C)
def signal_handler(sig, frame):
    print('Interrupción detectada, liberando recursos...')
    cap.release()  # Liberar la cámara
    cv2.destroyAllWindows()  # Cerrar las ventanas de OpenCV
    sys.exit(0)

# Registrar la señal Ctrl + C
signal.signal(signal.SIGINT, signal_handler)

def definir(resultados):
    tierra = 0
    agua = 0
    for i in resultados:
        if i[1] == 0:
            tierra += 1
        elif i[1] == 1:
            agua += 1
    if tierra < agua:
        return 1
    return 0

def distancia(dist1, dist2):
    suma = 0
    for i in range(3):  # RGB
        suma += (dist1[i] - dist2[i]) ** 2
    return math.sqrt(suma)

# Intentar cargar los datos de entrenamiento
try:
    datos = np.loadtxt('rsTrain.dat')
except Exception as e:
    print(f"Error al cargar los datos de entrenamiento: {e}")
    sys.exit(1)

# Reintentar la conexión a la cámara si falla
cap = None
while cap is None or not cap.isOpened():
    try:
        # Reemplaza esta URL con la URL de tu cámara IP
        # Ejemplo: rtsp://usuario:contraseña@direccion_ip:puerto/cam
        cap = cv2.VideoCapture('rtsp://usuario:contraseña@direccion_ip:puerto/cam')
        if not cap.isOpened():
            raise ValueError("No se pudo conectar a la cámara")
        print("Cámara conectada con éxito")
    except Exception as e:
        print(f"Error al conectar a la cámara: {e}")
        time.sleep(5)  # Esperar 5 segundos antes de reintentar

while True:
    try:
        # Leer el frame del video
        ret, frame = cap.read()
        if not ret:
            raise ValueError("No se pudo capturar el frame")
        
        # Extraer las bandas (R, G, B)
        banda1 = frame[:, :, 0]  # Canal R
        banda2 = frame[:, :, 1]  # Canal G
        banda3 = frame[:, :, 2]  # Canal B

        # Preparar los datos de las bandas
        bandas = []
        for linea in range(frame.shape[0]):
            for valor in range(frame.shape[1]):
                bandas.append((banda1[linea][valor], banda2[linea][valor], banda3[linea][valor]))

        # K-NN: Clasificación
        resultados = []
        k = 1
        for banda in bandas:
            vecinos = []
            for dato in datos:
                dist = distancia(banda, dato[:3])  # Solo 3 canales RGB
                vecinos.append((dist, dato[3]))  # La última columna es la clase
            vecinos.sort(key=lambda x: x[0])
            resultados.append(definir(vecinos[:k]))

        # Convertir el resultado en una imagen
        array = np.array(resultados, dtype=np.int8)
        imagen_resultado = array.reshape((frame.shape[0], frame.shape[1]))

        # Mostrar la imagen procesada
        cv2.imshow('Video procesado', imagen_resultado)

        # Salir al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error en el procesamiento del frame: {e}")
        # Otras acciones como reconectar a la cámara o pausar el sistema por un tiempo
        time.sleep(5)

# Liberar la cámara y cerrar las ventanas al final
cap.release()
cv2.destroyAllWindows()
