def code_chains(df):
    """ identify chain restaurants """
    chains = ['Taco Bell', 'Chipotle Mexican Grill', "Moe's Southwest Grill", "Del Taco", "Roberto's Taco Shop", "El Pollo Loco",
    "Rubio's Fresh Mexican Grill", "Qdoba Mexican Grill", "Baja Fresh Mexican Grill", "Filiberto's Mexican Food", "Freebirds World Burrito",
    "Papa John's Pizza", "Domino's Pizza", 'Pizza Hut', "Barro's Pizza", "Rosati's Pizza", "Peter Piper Pizza",
    'Olive Garden Italian Restaurant', "Jimmy John's", "Jersey Mike's Subs", "Panera Bread", "Arby's", "Dairy Queen",
    'In-N-Out Burger', "In & Out Burger", "McDonald's", "Burger King", "Jack in the Box", "Jack In the Box", "Carl's Jr", "Carl's Jr.",
    "Sonic Drive-In", "Smashburger",  "Five Guys Burgers and Fries", "Red Robin Gourmet Burgers", "Fatburger", "Whataburger",
    "Johnny Rockets", "Port of Subs", "Capriotti's Sandwich Shop", "Quiznos", "Firehouse Subs",
    "Streets of New York", "Outback Steakhouse", "Culver's", "Chick-Fil-A", "Chick-fil-A", "Tropical Smoothie Cafe",
    "Subway", "Panda Express", "Applebee's", "Chili's Grill & Bar", "Denny's", "Dennys", "Little Caesars Palace",
    "Wendy's", "KFC", "Kfc", "IHOP", "Buffalo Wild Wings", "Einstein Bros Bagels", "PT's", "Waffle House", "P F Chang's China Bistro"]
    chains_lower = [chain.lower() for chain in chains]

    for col in ['name_business', 'business_name']:
        if col in df.columns:
            business_var = col

    df[business_var] = df[business_var].str.replace(u'\xe2\x80\x99', "'")

    df['is_chain'] = df[business_var].isin(chains).astype(int)
    # Also check if the lower case name matches
    df.loc[df[business_var].isin(chains_lower), 'is_chain'] = 1
    return df