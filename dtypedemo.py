import numpy as np
import pandas as pd


schema = {
    'obv2wid': int,
    'sess_date': str,
    'year': str,
    'obo_trial': str,
    'obo_deftid': str,
    'obc_u_no': int,
    'obv_event': str,
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
df = pd.read_csv(fpath, sep='\t', dtype=schema)

# reveals an error in the source
