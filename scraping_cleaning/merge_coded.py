""" Merge the manually coded subset back into the full data set - create yelp_reviews_coded.csv """

import pandas

def main():
    data_directory = '../../Data/'
    infile = data_directory + 'yelp_reviews_coded_small.csv'
    original_file = data_directory + 'yelp_reviews_only.csv'
    outfile = data_directory + 'yelp_reviews_coded.csv'

    dataset_coded = pandas.read_csv(infile)
    dataset_original = pandas.read_csv(original_file)

    reviews_coded = dataset_coded['review_id'].tolist()

    ## Throw out the rows that were coded from the original data set
    dataset_original = dataset_original[~dataset_original['review_id'].isin(reviews_coded)]

    ## Append the original data set to the rows that were coded
    dataset = dataset_coded.append(dataset_original)

    dataset.to_csv(outfile, index = False)

if __name__ == '__main__':
    main()