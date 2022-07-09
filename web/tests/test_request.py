from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from web.models import RequestItem, Project
from model_bakery import baker
from django.conf import settings
import pytest

user_obj = get_user_model()

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
@pytest.mark.django_db
class TestRequestProject:
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        user     = baker.make(user_obj, is_mentor = True)
        proj     = baker.make(Project, admissionNo = 0, user=user, is_active = True)
        response = client.post('/api/request/', {'project_id': proj.id})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_can_destroy_approved_request_returns_401(self):
        user_obj = get_user_model()
        client   = APIClient()
        user     = baker.make(user_obj, is_mentor = False)
        client.force_authenticate(user = user)
        request  = baker.make(RequestItem, status = RequestItem.APPROVE, parent = user.requested_projects)
        response = client.delete('/api/request/{}/'.format(request.id))
        assert response.status_code == status.HTTP_403_FORBIDDEN
  
    def test_if_can_request_to_full_projects_returns_406(self):
        user_obj = get_user_model()
        client   = APIClient()
        user     = baker.make(user_obj, is_mentor = True)
        user2    = baker.make(user_obj, is_mentor = False)
        user2.profile_stud.is_verified = True
        user.profile_mentor.is_verified = True
        proj     = baker.make(Project, admissionNo = 0, user=user, is_active = True)
        client.force_authenticate(user = user2)
        response = client.post('/api/request/', {'project_id': proj.id})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
