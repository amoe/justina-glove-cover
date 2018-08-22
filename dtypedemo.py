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

output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=schema.keys(), delimiter='\t', quoting=csv.QUOTE_ALL)

writer.writeheader()
for row in all_rows:
    writer.writerow(row)


print("Done fixing data, stream pos = %d" % output.tell())


# reveals an error in the source

print('getting corpus data')


output.seek(0)
df = pd.read_csv(output, sep='\t', dtype=schema)

#output.close()
