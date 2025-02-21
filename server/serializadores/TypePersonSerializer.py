from rest_framework import serializers
from ..models import Type_person

class TypePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_person
        fields = ['id', 'rol']
    
    def validate(self, data):
        return data