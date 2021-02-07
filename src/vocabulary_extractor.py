import click

from src.definition_finder import find_definitions
from src.text_parser import parse_vocabulary
from src.vocabulary_filter import filter_vocabulary


@click.command()
@click.option('--input',
              help='Path to input text file')
@click.option('--output',
              help='Path to output text file with vocabulary extracted from '
                   'given input')
@click.option('--min-level',
              default=None,
              type=click.INT,
              help='Minimal level of presented vocabulary. Number 1-10')
def hello(input, output, min_level):
    with open(input, 'r') as f:
        text = f.read().replace("\n", " ")

    print(min_level)
    vocabulary = parse_vocabulary(text)
    vocabulary = filter_vocabulary(vocabulary, interesting_threshold=min_level)
    vocabulary = find_definitions(vocabulary)

    with open(output, 'w') as f:
        for context, v, definition in vocabulary:
            f.write(v + '\n')
            f.write('\tDefinition       : ' + definition + '\n')
            f.write('\tContext from text: ' + context + '\n')
            f.write('\n')


if __name__ == '__main__':
    hello()