import nltk
import random
import tkinter as tk
import os

from nltk import Tree
from nltk.corpus import treebank
from nltk.corpus import names
from nltk.corpus import wordnet as wn
from nltk.draw import TreeView, TreeWidget
from nltk.draw.util import CanvasFrame

from view.main_window import MainWindow

main_window = MainWindow()

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('brown')
nltk.download('names')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('treebank')
# in terminal pip3 install pandas

sentence = "At eight o'clock on Thursday morning. Arthur didn't feel very good."

# Tokenization
tokens = nltk.word_tokenize(sentence)
print(tokens)

# POS Tag
tagged = nltk.pos_tag(tokens)
print(tagged[0:6])

# Representing Tagged token
tagged_token = nltk.tag.str2tuple('fly/NN')
print(tagged_token)

entities = nltk.chunk.ne_chunk(tagged)
print(entities)

print(nltk.corpus.brown.tagged_words())


# classification : Gender identification
def gender_features(word):
    return {'last_letter': word[-1]}


print(gender_features('Shrek'))

labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in
                                                                         names.words('female.txt')])
random.shuffle(labeled_names)
featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(classifier.classify(gender_features('Neo')))
print(classifier.classify(gender_features('Trinity')))
print(nltk.classify.accuracy(classifier, test_set))

# Wordnet
print(wn.synsets('motorcar'))
print(wn.synset('car.n.01').lemma_names())
print(wn.synset('car.n.01').definition())

# display a parse tree form corpus treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
# t.draw()
cf = CanvasFrame(main_window._window)
t = Tree.fromstring('(S (NP this tree) (VP (V is) (AdjP pretty)))')
tc = TreeWidget(cf.canvas(),t)
cf.add_widget(tc,10,10) # (10,10) offsets
# cf.print_to_file('tree.png')
# cf.destroy()
main_window.start()



