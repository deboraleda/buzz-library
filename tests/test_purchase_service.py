import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)

import unittest
from unittest.mock import patch, MagicMock
from src import purchase_service

class PurchaseServiceTest(unittest.TestCase):
    
    @patch('src.model.db.session.commit')
    @patch('src.model.db.session.add')
    @patch('src.model.Book')
    @patch('src.model.logger.info')
    def test_create_purchase(self, mock_info, MockBook, mock_add, mock_commit):
        mock_book_instance = MagicMock()
        mock_book_instance.id = 1
        mock_book_instance.stock = 10
        mock_book_instance.deleted = False

        MockBook.query.filter.return_value.with_for_update.return_value.first.return_value = mock_book_instance

        quantity = 2
        book_id = 1

        new_purchase = purchase_service.create_purchase(book_id, quantity)

        assert new_purchase.get('quantity') == quantity
        assert new_purchase.get('book_id') == book_id
        assert mock_book_instance.stock == 10 - quantity
        assert new_purchase.get('status') == "Finished"

        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_info.assert_called_once()

    @patch('src.model.db.session.commit')
    @patch('src.model.db.session.add')
    @patch('src.model.Book')
    @patch('src.model.logger.info')
    def test_can_not_create_purchase(self, mock_info, MockBook, mock_add, mock_commit):
        mock_book_instance = MagicMock()
        mock_book_instance.id = 1
        mock_book_instance.stock = 10
        mock_book_instance.deleted = False

        MockBook.query.filter.return_value.with_for_update.return_value.first.return_value = mock_book_instance

        quantity = 0
        book_id = 1

        new_purchase = purchase_service.create_purchase(book_id, quantity)

        assert new_purchase.get('message') == "quantity can NOT be less than or equal to zero"

        mock_add.assert_not_called()
        mock_commit.assert_not_called()
        mock_info.assert_not_called()

    @patch('src.purchase_service.Request')
    def test_get_purchases(self, MockRequest):
        MockRequest.query.all.return_value = [
            MagicMock(serialize=lambda: {'quantity': 2, 'book_id': 1, 'status': "Finished"}),
            MagicMock(serialize=lambda:  {'quantity': 2, 'book_id': 3, 'status': "Finished"})
        ]

        purchases = purchase_service.get_purchases()

        self.assertEqual(len(purchases), 2)
        self.assertEqual(purchases[0]['book_id'], 1)
        self.assertEqual(purchases[1]['book_id'], 3)

        MockRequest.query.all.assert_called_once() 
    
    @patch('src.purchase_service.Request')
    def test_get_purchase_for_book(self, MockRequest):
        mock_filter = MagicMock()
        MockRequest.query.filter_by.return_value = mock_filter
        mock_filter.filter_by.return_value = mock_filter
        mock_filter.all.return_value = [
            MagicMock(serialize=lambda: {'quantity': 2, 'book_id': 1, 'status': "Finished"})
        ]

        purchases = purchase_service.get_purchases_for_book(1)

        self.assertEqual(len(purchases), 1)
        self.assertEqual(purchases[0]['book_id'], 1)

        MockRequest.query.filter_by.assert_called_once()  
        mock_filter.all.assert_called_once()