from django.shortcuts import render,get_object_or_404
from .models import Administradores,Imagen,Peliculas
from pagina_clientes.models import Usuario
from django.contrib.auth.models import User
import os
from django.conf import settings
# Create your views here.

def index(request):
    return render(request,'panel_administracion.html')

# Funciones administradores
def opc_admins(request):
    administradores = Administradores.objects.all()
    return render(request,'html/administradores/opciones_administradores.html',{'administradores':administradores})

def admins_totales(request):
    administradores = Administradores.objects.all()
    return render(request,'html/administradores/administradores_totales.html',{'administradores':administradores})

def crear_admin(request):
    if request.method == "POST":
        nombre_administrador = request.POST["nombre_admin"].strip()
        contrasena_administrador = request.POST["contrasena_admin"].strip()
        confirmar_contrasena_administrador = request.POST["confirmar_contrasena_admin"]
        if nombre_administrador == "" or contrasena_administrador == "":
            context = {'mensaje':'Error: Todos los campos son obligatorios'}
        elif contrasena_administrador == confirmar_contrasena_administrador:
            if User.objects.filter(username = nombre_administrador).exists():
                context = {'mensaje':'Error: El nombre del administrador ya existe'}
            else:
                User.objects.create_superuser(username=nombre_administrador,password=contrasena_administrador)
                administrador = Administradores.objects.create(nombre_admin = nombre_administrador, contrasena_admin = contrasena_administrador)
                context = {'mensaje':'Administrador creado exitosamente','administrador':administrador}
        else:
            context = {'mensaje':'Error: Las contraseñas no coinciden'}
        return render(request,'html/administradores/crear_administrador.html',context)
    else:
        return render(request,'html/administradores/crear_administrador.html')

def encontrar_administrador(request,pk):
    if pk != " ":
        administrador = Administradores.objects.get(id_admin = pk)
        context = {'administrador':administrador}
    if administrador:
        return render(request,'html/administradores/modificar_administrador.html',context)
    else:
        context = {'mensaje':'Error, id del administrador no encontrado'}
        return render(request,'html/administradores/opciones_administradores.html',context)

def modificar_administrador(request):
    if request.method == "POST":
        id_admin = request.POST["id_admin"]
        administrador = get_object_or_404(Administradores,id_admin = id_admin)
        nombre_admin = request.POST["nombre_admin"].strip()
        contrasena_admin = request.POST["contrasena_admin"].strip()
        contrasena_nueva1 = request.POST["contrasena_nueva1"].strip()
        contrasena_nueva2 = request.POST["contrasena_nueva2"].strip()
        bandera = False
        mensaje = ''
        if nombre_admin == "":
            if nombre_admin != administrador.nombre_admin.strip():
                if Administradores.objects.filter(nombre_admin = nombre_admin).exists():
                    mensaje = 'Error: El nombre de administrador ya existe'
                else:
                    administrador.nombre_admin = nombre_admin
                    bandera = True
        if contrasena_nueva1 != "" or contrasena_nueva2 != "":
            if contrasena_nueva1 != contrasena_admin:
                if contrasena_nueva1 == contrasena_nueva2:
                    administrador.contrasena_admin = contrasena_nueva1
                    bandera = True
                else:
                    mensaje = 'Error: Las contraseñas nuevas deben ser iguales'
            else:
                mensaje = 'Error: La contraseña nueva no puede ser igual a la anterior'
        elif not bandera:
            mensaje = 'Error: No se ha realizado ningún cambio'
        if bandera:
            administrador.save()
            mensaje = 'Administrador actualizado exitosamente'
        context = {'mensaje':mensaje,'administrador':administrador}
        return render(request,'html/administradores/modificar_administrador.html',context)
    else:
        administrador = Administradores.objects.all()
        context = {'administrador':administrador}
        return render(request,'html/administradores/opciones_administradores.html',context)

def eliminar_administrador(request,pk):
    context = {}
    try:
        administrador = Administradores.objects.get(id_admin = pk)
        administrador.delete()
        total_administradores = Administradores.objects.all()
        context['total_administradores':total_administradores]
        return render(request,'html/administradores/opciones_administradores.html',context)
    except Administradores.DoesNotExist:
        administrador = Administradores.objects.all()
        context = {'administrador':administrador,'mensaje': 'Error, id del administrador no encontrado'}
        return render(request,'html/administradores/opciones_administradores',context)

# Funciones Imagenes
def opciones_imagen(request):
    imagen = Imagen.objects.all()
    context = {'imagen':imagen}
    return render(request, 'html/Imagenes/opciones_imagenes.html', context)

def imagenes_totales(request):
    imagen = Imagen.objects.all()
    context = {'imagen':imagen}
    return render(request, 'html/Imagenes/imagenes_totales.html', context)

def subir_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get("imagen")
        titulo_imagen = request.POST["titulo_imagen"]
        descripcion_imagen = request.POST["descripcion_imagen"]
        if imagen and not descripcion_imagen.isspace() and not titulo_imagen.isspace():
            productos_campos = {
                "imagen": imagen,
                "titulo": titulo_imagen,
                "descripcion_imagen": descripcion_imagen
            }
            imagen = Imagen.objects.create(**productos_campos)
            context = {'mensaje': 'Imagen guardada con éxito', 'imagen': imagen}
            return render(request, 'html/Imagenes/subir_imagen.html', context)
        else:
            context = {'mensaje': 'Error: Debes completar todos los campos obligatorios'}
            return render(request, 'html/Imagenes/subir_imagen.html', context)
    else:
        return render(request, 'html/Imagenes/subir_imagen.html')

def encontrar_imagen(request,pk):
    if pk != " ":
        imagen = Imagen.objects.get(id_imagen=pk)
        context={'imagen':imagen}
    if imagen:
        return render(request,'html/Imagenes/modificar_imagen.html',context)
    else:
        context={'mensaje':'Error, id de la imagen no encontrada'}
        return render(request,'html/Imagenes/opciones_imagenes.html',context)

def modificar_imagen(request):
    if request.method == "POST":
        id_imagen = request.POST["id_imagen"]
        imagen = get_object_or_404(Imagen, id_imagen=id_imagen)
        file_imagen = request.FILES.get("file_imagen")
        titulo_imagen = request.POST["titulo_imagen"]
        descripcion_imagen = request.POST["descripcion_imagen"]
        cambios_realizados = False
        if file_imagen:
            if imagen.imagen:
                ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
                if os.path.isfile(ruta_imagen_anterior):
                    os.remove(ruta_imagen_anterior)
            imagen.imagen = file_imagen
            cambios_realizados = True
        if imagen.titulo != titulo_imagen:
            imagen.titulo = titulo_imagen
            cambios_realizados = True
        if imagen.descripcion_imagen != descripcion_imagen:
            imagen.descripcion_imagen = descripcion_imagen
            cambios_realizados = True
        if cambios_realizados:
            imagen.save()
            mensaje = 'Imagen actualizada con éxito'
        else:
            mensaje = 'No se realizaron cambios en la imagen'
        context = {'mensaje': mensaje, 'imagen': imagen}
        return render(request, 'html/Imagenes/modificar_imagen.html', context)
    else:
        imagen = Imagen.objects.all()
        context = {'imagen': imagen}
        return render(request, 'html/Imagenes/opciones_imagenes.html', context)

def eliminar_imagen(request, pk):
    context = {}
    try:
        imagenes = Imagen.objects.get(id_imagen=pk)
        imagen_url = imagenes.imagen.url
        imagenes.delete()
        if imagen_url:
            ruta_imagen = os.path.abspath(os.path.join(settings.MEDIA_ROOT, imagen_url.replace('/media/', '')))
            if os.path.isfile(ruta_imagen):
                os.remove(ruta_imagen)
                context = {'mensaje': 'Imagen eliminada con exito'}
        imagenes = Imagen.objects.all()
        context['imagenes'] = imagenes
        return render(request, 'html/Imagenes/opciones_imagenes.html', context)
    except Imagen.DoesNotExist:
        imagenes = Imagen.objects.all()
        context = {'imagenes': imagenes, 'mensaje': 'Error, id de la imagen no encontrada'}
        return render(request, 'html/Imagenes/opciones_imagenes.html', context)

# Funciones productos
def opciones_peliculas(request):
    peliculas = Peliculas.objects.all()
    context = {'peliculas':peliculas}
    return render(request, 'html/peliculas/opciones_peliculas.html', context)

def peliculas_totales(request):
    peliculas = Peliculas.objects.all()
    context = {'peliculas':peliculas}
    return render(request, 'html/peliculas/peliculas_totales.html', context)

def crear_pelicula(request):
    if request.method == "POST":
        titulo = request.POST["titulo"].strip()
        precio = request.POST["precio"].strip()
        imagen = request.FILES.get("imagen")
        if not (titulo and precio):
            context = {'mensaje':'Error: Debe rellenar todos los campos obligatorios'}
            return render(request,'html/peliculas/crear_pelicula.html',context)
        if not imagen:
            context = {'mensaje':'Error: Debes seleccionar una imagen'}
            return render(request,'html/peliculas/crear_pelicula.html')
        try:
            precio_int = int(precio)
            if precio_int <= 0:
                raise ValueError
        except ValueError:
            context = {'mensaje':'Error: El precio debe ser un número mayor a 0'}
            return render(request,'html/peliculas/crear_pelicula.html',context)
        pelicula_campos = {"titulo": titulo,"precio":precio,"imagen":imagen}
        pelicula = Peliculas.objects.create(**pelicula_campos)
        context = {'mensaje':'Pelicula creada exitosamente','pelicula':pelicula}
        return render(request,'html/peliculas/crear_pelicula.html',context)
    else:
        return render(request,'html/peliculas/crear_pelicula.html')

def encontrar_pelicula(request,pk):
    if pk != " ":
        peliculas = Peliculas.objects.get(id_pelicula=pk)
        context = {'peliculas':peliculas}
    if peliculas:
        return render(request,'html/peliculas/modificar_pelicula.html',context)
    else:
        context = {'mensaje': 'Error: Id de la palicula no encontrada'}
        return render(request,'html/peliculas/opciones_peliculas.html',context)

def modificar_pelicula(request):
    if request.method == "POST":
        id_pelicula = request.POST["id_pelicula"]
        peliculas = get_object_or_404(Peliculas,id_pelicula=id_pelicula)
        titulo = request.POST["titulo"].strip()
        precio = request.POST["precio"].strip()
        imagen = request.FILES.get("imagen")
        bandera = False
        mensaje = ""
        if titulo and peliculas.titulo != titulo:
            peliculas.titulo = titulo
            bandera = True
        if precio:
            try:
                precio_int = int(precio)
                if precio_int <=0:
                    raise ValueError
                if peliculas.precio != precio_int:
                    peliculas.precio = precio_int
                    bandera = True
            except ValueError:
                mensaje = "Error: El precio debe ser un número mayor a 0"
        if imagen:
            if peliculas.imagen:
                ruta_imagen_anterior = os.path.join(settings.MEDIA_ROOT, str(peliculas.imagen))
                if os.path.isfile(ruta_imagen_anterior):
                    os.remove(ruta_imagen_anterior)
            peliculas.imagen = imagen
            bandera = True
        if imagen:
            peliculas.imagen = imagen
            bandera = True
        if bandera:
            peliculas.save()
            mensaje = 'Pelicula actualizada con exito'
        elif not mensaje:
            mensaje = "No se realizaron cambion en la pelicula"
        context = {'mensaje':mensaje,"peliculas":peliculas}
        return render(request,'html/peliculas/modificar_pelicula.html',context)
    else:
        peliculas = Peliculas.objects.all()
        context = {'peliculas':peliculas}
        return render(request,'html/peliculas/opciones_peliculas.html',context)

def eliminar_pelicula(request,pk):
    context = {}
    try:
        peliculas = Peliculas.objects.get(id_pelicula = pk)
        imagen_url = peliculas.imagen.url
        peliculas.delete()
        if imagen_url:
            ruta_imagen = os.path.abspath(os.path.join(settings.MEDIA_ROOT, imagen_url.replace('/media/', '')))
            if os.path.isfile(ruta_imagen):
                os.remove(ruta_imagen)
                context = {'mensaje': 'Pelicula eliminada correctamente'}
        peliculas = Peliculas.objects.all()
        context['peliculas'] = peliculas
        return render(request,'html/peliculas/opciones_peliculas.html',context)
    except Peliculas.DoesNotExist:
        peliculas = Peliculas.objects.all()
        context = {'peliculas':peliculas,'mensaje':'Error, id de la pelicula no encontrada'}
        return render(request,'html/peliculas/opciones_peliculas.html',context)

# Funciones usuarios
def opciones_usuarios(request):
    usuario = Usuario.objects.all()
    context = {'usuario':usuario}
    return render(request, 'html/usuarios/opciones_usuarios.html',context)

def usuarios_totales(request):
    usuario = Usuario.objects.all()
    context = {'usuario':usuario}
    return render(request, 'html/usuarios/usuarios_totales.html',context)

def crear_usuario(request):
    if request.method == "POST":
        correo_usuario = request.POST["correo_usuario"].strip()
        contrasena_usuario = request.POST["contrasena_usuario"].strip()
        confirmar_contrasena_usuario = request.POST["confirmar_contrasena_usuario"].strip()
        if not (correo_usuario and contrasena_usuario and confirmar_contrasena_usuario):
            context = {'mensaje': 'Error: Todos los campos son obligatorios'}
        elif contrasena_usuario == confirmar_contrasena_usuario:
            if Usuario.objects.filter(correo_usuario=correo_usuario).exists():
                context = {'mensaje': 'Error: El correo ingresado ya está en uso'}
            else:
                MAX_CORREO_USUARIO_LENGTH = 50
                MAX_CONTRASENA_USUARIO = 30
                if len(correo_usuario) > MAX_CORREO_USUARIO_LENGTH:
                    context = {'mensaje': f'❌ Error: El correo del usuario debe tener como máximo {MAX_CORREO_USUARIO_LENGTH} caracteres'}
                elif len(contrasena_usuario) > MAX_CONTRASENA_USUARIO:
                    context = {'mensaje': f'❌ Error: La contraseña de usuario debe tener como máximo {MAX_CONTRASENA_USUARIO} caracteres'}
                else:
                    campos_usuario = {
                        "correo_usuario": correo_usuario,
                        "contrasena_usuario": contrasena_usuario
                    }
                    usuario = Usuario.objects.create(**campos_usuario)
                    context = {'mensaje': 'Usuario creado con éxito', 'usuario': usuario}
        else:
            context = {'mensaje': 'Error: Las contraseñas deben ser iguales'}
        return render(request, 'html/usuarios/crear_usuario.html', context)
    else:
        return render(request, 'html/usuarios/crear_usuario.html')

def encontrar_usuario(request,pk):
    if pk != " ":
        usuario = Usuario.objects.get(id_usuario = pk)
    context = {'usuario':usuario}
    if usuario:
        return render(request,'html/usuarios/modificar_usuario.html',context)
    else:
        context={'mensaje':'Error, id del usuario no encontrado'}
        return render(request,'html/usuarios/opciones_usuarios.html',context)

def modificar_usuario(request):
    if request.method == "POST":
        id_usuario = request.POST["id_usuario"]
        usuario = get_object_or_404(Usuario, id_usuario = id_usuario)
        correo_usuario = request.POST["correo_usuario"].strip()
        contrasena_usuario = request.POST["contrasena_usuario"].strip()
        contrasena_nueva1 = request.POST["contrasena_nueva1"].strip()
        contrasena_nueva2 = request.POST["contrasena_nueva2"].strip()
        bandera = False
        mensaje = ''
        if correo_usuario != "":
            if correo_usuario != usuario.correo_usuario.strip():
                if Usuario.objects.filter(correo_usuario=correo_usuario).filter():
                    mensaje = 'Error: El correo del usuario ya está en uso'
                else:
                    usuario.correo_usuario = correo_usuario
                    bandera = True
        if contrasena_nueva1 != "" or contrasena_nueva2 != "":
            if contrasena_nueva1 != contrasena_usuario:
                if contrasena_nueva1 == contrasena_nueva2:
                    usuario.contrasena_usuario = contrasena_nueva1
                    bandera = True
                else:
                    mensaje = 'Error: Las contraseñas nuevas deben ser iguales'
            else:
                mensaje = 'Error: La contraseña nueva no puede ser igual a la anterior'
        elif not bandera:
            mensaje = 'Error: No se ha realizado ningún cambio'
        if bandera:
            usuario.save()
            mensaje = 'Usuario actualizado con éxito'
        context = {'mensaje': mensaje, 'usuario': usuario}
        return render(request, 'html/usuarios/modificar_usuario.html', context)
    else:
        usuario = Usuario.objects.all()
        context = {'usuario':usuario}
        return render(request, 'html/usuarios/opciones_usuarios.html',context)

def eliminar_usuario(request,pk):
    context = {}
    try:
        usuario = Usuario.objects.get(id_usuario=pk)
        usuario.delete()
        usuarios_totales = Usuario.objects.all()
        context['usuarios_totales'] = usuarios_totales
        return render(request,'html/usuarios/opciones_usuarios.html',context)
    except Usuario.DoesNotExist:
        usuario = Usuario.objects.all()
        context = {'usuario':usuario,'mensaje':'Error, id del usuario no encontrado'}
        return render(request,'html/usuarios/opciones_usuarios.html',context)