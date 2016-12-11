"""
Scrape the Yelp search engine to find all business links for given zip codes.

python business_links.py -z="../../Data/input/zips_2010_ordered.csv" -l="../../Data/scraped-ex/links0to500.txt" -zs="../../Data/scraped-ex/zips_searched_0to500.txt" -lr=0 -hr=500


python business_links.py -z="../../Data/input/zips_2010_ordered.csv" -l="../../Data/scraped/links0to500.txt" -zs="../../Data/scraped/zips_searched_0to500.txt" -lr=0 -hr=500
python business_links.py -z="../../Data/input/zips_2010_ordered.csv" -l="../../Data/scraped/links0to500b.txt" -zs="../../Data/scraped/zips_searched_0to500b.txt" -lr=262 -hr=500
python business_links.py -z="../../Data/input/zips_ordered_262_fewdigits.txt" -l="../../Data/scraped/links0to500_fewdigits.txt" -zs="../../Data/scraped/zips_searched_0to500_fewdigits.txt"
python business_links.py -z="../../Data/input/zips_2010_ordered.csv" -l="../../Data/scraped/links0to500c.txt" -zs="../../Data/scraped/zips_searched_0to500c.txt"
python business_links.py -z="../../Data/input/zips_2010_ordered.csv" -l="../../Data/scraped/links0to500d.txt" -zs="../../Data/scraped/zips_searched_0to500d.txt" -lr=384 -hr=385 -mp=94
python business_links.py -z="../../Data/input/zips_2010_ordered.csv" -l="../../Data/links0to500d.txt" -zs="../../Data/scraped/zips_searched_0to500d.txt" -lr=534

"""

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

from constants import *
from bs4 import BeautifulSoup
import os
import argparse
import time
import re
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def main():
    """
    Args:
        low_row: minimum row number of zipcode file to find links for (inclusive)
        high_row: maximum row number of zipcode file to find links for (inclusive)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--zipcode_file', dest = 'zipcode_file', type = str)
    parser.add_argument('-l', '--links_file', dest = 'links_file', type = str)
    parser.add_argument('-zs', '--zipcodes_searched', dest = 'zipcodes_searched', type = str)
    parser.add_argument('-lr', '--low_row', dest = 'low_row', type = int, default = 0)
    parser.add_argument('-hr', '--high_row', dest = 'high_row', type = int, default = 10000)
    parser.add_argument('-mp', '--min_page', dest = 'min_page', type = int, default = None)
    input_values = parser.parse_args()

    links_headers = 'business_link' + '\t' + 'zipcode'
    write_line(input_values.links_file, links_headers)
    write_line(input_values.zipcodes_searched, 'zipcode')

    driver = new_driver()
    driver.get(YELP_BASE)
    with open(input_values.zipcode_file, 'r') as f:
        reader = csv.DictReader(f)

        for row_number, row in enumerate(reader):
            if row_number < input_values.low_row:
                continue

            if row_number >= input_values.high_row:
                break

            # Every NEW_DRIVER_FREQ zip codes, quit the driver and open a new one
            if row_number % NEW_DRIVER_FREQ == 0:
                driver.close()
                driver.quit()
                driver = new_driver()
                driver.get(YELP_BASE)

            zipcode = row['zipcode']
            zipcode = add_zeros(zipcode)
            print 'going to search ' + zipcode
            driver = search_zipcode(driver, zipcode, input_values.links_file, input_values.min_page)

            write_line(input_values.zipcodes_searched, zipcode)
    driver.close()
    driver.quit()

def search_zipcode(driver, zipcode, links_file, min_page):
    """
    Go through all possible pages from search for a given zip code.

    Args:
        driver (selenium driver)
        zipcode (int or string): zip code to search for
        links_file (str): file to keep list of business links
        min_page (int): minimum page number to start at
    """
    time.sleep(LOADING_TIME)
    driver = fill_forms(driver, zipcode)

    # If a minimum page number was inputted, go to that url directly
    if min_page:
        url = driver.current_url
        page_url = url.split('&ns=1')[0] + '&start=' + str((min_page - 1) * 10)
        driver.get(page_url)

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    
    # If it hit a captcha, stop everything
    if check_captcha(soup):
        sys.exit('Hit Captcha at zipcode ' + zipcode)

    # If it didn't find anything for that zip code, skip it
    if not soup.find(text = "Sorry, but we didn't understand the location you entered."):
        # Go to each business link on search page
        driver = go_through_businesses(driver, soup, links_file, zipcode)

        # Go to next page of businesses in search, if there is a next page
        while True:
            try:
                # next_tag = driver.find_element_by_xpath("//a[@class='page-option prev-next next']")
                next_tag = driver.find_element_by_xpath("//a[@class='u-decoration-none next pagination-links_anchor']")
            # If there's no next button, you're done
            except:
                break
            else:
                driver.execute_script("return arguments[0].scrollIntoView();", next_tag)
                time.sleep(LOADING_TIME)

                next_tag.click()
                time.sleep(LOADING_TIME)
                source = driver.page_source
                soup = BeautifulSoup(source, "html.parser")
                driver = go_through_businesses(driver, soup, links_file, zipcode)

    return driver

def fill_forms(driver, zipcode):
    category_form = driver.find_element_by_id("find_desc")
    location_form = driver.find_element_by_id("dropperText_Mast")

    clear_form(category_form)
    category_form.send_keys("Mexican")
    clear_form(location_form)
    location_form.send_keys(zipcode + Keys.ENTER)

    driver.title

    return driver

def clear_form(form):
    for i in range(20):
        form.send_keys(Keys.BACKSPACE)

def go_through_businesses(driver, soup, links_file, zipcode):
    """ Go to each business link on this page """
    result_tags = soup.find_all('li', {'class': 'regular-search-result'})
    correct_businesses = 0
    for result_tag in result_tags:
        business_tag = result_tag.find('div', {'class': 'biz-listing-large'})
        # Check that it's in the right zip code
        if not correct_zipcode(business_tag, zipcode):
            continue

        business_link = YELP_BASE + business_tag.find('div', {'class': 'main-attributes'}).find('a', {'class': 'biz-name'})['href']
        # Add business link to links file
        links_line = business_link + '\t' + zipcode
        write_line(links_file, links_line)
        correct_businesses += 1

    print 'found ' + str(correct_businesses) + ' businesses for ' + zipcode

    return driver

def write_line(outfile, message):
    with open(outfile, 'a') as f:
        f.write(message + '\n')

def new_driver():
    # driver = webdriver.PhantomJS(service_args=["--webdriver-loglevel=NONE"])
    driver = webdriver.Firefox()
    # Wait to find each element if not immediately available
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver

def correct_zipcode(business_tag, zipcode):
    """ Check if business has correct zip code """
    try:
        address = business_tag.find('div', {'class': 'secondary-attributes'}).find('address').text
        zipcode_found = re.search(re.compile('(^|[^\d])\d{5}($|[^\d])'), address).group(0)
        zipcode_found = re.search(re.compile('\d{5}'), zipcode_found).group(0)
        return zipcode_found == zipcode
    except:
        return False

def add_zeros(zipcode):
    """ Make zipcode have leading zeros if needed """
    return '0' * (5 - len(zipcode)) + zipcode

def check_captcha(soup):
    return soup.find('form', {'id': 'distilCaptchaForm'})

if __name__ == '__main__':
    main()