# Food Catalog

## Project Overview

> To Develop an application that provides a list of items with various categories as well as provide a user registration and authentication system. Registered users have the ability to add, update or delete their items. However, the user doesn't need to be logged in in order to view all the categories and it's respective items. Also, this application is user specific i.e. the user who created a category or an item is only the sole person who has the ability to add, edit, or delete it. This application uses third party authentication with Google Sign in.

## Implementation

> Keeping the project statement in mind, I implemented a food catalog application which list out various food categories and its respective food items. Users can view the description of a specific food item of a particular category. Logged in users have the ability to add, edit or delete the categories and items. Moreover, a user can't modify an item or a category he hasn't created itself.

## Things Learnt

* Developing RESTful web application using the Python framework Flask
* Implementing third-party OAuth authentication
* Implementing CRUD operations using SQLAlchemy ORM for python

## Skills Required

* HTML/CSS/Bootstrap
* Javascript/jQuery
* Python/Flask
* Jinja2
* Knowledge of databases
* CRUD with SQLAlchemy ORM
* Google OAuth
* Knowledge of APIs

## Getting Started

### Prerequisites

* Python 2.7
* pip
* virtualenv

### Project Setup

1. Clone this repo
2. Open the folder inside a terminal: `cd Food-Catalog/`
3. Create a virtual environment with `python2` interpreter: `virtualenv --python=/usr/bin/python2 venv`
4. Activate the virtual environment using: `source venv/bin/activate`
5. Then run `pip install -r requirements.txt` to install the dependencies
6. <em>(Optional)</em>
    Setup the database and initialize it with some data by running

    ```
    $ python database_setup.py
    $ python populate_database.py
    ```
7. Start the local web server by running

    ```
    python catalog.py
    ```
8. Access the web application by typing the following url in your web browser

    ```
    http://localhost:5000
    ```

> Note: If you haven't performed Step 8, you need to add the categories and items from within the web application.

## JSON Endpoints

* `/api/v1/catalog.json/` --> Returns JSON of all the items present in the database
* `/api/v1/category/<string:category>/JSON/` --> Returns JSON of all the items of a particular category
* `/api/v1/category/<string:category>/item/<string:item>/JSON/` --> Returns JSON of a particular item of a category
* `/api/v1/catalog/categories/JSON/` --> Returns JSON of all the categories present in the database

## References

* Bootstrap Documentation
* Snackbar/Toast learnt from W3Schools
* .gitignore file made with gitignore.io
* Stack Overflow for debugging errors

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details
