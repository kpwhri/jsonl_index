"""
Index a jsonl corpus file by a particular id.

Usage:
    with JsonlIndex(path) as idx:
        data = idx.get(id)
"""

import json
import pickle
from pathlib import Path

import logging


class JsonlIndex:

    def __init__(self, path: Path, key, load=False):
        self.path = path
        self.index_path = Path(f'{path}.idx')
        self.key = key
        self.index = {}
        self._is_loaded = False
        if load:
            self.load()

    def __enter__(self):
        if not self._is_loaded:
            self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def exists(self):
        return self.index_path.exists()

    def load(self, *, force_rebuild=False):
        if self.index_path.exists() and not force_rebuild:
            with open(self.index_path, 'rb') as fh:
                self.index = pickle.load(fh)
        else:
            self.index = {}
            self._build_index()
        self._is_loaded = True
        return len(self.index)

    def _build_index(self):
        logging.info(f'Index not found! - building index at {self.index_path}.')
        with open(self.path, 'rb') as fh:
            offset = 0
            for line in fh:
                key = json.loads(line.decode('utf8'))[self.key]
                self.index[key] = offset
                offset += len(line)
        with open(self.index_path, 'wb') as out:
            pickle.dump(self.index, out)

    def get(self, key) -> dict:
        if not self._is_loaded:
            raise ValueError(f'Index not loaded.')
        if key not in self.index:
            logging.warning(f'Invalid key (not present in index): {key}')
            return {}
        with open(self.path, 'rb') as fh:
            fh.seek(self.index[key])
            return json.loads(fh.readline().decode('utf8'))

    def __str__(self):
        return f'JsonlIndex({self.index_path})'

    __repr__ = __str__
