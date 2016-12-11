import pandas as pd
import sys

def main():
    data_directory = '../../Data/'
    infile = data_directory + 'yelp_reviews_merged.csv'
    basic_file = data_directory + 'yelp_reviews_descriptive.txt'

    df = pd.read_csv(infile)
    basic_stats(df, basic_file)

def basic_stats(df, basic_file):
    orig_stdout = sys.stdout
    f = file(basic_file, 'w')
    sys.stdout = f

    print 'Number of reviews: ' + str(len(df.index)) + '\n'

    print 'Number of businesses: ' + str(len(df['business_id'].unique())) + '\n'

    print 'Number of zip codes: ' + str(len(df['zipcode'].unique())) + '\n'
    print 'Number of zip codes with ACS demographic data: ' + str(len(df['zip_zipcode'].unique())) + '\n'


    print 'Number of CBSA: ' + str(len(df['cbsa'].unique())) + '\n'
    print 'Number of CBSA with dissimilarity data: ' + str(len(df['cbsa_cbsaid'].unique())) + '\n'

    print 'Number of states: ' + str(len(df['state'].unique()))

    sys.stdout = orig_stdout
    f.close()

if __name__ == '__main__':
    main()