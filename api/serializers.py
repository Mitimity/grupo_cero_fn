from rest_framework import serializers
from grupoCero.models import Obra,Tecnica

#Definir clase con los campos para se
class ObrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = ["nombreObra","imagen","tecnica","valor"]

class TecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnica
        fields = ["nombre_tecnica"]