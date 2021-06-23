from django.contrib import admin
#importar modelos
from .models import Tecnica, Obra,Autor,Comentario,Galeria

# Register your models here.
admin.site.register(Tecnica)
admin.site.register(Obra)
admin.site.register(Autor)
admin.site.register(Comentario)
admin.site.register(Galeria)