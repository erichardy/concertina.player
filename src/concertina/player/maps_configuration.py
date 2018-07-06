# -*- coding: utf-8 -*-

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


@implementer(ImapConfiguration)
class mapConfiguration(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.default_loc = (48.5071371897, -4.60468769073)

    @property
    def default_location(self):
        """
        https://github.com/sithmel/Products.Maps/blob/master/\
        Products/Maps/browser/config.py
        """
        logger.info('dans maps config !!!')
        return self.default_loc
