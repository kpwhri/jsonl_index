import argparse


def _parse_target(d):
    if 'target' in d:
        try:
            d['target'] = int(d['target'])
        except ValueError:
            pass
    return d


def get_args(include_target=False):
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@!')
    parser.add_argument('jsonl_corpus',
                        help='Path to jsonlines corpus.')
    parser.add_argument('key', nargs='?', default=None,
                        help='The key to index on (e.g., `id`). Default will use line number.')
    if include_target:
        parser.add_argument('--target', dest='target', required=True,
                            help='Value of key to be searched for. Will try to interpret as int or leave as string.')
    return _parse_target(vars(parser.parse_args()))
