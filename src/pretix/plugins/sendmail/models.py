from django.db import models
from django.urls import reverse
from i18nfield.fields import I18nCharField, I18nTextField

from pretix.base.models import Event, SubEvent, OrderPosition, Item


class ScheduledMail(models.Model):
    rule = models.ForeignKey("Rule", on_delete=models.CASCADE)
    subevent = models.ForeignKey(SubEvent, null=True, on_delete=models.CASCADE)

    sent = models.BooleanField(default=False)


class Rule(models.Model):
    # written with far too much mate and far too little energy.

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

    subevent = models.ManyToManyField(SubEvent, through=ScheduledMail)

    subject = I18nCharField(max_length=255)
    template = I18nTextField()

    all_products = models.BooleanField(default=True)
    limit_products = models.ManyToManyField(Item, blank=True)
    include_pending = models.BooleanField(default=False, blank=True)

    send_date = models.DateTimeField(null=True, blank=True)
    send_offset = models.DurationField(null=True, blank=True)
    send_offset_days = models.DateField(null=True, blank=True)


    date_is_absolute = models.BooleanField(default=True, blank=True)
    offset_to_event_end = models.BooleanField(default=False)
    offset_is_after = models.BooleanField(default=False)

    send_to = models.CharField(max_length=10, choices=SEND_TO_CHOICES)

    # test_field = models.DateTimeField(blank=True)

    def get_absolute_url(self):
        return reverse('plugins:sendmail:updaterule', kwargs={
            'organizer': self.subevent.organizer.slug,
            'event': self.subevent.event.slug,
            'rule': self.pk,
        })
