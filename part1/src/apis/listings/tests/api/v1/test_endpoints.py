import tempfile
import shutil
import os

from PIL import Image

from django.urls import reverse
from django.core.files import File
from django.contrib.gis.geos import fromstr

from rest_framework.test import APITestCase
from rest_framework import status

from apis.listings.models import Location, ListingPhoto, Listing

def _test_create_image():
    image = Image.new('RGB', (100, 100))

    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)

    return tmp_file

def _cleanup(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

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
            "image": [_test_create_image()],
            "type": "facade"
        }

        url = reverse(
            'api_v1_listings:create_listing_photo',
        )

        response = self.client.post(url, data, format='multipart')
        photo = ListingPhoto.objects.get(id=response.data['photos']['id'])

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('photos' in response.data)
        _cleanup(os.path.dirname(photo.image.path))


class ListingDetailEndpointTest(APITestCase):

    def setUp(self):
        self.location = Location.objects.create(
            street="Yautepec, Condesa",
            suburb="Condesa",
            city="Cuauhtémoc",
            state="Ciudad de México",
            zipcode="06140",
            point=fromstr(f'POINT({19.4125748} {-99.1795313})')
        )

        self.listing = Listing.objects.create(
            baths=1,
            beds=1,
            size=250,
            price=1000000,
            location=self.location
        )

        self.listing_photo = ListingPhoto.objects.create(
            listing=self.listing,
            type='facade'
        )
        self.listing_photo.image.save('my_home.jpg', _test_create_image())

        self.url = reverse(
            'api_v1_listings:retrieve_listing',
            kwargs={'pk': self.listing.id}
        )

    def test_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('listing' in response.data)
        self.assertTrue('location' in response.data['listing'])
        self.assertEqual(type(response.data['listing']['location']).__name__, 'OrderedDict')
        self.assertTrue('photos' in response.data['listing'])
        _cleanup(os.path.dirname(self.listing_photo.image.path))

    def test_patch(self):
        data = {
            "baths": 2,
            "beds": 5,
            "size": 150,
            "price": 1100000,
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            type(response.data['listing']).__name__, 'OrderedDict')
        self.assertEqual(response.data['listing']['baths'], 2)
        self.assertEqual(response.data['listing']['beds'], 5)
        self.assertEqual(response.data['listing']['price'], "1100000.00")

    def test_delete(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
