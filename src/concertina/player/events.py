# -*- coding: utf-8 -*-

# from plone import api
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import INormalizer

import datetime
import logging


logger = logging.getLogger('collective.player:musicplayer_events')


class setMusicplayerRegistrationDate():

    def __init__(self, context, event):
        context.register_date = datetime.datetime.today()
        context.reindexObject()


class sendNotification():
    """
    Send notification to site admin
    """
    def __init__(self, context, event):
        logger.info(u'notification sent to site admin')


class sendConfirmation():
    """
    Send confirmation to subscriber
    """
    def __init__(self, context, event):
        logger.info(u'Confirmation sent to subscriber')
