from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from server.models import CustomUser, Type_person
from server.serializers import UserSerializer, TypePersonSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password']) 
        user.type_id = 1 
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Se requiere 'username' y 'password'"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({
        "token": token.key,
        "usuario": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)  
    return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['PUT', 'PATCH'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def update_user(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)

#     if 'role' in request.data and request.user.id != user.id:
#         return Response({"error": "No puedes cambiar el rol de otro usuario"}, status=status.HTTP_403_FORBIDDEN)

#     if 'username' in request.data and request.user.id != user.id:
#         return Response({"error": "No puedes cambiar el username de otro usuario"}, status=status.HTTP_403_FORBIDDEN)

#     serializer = UserSerializer(instance=user, data=request.data, partial=True)  

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SaveRolesView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        validate = TypePersonSerializer(data = request.data)
        if validate.is_valid():
            # return Response(validate)
            validate()
            

            return Response({"rol": validate.data})
        else:
            return Response(validate.errors, status = status.HTTP_400_BAD_REQUEST)
            
       