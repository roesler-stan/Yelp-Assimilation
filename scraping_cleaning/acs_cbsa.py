"""
Make acs_msa_14.csv, MSA-level ACS demographic data

Data sources:
    MSA's (310), 2014 5-year estimages

    total residents: S0101: ACS_15_1YR_S0101_with_ann.csv
    mean income: S1902, ACS_14_5YR_S1902_with_ann.csv
    unemployment for white and hispanic people, S2301: ACS_14_5YR_S2301_with_ann.csv
    percent white and percent Hispanic: DP05: ACS_14_5YR_DP05_with_ann.csv
    foreign born: S0501: ACS_14_5YR_S0501_with_ann.csv
    education for whites: ACS_14_5YR_C15002A_with_ann.csv
    education for Hispanics ACS_14_5YR_C15002I_with_ann.csv
    language spoken at home: S1601: ACS_14_5YR_S1601_with_ann.csv
    nativity for whites: B05003A: ACS_14_5YR_B05003A_with_ann.csv
    nativity for hispanics: B05003H: ACS_14_5YR_B05003H_with_ann.csv
    year of entry by nativity: B05005: ACS_14_5YR_B05005_with_ann.csv
"""

import pandas as pd
import re

def main():
    in_directory = '../../Data/acs cbsa/'
    outfile = '../../Data/acs_cbsa_14.csv'

    residents_filename = in_directory + 'ACS_15_1YR_S0101_with_ann.csv'
    inc_filename = in_directory + 'ACS_14_5YR_S1902_with_ann.csv'
    emp_filename = in_directory + 'ACS_14_5YR_S2301_with_ann.csv'
    hisp_filename = in_directory + 'ACS_14_5YR_DP05_with_ann.csv'
    foreign_filename = in_directory + 'ACS_14_5YR_S0501_with_ann.csv'
    educ_filenames = [in_directory + col for col in ['ACS_14_5YR_C15002A_with_ann.csv', 'ACS_14_5YR_C15002I_with_ann.csv']]
    language_filename = in_directory + 'ACS_14_5YR_S1601_with_ann.csv'
    nativity_filenames = [in_directory + col for col in ['ACS_14_5YR_B05003A_with_ann.csv', 'ACS_14_5YR_B05003H_with_ann.csv']]
    nativity_year_filename = in_directory + 'ACS_14_5YR_B05005_with_ann.csv'
    
    residents_data = residents(residents_filename)
    inc_data = clean_inc(inc_filename)
    emp_data = emp(emp_filename)
    hisp_data = hispanic(hisp_filename)
    foreign_data = foreign_born(foreign_filename)
    educ_data = educ(educ_filenames)
    language_data = language(language_filename)
    nativity_data = nativity(nativity_filenames)
    nativity_year_data = nativity_year(nativity_year_filename, residents_data)

    full_data = pd.merge(residents_data, inc_data, how = 'outer', on = ['Id2', 'Geography'])
    full_data = pd.merge(full_data, emp_data, how = 'outer', on = ['Id2', 'Geography'])
    full_data = pd.merge(full_data, hisp_data, how = 'outer', on = ['Id2', 'Geography'])
    full_data = pd.merge(full_data, foreign_data, how = 'outer', on = ['Id2', 'Geography'])
    full_data = pd.merge(full_data, educ_data, how = 'outer', on = ['Id2', 'Geography'])
    full_data = pd.merge(full_data, language_data, how = 'outer', on = ['Id2', 'Geography'])
    full_data = pd.merge(full_data, nativity_data, how = 'outer', on = ['Id2', 'Geography'])
    full_data = pd.merge(full_data, nativity_year_data, how = 'outer', on = ['Id2', 'Geography'])

    full_data['nativity_pct_foreign_hispanic'] = ((full_data['nativity_h_noncitizen'] + full_data['nativity_h_foreign_naturalised']) \
        / full_data['total_residents']) * 100
    full_data['nativity_pct_noncitizen_hispanic'] = (full_data['nativity_h_noncitizen'] / full_data['total_residents']) * 100

    full_data = full_data.rename(columns = {'Id2': 'cbsaid', 'Geography': 'cbsaname'})
    full_data = make_floats(full_data)
    full_data.to_csv(outfile, header = True, index = False, quotechar = '"')

def residents(filename):
    df = read_noheaders(filename)
    df = df.rename(columns = {'Total; Estimate; Total population': 'total_residents'})
    df = df[['Id2', 'Geography', 'total_residents']]
    return df

def clean_inc(filename):
    df = read_noheaders(filename)
    df = df.rename(columns = {'Mean income (dollars); Estimate; All households': 'mean_inc'})
    df = df[['Id2', 'Geography', 'mean_inc']]
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

    desired_cols = ['Id2', 'Geography', total_name, unemp_onerace, w_unemp, b_unemp, h_unemp]
    df = df[desired_cols]
    df = df.rename(columns = {total_name: 'total_unemp', unemp_onerace: 'one_race_unemp', w_unemp: 'w_unemp', b_unemp: 'b_unemp', h_unemp: 'h_unemp'})
    df = df.rename(columns = lambda x: x.lower())
    df = df.rename(columns = {'id2': 'Id2', 'geography': 'Geography'})

    return df

def hispanic(filename):
    """ Ethnicity data """
    df = read_noheaders(filename)
    df = df.rename(columns = {'Percent; HISPANIC OR LATINO AND RACE - Total population - Hispanic or Latino (of any race) - Mexican': 'ethnicity_mexican_percent',
        'Percent; HISPANIC OR LATINO AND RACE - Total population - Not Hispanic or Latino - White alone': 'ethnicity_white_percent'})
    df = df[['Id2', 'Geography', 'ethnicity_mexican_percent', 'ethnicity_white_percent']]
    return df

def foreign_born(filename):
    df = read_noheaders(filename)
    df['percent_foreign_born'] = (df['Foreign born; Estimate; Total population'] / df['Total; Estimate; Total population']) * 100
    df = df[['Id2', 'Geography', 'percent_foreign_born']]
    return df

def educ(filenames):
    white_educ = read_noheaders(filenames[0])
    hispanic_educ = read_noheaders(filenames[1])

    white_educ['white_educ_lt_hs'] = ((white_educ['Estimate; Male: - Less than high school diploma'] + white_educ['Estimate; Female: - Less than high school diploma']) / white_educ['Estimate; Total:']) * 100
    white_educ['white_educ_hs'] = ((white_educ['Estimate; Male: - High school graduate (includes equivalency)'] + white_educ['Estimate; Female: - High school graduate (includes equivalency)']) / white_educ['Estimate; Total:']) * 100
    white_educ['white_educ_some_college'] = ((white_educ["Estimate; Male: - Some college or associate's degree"] + white_educ["Estimate; Female: - Some college or associate's degree"]) / white_educ['Estimate; Total:']) * 100
    white_educ['white_educ_bachelors_plus'] = ((white_educ["Estimate; Male: - Bachelor's degree or higher"] + white_educ["Estimate; Female: - Bachelor's degree or higher"]) / white_educ['Estimate; Total:']) * 100

    hispanic_educ['hispanic_educ_lt_hs'] = ((hispanic_educ['Estimate; Male: - Less than high school diploma'] + hispanic_educ['Estimate; Female: - Less than high school diploma']) / hispanic_educ['Estimate; Total:']) * 100
    hispanic_educ['hispanic_educ_hs'] = ((hispanic_educ['Estimate; Male: - High school graduate (includes equivalency)'] + hispanic_educ['Estimate; Female: - High school graduate (includes equivalency)']) / hispanic_educ['Estimate; Total:']) * 100
    hispanic_educ['hispanic_educ_some_college'] = ((hispanic_educ["Estimate; Male: - Some college or associate's degree"] + hispanic_educ["Estimate; Female: - Some college or associate's degree"]) / hispanic_educ['Estimate; Total:']) * 100
    hispanic_educ['hispanic_educ_bachelors_plus'] = ((hispanic_educ["Estimate; Male: - Bachelor's degree or higher"] + hispanic_educ["Estimate; Female: - Bachelor's degree or higher"]) / hispanic_educ['Estimate; Total:']) * 100

    white_educ = white_educ[['Id2', 'Geography', 'white_educ_lt_hs', 'white_educ_hs', 'white_educ_some_college', 'white_educ_bachelors_plus']]
    hispanic_educ = hispanic_educ[['Id2', 'Geography', 'hispanic_educ_lt_hs', 'hispanic_educ_hs', 'hispanic_educ_some_college', 'hispanic_educ_bachelors_plus']]

    educ_df = white_educ.merge(hispanic_educ, on = ['Id2', 'Geography'], how = 'outer')
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
    df = df[['Id2', 'Geography', 'language_english', 'language_spanish', 'language_spanish_english_well', 'language_spanish_english_notwell']]
    return df

def nativity(filenames):
    white_nativity = read_noheaders(filenames[0])
    hispanic_nativity = read_noheaders(filenames[1])
    d = {'w': white_nativity, 'h': hispanic_nativity}

    for race, df in d.items():
        native = []
        foreign_naturalised = []
        noncitizen = []
        for age in ['Under 18 years', '18 years and over']:
            for gender in ['Male', 'Female']:
                native.append('Estimate; ' + gender + ': - ' + age + ': - Native')
                foreign_naturalised.append('Estimate; ' + gender + ': - ' + age + ': - Foreign born: - Naturalized U.S. citizen')
                noncitizen.append('Estimate; ' + gender + ': - ' + age + ': - Foreign born: - Not a U.S. citizen')
        
        total_var = race + '_total'
        native_var = race + '_native'
        foreign_naturalised_var = race + '_foreign_naturalised'
        noncitizen_var = race + '_noncitizen'
        foreign_pct_var = race + '_foreign_pct'
        noncitizen_pct_var = race + '_noncitizen_pct'
        native_to_foreign_var = race + '_native_to_foreign'
        
        df[native_var] = df[native].sum(axis = 1)
        df[foreign_naturalised_var] = df[foreign_naturalised].sum(axis = 1)
        df[noncitizen_var] = df[noncitizen].sum(axis = 1)
        df[total_var] = df[native_var] + df[foreign_naturalised_var] + df[noncitizen_var]
        df[foreign_pct_var] = ((df[foreign_naturalised_var] + df[noncitizen_var]) / df[total_var]) * 100
        df[noncitizen_pct_var] = (df[noncitizen_var] / df[total_var]) * 100
        df[native_to_foreign_var] = df[native_var] / (df[foreign_naturalised_var] + df[noncitizen_var])
        df = df[['Id2', 'Geography', native_var, foreign_naturalised_var, noncitizen_var, total_var, foreign_pct_var, noncitizen_pct_var,
        native_to_foreign_var]]

    df = white_nativity.merge(hispanic_nativity, on = ['Id2', 'Geography'], how = 'outer')
    df = df.rename(columns = lambda x: 'nativity_' + x)
    df = df.rename(columns = {'nativity_Id2': 'Id2', 'nativity_Geography': 'Geography'})
    return df

def nativity_year(filename, residents_data):
    df = read_noheaders(filename)
    residents = residents_data[['Id2', 'Geography', 'total_residents']]
    df = df.merge(residents, on = ['Id2', 'Geography'], how = 'left')

    entered_10_later = df['Estimate; Entered 2010 or later - Foreign born:']
    entered_00to09 = df['Estimate; Entered 2000 to 2009 - Foreign born:']
    entered_90to99 = df['Estimate; Entered 1990 to 1999: - Foreign born:']
    entered_before_90 = df['Estimate; Entered before 1990: - Foreign born:']
    entered_foreign = entered_10_later + entered_00to09 + entered_90to99 + entered_before_90
    total = df['total_residents']

    df['pct_foreign_entered'] = (entered_foreign / total) * 100
    df['pct_foreign_entered_after_2010'] = (entered_10_later / total) * 100
    df['pct_foreign_entered_00to09'] = (entered_00to09 / total) * 100
    df['pct_foreign_entered_90to99'] = (entered_90to99 / total) * 100
    df['pct_foreign_entered_before_90'] = (entered_before_90 / total) * 100
    df['pct_foreign_entered_before_2000'] = ((entered_before_90 + entered_90to99) / total) * 100
    df['pct_foreign_entered_before_2010'] = ((entered_before_90 + entered_90to99 + entered_00to09) / total) * 100
    df['pct_foreign_entered_after_1999'] = ((entered_00to09 + entered_10_later) / total) * 100
    df['pct_foreign_entered_after_1989'] = ((entered_90to99 + entered_00to09 + entered_10_later) / total) * 100
    df = df[['Id2', 'Geography', 'pct_foreign_entered', 'pct_foreign_entered_after_2010', 'pct_foreign_entered_00to09',
    'pct_foreign_entered_90to99', 'pct_foreign_entered_before_90', 'pct_foreign_entered_before_2000', 'pct_foreign_entered_before_2010',
    'pct_foreign_entered_after_1999', 'pct_foreign_entered_after_1989']]

    df = df.rename(columns = lambda x: 'nativity_' + x)
    df = df.rename(columns = {'nativity_Id2': 'Id2', 'nativity_Geography': 'Geography'})
    return df

def read_noheaders(filename):
    df = pd.read_csv(filename, skiprows = 1)
    return df

def make_floats(df):
    for col in df.columns:
        df[col] = df[col].convert_objects(convert_numeric=True)
    return df

if __name__ == '__main__':
    main()