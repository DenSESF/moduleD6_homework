# flake8: noqa E501
from django import template
import os
import re
import json
from flashtext import KeywordProcessor


register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    if isinstance(value, str):
        keyword_processor = KeywordProcessor()
        if os.path.isfile('whiteboard/templatetags/censuredlist.json'):
            with open('whiteboard/templatetags/censuredlist.json', 'r') as file_censor:
                censured_words_dict = json.load(file_censor)
            keyword_processor.add_keywords_from_dict(censured_words_dict)
        return keyword_processor.replace_keywords(value)
    else:
        raise ValueError(f'Нельзя цензурировать {type(value)}')


@register.filter(name='RegExError')
def RegExError(value):
    pattern = re.compile(r'^[*][\w\s_]*[*]\s([\w\s\d.]*)')
    error = pattern.search(value)
    if error is not None:
        return error[1]
    return value
