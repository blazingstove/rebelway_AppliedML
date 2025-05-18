import pytest
from library_manager.library import *
from library_manager.book import classic_books
from library_manager.utils import save_json

@pytest.fixture
def lib_man():
    save_json(database_testpath, data={})
    lib_man = CLibraryManager()
    lib_man.load_db(test=True)
    for title in classic_books:
       lib_man.add_book(title, classic_books[title])
    return lib_man 

def test_add_books_to_library(lib_man)->None:
    assert len(lib_man.library_data['books']) == len(classic_books)

def test_find_book(lib_man)->None:
    for title_search in classic_books:
        found_titles = lib_man.find_book(title_search)
        assert len(found_titles) == 1

def test_checkout_books(lib_man)->None:
    for title in classic_books:
        lib_man.check_out_book('test_borrower', title)
    for book in lib_man.library_data['books']:
        assert book.book_data['checked_out']

def test_return_books(lib_man)->None:
    for title in classic_books:
        lib_man.check_out_book('test_borrower', title)
    for title in classic_books:
        lib_man.return_books('test_borrower')
    for book in lib_man.library_data['books']:
        assert not book.book_data['checked_out']

def test_get_overdue_books(lib_man)->None:
    
    for title in classic_books:
        lib_man.check_out_book('test_borrower', title)

    for book in lib_man.library_data['books']:
        book.book_data['checked_out_date'] = time.time() - ((s_max_checkout_days + 1) * s_secs_in_day)
        lib_man.library_data['data'][book.book_id] = book.book_data
    
    overdue_books = lib_man.list_overdue_books()
    
    assert len(overdue_books.keys()) == len(classic_books)
   
def test_remove_books_from_library(lib_man)->None:
    for title in classic_books:
        lib_man.remove_book(title)
    assert len(lib_man.library_data['books']) == 0