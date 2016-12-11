""" Draw word cloud using data from Yelp.com reviews of Mexican restaurants """

import pandas
import re
import numpy
from PIL import Image
import wordcloud as wc
import matplotlib.pyplot as plt
import nltk

def main():
    data_directory = '../../Data/'
    output_directory = '../../Output/'

    infile = data_directory + 'yelp_reviews_only.csv'
    mask_file = data_directory + 'speech_bubble.png'
    outfile_adj = output_directory + 'yelp_adj.png'

    dataset = pandas.read_csv(infile)
    text = select_text(dataset)

    entities = parse_text(text, lemmatize = False)
    adjectives = [str(entity[0]) for entity in entities if entity[-1] == 'JJ']
    adjectives = [w for w in adjectives if w != 'deliciou']
    adjectives_text = ' '.join(adjectives)

    max_words = 2000
    masked_cloud(adjectives_text, outfile_adj, max_words, mask_file)

def masked_cloud(text, outfile, max_words, mask_file):
    """ Make a word cloud in the shape of the mask file's black parts """
    mask_shape = numpy.array(Image.open(mask_file))
    word_cloud = wc.WordCloud(max_words = max_words, background_color = "white", mask = mask_shape)
    # stopwords = wc.STOPWORDS.add("said")    
    word_cloud.generate(text)
    word_cloud.to_file(outfile)

def select_text(dataset):
    """ Take dataset with reviews column and return text from all reviews. """
    reviews = dataset['review'].to_string()
    reviews = re.sub('(\d+)|([\t\n\r\f\v])','',reviews)
    while '  ' in reviews:
        reviews = reviews.replace('  ', ' ')
    return reviews

def parse_text(text, lemmatize):
    text = text.lower()
    tokens = nltk.word_tokenize(text)

    if lemmatize:
        wnl = nltk.WordNetLemmatizer()
        tokens = [wnl.lemmatize(t) for t in tokens]

    tagged = nltk.pos_tag(tokens)
    
    # Check for named entities (e.g. "Pride and Prejudice" vs. pride) - this step takes a long time
    entities = nltk.chunk.ne_chunk(tagged)
    return entities

if __name__ == '__main__':
    main()