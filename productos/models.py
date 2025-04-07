from django.db import models

# Create your models here.
class Producto(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateField()
    nombre = models.CharField(max_length=200)
    precio_de_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_produccion = models.DecimalField(max_digits=10, decimal_places=2)
    piezas = models.BooleanField()
    for_public = models.BooleanField()
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre + self.precio_de_venta + self.precio_produccion + self.stock + self.imagen + self.piezas + self.for_public


    
