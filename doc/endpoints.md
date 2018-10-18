Books Wishlist API Endpoint Documentation
----
  Fetch a list of all users or add a new user to the database

* **URL:**
  api/users
* **Method:**
  `GET` | `POST` 
* **Data Params**  
  `{"first_name": "first name", "last_name": "last name", "email": "email_address@host", "password": "password"}`

* **Success Response:**  
  `GET`  
  **Code:** 200  
  **Content:**
  `{"users": [ {"user_id": 1, "first_name": "first name", "last_name": "last name", "email": "email_address@host", "password": "password"}, .... ] }`  
  
  `POST`  
  **Code:** 201  
  **Content:**
  `{"user": {"user_id": 1, first_name": "first name", "last_name": "last name", "email": "email_address@host", "password": "password"} }`
 
* **Error Response:**  
  `POST`  
  **Code:** 409 CONFLICT  
  **Content:**
  `{ "message": "User with this email already exists" }`

* **Sample Call:**  
  `GET`: `curl /api/users`  
  `POST`: `curl -X POST -H "Content-Type: application/json" -d '{"first_name": "first name", "last_name": "last name", "email": "email_address@host", "password": "password"}' /api/users`

----
  Fetch a list of all books or add a new book to the library

* **URL:**
  api/books
* **Method:**
  `GET` | `POST` 
* **Data Params**  
  `{"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"}`

* **Success Response:**  
  `GET`  
  **Code:** 200  
  **Content:**
  `{"books": [ {"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"}, .... ] }`  
  
  `POST`  
  **Code:** 201  
  **Content:**
  `{"book": {"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"} }`
 
* **Error Response:**  
  `POST`  
  **Code:** 400 BAD REQUEST  
  **Content:**
  `{ "message": "Publication date (pub_date) must be in YYYY-mm-dd format" }`  
  or  
  **Code:** 409 CONFLICT  
  **Content:**
  `{ "message": "Book with this ISBN already exists" }`

* **Sample Call:**  
  `GET`: `curl /api/books`  
  `POST`: `curl -X POST -H "Content-Type: application/json" -d '{"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "pub_date": "1954-07-29", "isbn": "9789655171990"}' /api/users/1/books`

----
  Fetch a user's book wishlist or add a book to a user's wishlist

* **URL:**
  api/users/:id/books
* **Method:**
  `GET` | `POST` 
* **Data Params**  
  `{"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"}`
*  **URL Params**
   **Required:**
   `id=[integer]`
* **Auth**  
  To add to a user's wishlist, HTTP Basic authentication using the email and password of the user whose wishlist is beind added to is required.  
  Users are not authorized to add books to another user's wishlist.   
  No auth is required to fetch a user's book wishlist.  
* **Success Response:**  
  `GET`  
  **Code:** 200  
  **Content:**
  `{"books": [ {"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"}, .... ] }`  
  
  `POST`  
  **Code:** 201  
  **Content:**
  `{"book": {"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"} }`
 
* **Error Response:**  
  `POST`  
  **Code:** 400 BAD REQUEST  
  **Content:**
  `{ "message": "Publication date (pub_date) must be in YYYY-mm-dd format" }`  
  or  
  **Code:** 401 UNAUTHORIZED  
  **Content:**
  `Unauthorized Access`  
  or  
  **Code:** 409 CONFLICT  
  **Content:**
  `{ "message": "Book with this ISBN already in user's wishlist" }` or `{ "message": "Different book with this ISBN already exists" }`
* **Sample Call:**  
  `GET`: `curl /api/users/1/books`  
  `POST`: `curl -u email_address@host:password -X POST -H "Content-Type: application/json" -d '{"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "pub_date": "1954-07-29", "isbn": "9789655171990"}' /api/users/1/books`

----
  Update/create a book in a user's wishlist, delete a book from a user's wishlist, or fetch a book from a user's wishlist

* **URL:**
  api/users/:id/books/:isbn
* **Method:**
  `GET` | `PUT` | `DELETE` 
* **Data Params**  
  `{"title": "title", "author": "author", "pub_date": "YYYY-mm-dd"}`
*  **URL Params**
   **Required:**
   `id=[integer]`
   `isbn=[string]`
* **Auth**  
  To update or delete a book in a user's wishlist, HTTP Basic authentication using the email and password of the user whose wishlist is being updated is required.  
  Users are not authorized to update or delete a book from another user's wishlist.  
  No auth is required to fetch a book from a user's wishlist.  
* **Success Response:**  
  `GET`  
  **Code:** 200  
  **Content:**
  `{"book": {"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"} }`  
  
  `PUT`  
  **Code:** 200  
  **Content:**
  `{ "message": "User's book wishlist updated successfully" }`

  `DELETE`  
  **Code:** 200  
  **Content:**
  `{ "message": "Book deleted from user's wishlist successfully" }`
 
* **Error Response:**  
  `PUT`  
  **Code:** 400 BAD REQUEST  
  **Content:**
  `{ "message": "Publication date (pub_date) must be in YYYY-mm-dd format" }`  
  or  
  **Code:** 401 UNAUTHORIZED  
  **Content:**
  `Unauthorized Access` or `{ "message": "Users are only allowed to update books in their own wishlist" }`  
  
  `DELETE`  
  **Code:** 401 UNAUTHORIZED  
  **Content:**
  `Unauthorized Access` or `{ "message": "Users are only allowed to delete books from their own wishlist" }`  
  or  
  **Code:** 404 NOT FOUND  
  **Content:**
  `{ "message": "Book with this ISBN not in user's wishlist" }`
* **Sample Call:**  
  `GET`: `curl /api/users/1/books/9789655171990`  
  `PUT`: `curl -u email_address@host:password -X PUT -H "Content-Type: application/json" -d '{"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "pub_date": "1954-07-29"}' /api/users/1/books/9789655171990`  
  `DELETE`: `curl -u email_address@host:password -X DELETE /api/users/1/books/9789655171990`

----
  Fetch a single user from the database

* **URL:**
  api/users/:id
* **Method:**
  `GET`
*  **URL Params**
   **Required:**
   `id=[integer]`
* **Success Response:**  
  `GET`  
  **Code:** 200  
  **Content:**
  `{"user": {"user_id": 1, "first_name": "first name", "last_name": "last name", "email": "email_address@host", "password": "password"} }`  
* **Sample Call:**  
  `GET`: `curl /api/users/1` 

----
  Fetch a single book from the database

* **URL:**
  api/books/:isbn
* **Method:**
  `GET`
*  **URL Params**
   **Required:**
   `isbn=[string]`
* **Success Response:**  
  `GET`  
  **Code:** 200  
  **Content:**
  `{"book": {"title": "title", "author": "author", "pub_date": "YYYY-mm-dd", "isbn": "ISBN"} }`  
* **Sample Call:**  
  `GET`: `curl /api/books/9789655171990`

----
  Fetch a list of users who have a particular book on their wishlist

* **URL:**
  api/books/:isbn/users
* **Method:**
  `GET` 
* **Success Response:**  
  GET  
  **Code:** 200  
  **Content:**
  `{"users": [ {"user_id": 1, "first_name": "first name", "last_name": "last name", "email": "email_address@host", "password": "password"}, .... ] }`  
* **Sample Call:**  
  `GET`: `curl /api/books/9789655171990/users` 

