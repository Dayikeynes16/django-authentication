import decimal
from rest_framework import serializers
from .models import CortesDiarios
from django.utils.timezone import now, datetime

class CortesDiariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CortesDiarios
        fields = '__all__'

    id = serializers.IntegerField(read_only=True)
    fecha = serializers.DateField(read_only=True)
    efectivo = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    tarjeta = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    transferencia = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2, )


    # def create(self, validated_data):
    #     fecha = now().date()
    #     if CortesDiarios.objects.filter(fecha=fecha).exists():
    #         raise serializers.ValidationError({"fecha": "Ya existe un corte de caja para esta fecha."})
    #     instance = CortesDiarios.objects.create(
    #         fecha=now().date(),
    #         efectivo=decimal.Decimal(validated_data.get('efectivo', 0)),  # Agregamos un valor por defecto en caso de None
    #         tarjeta=decimal.Decimal(validated_data.get('tarjeta', 0)),
    #         transferencia=decimal.Decimal(validated_data.get('transferencia', 0)),
    #         total=decimal.Decimal(validated_data.get('efectivo', 0)) + 
    #               decimal.Decimal(validated_data.get('tarjeta', 0)) + 
    #               decimal.Decimal(validated_data.get('transferencia', 0)),
    #         gastos=decimal.Decimal(0)
    #     )
    #     return instance  # Retornamos la instancia creada correctamente
