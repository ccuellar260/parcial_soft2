import cv2
import face_recognition
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.shortcuts import render


# AQUI SE CREAN LAS VISTAS DE LA APLICACION
def show_camara_view(request):
    return render(request, 'show_camara.html')



def get_camera_frame():
    
    video_capture = cv2.VideoCapture(0)
    while True:
        # Captura el fotograma desde la cámara
        ret, frame = video_capture.read()

        # Verifica si la captura fue exitosa
        if not ret:
            continue

        # Convertir la imagen capturada de BGR a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Buscar los rostros en el fotograma
        face_locations = face_recognition.face_locations(rgb_frame)

        # Dibujar un rectángulo alrededor de los rostros
        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Codificar el fotograma en JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        # Devolver el fotograma
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Vista para mostrar el reconocimiento facial en tiempo real
def face_recognition_view(request):
    return StreamingHttpResponse(get_camera_frame(), content_type='multipart/x-mixed-replace; boundary=frame')
