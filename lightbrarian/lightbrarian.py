import json
import argparse
import os
import sys
from pathlib import Path

# https://developers.google.com/books/docs/v1/libraries
# Using the Google API client to work with the Books API.
from googleapiclient.discovery import build

def print_books(books):
    for i, book in enumerate(books):
        print(f"Book ID: [{i + 1}]")
        print(f"Title: {book['volumeInfo'].get('title', 'Unknown title')}")
        print(f"Author(s): {','.join(book['volumeInfo'].get('authors', ['Unknown author']))}")
        print(f"Publisher: {book['volumeInfo'].get('publisher', 'Unknown publisher')}")
        print('---')

def search_books(command, book_title, book_author, book_publisher, max_results, google_api_token, lightbrarian_reading_list_path):
    '''
    Use the Google Books API to search for books (aka volumes).
    '''
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

    # Construct a query string ('q') to be used when running the query.
    # https://developers.google.com/books/docs/v1/using#PerformingSearch
    for query_element in query_elements:
        if query_element['search_value'] is not None:
            query_string_list.append(f"{query_element['search_field']}:{query_element['search_value']}") 

    query_string = "+".join(query_string_list)

    # The build() function allows us to generate a 'service' which can then be used to invoke the Google Books API.
    # https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build
    with build('books', 'v1', developerKey=google_api_token) as service:
        response = service.volumes().list(q=query_string, maxResults=max_results).execute()

    books = response.get("items", [])

    total_search_results = len(books)

    print("")
    print("---SEARCH RESULTS---")
    print("")
    print(f"Total search results: {total_search_results}")
    print("")

    print_books(books)

    # Prompt user to enter a book ID to save to the reading list.
    if total_search_results > 0:
        selected_book_id = -1
        while not selected_book_id in range(0,(total_search_results + 1)):
            selected_book_id = input(f"Enter Book ID (1-{total_search_results}) to save to reading list or 0 to skip: ") or 0
            try:
                selected_book_id = int(selected_book_id)
            except ValueError:
                selected_book_id = -1
                print(f"Invalid Book ID, please enter a number between 1 and {total_search_results}.")

        if selected_book_id != 0:
            save_to_reading_list(lightbrarian_reading_list_path, books[selected_book_id-1])

    return books

def save_to_reading_list(lightbrarian_reading_list_path, book):
    with open(lightbrarian_reading_list_path, 'r+') as lightbrarian_reading_list_file:
        data = json.load(lightbrarian_reading_list_file)
        data["books"].append(book)
        lightbrarian_reading_list_file.seek(0)
        json.dump(data, lightbrarian_reading_list_file)
        lightbrarian_reading_list_file.truncate()

def print_reading_list(lightbrarian_reading_list_path):
    try:
        with open(lightbrarian_reading_list_path, 'r') as lightbrarian_reading_list_file:
            reading_list_data = json.load(lightbrarian_reading_list_file)
    except FileNotFoundError as exception:
        sys.exit("No reading list found. Please run the search command to add books to your reading list.")
    
    books = reading_list_data["books"]

    print_books(books)

    return books

def parse_arguments():
    '''
    Parse the arguments provided at the command line.

    Two subcommands are supported:
    1. lightbrarian search
    2. lightbrarian list
    '''
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
    '''
    Create the reading list file if it does not exist already.
    '''
    if not os.path.exists(lightbrarian_root_path):
        os.makedirs(lightbrarian_root_path)

    if not os.path.exists(lightbrarian_reading_list_path):
        with open(lightbrarian_reading_list_path, "w") as lightbrarian_reading_list_file:
            blank_reading_list = {
                "books": []
            }
            json.dump(blank_reading_list, lightbrarian_reading_list_file)

def cli():
    '''
    Main entry point into the script.
    '''
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
        print_reading_list(lightbrarian_reading_list_path=lightbrarian_reading_list_path)

if __name__ == "__main__":
    cli()