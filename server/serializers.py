from rest_framework import serializers
from server.models import User, UserProfile, Role

class roleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'permissions']
        extra_kwargs = {
            'name': {'required': True},
            'permissions': {'required': False}
        }

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError({'name': 'El nombre del rol es requerido'})
        
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'address', 'city', 'state', 'additional_info']
        extra_kwargs = {
            'user': {'required': True},
            'address': {'required': False},
            'city': {'required': False},
            'state': {'required': False},
            'additional_info': {'required': False}
        }
    
    def validate(self, data):
        if not data.get('user'):
            raise serializers.ValidationError({'user': 'El usuario es requerido'})
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'full_name', 'phone', 'employee_id', 'rfc', 'curp', 'hire_date', 'username', 'password']
        extra_kwargs = {
            'role': {'required': True},
            'full_name': {'required': True},
            'phone': {'required': False},
            'employee_id': {'required': False},
            'rfc': {'required': False},
            'curp': {'required': False},
            'hire_date': {'required': False},
            'username': {'required': True},
            'password': {'required': True}
        }           
    def validate(self, data):
        if not data.get('role'):
            raise serializers.ValidationError({'role': 'El rol es requerido'})
        
        return data
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



    


