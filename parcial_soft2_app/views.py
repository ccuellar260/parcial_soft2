# parcial_soft2_app/views.py

from django.http import HttpResponse
from django.shortcuts import render



def saludo(request):
    return HttpResponse("¡Hola! xd xdLas dependencias xd xdde OpenCV y face_recognition están funcionando correctamente.")

def video_stream(request):
    return render(request, 'video_stream.html')

def dashboard(request):
    # return HttpResponse("¡Hola! Las dependencias xd xdde OpenCV y face_recognition están funcionando correctamente.")
    return render(request, 'dashboard.html')
