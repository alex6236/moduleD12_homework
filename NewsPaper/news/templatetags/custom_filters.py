from django import template
import re
# import os

# current_directory = os.getcwd()
# contents = os.listdir(current_directory)
# print(contents)

register = template.Library()

@register.filter(name='censor')
def censor(value):
    with open('words.txt', 'r', encoding='utf-8') as f:
        bad_words = f.read().split()
        for w in bad_words:
            word = r'\b{}\b'.format(w)
            value = re.sub(word, '!п-'+'и-'*len(w)+'п!', value)
        return value