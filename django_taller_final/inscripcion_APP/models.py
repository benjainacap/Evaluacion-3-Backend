from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

ESTADO = (
    ('Reservado','RESERVADO'),
    ('Completada', 'COMPLETADA'),
    ('Anulada','ANULADA'),
    ('No Asisten','NO ASISTEN'),
)
class Inscripcion(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    fecha = models.DateField()
    institucion = models.CharField(max_length=50)
    hora = models.TimeField(auto_now=False)
    estado = models.CharField(max_length=10, choices=ESTADO, default='Reservado')
    observaciones = models.CharField(max_length=100, blank=True)

class Institucion(models.Model):
    nombre = models.CharField(max_length=50)
