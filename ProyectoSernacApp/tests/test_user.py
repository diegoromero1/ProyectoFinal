import pytest
from faker import Faker
from ddf import G
from django.test import TestCase, Client
from ProyectoSernacApp.models import Usuario
from ProyectoSernacApp.tests.custom_faker_providers import EmailProvider

fake = Faker()


fake.add_provider(EmailProvider)


@pytest.fixture
def user_creation():
    return Usuario(
        username='cualquiera',
        email=fake.email(),
        password='12345',
        nombres=fake.name(),
        is_staff=False

    )


@pytest.mark.django_db
def test_common_user_creation2(user_creation):
    user_creation.save()
    assert user_creation.username == 'cualquiera'


@pytest.fixture
def user_creation3():
    return G(Usuario)


@pytest.mark.django_db
def test_common_user_creation3(user_creation3):
    print(user_creation3.nombres)
    user_creation3.is_staff = False
    user_creation3.save()
    assert user_creation3.is_staff == False


@pytest.mark.django_db
def test_common_user_creation():
    user = Usuario.objects.create_user(
        username='usertest',
        email='usertest@gmal.com',
        password='12345',
        nombres='usertest',
        is_staff=False

    )
    assert user.username == 'usertest'


@pytest.mark.django_db
def test_superuser_creation():
    user = Usuario.objects.create_superuser(
        username='usertest',
        email='usertest@gmal.com',
        password='12345',
        nombres='usertest',

    )
    assert user.is_superuser


@pytest.mark.django_db
def test_staff_user_creation():
    user = Usuario.objects.create_user(
        username='usertest',
        email='usertest@gmal.com',
        password='12345',
        nombres='usertest',
        is_staff=True

    )
    assert user.is_staff


@pytest.mark.django_db
def test_user_creation_fail():
    with pytest.raises(Exception):
        Usuario.objects.create_user(
            email='usertest@gmal.com',
            password='12345',
            is_staff=False
     )


class UsuarioMoldelTest(TestCase):
    def setUp(self):
        Usuario.objects.create_user(username='diego',
                                    email= fake.email(),nombres='diego',
                                    password='12345',is_staff=False)

    def test_common_user_creation(self):
        usuario = Usuario.objects.get(id=1)
        field_label = Usuario._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')






