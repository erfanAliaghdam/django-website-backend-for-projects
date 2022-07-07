from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from web.models import RequestItem, Project
from model_bakery import baker
import pytest
user_obj = get_user_model()

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
  
    def test_if_can_request_to_full_projects_returns_406(self):
        client   = APIClient()
        user     = baker.make(user_obj, is_mentor = True)
        user2    = baker.make(user_obj, is_mentor = False)
        user2.profile_stud.is_verified = True
        user.profile_mentor.is_verified = True
        proj     = baker.make(Project, admissionNo = 0, user=user, is_active = True)
        print(proj.id)
        client.force_authenticate(user = user2)
        response = client.post('/api/request/', {'project_id': proj.id})
        print(response.__dict__)
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
