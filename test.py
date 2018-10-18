import unittest
import os
import json
from base64 import b64encode
from api import app, db
from flask_sqlalchemy import SQLAlchemy

class BooksWishlistTestCase(unittest.TestCase):
    """
    Test all endpoints in API using temporary database
    """

    # Create test client, database and data structures
    def setUp(self):

        self.client = app.test_client

        with app.app_context():
            db.create_all()

        self.user_one = {
            "first_name": "foo",
            "last_name": "bar",
            "email": "foobar@gmail.com",
            "password": "foobar"
            }

        self.user_two = {
            "first_name": "bar",
            "last_name": "foo",
            "email": "barfoo@gmail.com",
            "password": "barfoo"
            }

        self.first_book = {
            "title": "test book one",
            "author": "test client",
            "pub_date": "2018-10-16",
            "isbn": "12345678912345"
            }

        self.second_book = {
            "title": "test book two",
            "author": "test client",
            "pub_date": "2018-10-16",
            "isbn": "89124"
            }

        self.third_book = {
            "title": "test book three",
            "author": "test client and more",
            "pub_date": "2018-10-16",
            "isbn": "123456789125"
            }

    # Test /api/users
    def test_users(self):
        # Add user and verify response
        post_response = self.client().post('/api/users', data=self.user_one)
        self.assertEqual(post_response.status_code, 201)
        self.assertIn('user_id', str(post_response.data))
        self.assertIn(self.user_one['email'], str(post_response.data))
        self.assertIn(self.user_one['first_name'], str(post_response.data))
        self.assertIn(self.user_one['last_name'], str(post_response.data))

        # Verify user is in list returned from GET
        get_response = self.client().get('/api/users')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(self.user_one['email'], str(get_response.data))
        self.assertIn(self.user_one['first_name'], str(get_response.data))
        self.assertIn(self.user_one['last_name'], str(get_response.data))

    # Test /api/user/<id>
    def test_user(self):
        # Add user, verify response and parse user ID
        user_post_response = self.client().post('/api/users', data=self.user_one)
        self.assertEqual(user_post_response.status_code, 201)
        user_post_response_json = json.loads(user_post_response.data)['user']
        user_one_id = str(user_post_response_json['user_id'])

        # Verify user info returned from GET
        get_response = self.client().get('/api/users/' + user_one_id)
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(self.user_one['email'], str(get_response.data))
        self.assertIn(self.user_one['first_name'], str(get_response.data))
        self.assertIn(self.user_one['last_name'], str(get_response.data))    

    # Test /api/books
    def test_books(self):
        # Add books and verify responses
        post_response = self.client().post('/api/books', data=self.first_book)
        self.assertEqual(post_response.status_code, 201)
        self.assertIn(self.first_book['isbn'], str(post_response.data))
        self.assertIn(self.first_book['title'], str(post_response.data))
        self.assertIn(self.first_book['author'], str(post_response.data))
        self.assertIn(self.first_book['pub_date'], str(post_response.data))

        post_response_two = self.client().post('/api/books', data=self.second_book)
        self.assertEqual(post_response_two.status_code, 201)

        # Verify books are in list returned from GET
        get_response = self.client().get('/api/books')
        self.assertEqual(get_response.status_code, 200)

        self.assertIn(self.first_book['isbn'], str(get_response.data))
        self.assertIn(self.first_book['title'], str(get_response.data))
        self.assertIn(self.first_book['author'], str(get_response.data))
        self.assertIn(self.first_book['pub_date'], str(get_response.data))

        self.assertIn(self.second_book['isbn'], str(get_response.data))
        self.assertIn(self.second_book['title'], str(get_response.data))
        self.assertIn(self.second_book['author'], str(get_response.data))
        self.assertIn(self.second_book['pub_date'], str(get_response.data))

    # Test /api/books/<isbn>
    def test_book(self):
        # Add book and verify response
        post_response = self.client().post('/api/books', data=self.first_book)
        self.assertEqual(post_response.status_code, 201)

        # Verify book info returned from GET
        endpoint = '/api/books/' + self.first_book['isbn']
        get_response = self.client().get(endpoint)
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(self.first_book['isbn'], str(get_response.data))
        self.assertIn(self.first_book['title'], str(get_response.data))
        self.assertIn(self.first_book['author'], str(get_response.data))
        self.assertIn(self.first_book['pub_date'], str(get_response.data))

    # Test /api/users/<id>/books
    def test_user_books(self):
        # Add user, verify response and parse user ID
        user_post_response = self.client().post('/api/users', data=self.user_two)
        self.assertEqual(user_post_response.status_code, 201)
        user_post_response_json = json.loads(user_post_response.data)['user']
        user_two_id = str(user_post_response_json['user_id'])

        # Configure auth
        auth_creds = self.user_two['email'] + ':' + self.user_two['password']
        headers = {
            'Authorization': 'Basic ' + b64encode(auth_creds.encode('UTF-8')).decode('ascii')
        }

        # Add book to user_two's wishlist and verify books list returned from GET
        endpoint = '/api/users/' + user_two_id + '/books'
        post_response = self.client().post(endpoint, data=self.second_book, headers=headers)
        self.assertEqual(post_response.status_code, 201)
        self.assertIn(self.second_book['isbn'], str(post_response.data))

        get_response = self.client().get(endpoint)
        self.assertEqual(get_response.status_code, 200)

        self.assertIn(self.second_book['isbn'], str(get_response.data))
        self.assertIn(self.second_book['title'], str(get_response.data))
        self.assertIn(self.second_book['author'], str(get_response.data))
        self.assertIn(self.second_book['pub_date'], str(get_response.data))

    # Test /api/users/<id>/books/<isbn>
    def test_user_book(self):
        # Add user, verify response, parse user ID, configure auth
        user_post_response = self.client().post('/api/users', data=self.user_two)
        self.assertEqual(user_post_response.status_code, 201)
        user_post_response_json = json.loads(user_post_response.data)['user']
        user_two_id = str(user_post_response_json['user_id'])
        auth_creds = self.user_two['email'] + ':' + self.user_two['password']
        headers = {
            'Authorization': 'Basic ' + b64encode(auth_creds.encode('UTF-8')).decode('ascii')
        }

        # Add book to user_two's wishlist and verify response
        endpoint = '/api/users/' + user_two_id + '/books'
        post_response = self.client().post(endpoint, data=self.second_book, headers=headers)
        self.assertEqual(post_response.status_code, 201)
        self.assertIn(self.second_book['isbn'], str(post_response.data))

        # Verify book info returned from GET
        endpoint = '/api/users/' + user_two_id + '/books/' + self.second_book['isbn']
        get_response = self.client().get(endpoint)
        self.assertEqual(get_response.status_code, 200)

        self.assertIn(self.second_book['isbn'], str(get_response.data))
        self.assertIn(self.second_book['title'], str(get_response.data))
        self.assertIn(self.second_book['author'], str(get_response.data))
        self.assertIn(self.second_book['pub_date'], str(get_response.data))

        # Update book and verify response
        book_update = {'title': 'updated', 'pub_date': '2018-10-10', 'author': 'updated'}
        put_response = self.client().put(endpoint, data=book_update, headers=headers)
        self.assertEqual(put_response.status_code, 200)

        # Delete book and verify response
        delete_response = self.client().delete(endpoint, headers=headers)
        self.assertEqual(delete_response.status_code, 200)

    # Test /api/books/<isbn>/users
    def test_book_users(self):
        # Add users and verify responses
        response = self.client().post('/api/users', data=self.user_one)
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/users', data=self.user_two)
        self.assertEqual(response.status_code, 201)
        response = self.client().post('/api/books', data=self.first_book)
        self.assertEqual(response.status_code, 201)

        # Add book to user_one's wishlist and verify response
        auth_creds = self.user_one['email'] + ':' + self.user_one['password']
        headers = {
            'Authorization': 'Basic ' + b64encode(auth_creds.encode('UTF-8')).decode('ascii')
        }
        response = self.client().post('/api/users/1/books', data=self.first_book, headers=headers)
        self.assertEqual(response.status_code, 201)

        # Add book to user_two's wishlist and verify response
        auth_creds = self.user_two['email'] + ':' + self.user_two['password']
        headers = {
            'Authorization': 'Basic ' + b64encode(auth_creds.encode('UTF-8')).decode('ascii')
        }
        response = self.client().post('/api/users/2/books', data=self.first_book, headers=headers)
        self.assertEqual(response.status_code, 201)

        # Verify users list returned from GET
        endpoint = 'api/books/' + self.first_book['isbn'] + '/users'
        response = self.client().get(endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_one['email'], str(response.data))
        self.assertIn(self.user_two['email'], str(response.data))

    # Test user attempting to update another user's wishlist
    def test_unauthorized_access(self):
        # Add user, verify response and parse user ID
        user_post_response = self.client().post('/api/users', data=self.user_two)
        self.assertEqual(user_post_response.status_code, 201)
        user_post_response_json = json.loads(user_post_response.data)['user']
        user_two_id = str(user_post_response_json['user_id'])

        # Configure auth to use a different user's creds
        auth_creds = self.user_one['email'] + ':' + self.user_one['password']
        headers = {
            'Authorization': 'Basic ' + b64encode(auth_creds.encode('UTF-8')).decode('ascii')
        }

        # Attempt to add a book to user_one's wishlist, verify 401 (unauthorized) is returned
        endpoint = '/api/users/' + user_two_id + '/books'
        post_response = self.client().post(endpoint, data=self.second_book, headers=headers)
        self.assertEqual(post_response.status_code, 401)

    # Delete temporary database
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            os.unlink(app.config['DATABASE'])

if __name__ == "__main__":
    unittest.main()