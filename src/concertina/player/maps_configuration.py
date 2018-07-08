# -*- coding: utf-8 -*-

from concertina.player.interfaces import IConcertinaPlayerSettings
from plone import api
from zope.interface import Attribute
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.browser import BrowserView

import logging


logger = logging.getLogger('collective.player:maps_configuration')


class ImapConfiguration(Interface):
    """
    """
    default_location = Attribute('The default coordinates for new locations.')
    zoom = Attribute('The default zoom')


@implementer(ImapConfiguration)
class mapConfiguration(BrowserView):
    """
    We need to create here a multi-adapter which is used to configure
    default parameters for the map.
    It misses the zoom configuration....????
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        xlatitude = api.portal.get_registry_record(
            'latitude',
            interface=IConcertinaPlayerSettings)
        xlongitude = api.portal.get_registry_record(
            'longitude',
            interface=IConcertinaPlayerSettings)
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
        # logger.info('dans maps config !!!')
        return self.default_loc
