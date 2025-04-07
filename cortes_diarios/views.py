import datetime
import decimal
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CortesDiarios
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import CortesDiariosSerializer
from django.db.models import Avg

# Renderizar una plantilla HTML (si la necesitas)
def DS(request):
    return render(request, 'cortes/index.html')

class CortesDiariosView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        fecha_actual = now().date()

        serializer = CortesDiariosSerializer(data=request.data)

        if serializer.is_valid():

            instance, created = CortesDiarios.objects.get_or_create(
            fecha=fecha_actual,
            defaults={  
                "efectivo": decimal.Decimal(request.data.get("efectivo", 0)),
                "tarjeta": decimal.Decimal(request.data.get("tarjeta", 0)),
                "transferencia": decimal.Decimal(request.data.get("transferencia", 0)),
                "total": decimal.Decimal(request.data.get("efectivo", 0)) + 
                         decimal.Decimal(request.data.get("tarjeta", 0)) + 
                         decimal.Decimal(request.data.get("transferencia", 0))
            }
        )

            if not created:

                instance.efectivo = decimal.Decimal(request.data.get("efectivo", instance.efectivo))
                instance.tarjeta = decimal.Decimal(request.data.get("tarjeta", instance.tarjeta))
                instance.transferencia = decimal.Decimal(request.data.get("transferencia", instance.transferencia))
                instance.total = instance.efectivo + instance.tarjeta + instance.transferencia
                instance.save()

            return Response(CortesDiariosSerializer(instance).data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

        
    def get(self, request):
        cortes = CortesDiarios.objects.filter(fecha=now().date())
        
        if not cortes.exists():
            corte = CortesDiarios.objects.create(
                fecha=now().date(),
                total=0,
                efectivo=0,
                tarjeta=0,
                transferencia=0
            )
            serializer = CortesDiariosSerializer(corte)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Obtener solo el primer registro del día
        corte = cortes.first()  # Obtiene solo el primer objeto
        serializer = CortesDiariosSerializer(corte)  # Sin many=True porque es un solo objeto
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        cortes = CortesDiarios.objects.all()
        cortes.delete()
        return Response(status=status.HTTP_200_OK)


class historial(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        historial = CortesDiarios.objects.order_by('-fecha').all()
        promedio_global = CortesDiarios.objects.aggregate(promedio_global=Avg('total'))['promedio_global'] or 0
        siete_dias_atras = now() - datetime.timedelta(days=7)
        promedio_7_dias = CortesDiarios.objects.filter(fecha__gte=siete_dias_atras).aggregate(promedio_7_dias=Avg('total'))['promedio_7_dias'] or 0

        serializer = CortesDiariosSerializer(historial, many=True)
        return Response(
           {
            'historial': serializer.data,
            'promedio_global': round(promedio_global, 2),
            'promedio_7_dias': round(promedio_7_dias, 2)
        }, status=status.HTTP_200_OK)


        

