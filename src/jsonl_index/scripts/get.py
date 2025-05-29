import json

from jsonl_index import JsonlIndex
from jsonl_index.scripts.args import get_args


def main():
    args = get_args(include_target=True)
    print(f'Building index for corpus {args["jsonl_corpus"]} with index on {args["key"] or "line number"}.')
    with JsonlIndex(args['jsonl_corpus'], args['key'], load=True) as idx:
        print(f'Index is ready at {idx.index_path}.')
        print(f'Searching for key: "{args["target"]}"')
        print(json.dumps(idx.get(args['target']), indent=2))


if __name__ == '__main__':
    main()
