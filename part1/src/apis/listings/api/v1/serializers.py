from rest_framework import serializers

from django.contrib.gis.geos import fromstr

from apis.listings.models import Listing, Location, ListingPhoto


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['street', 'suburb', 'city', 'state', 'zipcode', 'point']


class ListingSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Listing
        fields = [
                    'id', 'baths', 'beds', 'size', 'price',
                    'location', 'slug', 'listing_type', 'description',
                    'created_at'
                ]

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location_data['point'] = self._get_point(location_data['point'])

        listing = Listing.objects.create(**validated_data)
        Location.objects.create(listing=listing, **location_data)

        return listing

    def to_representation(self, instance):
         data = super(ListingSerializer, self).to_representation(instance)

         return {
            "listing": data
            }

    def _get_point(self, data):
        longitude, latitude = data.split(',')
        return fromstr(f'POINT({longitude} {latitude})')

class ListingPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListingPhoto
        fields = ['id', 'image', 'type', 'listing']

    def to_representation(self, instance):
         data = super(ListingPhotoSerializer, self).to_representation(instance)

         return {
            "photos": data
            }
