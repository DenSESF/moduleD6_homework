# flake8: noqa E501
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


# @register.simple_tag(takes_context=False)
# def get_list_category():
#     category_list = list(Category.objects.values_list('id', 'name'))
#     return list(map(lambda x: tuple([str(x[0]), x[1]]), category_list))


# Неудачное решение перенес логику в NewsList
# @register.simple_tag(takes_context=True)
# def is_subscriber(context, **kwargs):
#     user = context['request'].user
#     cat_id = context['request'].GET.get('cat')
#     if not user.is_authenticated or cat_id is None:
#          return False
#     news = context['object_list'].values(category=cat_id)
#     if news.exists():
#             # return Category.objects.get(pk=int(cat_id)).subscribers.filter(username=user).exists()
#             return news.filter(category__user__username=user).exists()
#     return False
