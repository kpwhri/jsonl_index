# Jsonlines Index

While jsonlines can be a useful format for storing a corpus (i.e., separable flat file), it is not useful for quick
lookup of a particular text. The `build_index(corpus_path)` function will create an index allowing rapid lookup of
individual lines of the corpus based on a key.

Command line usage:

```bash
ax-build-index /path/to/corpus.jsonl [key]
```

```python
from pathlib import Path
from jsonl_index import JsonlIndex

path = Path(r'C:\path\to\corpus.jsonl')
with JsonlIndex(path, 'id') as idx:
    # index will automatically be built if it doesn't exist (which may take some time)
    data = idx.get('234')  # returns dict of row for id
```

This will build an index at `/path/to/corpus.jsonl.id-idx` which will be automatically used by other scripts.
