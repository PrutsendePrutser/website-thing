from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class ImageWithCaptionSnippet(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    caption = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('caption'),
        ImageChooserPanel('image'),
    ]
