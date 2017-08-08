import csv

def main():
	infile = '../../Data/cps_intermarriage.csv'
	outfile = '../../Data/cps_intermarriage_stats.csv'
	couples = count_couples(infile)
	area_types = count_areas(couples)
	write_file(area_types, outfile)


def count_couples(infile):
	couples = {}
	with open(infile, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			household = row['serial']
			if couples.has_key(household):
				continue
			mexican = row['mex']
			spouse_mexican = row['spmex']
			# Only continue if spouse exists and Mexicanness is known
			if not spouse_mexican:
				continue
			couple_type = get_type(mexican, spouse_mexican)
			metfips = row['metfips']
			couples[household] = (metfips, couple_type)
	return couples


def count_areas(couples):
	area_types = {}
	for household, data in couples.items():
		metfips = data[0]
		couple_type = data[1]
		if area_types.has_key(metfips):
			area_types[metfips][couple_type] = area_types[metfips].get(couple_type, 0) + 1
		else:
			area_types[metfips] = {couple_type: 1}
	return area_types


def write_file(area_types, outfile):
	headers = ['metfips', 'cps_mex_interracial_pct']
	with open(outfile, 'w') as f:
		writer = csv.DictWriter(f, headers)
		writer.writeheader()
		for metfips, data in area_types.items():
			mexican = data.get('mexican', 0)
			non_mexican = data.get('non_mexican', 0)
			mixed = data.get('mixed', 0)
			if (mixed + mexican) == 0:
				wmex_mixed_pct = None
			else:
				wmex_mixed_pct = (float(mixed) / (mixed + mexican)) * 100
			row = {'metfips': metfips, 'cps_mex_interracial_pct': wmex_mixed_pct}
			writer.writerow(row)


def get_type(person, spouse):
	if (person == '0' and spouse == '1') or (spouse == '0' and person == '1'):
		return 'mixed'
	elif person == '0' and spouse == '0':
		return 'non_mexican'
	elif person == '1' and spouse == '1':
		return 'mexican'
	else:
		return 'error'


if __name__ == "__main__":
	main()
