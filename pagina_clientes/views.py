from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .models import Usuario
from administrador.models import Peliculas
from django.shortcuts import redirect


# Create your views here.

def index(request):
    return render(request,'index.html')

def cartelera(request):
    peliculas=Peliculas.objects.all()
    context={'peliculas':peliculas}
    return render(request,'html/cartelera.html',context)

def inicio(request):
    return render(request,'html/inicio.html')

def formulario(request):
    return render(request,'html/formulario.html')

def login(request):
    if request.method == "POST":
        correo_usuario = request.POST.get("email")
        contrasena = request.POST.get("password")
        usuario = Usuario.objects.filter(correo_usuario=correo_usuario, contrasena_usuario=contrasena).first()
        if usuario:
            return redirect('index')
        else:
            return render(request,'html/login.html',{"error":"Correo o contraseña erroneos, intente nuevamente"})
    else:
        return render(request, 'html/login.html')

def mas_visto(request):
    return render(request,'html/Lomasvisto.html')

def preventas(request):
    return render(request,'html/preventas.html')

def signup(request):
    if request.method == "POST":
        correo_usuario = request.POST["email"]
        contrasena_usuario = request.POST["password"]
        if Usuario.objects.filter(correo_usuario = correo_usuario).exists():
            print("No Registrado")
            return render(request,'html/signup.html',{'error':'El correo electrónico ya está en uso'})
        print("Registrado")
        usuario = Usuario(correo_usuario = correo_usuario, contrasena_usuario = contrasena_usuario)
        usuario.save()
        return redirect("login")
    else:
        return render(request, "html/signup.html")