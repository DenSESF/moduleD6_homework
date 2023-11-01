from django import template


register = template.Library()

@register.filter(name='multiply')

def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return value * arg
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')
