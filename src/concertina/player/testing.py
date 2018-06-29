# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import concertina.player


class ConcertinaPlayerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=concertina.player)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'concertina.player:default')


CONCERTINA_PLAYER_FIXTURE = ConcertinaPlayerLayer()


CONCERTINA_PLAYER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONCERTINA_PLAYER_FIXTURE,),
    name='ConcertinaPlayerLayer:IntegrationTesting',
)


CONCERTINA_PLAYER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONCERTINA_PLAYER_FIXTURE,),
    name='ConcertinaPlayerLayer:FunctionalTesting',
)


CONCERTINA_PLAYER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CONCERTINA_PLAYER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ConcertinaPlayerLayer:AcceptanceTesting',
)
