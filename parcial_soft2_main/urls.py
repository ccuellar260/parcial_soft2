# from django.contrib import admin
from django.urls import path
from parcial_soft2_app import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('show_camara/1',views.show_camara_view,  name='show_camara' ),
    path('recognition/', views.face_recognition_view, name='face_recognition'),
]
