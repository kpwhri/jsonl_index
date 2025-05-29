"""
Tests on the corpus `animals.jsonl`. Comparison is made to reading the file into memory.
"""
import json
from pathlib import Path

import pytest

from jsonl_index import JsonlIndex


def remove_indices(path: Path):
    for file in path.iterdir():
        if 'idx' in file.suffix:
            file.unlink()
    return path


def load_jsonl_by(corpus_path, by=None):
    dataset = {}
    with open(corpus_path, encoding='utf8') as fh:
        for i, line in enumerate(fh):
            data = json.loads(line)
            if by is None:
                key = i
            else:
                key = data[by]
                try:
                    key = int(key)
                except ValueError:
                    pass
            dataset[key] = data
    return dataset


@pytest.fixture(scope='package')
def corpus_dir():
    path = Path('data')
    remove_indices(path)
    yield path
    remove_indices(path)


@pytest.fixture
def animal_corpus_by_id(corpus_dir):
    key = 'id'
    corpus_path = corpus_dir / 'animals.jsonl'
    yield from get_corpus_and_dataset(corpus_path, key)


@pytest.fixture
def animal_corpus_by_title(corpus_dir):
    key = 'title'
    corpus_path = corpus_dir / 'animals.jsonl'
    yield from get_corpus_and_dataset(corpus_path, key)


@pytest.fixture
def animal_corpus_by_line_number(corpus_dir):
    key = None
    corpus_path = corpus_dir / 'animals.jsonl'
    yield from get_corpus_and_dataset(corpus_path, key)


def get_corpus_and_dataset(corpus_path, key):
    dataset = load_jsonl_by(corpus_path, by=key)
    with JsonlIndex(corpus_path, key=key, load=True) as idx:
        yield idx, dataset


@pytest.mark.parametrize('key', [1001, 1003, 1007, 1140, 1135])
def test_animals_corpus_id(animal_corpus_by_id, key):
    idx, dataset = animal_corpus_by_id
    idx_data = idx.get(key)
    ds_data = dataset[key]
    assert idx_data == ds_data


@pytest.mark.parametrize('key', [5, 6, 29, 0, 27])
def test_animals_corpus_line_number(animal_corpus_by_line_number, key):
    idx, dataset = animal_corpus_by_line_number
    idx_data = idx.get(key)
    ds_data = dataset[key]
    assert idx_data == ds_data


@pytest.mark.parametrize('key', ['Aye-aye', 'Binturong', 'Sunda Colugo', 'Tarsier'])
def test_animals_corpus_title(animal_corpus_by_title, key):
    idx, dataset = animal_corpus_by_title
    idx_data = idx.get(key)
    ds_data = dataset[key]
    assert idx_data == ds_data
