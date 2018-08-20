from collections import defaultdict
from CoVerModel import CoVeRModel
import string
import spacy
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import json

nlp = spacy.load('en_core_web_md')
sess = tf.InteractiveSession()

def get_corpus():
    print('getting corpus data')
    fpath = 'voa/OBV2/obv_words_v2_28-01-2017.tsv'
    df = pd.read_csv(fpath, sep='\t')

    female_speech = df.loc[(df['obc_sex'] == 'f') & (df['obc_hiscoLabel'] != 'Lawyer'),'words']
    male_speech = df.loc[df['obc_sex'] == 'm','words'] # male speech including lawyers

    return female_speech,male_speech


def get_parsed_corpus(speech,quan):
    print('getting spacy parsed corpus')
    # used spacy for the parsing and get the pos to find the similarities
    parsed_speech = [nlp(speech.iloc[i]) for i in range(quan)]
    # remove punctuations
    parsed_speech_corpus = [[word.text for word in sen if word.text not in string.punctuation] for sen in parsed_speech]

    return parsed_speech_corpus

def analysis(cover):
    #### ANALYSIS ####
    print('ANALYSIS')
    covariates = cover.covariates
    [female, male] = cover._CoVeRModel__words
    embeddings = cover.embeddings

    female_embedding = tf.multiply(embeddings,covariates[0])
    female_embedding = sess.run(female_embedding)

    male_embedding = tf.multiply(embeddings,covariates[1])
    male_embedding = sess.run(male_embedding)

    common_words = list(set(female).intersection(male))

    return female_embedding,male_embedding,common_words

def avg(arr):
    avg = np.mean(arr, axis=1)
    
    return avg

def write_file(file_path, arr):
    print('writing', file_path)
    with open(file_path, 'w') as outfile:
        outfile.write('# Array shape: {0}\n'.format(arr.shape))
        for data_slice in arr:
            np.savetxt(outfile, data_slice, fmt='%-7f')
            outfile.write('\n# New slice\n\n')

def main(limit=None):
    [female_speech, male_speech] = get_corpus()

    if limit is None:
        female_limit = int(len(female_speech))
        male_limit = int(len(male_speech))
    else:
        female_limit = limit
        male_limit = limit

    parsed_female_corpus = get_parsed_corpus(female_speech, female_limit)
    parsed_male_corpus = get_parsed_corpus(male_speech, male_limit)
    parsed_corpora = [parsed_female_corpus] + [parsed_male_corpus]
    cover = CoVeRModel(embedding_size=300,context_size=10,min_occurrences=5,learning_rate=0.05,batch_size=512)
    cover.fit_corpora(parsed_corpora)
    cover.train()

    [female_embedding,male_embedding,common_words] = analysis(cover)

    cover.train()
    [fe,ma,_] = analysis(cover)
    male_embedding = np.stack((male_embedding,ma), axis=1)
    female_embedding = np.stack((female_embedding,fe), axis=1)

    # XXX: Now that the model is deterministic, this is pretty futile
    # because the result isn't going to change from run to run anyway. -- amoe
    for i in range(3):
      cover.train()
      [fe,ma,_] = analysis(cover)
      n = cover._CoVeRModel__vocab_size
      m = cover.embedding_size

      fe = fe.reshape(n,1,m)
      female_embedding = np.append(female_embedding,fe,axis=1)

      ma = ma.reshape(n,1,m)
      male_embedding = np.append(male_embedding,ma,axis=1)

    female_avg = avg(female_embedding)
    fpath = os.getcwd() + '/female'
    cover.generate_tsne(path=fpath, embeddings=female_avg)

    male_avg = avg(male_embedding)
    mpath = os.getcwd() + '/male'
    cover.generate_tsne(path=mpath, embeddings=male_avg)

    print('FINISHED')

    with open('fe.json', 'w') as f:
        json.dump(female_avg.tolist(), f)

    with open('me.json', 'w') as f:
        json.dump(male_avg.tolist(), f)
    return {
        'female_embedding': female_avg.tolist(),
        'male_embedding': male_avg.tolist()
    }
