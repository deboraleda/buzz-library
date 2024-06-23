from . import app, logger
from flask import jsonify, request, abort
from .db import db
from . import book_service, purchase_service


def assert_book_data():
    required_fields = ['title', 'author', 'publication_year', 'stock', 'category']
    data = request.get_json() 
    if not data:
        logger.info(f'No book data available: {data}')
        abort(400, description="No data provided.")
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        logger.info(f'Missing fields: {missing_fields}')
        abort(400, description=f"Missing fields: {', '.join(missing_fields)}")
    return data


@app.route('/books', methods=['GET'])
def get_books():
    title = request.args.get('title')  
    category = request.args.get('category')  

    books = book_service.get_books(title=title, category=category)  
    logger.info(f'Getting books: {books}')
    return jsonify(books), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = book_service.get_book_by_id(book_id)
    if book.get("message"):
        logger.info(f'No book found with id: {book_id}')
        return jsonify(book), 404
    logger.info(f'Getting book: {book_id}')
    return jsonify(book), 200


@app.route('/book', methods=['POST'])
def create_book():
    data = assert_book_data()  
    book = book_service.add_book(data['title'], data['author'], data['publication_year'], data['stock'], data['category'])
    if book.get("message"):
        logger.info(f'Can not create book: {book}')
        return jsonify(book), 400
    logger.info(f'Created book: {book}')
    return jsonify(book), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def edit_book(book_id):
    data = request.get_json()
    book = book_service.update_book(book_id, data.get('title'),
                            data.get('author'),
                            data.get('publication_year'),
                            data.get('stock'),
                            data.get('category'))
    if book.get("message"):
        logger.info(f'No book found with id: {book_id}')
        return jsonify(book), 404
    logger.info(f'Updated book: {book_id}')
    return jsonify(book), 200


@app.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    removed = book_service.delete_book(book_id)
    if not removed:
        logger.info(f'No book found with id: {book_id}')
        return jsonify({"message": "not found"}), 404
    logger.info(f'Deleting book with id: {book_id}')
    return jsonify({'success': removed}), 200


@app.route('/purchase', methods=['POST'])
def add_purchase():
    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity')

    if book_id == None or quantity == None:
        logger.info(f'No request data available: {data}')
        abort(400, description="Missing book_id or quantity.")

    purchase = purchase_service.create_purchase(book_id, quantity)
    if purchase.get("message"):
        logger.info(f'Purchase not available: {purchase}')
        return jsonify(purchase), 400

    logger.info(f'New purchase created successfully: {purchase}')
    return jsonify(purchase), 201

@app.route('/purchases',  methods=['GET'])
def get_purchases():
    purchases = purchase_service.get_purchases()
    logger.info(f'Getting purchases: {purchases}')
    return jsonify(purchases), 200


@app.route('/purchases/book/<int:book_id>',  methods=['GET'])
def get_purchase_for_book(book_id):
    purchases = purchase_service.get_purchases_for_book(book_id)
    logger.info(f'Found {len(purchases)} purchases for book ID {book_id}.')
    return jsonify(purchases), 200

