import pandas as pd
import numpy as np
import csv

def main():
    data_directory = '../../Data/'
    academic_data_directory = '../../Data/academic/'
    map_directory = '../../Data/app data/'

    scraped_file = data_directory + 'yelp_reviews_merged.csv'
    academic_reviews_infile = academic_data_directory + 'yelp_academic_dataset_cleaned.csv'
    academic_businesses_infile = academic_data_directory + 'yelp_academic_businesses_cleaned.csv'
    
    scraped_count_file = map_directory + 'scraped_reviews_count.tsv'
    scraped_reviews_file = map_directory + 'scraped_reviews.csv'
    academic_reviews_outfile = map_directory + 'academic_reviews.csv'
    academic_businesses_outfile = map_directory + 'academic_businesses.csv'

    # scraped_count(scraped_file, scraped_count_file)
    # scraped_reviews(scraped_file, scraped_reviews_file)
    academic_reviews(academic_reviews_infile, academic_reviews_outfile)
    # academic_businesses(academic_businesses_infile, academic_businesses_outfile)

def scraped_count(infile, outfile):
    dataset = pd.read_csv(infile)
    reviews_count = dataset.groupby('zipcode')['review'].count().reset_index()
    reviews_count.rename(columns = {'zipcode': 'id', 'review': 'rate'}, inplace = True)
    reviews_count.to_csv(outfile, index = False, sep = '\t')

def scraped_reviews(infile, outfile):
    dataset = pd.read_csv(infile)

    dataset['category'] = 'Mexican'
    dataset['business_city'] = dataset['business_city'].str.title()
    dataset['business_name'] = dataset['business_name'].str.title()
    dataset['state'] = dataset['state'].str.upper()
    dataset = dataset.rename(columns = {'review': 'text', 'business_name': 'name', 'business_city': 'city', 'reviewer_name': 'uname'})

    cols = ['latitude', 'longitude', 'category', 'state', 'city', 'name', 'text', 'uname']
    dataset = clean_data(dataset, cols)

    # Column order matters for SQL database
    ordered_cols = ['id', 'lat', 'lon', 'cat', 'city', 'state', 'name', 'text', 'uname']
    dataset = dataset[ordered_cols]
    dataset.to_csv(outfile, index = False)

def academic_reviews(academic_reviews_infile, academic_reviews_outfile):
    # academic dataset contains city, state, full_address, latitude, longitude
    dataset = pd.read_csv(academic_reviews_infile)

    cols = ['latitude', 'longitude', 'category', 'state', 'city', 'name', 'text', 'user_name']
    dataset = clean_data(dataset, cols)

    # Column order matters for SQL database
    ordered_cols = ['id', 'lat', 'lon', 'cat', 'city', 'state', 'name', 'text', 'uname']
    dataset = dataset[ordered_cols]

    # Quoting is very important!
    dataset.to_csv(academic_reviews_outfile, index = False, quoting = csv.QUOTE_ALL)

def academic_businesses(academic_businesses_infile, academic_businesses_outfile):
    dataset = pd.read_csv(academic_businesses_infile)

    cols = ['latitude', 'longitude', 'category', 'state', 'city', 'name', 'review_count']
    dataset = clean_data(dataset, cols)

    # Column order matters for SQL database
    ordered_cols = ['id', 'lat', 'lon', 'cat', 'count', 'city', 'state', 'name']
    dataset = dataset[ordered_cols]
    dataset.to_csv(academic_businesses_outfile, index = False)

def clean_data(dataset, cols):
    dataset = dataset[cols]

    # Only include American states I know are present
    valid_states = ['AZ', 'PA', 'NC', 'SC', 'WI', 'IL', 'NV', 'WA', 'CA', 'MN', 'MA', 'OR']
    dataset = dataset.loc[dataset['state'].isin(valid_states), :]
 
    # Encode any columns with text (name is the problematic one)
    for col in dataset.columns:
        if dataset[col].dtype == 'O':
            dataset[col] = dataset[col].str.decode('ascii', errors = 'ignore')

    dataset = dataset.dropna()

    # give shorter names
    dataset = dataset.rename(columns = {'category': 'cat', 'review_count': 'count',
        'latitude': 'lat', 'longitude': 'lon', 'user_name': 'uname'})

    # Shuffle the rows
    random_index = np.random.permutation(dataset.index)
    dataset = dataset.reindex(random_index)

    dataset['id'] = dataset.index

    return dataset

if __name__ == '__main__':
    main()