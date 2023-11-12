from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    parameters = context['request'].GET.copy()
    # keys = parameters.dict().keys()
    # for k in keys:
    #     if parameters.get(k, default=None) is None:
    #         parameters.pop(k)
    for parameter_key, parameter_val in kwargs.items():
        parameters[parameter_key] = parameter_val
    return parameters.urlencode()

@register.simple_tag(takes_context=False)
def time_now():
    return timezone.localtime(timezone.now())
