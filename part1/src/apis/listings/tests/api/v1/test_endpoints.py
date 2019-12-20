import tempfile
import shutil
import os

from PIL import Image

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from apis.listings.models import Location, ListingPhoto

class ListingEndpointTest(APITestCase):

    def setUp(self):
        self.url = reverse('api_v1_listings:list_create_listing')


    def test_post(self):
        data = {
            "baths": 1,
            "beds": 1,
            "size": 250,
            "price": 1000000,
            "description": "Exclusiva Casa Totalmente remodelada en venta, \
                            ubicada en la calle Yautepec de la prestigiosa \
                            Colonia Condesa, que conserva el estilo más puro  \
                            “Art Decó” que caracteriza a la Colonia.",
            "listing_type": "house",
            "slug": "bla",
            "location": {
                "street":"Yautepec, Condesa",
                "suburb":"Condesa",
                "city":"Cuauhtémoc",
                "state":"Ciudad de México",
                "zipcode":"06140",
                "point":"19.4125748,-99.1795313"
            }
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('listing' in response.data)

        data = {
            "listing": response.data['listing']['id'],
            "image": [self._test_create_image()],
            "type": "facade"
        }

        url = reverse(
            'api_v1_listings:create_listing_photo',
        )
        
        response = self.client.post(url, data, format='multipart')
        photo = ListingPhoto.objects.get(id=response.data['photos']['id'])

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('photos' in response.data)
        self._cleanup(os.path.dirname(photo.image.path))

    def _test_create_image(self):
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        return tmp_file

    def _cleanup(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
