import uuid

from django.db import models
from django.contrib.gis.db import models
from djmoney.models.fields import MoneyField
from moneyed import MXN, Money
from django.utils.translation import ugettext_lazy as _

from .choices import (
    LISTING_STATUS,
    LISTING_TYPES,
    PHOTO_TYPES
)

class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    baths = models.PositiveIntegerField(
        _('Bathrooms'),
        default=0,
        null=True,
        blank=True
    )

    beds = models.PositiveIntegerField(
        _('Bedrooms'),
        default=0,
        null=True,
        blank=True
    )

    size = models.PositiveIntegerField(
        _('Size(m2)'),
        default=0,
        null=True,
        blank=True
    )

    price = MoneyField(
        default=Money(0, MXN),
        max_digits=12,
        decimal_places=2,
        verbose_name=_('Price')
    )

    location = models.OneToOneField(
        'Location',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Location')
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name=_('Slug')
    )

    listing_type = models.CharField(
        max_length=30,
        choices=LISTING_TYPES,
        verbose_name=_('Listing Type')
    )

    description = models.CharField(
        max_length=355,
        blank=True,
        null=True,
        verbose_name=_('Description')
    )

    status = models.CharField(
        max_length=10,
        choices=LISTING_STATUS,
        null=True,
        verbose_name=_('Status')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ListingPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(
        'Listing',
        on_delete=models.CASCADE
    )
    name = models.CharField(_('Name'), max_length=60)
    image = models.ImageField(_('Image'), upload_to='listing/')
    type = models.CharField(
        max_length=30,
        choices=PHOTO_TYPES,
        verbose_name=_('Photo Type')
    )
    order = models.PositiveSmallIntegerField(_('Order'), default=99, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street = models.CharField(_('Street'), max_length=200)
    suburb = models.CharField(_('Suburb'), max_length=200)
    city = models.CharField(_('City'), max_length=100)
    state = models.CharField(_('State'), max_length=100)
    zipcode = models.CharField(_('Zipcode'), max_length=20)
    point = models.PointField(_('Coordinate'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
