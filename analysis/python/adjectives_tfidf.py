import pandas as pd
import numpy as np
import nltk
import string
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    data_directory = "/Users/katharina/Dropbox/Projects/Yelp/Data/academic/"
    infile = data_directory + "academic_dataset_cleaned_small.csv"
    outfile = data_directory + "adjectives_tfidf.csv"
    academic_data = pd.read_csv(infile)

    token_dict = {}
    categories = ['Mexican', 'Italian', 'American']
    states = ['AZ', 'WI']
    for category in categories:
        for state in states:
            data = academic_data[(academic_data['state'] == state) & (academic_data['category'] == category)]
            text = ' '.join(data['review'].tolist()).lower()
            adjectives_text = clean_text(text)
            cat_state = category + " in " + state
            token_dict[cat_state] = adjectives_text

    tfidf = TfidfVectorizer()
    tfs = tfidf.fit_transform(token_dict.values())
    tfidf_data = pd.DataFrame([ pd.SparseSeries(tfs[i].toarray().ravel()) for i in np.arange(tfs.shape[0]) ])
    columns = tfidf.get_feature_names()
    tfidf_data.columns = columns
    tfidf_data.index = token_dict.keys()

    tfidf_data = tfidf_data.stack().reset_index()
    tfidf_data = tfidf_data.rename(columns = {'level_0': 'cat_state', 'level_1': 'term', 0: 'tfidf'})
    top20_data = tfidf_data.sort(['cat_state', 'tfidf'], ascending = False).groupby('cat_state').head(20)
    top20_data.to_csv(outfile, index = False)

def clean_text(text):
    text = text.decode('unicode_escape', errors = 'ignore').encode('ascii', errors = 'ignore')
    table = string.maketrans("","")
    text = text.translate(table, string.punctuation)
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    # Check for named entities (e.g. "Pride and Prejudice" vs. pride) - this step takes a long time
    entities = nltk.chunk.ne_chunk(tagged)
    adjectives = [str(entity[0]) for entity in entities if entity[-1] == 'JJ']
    adjectives_text = ' '.join(adjectives)
    return adjectives_text

if __name__ == "__main__":
    main()