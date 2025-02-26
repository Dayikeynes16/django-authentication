from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from server.models import User, Role, UserProfile
from server.serializers import UserSerializer, roleSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

class SaveRolesView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        validate = roleSerializer(data = request.data)
        if validate.is_valid():
            validate.save()
            return Response(validate.data)
        else:
            return Response(validate.errors, status = status.HTTP_400_BAD_REQUEST)

class SaveUserView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        validate = UserSerializer(data = request.data)
        if validate.is_valid():
            validate.save()
            return Response(validate.data)
        else:
            return Response(validate.errors, status = status.HTTP_400_BAD_REQUEST)

class SaveUserProfileView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        validate = UserProfileSerializer(data = request.data)
        if validate.is_valid():
            validate.create()
            return Response(validate.data)
        
        else:
            return Response(validate.errors, status = status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username = username, password = password)
        
        if user:
            token, created = Token.objects.get_or_create(user = user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Credenciales inválidas'}, status = status.HTTP_400_BAD_REQUEST)
        

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)

class UpdateUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = get_object_or_404(User, pk = pk)
        validate = UserSerializer(user, data = request.data)
        if validate.is_valid():
            validate.save()
            if request.data.get('password'):
                user.set_password(request.data['password'])
                user.save()
            return Response(validate.data)
        else:
            return Response(validate.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk = pk)
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)