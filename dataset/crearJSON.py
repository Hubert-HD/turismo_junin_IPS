import json, re, string

provincias = []
recursos = []
categorias = []

with open('datos_junin.json') as file:
  data = json.load(file)
  provinciasList = []
  for o in data:
    categoria = o["CATEGORIA"][3:]
    provincia = o["PROVINCIA"]
    try:
      categorias.index(categoria)
    except:
      categorias.append(categoria)
    try:
      provinciasList.index(provincia)
    except:
      provinciasList.append(provincia)
  
  for p in provinciasList:
    provincias.append({
      "nombre": p,
      "distritos": []
    })

  for o in data:
    distrito = o["DISTRITO"]
    provincia = o["PROVINCIA"]
    i = provinciasList.index(provincia)
    try:
      provincias[i]["distritos"].index(distrito)
    except:
      provincias[i]["distritos"].append(distrito)
  
  for o in data:
    nombre = o["NOMBRE_RE"].lower()
    nombre = string.capwords(nombre, sep=None)
    provincia = o["PROVINCIA"]
    distrito = o["DISTRITO"]
    categoria = o["CATEGORIA"][3:]
    coordenada = o["the_geom"]
    patron = re.compile('-[0-9]+.[0-9]+')
    longuitud = float(patron.findall(coordenada)[0])
    latitud = float(patron.findall(coordenada)[1])

    recursos.append({
      "nombre": nombre,
      "categoria": categoria,
      "ubicacion": {
        "provincia": provincia,
        "distrito": distrito
      },
      "coordenadas":{
        "latitud": latitud,
        "longuitud": longuitud
      },
      "imagen": "imagen",
      "subtitulo": "subtitulo",
      "descripcion": "descripcion"
    })

with open('data.json', 'w') as file:
  dict = {
    "categorias": categorias,
    "provincias": provincias,
    "recursos": recursos
  }
  json.dump(dict, file, indent=4)