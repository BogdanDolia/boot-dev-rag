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
            movies = json.load(open("data/movies.json", encoding="utf-8"))
            movies_by_id = {movie["id"]: movie for movie in movies["movies"]}
            with open("data/stopwords.txt", encoding="utf-8") as f:
                stop_words = set(f.read().splitlines())

            search_query = preprocess(args.query, stop_words)
            for _, movie in movies_by_id.items():
                movie_query = preprocess(movie["title"], stop_words)
                # This is a list comprehension that checks if the search query is in the movie query
                # and if the length of the search query is greater than 2
                matches = [
                    s
                    for s in search_query
                    for m in movie_query
                    if (len(s) > 2 and s in m)
                ]
                if len(matches) > 0:
                    print(f"- '{movie['title']}'")
        case "build":
            movies = json.load(open("data/movies.json", encoding="utf-8"))
            index = InvertedIndex()
            index.build(movies["movies"])
            index.save()
            docs = index.get_documents("merida")
            print(docs[0])
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
