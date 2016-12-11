# -*- coding: utf-8 -*-

# business_id is not comparable in academic vs. scraped data

import pandas as pd
import numpy as np
import csv
import string

def main():
    data_directory = '../../Data/'
    academic_file = data_directory + 'academic/academic_dataset_cleaned.csv'
    scraped_file = data_directory + 'yelp_reviews_merged.csv'
    reviews_outfile = data_directory + 'app_data/all_reviews.csv'
    business_outfile = data_directory + 'app_data/all_businesses.csv'

    scraped_reviews = clean_scraped(scraped_file)
    academic_reviews = clean_academic(academic_file)
    
    reviews = academic_reviews.append(scraped_reviews)
    reviews = make_titles(reviews)
    reviews['state'] = reviews['state'].str.upper()
    reviews = reviews[(reviews['lat'].notnull()) & (reviews['lon'].notnull())]
    reviews = reviews.drop_duplicates(subset=['review_id'])

    # Columns to aggregate across reviews
    aggregate_dict = {'lat': np.mean, 'lon': np.mean, 'cat': np.max, 'city': np.max, 'state': np.max, 'name': np.max, 'stars': np.mean, 'dollars': np.mean,
    'type': np.max}
    businesses = reviews.groupby('business_id').agg(aggregate_dict).reset_index()
    businesses = businesses[['business_id', 'type', 'lat', 'lon', 'cat', 'city', 'state', 'name', 'stars', 'dollars']]
    businesses.to_csv(business_outfile, index = False, quoting = csv.QUOTE_ALL)

    # Quoting is very important!
    reviews = reviews[['review_id', 'type', 'business_id', 'text', 'uname', 'stars']]
    reviews.to_csv(reviews_outfile, index = False, quoting = csv.QUOTE_ALL)

def clean_scraped(scraped_file):
    # Clean scraped reviews
    cols = ['business_id', 'review_id', 'latitude', 'longitude', 'category', 'business_city', 'business_state', 'business_name',
    'reviewer_name', 'text', 'reviewer_rating', 'dollars']
    scraped_reviews = pd.read_csv(scraped_file, usecols=cols)
    scraped_reviews = scraped_reviews.rename(columns = {'latitude': 'lat', 'longitude': 'lon', 'category': 'cat', 'business_name': 'name',
        'reviewer_name': 'uname', 'business_city': 'city', 'business_state': 'state', 'reviewer_rating': 'stars'})
    scraped_reviews['type'] = 'Scraped'
    return scraped_reviews

def clean_academic(academic_file):
    # Clean academic business data
    academic_reviews = pd.read_csv(academic_file)
    # Rename 'stars' b/c it is also a characteristic of reviews, as with type
    academic_reviews = academic_reviews.rename(columns = {'type': 'academic_type'})
    academic_reviews = academic_reviews.rename(columns = {'latitude': 'lat', 'longitude': 'lon', 'category': 'cat', 'name_review': 'uname',
    	'stars_review': 'stars', 'name_business': 'name'})
    # Remove non-US states, e.g. Quebec and Ontario
    academic_reviews = academic_reviews[~academic_reviews['state'].isin(['QC', 'ON', 'EDH', 'MLN', 'FIF', 'ELN', 'XGL', 'BW', 'RP', 'KHL', 'NW'])]
    academic_reviews = academic_reviews[academic_reviews['state'].notnull()]
    academic_reviews['type'] = 'Academic'
    academic_reviews['dollars'] = np.nan
    return academic_reviews

def replace_apost(value):
    for letter in string.ascii_lowercase:
        if "'" + letter.upper() in value:
            value = value.replace("'" + letter.upper(), "'" + letter.lower())
    return value

def make_titles(data):
    title_cols = ['city', 'name', 'uname']
    for col in title_cols:
        if col in data.columns:
            # data[col] = data[col].str.replace('[^\x00-\x7F]', '')
            data[col] = data[col].str.decode('unicode_escape', errors = 'ignore').str.encode('ascii', errors = 'ignore')
            data[col] = data[col].str.replace("’", "'").str.title()
            # replace upper case S after apostrophe with lower case s
            data[col] = data[col].astype(str).map(replace_apost)
    return data

if __name__ == '__main__':
    main()