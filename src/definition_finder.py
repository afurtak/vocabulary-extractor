import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')

from .vocabulary_filter import wordnet_pos_code


def find_definitions(vocabulary):
    vocabulary = [
        (context, v, find_definition(v, wordnet_pos_code(tag)))
        for context, v, tag in vocabulary
    ]

    return [
        (context, v, definition)
        for context, v, definition in vocabulary
        if definition
    ]


def find_definition(phrase, tag):
    phrase = phrase.replace(" ", "_")
    try:
        return wn.synset(f'{phrase}.{tag}.01').definition()
    except:
        return None
