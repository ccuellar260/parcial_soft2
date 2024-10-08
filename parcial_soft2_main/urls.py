"""
URL configuration for parcial_soft2_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from parcial_soft2_app import views  # Importa directamente la vista
#importra controllador 
from parcial_soft2_app.controllers import FaceIdController
from parcial_soft2_app.controllers import FaceIdPesado
from parcial_soft2_app.controllers import DarioController
from parcial_soft2_app.controllers import YoloController
from parcial_soft2_app.controllers import TensorflowController


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('saludo/', views.saludo, name='saludo'),  # Ruta para la vista saludo
    path('video_face_id/', views.video_stream, name='video_face_id'),  # Nueva ruta para la transmisión de video
    path('video_objetos/', views.video_objetos, name='video_objetos'),  # Nueva ruta para la transmisión de video
    path('', views.dashboard, name='dashboard'),  # Ruta para la página HTML
    path('verificacion/', DarioController.verificacion, name='verificacion'),  # Ruta para la página HTML

   #metodo para la transmision de video
    # path('video_feed/', views.video_feed, name='video_feed'),  # Nueva ruta para la transmisión de video
    path('video_feed/',FaceIdController.video_feed , name='video_feed'),  # Nueva ruta para la transmisión de video
    path('video_yolo/', YoloController.video_feed, name='video_yolo'),
    path('video_tensorflow/', TensorflowController.video_feed, name='video_tensorflow'),  #
   
]