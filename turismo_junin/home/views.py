from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q

from allauth.socialaccount.models import SocialAccount
from .models import Provincia, Categoria, Distrito, Recurso, Coordenada, Favorito

def contextAddUser(request, context):
  user = {
    "is_authenticated": request.user.is_authenticated
  }
  if request.user.is_authenticated:
    data = SocialAccount.objects.get(user=request.user).extra_data
    user["nombre"] = data["name"]
    user["imagen"] = data["picture"]

  context["user"] = user
  return context

def crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado):
  recursoCard = {
    'image': imagen,
    'nombre': nombre,
    'provincia': provincia,
    'categoria': categoria,
    'corazon': {
      "contador": corazones,
      "marcado": marcado
    }
  }
  return recursoCard

# Envía los recursos turístico recomendados que se mostrará en la página principal
def homeView(request):
  recomendados = []
  if request.user.is_authenticated:
    user = SocialAccount.objects.get(user=request.user)
    for recurso in Recurso.objects.order_by('-puntuacion')[:8]:
      imagen = recurso.image_URL
      nombre = recurso.nombre
      provincia = recurso.distrito_id.provincia_id.nombre
      categoria = recurso.categoria_id.nombre
      corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
      marcado = Favorito.objects.filter(recurso_id=recurso, usuario_id=user, is_active=True).exists()
      recomendados.append(crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado))
  else:
    for recurso in Recurso.objects.order_by('-puntuacion')[:8]:
      imagen = recurso.image_URL
      nombre = recurso.nombre
      provincia = recurso.distrito_id.provincia_id.nombre
      categoria = recurso.categoria_id.nombre
      corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
      marcado = False
      recomendados.append(crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado))

  context ={
    "recomendados" : recomendados
  }
  context = contextAddUser(request, context)
  return render(request, 'pages/home.html', context)

# Envía los lugares turístico recomendados por categoría (naturales, culturales, realizaciones), las provincias de Junín y las categorías (Sitios Naturales, Sitios Culturales, Realizaciones Contemporáneas) que se mostrará en la página de destinos
def destinoView(request):
  provincias = Provincia.objects.all()
  categoriasTangibles = Categoria.objects.filter(tipo=True)
  recomendados = {}
  if request.user.is_authenticated:
    user = SocialAccount.objects.get(user=request.user)
    for categoria in categoriasTangibles:
      categoriaNombre = categoria.nombre
      recomendados[categoriaNombre] = []
      for recurso in Recurso.objects.filter(categoria_id=categoria).order_by("-puntuacion")[:3]:
        imagen = recurso.image_URL
        nombre = recurso.nombre
        provincia = recurso.distrito_id.provincia_id.nombre
        categoria = recurso.categoria_id.nombre
        corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
        marcado = Favorito.objects.filter(recurso_id=recurso, usuario_id=user, is_active=True).exists()
        recomendados[categoriaNombre].append(crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado))
  else:
    for categoria in categoriasTangibles:
      categoriaNombre = categoria.nombre
      recomendados[categoriaNombre] = []
      for recurso in Recurso.objects.filter(categoria_id=categoria).order_by("-puntuacion")[:3]:
        imagen = recurso.image_URL
        nombre = recurso.nombre
        provincia = recurso.distrito_id.provincia_id.nombre
        categoria = recurso.categoria_id.nombre
        corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
        marcado = False
        recomendados[categoriaNombre].append(crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado))
  context ={
    "provincias": provincias,
    "categorias": categoriasTangibles,
    "recomendados" : recomendados
  }
  context = contextAddUser(request, context)
  return render(request, 'pages/destinos.html', context)

# Envía los datos del lugar turístico que pidió el cliente desde su navegador y los recursos turísticos recomendados que se mostrará en la página respectiva al lugar turístico pedido.
def lugarTuristicoView(request, nombre):
  if(Recurso.objects.filter(nombre=nombre).exists()):
    recursoTuristico = {}
    recomendados = []
    recurso = Recurso.objects.filter(nombre=nombre).get()
    recursoTuristico["nombre"] = recurso.nombre
    recursoTuristico["imagen"] = recurso.image_URL
    recursoTuristico["provincia"] = recurso.distrito_id.provincia_id.nombre
    recursoTuristico["distrito"] = recurso.distrito_id.nombre
    recursoTuristico["categoria"] = recurso.categoria_id.nombre
    recursoTuristico["subtitulo"] = recurso.subtitulo
    recursoTuristico["descripcion"] = recurso.descripcion
    recursoTuristico["corazones"] = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
    recursoTuristico["marcado"] = False
    if request.user.is_authenticated:
      user = SocialAccount.objects.get(user=request.user)
      recursoTuristico["marcado"] = Favorito.objects.filter(recurso_id=recurso, usuario_id=user, is_active=True).exists()
      for recurso in Recurso.objects.order_by('-puntuacion').exclude(nombre=nombre)[:8]:
        imagen = recurso.image_URL
        nombre_recurso = recurso.nombre
        provincia = recurso.distrito_id.provincia_id.nombre
        categoria = recurso.categoria_id.nombre
        corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
        marcado = Favorito.objects.filter(recurso_id=recurso, usuario_id=user, is_active=True).exists()
        recomendados.append(crearCardRecurso(imagen, nombre_recurso, provincia, categoria, corazones, marcado))
    else:
      for recurso in Recurso.objects.order_by('-puntuacion').exclude(nombre=nombre)[:8]:
        imagen = recurso.image_URL
        nombre_recurso = recurso.nombre
        provincia = recurso.distrito_id.provincia_id.nombre
        categoria = recurso.categoria_id.nombre
        corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
        marcado = False
        recomendados.append(crearCardRecurso(imagen, nombre_recurso, provincia, categoria, corazones, marcado))    
    context = {
      "recurso": recursoTuristico,
      "recomendados" : recomendados
    };
    context = contextAddUser(request, context)
    return render(request, 'pages/lugar.html', context)
  else:
    return render(request, 'no_econtrado.html')

def favoritosView(request):
  provincias = Provincia.objects.all()
  categorias_tangibles = Categoria.objects.filter(tipo=True)
  categorias_no_tangibles = Categoria.objects.filter(tipo=False)
  context ={
    "provincias": provincias,
    "categorias": {
      "tangibles": categorias_tangibles,
      "no_tangibles": categorias_no_tangibles
    }
  }
  if request.user.is_authenticated:
    context = contextAddUser(request, context)
    return render(request, 'pages/favoritos-auth.html', context)
  else:
    return render(request, 'pages/favoritos.html')

# Envía un archivo json con los distritos correspondientes de provincia (donde la provincia es pasada como un parámetro de una petición GET)
def getDistritos(request):
  provincia = request.GET['provincia']
  data=[]
  if Provincia.objects.filter(nombre=provincia).exists():
    for distrito in Distrito.objects.filter(provincia_id__nombre=provincia):
      data.append(distrito.nombre)
  return JsonResponse(data, safe=False)

# Envía un archivo json con los lugares turísticos correspondientes al filtro que realizó el cliente desde su navegador (donde los parámetros del filtro por provincia, por distrito y por categoría son pasados como parámetros de una petición GET)
def getDestinos(request):
  provinciaGET = request.GET["provincia"];
  distritoGET = request.GET["distrito"];
  categoriaGET = request.GET["categoria"];
  data = []
  if request.user.is_authenticated:
    user = SocialAccount.objects.get(user=request.user)
    for recurso in Recurso.objects.order_by('nombre'):
      imagen = recurso.image_URL
      nombre = recurso.nombre
      provincia = recurso.distrito_id.provincia_id.nombre
      distrito = recurso.distrito_id.nombre
      categoria = recurso.categoria_id.nombre
      corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
      marcado = Favorito.objects.filter(recurso_id=recurso, usuario_id=user, is_active=True).exists()
      card = crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado)
      card["distrito"] = recurso.distrito_id.nombre
      data.append(card)
  else:
    for recurso in Recurso.objects.order_by('-puntuacion'):
      imagen = recurso.image_URL
      nombre = recurso.nombre
      provincia = recurso.distrito_id.provincia_id.nombre
      categoria = recurso.categoria_id.nombre
      corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
      marcado = False
      card = crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado)
      card["distrito"] = recurso.distrito_id.nombre
      data.append(card)

  if Provincia.objects.filter(nombre=provinciaGET).exists():
    newData = []
    for r in data:
      if r["provincia"] == provinciaGET:
        newData.append(r)
    data = newData
  if Distrito.objects.filter(nombre=distritoGET).exists():
    newData = []
    for r in data:
      if r["distrito"] == distritoGET:
        newData.append(r)
    data = newData
  if Categoria.objects.filter(nombre=categoriaGET).exists():
    newData = []
    for r in data:
      if r["categoria"] == categoriaGET:
        newData.append(r)
    data = newData
  return JsonResponse(data, safe=False)

# Envía un archivo json con las coordenada de un lugar turístico (donde el nombre del lugar turístico es pasado como parámetro de una petición GET)
def getCoordenadas(request):
  nombre = request.GET["nombre"];
  data = {
    "latitud": 0,
    "longuitud": 0,
  }
  if Coordenada.objects.filter(recurso_id__nombre=nombre).exists():
    coordenada = Coordenada.objects.filter(recurso_id__nombre=nombre).get()
    data["latitud"] = coordenada.latitud
    data["longuitud"] = coordenada.longitud
  return JsonResponse(data, safe=False)

# Envía un archivo json con las coordenada de un lugar turístico (donde el nombre del lugar turístico es pasado como parámetro de una petición GET)
def getRecomendaciones(request):
  data = []
  if request.user.is_authenticated:
    user = SocialAccount.objects.get(user=request.user)
    for recurso in Recurso.objects.order_by('-puntuacion')[:8]:
      imagen = recurso.image_URL
      nombre = recurso.nombre
      provincia = recurso.distrito_id.provincia_id.nombre
      categoria = recurso.categoria_id.nombre
      corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
      marcado = Favorito.objects.filter(recurso_id=recurso, usuario_id=user, is_active=True).exists()
      data.append(crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado))
  else:
    for recurso in Recurso.objects.order_by('-puntuacion')[:8]:
      imagen = recurso.image_URL
      nombre = recurso.nombre
      provincia = recurso.distrito_id.provincia_id.nombre
      categoria = recurso.categoria_id.nombre
      corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
      marcado = False
      data.append(crearCardRecurso(imagen, nombre, provincia, categoria, corazones, marcado))
  return JsonResponse(data, safe=False)

def getRecursos(request):
  provincia = request.GET["provincia"];
  distrito = request.GET["distrito"];
  categoria = request.GET["categoria"];
  recursosFavoritos = []
  if request.user.is_authenticated:
    user = SocialAccount.objects.get(user=request.user)
    favoritos = Favorito.objects.order_by("-recurso_id__puntuacion").filter(usuario_id=user, is_active=True)
    for favorito in favoritos:
      recurso = favorito.recurso_id        
      imagen = recurso.image_URL
      nombre = recurso.nombre
      provinciaNombre = recurso.distrito_id.provincia_id.nombre
      categoriaNombre = recurso.categoria_id.nombre
      corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
      marcado = True
      card = crearCardRecurso(imagen, nombre, provinciaNombre, categoriaNombre, corazones, marcado)
      card["distrito"] = recurso.distrito_id.nombre
      recursosFavoritos.append(card)
    if Provincia.objects.filter(nombre=provincia).exists():
      newData = []
      for r in recursosFavoritos:
        if r["provincia"] == provincia:
          newData.append(r)
      recursosFavoritos = newData
    if Distrito.objects.filter(nombre=distrito).exists():
      newData = []
      for r in recursosFavoritos:
        if r["distrito"] == distrito:
          newData.append(r)
      recursosFavoritos = newData
    if Categoria.objects.filter(nombre=categoria).exists():
      newData = []
      for r in recursosFavoritos:
        if r["categoria"] == categoria:
          newData.append(r)
      recursosFavoritos = newData
  return JsonResponse(recursosFavoritos, safe=False)

def addFavoritos(request):
  nombre = request.GET["nombre"];
  data = {}
  if request.user.is_authenticated and Recurso.objects.filter(nombre=nombre).exists():
    recurso = Recurso.objects.get(nombre=nombre)
    user = SocialAccount.objects.get(user=request.user)
    if Favorito.objects.filter(usuario_id=user, recurso_id=recurso).exists():
      favorito = Favorito.objects.get(usuario_id=user, recurso_id=recurso)
      if favorito.is_active == True:
        favorito.is_active = False
        favorito.save()
        data["status"] = "QUITAR"
      else:
        favorito.is_active = True
        favorito.save()
        data["status"] = "CAMBIAR_AÑADIR"
    else:
      Favorito.objects.create(usuario_id=user, recurso_id=recurso, is_active=True)
      data["status"] = "CREAR_AÑADIR"
    cant_corazones = Favorito.objects.filter(recurso_id=recurso, is_active=True).count()
    recurso.puntuacion = cant_corazones * 10
    recurso.save()
    data["corazones"] = cant_corazones
  else:
    data["status"] = "SIN_PERMISOS"
  return JsonResponse(data, safe=False)