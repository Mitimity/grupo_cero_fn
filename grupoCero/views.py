from django.shortcuts import render
# importamos los modelos de tabla de la BDD
from .models import Comentario, Obra, Tecnica, Autor, Galeria

# importar el modelo de tabla User 
from django.contrib.auth.models import User
# importar librerias que permitan la validacion del login
from django.contrib.auth import authenticate,logout,login as login_aut
# importar libreria decoradora que permite evitar el ingreso de usuarios a las paginas web
from django.contrib.auth.decorators import login_required, permission_required

# --------------------------------------PUSH------------------------------------------
import requests

def consumir_api(request):
    response = requests.get("http://127.0.0.1:8000/api/obras/")
    listado_obras = response.json()

    response = requests.get("http://127.0.0.1:8000/api/tecnica/")
    listado_tecnicas = response.json()
    
    if request.POST:
        nombre = request.POST.get("txtNombreObr")
        response = requests.get("http://127.0.0.1:8000/api/buscar_obra/"+nombre+"/")
        listado_obras = response.json()
    
    contexto = {"obras":listado_obras,"tecnicas":listado_tecnicas}

    return render(request,"api.html",contexto)
# ------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
# incorporar las librerias necesarias para trabajar con la carga de adtos
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseBadRequest, response
from django.core import serializers
import json
from fcm_django.models import FCMDevice
# creacion de la vista para el desarrollo del metodo

@csrf_exempt
@require_http_methods(['POST'])
def guardar_token(request):
    body = request.body.decode('utf-8')
    datos_body = json.loads(body)
    token = datos_body['token']
    # preguntar si el token existe
    existe = FCMDevice.objects.filter(registration_id=token,active=True)
    if len(existe)>0:
        return HttpResponseBadRequest(json.dumps({'mensaje','el token existe'}))
    dispositivo = FCMDevice()
    dispositivo.registration_id = token
    dispositivo.active = True
    # solo si el usuario esta registrado antes
    if request.user.is_authenticated:
        dispositivo.user = request.user
    # grabar el dipositivo
    try:
        dispositivo.save()
        return HttpResponse(json.dumps({'mensaje','dispositivo almacenado'}))
    except:
        return HttpResponseBadRequest(json.dumps({'mensaje','no pudo almacenar el token'}))
# ------------------------------------------------------------------------------------


# Create your views here.
def index(request):
    imag = Obra.objects.filter(publicar=True)
    tecnicas = Tecnica.objects.all()
    carrusel = Obra.objects.filter(publicar=True).order_by('nombreObra')[:2]
    aut = Autor.objects.all().order_by('usuario')
    caut = Autor.objects.all().order_by('usuario').count()
    cobr = Obra.objects.filter(publicar=True).count()
    mensaje = "0"
    icono = ""

    contexto = {"obras":imag, "tecnicas":tecnicas,"carru":carrusel,"aut":aut,"caut":caut,"cobr":cobr,"mensaje":mensaje,"icono":icono}
    return render(request,"index.html",contexto)

def filtro_tec(request):
    carrusel = Obra.objects.filter(publicar=True).order_by('nombreObra')[:3]
    obra = Obra.objects.filter(publicar=True)
    tecnicas = Tecnica.objects.all()
    aut = Autor.objects.all().order_by('usuario')
    caut = Autor.objects.all().order_by('usuario').count()
    mensaje = "0"
    icono = ""

    if request.POST:
        tecnica = request.POST.get("cboFiltroTecnica")
        obj_cate = Tecnica.objects.get(nombre_tecnica=tecnica)
        obra = Obra.objects.filter(tecnica=obj_cate).filter(publicar=True)
        cobr = Obra.objects.filter(tecnica=obj_cate).filter(publicar=True).count()

    contexto = {"obras":obra,"tecnicas":tecnicas,"carru":carrusel,"aut":aut,"caut":caut,"cobr":cobr,"mensaje":mensaje,"icono":icono}
    return render(request, "index.html",contexto)   
    
def buscar_obra(request):
    carrusel = Obra.objects.filter(publicar=True).order_by('nombreObra')[:3]
    obra = Obra.objects.filter(publicar=True)
    tecnica = Tecnica.objects.all()
    aut = Autor.objects.all().order_by('usuario')
    caut = Autor.objects.all().order_by('usuario').count()
    mensaje = "0"
    icono = ""

    if request.POST:
        nombre = request.POST.get("txtNombreObr")
        obra = Obra.objects.filter(nombreObra=nombre).filter(publicar=True)
        cobr = Obra.objects.filter(nombreObra=nombre).filter(publicar=True).count()
    contexto = {"obras":obra,"tecnicas":tecnica,"carru":carrusel,"aut":aut,"caut":caut,"cobr":cobr,"mensaje":mensaje,"icono":icono}
    return render(request, "index.html",contexto)   

def buscar_autor(request):
    carrusel = Obra.objects.filter(publicar=True).order_by('nombreObra')[:3]
    obra = Obra.objects.filter(publicar=True)
    tecnica = Tecnica.objects.all()
    aut = Autor.objects.all().order_by('usuario')
    cobr = Obra.objects.filter(publicar=True).count()
    mensaje = "0"
    icono = ""

    if request.POST:
        nombre = request.POST.get("txtNombreAutor")
        obj_autor = User.objects.get(username=nombre)
        aut = Autor.objects.filter(usuario=obj_autor)
        caut = Autor.objects.filter(usuario=obj_autor).count()
    contexto = {"obras":obra,"tecnicas":tecnica,"carru":carrusel,"aut":aut,"caut":caut,"cobr":cobr,"mensaje":mensaje,"icono":icono}
    return render(request, "index.html",contexto)   

def consulta(request,id):
    obr = Obra.objects.get(nombreObra=id)
    gal = Galeria.objects.filter(obra_orig=obr)
    contexto = {"obras":obr,"galeria":gal}
    return render(request,"cons_obr.html",contexto)

def consultaArtista(request,id):
    tecnicas = Tecnica.objects.all()

    artista = Autor.objects.get(id_autor=id)

    obr = Obra.objects.filter(autor=artista).filter(publicar=True)
    coun = Obra.objects.filter(autor=artista).filter(publicar=True).count()

    contexto = {"obras":obr, "tecnicas":tecnicas,"contador":coun,"artista":artista}
    return render(request,"cons_autor.html",contexto)

def contacto(request):
    mensaje = "0"
    icono = ""
    if request.POST:
        corr = request.POST.get("txtCorreo")
        com = request.POST.get("txtComentario")

        try:
            comen = Comentario()
            comen.correo=corr
            comen.comentario=com
            comen.save()
            mensaje = "El mensaje ha sido enviado con éxito."
            icono = "success"
        except:
            mensaje = "El mensaje ha tenido un error en él envió."
            icono = "error"
    contexto = {"mensaje":mensaje,"icono":icono}    
    return render(request,"contacto.html",contexto)

def crear_usuario(request):
    imag = Obra.objects.filter(publicar=True)
    tecnicas = Tecnica.objects.all()
    carrusel = Obra.objects.filter(publicar=True).order_by('nombreObra')[:2]
    aut = Autor.objects.all().order_by('usuario')
    caut = Autor.objects.all().order_by('usuario').count()
    cobr = Obra.objects.filter(publicar=True).count()
    mensaje = "0"
    icono = ""

    if request.POST:
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        nom_usuario = request.POST.get("txtNombreUsuario")
        email = request.POST.get("txtCorreo")
        clave = request.POST.get("txtClave")
        claveConf = request.POST.get("txtClaveConf")
        ima = request.FILES.get("txtImgUsuario")
        pres = request.POST.get("txtPresentacion")

        if clave!=claveConf:
            mensaje = "Ha ocurrido un error, las contraseñas deben ser las mismas."
            icono = "error"
            contexto= {"mensaje":mensaje,"icono":icono}
            return render(request,"crear_usuario.html",contexto)

        try:
            usu = User.objects.get(username=nom_usuario)
            mensaje = "Ha ocurrido un error, por favor revise que los datos sean correctos."
            icono = "error"
            contexto = {"mensaje":mensaje,"icono":icono}
            return render(request,"crear_usuario.html",contexto)

        except:
            #Ingresar datos a usuarios
            usu = User()
            usu.first_name=nombre
            usu.last_name=apellido
            usu.email=email
            usu.username=nom_usuario
            usu.set_password(clave)
            usu.save()

            #Ingresar a la tabla de Autor
            usuar = User.objects.get(username=nom_usuario)
            autor = Autor()
            autor.usuario = usuar
            if ima is not None:
                autor.imagen = ima
            if pres is not None:
                autor.presentacion = pres
            autor.save()
            
            us = authenticate(request,username=nom_usuario,password=clave)
            login_aut(request,us)
            imag = Obra.objects.filter(publicar=True)
            tecnicas = Tecnica.objects.all()

            mensaje = "Ha iniciado sesión."
            icono = "success"
            contexto = {"obras":imag, "tecnicas":tecnicas,"carru":carrusel,"aut":aut,"caut":caut,"cobr":cobr,"mensaje":mensaje,"icono":icono} 
            return render(request,"index.html",contexto)

    contexto = {"mensaje":mensaje,"icono":icono}
    return render(request,"crear_usuario.html",contexto)

@login_required(login_url='/inicio_sesion/')
def ingresar_obra_adm(request):
    mensaje = "0"
    icono = ""
    nom_user= request.user.username
    tecnicas = Tecnica.objects.all()

    obj_aut = User.objects.get(username=nom_user)
    autor = Autor.objects.get(usuario=obj_aut)

    obras = Obra.objects.filter(autor=autor)
    cobr = Obra.objects.filter(autor=autor).count()

    if request.POST:
        ima = request.FILES.get("txtObra")
        nom_obra = request.POST.get("txtNombreObra")
        descr = request.POST.get("txtDescripcion")
        hist = request.POST.get("txtHistoria")
        val = request.POST.get("txtValor")
        #dato de tabla foranea
        tecn = request.POST.get("cboTecnicaUsada")
        obj_tec = Tecnica.objects.get(nombre_tecnica=tecn)

        #guardar datos
        try:
            n_obra = Obra.objects.get(nombreObra=nom_obra)
            icono = "error"
            mensaje = "El nombre de la obra coinside con una ya existente."

            obras = Obra.objects.filter(autor=autor)
            cobr = Obra.objects.filter(autor=autor).count()
            
        except:
            n_obra = Obra()
            n_obra.nombreObra = nom_obra
            if ima is not None:
                n_obra.imagen=ima
            n_obra.descripcion=descr
            n_obra.historia=hist
            n_obra.valor=val
            n_obra.tecnica=obj_tec
            n_obra.autor=autor
            n_obra.save()

            # envio el token
            dispositivos = FCMDevice.objects.filter(active=True)
            dispositivos.send_message(
                title='¡¡Tenemos una nueva obra!!',
                body= nom_user+' ha subido una nueva obra.',
                icon='/static/img/icono.png'
            )
            icono = "success"
            mensaje = "La obra se ha ingresado con éxito."
            obras = Obra.objects.filter(autor=autor)
            cobr = Obra.objects.filter(autor=autor).count()

    contexto = {"tecnicas":tecnicas,"obras":obras,"cobr":cobr,"mensaje":mensaje,"icono":icono}
    return render(request,"administracion.html",contexto)

def inicio_sesion (request):
    mensaje = "0"
    icono = ""
    if request.POST:
        nombre = request.POST.get("txtUser")
        password = request.POST.get("txtClaveInicio")
        us = authenticate(request, username=nombre, password=password)

        if us is not None and us.is_active:
            imag = Obra.objects.filter(publicar=True)
            tecnicas = Tecnica.objects.all()
            carrusel = Obra.objects.filter(publicar=True).order_by('nombreObra')[:2]
            aut = Autor.objects.all().order_by('usuario')
            caut = Autor.objects.all().order_by('usuario').count()
            cobr = Obra.objects.filter(publicar=True).count()
            mensaje = "Ha iniciado sesión."
            icono = "success"
            login_aut(request,us)

            contexto = {"obras":imag, "tecnicas":tecnicas,"carru":carrusel,"aut":aut,"caut":caut,"cobr":cobr,"mensaje":mensaje,"icono":icono} 
            return render(request,"index.html",contexto)
        else:
            mensaje = "Ha ocurrido un error, por favor intente nuevamente."
            icono = "error"
            contexto = {"mensaje":mensaje,"icono":icono}
            return render(request,"inicio_sesion.html",contexto)

    contexto = {"mensaje":mensaje,"icono":icono}
    return render(request,"inicio_sesion.html",contexto)

def cerrar_sesion (request):
    imag = Obra.objects.filter(publicar=True)
    tecnicas = Tecnica.objects.all()
    carrusel = Obra.objects.filter(publicar=True).order_by('nombreObra')[:2]
    aut = Autor.objects.all().order_by('usuario')
    caut = Autor.objects.all().order_by('usuario').count()
    cobr = Obra.objects.filter(publicar=True).count()

    logout(request)
    mensaje = "Ha cerrado su sesión."
    icono = "success"
    contexto = {"obras":imag, "tecnicas":tecnicas,"carru":carrusel,"aut":aut,"caut":caut,"cobr":cobr,"mensaje":mensaje,"icono":icono}
    return render(request,"index.html",contexto)

@login_required(login_url='/inicio_sesion/')
def eliminar_obra (request,id):
    nom_user= request.user.username
    oba= Obra.objects.get(id_obra=id)
    oba.delete()
    icono = "success"
    mensaje = "La obra ha sido eliminada con exito."

    tecnicas = Tecnica.objects.all()
    obj_user= User.objects.get(username=nom_user)
    autor = Autor.objects.get(usuario=obj_user)
    obras = Obra.objects.filter(autor=autor)
    cobr = Obra.objects.filter(autor=autor).count()
    contexto = {"tecnicas":tecnicas,"obras":obras,"mensaje":mensaje,"icono":icono,"cobr":cobr}
    return render(request,"administracion.html",contexto)

@login_required(login_url='/inicio_sesion/')
def modificar_obra(request,id):
    oba= Obra.objects.get(id_obra=id)
    tecnicas = Tecnica.objects.all()

    contexto = {"tecnicas":tecnicas,"obras":oba}
    return render(request,"modificar.html",contexto)

@login_required(login_url='/inicio_sesion/')
def modificacion(request):
    mensaje="0"
    icono = ""
    nom_user= request.user.username
    obj_usua = User.objects.get(username=nom_user)
    autor = Autor.objects.get(usuario=obj_usua)

    tecnicas = Tecnica.objects.all()
    obras = Obra.objects.filter(autor=autor)
    cobr = Obra.objects.filter(autor=autor).count()


    contexto = {"tecnicas":tecnicas,"obras":obras,"cobr":cobr}
    if request.POST:
        ima = request.FILES.get("txtObra")
        nom_obra = request.POST.get("txtNombreObra")
        descr = request.POST.get("txtDescripcion")
        hist = request.POST.get("txtHistoria")
        val = request.POST.get("txtValor")
        tecn = request.POST.get("cboTecnicaUsada")
        obj_tec = Tecnica.objects.get(nombre_tecnica=tecn)

        try:
            obr = Obra.objects.get(nombreObra=nom_obra)
            obr.descripcion = descr
            obr.historia = hist
            obr.valor = val
            obr.tecnica = obj_tec
            obr.comentario='--'
            if ima is not None:
                obr.imagen = ima
            obr.save()
            mensaje= "Se modifico la obra '"+nom_obra+"'."
            icono = "success"
        except:
            mensaje= "No se encontro la obra '"+nom_obra+"'."
            icono = "error"
        
        obras = Obra.objects.filter(autor=autor)
        cobr = Obra.objects.filter(autor=autor).count()
        contexto = {"tecnicas":tecnicas,"mensaje":mensaje,"icono":icono,"obras":obras,"cobr":cobr}
    return render(request,"administracion.html",contexto)

@login_required(login_url='/inicio_sesion/')
def mi_perfil(request):
    mensaje = '0'
    icono = ''
    nom_user= request.user.username
    obj_aut = User.objects.get(username=nom_user)
    aut = Autor.objects.get(usuario=obj_aut)

    contexto = {"cuenta":aut,"mensaje":mensaje,"icono":icono}
    return render(request,"mi_perfil.html",contexto)

@login_required(login_url='/inicio_sesion/')
def mi_perfil_mod(request):
    mensaje = '0'
    icono = ''
    nom_user= request.user.username
    obj_aut = User.objects.get(username = nom_user)
    aut = Autor.objects.get(usuario=obj_aut)

    contexto = {"cuenta":aut,"mensaje":mensaje,"icono":icono}
    if request.POST:
        ima = request.FILES.get("txtImgUsuario")
        nomb = request.POST.get("txtNombre")
        apell = request.POST.get("txtApellido")
        usuar = request.POST.get("txtUsuario")
        corr = request.POST.get("txtCorreo")
        presen = request.POST.get("txtPresentacion")

        try:
            usu = User.objects.get(username=nom_user)
            usu.first_name=nomb
            usu.last_name=apell
            usu.email=corr
            usu.username=usuar
            usu.save()
        except:
            icono = "error"
            mensaje= "No se pudo modificar al usuario "+usuar

        try:
            usu = User.objects.get(username=nom_user)
            autor = Autor.objects.get(usuario = usu)
            autor.usuario = usu
            if ima is not None:
                autor.imagen = ima
            if presen is not None:
                autor.presentacion = presen
            autor.save()
            icono = "success"
            mensaje= "Se modifico al usuario "+usuar
        except:
            icono = "error"
            mensaje= "No se pudo modificar al usuario "+usuar
        aut = Autor.objects.get(usuario=obj_aut)

        contexto = {"cuenta":aut,"mensaje":mensaje,"icono":icono}
    return render(request,"mi_perfil.html",contexto)

@login_required(login_url='/inicio_sesion/')
def insertar_gal(request):
    mensaje="0"
    icono=''
    if request.POST:
        nombre = request.POST.get("txtObraGal")
        img = request.FILES.get("txtImgGal")
        obj_obra = Obra.objects.get(nombreObra=nombre)

        gale = Galeria()
        gale.imagen = img
        gale.obra_orig = obj_obra
        gale.save()
        mensaje = "Se añadió la imagen a la galería de '"+nombre+"' con éxito."
        icono = "success"

    nom_user= request.user.username
    tecnicas = Tecnica.objects.all()
    obj_user = User.objects.get(username=nom_user)
    autor = Autor.objects.get(usuario=obj_user)

    obras = Obra.objects.filter(autor=autor)
    cobr = Obra.objects.filter(autor=autor).count()
    contexto = {"tecnicas":tecnicas,"obras":obras,"cobr":cobr,"mensaje":mensaje,"icono":icono}
    return render(request,"administracion.html",contexto)