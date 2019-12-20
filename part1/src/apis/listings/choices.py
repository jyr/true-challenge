from django.utils.translation import ugettext_lazy as _

LISTING_STATUS = (
    ('rejected', _('Rejected')),
    ('accepted', _('Accepted'))
)


LISTING_TYPES = (
    ('house', _('Houses')),
    ('apartment', _('Apartments')),
    ('development', _('Development')),
    ('land', _('Lands')),
)

PHOTO_TYPES = (
    ('facade',_('Facade')),
    ('interior',_('Interior')),
    ('baths',_('Bathrooms')),
    ('beds',_('Bedrooms')),
    ('kitchen',_('kitchen')),
)
