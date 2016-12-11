""" Fix issue where zipcodes with leading zeros weren't searched for properly.

In zipcodes searched, pull out zip codes with fewer than 5 digits and make them complete, into new file """

import csv

def main():
	directory = '../Data/'
	zips_searched_file = directory + 'zips_searched_0to500.txt'
	outfile = directory + 'input/zips_ordered_262_fewdigits.txt'

	with open(outfile, 'w') as outf:
		writer = csv.DictWriter(outf, fieldnames = ['zipcode'])
		writer.writeheader()

		with open(zips_searched_file, 'r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				zipcode = row['zipcode']
				# Only write zip codes that have fewer than 5 digits
				if len(zipcode) < 5:
					zipcode = add_zeros(zipcode)
					writer.writerow({'zipcode': zipcode})

def add_zeros(zipcode):
    """ Make zipcode have leading zeros if needed """
    return '0' * (5 - len(zipcode)) + zipcode

if __name__ == '__main__':
    main()