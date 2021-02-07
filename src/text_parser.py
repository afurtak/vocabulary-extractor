import re

import nltk
from nltk.tokenize import sent_tokenize
from nltk.parse.corenlp import GenericCoreNLPParser, CoreNLPDependencyParser
from typing import List

nltk.download('punkt')


def parse_vocabulary(
        text: str,
        dependency_parser: GenericCoreNLPParser = CoreNLPDependencyParser()
) -> (str, str):
    sentences = sent_tokenize(text)
    sentences = [clean_sentence(sentence) for sentence in sentences]

    parsed_trees = [
        (sent, dependency_parser.raw_parse(sent))
        for sent in sentences
    ]

    tree = [
        (sent, parse_tree(tree))
        for sent, tree in parsed_trees
    ]

    vocabulary = [
        (sent, get_vocabulary(sent, nodes))
        for sent, nodes in tree
    ]

    vocabulary = [
        (sent, v)
        for sent, v in vocabulary
        if v and len(v) != 0
    ]

    vocabulary = [
        [(sent, v[0], v[1]) for v in context]
        for sent, context in vocabulary
    ]

    vocabulary = sum(vocabulary, [])

    vocabulary = [
        (sent, sorted(v, key=lambda x:x[1]), tag)
        for sent, v, tag in vocabulary
    ]

    vocabulary = [
        (sent, " ".join(map(lambda x: x[0], v)), tag)
        for sent, v, tag in vocabulary
    ]

    return vocabulary


def parse_tree(tree: iter) -> List[dict]:
    deps, = tree

    return [
        deps.get_by_address(i)
        for i in range(1, len(deps.nodes))
    ]


def get_vocabulary(sent, all_nodes):
    words = [
        (node['address'], node['word'])
        for node in all_nodes
        if re.match(r'\w+', node['word'])
    ]

    incorrect_pos = [
        pos
        for pos, word in words
        if len(re.findall('\\b{}\\b'.format(word), sent)) == 0
    ]
    visited = set(incorrect_pos)

    result = []
    for node in all_nodes:
        if node['address'] not in visited and not is_compound_dependency(node['rel']):
            result.append(t(all_nodes, node, visited))
    return result


def t(all_nodes, node, visited):
    if node['address'] in visited:
        return []
    visited.add(node['address'])

    deps = get_compound_dependency(node)
    if deps:
        a = [(node['lemma'], node['address'])]
        b = [
            t(all_nodes, all_nodes[x - 1], visited)
            for x in deps
        ]
        b = sum([x[0] for x in b if len(x) > 0], [])
        c = node['tag']
        return a + b, c
    else:
        return [(node['lemma'], node['address'])], node['tag']


def is_compound_dependency(dep):
    return dep.startswith('compound')


def get_compound_dependency(node):
    for dep in node['deps']:
        if is_compound_dependency(dep):
            return node['deps'][dep]
    return None


def clean_sentence(sentence):
    return sentence
