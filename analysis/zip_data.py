import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import pandas as pd
import numpy as np

def main():
    in_directory = "/Users/katharina/Dropbox/Projects/Yelp/Data/"
    out_directory = "/Users/katharina/Dropbox/Projects/Yelp/map zipcodes/"
    infile = in_directory + "scraped.Rdata"
    outfile = out_directory + 'zip_data.csv'
    robjects.r.load(infile)
    df = robjects.r['scraped_data']
    df = pd.DataFrame(pandas2ri.ri2py(df))

    cols = ['zip_ethnicity_mexican_percent', 'mexican_present']
    all_cols = cols + ['zipcode', 'is_chain']
    df = df[all_cols]
    chains_data = df[df['is_chain'] == 1]
    nochains_data = df[df['is_chain'] == 0]

    zip_data = df.groupby('zipcode')[cols].mean().reset_index()
    zip_data['zip_ethnicity_mexican_percent'] = zip_data['zip_ethnicity_mexican_percent']
    cols.remove('zip_ethnicity_mexican_percent')

    zip_data_chains = chains_data.groupby('zipcode')[cols].mean().reset_index()
    zip_data_nochains = nochains_data.groupby('zipcode')[cols].mean().reset_index()
    zip_data_chains = zip_data_chains.rename(columns = {'mexican_present': 'mexican_present_chains'})
    zip_data_nochains = zip_data_nochains.rename(columns = {'mexican_present': 'mexican_present_nochains'})

    zip_data = zip_data.merge(zip_data_chains, on = ['zipcode'], how = 'outer')
    zip_data = zip_data.merge(zip_data_nochains, on = ['zipcode'], how = 'outer')
    zip_data['zipcode'] = zip_data['zipcode'].astype(str)
    zip_data['zipcode'] = zip_data['zipcode'].map(leading_zeros)
    zip_data['mexican_present'] = zip_data['mexican_present'] * 100
    zip_data['mexican_present_chains'] = zip_data['mexican_present_chains'] * 100
    zip_data['mexican_present_nochains'] = zip_data['mexican_present_nochains'] * 100
    zip_data = zip_data.rename(columns = {'zip_ethnicity_mexican_percent': 'residents_mexican'})

    zip_data.to_csv(outfile, index=False)

def leading_zeros(zipcode):
    leading = (5 - len(zipcode)) * "0"
    return leading + zipcode

if __name__ == "__main__":
    main()