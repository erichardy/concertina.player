# -*- coding: utf-8 -*-

# from plone import api
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import INormalizer
import datetime


class setMusicplayerRegistrationDate():

    def __init__(self, context, event):
        context.register_date = datetime.datetime.today()
        context.reindexObject()
