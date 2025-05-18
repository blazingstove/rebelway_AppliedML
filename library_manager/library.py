import os
import time
import inspect
from dataclasses import dataclass, field
from library_manager.book import CBook
from library_manager.utils import load_json, save_json, get_unique_id

database_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
database_path = os.path.join(database_dir, 'library_database.json')
database_testpath = os.path.join(database_dir, 'test_library_database.json')

s_max_checkout_days = 30
s_secs_in_day = (60 * 60 * 24)

@dataclass
class CLibraryManager:
    """ A class for managing a book library """

    library_data: dict=field(default_factory=dict)
    db_path: str=database_path
    
    def load_db(self, test=False):
        """ Load the library database """
    
        if test:
            self.db_path = database_testpath
        
        # Ensure we have a data base JSON if this is a new system
    
        if not os.path.exists(self.db_path):
            save_json(self.db_path)
    
        # Load the book data base
    
        self.library_data = {"data":{},"books":[]}
        self.library_data["data"] = load_json(self.db_path)

        # Cache the book objects

        for id in self.library_data["data"]:
            self.library_data["books"].append(CBook(self.library_data["data"][id], id))

    def _update_db(self):
        save_json(self.db_path, data=self.library_data['data'])
    
    def add_book(self, title, author):
        """ Add a new book to the system 
        Args:
            title (str) : title of the new book
            author (str): author of the new book
        
        """
        
        # Early out if the book already exists in the database

        for book in self.library_data['books']:
            if book.book_data['title'] == title:
                return
       
        # Add the new book

        book = CBook()
        book.book_data['title'] = title
        book.book_data['author'] = author
        self.library_data["data"][book.book_id] = book.book_data
        self.library_data["books"].append(book)
        self._update_db()

        print(f'Added book to library system: {title}')

    def remove_book(self, title):
        """ Add a new book to the system 
        Args:
            title (str) : title of the new book
            author (str): author of the new book
        
        """
        
        for book in self.library_data['books']:
            if book.book_data['title'] == title:
                del self.library_data["data"][book.book_id]
                self.library_data["books"].remove(book)
                print(f'Removed book from library system: {title}')
                break

        self._update_db()
    
    def check_out_book(self, borrower_name, title):
        """Checkout the input title to the input borrower
        
        Args:
            borrower_name (str): name of borrower
            title (str): name of book
        
        """

        for book in self.library_data['books']:
            book.check_out_book(borrower_name, title)
            self.library_data['data'][book.book_id] = book.book_data

        self._update_db()

    def return_books(self, borrower_name, book_titles=[]):
        """Checkout the input title to the input borrower
        
        Args:
            borrower_name (str): name of borrower returning books
            book_titles (list): (optional) name of books, if empty then return all books checkout to this borrower
        
        """
        
        for book in self.library_data['books']:

            if len(book_titles):
                if book.book_data['title'] not in book_titles:
                    continue
            
            # Attempt to return the book if its checked by the input borrower

            book.return_book(borrower_name)
            
            print(f"{book.book_data['title'] } returned to library by {borrower_name}")

            # Update the data model

            self.library_data['data'][book.book_id] = book.book_data
    
        self._update_db()

    def list_overdue_books(self)->dict:
        """ Return a dict() of book titles that have been checked out 
        for over 30 days, where each key is the book title and each value is a dict where the key
        is the borrower and the value is the days overdue

        Example: {"book_title":{"borrower": 3},..} 
           
        """

        overdue_books = dict()

        for book in self.library_data['books']:
            if not book.book_data['checked_out']:
                continue

            title = book.book_data['title']
            borrower_name = book.book_data['checked_out_by']

            secs_since_checkout = time.time() - book.book_data['checked_out_date']
            days_checked_out = (secs_since_checkout / s_secs_in_day)

            # Report on overdue book

            if days_checked_out > s_max_checkout_days:
                overdue_days = int(days_checked_out - s_max_checkout_days)
                overdue_books[title] = {borrower_name : overdue_days}
                
                print(f"Book: {title} | Checked out by: {borrower_name} | {overdue_days} days overdue")
        
        return overdue_books
    
    def find_book(self, title_search)->list:
        """ Try and find the book with the specified search string """
        found_books = []
        for book in self.library_data['books']:
            title = book.book_data['title']
            if title_search.lower() in title.lower():
                found_books.append(title)
        return found_books
