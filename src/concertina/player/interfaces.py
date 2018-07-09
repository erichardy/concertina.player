# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from concertina.player import _
from plone.supermodel import model
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import ASCIILine
from zope.schema import Int
from zope.schema import Text


class IConcertinaPlayerLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


default_instruments = u"""Concertina système Anglo
Concertina système English
Concertina système duet
Concertina système franglo
Concertina autre système
Accordéon diatonique
Accordéon Chromatique
Violon
Alto
Violoncelle
Flute traversière
Flûte à bec
Thin whisle
Guitare
Bodhran
Chant
Mandoline
Bouzouki
Autre
"""
default_music_types = u"""
Musiques traditionnelles Irlandaise
Musiques traditionnelles Bretonne
Musiques traditionnelles Scandinave
Musiques traditionnelles de l'Est
Jazz classique
Jazz moderne
Classique
Baroque
Autre
"""


class IConcertinaPlayerSettings(model.Schema):
    model.fieldset('music',
                   label=_(u'Music'),
                   fields=['instruments',
                           'musics',
                           ])
    instruments = Text(
        title=_(u'list of instruments'),
        description=_(u'one instrument name per line'),
        default=default_instruments,
        required=True,
        )
    musics = Text(
        title=_(u'list of music types'),
        description=_(u'one type name per line'),
        default=default_music_types,
        required=True,
        )

    model.fieldset('geo',
                   label=_(u'maps'),
                   fields=['latitude',
                           'longitude',
                           'zoom']
                   )
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
