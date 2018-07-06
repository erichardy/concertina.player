# -*- coding: utf-8 -*-

# from zope.interface import alsoProvides
# from plone.protect.interfaces import IDisableCSRFProtection
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from plone.protect import CheckAuthenticator
# from plone.protect import protect
from plone import api
from plone.app.uuid.utils import uuidToObject
from Products.CMFPlone.utils import safe_unicode
from zope.publisher.browser import BrowserView

# from mareetrad.trader.utils import mareeTradMailActivated
import logging


logger = logging.getLogger('concertina.player:Thanks: ')


for_trader_txt = u"""
<h2>Vous venez de vous inscrire pour la Marée Trad 2018</h2>
<p>Vous avez saisi les éléments ci-dessous :</p>
<p>_trader_description_</p>
<p>Vous serez averti de la suite des événements plus tard</p>
<p> </p>
"""


class thanksMusicplayerView(BrowserView):

    def getMusicplayer(self):
        # alsoProvides(self.request, IDisableCSRFProtection)
        with api.env.adopt_roles(['Manager']):
            self.musicplayer = {}
            # logger.info(self.request.form)
            uuid = self.request.get('uuid')
            obj = uuidToObject(uuid)
            # logger.info(obj.getId())
            self.musicplayer = {}
            self.musicplayer['email'] = obj.email
            self.musicplayer['last_name'] = obj.last_name
            self.musicplayer['firstname'] = obj.first_name
            self.musicplayer['pseudo'] = obj.pseudo
            self.musicplayer['phone'] = obj.mobile
            self.musicplayer['mobile'] = obj.mobile
            self.musicplayer['reg_date'] = obj.register_date.strftime(
                '%d/%m/%Y %H:%M'
                )
            self.musicplayer['mails_activated'] = obj.aq_parent.mails_activated
            self.musicplayer['sender'] = obj.aq_parent.sender_registration
            send_notification = obj.aq_parent.send_notification
            self.musicplayer['send_notification'] = send_notification
            mail_notification = obj.aq_parent.mail_notification
            self.musicplayer['mail_notification'] = mail_notification
            self.musicplayer['html'] = obj.aq_parent.for_traders

        return self.musicplayer

    def getHTMLContent(self, musicplayer):
        """
        TOTO: prendre le texte à envoyer du dossier parent : mareetrad
        """
        # import pdb;pdb.set_trace()
        raw = musicplayer['html'].output

        content = u'Nom: ' + musicplayer['last_name'] + u'<br />'
        content += u'Prénom: ' + musicplayer['firstname'] + u'<br />'
        content += u'email: ' + musicplayer['email'] + u'<br />'
        content += u'Pseudo: ' + musicplayer['pseudo'] + u'<br />'
        # content += u'Tel: ' + musicplayer['mobile'] + u'<br />'
        content += u'<br /><br />'
        content += u'Inscription réalisée le : '
        content += musicplayer['reg_date'] + u'<br />'
        raw = raw.replace(
            u'_trader_description_', content
            )
        return raw

    def sendToMusicplayer(
            self, mails_activated, htmlContent, recipient, sender
            ):
        if not mails_activated:
            return
        message = MIMEMultipart()
        part = MIMEText(safe_unicode(htmlContent), u'html', _charset='utf-8')
        message.attach(part)
        subject = u'[Concertina.fr] Votre inscription au site'
        try:
            api.portal.send_email(sender,
                                  recipient=recipient,
                                  subject=subject,
                                  body=message)
        except Exception:
            logger.info('Error : mail to ' +
                        recipient + ' Failed !')

    def sendNotification(self,
                         send_notification,
                         htmlContent,
                         recipient,
                         sender):
        if not send_notification:
            return
        message = MIMEMultipart()
        messageContent = u'<h3>Une nouvelle inscription'
        messageContent += u' au site concertina.fr :</h3>'
        messageContent += u'<br />'
        messageContent += htmlContent
        part = MIMEText(
            safe_unicode(messageContent),
            u'html',
            _charset='utf-8')
        message.attach(part)
        subject = u'[Concertina.fr] Nouvelle inscription...'
        try:
            api.portal.send_email(sender,
                                  recipient=recipient,
                                  subject=subject,
                                  body=message)
        except Exception:
            logger.info('Error : mail to ' +
                        recipient + ' Failed !')
