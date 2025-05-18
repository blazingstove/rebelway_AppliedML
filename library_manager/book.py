import time
import copy
from dataclasses import dataclass, field
from library_manager.utils import get_unique_id

book_template_data = {"title": "",
                      "author": "",
                      "checked_out": False,
                      "checked_out_by": "",
                      "checked_out_date": 0,
                    }


classic_books = {
                "Pride and Prejudice": "Jane Austen",
                "Moby-Dick": "Herman Melville",
                "1984": "George Orwell",
                "The Great Gatsby": "F. Scott Fitzgerald",
                "War and Peace": "Leo Tolstoy",
                "To Kill a Mockingbird": "Harper Lee",
                "Crime and Punishment": "Fyodor Dostoevsky",
                "The Catcher in the Rye": "J.D. Salinger",
                "The Odyssey": "Homer",
                "Don Quixote": "Miguel de Cervantes"
                }

def get_template_book_data():
    return copy.deepcopy(book_template_data)

@dataclass
class CBook:
    """  A class for managing a book """

    book_data: dict=field(default_factory=get_template_book_data)
    book_id: str=field(init=True, default_factory=get_unique_id)

    def check_out_book(self, borrower_name, title):
        """ Check out this book
        
        Args:
            borrower_name (str): name of the borrower
            title (str): title of the book that the borrower wants to check out
        """

        if title != self.book_data['title']:
            print(title)
            print(self.book_data['title'])
            return
         
        if self.book_data['checked_out']:
            if self.book_data['checked_out_by'] != borrower_name:
                print(f"Book is already checked out by: { self.book_data['checked_out_by']}")
                return
        
        self.book_data['checked_out'] = True
        self.book_data['checked_out_by'] = borrower_name
        self.book_data['checked_out_date'] = time.time()
        
        print(f"{title} now checked out by {borrower_name}")
     
    def return_book(self, borrower_name): 
        """ Return the book to the library"""
        
        if not self.book_data['checked_out']:
            return True
        
        if borrower_name == self.book_data['checked_out_by']:
            self.book_data['checked_out'] = False
            self.book_data['checked_out_by'] = ''
            self.book_data['checked_out_date'] = 0