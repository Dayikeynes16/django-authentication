from django.contrib.auth.models import AbstractUser
from django.db import models

class Type_person(models.Model):
    rol = models.CharField(max_length=15)
    
    def __str__(self):
        return self.rol 

class CustomUser(AbstractUser):
    SEXO_CHOICES = [
        (1, 'Hombre'),
        (2, 'Mujer'),
    ]
    

    fecha_nacimiento = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Fecha de nacimiento"
    )
    
    sexo = models.IntegerField(
        choices=SEXO_CHOICES,
        null=True,
        blank=True,
        verbose_name="Sexo"
    )

    apellido_paterno = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Apellido Paterno"
    )

    apellido_materno = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Apellido Materno"
    )

    telefono = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Teléfono"
    )
    
    rfc = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        verbose_name="RFC"
    )

    type = models.ForeignKey(
        Type_person,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    curp = models.CharField(
        max_length=18,
        unique=True,
        null=True,
        blank=True,
        verbose_name="CURP"
    )
       
    nombre = models.CharField(
        max_length=50,  
        null=False,
        blank=False,
        verbose_name="Nombre"
    )

    def __str__(self):
        return f"{self.nombre} {self.username} {self.apellido_paterno} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"