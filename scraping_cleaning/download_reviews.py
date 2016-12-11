"""
Download all pages for each business listed in links file.

python download_reviews.py -o="../../Data/zips_0to500-ex/" -l="../../Data/scraped-ex/links0to500.txt"

python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500.txt" -lr=674
python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500_fewdigits.txt" -lr=25
python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500b.txt" -lr=521
python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500_missed.txt"
python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500c.txt" -lr=1054
python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500_missed_auto.csv" -d=","

python download_reviews.py -o="../../Data/zips_0to500/" -l="../../Data/scraped/links0to500d.txt" -lr=1903

"""

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

from constants import *
import os
import argparse
from bs4 import BeautifulSoup
import time
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out_directory', dest = 'out_directory', type = str)
    parser.add_argument('-l', '--links_file', dest = 'links_file', type = str)
    parser.add_argument('-d', '--delimiter', dest = 'delimiter', type = str, default = '\t')
    parser.add_argument('-lr', '--low_row', dest = 'low_row', type = int, default = 0)
    parser.add_argument('-hr', '--high_row', dest = 'high_row', type = int, default = 10000)
    input_values = parser.parse_args()

    driver = new_driver()
    with open(input_values.links_file, 'r') as f:
        reader = csv.DictReader(f, delimiter = input_values.delimiter)

        for row_number, row in enumerate(reader):
            if row_number < input_values.low_row:
                continue
            if row_number > input_values.high_row:
                break

            # Every NEW_DRIVER_FREQ links, quit the driver and open a new one
            if row_number % NEW_DRIVER_FREQ == 0:
                driver.close()
                driver.quit()
                driver = new_driver()

            business_link = row['business_link']
            zipcode = row['zipcode']
            driver = save_business_pages(driver, business_link, input_values.out_directory, zipcode)
    driver.close()
    driver.quit()

def save_business_pages(driver, business_link, out_directory, zipcode):
    """
    Go through all reviews pages for a business
    Args:
        business_link (str): url that led to business page
        Returns a driver that has gone through many pages for the business
    """
    page_no = 0
    business_id = business_link.split('/biz/')[1].split('?')[0]
    business_directory = os.path.join(out_directory, zipcode, business_id)
    print 'starting business ' + business_id + ' in zipcode ' + zipcode

    if not os.path.exists(business_directory):
        os.makedirs(business_directory)

    page_filename = os.path.join(business_directory, business_id + '_' + str(page_no) + '.html')

    driver.get(business_link)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    with open(page_filename, 'w') as f:
        f.write(soup.prettify().encode('utf-8'))

    while True:
        try:
            # Check if there is a loading error before you try to click "next"
            if loading_error(soup):
                sys.exit('Continually loading at business ' + business_id + ', zip code ' + zipcode)

            # next_tag = driver.find_element_by_xpath("//a[@class='page-option prev-next next']")
            next_tag = driver.find_element_by_xpath("//a[@class='u-decoration-none next pagination-links_anchor']")
        # If there's no next button, you're done
        except:
            break
        else:
            # Sleep for a bit to let it load completely and be able to click
            time.sleep(LOADING_TIME)
            next_tag.click()
            page_no += 1

            # Sleep for a bit to let it load completely and not be faded
            time.sleep(LOADING_TIME)
            page_filename = os.path.join(business_directory, business_id + '_' + str(page_no) + '.html')
            source = driver.page_source
            soup = BeautifulSoup(source, "html.parser")
                        
            with open(page_filename, 'w') as f:
                f.write(soup.prettify().encode('utf-8'))

    return driver

def loading_error(soup):
    """ Return true if the page is continually loading (throbber-overlay is visible) """
    throbber_tag = soup.find('div', {'class': 'throbber-overlay'})
    throbber_style = str(throbber_tag['style'])
    return 'display: block;' in throbber_style

def new_driver():
    # driver = webdriver.PhantomJS(service_args=["--webdriver-loglevel=NONE"])
    driver = webdriver.Firefox()
    # Wait to find each element if not immediately available
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver

if __name__ == '__main__':
    main()