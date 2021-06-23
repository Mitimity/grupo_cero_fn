# Generated by Django 3.2.4 on 2021-06-23 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id_autor', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(default='usuarios/usuario.png', upload_to='usuarios')),
                ('presentacion', models.CharField(default='Artista sin presentación.', max_length=500)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id_comentario', models.AutoField(primary_key=True, serialize=False)),
                ('correo', models.CharField(max_length=150)),
                ('comentario', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tecnica',
            fields=[
                ('nombre_tecnica', models.CharField(max_length=60, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id_obra', models.AutoField(primary_key=True, serialize=False)),
                ('nombreObra', models.CharField(max_length=60)),
                ('imagen', models.ImageField(default='fotos/default.png', upload_to='fotos')),
                ('descripcion', models.CharField(default='Esta obra no posee una descripción disponible.', max_length=500)),
                ('historia', models.CharField(default='Esta obra no posee una historia disponible.', max_length=500)),
                ('valor', models.CharField(default='0', max_length=60)),
                ('publicar', models.BooleanField(default=False)),
                ('comentario', models.TextField(default='--')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupoCero.autor')),
                ('tecnica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupoCero.tecnica')),
            ],
        ),
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('id_imag', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(upload_to='galeria')),
                ('obra_orig', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grupoCero.obra')),
            ],
        ),
    ]
