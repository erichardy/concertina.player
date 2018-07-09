# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from concertina.player import _
from dexterity.membrane.behavior.user import INameFromFullName
from dexterity.membrane.content.member import IEmail
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.dexterity.browser import add
from plone.dexterity.content import Container
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
# from plone.namedfile import field as namedfile
# from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from z3c.form import button
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import IEditForm
from z3c.form.interfaces import INPUT_MODE
# from plone.z3cform.fieldsets.utils import move
from zope import schema
from zope.componen import adapter
from zope.interface import implementer
from zope.interface import Interface

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

    directives.read_permission(instrument='cmf.ModifyPortalContent')
    directives.write_permission(instrument='cmf.ModifyPortalContent')
    instrument = schema.Choice(
        title=_(u'instrument played'),
        description=_(u'you can choose "Other"'),
        source='player.instruments',
        default=u'',
        required=True,
        )
    directives.read_permission(music='cmf.ModifyPortalContent')
    directives.write_permission(music='cmf.ModifyPortalContent')
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
    directives.omitted('register_date')
    directives.no_omit(IEditForm, 'register_date',)
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


class subscribeForm(AutoExtensibleForm, form.Form):
    """
    https://z3cform.readthedocs.io/en/latest/mustread/form.html#
    """
    schema = IMusicPlayer
    ignoreContext = True
    label = _(u'subscribe form')
    description = _(u'This form is used for subscriptions')
    template = ViewPageTemplateFile('subscribeView.pt')

    def update(self):
        self.request.set('disable_border', True)
        super(subscribeForm, self).update()

    def updateWidgets(self):
        super(form.Form, self).updateWidgets()
        self.widgets['instrument'].mode = HIDDEN_MODE
        self.widgets['music'].mode = HIDDEN_MODE

    @button.buttonAndHandler(_(u'Subscribe'), name='subscribe')
    def handleApply(self, action):
        # portal = api.portal.get()
        with api.env.adopt_roles(['Manager']):
            data, errors = self.extractData()
            if errors:
                self.status = _('Please correct errors')
                return
            """
            obj = self.createAndAdd(data)
            uuid = api.content.get_uuid(obj=obj)
            # context is now the musicplayers folder
            url = portal.absolute_url()
            url += '/@@thanks_musicplayer_view?uuid=' + uuid
            # url = addTokenToUrl(url)
            # import pdb;pdb.set_trace()
            self.request.response.redirect(url)
            """
            logger.info(data)

    @button.buttonAndHandler(_(u'Cancel subscription'))
    def handleCancel(self, action):
        data, errors = self.extractData()
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


@implementer(IMusicPlayer)
@adapter(Interface)
class QueryFormAdapter(object):

    def __init__(self, context):
        self.email = None
        self.pseudo = None
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.mobile = None
        self.instrument = None
        self.music = None


class SubscribeView(add.DefaultAddView):
    form = subscribeForm


class AddForm(add.DefaultAddForm):
    portal_type = 'musicplayer'
    ignoreContext = True
    label = _(u'Subscribe as a music player on this site !')
    template = ViewPageTemplateFile('musicplayer_add_view.pt')

    def _getWidgetInGroups(self, f):
        """
        :param f: le champ recherché
        :type f: str
        :returns: le champ (objet ``field``) recherché dans les groupes
            ou ``False`` si non trouvé
        """
        for group in self.groups:
            w = group.widgets.get(f)
            if w is not None:
                return w
        return False

    def update(self):
        """
        C'est le bazard !
        Il vaut mieux faire une template "spéciale" pour l'inscription...
        et une autre "spéciale" pour que chaque inscrit puisse compléter
        ses données perso...
        """
        super(add.DefaultAddForm, self).update()
        # move(self, 'music', before='*')
        # move(self, 'music', after='email')
        logger.info('in update')
        # print dir(self.groups)
        logger.info(self.fields.keys())
        fi = self._getWidgetInGroups('IAltTexts.display_one')
        logger.info(fi)
        fi.mode = HIDDEN_MODE
        email = self.widgets.get('email')
        email.mode = HIDDEN_MODE
        for w in self.widgets.keys():
            wi = self.widgets.get(w)
            wi.mode = HIDDEN_MODE
        email = self.widgets.get('email')
        email.mode = INPUT_MODE
        geo = self.widgets.get('IGeolocatable.geolocation')
        geo.mode = INPUT_MODE

        for group in self.groups:
            for w in group.widgets.keys():
                wi = group.widgets.get(w)
                wi.mode = HIDDEN_MODE
        # import pdb;pdb.set_trace()
        # if not api.user.is_anonymous():
        # super(AddForm, self).update()
        # super(add.DefaultAddForm, self).update()

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


"""
(Pdb) self.groups[0].widgets.keys()
['ICategorization.subjects', 'ICategorization.language']
(Pdb) self.groups[1].widgets.keys()
['IPublication.effective', 'IPublication.expires']
(Pdb) self.groups[2].widgets.keys()
['IOwnership.creators', 'IOwnership.contributors', 'IOwnership.rights']
(Pdb) self.groups[3].widgets.keys()
['IProvidePasswords.password', 'IProvidePasswords.confirm_password']
(Pdb) self.groups[4].widgets.keys()
['IThumbnail.thumbnail', 'IThumbnail.use_thumb_default', 'IThumbnail.use_\
thumb_default_sizes', 'IThumbnail.thumb_width', 'IThumbnail.thumb_height']
(Pdb) self.groups[5].widgets.keys()
['IAltTexts.display_one', 'IAltTexts.label_one', 'IAltTexts.presentation_one',\
 'IAltTexts.display_two', 'IAltTexts.label_two', 'IAltTexts.presentation_two']
(Pdb) self.groups[6].widgets.keys()
*** IndexError: tuple index out of range

(Pdb) self.schema.names
<bound method SchemaClass.names of <SchemaClass concertina.player.content.\
musicplayer.IMusicPlayer>>
(Pdb) self.schema.names()
['last_name', 'instrument', 'mobile', 'pseudo', 'first_name', 'register_date',\
 'phone', 'music']

"""
