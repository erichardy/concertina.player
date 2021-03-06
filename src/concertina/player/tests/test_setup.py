# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from concertina.player.testing import CONCERTINA_PLAYER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that concertina.player is properly installed."""

    layer = CONCERTINA_PLAYER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if concertina.player is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'concertina.player'))

    def test_browserlayer(self):
        """Test that IConcertinaPlayerLayer is registered."""
        from concertina.player.interfaces import (
            IConcertinaPlayerLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IConcertinaPlayerLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CONCERTINA_PLAYER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['concertina.player'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if concertina.player is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'concertina.player'))

    def test_browserlayer_removed(self):
        """Test that IConcertinaPlayerLayer is removed."""
        from concertina.player.interfaces import \
            IConcertinaPlayerLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IConcertinaPlayerLayer,
            utils.registered_layers())
