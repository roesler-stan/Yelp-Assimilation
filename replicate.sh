#!/bin/sh

# start in scraping_cleaning directory

# selected only zip codes from metropolitan areas - outdated
python zips.py

# use Yelp API to get 20-40 business IDs in a given zip code - outdated
python search_businesses_api.py


## The following two files will fail often - you need to restart the process manually, changing the lines you start at
# Scrape the business links by searching Yelp, make list of business links -> e.g. links0to500.txt
# lr is the line row of the zip codes file at which to begin
python business_links.py -z="../../Data/input/zips_2010_ordered.csv" -l="../../Data/scraped/links0to500.txt" -zs="../../Data/scraped/zips_searched_0to500.txt" -lr=0 -hr=500

# download all html pages for each business in business links file -> zipcode/business/0.html
# lr is the line row of the business links file at which to begin
# uses constants in constants.py
python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500.txt" -lr=674



# clean HTML pages to extract reviews and other information -> reviews_0to500.csv
# uses clean_page_helper.py to specify how to extract fields from HTML
python clean_page.py

# file run once manually to correct some zip codes that had been miscoded (e.g. 06840 was 6840) - hopefully won't need again
python find_low_zips.py

# convert academic dataset json files to csv (change file names)
python json_to_csv_converter.py ../../Data/academic/yelp_academic_dataset_review.json



# clean dissimilarity index data - create cbsa_summary.csv
python cbsa_summary.py

# Clean ACS CBSA (MSA) data - create acs_cbsa_14.csv
python acs_cbsa.py

# clean ACS data - create acs_zipcodes_14.csv
python acs_zipcodes.py

# clean academic dataset - create yelp_academic_dataset_cleaned.csv
python academic.py

# install nltk packages
sh setup.sh

# code reviews and merge them with other datasets (e.g. ACS) - yelp_reviews_merged.csv
python merge.py




# Go into the analysis folder
cd ../analysis

# describe the dataset (yelp_reviews_merged.csv) - create yelp_reviews_descriptive.txt
python describe_basic.py

# draw a word cloud using only review text from yelp_reviews_only.csv
python word_cloud.py




## OUTDATED:
# make file with only reviews and their ID's - yelp_reviews_only.csv and yelp_reviews_only_small.csv
# python reviews_only.py

# Manually code the data set by copying and editing a small subset (yelp_reviews_only_small.csv) - create yelp_reviews_coded_small.csv
# So far, I have coded it as 0: not at all, 1: a bit, 2: a lot - or as binary (e.g. discusses_authentic)

# merge hand-coded subset back in with file of all reviews - create yelp_reviews_coded.csv
#python merge_coded.py

# train logistic regression model and label data - create yelp_reviews_classified.csv and yelp_reviews_classified_small.csv
#python classify.py