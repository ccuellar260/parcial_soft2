from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del usuario (o puedes usar algún identificador)
    veces_detectado = models.IntegerField(default=0)  # Número de veces que ha sido detectado
    encoding = models.BinaryField()  # Almacenar el encoding facial (representación numérica)
    fecha_ultimo_registro = models.DateTimeField(auto_now=True)  # Fecha de la última detección

    class Meta:
        db_table = 'Persona'  # Nombre personalizado de la tabla