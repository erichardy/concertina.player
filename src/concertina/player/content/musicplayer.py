# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from concertina.player import _
from dexterity.membrane.behavior.user import INameFromFullName
from dexterity.membrane.content.member import IEmail
from plone.dexterity.browser import add
from plone.dexterity.content import Container
from plone import api
from plone.autoform import directives as form
# from plone.namedfile import field as namedfile
# from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from z3c.form import button
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import implementer
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import (
    newSecurityManager, setSecurityManager)
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import logging


logger = logging.getLogger('collective.player:musicplayer')


class IMusicPlayerNameFromFullName(INameFromFullName):
    """
    """


class IMusicPlayer(IEmail):
    """ Marker interface and Dexterity Python Schema for Player
    """
    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=True,
    )

    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=True,
    )
    """
    a ajouter:
    pseudo
    adresse
    tel fixe
    tel mobile
    site web perso
    Choix d'afficher les info perso aux autres musiciens ?
    liens social : facebook, twiter, google+, etc...
    """
    form.omitted('register_date')
    form.no_omit(IEditForm, 'register_date',)
    register_date = schema.Datetime(
        title=_(u'registring date'),
        required=False,
        # defaultFactory=registerDate
        )

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IMusicPlayer)
class MusicPlayer(Container):
    """
    """


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return 'AnonymousMusicplayer'


class AddForm(add.DefaultAddForm):
    portal_type = 'musicplayer'
    ignoreContext = True
    label = _(u'Subscribe as a music player on this site !')
    template = ViewPageTemplateFile('musicplayer_add_view.pt')

    def update(self):
        super(add.DefaultAddForm, self).update()

    def updateWidgets(self):
        super(add.DefaultAddForm, self).updateWidgets()

    @button.buttonAndHandler(_(u'Subscribe'), name='subscribe')
    def handleApply(self, action):
        portal = api.portal.get()
        sm = getSecurityManager()
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return
        try:
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', ['Manager'], '')
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)
            obj = self.createAndAdd(data)
            uuid = api.content.get_uuid(obj=obj)
            # context is now the musicplayers folder
            # repo = obj.__of__(self.context)
            url = portal.absolute_url()
            url += '/@@thanks_trader_view?uuid=' + uuid
            # url = addTokenToUrl(url)
            # import pdb;pdb.set_trace()
            self.request.response.redirect(url)
        finally:
            # Restore the old security manager
            setSecurityManager(sm)

    @button.buttonAndHandler(_(u'Cancel subscription'))
    def handleCancel(self, action):
        data, errors = self.extractData()
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


class AddView(add.DefaultAddView):
    form = AddForm
