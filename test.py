# test skeleton

import main
import json

EXPECTED_PATHS = {
    'female_embedding': 'expected_female_embeddings.json',
    'male_embedding': 'expected_male_embeddings.json'
}

expected_data = {}

for k, v in EXPECTED_PATHS.items():
    with open("resources/%s" % v, 'r') as f:
        expected_data[k] = json.load(f)

def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4

def test_main():
    result = main.main(limit=10)

    assert result['female_embedding'] == expected_data['female_embedding']
    assert result['male_embedding'] == expected_data['male_embedding']

