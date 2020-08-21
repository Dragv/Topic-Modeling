import nltk
import spacy

spacy.load('en')
from spacy.lang.en import English
parser = English()

nltk.download('wordnet')
from nltk.corpus import wordnet as wn

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def getLemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

from nltk.stem.wordnet import WordNetLemmatizer
def getRootWord(word):
    return WordNetLemmatizer().lemmatize(word)

def tokenize(text):
    ldaTokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            ldaTokens.append('URL')
        elif token.orth_.startswith('@'):
            ldaTokens.append('SCREEN_NAME')
        else:
            ldaTokens.append(token.lower_)
    return ldaTokens

def prepareText(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len (token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [getLemma(token) for token in tokens]
    return tokens

def StringToCSV(text):
    return text.split('\. ')

from gensim import corpora


from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/send', methods=['POST'])
def hello_world():
    request.form('text')
    return 'Hello, World!'

import random
if __name__ == "__main__":
    text_data = []
    with open('dataset.csv') as f:
        for line in f:
            tokens = prepareText(line)
            if random.random() > .99:
                text_data.append(tokens)

    print(text_data)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    import pickle
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')

    import gensim
    NUM_TOPICS = 5
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word = dictionary, passes = 15)
    topics = ldamodel.print_topics(num_words = 4)
    for topic in topics:
        print(topic)

    app.run()
