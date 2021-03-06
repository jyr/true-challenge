from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from apis.listings.models import Listing
from apis.listings.api.v1.serializers import (
    ListingSerializer,
    LocationSerializer,
    ListingPhotoSerializer
)

class ListingEndpoint(APIView):
    """
    post:
    Create a listing
    """

    @swagger_auto_schema(responses={201: ListingSerializer})
    def post(self, request, *args, **kwargs):
        serializer = ListingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            try:
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except:
                raise Http404

        return Response(
                {"error":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


class ListingPhotoEndpoint(APIView):
    """
    post:
    Uploads photos for type by listing
    """

    @swagger_auto_schema(responses={201: ListingPhotoSerializer})
    def post(self, request, *args, **kwargs):
        # TODO: Refactor get an images array

        serializer = ListingPhotoSerializer(data=request.data)

        if serializer.is_valid():
            listing = Listing.objects.get(pk=request.data['listing'])
            serializer.save(listing= listing)

            try:
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except:
                raise Http404

        return Response(
                {"error":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


class ListingDetailEndpoint(APIView):

    def get_object(self, pk):
        try:
            return Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
           raise Http404

    @swagger_auto_schema(responses={200: ListingSerializer})
    def get(self, request, pk, format=None):
        """
        get:
        Retrieve a listing
        """

        instance = self.get_object(pk)
        serializer = ListingSerializer(instance)

        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ListingSerializer})
    def patch(self, request, pk, format=None):
        """
        patch:
        Update a listing.
        """

        instance = self.get_object(pk)
        serializer = ListingSerializer(
            instance,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            try:
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            except:
                raise Http404

        return Response(
                {"error":serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(responses={200: ListingSerializer})
    def delete(self, request, pk, format=None):
        """
        del:
        Delete a listing.
        """
        instance = self.get_object(pk)
        instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
