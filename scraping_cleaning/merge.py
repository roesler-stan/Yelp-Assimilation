""" Merge the classified reviews with their original data as well as zip code and CBSA data """

import pandas as pd
import code_reviews as cr
import code_chains as cc

def main():
    data_directory = '../../Data/'
    crosswalks_directory = data_directory + 'crosswalks/'

    infile = data_directory + 'reviews_0to500.csv'
    outfile = data_directory + 'yelp_reviews_merged.csv'
    outfile_small = data_directory + 'yelp_reviews_merged_small.csv'

    acs_zip_file = data_directory + 'acs_zipcodes_14.csv'
    cbsa_summary_file = data_directory + 'cbsa_summary.csv'
    acs_cbsa_file = data_directory + 'acs_cbsa_14.csv'

    # zip code crosswalks from http://www2.census.gov/geo/docs/maps-data/data/rel/...
    zip_to_county_file = crosswalks_directory + 'zcta_county_rel_10.txt'
    zip_to_cbsa_file = crosswalks_directory + 'zcta_cbsa_rel_10.txt'

    # state codes come from https://www.census.gov/geo/reference/ansi_statetables.html
    states_file = crosswalks_directory + 'state_fips.csv'

    df = clean_reviews(infile)
    filenames = (acs_zip_file, zip_to_county_file, zip_to_cbsa_file, states_file, cbsa_summary_file, acs_cbsa_file)
    df = merge_data(df, filenames)

    cps_file = data_directory + 'cps_intermarriage_stats.csv'
    cps_data = pd.read_csv(cps_file)
    df = df.merge(cps_data, left_on = ['cbsa'], right_on = ['metfips'], suffixes = ['', '_cps'], how = 'left')
    
    df.to_csv(outfile, index = False, header = True)
    df[:100].to_csv(outfile_small, index = False, header = True)

def clean_reviews(infile):
    df = pd.read_csv(infile)
    df = df.rename(columns = {'review': 'text'})
    df['categories'] = df['category1'].astype(str) + ', ' + df['category2'].astype(str) + ', ' + df['category3'].astype(str) + \
     ', ' + df['category4'].astype(str) + ', ' + df['category5'].astype(str)

    # Code categories (Mexican, Italian, or American) - required before running code_themes
    df = cr.categories(df)
    # Code reviews for themes
    df = cr.code_themes(df)
    # Label chains
    df = cc.code_chains(df)

    return df

def merge_data(df, filenames):
    """ Keep in mind that zip codes have been converted to floats, so they do not have leading zeros """
    dfs = read_data(df, filenames)
    dfs = clean_data(dfs)
    df, acs_zip_data, zip_to_county_data, zip_to_cbsa_data, states_data, cbsa_summary_data, acs_cbsa_data = dfs

    # Add zipcode-level demographic data
    acs_zip_data.rename(columns = lambda x: 'zip_' + x, inplace = True)
    df = df.merge(acs_zip_data, left_on = ['zipcode'], right_on = ['zip_zipcode'], suffixes = ['', '_acs_zip'], how = 'left')

    # Add county, CBSA, and state number from crosswalks
    df = df.merge(zip_to_county_data, left_on = ['zipcode'], right_on = ['zipcode'], suffixes = ['', '_cw_county'], how = 'left')
    df = df.merge(zip_to_cbsa_data, left_on = ['zipcode'], right_on = ['zipcode'], suffixes = ['', '_cw_cbsa'], how = 'left')
    df = df.merge(states_data, left_on = ['state_number'], right_on = ['state_number'], suffixes = ['', '_cw_state'], how = 'left')

    # Add CBSA-level summary data
    cbsa_summary_data.rename(columns = lambda x: 'cbsa_summary_' + x, inplace = True)
    df = df.merge(cbsa_summary_data, left_on = ['cbsa'], right_on = ['cbsa_summary_cbsaid'], suffixes = ['', '_cbsa_summary'], how = 'left')

    # Add ACS CBSA data
    acs_cbsa_data.rename(columns = lambda x: 'cbsa_' + x, inplace = True)
    df = df.merge(acs_cbsa_data, left_on = ['cbsa'], right_on = ['cbsa_cbsaid'], suffixes = ['', '_acs_cbsa'], how = 'left')

    return df

def read_data(df, filenames):
    acs_zip_file, zip_to_county_file, zip_to_cbsa_file, states_file, cbsa_summary_file, acs_cbsa_file = filenames

    acs_zip_data = pd.read_csv(acs_zip_file)
    zip_to_county_data = pd.read_csv(zip_to_county_file)
    zip_to_cbsa_data = pd.read_csv(zip_to_cbsa_file)
    states_data = pd.read_csv(states_file)
    cbsa_summary_data = pd.read_csv(cbsa_summary_file)
    acs_cbsa_data = pd.read_csv(acs_cbsa_file)
    
    return (df, acs_zip_data, zip_to_county_data, zip_to_cbsa_data, states_data, cbsa_summary_data, acs_cbsa_data)

def clean_data(dfs):
    df, acs_zip_data, zip_to_county_data, zip_to_cbsa_data, states_data, cbsa_summary_data, acs_cbsa_data = dfs

    zip_to_county_data = clean_crosswalk(zip_to_county_data)
    zip_to_cbsa_data = clean_crosswalk(zip_to_cbsa_data)

    ## Remove duplicate zip codes from zip code-level data
    zip_to_county_data = zip_to_county_data.drop_duplicates('zipcode')
    zip_to_cbsa_data = zip_to_cbsa_data.drop_duplicates('zipcode')

    # acs_zip_data = acs_zip_data[['zipcode', 'mean_inc', 'total_residents', 'w_residents_percent', 'b_residents_percent', 'h_residents_percent',
    # 'nonw_residents_percent', 'total_unemp', 'one_race_unemp', 'w_unemp', 'b_unemp', 'h_unemp']]
    zip_to_county_data = zip_to_county_data[['zipcode', 'county', 'state_number', 'zpop']]
    zip_to_cbsa_data = zip_to_cbsa_data[['zipcode', 'cbsa']]

    states_data = clean_states(states_data)

    return (df, acs_zip_data, zip_to_county_data, zip_to_cbsa_data, states_data, cbsa_summary_data, acs_cbsa_data)

def clean_crosswalk(df):
    df.rename(columns = lambda x: x.lower(), inplace = True)
    df.rename(columns = {'zcta5': 'zipcode', 'state': 'state_number'}, inplace = True)
    return df

def clean_states(df):
    df.rename(columns = lambda x: x.lower(), inplace = True)
    df.rename(columns = {'state': 'state_name', 'fips': 'state_number', 'usps': 'state'}, inplace = True)
    df['state'] = df['state'].str.lower()
    return df

if __name__ == '__main__':
    main()