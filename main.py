#library system
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn})"

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        return f"Added: {book.display_info()}"

    def remove_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                return f"Removed: {book.display_info()}"
        return f"Book '{title}' not found."

    def list_books(self):
        if not self.books:
            return f"{self.name} has no books."
        result = f"\n=== Books in {self.name} ===\n"
        for i, book in enumerate(self.books, 1):
            result += f"{i}. {book.display_info()}\n"
        return result

    def search_by_title(self, search_term):
        found = [book for book in self.books
                 if search_term.lower() in book.title.lower()]
        if found:
            result = f"\nFound {len(found)} book(s):\n"
            for book in found:
                result += f"- {book.display_info()}\n"
            return result
        return f"Book '{search_term}' not found"

    #library test

    library = Library()

    book1 = Book("Sweetbitter", "Stephanie Danler", "1111")
    book2 = Book("Masters of Death", "Olivie Blake", "2222")
    book3 = Book("Sword Catcher", "Cassandra Clare", "3333")

    library.list_books()
    library.search_book_by_title("Sweetbitter")
    library.remove_book("Sword Catcher")
    library.list_books()