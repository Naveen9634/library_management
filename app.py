from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample data structure for books, with IDs for identification
books = []
next_id = 1  # Simple counter for assigning book IDs

@app.route('/books', methods=['GET'])
def get_books():
    """Get all books"""
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    """Add a new book"""
    global next_id
    data = request.get_json()
    
    # Assign an ID to the new book and append it to the list
    new_book = {
        "id": next_id,
        "title": data.get("title"),
        "author": data.get("author")
    }
    books.append(new_book)
    next_id += 1  # Increment the ID for the next book
    return jsonify({"message": "Book added successfully", "book": new_book}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    book = next((b for b in books if b['id'] == book_id), None)
    if book is None:
        abort(404)  # Not found
    return jsonify(book)

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a specific book by ID"""
    book = next((b for b in books if b['id'] == book_id), None)
    if book is None:
        abort(404)  # Not found
    
    data = request.get_json()
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    
    return jsonify({"message": "Book updated successfully", "book": book})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a specific book by ID"""
    global books
    books = [b for b in books if b['id'] != book_id]  # Filter out the book to delete
    return jsonify({"message": "Book deleted successfully"}), 204

if __name__ == '__main__':
    app.run(debug=True)
