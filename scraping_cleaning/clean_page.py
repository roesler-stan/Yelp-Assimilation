"""
TO DO: get attributes (like reservations)

This program gets review text from Yelp page .html files.

python clean_page.py -dd="../../Data/" -id="zips_0to500-ex" -o="reviews_0to500-ex.csv" -mf="scraped-ex/links0to500_missed_auto.csv" -nf="scraped-ex/links_0to500_noreviews.csv" -sf="input/states_key.csv"

python clean_page.py -dd="../../Data/" -id="zips_0to500" -o="reviews_0to500.csv" -mf="scraped/links0to500_missed_auto.csv" -nf="scraped/links_0to500_noreviews.csv" -sf="input/states_key.csv"
"""

# from cleaning_constants import *
from clean_page_helper import *
import os
import argparse
import urllib2
import urllib
import urlparse
from bs4 import BeautifulSoup
import csv
import re
import pandas
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dd', '--data_directory', dest = 'data_directory', type = str)
    parser.add_argument('-id', '--input_directory', dest = 'input_directory', type = str)
    parser.add_argument('-o', '--outfile', dest = 'outfile', type = str)
    parser.add_argument('-mf', '--missed_file', dest = 'missed_file', type = str)
    parser.add_argument('-nf', '--noreviews_file', dest = 'noreviews_file', type = str)
    parser.add_argument('-sf', '--states_file', dest = 'states_file', type = str)

    input_values = parser.parse_args()
    data_directory = input_values.data_directory
    outfile = data_directory + input_values.outfile
    input_directory = data_directory + input_values.input_directory
    missed_file = data_directory + input_values.missed_file
    noreviews_file = data_directory + input_values.noreviews_file
    states_file = data_directory + input_values.states_file

    headers = ['business_name', 'business_id', 'zipcode', 'average_rating', 'dollars',
    'reviewer_location', 'reviewer_city', 'reviewer_state', 'reviewer_country',
    'categories_count', 'category1', 'category2', 'category3', 'category4', 'category5', 'is_mexican',
    'reviewer_user_id', 'review_id', 'reviewer_name', 'reviewer_first_name', 'reviewer_last_name',
    'reviewer_rating', 'reviewer_friends', 'reviewer_reviews_count',
    'voted_useful', 'voted_funny', 'voted_cool', 'review', 'filename',
    'business_city', 'business_state', 'business_zipcode', 'street_address', 'latitude', 'longitude', 'website']

    with open(missed_file, 'w') as mf:
        mf.write(','.join(['filename', 'business_id', 'zipcode','business_link']) + '\n')

    with open(outfile, 'w') as f:
        writer = csv.DictWriter(f, fieldnames = headers)
        writer.writeheader()

        for folder_path, business_folders, filenames in os.walk(input_directory):
            files = [os.path.join(folder_path, f) for f in filenames if f.endswith(".html")]

            for filename in files:
                parameters = filename, writer, missed_file, noreviews_file, states_file
                parse_page(parameters)

def parse_page(parameters):
    """
    Find review for business with given business_id and write result to output file

    Args:
        filename (str): filename of html page from which to get review text
        writer (csv object): csv writer for output file
    """
    filename, writer, missed_file, noreviews_file, states_file = parameters

    # Encode the filename as ASCII to UTF-8 and then url quote its path in case it has non-ASCII symbols in it
    parsed_link = urlparse.urlsplit(filename.encode('utf8'))
    parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path))
    encoded_link = parsed_link.geturl()

    data = urllib2.urlopen('file:' + encoded_link)
    soup = BeautifulSoup(data, "html.parser")
    zipcode = filename.split('/')[-3]
    business_id = filename.split('/')[-2]
    business_link = 'http://www.yelp.com/biz/' + business_id

    # If it didn't find a title, mark it as a broken page and move on
    title_tag = soup.find('h1', {'class': 'biz-page-title'})
    if not title_tag:
        with open(missed_file, 'a') as mf:
            mf.write(','.join([filename, business_id, zipcode, business_link]) + '\n')
        return ''

    business_attributes = []
    business_name = title_tag.text.strip()
    rating = find_rating(soup)
    dollars = find_dollars(soup)
    categories = find_categories(soup)
    address_data = find_address(soup)

    business_attributes = [business_name, business_id, rating, dollars, filename, zipcode]
    business_attributes.extend(address_data)

    review_tags = find_reviews_tags(soup)
    # If there aren't any reviews, add it to the file of businesses without reviews and move on
    if not review_tags:
        with open(noreviews_file, 'a') as nf:
            nf.write(', '.join([filename, business_id, zipcode, business_link]) + '\n')
            return ''

    for review_tag in review_tags:
        row = find_review_info(review_tag, states_file)
        row = add_business_data(row, business_attributes)

        if categories:
            row['categories_count'] = len(categories)
            row['is_mexican'] = float('Mexican' in categories)
            for i, category in enumerate(categories):
                # index by 1
                category_number = i + 1
                if category_number > 5:
                    break
                row['category' + str(category_number)] = category

        row = make_lower(row)
        writer.writerow(row)

def add_business_data(row, business_attributes):
    """ Include measures for the entire business """
    business_name, business_id, rating, dollars, filename, zipcode, business_city, business_state, business_zipcode, street_address, latitude, longitude, website = business_attributes

    row['business_name'] = business_name
    row['business_id'] = business_id
    row['average_rating'] = rating
    row['dollars'] = dollars
    row['filename'] = filename
    row['zipcode'] = zipcode
    row['business_city'] = business_city
    row['business_state'] = business_state
    row['business_zipcode'] = business_zipcode
    row['street_address'] = street_address
    row['latitude'] = latitude
    row['longitude'] = longitude
    row['website'] = website

    return row

def find_review_info(review_tag, states_file):
    row = {}

    if review_tag.has_attr('data-review-id'):
        row['review_id'] = review_tag['data-review-id']
    
    if review_tag.has_attr('data-signup-object'):
        row['reviewer_user_id'] = review_tag['data-signup-object'].split('user_id:')[-1]

    # Reviewer-specific measures
    row['review'] = find_review(review_tag)
    row['reviewer_rating'] = find_reviewer_rating(review_tag)
    row['reviewer_friends'] = find_friends(review_tag)
    row['reviewer_reviews_count'] = find_reviewer_review_counts(review_tag)
    row = find_voting_feedback(review_tag, row)

    row = find_reviewer_name(review_tag, row)
    row = find_location(review_tag, row, states_file)
    return row

def find_reviews_tags(soup):
    """ Returns tag containing reviews """
    list_tag = soup.find('div',{'class':'review-list'})

    if list_tag:
        review_tags = list_tag.find_all('div', {'class': 'review--with-sidebar'})
        if review_tags:
            # Ignore the "with so few reviews, your opinion..." box trying to get users to add a review
            review_tags = [review_tag for review_tag in review_tags if review_tag.has_attr('data-review-id')]
            return review_tags

if __name__ == '__main__':
    main()