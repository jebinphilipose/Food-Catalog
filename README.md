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
* Vagrant
* Virtual Box
* FSND Vagrantfile

### Project Setup

1. Install [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. Download this [fsnd-virtual-machine](https://d17h27t6h515a5.cloudfront.net/topher/2017/May/59125904_fsnd-virtual-machine/fsnd-virtual-machine.zip) file
3. Extract the zip file and clone this repo inside **vagrant/catalog/** directory
4. After that open up a terminal inside the **vagrant/** directory and enter the command `vagrant up`. It will start downloading the necessary files
5. Then enter, `vagrant ssh` to login to the virtual machine
6. After that, enter `cd /vagrant/` and then `sudo pip install -r requirements.txt` to install the dependencies
7. Change your location to **/vagrant/catalog/[PROJECT_FOLDER]/** directory which you have previously cloned
8. <em>(Optional)</em>
    Setup the database and initialize it with some data

    ```
    $ python database_setup.py
    $ python populate_database.py
    ```
9. Start the local web server

    ```
    python catalog.py
    ```
10. Access the web application by typing the following url in your web browser

    ```
    http://localhost:5000
    ```

> Note: If you haven't performed Step 8, you need to add the categories and items from within the web application.

## JSON Endpoints

* `/api/v1/catalog.json/` --> Returns JSON of all the items present in the database
* `/api/v1/category/<string:category>/JSON/` --> Returns JSON of all the items of a particular category
* `/api/v1/category/<string:category>/item/<string:item>/JSON/` --> Returns JSON of a particular item of a category
* `/api/v1/catalog/categories/JSON/` --> Returns JSON of all the categories present in the database

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details