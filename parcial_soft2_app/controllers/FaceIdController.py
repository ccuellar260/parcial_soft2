from django.http import StreamingHttpResponse

import cv2
import face_recognition



def gen_camera():
    # Iniciar la cámara
    video_capture = cv2.VideoCapture(1)
    process_this_frame = True  # Variable para controlar cuándo procesar un cuadro

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Procesar solo 1 de cada 2 cuadros para mejorar el rendimiento
        if process_this_frame:
            # Redimensionar el cuadro para acelerar el procesamiento
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            # Convertir el cuadro reducido de BGR a RGB
            rgb_small_frame = small_frame[:, :, ::-1]

            # Detectar los rostros usando el modelo HOG (más rápido que CNN)
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")

        # Alternar el procesamiento de cuadros
        process_this_frame = not process_this_frame

        # Dibujar cuadros alrededor de los rostros detectados en el cuadro original
        for (top, right, bottom, left) in face_locations:
            # Escalar nuevamente las coordenadas a la resolución original
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Convertir el frame a JPEG y devolverlo como streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    video_capture.release()

def video_feed(request):
    return StreamingHttpResponse(gen_camera(), content_type='multipart/x-mixed-replace; boundary=frame')