import pandas as pd
import numpy as np
import csv
import re
import code_reviews as cr
import code_chains as cc

def main():
    in_directory = '../../Data/academic/input_round8/'
    out_directory = '../../Data/academic/'
    review_file = in_directory + 'yelp_academic_dataset_review.csv'
    business_file = in_directory + 'yelp_academic_dataset_business.csv'
    user_file = in_directory + 'yelp_academic_dataset_user.csv'
    outfile = out_directory + 'academic_dataset_cleaned.csv'

    df_review = pd.read_csv(review_file)
    df_business = pd.read_csv(business_file)
    df_user = pd.read_csv(user_file)

    # Merge the datasets, keeping them on the review level
    # Each review has one user and is for one business, so we use left outer joins
    df = df_review.merge(df_user, on = ['user_id'], how = 'left', suffixes = ['_review', '_user'])
    df = df.merge(df_business, on = ['business_id'], how = 'left', suffixes = ['_review', '_business'])

    df = clean_data(df)

    # Quoting is very important!
    df.to_csv(outfile, index = False, quoting = csv.QUOTE_ALL)

def clean_data(df):
    # Only include restaurants
    df = df[df['categories'].str.contains('restaurant', case = False, na = False)]

    df['date'] = pd.to_datetime(df['date'], errors = 'coerce', format = '%Y-%m-%d')
    df['year'] = df['date'].dt.year

    # Convert 'yelping since' to datetime
    df['yelping_since'] = pd.to_datetime(df['yelping_since'], errors = 'coerce', format = '%Y-%m')
    df['yelping_since_year'] = df['yelping_since'].dt.year

    df = clean_attributes(df)

    # Decode non-Ascii text
    df['text'] = df['text'].str.decode('unicode_escape', errors = 'ignore').str.encode('ascii', errors = 'ignore')
    df = cr.categories(df)
    df = cr.code_themes(df)
    df = cc.code_chains(df)

    df = df.rename(columns = lambda x: x.replace('.', '_'))

    # Shuffle the data, using the same seed to be able to keep track of the data
    np.random.seed(72)
    df = df.reindex(np.random.permutation(df.index))

    return df

def clean_attributes(df):
    # Convert all attributes booleans to floats: also considers 1 and 0 to be boolean
    for col in [c for c in df.columns if 'attributes' in c]:
        col_values = df[col][:50].unique().tolist()
        if True in col_values or False in col_values:
            df[col] = df[col].astype(bool).astype(float)
    return df

if __name__ == '__main__':
    main()