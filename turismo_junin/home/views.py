from django.shortcuts import render
from django.http import JsonResponse

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

# Envía los recursos turístico recomendados que se mostrará en la página principal
def homeView(request):
  recomendados = []
  for recurso in Recurso.objects.all().order_by('nombre')[:5]:
    recomendados.append({
      'id': recurso.id,
      'imagen': recurso.image_URL,
      'nombre': recurso.nombre,
      'provincia': recurso.distrito_id.nombre,
      'categoria': recurso.categoria_id.nombre,
      'corazones': Favorito.objects.filter(recurso_id=recurso).count()
    })

  context ={
    "recomendados" : recomendados
  }

  context = contextAddUser(request, context)
  return render(request, 'pages/home.html', context)

# Envía los lugares turístico recomendados por categoría (naturales, culturales, realizaciones), las provincias de Junín y las categorías (Sitios Naturales, Sitios Culturales, Realizaciones Contemporáneas) que se mostrará en la página de destinos
def destinoView(request):
  provincias = []
  categorias = []
  naturales = []
  culturales = []
  realizaciones = []
  for provincia in Provincia.objects.all():
    provincias.append(provincia.nombre)
  for categoria in Categoria.objects.filter(tipo=True):
    categorias.append(categoria.nombre)
  for recurso in Recurso.objects.all().order_by('nombre')[:3]:
    r = {
      'imagen': recurso.image_URL,
      'nombre': recurso.nombre,
      'provincia': recurso.distrito_id.nombre,
      'categoria': recurso.categoria_id.nombre,
      'corazones': 0
    }
    naturales.append(r)
    culturales.append(r)
    realizaciones.append(r)

  context ={
    "provincias": provincias,
    "categorias": categorias,
    "recomendados" : {
      "naturales" : naturales,
      "culturales" : culturales,
      "realizaciones" : realizaciones
    }
  }
  context = contextAddUser(request, context)
  return render(request, 'pages/destinos.html', context)

# Envía los datos del lugar turístico que pidió el cliente desde su navegador y los recursos turísticos recomendados que se mostrará en la página respectiva al lugar turístico pedido.
def lugarTuristicoView(request, nombre):
  if(Recurso.objects.filter(nombre=nombre).exists()):
    recomendados = []
    for recurso in Recurso.objects.all().order_by('nombre')[:5]:
      recomendados.append({
        'id': recurso.id,
        'imagen': recurso.image_URL,
        'nombre': recurso.nombre,
        'provincia': recurso.distrito_id.provincia_id.nombre,
        'categoria': recurso.categoria_id.nombre,
        'corazones': 0
      })
    recurso = Recurso.objects.filter(nombre=nombre).get()
    context = {
      "imagen": recurso.image_URL,
      "nombre": recurso.nombre,
      "subtitulo": recurso.subtitulo,
      "provincia": recurso.distrito_id.provincia_id.nombre,
      "distrito": recurso.distrito_id.nombre,
      "categoria": recurso.categoria_id.nombre,
      "corazones": 0,
      "parrafos": [ recurso.descripcion ],
      "recomendados" : recomendados
    };
    context = contextAddUser(request, context)
    return render(request, 'pages/lugar.html', context)
  else:
    return render(request, 'no_econtrado.html')

def favoritosView(request):
  provincias = []
  categorias_tangibles = []
  categorias_no_tangibles = []
  for provincia in Provincia.objects.all():
    provincias.append(provincia.nombre)
  for categoria in Categoria.objects.filter(tipo=True):
    categorias_tangibles.append(categoria.nombre)
  for categoria in Categoria.objects.filter(tipo=False):
    categorias_no_tangibles.append(categoria.nombre)

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
  for distrito in Distrito.objects.filter(provincia_id__nombre=provincia):
    data.append(distrito.nombre)
  return JsonResponse(data, safe=False)

# Envía un archivo json con los lugares turísticos correspondientes al filtro que realizó el cliente desde su navegador (donde los parámetros del filtro por provincia, por distrito y por categoría son pasados como parámetros de una petición GET)
def getDestinos(request):
  provincia = request.GET["provincia"];
  distrito = request.GET["distrito"];
  categoria = request.GET["categoria"];

  recursos = Recurso.objects.all()
  if Provincia.objects.filter(nombre=provincia).exists():
    recursos = recursos & Recurso.objects.filter(distrito_id__provincia_id__nombre=provincia)
  if Distrito.objects.filter(nombre=distrito).exists():
    recursos = recursos & Recurso.objects.filter(distrito_id__nombre=distrito)
  if Categoria.objects.filter(nombre=categoria).exists():
    recursos = recursos & Recurso.objects.filter(categoria_id__nombre=categoria)

  data=[]
  for recurso in recursos:
    data.append({
      'id': recurso.id,
      'link': recurso.image_URL,
      'nombre': recurso.nombre,
      'provincia': recurso.distrito_id.provincia_id.nombre,
      'distrito': recurso.distrito_id.nombre,
      'categoria': recurso.categoria_id.nombre,
      'corazones': 0
    })

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
  provincia = request.GET["provincia"];
  distrito = request.GET["distrito"];
  categoria = request.GET["categoria"];

  recursos = Recurso.objects.all().order_by('nombre')[:5]
  data=[]
  for recurso in recursos:
    data.append({
      'link': recurso.image_URL,
      'nombre': recurso.nombre,
      'provincia': recurso.distrito_id.provincia_id.nombre,
      'distrito': recurso.distrito_id.nombre,
      'categoria': recurso.categoria_id.nombre,
      'corazones': 0
    })

  return JsonResponse(data, safe=False)

def getRecursos(request):
  provincia = request.GET["provincia"];
  distrito = request.GET["distrito"];
  categoria = request.GET["categoria"];
  data = []
  if request.user.is_authenticated:
    user = SocialAccount.objects.get(user=request.user)
    favoritos = Favorito.objects.filter(usuario_id=user)
    for favorito in favoritos:
      recurso = favorito.recurso_id        
      data.append({
        'id': recurso.id,
        'link': recurso.image_URL,
        'nombre': recurso.nombre,
        'provincia': recurso.distrito_id.provincia_id.nombre,
        'distrito': recurso.distrito_id.nombre,
        'categoria': recurso.categoria_id.nombre,
        'corazones': 0
      })
    if Provincia.objects.filter(nombre=provincia).exists():
      newData = []
      for recurso in data:
        if recurso["provincia"] == provincia:
          newData.append(recurso)
      data = newData
    if Distrito.objects.filter(nombre=distrito).exists():
      newData = []
      for recurso in data:
        if recurso["distrito"] == distrito:
          newData.append(recurso)
      data = newData
    if Categoria.objects.filter(nombre=categoria).exists():
      newData = []
      for recurso in data:
        if recurso["categoria"] == categoria:
          newData.append(recurso)
      data = newData
  return JsonResponse(data, safe=False)

#-usuario es anonimo user (anonimo, auth) tipo (all, natural, cultural, contemporaneo)
def getRecursosRecomendados(user):
  recomendados = []
  if user.is_authenticated:
    favoritos = Favorito.objects.exclude(usuario_id=user)
    for f in favoritos:
      recurso = favorito.recurso_id
    print("f")
  else:
    for favorito in favoritos:
      recurso = favorito.recurso_id
      data.append({
        'id': recurso.id,
        'link': recurso.image_URL,
        'nombre': recurso.nombre,
        'provincia': recurso.distrito_id.provincia_id.nombre,
        'distrito': recurso.distrito_id.nombre,
        'categoria': recurso.categoria_id.nombre,
        'corazones': 0
      })

  return recomendados