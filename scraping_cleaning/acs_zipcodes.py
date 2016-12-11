""" Make acs_zipcodes_14.csv, zipcode-level ACS demographic data """

import pandas as pd
import re

"""
Data sources:
    5-digit zip code tabulation areas (860), 2014 5-year estimages

    race: B02001, ACS_14_5YR_B02001_with_ann.csv
    gender and age: S0101, ACS_14_5YR_S0101_with_ann.csv
    mean income: S1902, ACS_14_5YR_S1902_with_ann.csv
    unemployment for white and hispanic people, S2301: ACS_14_5YR_S2301_with_ann.csv
    percent white and percent Hispanic: DP05: ACS_14_5YR_DP05_with_ann.csv
    foreign born: S0501: ACS_14_5YR_S0501_with_ann.csv
    education for whites: ACS_14_5YR_C15002A_with_ann.csv
    education for Hispanics ACS_14_5YR_C15002I_with_ann.csv
    language spoken at home: S1601: ACS_14_5YR_S1601_with_ann.csv
"""

def main():
    in_directory = '../../Data/acs zipcodes/'
    outfile = '../../Data/acs_zipcodes_14.csv'

    race_filename = in_directory + 'ACS_14_5YR_B02001_with_ann.csv'
    gender_filename = in_directory + 'ACS_14_5YR_S0101_with_ann.csv'
    inc_filename = in_directory + 'ACS_14_5YR_S1902_with_ann.csv'
    emp_filename = in_directory + 'ACS_14_5YR_S2301_with_ann.csv'
    hisp_filename = in_directory + 'ACS_14_5YR_DP05_with_ann.csv'
    foreign_filename = in_directory + 'ACS_14_5YR_S0501_with_ann.csv'
    educ_filenames = [in_directory + col for col in ['ACS_14_5YR_C15002A_with_ann.csv', 'ACS_14_5YR_C15002I_with_ann.csv']]
    language_filename = in_directory + 'ACS_14_5YR_S1601_with_ann.csv'
    
    full_data = clean_race(race_filename)
    gender_age_data = gender_age(gender_filename)
    inc_data = clean_inc(inc_filename)
    emp_data = emp(emp_filename)
    hisp_data = hispanic(hisp_filename)
    foreign_data = foreign_born(foreign_filename)
    educ_data = educ(educ_filenames)
    language_data = language(language_filename)

    full_data = pd.merge(full_data, gender_age_data, how = 'outer', on = 'Geography')
    full_data = pd.merge(full_data, inc_data, how = 'outer', on = 'Geography')
    full_data = pd.merge(full_data, emp_data, how = 'outer', on = 'Geography')
    full_data = pd.merge(full_data, hisp_data, how = 'outer', on = 'Geography')
    full_data = pd.merge(full_data, foreign_data, how = 'outer', on = 'Geography')
    full_data = pd.merge(full_data, educ_data, how = 'outer', on = 'Geography')
    full_data = pd.merge(full_data, language_data, how = 'outer', on = 'Geography')
    
    full_data['Geography'] = full_data['Geography'].map(remove_text)
    full_data = full_data.rename(columns = {'Geography': 'zipcode'})
    full_data = make_floats(full_data)
    full_data.to_csv(outfile, header = True, index = False, quotechar = '"')

# Calculating resident percentages
def clean_race(race_filename):
    df = read_noheaders(race_filename)

    good_columns = [col for col in df.columns if 'Margin' not in col]
    df = df[good_columns]
    df = df.drop(df[['Id', 'Id2']], axis = 1)

    df = df.rename(columns = lambda x: x.replace('Estimate; Total: - ', ''))
    df = df.rename(columns = lambda x: x.split(' alone')[0].lower())
   
    df = df.rename(columns = {'white':'w_residents', 'black or african american':'b_residents',
        'american indian and alaska native':'i_residents', 'asian':'a_residents', 'native hawaiian and other pacific islander':'h_residents',
        'some other race':'o_residents', 'two or more races:':'m_residents', 'two or more races: - two races including some other race': 'mi_residents',
        'two or more races: - two races excluding some other race, and three or more races':'mt_residents',
        'estimate; total:':'total_residents', 'geography': 'Geography'})
    
    df.loc[df['total_residents'] != 0, 'b_residents_percent'] = (df.loc[df['total_residents'] != 0, 'b_residents'] / df.loc[df['total_residents'] != 0, 'total_residents']) * 100
    df.loc[df['total_residents'] != 0, 'w_residents_percent'] = (df.loc[df['total_residents'] != 0, 'w_residents'] / df.loc[df['total_residents'] != 0, 'total_residents']) * 100
    df.loc[df['total_residents'] != 0, 'h_residents_percent'] = (df.loc[df['total_residents'] != 0, 'h_residents'] / df.loc[df['total_residents'] != 0, 'total_residents']) * 100
    df['nonw_residents_percent'] = 100 - df['w_residents_percent']
    
    return df

def gender_age(filename):
    df = read_noheaders(filename)
        
    desired_cols = ['Geography', 'Total; Estimate; Total population', 'Male; Estimate; Total population',
                    'Total; Estimate; AGE - 15 to 19 years', 'Male; Estimate; AGE - 15 to 19 years',
                    'Total; Estimate; AGE - 20 to 24 years', 'Male; Estimate; AGE - 20 to 24 years']                    
    df = df[desired_cols]
    
    df = df.rename(columns = lambda x: re.sub('; Estimate; ','', x))
    df = df.rename(columns = lambda x: re.sub('Total population','', x))
    df = df.rename(columns = lambda x: re.sub('AGE - 15 to 19 years','_15_19', x))
    df = df.rename(columns = lambda x: re.sub('AGE - 20 to 24 years','_20_24', x))
    df = df.rename(columns = {'Total': 'total_gender'})    
    df = df.rename(columns = lambda x: x.lower())
    df = df.rename(columns = {'male': 'male_residents', 'geography': 'Geography'})

    df = make_floats(df)
    df['percent_male'] = (df['male_residents'] / df['total_gender']) * 100
            
    return df

def clean_inc(filename):
    df = read_noheaders(filename)
    df = df.rename(columns = {'Mean income (dollars); Estimate; All households': 'mean_inc'})
    df = df[['Geography', 'mean_inc']]
    return df

def emp(filename):
    """ Total and black, white, and hispanic unemployment rates
    Measures for black and white can include hispanics, b/c that's all we have for black people """
    df = read_noheaders(filename)
    
    unemp_name = 'Unemployment rate; Estimate; '
    total_name = unemp_name + 'Population 16 years and over'
    unemp_onerace = unemp_name + 'RACE AND HISPANIC OR LATINO ORIGIN - One race'

    w_unemp = unemp_onerace + ' - White'
    b_unemp = unemp_onerace + ' - Black or African American'
    h_unemp = unemp_name + 'Hispanic or Latino origin (of any race)'

    desired_cols = ['Geography', total_name, unemp_onerace, w_unemp, b_unemp, h_unemp]
    df = df[desired_cols]
    df = df.rename(columns = {total_name: 'total_unemp', unemp_onerace: 'one_race_unemp', w_unemp: 'w_unemp', b_unemp: 'b_unemp', h_unemp: 'h_unemp'})
    df = df.rename(columns = lambda x: x.lower())
    df = df.rename(columns = {'geography': 'Geography'})

    return df

def hispanic(filename):
    """ Ethnicity data """
    df = read_noheaders(filename)
    df = df.rename(columns = {'Percent; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race) - Mexican': 'ethnicity_mexican_percent',
        'Percent; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - White alone': 'ethnicity_white_percent'})
    df = df[['Geography', 'ethnicity_mexican_percent', 'ethnicity_white_percent']]
    return df

def foreign_born(filename):
    df = read_noheaders(filename)
    df['percent_foreign_born'] = df['Foreign born; Estimate; Total population'] / df['Total; Estimate; Total population']
    df = df[['Geography', 'percent_foreign_born']]
    return df

def educ(filenames):
    white_educ = read_noheaders(filenames[0])
    hispanic_educ = read_noheaders(filenames[1])

    white_educ['white_educ_lt_hs'] = (white_educ['Estimate; Male: - Less than high school diploma'] + white_educ['Estimate; Female: - Less than high school diploma']) / white_educ['Estimate; Total:']
    white_educ['white_educ_hs'] = (white_educ['Estimate; Male: - High school graduate (includes equivalency)'] + white_educ['Estimate; Female: - High school graduate (includes equivalency)']) / white_educ['Estimate; Total:']
    white_educ['white_educ_some_college'] = (white_educ["Estimate; Male: - Some college or associate's degree"] + white_educ["Estimate; Female: - Some college or associate's degree"]) / white_educ['Estimate; Total:']
    white_educ['white_educ_bachelors_plus'] = (white_educ["Estimate; Male: - Bachelor's degree or higher"] + white_educ["Estimate; Female: - Bachelor's degree or higher"]) / white_educ['Estimate; Total:']

    hispanic_educ['hispanic_educ_lt_hs'] = (hispanic_educ['Estimate; Male: - Less than high school diploma'] + hispanic_educ['Estimate; Female: - Less than high school diploma']) / hispanic_educ['Estimate; Total:']
    hispanic_educ['hispanic_educ_hs'] = (hispanic_educ['Estimate; Male: - High school graduate (includes equivalency)'] + hispanic_educ['Estimate; Female: - High school graduate (includes equivalency)']) / hispanic_educ['Estimate; Total:']
    hispanic_educ['hispanic_educ_some_college'] = (hispanic_educ["Estimate; Male: - Some college or associate's degree"] + hispanic_educ["Estimate; Female: - Some college or associate's degree"]) / hispanic_educ['Estimate; Total:']
    hispanic_educ['hispanic_educ_bachelors_plus'] = (hispanic_educ["Estimate; Male: - Bachelor's degree or higher"] + hispanic_educ["Estimate; Female: - Bachelor's degree or higher"]) / hispanic_educ['Estimate; Total:']

    white_educ = white_educ[['Geography', 'white_educ_lt_hs', 'white_educ_hs', 'white_educ_some_college', 'white_educ_bachelors_plus']]
    hispanic_educ = hispanic_educ[['Geography', 'hispanic_educ_lt_hs', 'hispanic_educ_hs', 'hispanic_educ_some_college', 'hispanic_educ_bachelors_plus']]

    educ_df = white_educ.merge(hispanic_educ, on = ['Geography'], how = 'outer')
    return educ_df

def language(filename):
    """ Percent of population over 5 years old, language spoken at home """
    df = read_noheaders(filename)
    # Calculate percentage of total population who is Spanish speaker and speaks English well or not well
    df['language_spanish_english_well'] = pd.to_numeric(df['Percent of specified language speakers  - Speak English "very well"; Estimate; Population 5 years and over'], errors='coerce') \
    * (pd.to_numeric(df['Total; Estimate; Speak a language other than English - Spanish or Spanish Creole'], errors="coerce")/ 100)
    df['language_spanish_english_notwell'] = pd.to_numeric(df['Percent of specified language speakers  - Speak English  less than "very well"; Estimate; Population 5 years and over'], errors="coerce") \
    * (pd.to_numeric(df['Total; Estimate; Speak a language other than English - Spanish or Spanish Creole'], errors="coerce") / 100)

    df = df.rename(columns = {'Total; Estimate; Speak a language other than English - Spanish or Spanish Creole': 'language_spanish',
        'Total; Estimate; Speak only English': 'language_english'})
    df = df[['Geography', 'language_english', 'language_spanish', 'language_spanish_english_well', 'language_spanish_english_notwell']]
    return df

def remove_text(zip_string):
    if 'ZCTA5 ' in zip_string:
        return zip_string.split('ZCTA5 ')[1]
    else:
        return numpy.nan

def read_noheaders(filename):
    df = pd.read_csv(filename, skiprows = 1)
    return df

def make_floats(df):
    for col in df.columns:
        df[col] = df[col].convert_objects(convert_numeric=True)

    return df

if __name__ == '__main__':
    main()