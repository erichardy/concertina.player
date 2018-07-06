# -*- coding: utf-8 -*-

from concertina.player import _
from plone import api
from zope.interface import Attribute
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.browser import BrowserView
from zope.schema import ASCIILine
from zope.schema import Int

import logging


logger = logging.getLogger('collective.player:maps_configuration')


class IDefaultMapsParams(Interface):
    """
    records registry
    Ars : 46.601071219913514, 2.0026445388793945
    Milizac = 48.469279317167164, -4.5648193359375
    """
    latitude = ASCIILine(
        title=_(u'default latitude'),
        default='46.601071219913514',
        required=True,
        )
    longitude = ASCIILine(
        title=_(u'default longitude'),
        default='2.0026445388793945',
        required=True,
        )
    zoom = Int(
        title=_(u'default zoom'),
        default=7,
        )


class ImapConfiguration(Interface):
    """
    """
    default_location = Attribute('The default coordinates for new locations.')
    zoom = Attribute('The default zoom')


@implementer(ImapConfiguration)
class mapConfiguration(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        xlatitude = api.portal.get_registry_record(
            'latitude',
            interface=IDefaultMapsParams)
        xlongitude = api.portal.get_registry_record(
            'longitude',
            interface=IDefaultMapsParams)
        try:
            latitude = float(xlatitude)
        except Exception:
            latitude = 0.0
        try:
            longitude = float(xlongitude)
        except Exception:
            longitude = 0.0
        self.default_loc = (latitude, longitude)

    @property
    def default_location(self):
        """
        https://github.com/sithmel/Products.Maps/blob/master/\
        Products/Maps/browser/config.py
        """
        logger.info('dans maps config !!!')
        return self.default_loc
