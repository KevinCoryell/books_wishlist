from datetime import datetime
from . import db
import json
from werkzeug.security import generate_password_hash, check_password_hash

# Add user_books association table to keep track of user wishlists
user_books = db.Table('user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('isbn', db.String, db.ForeignKey('books.isbn')), 
    db.PrimaryKeyConstraint('user_id', 'isbn')
)

def commit():
    db.session.commit()

class UserModel(db.Model):
    """
    Users resource database model
    Attributes: id, first_name, last_name, email, password_hash
    """

    __tablename__ = 'users'

    # Define database fields
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Add relationship to books
    books = db.relationship('BookModel', secondary='user_books', backref='users', lazy='subquery')

    # Password security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Add new user to database
    def add_to_db(self):
        db.session.add(self)
    
    def serialize(user):
        return {
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

    def __repr__(self):
        return json.dumps( { 'user_id': self.id, 
                 'first_name': self.first_name, 
                 'last_name': self.last_name, 
                 'email': self.email
                } )

class BookModel(db.Model):
    """
    Books resource database model
    Attributes: isbn, title, author, pub_date
    """

    __tablename__ = 'books'

    # Define database fields
    isbn = db.Column(db.String(16), primary_key=True)
    title = db.Column(db.String(140))
    author = db.Column(db.String(128), index=True)
    pub_date = db.Column(db.Date)

    # Add new book from database
    def add_to_db(self):
        db.session.add(self)

    def serialize(book):
        return {
            'isbn': book.isbn,
            'title': book.title,
            'author': book.author,
            'pub_date': datetime.strftime(book.pub_date, '%Y-%m-%d')
        }

    def __repr__(self):
        return json.dumps( {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'pub_date': datetime.strftime(self.pub_date, '%Y-%m-%d')
        } )