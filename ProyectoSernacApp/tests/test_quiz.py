import pytest
from ddf import G,F
from ProyectoSernacApp.models import PreguntasRespondidas
from faker import Faker
fake = Faker()
"""
@pytest.fixture
def crate_pregunta():
    return G(PreguntasRespondidas, QuizUsuario=[F(usuario=fake.name())])

@pytest.mark.django_db
def test_crate_pregunta(crate_pregunta):
    print(PreguntasRespondidas.pregunta.all())
    assert crate_pregunta.pregunta
"""