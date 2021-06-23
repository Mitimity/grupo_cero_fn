from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Tecnica(models.Model):
    nombre_tecnica = models.CharField(primary_key=True, max_length=60)
    
    def __str__(self):
        return self.nombre_tecnica

class Autor(models.Model):
    id_autor = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='usuarios',default='usuarios/usuario.png')
    presentacion = models.CharField(max_length=500, default='Artista sin presentación.')
    
    def __str__(self):
        return str(self.usuario)
    
class Obra(models.Model):
    id_obra = models.AutoField(primary_key=True)
    nombreObra = models.CharField(max_length=60)
    imagen = models.ImageField(upload_to='fotos',default='fotos/default.png')
    descripcion = models.CharField(max_length=500, default='Esta obra no posee una descripción disponible.')
    historia = models.CharField(max_length=500, default='Esta obra no posee una historia disponible.')
    valor = models.CharField(default='0', max_length=60)
    publicar = models.BooleanField(default=False)
    comentario = models.TextField(default='--')
    tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreObra+" ~Publicado: "+str(self.publicar)+" - "+self.comentario
    
class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    correo = models.CharField(max_length=150)
    comentario = models.CharField(max_length=500)

    def __str__(self):
        return self.correo

class Galeria(models.Model):
    id_imag = models.AutoField(primary_key=True)
    imagen = models.ImageField(upload_to='galeria')
    obra_orig = models.ForeignKey(Obra, on_delete=models.CASCADE)
    def __str__(self):
        return "Numero: "+str(self.id_imag)
