#!/usr/bin/env python3

import argparse
import json
import string


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            movies = json.load(open("data/movies.json"))
            movies_by_id = {movie["id"]: movie for movie in movies["movies"]}
            n = 1
            for movie_id, movie in movies_by_id.items():
                if normalize_query(args.query) in normalize_query(movie["title"]):
                    print(f"{n}. {movie["title"]}")
                    n += 1
        case _:
            parser.print_help()


def normalize_query(query: str) -> str:
    query = query.translate(str.maketrans('', '', string.punctuation))
    return query.lower()


if __name__ == "__main__":
    main()
