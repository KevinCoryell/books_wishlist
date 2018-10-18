# books_wishlist
Restful API for managing user books wishlists  
Project description can be viewed in `doc/description.pdf`

* **Deployment Instructions**
	1.  Download or clone project to server with Python 3 and pip installed
	* If downloading a zip file, unzip it before proceeding
	* Ensure files and directory structure match the repo
	2.  Create virtual environment in books_wishlist top-level directory
	`python3 -m venv venv`
	3.  Activate virtual environment
	`source venv/bin/activate`
	4.  Install Flask and other required packages
	`pip install -r requirements.txt`
	5.  Configure Flask environment settings
	`source .flaskenv`
	* Alternatively, run `export FLASK_ENV=development`, `export FLASK_DEBUG=false` and `export FLASK_APP=books_wishlist.py`
	6.  Startup the application
	`flask run`
	* The default port is 5000, but this can be changed
	7.  Interact with the API using any REST client, curl, etc.
	* E.g., running `curl http://localhost:5000/api/users` will return the (initially empty) list of users
	8.  The database is created and managed by the app in a `database.db` file

Full endpoint usage documentation is contained in `doc/endpoints.md`

* **Testing Instructions**
	1.  Follow deployment instructions through environment configuration
	2.  Edit `config.py` file and set `TESTING = True`
	* This will allow a temporary database to be setup for testing
	3.  Run test script
	`python test.py`
	4.  Results will display on the terminal after all tests have been run  

Please note that this is a simple app not intended for primetime

