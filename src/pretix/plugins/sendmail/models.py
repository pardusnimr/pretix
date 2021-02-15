from django.db import models
from django.urls import reverse
from django_scopes import ScopedManager
from i18nfield.fields import I18nCharField, I18nTextField

from pretix.base.models import Event, SubEvent, OrderPosition, Item


class ScheduledMail(models.Model):
    rule = models.ForeignKey("Rule", on_delete=models.CASCADE)
    subevent = models.ForeignKey(SubEvent, null=True, on_delete=models.CASCADE)

    sent = models.BooleanField(default=False)


class Rule(models.Model):
    # written with far too much mate and far too little energy.

    # todo: consider using a slug instead of pk in the urls

    CUSTOMERS = "customers"
    ATTENDEES = "attendees"

    SEND_TO_CHOICES = [
        (CUSTOMERS, "Customers"),
        (ATTENDEES, "Attendees"),
    ]

    AFTER = "after"
    BEFORE = "before"

    OFFSET_CHOICES = [
        (AFTER, "After"),
        (BEFORE, "Before"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    subevent = models.ManyToManyField(SubEvent, through=ScheduledMail)

    subject = I18nCharField(max_length=255)
    template = I18nTextField()

    # all products or limit products
    all_products = models.BooleanField(default=True, blank=True)
    limit_products = models.ManyToManyField(Item, blank=True)

    include_pending = models.BooleanField(default=False, blank=True)

    # either send_date or send_offset_* have to be set
    send_date = models.DateTimeField(null=True, blank=True)
    send_offset_days = models.IntegerField(null=True, blank=True)
    send_offset_time = models.TimeField(null=True, blank=True)

    date_is_absolute = models.BooleanField(default=True, blank=True)
    offset_to_event_end = models.BooleanField(default=False, blank=True)
    offset_is_after = models.BooleanField(default=False, blank=True)

    send_to = models.CharField(max_length=10, choices=SEND_TO_CHOICES)

    objects = ScopedManager(event='event')

    def get_absolute_url(self):  # TODO: figure out why the fuck this isn't doing anything
        return reverse('plugins:sendmail:updaterule', kwargs={
            'organizer': self.event.organizer.slug,
            'event': self.event.event.slug,
            'rule': self.pk,
        })
