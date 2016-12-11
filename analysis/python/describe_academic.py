import pandas as pd
import sys

def main():
    directory = '../../Data/academic/'
    infile = directory + 'academic_dataset_cleaned.csv'
    outfile = directory + 'academic_descriptive.txt'

    describe(infile, outfile)

def describe(infile, outfile):
    orig_stdout = sys.stdout
    f = file(outfile, 'w')
    sys.stdout = f

    df = pd.read_csv(infile)

    print 'Years: ' + str(df['year'].value_counts()) + '\n'

    print 'Number of restaurants: ' + str(len(df['business_id'].unique())) + '\n'
    print 'Number of reviews: ' + str(df['text'].count()) + '\n'
    print 'Number of Mexican reviews: ' + str(df.loc[df['category'] == 'mexican', 'text'].count()) + '\n'

    print 'Restaurant categories:\n' + str(df['category'].value_counts()) + '\n'

    print 'Number of categories we care about per restaurant (e.g. Mexican and Chinese)\n'
    print df['number_categories'].value_counts()

    sys.stdout = orig_stdout
    f.close()

if __name__ == '__main__':
    main()