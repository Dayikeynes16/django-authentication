from django.db import models

# Create your models here.
class CortesDiarios(models.Model):
    fecha = models.DateField()
    efectivo = models.DecimalField(max_digits=10, decimal_places=2)
    tarjeta = models.DecimalField(max_digits=10, decimal_places=2)
    transferencia = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    gastos = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.fecha + self.total + self.efectivo + self.tarjeta + self.transferencia + self.gastos

class Efectivo(models.Model):
    fecha = models.DateField()
    efectivo = models.DecimalField(max_digits=10, decimal_places=2)
    comentarios = models.CharField(max_length=200)
    def __str__(self):
        return self.efectivo + self.fecha

class Gastos(models.Model):
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=20)
    comentarios = models.CharField(max_length=200)
    def __str__(self):
        return self.motivo  + self.total, self.fecha