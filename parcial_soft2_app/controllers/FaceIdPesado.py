# parcial_soft2_app/views.py

from django.http import StreamingHttpResponse
from django.shortcuts import render
import cv2
import face_recognition

def gen_camera():
    # Iniciar la cámara
    video_capture = cv2.VideoCapture(1)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convertir el cuadro de BGR a RGB
        rgb_frame = frame[:, :, ::-1]

        # Detectar los rostros
        face_locations = face_recognition.face_locations(rgb_frame)

        # Dibujar cuadros alrededor de los rostros detectados
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Convertir el frame a JPEG y devolverlo como streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    video_capture.release()

def video_feed(request):
    return StreamingHttpResponse(gen_camera(), content_type='multipart/x-mixed-replace; boundary=frame')
