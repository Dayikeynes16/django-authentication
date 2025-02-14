from rest_framework import serializers
from server.models import CustomUser  # Asegúrate de importar el modelo correcto

class UserSerializer(serializers.ModelSerializer):
    sexo = serializers.ChoiceField(choices=CustomUser.SEXO_CHOICES, required=False)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)  # Asegurar que solo acepta valores válidos

    class Meta:
        model = CustomUser
        fields = [
            'id', 'nombre', 'username', 'email', 'password', 'fecha_nacimiento', 'sexo',
            'apellido_paterno', 'apellido_materno', 'telefono', 'rfc', 'curp', 'role'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'nombre': {'required': True}, 
            'rfc': {'required': False, 'allow_null': True},
            'curp': {'required': False, 'allow_null': True},
            'telefono': {'required': False, 'allow_null': True},
            'apellido_paterno': {'required': False, 'allow_null': True},
            'apellido_materno': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        """
        Validar que los campos requeridos dependan del rol.
        """
        role = data.get('role', None)

        if not data.get('nombre'):
            raise serializers.ValidationError({'nombre': 'El nombre es obligatorio para todos los usuarios.'})

        if role == 'cliente':
            if not data.get('telefono'):
                raise serializers.ValidationError({'telefono': 'El teléfono es obligatorio para clientes.'})
        
        elif role == 'chofer':
            if not data.get('rfc'):
                raise serializers.ValidationError({'rfc': 'El RFC es obligatorio para choferes.'})
            if not data.get('curp'):
                raise serializers.ValidationError({'curp': 'El CURP es obligatorio para choferes.'})
            if not data.get('apellido_paterno'):
                raise serializers.ValidationError({'apellido_paterno': 'El apellido paterno es obligatorio para choferes.'})
            if not data.get('apellido_materno'):
                raise serializers.ValidationError({'apellido_materno': 'El apellido materno es obligatorio para choferes.'})

        return data

    def create(self, validated_data):
        """
        Crea un usuario con los datos validados, asegurando que la contraseña se guarde correctamente.
        """
        password = validated_data.pop('password', None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)  # Asegura que la contraseña se guarde encriptada
            user.save()
        return user

    def update(self, instance, validated_data):
        """
        Actualiza un usuario existente, asegurando que si se envía una nueva contraseña, se guarde correctamente.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Asigna los valores actualizados

        if password:
            instance.set_password(password)  # Guarda la nueva contraseña encriptada
        instance.save()
        return instance
