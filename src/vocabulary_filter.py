import json
import requests
import nltk
from nltk.corpus import stopwords, wordnet as wn
import re
from tqdm import tqdm

nltk.download('stopwords')
nltk.download('wordnet')


def filter_vocabulary(
        vocabulary,
        interesting_threshold=None):
    vocabulary = filter_stopwords(vocabulary)
    vocabulary = remove_duplicates(vocabulary)
    vocabulary = filter_not_correct_words(vocabulary)
    vocabulary = filter_with_proper_tag(vocabulary)
    vocabulary = filter_words_in_dictionary(vocabulary)
    if interesting_threshold:
        vocabulary = filter_interesting_vocabulary(vocabulary, interesting_threshold)
    return vocabulary


def remove_duplicates(vocabulary):
    x = set()
    result = []
    for context, v, tag in vocabulary:
        if (v.lower(), tag) not in x:
            result.append((context, v, tag))
            x.add((v.lower(), tag))
    return result


def filter_stopwords(vocabulary):
    return [
        (context, v, tag)
        for context, v, tag in vocabulary
        if v.lower() not in stopwords.words('english')
    ]


def filter_with_proper_tag(vocabulary):
    return [
        (context, v, tag)
        for context, v, tag in vocabulary
        if wordnet_pos_code(tag) != ''
    ]


def wordnet_pos_code(tag):
    if tag.startswith('NN'):
        return wn.NOUN
    elif tag.startswith('VB'):
        return wn.VERB
    elif tag.startswith('JJ'):
        return wn.ADJ
    elif tag.startswith('RB'):
        return wn.ADV
    else:
        return ''


def filter_not_correct_words(vocabulary):
    return [
        (context, v, tag)
        for context, v, tag in vocabulary
        if re.match(r"[a-z\']", v.lower())
    ]


def filter_words_in_dictionary(vocabulary):
    return [
        (context, v, tag)
        for context, v, tag in vocabulary
        if len(wn.synsets(v.lower().replace(" ", "_"))) > 0
    ]


def filter_interesting_vocabulary(vocabulary, interesting_threshold):
    return list(filter(
        lambda x: is_compound(x[1]) or get_word_difficulty(x[1]) >= interesting_threshold,
        tqdm(vocabulary),
    ))


def is_compound(word):
    return len(word.split(' ')) > 1


def get_word_difficulty(word):
    url = "https://twinword-language-scoring.p.rapidapi.com/word/"
    querystring = {"entry": word}
    headers = {
        'x-rapidapi-key': get_rapidapi_key(),
        'x-rapidapi-host': "twinword-language-scoring.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        response = json.loads(response.text)
        try:
            return response['ten_degree']
        except:
            return 0
    else:
        raise RuntimeError("Something gone wrong with the connection to the "
                           "twinword-language-scoring.p.rapidapi.com api")


def get_rapidapi_key():
    with open('x-rapidapi-key', 'r') as f:
        return f.readline()