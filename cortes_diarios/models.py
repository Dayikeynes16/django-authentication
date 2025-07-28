from django.db import models



# Create your models here.
class CortesDiarios(models.Model):
    fecha = models.DateField(unique=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tarjeta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.fecha + self.total + self.efectivo + self.tarjeta + self.transferencia 


class Efectivo(models.Model):
    fecha = models.DateField()
    efectivo = models.DecimalField(max_digits=10, decimal_places=2)
    comentarios = models.CharField(max_length=200)
    def __str__(self):
        return self.efectivo + self.fecha

