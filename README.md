# Procesamiento de Video en Tiempo Real usando K-NN

Este proyecto implementa un sistema de procesamiento de video en tiempo real utilizando el algoritmo K-NN para clasificar píxeles de una cámara IP en categorías como "tierra" y "agua".

## Descripción

El objetivo principal del proyecto es clasificar los píxeles capturados por una cámara en tiempo real utilizando datos de entrenamiento previamente almacenados. El sistema se conecta a una cámara IP, captura el video, extrae las bandas RGB de cada frame, y utiliza el algoritmo K-NN para clasificar los píxeles.

## Requisitos

- Python 3.x
- OpenCV
- NumPy
- Una cámara IP

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tuusuario/procesamiento-video-knn.git
    ```
2. Instala las dependencias:
    ```bash
    pip install numpy opencv-python
    ```
3. Asegúrate de tener los datos de entrenamiento (`rsTrain.dat`) en el mismo directorio.
