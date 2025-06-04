from rest_framework import status
from rest_framework.test import APITestCase

from activity import services
from .factories import create_user, create_target


class ActivityAPITests(APITestCase):
    def setUp(self):
        self.user = create_user()
        target = create_target()
        services.follow_target(user=self.user, target=target)
        self.client.force_authenticate(self.user)
        self.target = target

    def test_list_targets_api(self):
        response = self.client.get('/activity/targets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unseen_count_api(self):
        response = self.client.get('/activity/unseen-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)

    def test_follow_unfollow_api(self):
        other_user = create_user(phone='09120000011')
        url = f'/activity/users/{other_user.id}/targets/{self.target.id}/follow/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        url = f'/activity/users/{other_user.id}/targets/{self.target.id}/unfollow/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_activities_api(self):
        services.create_activity(actor=self.user, verb='did something')
        url = f'/activity/users/{self.user.id}/activities/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_object_activities_api(self):
        other_user = create_user(phone='09120000022')
        services.create_activity(actor=other_user, verb='acted', target=self.user)
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(self.user)
        url = f'/activity/objects/{ct.id}/{self.user.id}/activities/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_followed_targets_api(self):
        url = f'/activity/users/{self.user.id}/targets/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

