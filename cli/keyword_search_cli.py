"""Keyword Search CLI"""
#!/usr/bin/env python3

import sys
import argparse
import json

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.inverted_index import InvertedIndex
from lib.text_utils import preprocess

# Add project root to path so `lib` is importable when running script directly


def main() -> None:
    """Main function"""
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")
    subparsers.add_parser("build", help="Build the index")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            try:
                index = InvertedIndex()
                index.load()
                print("Index loaded successfully")
            except FileNotFoundError as exc:
                print(f"Error loading index: {exc}")
                sys.exit(1)

            for s in args.query.split():
                docs = index.get_documents(s)
                i = 1
                for doc in docs:
                    if i > 5:
                        break
                    i += 1
                    print(f"- '{index.docmap[doc]['title']}'")

        case "build":
            movies = json.load(open("data/movies.json", encoding="utf-8"))
            index = InvertedIndex()
            index.build(movies["movies"])
            index.save()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
