# -*- coding: utf-8 -*-

__docformat__ = 'restructuredtext en'
from concertina.player.interfaces import IConcertinaPlayerSettings
from plone import api
from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger('mareetrad.trader/vocabs')


def make_terms(terms, rawLinesStr):
    normalizer = getUtility(INormalizer)
    rawLines = rawLinesStr.split('\n')
    lines = [l for l in rawLines if l.strip('\r').strip(' ')]
    for line in lines:
        key = normalizer.normalize(line, locale='fr')
        label = line
        terms.append(SimpleVocabulary.createTerm(key, str(key), label))
    return terms


def make_voc(terms, linesstr):
    return SimpleVocabulary(make_terms(terms, linesstr))


def make_voc_with_blank(terms, linesstr):
    terms.append(SimpleVocabulary.createTerm(None, '', u''))
    return SimpleVocabulary(make_terms(terms, linesstr))


@implementer(IVocabularyFactory)
class _Instruments(object):

    def __call__(self, context):
        terms = []
        xx_intruments = api.portal.get_registry_record(
                'instruments',
                interface=IConcertinaPlayerSettings)
        return make_voc_with_blank(terms, xx_intruments)


@implementer(IVocabularyFactory)
class _Musics(object):

    def __call__(self, context):
        terms = []
        xx_musics = api.portal.get_registry_record(
                'musics_type',
                interface=IConcertinaPlayerSettings)
        return make_voc_with_blank(terms, xx_musics)


Instruments = _Instruments()
Musics = _Musics()
