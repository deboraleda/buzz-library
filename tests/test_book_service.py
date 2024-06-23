import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)

import unittest
from unittest.mock import patch, MagicMock
from src import book_service

class BookServiceTest(unittest.TestCase):
    
    @patch('src.model.db.session.commit')
    @patch('src.model.db.session.add')
    @patch('src.model.logger.info')
    def test_create_book(self, mock_info, mock_add, mock_commit):

        title = "Sample Book"
        author = "Author Name"
        publication_year = 2021
        stock = 10
        category = "Fiction"

        new_book = book_service.add_book(title, author, publication_year, stock, category)

        assert new_book.get('title') == title
        assert new_book.get('author') == author
        assert new_book.get('publication_year') == publication_year
        assert new_book.get('stock') == stock
        assert new_book.get('category') == category
        assert not new_book.get('deleted')

        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_info.assert_called_once()

    @patch('src.model.db.session.commit')
    @patch('src.model.db.session.add')
    @patch('src.model.logger.info')
    def test_can_not_create_book(self, mock_info, mock_add, mock_commit):

        title = "Sample Book"
        author = "Author Name"
        publication_year = 2021
        stock = -10
        category = "Fiction"

        new_book = book_service.add_book(title, author, publication_year, stock, category)

        assert new_book.get('message') == "stock can NOT be less than or equal to zero"

        mock_add.assert_not_called()
        mock_commit.assert_not_called()
    
    @patch('src.book_service.Book')
    def test_get_books(self, MockBook):
        mock_filter = MagicMock()
        MockBook.query.filter.return_value = mock_filter
        mock_filter.filter.return_value = mock_filter
        mock_filter.all.return_value = [
            MagicMock(serialize=lambda: {'title': "Effective Python", 'category': "Programming"}),
            MagicMock(serialize=lambda: {'title': "Fluent Python", 'category': "Programming"})
        ]

        books = book_service.get_books(title="Python", category="Programming")

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['title'], "Effective Python")
        self.assertEqual(books[1]['title'], "Fluent Python")

        MockBook.query.filter.assert_called_once()  
        mock_filter.filter.assert_called() 
        mock_filter.all.assert_called_once()
    
    @patch('src.book_service.Book')
    def test_get_book_by_id(self, MockBook):
        mock_book_instance = MagicMock()
        mock_book_instance.serialize.return_value = {"title": "Python", "category": "Programming"}
        MockBook.query.filter.return_value.first.return_value = mock_book_instance
        
        book = book_service.get_book_by_id(1)

        self.assertEqual(book['title'], 'Python')
        self.assertEqual(book['category'], 'Programming')

        MockBook.query.filter.assert_called_once()  
        MockBook.query.filter.return_value.first.assert_called_once() 
        mock_book_instance.serialize.assert_called_once()

    
    @patch('src.book_service.Book')
    def test_get_book_by_id_not_found(self, MockBook):
        MockBook.query.filter.return_value.first.return_value = None
        book = book_service.get_book_by_id(1)
        self.assertEqual(book, {"message": "not found"})

        MockBook.query.filter.assert_called_once()
        MockBook.query.filter.return_value.first.assert_called_once()
    
    @patch('src.book_service.Book')
    def test_update_book_success(self, MockBook):
        mock_book_instance = MagicMock()
        mock_book_instance.serialize.return_value = {
            'id': 1,
            'title': "Updated Title",
            'author': "Updated Author",
            'publication_year': 2024,
            'stock': 50,
            'category': "Updated Category"
        }

        MockBook.query.filter().first.return_value = mock_book_instance

        def update_mock(title, author, publication_year, stock, category):
            mock_book_instance.title = title
            mock_book_instance.author = author
            mock_book_instance.publication_year = publication_year
            mock_book_instance.stock = stock
            mock_book_instance.category = category

        mock_book_instance.update = MagicMock(side_effect=update_mock)

        result = book_service.update_book(1, "Updated Title", "Updated Author", 2024, 50, "Updated Category")

        self.assertEqual(result['title'], "Updated Title")  
        self.assertEqual(result['author'], "Updated Author") 
        self.assertEqual(result['publication_year'], 2024)
        self.assertEqual(result['stock'], 50)
        self.assertEqual(result['category'], "Updated Category") 
        mock_book_instance.update.assert_called_once_with(
            title="Updated Title",
            author="Updated Author",
            publication_year=2024,
            stock=50,
            category="Updated Category"
        )  
        mock_book_instance.serialize.assert_called_once()

    
    @patch('src.book_service.Book')
    def test_update_book_not_found(self, MockBook):
        MockBook.query.filter().first.return_value = None

        result = book_service.update_book(999, "New Title", "New Author", 2023, 100, "New Category")

        self.assertEqual(result, {"message": "not found"}) 


    @patch('src.book_service.Book')
    def test_delete_book_success(self, MockBook):
        mock_book_instance = MagicMock()
        MockBook.query.filter().first.return_value = mock_book_instance

        mock_book_instance.deleted = False
        result = book_service.delete_book(1)
        self.assertTrue(result)
        mock_book_instance.delete.assert_called_once()

    @patch('src.book_service.Book')
    def test_delete_book_not_found(self, MockBook):
        MockBook.query.filter().first.return_value = None
        result = book_service.delete_book(999)

        self.assertFalse(result) 

if __name__ == '__main__':
    unittest.main()