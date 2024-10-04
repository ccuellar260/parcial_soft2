import cv2
import torch
from django.http import StreamingHttpResponse
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Cargar el modelo preentrenado YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()  # Colocar el modelo en modo de inferencia

# Función para procesar la cámara
def gen_camera():
    # Iniciar la cámara (cambiar 0 por el ID de la cámara si tienes varias)
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Realizar inferencia con YOLOv5 en el frame capturado
        results = model(frame)

        # Dibujar los cuadros delimitadores en el frame
        for det in results.xyxy[0]:  # xyxy: coordenadas de las cajas delimitadoras
            x1, y1, x2, y2, conf, cls = det
            label = f'{model.names[int(cls)]} {conf:.2f}'

            # Verificar si el objeto detectado es un cuchillo (knife en inglés)
            if 'knife' in label.lower() and conf >= 0.5:
                color = (0, 0, 255)  # Rojo si es un cuchillo
            else:
                color = (0, 255, 0)  # Verde para otros objetos

            # Dibujar el cuadro delimitador
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Convertir el frame a formato JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        # Enviar el frame como un flujo de video
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    video_capture.release()

# Controlador para manejar el video
def video_feed(request):
    return StreamingHttpResponse(gen_camera(), content_type='multipart/x-mixed-replace; boundary=frame')
