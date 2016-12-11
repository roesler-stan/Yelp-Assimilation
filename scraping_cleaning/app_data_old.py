# -*- coding: utf-8 -*-

# business_id is not comparable in academic vs. scraped data

import pandas as pd
import numpy as np
import csv
import string

def main():
    data_directory = '../../Data/'
    directory = data_directory + 'academic/'
    
    review_file = directory + 'yelp_academic_dataset_review.csv'
    business_file = directory + 'yelp_academic_dataset_business.csv'
    user_file = directory + 'yelp_academic_dataset_user.csv'
    scraped_file = data_directory + 'yelp_reviews_merged.csv'
    reviews_outfile = data_directory + 'app_data/all_reviews.csv'
    business_outfile = data_directory + 'app_data/all_businesses.csv'

    review_cols_long = ['review_id', 'business_id', 'lat', 'lon', 'cat', 'city', 'state', 'name', 'text', 'uname', 'type']
    review_cols = ['review_id', 'type', 'business_id', 'text', 'uname']
    business_cols = ['business_id', 'type', 'lat', 'lon', 'cat', 'city', 'state', 'name']

    scraped_reviews = clean_scraped(scraped_file, review_cols_long)
    scraped_businesses = scraped_reviews.groupby('business_id').agg({'lat': np.mean, 'lon': np.mean,
        'cat': np.max, 'city': np.max, 'state': np.max, 'name': np.max}).reset_index()
    scraped_businesses['type'] = 'Scraped'
    scraped_reviews = scraped_reviews[review_cols]

    academic_businesses = clean_businesses(business_file, business_cols)
    businesses = academic_businesses.append(scraped_businesses)
    businesses = businesses[(businesses['lat'].notnull()) & (businesses['lon'].notnull())]
    businesses = make_titles(businesses)
    businesses['state'] = businesses['state'].str.upper()
    businesses = businesses[business_cols]
    businesses.to_csv(business_outfile, index = False, quoting = csv.QUOTE_ALL)
    
    academic_reviews = clean_academic(review_file, user_file, review_cols)
    academic_reviews = academic_reviews.merge(academic_businesses[['business_id', 'name', 'cat', 'city', 'state', 'lat', 'lon']], on = ['business_id'], how = 'inner')
    academic_reviews = academic_reviews[review_cols]
    reviews = academic_reviews.append(scraped_reviews)
    reviews = make_titles(reviews)

    # Only include reviews that have an associated business - to enable foreign key and for efficiency
    business_ids = businesses['business_id'].tolist()
    reviews = reviews[reviews['business_id'].isin(business_ids)]

    # Quoting is very important!
    reviews = reviews[review_cols]
    reviews.to_csv(reviews_outfile, index = False, quoting = csv.QUOTE_ALL)

def clean_academic(review_file, user_file, review_cols):
    # Clean academic reviews
    academic_reviews = pd.read_csv(review_file)

    # Clean user data and merge it with reviews-businesses reviews_data
    # It never happens that you have business and review data, but no user data
    cols = ['user_id', 'name', 'yelping_since']
    user_data = clean_users(user_file, cols)
    reviews_data = academic_reviews.merge(user_data, on = ['user_id'], how = 'inner')
    reviews_data = reviews_data.rename(columns = lambda x: x.replace('.', '_'))
    reviews_data['type'] = 'Academic'

    # Most columns are named from the business's perspetive, e.g. 'name' = business name
    reviews_data = reviews_data.rename(columns = {'latitude': 'lat', 'longitude': 'lon', 'category': 'cat', 'user_name': 'uname'})
    return reviews_data

def clean_scraped(scraped_file, review_cols):
    # Clean scraped reviews
    scraped_data = pd.read_csv(scraped_file)
    scraped_data['type'] = 'Scraped'
    scraped_data['categories'] = scraped_data['category1'].fillna('') + ',' + scraped_data['category2'].fillna('') + ',' + \
    scraped_data['category3'].fillna('') + ',' + scraped_data['category4'].fillna('') + ',' + scraped_data['category5'].fillna('')
    scraped_data = categories(scraped_data)

    orig_cols = ['business_id', 'review_id', 'latitude', 'longitude', 'category', 'business_city', 'business_state', 'business_name',
    'reviewer_name', 'type', 'review']
    scraped_data = scraped_data[orig_cols]
    scraped_data = scraped_data.rename(columns = {'latitude': 'lat', 'longitude': 'lon', 'category': 'cat', 'business_name': 'name',
        'reviewer_name': 'uname', 'business_city': 'city', 'business_state': 'state', 'review': 'text'})
    scraped_data = scraped_data[review_cols]

    return scraped_data

def clean_users(user_file, cols):
    user_data = pd.read_csv(user_file)
    user_data = user_data[cols]

    # Convert 'yelping since' to datetime
    user_data['yelping_since'] = pd.to_datetime(user_data['yelping_since'], errors = 'coerce', format = '%Y-%m')

    user_data = user_data.rename(columns = lambda x: 'user_' + x)
    user_data = user_data.rename(columns = {'user_user_id': 'user_id'})
    return user_data

def clean_businesses(business_file, business_cols):
    # Clean academic business data
    business_data = pd.read_csv(business_file)

    # Only include restaurants
    business_data = business_data[business_data['categories'].str.contains('restaurant', case = False, na = False)]
    business_data = categories(business_data)
    business_data = business_data[business_data['category'].notnull()]

    # Rename 'stars' b/c it is also a characteristic of reviews, as with type
    business_data = business_data.rename(columns = {'stars': 'business_stars', 'type': 'business_type'})
    business_data = business_data.rename(columns = {'latitude': 'lat', 'longitude': 'lon', 'category': 'cat'})
    # Remove non-US states, e.g. Quebec and Ontario
    business_data = business_data[~business_data['state'].isin(['QC', 'ON', 'EDH', 'MLN', 'FIF', 'ELN', 'XGL', 'BW', 'RP', 'KHL', 'NW'])]

    business_data['type'] = 'Academic'
    business_data = business_data[business_cols]
    # Remove data missing lat or lon
    business_data = business_data[(business_data['lat'].notnull()) & (business_data['lon'].notnull())]
    return business_data

def categories(data):
    # Code the category for ethnicities of interest and remove all other restaurants
    # assumes that ethnicities don't overlap
    ethnicities = ['Mexican', 'Chinese', 'Italian', 'American']

    data['number_categories'] = 0
    for ethnicity in ethnicities:
        data.loc[data['categories'].str.contains(ethnicity, na = False, case = False), 'category'] = ethnicity
        data.loc[data['categories'].str.contains(ethnicity, na = False, case = False), 'number_categories'] += 1

    data.loc[data['category'].isnull(), 'category'] = 'Other'
    data.loc[data['number_categories'] > 1, 'category'] = 'Multiple'

    return data

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

def business_id(data):
    data['business_id'] = data['name'].fillna('') + '-' + data['lat'].round(8).astype(str).fillna('')
    return data

if __name__ == '__main__':
    main()