from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Routes for CRUD operations
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({'id': book.id, 'title': book.title, 'author': book.author})
    return jsonify(book_list)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author})
    return jsonify({'message': 'Book not found'}), 404

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
