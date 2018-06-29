# -*- coding: utf-8 -*-
from concertina.player.content.player import IPlayer  # NOQA E501
from concertina.player.testing import CONCERTINA_PLAYER_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class PlayerIntegrationTest(unittest.TestCase):

    layer = CONCERTINA_PLAYER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_player_schema(self):
        fti = queryUtility(IDexterityFTI, name='player')
        schema = fti.lookupSchema()
        self.assertEqual(IPlayer, schema)

    def test_ct_player_fti(self):
        fti = queryUtility(IDexterityFTI, name='player')
        self.assertTrue(fti)

    def test_ct_player_factory(self):
        fti = queryUtility(IDexterityFTI, name='player')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IPlayer.providedBy(obj),
            u'IPlayer not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_player_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='player',
            id='player',
        )

        self.assertTrue(
            IPlayer.providedBy(obj),
            u'IPlayer not provided by {0}!'.format(
                obj.id,
            ),
        )
