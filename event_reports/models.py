from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class EventReportPage(Page):
    author = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    date = models.DateField("Post date")
    event_report = StreamField([
        ('event_text_block', blocks.RichTextBlock()),
        ('event_sub_header', blocks.CharBlock()),
        ('event_picture', ImageChooserBlock())
    ])

EventReportPage.content_panels = [
    FieldPanel('author'),
    FieldPanel('date'),
    StreamFieldPanel('event_report'),
]