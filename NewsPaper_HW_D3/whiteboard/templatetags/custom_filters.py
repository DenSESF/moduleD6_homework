from django import template
import os
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
