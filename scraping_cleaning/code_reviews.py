import re

# Concept to look for and its regular expression
regex_dict = {'strange': 'strange|weird|foreign',
'authentic': 'authentic|tradition|real(\\b|$)',
'ranking': 'best|worst|average',
'frequency': 'often|always|week|day|daily',
'authority': 'expert|connoisseur|aholic',
'partner': 'girlfriend|boyfriend|(\\bgf\\b)|(\\bbf\\b)',
'family': 'girlfriend|boyfriend|(\\bgf\\b)|(\\bbf\\b)|wife|husband|hubby|mom|dad|mother|father|son|daughter|kids|partner',
'service': 'staff|employee|service',
'spicy': 'spicy|spice|hot',
'exotic': 'exotic|adventur|rare',
'maternal': 'grandma|grandmother|nana|nonna|abuela|abuelita|nonnie|nona|nana',
'mexican': 'mexican|mexico',
'italian': 'italian|italy',
'american': '(A|a)merica|\\bUSA\\b|\\bUS\\b|(U|u)nited (S|s)tates'} # Keep case for USA and US

def code_themes(df):
    """ Create column with word count for each review and rename 'text' to 'review'
    Requires categories to be run beforehand
    """
    # \S matches non-whitespace, so this counts the number of multiple non-whitespace groups: words
    df['word_count'] = df['text'].str.count('\S+', flags = re.I)
    df['characters_count'] = df['text'].str.len()

    for var, regex in regex_dict.items():
        # Use case to find 'USA' and 'US'
        if var == 'american':
            df[var + '_present'] = df['text'].str.contains(regex, na=False).astype(float)
            df[var + '_count'] = df['text'].str.count(regex)
        else:
            df[var + '_present'] = df['text'].str.contains(regex, flags = re.I, na=False).astype(float)
            df[var + '_count'] = df['text'].str.count(regex, flags = re.I)
        df[var + '_count_perword'] = (df[var + '_count']).astype(float) / df['word_count']
        df[var + '_present_perword'] = (df[var + '_present']).astype(float) / df['word_count']

    for ethnicity in ['Mexican', 'Italian', 'American']:
        df.loc[df['category'].str.contains(ethnicity, flags=re.I), 'ethnicity_count'] = df.loc[df['category'].str.contains(ethnicity, flags=re.I), ethnicity.lower() + '_count']
        df.loc[df['category'].str.contains(ethnicity, flags=re.I), 'ethnicity_present'] = df.loc[df['category'].str.contains(ethnicity, flags=re.I), ethnicity.lower() + '_present']
        df.loc[df['category'].str.contains(ethnicity, flags=re.I), 'ethnicity_count_perword'] = df.loc[df['category'].str.contains(ethnicity, flags=re.I), ethnicity.lower() + '_count_perword']
        df.loc[df['category'].str.contains(ethnicity, flags=re.I), 'ethnicity_present_perword'] = df.loc[df['category'].str.contains(ethnicity, flags=re.I), ethnicity.lower() + '_present_perword']

    # Find mention of food poisoning, excluding "sick of" language
    food_poisoning = '(^|\W)(poison|diarr?h|diarr?ea|sick(?! of )|puke|throw up|vomit)'
    df['food_poisoning'] = df['text'].str.contains(food_poisoning, flags=re.I, na=False).astype(int)

    return df

def categories(df):
    """ Code the category for ethnicities of interest and remove all other restaurants, assumes that ethnicities don't overlap """
    ethnicities = ['Mexican', 'Italian', 'American']
    df['num_categories'] = 0
    for ethnicity in ethnicities:
        df.loc[df['categories'].str.contains(ethnicity, flags=re.I, na=False, case=False), 'category'] = ethnicity
        df.loc[df['categories'].str.contains(ethnicity, flags=re.I, na=False, case=False), 'num_categories'] += 1
    df.loc[df['category'].isnull(), 'category'] = 'Other'
    df.loc[df['num_categories'] > 1, 'category'] = 'Multiple'
    df = df[df['category'].notnull()]
    return df