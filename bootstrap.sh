#! /bin/sh

echo "Setting up tensorflowglove."
tf_glove_url="https://raw.githubusercontent.com/GradySimon/tensorflow-glove/6a05b0545283cb2e576f2286e5dca11a1e42bbb9/tf_glove.py"

module_dir="ext/tensorflowglove"

mkdir -p "$module_dir"
curl -o "$module_dir/tf_glove.py" "$tf_glove_url"

echo "Retrieving corpus."

corpus_zip_url="https://raw.githubusercontent.com/sharonhoward/voa/ecc48039d84bfe4ba906d6a7a2a86a1c80fc68d4/OBV2/obv_words_v2_28-01-2017.tsv.zip"
tmp_zip_path=$(mktemp -t tagzip-XXXXXXXX.zip)

curl -o "$tmp_zip_path" "$corpus_zip_url"

corpus_path="voa/OBV2"
mkdir -p "$corpus_path"
unzip -d "$corpus_path" "$tmp_zip_path"

