from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    password_change_required = models.BooleanField(default=True)

class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField()

class Repuestos(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField()
    
class Trabajo(models.Model):

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]

    CRITICIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Alta', 'Alta'),
        ('Urgente', 'Urgente'),
    ]

    estado = models.CharField(
        max_length=50,
        choices=ESTADO_CHOICES,
        default='Pendiente'
    )

    criticidad = models.CharField(
        max_length=50,
        choices=CRITICIDAD_CHOICES,
        default='Baja'
    )

    descripcion = models.TextField()
    hechos = models.TextField()