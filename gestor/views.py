from django.http import HttpResponse
from django.shortcuts import redirect, render
from .formularios import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import datetime

from gestor.models import articulo
from gestor.models import cliente

def formulario(request):
    return render(request, "formulario.html")

def formularioBusqueda(request):
    arti=[]
    ar=articulo.objects.all()
    for i in ar:
        arti.append(i.seccion)
    arti=sorted(list(set(arti)))
    return render(request, "formuBusqueda.html", {'articulos':arti})

def resultado(request):

    if len(request.GET["producto"])>=20:
        arti=[]
        ar=articulo.objects.all()
        for i in ar:
            arti.append(i.seccion)
        arti=sorted(list(set(arti)))
        return render(request, "formuBusqueda.html",{'articulos':arti, 'error': True})
    
    encontrado= True
    if not(request.GET["producto"]=="") and not(request.GET["seccion"]=="todos"):
        nombre=request.GET["producto"]
        seccion=request.GET["seccion"]
        resultado=articulo.objects.filter(nombre__icontains=nombre, seccion=seccion)
    
    elif not(request.GET["producto"]=="") and request.GET["seccion"]=="todos":
        nombre=request.GET["producto"]
        resultado=articulo.objects.filter(nombre__icontains=nombre)
    
    elif request.GET["producto"]=="" and not(request.GET["seccion"]=="todos"):
        seccion=request.GET["seccion"]
        resultado=articulo.objects.filter(seccion=seccion)
    
    elif request.GET["producto"]=="" and request.GET["seccion"]=="todos":
        resultado=articulo.objects.all()
    if not resultado:
        encontrado=False
    return render(request, "resulBusqueda.html",{'registro':resultado, 'estatus':encontrado})

def respuesta(request):
    añoActual=datetime.datetime.now().year
    diaActual=datetime.datetime.now().day
    mesActual=datetime.datetime.now().month
    añoNacimiento = int(request.GET["nacimiento"].split('-')[0])
    mesNacimiento = int(request.GET["nacimiento"].split('-')[1])
    diaNacimiento = int(request.GET["nacimiento"].split('-')[2])

    edad= añoActual - añoNacimiento
    if mesNacimiento > mesActual:
        edad-=1
    elif mesActual==mesNacimiento:
        if diaActual < diaNacimiento:
            edad-=1

    nombre=request.GET["nombre"]
    genero=request.GET["genero"]
    return render(request, 'respu.html', {'nombre':nombre, 'edad':edad, 'genero':genero})

def validacion(request):
    nombre= request.POST["nombre"]
    direccion= request.POST["direccion"]
    telefono= request.POST["telefono"]
    password= request.POST["password"]
    passwordRep= request.POST["passwordRep"]
    email= request.POST["email"]
    status=(nombre, direccion, telefono, password, passwordRep, email)

    if len(list(status.keys()))>0:
        return render(request, 'registro.html', {'status':status})
    else:
        cliente.objects.create(nombre=nombre, direccion=direccion, email=email, telefono=telefono, password=password)
        return render(request, "registroExitoso.html", {'nombre':nombre})



# def verificacion(nombre, direccion, telefono, password, passwordRep,email):
#     dicError={}

#     if len(nombre)>=40 or len(nombre) < 3:
#         dicError.setdefault('errorNombre', 'El nombre debe contener mas de 3 letras y menor o igual a 40 letras')
    
#     if len(direccion)>=40 or len(direccion):
#         dicError.setdefault('errorDireccion', 'La direccion debe contener mas de 3 letras')

#     if not(len(telefono)==10):
#         dicError.setdefault('errorTelefono', 'El numero telefonico dede tener 10 digitos')

#     for i in telefono:
#         if ord(i) < 48 or ord(i) > 58:
#             if 'errorTelefono' in dicError:
#                 dicError['errorTelefono']="El telefono solo puede contener numeros"
#                 break
#             else:
#                 dicError.setdefault("errorTelefono", "El numero telefonico no puede contener letras")
#                 break
#     if len(password)==0:
#         dicError.setdefault('errorDireccion', "Debe ingresar una direccion")
    
#     if len(password)>= 21 or len(password)<=7:
#         if 'errorPassword' in dicError:
#             dicError['errorpassword']="La contraseña debe tener al menos 8 caracteres y no ser mayor a 20 caracteres"
#         else:
#             dicError.setdefault('errorPassword', "La contraseña debe tener al menos 8 caracteres y no ser mayor a 20 caracteres")
    
#     if not(password==passwordRep):
#         if 'errorPasword' in dicError:
#             dicError['errorPassword']= "La contraseña y la repeticion de la contraseña no coinciden"
#         else:
#             dicError.setdefault('errorPassword', "La contraseña y la repeticion de la contraseña no coinciden")
    
#     if len(email)==0:
#         dicError.setdefault('errorEmail', "Debe ingresar un correo")
#         emailEnBase = cliente.objects.filter(email=email)
#     if not len(emailEnBase)==0:
#         if "errorEmail" in  dicError:
#             dicError['erorEmail']="El correo electronico no esta disponible"
#         else:
#             dicError.setdefault('errorEmail', "El correo electronico no esta disponible")
#     return dicError

def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            form.save()
            messages.success(request, "Usuario %s creado" %username)

    else:
        form=UserRegisterForm()
    contexto={"formulario":form}
    return render(request, "register.html", contexto)

def ingresar(request):
    if request.method=='POST':
        form=AuthenticationForm(request, request.POST)
        if form.is_valid():
            nombreUsuario=form.cleaned_data.GET['username']
            contraseña=form.cleaned_data.GET['password']
            usuario=authenticate(username=nombreUsuario, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, "Bienvenido nuevamente %s" %nombreUsuario)
                return redirect("home")
            else:
                messages.error(request, "El usuario o contraseña son incorrectos")
        else:
            messages.error(request, "El usuario o contraseña son incorrectos")
            
    else:
        form=AuthenticationForm()
    contexto={"formulario":form}
    return render(request, "login.html", contexto)

def home(request):
    return render(request, "index.html")

def salir(request):
    logout(request)
    messages.success(request, "Session Cerrada")
    return redirect("ingresar")