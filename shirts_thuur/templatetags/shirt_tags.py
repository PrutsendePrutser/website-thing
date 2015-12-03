"""Custom tags for shirts app
    Hey, your shirt tag is showing..
"""

from django import template
from shirts_thuur.models import *

register = template.Library()

# snippet for interested (un)related links
@register.inclusion_tag('shirts_thuur/tags/interesting_refs.html',
                       takes_context=True)
def interesting_refs(context):
    return {
        'interesting_refs': InterestingThing.objects.all(),
        'request': context['request'],
    }