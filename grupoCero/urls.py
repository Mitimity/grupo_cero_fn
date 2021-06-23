from django.contrib import admin
from django.urls import path, include
from .views import index,consulta,crear_usuario,inicio_sesion,contacto,cerrar_sesion,ingresar_obra_adm,eliminar_obra,modificar_obra,modificacion,consultaArtista,filtro_tec,buscar_obra,buscar_autor,mi_perfil,mi_perfil_mod,insertar_gal,guardar_token,consumir_api

urlpatterns = [
    path('',index,name='IND'),
    path('filtro_tec/',filtro_tec,name='FTEC'),
    path('buscar_obra/',buscar_obra,name='FOB'),
    path('buscar_autor/',buscar_autor,name='FAU'),
    path('consulta/<id>/',consulta,name='CONS'),
    path('crear_usuario/',crear_usuario,name='CRE'),
    path('inicio_sesion/',inicio_sesion,name='INI'),
    path('contacto/',contacto,name='CONT'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRAR'),
    path('ingresar_obra_adm/',ingresar_obra_adm,name='ADM'),
    path('eliminar_obra/<id>/',eliminar_obra,name='ELIM'),
    path('modificar_obra/<id>/',modificar_obra,name='MODIM'),
    path('modificacion/',modificacion,name='MOD'),
    path('consulta_autor/<id>/',consultaArtista,name='CONSAUT'),
    path('mi_perfil/',mi_perfil,name='PERFIL'),
    path('mi_perfil_mod/',mi_perfil_mod,name='MODPER'),
    path('insertar_gal/',insertar_gal,name='INSGAL'),
    path('guardar-token/',guardar_token,name='GUARDART'),
    path('consumir_api/',consumir_api,name='API')
]