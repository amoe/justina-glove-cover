import numpy as np
import pandas as pd
import csv
import pprint

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

print('getting corpus data')
fpath = 'voa/OBV2/obv_words_v2_28-01-2017.tsv'
#df = pd.read_csv(fpath, sep='\t', dtype=schema)

all_rows = []

with open(fpath, 'r') as f:
    reader = csv.DictReader(f, skipinitialspace=True, delimiter='\t')

    for index, row in enumerate(reader):
        if row['obv2wid'] == '20442':
            new_row = row.copy()

            # These values were shifted by one, and the words type is missing.
            # I have inferred it manually
            new_row['defendant'] = row['words_count']
            new_row['words_count'] = row['obv_words_type']
            new_row['obv_words_type'] = 'd'
            
            all_rows.append(new_row)
        else:
            all_rows.append(row)

print("Read %d rows" % len(all_rows))


print("Writing fixed version")
with open('fixed.tsv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=schema.keys(), delimiter='\t', quoting=csv.QUOTE_ALL)

    writer.writeheader()
    for row in all_rows:
        writer.writerow(row)
print("Done fixing data")


# reveals an error in the source
