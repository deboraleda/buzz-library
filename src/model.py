from .db import db
import logging

logger = logging.getLogger(__name__)

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=True)
    deleted = db.Column(db.Boolean, default=False, nullable=False) 

    def __init__(self, title, author, publication_year, stock, category, deleted):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.stock = stock
        self.category = category
        self.deleted = deleted
    
    @classmethod
    def create(cls, title, author, publication_year, stock, category):
        new_book = cls(title=title, author=author,
                        publication_year=publication_year, stock=stock,
                        category=category, deleted=False)
        db.session.add(new_book)
        db.session.commit()
        logger.info(f'Created new book: {new_book}')
        return new_book
    
    def delete(self):
        logger.info(f'Soft deleting book {self.id} - Title: {self.title}')
        self.deleted = True
        db.session.commit()
    
    def update(self, title=None, author=None, publication_year=None, stock=None, category=None):
        if title is not None:
            self.title = title
        if author is not None:
            self.author = author
        if publication_year is not None:
            self.publication_year = publication_year
        if stock is not None:
            self.stock = stock
        if category is not None:
            self.category = category

        db.session.commit()
        logger.info(f'Updated book {self.id} - Title: {self.title}, Author: {self.author}')

    def __repr__(self):
        return f"<Book {self.title}, by {self.author}>"


class Request(db.Model):
    __tablename__ = 'requests'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    book = db.relationship('Book')

    def __init__(self, book_id, quantity, status):
        self.book_id = book_id
        self.quantity = quantity
        self.status = status
    
    @classmethod
    def create(cls, book_id, quantity):
        book = Book.query.filter(Book.id == book_id, Book.deleted == False).with_for_update().first()

        if not book:
            logger.info(f'Book not found: {book_id}')
            return {"message": "Book not found."}
        if book.stock < quantity:
            logger.info(f'Insufficient stock. Refused!')
            return {"message": "Insufficient stock. Refused!"}

        new_request = cls(book_id=book.id, quantity=quantity, status="Finished")
        
        db.session.add(new_request)
        book.stock -= quantity
        db.session.commit()
        logger.info(f'Created new purchase: {new_request}')
        return new_request.serialize()
    
    def serialize(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'quantity': self.quantity,
            'status': self.status
        }

    def __repr__(self):
        return f"<Pedido {self.id} - Book ID {self.book_id} - Quantity {self.quantity} - Status {self.status}>"
