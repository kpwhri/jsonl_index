import json

from jsonl_index import JsonlIndex
from jsonl_index.scripts.args import get_args


def main():
    args = get_args()
    print(f'Building index for corpus {args["jsonl_corpus"]} with index on {args["key"] or "line number"}.')
    with JsonlIndex(args['jsonl_corpus'], args['key'], load=True) as idx:
        print(f'Index is ready at {idx.index_path}.')
        print(f'Type "exit" or "quit" to terminate app.')
        while True:
            target_id = input(f'Specify {args["key"] or "line number"}>> ')
            if target_id.lower() in {'exit', 'quit'}:
                break
            try:
                target_id = int(target_id)
            except ValueError:
                pass
            print(json.dumps(idx.get(target_id), indent=2))


if __name__ == '__main__':
    main()
