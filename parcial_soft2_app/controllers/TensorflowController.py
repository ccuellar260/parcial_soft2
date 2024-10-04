import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from django.http import StreamingHttpResponse
import torch

# Cargar el modelo de detección de peleas preentrenado
model_url = "https://tfhub.dev/deepmind/i3d-kinetics-400/1"
violence_model = hub.load(model_url)
# Cargar el modelo YOLOv5
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def gen_camera():
    # Iniciar la cámara
    video_capture = cv2.VideoCapture(1)
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Redimensionar el frame para mejorar el rendimiento
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convertir de BGR a RGB
        rgb_small_frame = small_frame[:, :, ::-1]

        # Inicializa la variable 'pelea' en False por defecto
        pelea = False

        # Detección de pelea (asegúrate de que esta función siempre retorne True o False)
        pelea = is_fight_detected(rgb_small_frame)  # Verifica si hay pelea en el frame

        # Detectar personas con YOLO o algún otro modelo
        persons_detected = detect_persons(frame)  # Función para detectar personas

        # Dibujar cuadros alrededor de las personas detectadas
        for (x, y, w, h) in persons_detected:
            color = (0, 0, 255) if pelea else (0, 255, 0)  # Rojo si hay pelea, Verde si no

            # Dibujar el cuadro alrededor de la persona detectada
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Convertir el frame a JPEG y devolverlo como streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    video_capture.release()


# Función para detectar pelea usando el modelo TensorFlow
def is_fight_detected(frames):
    frames = np.expand_dims(frames, axis=0)  # Añadir batch dimension
    predictions = violence_model.signatures['default'](tf.constant(frames, dtype=tf.float32))
    return predictions['default'][0] > 0.5  # Ajustar el umbral según el modelo

# Función para detectar personas (puedes usar YOLO para esto)
def detect_persons(frame):
    # Utilizar el modelo YOLO para hacer predicciones en el frame
    results = yolo_model(frame)
    
    # Filtrar resultados solo para detecciones de personas (clase 0 en COCO)
    persons_detected = []
    for result in results.xyxy[0]:  # xyxy son las coordenadas de los cuadros detectados
        class_id = int(result[5])  # Clase detectada
        if class_id == 0:  # Clase 0 es 'persona' en el conjunto de datos COCO
            x1, y1, x2, y2 = int(result[0]), int(result[1]), int(result[2]), int(result[3])
            persons_detected.append((x1, y1, x2 - x1, y2 - y1))  # Devuelve las coordenadas en forma (x, y, w, h)
    
    return persons_detected  # Lista de coordenadas de las personas detectadas

# Vista para el streaming de video
def video_feed(request):
    return StreamingHttpResponse(gen_camera(), content_type='multipart/x-mixed-replace; boundary=frame')
