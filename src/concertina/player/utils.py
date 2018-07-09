# -*- coding: utf-8 -*-

from concertina.player import _
from plone import api
from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from zope.interface import Invalid
from zope.publisher.browser import BrowserView

import logging
import re


logger = logging.getLogger('concertina.player:utils')
checkEmail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}').match


def normalize(value):
    normalizer = getUtility(INormalizer)
    return normalizer.normalize(value, locale='fr')


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u'Invalid adress email'))
    return True


def sorted_by_date(trader1, trader2):
    """
    Pour tri, les dates les plus récentes en dernier
    """
    d1 = trader1.register_date
    d2 = trader2.register_date
    if d1 > d2:
        return 1
    if d1 < d2:
        return -1
    return 0


def mareeTradMailActivated(context):
    try:
        type_ok = context.portal_type in ['mareetrad', 'trader']
        if not type_ok:
            return False
    except Exception:
        return False
    if context.portal_type == 'trader':
        context = context.aq_parent
    return context.mails_activated


def publish(obj):
        api.content.transition(obj=obj, transition='publish')


trader1 = {}
trader1['title'] = u'tr1@tr1.tr1'
trader1['pseudo'] = u'tr1 pseudo'
trader1['instrument'] = u'accordéon'
trader1['other_instrument'] = u'Cymballes'
trader1['town'] = u'Brest'
trader1['age'] = 23
trader1['name'] = u'trader1'
trader1['firstname'] = u'fff trader1'
trader1['mobile'] = u'12 23 34 45 56'
trader2 = {}
trader2['title'] = u'tr2@tr2.tr2'
trader2['pseudo'] = u'tr2 pseudo'
trader2['instrument'] = u'tr2 instrument'
trader2['other_instrument'] = u'Cymballes'
trader2['town'] = u'Quimper'
trader2['age'] = 54
trader2['name'] = u'trader2 trader2'
trader2['firstname'] = u'fff trader2'
trader2['mobile'] = u'12 56 54 65 76'

trader3 = {}
trader3['title'] = u'tr3@tr3.tr3'
trader3['pseudo'] = u'tr3 pseudo'
trader3['instrument'] = u'autre'
trader3['other_instrument'] = u'Cymballes'
trader3['town'] = u'Ailleurs'
trader3['age'] = 76
trader3['name'] = u'trader3'
trader3['firstname'] = u'fff trader3'
trader3['mobile'] = u'11 12 22 23 33'

traders = [trader1, trader2, trader3]


class dataSet(BrowserView):

    def __call__(self):
        self.portal = api.portal.get()
        purge = self.request.form.get('purge')
        if purge:
            self.purgeDataSet()
            self.request.response.redirect(self.portal.absolute_url())
            return
        if self.portal.get('maree-trad-2020'):
            logger.info('maree-trad-2020 already exists !!!')
            return
        self.mareetraders = self.createMareeTraders(self.portal)
        publish(self.mareetraders)
        for trader in traders:
            self.createTrader(trader, self.mareetraders)
        self.request.response.redirect(self.mareetraders.absolute_url())

    def createMareeTraders(self, loc):
        return api.content.create(
            container=loc,
            type='mareetraders',
            title=u'Marée Trad 2020',
            mails_activated=False
            )

    def createTrader(self, trader, mareetraders):
        api.content.create(
            container=mareetraders,
            type='trader',
            title=trader['title'],
            pseudo=trader['pseudo'],
            instrument=trader['instrument'],
            other_instrument=trader['other_instrument'],
            town=trader['town'],
            age=trader['age'],
            name=trader['name'],
            firstname=trader['firstname'],
            mobile=trader['mobile'],
            )

    def purgeDataSet(self):
        mt = self.portal.get('maree-trad-2020')
        logger.info(mt)
        api.content.delete(obj=mt)
        try:
            mt = self.portal.get('maree-trad-2020')
            api.content.delete(obj=mt)
        except Exception:
            logger.info('No mareetraders to purge !!!')
            pass
