from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, StreamFieldPanel,
                                                InlinePanel,)
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from core.models import snippets


class EventReportIndex(Page):
    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    # Returns child pages so we can iterate over them in the template
    def child_pages(self):
        return EventReportPage.objects.live().child_of(self)

    subpage_types = ['EventReportPage', ]


class EventReportPage(Page):
    author = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    date = models.DateField("Post date")
    event_report = StreamField([
        ('event_text_block', blocks.RichTextBlock()),
        ('event_sub_header', blocks.CharBlock()),
        ('event_picture', SnippetChooserBlock(snippets.ImageWithCaptionSnippet))
    ])

    parent_page_types = ['EventReportIndex', ]

EventReportPage.content_panels = [
    FieldPanel('author'),
    FieldPanel('date'),
    StreamFieldPanel('event_report'),
]