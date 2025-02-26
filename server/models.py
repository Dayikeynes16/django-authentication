from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50)
    # Aquí puedes agregar permisos específicos si los necesitas
    permissions = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    rfc = models.CharField(max_length=13, unique=True, null=True, blank=True)
    curp = models.CharField(max_length=18, unique=True, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    additional_info = models.JSONField(null=True, blank=True)  # Para información extra flexible

    def __str__(self):
        return f"Perfil de {self.user.full_name}"