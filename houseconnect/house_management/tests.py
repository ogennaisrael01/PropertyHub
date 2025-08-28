from rest_framework.test import APITestCase
from house_management.models import House, Unit
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class HouseTestCase(APITestCase):
    def setUp(self):
        """ User setup for creation and authentications"""
        self.user = User.objects.create_user(
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

        # House create 
        self.house = House.objects.create(owner = self.user,
                                        title="Api test title",
                                        description= "APi test content",
                                        price="949494",
                                        location= "london",
                                        house_type= "apartments",
                                        is_available= True,
                                        for_rent= True,
                                        for_sale= True)
        
        self.unit = Unit.objects.create(house=self.house,
                                        unit_number="3744",
                                        bedrooms=48,
                                        bathrooms=20,
                                        living_rooms=12,
                                        rent_amount="0399",
                                        is_available=True

        )

    def test_create_house(self):
        """ API test for creation house objects """
        url = "/houses/"
        data = {
                "title": "Api test title",
                "description": "APi test content",
                "price": "949494",
                "location": "london",
                "house_type": "apartments",
                "is_available": True,
                "for_rent": True,
                "for_sale": True
            }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(House.objects.first().owner, self.user)
        self.assertEqual(House.objects.count(), 2)

    def test_house_listing(self):
        url = "/houses/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_house_update(self):
        url = f"/houses/{self.house.id}/"
        data = {
                "title":"update title",
                "description": "update content",
                "price": "38383",
                "location": "Jos",
                "house_type": "apartments",
                "is_available": True,
                "for_rent": True,
                "for_sale": False
            }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_house(self):

        url = f"/houses/{self.house.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unit_create(self):
        url = f"/houses/{self.house.id}/units/create/"
        data = {
                "unit_number": "Room 5A",
                "bedrooms": 2147483647,
                "bathrooms": 2147483647,
                "living_rooms": 2147483647,
                "rent_amount": "04949494",
                "is_available": True
            }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_house_search(self):
        url = "/houses/"
        data = {
            "search": "london"
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["location"], "london")

    def  test_unit_update(self):
        url = f"/houses/{self.house.id}/units/{self.unit.id}/"
        data = {
            "unit_number": "Room 5A",
            "bedrooms": 2147483647,
            "bathrooms": 2147483647,
            "living_rooms": 2147483647,
            "rent_amount": "04949494",
            "is_available": True
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.house.owner, self.user)

    def test_unit_retrieval(self):
        """ Making sure each individual unit are retrieved accordingly """
        url = f"/houses/{self.house.id}/units/{self.unit.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_house_rental(self):
        """ Api for house renting """
        url = f"/houses/{self.house.id}/rentals/"

        data = {
            "start_date": "2025-08-29",
            "end_date": "2025-09-28",
            "amount": "2929",
            "is_active": True
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rental_retrieval(self):
        url =  "/rentals/my_rentals/"
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unit_rental(self):
        url = f"/houses/{self.house.id}/units/{self.unit.id}/rentals/"
        data = {
            "start_date": "2025-08-29",
            "end_date": "2025-09-28",
            "amount": "4848",
            "is_active": True
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_image_creation(self):
        url = f"/houses/{self.house.id}/images/create/"
        data = {
            "caption": "Image Caption",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.house.owner, self.user)