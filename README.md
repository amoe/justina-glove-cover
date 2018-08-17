# TAG

Reimplementation of CoVeRModel for analysing the difference between male and
female speech.

The data files used can be found at [Sharon Howard's VOA
repository](https://github.com/sharonhoward/voa).

Grady Simon's [tf-glove](https://github.com/GradySimon/tensorflow-glove) package
is required to use this model.

dependencies:

Spacy 2.0.11
Numpy 1.15.0
Pandas 0.20.1
Tensorflow 1.1.0

The spacy model required is 2.0.0: you can install the [relevant
tarball](https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.0.0/en_core_web_md-2.0.0.tar.gz)
with pip.

The input file is expected to be found at
`voa/OBV2/obv_words_v2_28-01-2017.tsv`.

The `quan` parameter accepted by `get_parsed_corpus` is used to restrict the
corpus to a small set of examples.  Pass the length of the corpus to run the
model over the entire corpus.
