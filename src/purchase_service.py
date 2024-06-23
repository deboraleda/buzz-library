from .model import Request
from . import logger

def create_purchase(book_id, quantity):
    if quantity <= 0:
        return {"message": "quantity can NOT be less than or equal to zero"}
    new_purchase = Request.create(book_id, quantity)
    logger.info(f'Purchase created: {new_purchase}')
    return new_purchase

def get_purchases():
    purchases = Request.query.all()
    serialized_purchases = [purchase.serialize() for purchase in purchases]
    logger.info(f'Getting Purchases: {serialized_purchases}')
    return serialized_purchases

def get_purchases_for_book(book_id):
    purchases = Request.query.filter_by(book_id=book_id).all()
    if purchases:
        logger.info(f'Found {len(purchases)} purchases for book ID {book_id}.')
        return [purchase.serialize() for purchase in purchases]
    else:
        logger.info(f'No purchase found for book ID {book_id}.')
        return []