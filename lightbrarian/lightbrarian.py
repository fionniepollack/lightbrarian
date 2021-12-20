import json
import argparse
import os
import sys
from pathlib import Path

from googleapiclient.discovery import build

def print_books(books):
    for i, book in enumerate(books):
        print(f"Book ID: [{i + 1}]")
        print(f"Title: {book['volumeInfo'].get('title', 'Unknown title')}")
        print(f"Author(s): {','.join(book['volumeInfo'].get('authors', ['Unknown author']))}")
        print(f"Publisher: {book['volumeInfo'].get('publisher', 'Unknown publisher')}")
        print('---')

def search_books(command, book_title, book_author, book_publisher, max_results, google_api_token, lightbrarian_reading_list_path):
    query_elements = [
        {
            "search_field": "intitle",
            "search_value": book_title
        },
        {
            "search_field": "inauthor",
            "search_value": book_author
        },
        {
            "search_field": "inpublisher",
            "search_value": book_publisher
        }
    ]

    query_string_list = []

    for query_element in query_elements:
        if query_element['search_value'] is not None:
            query_string_list.append(f"{query_element['search_field']}:{query_element['search_value']}") 

    query_string = "+".join(query_string_list)

    with build('books', 'v1', developerKey=google_api_token) as service:
        response = service.volumes().list(q=query_string, maxResults=max_results).execute()

    total_search_results = len(response['items'])

    print("")
    print("---SEARCH RESULTS---")
    print("")
    print(f"Total search results: {total_search_results}")
    print("")

    books = response['items']
    print_books(books)

    selected_book_id = -1
    while not int(selected_book_id) in range(0,(total_search_results + 1)):
        selected_book_id = int(input(f"Enter Book ID (1-{total_search_results}) to save to reading list or 0 to skip: ") or 0)

    if selected_book_id != 0:
        with open(lightbrarian_reading_list_path, 'r+') as lightbrarian_reading_list_file:
            existing_data = json.load(lightbrarian_reading_list_file)
            existing_data["books"].append(books[selected_book_id-1])
            lightbrarian_reading_list_file.seek(0)
            json.dump(existing_data, lightbrarian_reading_list_file)
            lightbrarian_reading_list_file.truncate()

def list_books(lightbrarian_reading_list_path):
    try:
        with open(lightbrarian_reading_list_path, 'r') as lightbrarian_reading_list_file:
            reading_list_data = json.load(lightbrarian_reading_list_file)
    except FileNotFoundError as exception:
        sys.exit("No reading list found. Please run the search command to add books to your reading list.")
    
    books = reading_list_data["books"]

    print_books(books)

def parse_arguments():
    parser = argparse.ArgumentParser(description = "A command line application to search for books and construct a reading list.")
    subparsers = parser.add_subparsers(title = "command", dest = "command")
    subparsers.required = True
    
    parser_search = subparsers.add_parser("search", help = "Search for available books")
    parser_search.add_argument("--book-title", type = str, help = "A book title to search for")
    parser_search.add_argument("--book-author", type = str, help = "A book author to search for")
    parser_search.add_argument("--book-publisher", type = str, help = "A book publisher to search for")
    parser_search.add_argument("--max-results", type = int, default = 5, help = "The maximum number of search results to return")

    parser_list = subparsers.add_parser("list", help = "List books from reading list")

    args = parser.parse_args()

    if args.command == "search":
        if args.book_title is None and args.book_author is None and args.book_publisher is None:
            parser.error("at least one of --book-title, --book-author, --book-publisher required")

    return args

def initialize(lightbrarian_root_path, lightbrarian_reading_list_path):
    if not os.path.exists(lightbrarian_root_path):
        os.makedirs(lightbrarian_root_path)

    if not os.path.exists(lightbrarian_reading_list_path):
        with open(lightbrarian_reading_list_path, "w") as lightbrarian_reading_list_file:
            blank_reading_list = {
                "books": []
            }
            json.dump(blank_reading_list, lightbrarian_reading_list_file)


def cli():
    args = parse_arguments()
    
    command = args.command

    google_api_token = os.environ.get('GOOGLE_API_TOKEN', None)

    if google_api_token is None:
        sys.exit("The GOOGLE_API_TOKEN environment variable must be set. See the README.md for more details.")

    home_folder_path = str(Path.home())
    lightbrarian_root_path = os.path.join(home_folder_path, '.lightbrarian')
    lightbrarian_reading_list_path = os.path.join(lightbrarian_root_path, 'default_reading_list.json')

    initialize(lightbrarian_root_path, lightbrarian_reading_list_path)

    # https://www.peterbe.com/plog/vars-argparse-namespace-into-a-function
    if command == 'search':
        search_books(**vars(args), google_api_token=google_api_token, lightbrarian_reading_list_path=lightbrarian_reading_list_path)
    elif command == 'list':
        list_books(lightbrarian_reading_list_path=lightbrarian_reading_list_path)

if __name__ == "__main__":
    cli()