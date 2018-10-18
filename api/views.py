from datetime import datetime
from . import app, api, auth
from .models import UserModel, BookModel, commit
from flask import g
from flask_restful import Resource, reqparse

# Use for HTTP basic auth
@auth.verify_password
def verify_password(email, password):
    user = UserModel.query.filter_by(email = email).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True

# Base URL
@app.route('/')
@app.route('/api')
def index():
    return "Welcome to the books wishlist API"

class Users(Resource):
    """
    Resource: users
    Endpoint: /api/users
    Methods: GET, POST
    """

    # Initialize POST request parser
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type = str, required = True,
            help = 'First name not provided')
        self.reqparse.add_argument('last_name', type = str, required = True,
            help = 'Last name not provided')
        self.reqparse.add_argument('email', type = str, required = True,
            help = 'Email address not provided')
        self.reqparse.add_argument('password', type = str, required = True,
            help = 'Password not provided')
        super(Users, self).__init__()

    # Return list of users
    def get(self):
        return {'users': list(map(lambda x: UserModel.serialize(x), UserModel.query.all()))}

    # Add new user
    def post(self):
        data = self.reqparse.parse_args()

        if UserModel.query.filter_by(email=data['email']).first() is not None:
            return { "message": "User with this email already exists" }, 409
        
        user = UserModel(email = data['email'], first_name = data['first_name'], last_name = data['last_name'])
        user.set_password(data['password'])
        user.add_to_db()
        commit()

        return { 'user': UserModel.serialize(user) }, 201

class User(Resource):
    """
    Resource: users
    Endpoint: /api/users/<id>
    Methods: GET
    """

    # Return user info for user <id>
    def get(self, id):
        user = UserModel.query.get_or_404(id)
        return { 'user': UserModel.serialize(user) }

class Books(Resource):
    """
    Resource: books
    Endpoint: /api/books
    Methods: GET, POST
    """

    # Initialize POST request parser
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = "Title not provided")
        self.reqparse.add_argument('author', type = str, required = True,
            help = "Author not provided")
        self.reqparse.add_argument('isbn', type = str, required = True,
            help = "ISBN not provided")
        self.reqparse.add_argument('pub_date', type = str, required = True,
            help = "Publication date not provided")
        super(Books, self).__init__()

    # Return list of books
    def get(self):
        return {'books': list(map(lambda x: BookModel.serialize(x), BookModel.query.all()))}
    
    # Add new book
    def post(self):
        data = self.reqparse.parse_args()
        
        # Publication date validation
        try:
            pub_date = datetime.strptime(data['pub_date'], '%Y-%m-%d')
        except:
            return { "message": "Publication date (pub_date) must be in YYYY-mm-dd format" }, 400
            
        if BookModel.query.filter_by(isbn=data['isbn']).first() is not None:
            return { "message": "Book with this ISBN already exists" }, 409

        book = BookModel(isbn = data['isbn'], title = data['title'], author = data['author'], pub_date = pub_date)
        book.add_to_db()
        commit()

        return { 'book': BookModel.serialize(book) }, 201

class Book(Resource):
    """
    Resource: books
    Endpoint: /api/books/<isbn>
    Methods: GET
    """

    # Return book info for book <isbn>
    def get(self, isbn):
        book = BookModel.query.get_or_404(isbn)
        return { 'book': BookModel.serialize(book) }

class UserBooks(Resource):
    """
    Resource: books
    Endpoint: /api/users/<id>/books
    Methods: GET, POST
    """

    # Initialize POST request parser
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = "Title not provided")
        self.reqparse.add_argument('author', type = str, required = True,
            help = "Author not provided")
        self.reqparse.add_argument('isbn', type = str, required = True,
            help = "ISBN not provided")
        self.reqparse.add_argument('pub_date', type = str, required = True,
            help = "Publication date not provided")
        super(UserBooks, self).__init__()

    # Return list of books on user's wishlist
    def get(self, id):
        user = UserModel.query.get_or_404(id)
        return { 'books': list(map(lambda x: BookModel.serialize(x), user.books)) }

    # Add new book to user's wishlist
    # User can only add books to their own wishlist
    @auth.login_required
    def post(self, id):
        data = self.reqparse.parse_args()

        user = UserModel.query.get_or_404(id)

        try:
            pub_date = datetime.strptime(data['pub_date'], '%Y-%m-%d')
        except:
            return {"message": "Publication date (pub_date) must be in YYYY-mm-dd format" }, 400

        # Verify that user is adding book to their own wishlist
        if UserModel.query.filter_by(id=id, email=g.user.email).first() is None:
            return { "message": "Users are only allowed to add books to their own wishlist" }, 401

        # If book isn't in database, add it
        book = BookModel.query.filter_by(isbn=data['isbn']).first()            
        if book is None:
            book = BookModel(isbn = data['isbn'], title = data['title'], author = data['author'], pub_date = pub_date)
            book.add_to_db()
        # Ensure book isn't already in wishlist and that the attributes match up
        elif not(book.title == data['title'] and book.author == data['author'] and str(book.pub_date) == data['pub_date']):
            print(book.pub_date)
            print(data['pub_date'])

            return { "message": "Different book with this ISBN already exists" }, 409
        elif book in user.books:
            return { "message": "Book with this ISBN already in user's wishlist" }, 409

        user.books.append(book)
        commit()

        return { 'book': BookModel.serialize(book) }, 201

class UserBook(Resource):
    """
    Resource: books
    Endpoint: /api/users/<id>/books/<isbn>
    Methods: GET, PUT, DELETE
    """

    # Initialize PUT request parser
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = "Title not provided")
        self.reqparse.add_argument('author', type = str, required = True,
            help = "Author not provided")
        self.reqparse.add_argument('pub_date', type = str, required = True,
            help = "Publication date not provided")
        super(UserBook, self).__init__()

    # Return book info for book <isbn> in user <id>'s wishlist
    def get(self, id, isbn):
        user = UserModel.query.get_or_404(id)
        book = BookModel.query.get_or_404(isbn)
        if book not in user.books:
            return { "message": "Book with this ISBN not in user\'s wishlist" }, 404
        return { 'book': BookModel.serialize(book) }

    # Update book info for book <isbn> in user <id>'s wishlist
    # User can only update books in their own wishlist
    @auth.login_required
    def put(self, id, isbn):
        data = self.reqparse.parse_args()

        user = UserModel.query.get_or_404(id)

        if UserModel.query.filter_by(id=id, email=g.user.email).first() is None:
            return { "message": "Users are only allowed to update books in their own wishlist" }, 401

        try:
            pub_date = datetime.strptime(data['pub_date'], '%Y-%m-%d')
        except:
            return { "message": "Publication date (pub_date) must be in YYYY-mm-dd format" }, 400

        # If book isn't in database, add it
        book = BookModel.query.filter_by(isbn=isbn).first()  
        if book is None:
            book = BookModel(isbn = isbn, title = data['title'], author = data['author'], pub_date = pub_date)
            book.add_to_db()
        else:
            book.isbn=isbn
            book.title = data['title']
            book.author = data['author']
            book.pub_date = pub_date

        user.books.append(book)
        commit()

        return { "message": "User\'s book wishlist updated successfully" }

    # Delete book <isbn> from user <id>'s wishlist
    # Users can only delete books from their own wishlist
    @auth.login_required
    def delete(self, id, isbn):
        user = UserModel.query.get_or_404(id)
        book = BookModel.query.get_or_404(isbn)

        if UserModel.query.filter_by(id=id, email=g.user.email).first() is None:
            return { "message": "Users are only allowed to delete books from their own wishlist" }, 401

        if book not in user.books:
            return { "message": "Book with this ISBN not in user\'s wishlist" }, 404

        user.books.remove(book)
        commit()

        return { "message": "Book deleted from user\'s wishlist successfully" }

class BookUsers(Resource):
    """
    Resource: users
    Endpoint: /api/books/<isbn>/users
    Methods: GET
    """

    # Return list of users with book <isbn> in their wishlist
    def get(self, isbn):
        book = BookModel.query.get_or_404(isbn)

        return { 'users': list(map(lambda x: UserModel.serialize(x), book.users)) }

# Add API resources and corresponding endpoints
api.add_resource(Users, '/users', endpoint = 'users')
api.add_resource(User, '/users/<int:id>', endpoint = 'user')
api.add_resource(Books, '/books', endpoint = 'books')
api.add_resource(Book, '/books/<int:isbn>', endpoint = 'book')
api.add_resource(UserBooks, '/users/<int:id>/books', endpoint = 'user books list')
api.add_resource(UserBook, '/users/<int:id>/books/<int:isbn>', endpoint = 'user book')
api.add_resource(BookUsers, '/books/<isbn>/users', endpoint = 'book users list')