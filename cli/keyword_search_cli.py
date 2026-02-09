#!/usr/bin/env python3

import argparse
import json
import string

from nltk.stem import PorterStemmer


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
            with open("data/stopwords.txt") as f:
                stop_words = set(f.read().splitlines())

            search_query = preprocess(args.query, stop_words)
            for movie_id, movie in movies_by_id.items():
                movie_query = preprocess(movie["title"], stop_words)
                matches = [
                    s
                    for s in search_query
                    for m in movie_query
                    if (len(s) > 2 and s in m)
                ]
                if len(matches) > 0:
                    print(f"- '{movie['title']}'")
        case _:
            parser.print_help()


def preprocess(text: str, stop_words: set[str]) -> list[str]:
    normalized = normalize_query(text)
    tokens = tokenize(normalized)
    tokens_without_stop_words = remove_stop_words(tokens, stop_words)
    return stemmer(tokens_without_stop_words)


def normalize_query(query: str) -> str:
    query = query.translate(str.maketrans("", "", string.punctuation))
    return query.lower()


def tokenize(query: str) -> list[str]:
    return query.split()


def remove_stop_words(query: list[str], stop_words: set[str]) -> list[str]:
    res = [word for word in query if word not in stop_words]
    return res


def stemmer(tokens: list[str]) -> list[str]:
    stmr = PorterStemmer()
    return [stmr.stem(token) for token in tokens]


if __name__ == "__main__":
    main()
