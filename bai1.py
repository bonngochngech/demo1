import json
import time
from dataclasses import dataclass, asdict

# ==========================
# Decorator
# ==========================

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Execution Time: {end-start:.6f}s")
        return result
    return wrapper


# ==========================
# Exception
# ==========================

class BookNotFound(Exception):
    pass


class OutOfStock(Exception):
    pass


# ==========================
# Book
# ==========================

@dataclass(order=True)
class Book:
    id: str
    title: str
    author: str
    year: int
    quantity: int

    def __str__(self):
        return (f"{self.id:6} | "
                f"{self.title:25} | "
                f"{self.author:20} | "
                f"{self.year} | "
                f"{self.quantity}")


# ==========================
# Library
# ==========================

class Library:

    def __init__(self):
        self.books = []

    @timer
    def add_book(self, book):
        self.books.append(book)
        print("Added!")

    @timer
    def display(self):

        if not self.books:
            print("No books.")
            return

        print("-"*80)

        for book in self.books:
            print(book)

        print("-"*80)

    @timer
    def remove(self, book_id):

        for book in self.books:

            if book.id == book_id:
                self.books.remove(book)
                print("Deleted.")
                return

        raise BookNotFound("Book not found.")

    @timer
    def search(self, keyword):

        result = []

        for book in self.books:

            if keyword.lower() in book.title.lower():
                result.append(book)

        return result

    @timer
    def borrow(self, book_id):

        for book in self.books:

            if book.id == book_id:

                if book.quantity == 0:
                    raise OutOfStock("Book out of stock.")

                book.quantity -= 1
                print("Borrow success.")
                return

        raise BookNotFound("Book not found.")

    @timer
    def give_back(self, book_id):

        for book in self.books:

            if book.id == book_id:
                book.quantity += 1
                print("Return success.")
                return

        raise BookNotFound()

    @timer
    def save(self, filename="books.json"):

        data = [asdict(book) for book in self.books]

        with open(filename, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4)

        print("Saved.")

    @timer
    def load(self, filename="books.json"):

        with open(filename, "r", encoding="utf8") as f:

            data = json.load(f)

        self.books = [Book(**x) for x in data]

        print("Loaded.")

    # ---------------------
    # Merge Sort
    # ---------------------

    def merge_sort(self, arr):

        if len(arr) <= 1:
            return arr

        mid = len(arr)//2

        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])

        return self.merge(left, right)

    def merge(self, left, right):

        result = []

        i = j = 0

        while i < len(left) and j < len(right):

            if left[i].title < right[j].title:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result

    def sort_books(self):
        self.books = self.merge_sort(self.books)

    # ---------------------
    # Generator
    # ---------------------

    def search_generator(self, keyword):

        for book in self.books:

            if keyword.lower() in book.title.lower():
                yield book


# ==========================
# Menu
# ==========================

library = Library()

while True:

    print("""
======== LIBRARY =========

1.Add Book
2.Display
3.Search
4.Delete
5.Borrow
6.Return
7.Save
8.Load
9.Sort
0.Exit

==========================
""")

    choice = input("Choice: ")

    try:

        if choice == "1":

            id = input("ID: ")
            title = input("Title: ")
            author = input("Author: ")
            year = int(input("Year: "))
            quantity = int(input("Quantity: "))

            library.add_book(Book(id, title, author, year, quantity))

        elif choice == "2":

            library.display()

        elif choice == "3":

            key = input("Keyword: ")

            books = library.search(key)

            for b in books:
                print(b)

        elif choice == "4":

            id = input("ID: ")

            library.remove(id)

        elif choice == "5":

            id = input("ID: ")

            library.borrow(id)

        elif choice == "6":

            id = input("ID: ")

            library.give_back(id)

        elif choice == "7":

            library.save()

        elif choice == "8":

            library.load()

        elif choice == "9":

            library.sort_books()

        elif choice == "0":

            break

        else:

            print("Invalid!")

    except Exception as e:

        print(e)