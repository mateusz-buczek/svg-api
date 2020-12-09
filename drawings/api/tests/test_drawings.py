from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drawings.drawings.models import Body, Geometry


class BodyAndGeometryCreateTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:projection')
        self.data = {}

    def test_create_with_no_data(self):
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)

    def test_create_with_correct_data(self):
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)
        self.data = {
            "geometry": [
                {"x1": -207, "x2": -332, "y1": 9, "y2": 191, "z1": 0, "z2": 18},
                {"x1": -207, "x2": -332, "y1": 209, "y2": 391, "z1": 0, "z2": 18},
                {"x1": 207, "x2": 332, "y1": 9, "y2": 191, "z1": 0, "z2": 18},
                {"x1": 207, "x2": 332, "y1": 209, "y2": 391, "z1": 0, "z2": 18},
                {"x1": -8, "x2": 10, "y1": 9, "y2": 191, "z1": 0, "z2": 320},
                {"x1": -8, "x2": 10, "y1": 209, "y2": 391, "z1": 0, "z2": 320},
                {"x1": -350, "x2": -332, "y1": 9, "y2": 191, "z1": 0, "z2": 320},
                {"x1": -350, "x2": -332, "y1": 209, "y2": 391, "z1": 0, "z2": 320},
                {"x1": 332, "x2": 350, "y1": 9, "y2": 191, "z1": 0, "z2": 320},
                {"x1": 332, "x2": 350, "y1": 209, "y2": 391, "z1": 0, "z2": 320},
                {"x1": -350, "x2": 350, "y1": 391, "y2": 409, "z1": 0, "z2": 320},
                {"x1": -350, "x2": 350, "y1": 191, "y2": 209, "z1": 0, "z2": 320},
                {"x1": -350, "x2": 350, "y1": -9, "y2": 9, "z1": 0, "z2": 320}
            ],
            "projection_plane": "XY"
        }

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content_type, 'image/svg+xml')
        self.assertEqual(Body.objects.all().count(), 1)
        self.assertEqual(Geometry.objects.all().count(), 13)

    def test_create_with_incomplete_geometry_data(self):
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)
        self.data = {
            "geometry": [
                {"x2": -332, "y1": 9, "y2": 191, "z1": 0, "z2": 18},
            ],
            "projection_plane": "XY"
        }

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)

    def test_create_without_projection_plane_data(self):
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)
        self.data = {
            "geometry": [
                {"x1": 332, "x2": 350, "y1": 209, "y2": 391, "z1": 0, "z2": 320},
            ],

        }

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)

    def test_create_with_disallowed_projection_plane_data(self):
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)
        projection_plane = 'ZX'
        self.assertTrue(projection_plane not in settings.ALLOWED_PLANES)
        self.data = {
            "geometry": [
                {"x1": 332, "x2": 350, "y1": 209, "y2": 391, "z1": 0, "z2": 320},
            ],
            "projection_plane": projection_plane
        }

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(Body.objects.all().count(), 0)
        self.assertEqual(Geometry.objects.all().count(), 0)
