import requests

from .models import Book, Category, Author


def import_from_category(category, description=None):
    max_results = 40
    start = 0

    results = search(category, start, max_results)
    cat, created = Category.objects.get_or_create(name=category, description=description)
    insert(results, cat)
    total = results["totalItems"]

    while total > 0:
        total = total - max_results
        start = start + max_results
        insert(search(category, start, max_results), cat)


def insert(results, category):
    k = "volumeInfo"
    if "items" not in results:
        return
    books = results["items"]
    b = {}

    for book in books:
        try:
            authors = book[k]["authors"]
            b['title'] = book[k]["title"]
            b['description'] = book[k].get("description", False)
            if not b['description']:
                print "skipping book without descr..."
                continue
            b['info_link'] = book[k].get("infoLink")
            b['thumbnail_url'] = book[k]["imageLinks"]["thumbnail"]
            b['publisher'] = book[k].get("publisher")
            the_authors = [author for author in insert_authors(authors)]
            the_book = Book.objects.create(**b)
            the_book.authors.add(*the_authors)
            category.book_set.add(the_book)
            print "inserted book: ", the_book, the_book.id
        except Exception as e:
           print "skipping invalid entry...", e


def insert_authors(authors):
    for name in authors:
        a, created = Author.objects.get_or_create(name=name)
        yield a


def search(category, start, max_results):
    url = 'https://www.googleapis.com/books/v1/volumes?q=subject:"%s"&maxResults=%d&startIndex=%d' % (category, max_results, start)
    print "will search: ", url
    return requests.get(url).json()

    
