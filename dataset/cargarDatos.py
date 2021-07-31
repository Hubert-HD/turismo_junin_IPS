# python manage.py makemigrations
# python manage.py migrate
# python manage.py shell < cargarDatos.py

import json
from home.models import Provincia, Categoria, Distrito, Recurso, Coordenadas

with open('data.json') as file:
  data = json.load(file)

  print(Provincia.objects.all())
  print(Distrito.objects.all())
  print(Coordenadas.objects.all())
  print(Recurso.objects.all())

  provincias = data['provincias']
  categorias = data['categorias']
  recursos = data['recursos']

  for provincia in provincias:
    p = Provincia.objects.create(nombre=provincia["nombre"])
    for distrito in provincia["distritos"]:
      Distrito.objects.create(nombre=distrito, provincia_id=p)

  for categoria in categorias:
    Categoria.objects.create(nombre=categoria, tipo=True)

  for recurso in recursos:
    r = Recurso.objects.create(nombre=recurso["nombre"], image_URL=recurso["imagen"], subtitulo=recurso["subtitulo"], descripcion=recurso["descripcion"], distrito_id=Distrito.objects.get(nombre=recurso["ubicacion"]["distrito"]), categoria_id=Categoria.objects.get(nombre=recurso["categoria"]))
    Coordenadas.objects.create(latitud=recurso["coordenadas"]["latitud"], longitud=recurso["coordenadas"]["longuitud"], recurso_id=r)

print(Provincia.objects.all())
print(Categoria.objects.all())
print(Distrito.objects.all())
print(Coordenadas.objects.all())
print(Recurso.objects.all())
