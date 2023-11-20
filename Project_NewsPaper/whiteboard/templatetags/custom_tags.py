from django import template
# from django.utils import timezone

from whiteboard.models import Category

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

# Заменил на тэг django
# @register.simple_tag(takes_context=False)
# def time_now():
#     return timezone.localtime(timezone.now())


@register.simple_tag(takes_context=False)
def get_list_category():
    categorys = list(Category.objects.values_list('id', 'name'))
    first_item_to_str = lambda x: tuple([str(x[0]), x[1]])
    return list(map(first_item_to_str, categorys))


@register.simple_tag(takes_context=True)
def is_subscriber(context, **kwargs):
    cat_id = context['request'].GET.get('cat')
    if cat_id is not None and cat_id.isnumeric():
        user = context['request'].user
        return Category.objects.get(pk=cat_id).subscribers.filter(username=user).exists()
    return False
