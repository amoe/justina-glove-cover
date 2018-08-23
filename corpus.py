import numpy as np
import pandas as pd
import csv
import pprint
import io

schema = {
    'obv2wid': int,
    'sess_date': str,
    'year': str,
    'obo_trial': str,
    'obo_deftid': str,
    'obc_u_no': int,
    'obc_event': str,
    'obc_speaker': str,
    'obc_sex': np.character,
    'obc_hiscoLabel': str,
    'obc_hiscoCode': str,
    'obc_class': str,
    'obc_role': str,
    'obv_role': str,
    'words': str,
    'obv_words_type': np.character,
    'words_count': int,
    'defendant': str
}

fpath = 'voa/OBV2/obv_words_v2_28-01-2017.tsv'

all_rows = []

def row_is_misaligned(row):
    try:
        word_count = int(row['words_count'])
        return False
    except ValueError as e:
        return True

def fix_misaligned_row(row):
    new_row = row.copy()

    new_row['obv_words_type'] = 's'
    new_row['words_count'] = row['obv_words_type']
    new_row['defendant'] = row['words_count']

    return new_row

class CorpusPreparer(object):
    def get_corpus(self):
        with open(fpath, 'r') as f:
            reader = csv.DictReader(f, skipinitialspace=True, delimiter='\t')

            for index, row in enumerate(reader):
                if row_is_misaligned(row):
                    print("Fixing misaligned row")
                    row = fix_misaligned_row(row)

                all_rows.append(row)

        print("Read %d rows" % len(all_rows))
        print("Writing fixed version")

        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=schema.keys(),
            delimiter='\t',
            quoting=csv.QUOTE_ALL
        )

        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)


        print("Done fixing data, stream pos = %d" % output.tell())

        print('getting corpus data')


        output.seek(0)
        df = pd.read_csv(output, sep='\t', dtype=schema)

        return df
