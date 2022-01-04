import os
import pytest
# https://stackoverflow.com/a/54835985/17413097
from .lightbrarian import *

google_api_token = os.environ['GOOGLE_API_TOKEN']

# Create temporary default_reading_list.json to be used for all the tests.
@pytest.fixture(scope='session')
def test_initialize(tmp_path_factory):
    lightbrarian_reading_list_path = tmp_path_factory.mktemp('.lightbrarian') / 'default_reading_list.json'
    initialize(lightbrarian_reading_list_path.parent, lightbrarian_reading_list_path)
    return lightbrarian_reading_list_path

# Invoke the search_books function and save the first search result to the reading list.
def test_search_and_save_book(test_initialize, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 1)
    
    books = search_books(
        command='search',
        book_title='The',
        book_author=None,
        book_publisher=None,
        max_results=5,
        google_api_token=google_api_token,
        lightbrarian_reading_list_path=test_initialize
    )

    assert len(books) == 5

    # Confirm only 1 book is in the reading list.
    reading_list = print_reading_list(test_initialize)

    assert len(reading_list) == 1

def test_search_and_save_book_bad_user_input(test_initialize, monkeypatch):
    responses = iter(['this should be a number', 2])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))

    books = search_books(
        command='search',
        book_title='The',
        book_author=None,
        book_publisher=None,
        max_results=5,
        google_api_token=google_api_token,
        lightbrarian_reading_list_path=test_initialize
    )

    assert len(books) == 5

def test_delete_book_from_reading_list(test_initialize, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 1)

    deleted_book = delete_book_from_reading_list(
        command='delete',
        lightbrarian_reading_list_path=test_initialize
    )

    assert isinstance(deleted_book['volumeInfo']['title'], str)

def test_no_search_results(test_initialize):
    books = search_books(
        command='search',
        book_title='adbfpoa',
        book_author=None,
        book_publisher=None,
        max_results=5,
        google_api_token=google_api_token,
        lightbrarian_reading_list_path=test_initialize
    )

    assert len(books) == 0