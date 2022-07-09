from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from model_bakery import baker
from django.conf import settings
import pytest

@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        'ENGINE'     : settings.DATABASES['default']['ENGINE'],
        'NAME'       : settings.DATABASES['default']['NAME'],
        'USER'       : settings.DATABASES['default']['USER'],
        'PASSWORD'   : settings.DATABASES['default']['PASSWORD'],
        'HOST'       : settings.DATABASES['default']['HOST'],
        'PORT'       : settings.DATABASES['default']['PORT'],
    }

@pytest.mark.django_db()
class TestCreateProject:
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        response = client.post('/api/projects/', {'title': 'tfest', 'description': 'test', 'tag': 4, 'admissionNo':1})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_an_mentor_return_403(self):
        user_obj = get_user_model()
        client   = APIClient()
        client.force_authenticate(user = user_obj(is_mentor = False))
        response = client.post('/api/projects/', {'title': 'test', 'description': 'test', 'tag': 4,  'admissionNo':1})
        assert response.status_code == status.HTTP_403_FORBIDDEN

