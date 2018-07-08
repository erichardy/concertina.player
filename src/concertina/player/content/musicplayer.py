# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from concertina.player import _
from dexterity.membrane.behavior.user import INameFromFullName
from dexterity.membrane.content.member import IEmail
from plone import api
from plone.autoform import directives as form
from plone.dexterity.browser import add
from plone.dexterity.content import Container
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
# from plone.namedfile import field as namedfile
# from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from z3c.form import button
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import implementer

import logging


logger = logging.getLogger('collective.player:musicplayer')


class IMusicPlayerNameFromFullName(INameFromFullName):
    """
    """


class IMusicPlayer(IEmail):
    """ Marker interface and Dexterity Python Schema for Player
    """
    pseudo = schema.TextLine(
        title=_(u'your pseudo'),
        description=_(u'pseudo_description'),
        required=True,
    )

    first_name = schema.TextLine(
        title=_(u'First Name'),
        required=True,
    )

    last_name = schema.TextLine(
        title=_(u'Last Name'),
        required=True,
    )
    phone = schema.TextLine(
        title=_(u'plone number'),
        description=_(u'phone_description'),
        required=False,
    )
    mobile = schema.TextLine(
        title=_(u'mobile number'),
        description=_(u'mobile_description'),
        required=False,
    )
    instrument = schema.Choice(
        title=_(u'instrument played'),
        description=_(u'you can choose "Other"'),
        source='player.instruments',
        default=u'',
        required=True,
        )
    music = schema.Choice(
        title=_(u'music played'),
        description=_(u'you can choose "Other"'),
        source='player.musics',
        default=u'',
        required=True,
        )

    """
    a ajouter:
    adresse
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
    """
    coordonnees : context.geolocation.latitude , context.geolocation.longitude
    """
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
    3 workflow states for a musicplayer : 'pending', 'enabled', 'disabled'
    """


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
        with api.env.adopt_roles(['Manager']):
            data, errors = self.extractData()
            if errors:
                self.status = _('Please correct errors')
                return
            obj = self.createAndAdd(data)
            uuid = api.content.get_uuid(obj=obj)
            # context is now the musicplayers folder
            # repo = obj.__of__(self.context)
            url = portal.absolute_url()
            url += '/@@thanks_musicplayer_view?uuid=' + uuid
            # url = addTokenToUrl(url)
            # import pdb;pdb.set_trace()
            self.request.response.redirect(url)

    @button.buttonAndHandler(_(u'Cancel subscription'))
    def handleCancel(self, action):
        data, errors = self.extractData()
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


class AddView(add.DefaultAddView):
    form = AddForm
