# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy


# Set up functions to help produce human-friendly printing.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def skip_and_print(*args):
    """ Act like print(), but skip a line before printing. """
    print('\n' + str(args[0]), *args[1:])


def print_table(rows, padding=0):
    """ Print `rows` with content-based column widths. """
    col_widths = [
        max(len(str(value)) for value in col) + padding
        for col in zip(*rows)
    ]
    total_width = sum(col_widths) + len(col_widths) - 1
    fmt = ' '.join('%%-%ds' % width for width in col_widths)
    print(fmt % tuple(rows[0]))
    print('~' * total_width)
    for row in rows[1:]:
        print(fmt % tuple(row))


if __name__ == "__main__":
    # Load a language model and parse a document.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    nlp = spacy.load('en_core_web_sm')

    document_string = """
    The Waystone Inn lay in silence,
    and it was a silence of three parts.
    """

    # Remove starting, ending, and duplicated whitespace characters.
    document_string = ' '.join(document_string.split())

    skip_and_print('Working with string: "%s"' % document_string)
    doc = nlp(document_string)

    rows = [['Chunk', '.root', 'root.dep_', '.root.head']]
    for chunk in doc.noun_chunks:
        rows.append([
            chunk,  # A Span object with the full phrase.
            chunk.root,  # The key Token within this phrase.
            chunk.root.dep_,  # The grammatical role of this phrase.
            chunk.root.head  # The grammatical parent Token.
        ])
    print_table(rows, padding=4)

    # Find the head words of sentences.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    document_string = """
    It's the questions we can't answer that teach us the most.
    They teach us how to think.
    """

    # Remove starting, ending, and duplicated whitespace characters.
    document_string = ' '.join(document_string.split())

    skip_and_print('Working with string: "%s"' % document_string)
    doc = nlp(document_string)

    # For each sentence, spacy identifies a root of the dependency
    # tree. You can think of this as the grammatically most
    # meaningful word in the sentence.

    skip_and_print('Root word of each sentence:')
    rows = [['Root', '|', 'Sentence']]
    for sentence in doc.sents:
        rows.append([sentence.root, '|', sentence.text])
    print_table(rows)

    # Find all the dependent tokens of a given one.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # This means finding the words in a sentence being operated on
    # by the given input word. Another perspective is to view words
    # lower in the dependency tree (that is, being more dependent),
    # as being less important to the overall sentence meaning.

    skip_and_print('Dependent words (aka subtree) of some tokens:')
    rows = [['Token', '|', 'Subtree']]

    # Print subtrees for 'teach' in 1st sentence, 'most', and then
    # 'teach' in the 2nd sentence (which are tokens 9, 12, and 15).
    for token in [doc[9], doc[12], doc[15]]:
        subtree = [
            ('((%s))' if t is token else '%s') % t.text
            for t in token.subtree
        ]
        rows.append([token.text, '|', ' '.join(subtree)])
    print_table(rows)

    # Displays tree at localhost
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Valik smokes the kalik.")
    spacy.displacy.serve(doc, style="dep")
