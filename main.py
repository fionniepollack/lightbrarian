import json
import argparse
import os

from googleapiclient.discovery import build

def search_books(command, book_title, book_author, book_publisher, google_api_token):
    print(f'command: {command}')
    print(f'book_title: {book_title}')
    print(f'book_author: {book_author}')

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

    print(query_string)

    with build('books', 'v1', developerKey=google_api_token) as service:
        response = service.volumes().list(q=query_string).execute()

    print(json.dumps(response, sort_keys=True, indent=4))

def parse_arguments():
    parser = argparse.ArgumentParser(description = "A command line application to search for books and construct a reading list.")
    subparsers = parser.add_subparsers(title = "command", dest = "command")
    subparsers.required = True
    
    parser_search = subparsers.add_parser("search", help = "Search for available books")
    parser_search.add_argument("--book-title", type = str, help = "A book title to search for")
    parser_search.add_argument("--book-author", type = str, help = "A book author to search for")
    parser_search.add_argument("--book-publisher", type = str, help = "A book publisher to search for")

    # parser_bindiff = subparsers.add_parser("binexport", help = "Dump bindiff database")
    # parser_bindiff.add_argument("bindiff_output", type = str, help = "Output BinExport database file")
    # parser_bindiff.set_defaults(handler = handle_binexport)
    return parser.parse_args()

def cli():
    args = parse_arguments()
    
    command = args.command

    google_api_token = os.environ['GOOGLE_API_TOKEN']

    # https://www.peterbe.com/plog/vars-argparse-namespace-into-a-function
    if command == 'search':
        search_books(**vars(args), google_api_token=google_api_token)

if __name__ == "__main__":
    cli()