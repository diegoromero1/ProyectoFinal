from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from ProyectoSernacApp.models import Contacto


class ApiTestCase(TestCase):
    fixtures = ['ProyectoSernacApp.json', ]

    def setUp(self):
        self.client = APIClient()
        self.Contaco = {"nombre": "luz santana", "mensaje": "consulta sobre derechos"}
        User = get_user_model()
        self.user = User.objects.create_superuser('servidor', 'api@test.com', "Secret.123")
        c = Client()
        response = c.post('/api/login/', {'username': 'servidor', 'password': 'Secret.123'})
        self.token = response.json()["token"]
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token)

    def test_api_crear_consulta(self):
        response = self.client.post(
            reverse('api_crear_consulta'),
            self.Contaco,
            format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)