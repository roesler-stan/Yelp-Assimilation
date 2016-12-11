from bs4 import BeautifulSoup
import re
import json
import pandas

def find_review(review_tag):
    review_content = review_tag.find('div', {'class': 'review-content'})        
    description_tag = review_content.find('p', {'itemprop': 'description'})
    review_text = ''
    if description_tag:
        review_text = description_tag.text.encode('ascii', 'ignore').decode('ascii').strip()
        review_text = re.sub('\t|\n|"', '', review_text)
        while '  ' in review_text:
            review_text = re.sub('  ', ' ', review_text)
    return review_text

def find_reviewer_name(review_tag, row):
    name_tag = review_tag.find('a', {'class': 'user-display-name'})
    if name_tag:
        name = name_tag.text.strip()
        first_name = name.rsplit(' ', 1)[0]
        last_name = name.rsplit(' ', 1)[-1]
        row['reviewer_name'] = name
        row['reviewer_first_name'] = first_name
        row['reviewer_last_name'] = last_name
    return row

def find_reviewer_rating(review_tag):
    """ How many rating this user gave the restaurant """
    rating_tag = review_tag.find('div', {'itemprop': 'reviewRating'})
    if rating_tag:
        return float(rating_tag.find('meta')['content'])

def find_friends(review_tag):
    """ How many friends this user has """
    friend_tag = review_tag.find('li', {'class': 'friend-count'})
    if friend_tag and friend_tag.find('b'):
        return friend_tag.find('b').text.strip()

def find_reviewer_review_counts(review_tag):
    """ How many reviews this user has ever written """
    count_tag = review_tag.find('li', {'class': 'review-count'})
    if count_tag and count_tag.find('b'):
        return count_tag.find('b').text.strip()

def find_voting_feedback(review_tag, row):
    """ How other users rated this review """
    voting_feedback = review_tag.find('div', {'class': 'rateReview voting-feedback'})
    if voting_feedback:
        voting_tags = voting_feedback.find('ul', {'class': 'voting-buttons'})
        if not voting_tags or not voting_tags.find('a'):
            return ''
        voting_links = voting_tags.findAll('a')
        for link in voting_links:
            vote_type_tag = link.find('span', {'class': 'vote-type'})
            vote_count_tag = link.find('span', {'class': 'count'})
            if vote_type_tag and vote_count_tag:
                vote_type = vote_type_tag.text.strip().lower()
                vote_count = vote_count_tag.text.strip()
                row['voted_' + vote_type] = vote_count
    return row

def find_rating(soup):
    agg_rating_tag  = soup.find('div', {'itemprop': 'aggregateRating'})
    if agg_rating_tag and agg_rating_tag.find('meta'):
        return float(agg_rating_tag.find('meta')['content'])

        rating_tag = agg_rating_tag.find('div', {'class': 'rating-very-large'})
        if rating_tag and rating_tag.find('meta'):
            return float(rating_tag.find('meta')['content'])
    else:
        rating_tag = soup.find('div', {'class': 'rating-very-large'})
        for stars in range(1, 6):
            tag = rating_tag.find('i', {'class': 'stars_' + str(stars)})
            if tag:
                return stars

def find_dollars(soup):
    dollars_tag = soup.find('div', {'class': 'price-category'})
    if dollars_tag:
        dollars_tag_span = dollars_tag.find('span', {'class': 'price-range'})
        if dollars_tag_span:
            dollars = str(dollars_tag.find('span', {'class': 'price-range'}).text.strip())
            return len(dollars)

def find_categories(soup):
    categories = []
    categories_tag = soup.find('span', {'class': 'category-str-list'})
    if categories_tag:
        categories_list = categories_tag.findAll('a')   
        for category_a in categories_list:
            category_text = str(category_a.text.strip())
            categories.append(category_text)
        return categories

def find_location(review_tag, row, states_file):
    location = ''
    location_tag = review_tag.find('li', {'class': 'user-location'})
    if location_tag:
        location = str(location_tag.text.strip().encode('utf-8'))
        row['reviewer_location'] = location
        row['reviewer_city'] = find_city(location)
        
        state, country = find_state_country(location, states_file)
        row['reviewer_state'] = state
        row['reviewer_country'] = country
    return row

def find_city(location):
    city = location.split(', ')[0]
    return re.sub('[^a-zA-Z ]|_', '', city).replace('  ', ' ').strip().lower()

def find_state_country(location, states_file):
    states_key = pandas.read_csv(states_file)
    states_key['abbreviation'] = states_key['abbreviation'].str.lower()
    states_list = states_key['abbreviation'].tolist()

    state = None
    last_location = location.rsplit(', ', 1)[-1].lower()
    if last_location in states_list:
        state = last_location
        country = 'united states'
    else:
        country = last_location

    return state, country

def find_address(soup):
    business_city = business_state = business_zipcode = street_address = latitude = longitude = website = None
    mapbox_tag = soup.find('div', {'class': 'mapbox'})
    if mapbox_tag:
        mapbox_map = mapbox_tag.find('div', {'class': 'mapbox-map'})
        lat_long_tag = mapbox_map.find('div', {'class': 'lightbox-map hidden'})
        lat_long_dict = json.loads(lat_long_tag['data-map-state'])
        latitude = lat_long_dict['center']['latitude']
        longitude = lat_long_dict['center']['longitude']

    mapbox_text = mapbox_tag.find('div', {'class': 'mapbox-text'})
    address_tag = mapbox_text.find('li', {'class': 'map-box-address'})
    street_address_tag = address_tag.find('strong', {'class': 'street-address'})
    if street_address_tag:
        address_text_tag = street_address_tag.find('span', {'itemprop': 'streetAddress'})
        if address_text_tag:
            street_address = address_text_tag.text.strip()
        business_city_tag = street_address_tag.find('span', {'itemprop': 'addressLocality'})
        if business_city_tag:
            business_city = business_city_tag.text.strip()
        business_state_tag = street_address_tag.find('span', {'itemprop': 'addressRegion'})
        if business_state_tag:
            business_state = business_state_tag.text.strip()
        business_zipcode_tag = street_address_tag.find('span', {'itemprop': 'postalCode'})
        if business_zipcode_tag:
            business_zipcode = business_zipcode_tag.text.strip()

    website_tag = mapbox_tag.find('div', {'class': 'biz-website'})
    if website_tag:
        website = 'http://www.yelp.com' + website_tag.find('a')['href']

    return [business_city, business_state, business_zipcode, street_address, latitude, longitude, website]

def find_date(row, review_tag):
    date_tag = review_tag.find('meta', {'itemprop': 'datePublished'})
    if date_tag:
        date_string = date_tag['content']
        year = date_string.split('-')[0]
        row['review_date'] = date_string
        row['review_year'] = int(year)
    return row

def make_lower(row):
    for key, value in row.iteritems():
        # Encode all row values as utf-8
        if value and type(value) == unicode:
            value = value.encode('utf-8', 'ignore')
            row[key] = value
        # Make all text other than review and filename lower case
        if key not in ['review', 'filename'] and type(value) == str:
            row[key] = value.lower()
    return row