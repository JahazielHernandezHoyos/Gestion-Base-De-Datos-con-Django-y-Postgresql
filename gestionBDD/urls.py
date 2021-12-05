"""gestionBDD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestor.views import * #formulario, ingresar, register, respuesta, formularioBusqueda, resultado,verificacion,salir,home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('formulario/', formulario),
    path('respuesta/', respuesta),
    path('buscar/', formularioBusqueda),
    path('resultado/', resultado),
    path('validacion/', verificacion),
    path('register/', register, name='Registrar'),
    path('login/', ingresar, name='Ingresar'),
    path('salir/', salir, name='Salir'),
    path('', home, name='home'),
]