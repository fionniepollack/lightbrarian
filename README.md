# lightbrarian
A command line application that allows you to use the Google Books API to search for books and construct a reading list.

# Installation
```
$ pip3 install --upgrade --user git+https://github.com/fionniepollack/lightbrarian@main

# Confirm installation
$ lightbrarian --help
```

A Google API key is required to use `lightbrarian`. See [here](https://cloud.google.com/docs/authentication/api-keys) for instructions on how to generate the API key.

Once you've obtained an API key, set it as an environment variable in your shell before running any `lightbrarian` commands:
```
$ export GOOGLE_API_TOKEN=<INSERT TOKEN HERE>
```

# Developer Installation
```
$ git clone https://github.com/fionniepollack/lightbrarian

$ cd lightbrarian

$ python3 -m venv .venv

$ source .venv/bin/activate

$ pip3 install --editable .
```

# Usage
The `lightbrarian` CLI utility supports two sub-commands:
- `lightbrarian search [-h] [--book-title BOOK_TITLE] [--book-author BOOK_AUTHOR] [--book-publisher BOOK_PUBLISHER] [--max-results MAX_RESULTS]`
- `lightbrarian list [-h]`

Run `lightbrarian --help` or `lightbrarian <subcommand> --help` for details on using each sub-command.

### Search
The `search` sub-command allows the user to search for books in the Google book store based using the following arguments:
```
--book-title
--book-author
--book-publisher
```

After the search results are displayed you'll have the option to save one of the books to your lightbrarian reading list.

#### Example Searches

Search using just a book title:
```
$ lightbrarian search --book-title "The Great Gatsby"

---SEARCH RESULTS---

Total search results: 5

Book ID: [1]
Title: The Great Gatsby
Author(s): F. Scott Fitzgerald
Publisher: Simon and Schuster
---
Book ID: [2]
Title: The Great Gatsby
Author(s): Francis Scott Fitzgerald
Publisher: Everyman's Library
---
Book ID: [3]
Title: The Great Gatsby
Author(s): F. Scott Fitzgerald
Publisher: Signet
---
Book ID: [4]
Title: Great Gatsby
Author(s): Unknown author
Publisher: Unknown publisher
---
Book ID: [5]
Title: The Great Gatsby : Om Illustrated Classics
Author(s): F Scott Fitzgerald
Publisher: Om Books International
---
Enter Book ID (1-5) to save to reading list or 0 to skip:
```

Search using a title and publisher:
```
$ lightbrarian search --book-title "The Great Gatsby" --book-publisher "Signet"

---SEARCH RESULTS---

Total search results: 2

Book ID: [1]
Title: The Beautiful and Damned
Author(s): F. Scott Fitzgerald
Publisher: Penguin
---
Book ID: [2]
Title: A Cat on the Cutting Edge
Author(s): Lydia Adamson
Publisher: Signet Book
---
Enter Book ID (1-2) to save to reading list or 0 to skip: 2
```

### List
The `list` sub-command prints the user's reading list.

```
$ lightbrarian list

Book ID: [1]
Title: A Cat on the Cutting Edge
Author(s): Lydia Adamson
Publisher: Signet Book
---
```
