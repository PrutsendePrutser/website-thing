from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class EventReportBlock(blocks.StructBlock):
    event_name = blocks.CharBlock(required=True)
    event_date = blocks.DateTimeBlock(required=True)
    event_pictures = blocks.ListBlock(ImageChooserBlock(label="Picture"))
    event_text_block = blocks.RichTextBlock()
    event_sub_header = blocks.CharBlock()

    class Meta:
        form_classname = 'event-report-block struct-block'
