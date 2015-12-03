import wagtail.wagtailsearch
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailsnippets.models import register_snippet

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                MultiFieldPanel,
                                                InlinePanel,
                                                PageChooserPanel,)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsearch import index


@register_snippet
class InterestingThing(models.Model):
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    def __unicode__(self):
        return self.text


class ShirtLinkFields(models.Model):
    link_external = models.URLField(_("External link"), blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url_path
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
    ]

    class Meta:
        abstract = True


class ShirtLink(ShirtLinkFields):
    title = models.CharField(max_length=255, help_text=_("Link title"))

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(ShirtLinkFields.panels, _("Link"))
    ]

    class Meta:
        abstract = True


class ShirtIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        InlinePanel('shirt_links', label=_("Shirt links"))
    ]

    class Meta:
        verbose_name = _("Overzicht shirts")

    parent_page_types = []
    subpage_types = ['ShirtPage']

    def get_context(self, request, *args, **kwargs):
        context = super(ShirtIndexPage, self).get_context(request, *args, **kwargs)

        shirts = (self.get_children()
                  .select_related('shirtpage')
                  .live())
        context.update({
            'shirts': shirts,
        })
        return context


class ShirtPage(Page):
    # Fields
    shirt_image = models.ForeignKey(
        'shirts_thuur.ShirtImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    interesting_ref = models.ForeignKey(
        'shirts_thuur.InterestingThing',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField(_("Datum post"))
    story = RichTextField(_("Verhaal achter het shirt"))
    description = models.CharField(_("Omschrijving"), max_length=255)

    # Search indexing
    search_fields = Page.search_fields + (
        index.SearchField('description'),
        index.SearchField('story'),
        index.FilterField('date'),
    )

    # Content panels config
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('story', classname='full'),
        FieldPanel('description'),
        InlinePanel('related_links', label="Gerelateerde referenties"),
        InlinePanel('ref_placements', label=_("Interesting references")),
    ]

    # Promotion panel config
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('shirt_image')
    ]

    # Allowed parent/child pages
    parent_page_types = ['ShirtIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = _("Shirt pagina")


class ShirtIndexRelatedLink(Orderable, ShirtLink):
    page = ParentalKey('ShirtIndexPage', related_name='shirt_links')


class ShirtPageRelatedLink(Orderable):
    page = ParentalKey(ShirtPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class ShirtPageRefPlacement(Orderable, models.Model):
    page = ParentalKey('shirts_thuur.ShirtPage', related_name='ref_placements')
    ref = models.ForeignKey('shirts_thuur.InterestingThing', related_name='+')

    class Meta:
        verbose_name = _("Interesting reference")
        verbose_name_plural = _("Interesting references")

    panels = [
        SnippetChooserPanel('ref'),
    ]

    def __unicode__(self):
        return self.page.title + " -> " + self.ref.text


class ShirtImage(AbstractImage):
    caption = models.CharField(_("Caption"), max_length=255)

    admin_form_fields = Image.admin_form_fields + ('caption',)


class ShirtRendition(AbstractRendition):
    image = models.ForeignKey(ShirtImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Delete image source when image is deleted
@receiver(pre_delete, sender=ShirtImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete rendition file when rendition is deleted
@receiver(pre_delete, sender=ShirtRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)