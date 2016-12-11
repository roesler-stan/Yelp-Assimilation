""" Prepare the file containing zip codes for which to search """

import pandas

def main():
	directory = '../Data/'
	infile = directory + 'zip07_cbsa06.txt'
	full_outfile = directory + 'metros_data.csv'
	zips_outfile = directory + 'zips.txt'

	dataset = pandas.read_csv(infile)
	dataset = dataset.rename(columns=lambda x: str(x.lower()))

	dataset = dataset[dataset['cbsa lsad'].str.contains('metro', case = False, na = False)]
	zips = dataset['zip5'].unique()

	dataset.to_csv(full_outfile, index = False)

	with open(zips_outfile, 'w') as outf:
		outf.write('zipcode\n')
		for zipcode in zips:
			zipcode_str = clean_zip(zipcode)
			outf.write(zipcode_str + '\n')

def clean_zip(zipcode):
	zipcode_str = str(zipcode)
	if zipcode < 10000:
		zipcode_str = '0' + zipcode_str
	if zipcode < 1000:
		zipcode_str = '0' + zipcode_str
	if zipcode < 100:
		zipcode_str = '0' + zipcode_str
	if zipcode < 10:
		zipcode_str = '0' + zipcode_str

	return zipcode_str

if __name__ == '__main__':
    main()