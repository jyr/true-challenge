from django.urls import path

from apis.listings.api.v1 import endpoints

urlpatterns = ([
    path(
        route='',
        view=endpoints.ListingEndpoint.as_view(),
        name='list_create_listing'
    ),
    path(
        route='photos',
        view=endpoints.ListingPhotoEndpoint.as_view(),
        name='create_listing_photo'
    ),
    path(
        route='<uuid:pk>',
        view=endpoints.ListingDetailEndpoint.as_view(),
        name='retrieve_listing'
    )
])
