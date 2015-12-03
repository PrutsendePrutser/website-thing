from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from event_reports.blocks import EventReportBlock


class EventReportPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    event_report = StreamField([
        ('report', EventReportBlock()),
    ])

EventReportPage.content_panels = [
    FieldPanel('author'),
    FieldPanel('date'),
    StreamFieldPanel('event_report'),
]