from rest_framework.test import APITestCase
from accounts.models import CustomUser
from rest_framework import status
from accounts.models import Profile

class RegistrationTest(APITestCase):
    def test_user_registration(self):
        url = "/accounts/register/"
        data = {
            "email": "israel@example.com", 
            "username": "testisrael",
            "password": "0987poiu",
            "role": "Owner"
            }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(CustomUser.objects.count(), 1)

class ProfileTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="ogenna@example.com", 
            username="ogenna", 
            role="Owner", 
            password="0987poiu"
            )
        login_url = "/accounts/login/"
        data = {
            "email": self.user.email,
            "password": "0987poiu"
        }
        response = self.client.post(login_url, data, format="json")
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create_profile(self):

        url = "/accounts/profile/"
        data = {
            "phone_number": "09494882737",
            "address": "Jos city",
            }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        # print(f"Debug: {self.client._credentials} ")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.count(), 1)

    def test_get_profile(self):
        url = "/accounts/profile/me/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_updating_profile(self):
        profile = Profile.objects.create(user= self.user, phone_number="04949488", address="address")
        url = f"/accounts/profile/{profile.id}/"
        data = {
            "phone_number": "0984743",
            "address": "No 2 jos city"
        }
       
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first().user, self.user)
