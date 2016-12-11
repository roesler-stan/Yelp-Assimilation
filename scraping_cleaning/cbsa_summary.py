import pandas as pd
import re

"""
    http://www.arcgis.com/home/item.html?id=e6c5bea934a043b5966e14aab4137348    
"""

def main():
    in_directory = '../../Data/cbsa_summary/'
    infile = in_directory + 'CBSA_Summary.csv'
    outfile = '../../Data/cbsa_summary.csv'

    df = pd.read_csv(infile)
    df = clean_data(df)
    df.to_csv(outfile, index = False, header = True)

def clean_data(df):
    # columns to keep
    cols = ['CBSAID', 'CBSANAME', 'Total_Male', 'Total_Female', 'Total_under18', 'Total_18_64', 'Total_over64',
    'WHITE', 'BLACK', 'HISP', 'NATIVE', 'asian_pi']
    cols += [c for c in df.columns if 'dissim' in c]
    cols += [c for c in df.columns if 'perc' in c]
    # Remove 1990 variables
    cols = [c for c in cols if '_1990' not in c]
    # remove disability variables
    disability_text = re.compile('self_care|disabl|ambulatory|_hear|indep_living|cognitive|_vision', re.I)
    cols = [c for c in cols if not re.search(disability_text, c)]

    cols = list(set(cols))

    # put id columns first
    cols.remove('CBSAID')
    cols.remove('CBSANAME')
    cols = ['CBSAID', 'CBSANAME'] + cols
    
    df = df[cols]
    df.rename(columns = lambda x: x.lower(), inplace = True)
    return df

if __name__ == '__main__':
    main()