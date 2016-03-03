import logging

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import get_template
from django.utils import translation
from django.utils.translation import ugettext as _
from typing import Any, Dict

from pretix.base.i18n import LazyI18nString
from pretix.base.models import Event

logger = logging.getLogger('pretix.base.mail')


class TolerantDict(dict):

    def __missing__(self, key):
        return key


def mail(email: str, subject: str, template: str,
         context: Dict[str, Any]=None, event: Event=None, locale: str=None):
    """
    Sends out an email to a user.

    :param email: The e-mail this should be sent to.
    :param subject: The e-mail subject. Should be localized.
    :param template: The filename of a template to be used. It will
                     be rendered with the recipient's locale. Alternatively, you
                     can pass a LazyI18nString and ``context`` will be used
                     for a Python .format() call.
    :param context: The context for rendering the template.
    :param event: The event, used for determining the sender of the e-mail
    :param locale: The locale used while rendering the template

    :return: ``False`` on obvious failures, like the user having to e-mail
    address, ``True`` otherwise. ``True`` does not necessarily mean that
    the email has been sent, just that it has been queued by the e-mail
    backend.
    """
    _lng = translation.get_language()
    if locale:
        translation.activate(locale or settings.LANGUAGE_CODE)

    if isinstance(template, LazyI18nString):
        body = str(template)
        if context:
            body = body.format_map(TolerantDict(context))
    else:
        tpl = get_template(template)
        body = tpl.render(context)

    sender = event.settings.get('mail_from') if event else settings.MAIL_FROM

    subject = str(subject)
    if event:
        prefix = event.settings.get('mail_prefix')
        if prefix:
            subject = "[%s] %s" % (prefix, subject)

        body += "\r\n\r\n----\r\n"
        body += _(
            "You are receiving this e-mail because you placed an order for %s." % event.name
        )
        body += "\r\n"
    try:
        return mail_send([email], subject, body, sender, event.id if event else None)
    finally:
        translation.activate(_lng)


def mail_send(to: str, subject: str, body: str, sender: str, event: int=None) -> bool:
    email = EmailMessage(subject, body, sender, to=to)
    if event:
        event = Event.objects.get(id=event)
        backend = event.get_mail_backend()
    else:
        backend = get_connection(fail_silently=False)

    try:
        backend.send_messages([email])
        return True
    except Exception:
        logger.exception('Error sending e-mail')
        return False


if settings.HAS_CELERY and settings.EMAIL_BACKEND != 'django.core.mail.outbox':
    from pretix.celery import app

    mail_send_task = app.task(mail_send)

    def mail_send(*args, **kwargs):
        mail_send_task.apply_async(args=args, kwargs=kwargs)
