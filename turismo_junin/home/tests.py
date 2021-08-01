from django.test import TestCase

from .views import homeView
from .models import Provincia, Distrito, Categoria, Recurso
from allauth.socialaccount.models import SocialAccount

# Create your tests here.
class HomeTestCase(TestCase):
  def setUp(self):
    provincia = Provincia.objects.create(nombre="provincia")
    distrito = Distrito.objects.create(nombre="distrito", provincia_id=provincia)
    categoria = Categoria.objects.create(nombre="categoria", tipo=True)
    Recurso.objects.create(nombre="nombre", image_URL="imagen", subtitulo="subtitulo", descripcion="descripcion", distrito_id=distrito, categoria_id=categoria)
    SocialAccount.objects.create()

  def test_get_ok(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    print(response.context["recomendados"])
    """ self.assertEqual(len(response.context['customers']), 5) """
  
  def test_userlogeado(self):
    response = self.client.get("/")
    self.assertEqual(response.status_code, 200)
    print(response.context)
    """ self.assertEqual(len(response.context['customers']), 5) """
  