from django.shortcuts import render
    #dispone de paginas prediseñadas
from rest_framework import generics
    #indica el model y campo seria..
from .serializers import ObrasSerializer,TecnicaSerializer
    #datos a mostrar
from grupoCero.models import Obra, Tecnica

# Create your views here.

class ObraViewSet(generics.ListAPIView):
    #mostrar
    queryset = Obra.objects.all()
    #como
    serializer_class = ObrasSerializer

class TecnicaViewSet(generics.ListAPIView):
    queryset = Tecnica.objects.all()
    serializer_class = TecnicaSerializer

class BuscarObraViewSet(generics.ListAPIView):
    serializer_class = ObrasSerializer
    def get_queryset(self):
        nom = self.kwargs['nombre']
        return Obra.objects.filter(nombreObra=nom)