from src.model import Book
from . import logger


def get_books(title=None, category=None):
    query = Book.query.filter(Book.deleted == False)
    
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%')) 
    if category:
        query = query.filter(Book.category == category)

    books = query.all()
    serialized_books = [book.serialize() for book in books]
    logger.info(f'Getting books: {serialized_books}')
    return serialized_books


def get_book_by_id(book_id):
    book = Book.query.filter(Book.id == book_id, Book.deleted == False).first()

    if not book:
        logger.info(f'No book found with id: {book_id}')
        return {"message": "not found"}

    logger.info(f'Getting book: {book_id}')
    return book.serialize()


def add_book(title, author, publication_year, stock, category):
    if stock <= 0:
        return {"message": "stock can NOT be less than or equal to zero"}
    book = Book.create(title, author, publication_year, stock, category)
    logger.info(f'Created new book: {book}')
    return book.serialize()


def update_book(book_id, title, author, publication_year, stock, category):
    book = Book.query.filter(Book.id == book_id, Book.deleted == False).first()
    if not book:
        logger.info(f'No book found with id: {book_id}')
        return {"message": "not found"}
    
    book.update(
        title=title,
        author=author,
        publication_year=publication_year,
        stock=stock,
        category=category
    )
    logger.info(f'Updated book: {book_id}')
    return book.serialize()


def delete_book(book_id):
    book = Book.query.filter(Book.id == book_id, Book.deleted == False).first()
    if not book:
        logger.info(f'No book found with id: {book_id}')
        return False
    book.delete()
    logger.info(f'Deleted book: {book_id}')
    return True


def serialize_book(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publication_year': book.publication_year,
        'stock': book.stock,
        'category': book.category
    }


Book.serialize = serialize_book