from library_manager.book import *

def test_create_new_book()->None:
    book = CBook()
    book.book_data['title']  = 'Test_Book'
    book.book_data['author'] = 'Test_Author'
    assert book.book_data['title']  == 'Test_Book' and  book.book_data['author'] == 'Test_Author'

def test_unique_book_id()->None:
    book1 = CBook()
    book2 = CBook()
    assert book1.book_id != book2.book_id

def test_check_out_book()->None:
    book = CBook()
    book.book_data['title']  = 'Test_Book'
    book.book_data['checked_out'] = False
    book.check_out_book('test_borrower', 'Test_Book')
    assert book.book_data['checked_out'] and (book.book_data['checked_out_by'] == 'test_borrower')

def test_return_book()->None:
    book = CBook()
    book.book_data['title']  = 'Test_Book'
    book.check_out_book('test_borrower', 'Test_Book')
    book.return_book('test_borrower')
    assert not book.book_data['checked_out'] and (book.book_data['checked_out_by'] != 'test_borrower')
