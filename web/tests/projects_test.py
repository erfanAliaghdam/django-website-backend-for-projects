from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from web.models import RequestItem, Project, RequestedProjects
from model_bakery import baker
import pytest
user_obj = get_user_model()

@pytest.mark.django_db()
class TestCreateProject:
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        response = client.post('/api/projects/', {'title': 'test', 'description': 'test', 'tag': 4})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_an_mentor_return_401(self):
        client   = APIClient()
        client.force_authenticate(user = user_obj(is_mentor = False))
        response = client.post('/api/projects/', {'title': 'test', 'description': 'test', 'tag': 4})
        print(response)
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db()
class TestRequestProject:
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        response = client.post('/api/request/', {'project_id': 9})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_can_destroy_approved_request_returns_401(self):
        client   = APIClient()
        user     = baker.make(user_obj, is_mentor = False)
        client.force_authenticate(user = user)
        request  = baker.make(RequestItem, status = RequestItem.APPROVE, parent = user.requested_projects)
        response = client.delete('/api/request/{}/'.format(request.id))
        assert response.status_code == status.HTTP_403_FORBIDDEN
  