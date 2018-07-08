# -*- coding: utf-8 -*-

from concertina.player import _
from concertina.player.interfaces import IConcertinaPlayerSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm


class IConcertinaPlayerSettingsForm(RegistryEditForm):
    schema = IConcertinaPlayerSettings
    label = _(u'ConcertinaPlayer settings')
    description = _(u'Concertina Player Settings Description')

    """
    def updateFields(self):
        super(IIuemAgreementsSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(IIuemAgreementsSettingsForm, self).updateWidgets()
    """


class IMareetradTraderSettingsFormControlPanel(ControlPanelFormWrapper):
    form = IConcertinaPlayerSettingsForm
