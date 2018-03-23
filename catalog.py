from flask import (Flask,
                   abort,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   jsonify,
                   session as login_session,
                   make_response)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, User, Base

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json').read())['web']['client_id']

# Create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON Endpoints

# API to show details of all the items present in the database
@app.route('/api/v1/catalog.json/')
def catalog_json():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])


# API to show details of all the items of a particular category
@app.route('/api/v1/category/<string:category>/JSON/')
def items_json(category):
    items = session.query(Item).filter_by(category_name=category).all()
    return jsonify(Items=[i.serialize for i in items])


# API to show details of a particular item
@app.route('/api/v1/category/<string:category>/item/<string:item>/JSON/')
def item_json(category, item):
    item = session.query(Item).filter_by(category_name=category,
                                         name=item).one()
    return jsonify(Item=item.serialize)


# API to show all categories present in the database
@app.route('/api/v1/catalog/categories/JSON/')
def categories_json():
    categories = session.query(Category).all()
    return jsonify(Categories=[c.serialize for c in categories])


# Login Page
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    page = 'login'
    return render_template('login.html', page=page, STATE=state)


# GConnect Server
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if the user is alredy logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already\
                                             connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Already, logged in as %s" % login_session['username'])
        return response

    # Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists in the database, if it doesn't register the user
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px;border-radius: 50%;\
                           -webkit-border-radius: 150px;\
                           -moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    return output


# GDisconnect Server
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # GET request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
          % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You've been logged out successfully!")
        return redirect(url_for('show_catalog'))
    else:
        response = make_response(json.dumps('''Failed to revoke token for
                                            given user.''', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show all categories and latest items
@app.route('/')
@app.route('/catalog/')
def show_catalog():
    categories = session.query(Category).order_by(Category.name)
    items = []
    for c in categories:
        i = session.query(Item)\
                   .filter_by(category_name=c.name)\
                   .order_by(Item.time.desc()).first()
        if i:
            items.append(i)
    return render_template('catalog.html', categories=categories, items=items,
                           login_session=login_session)


# Show items for a specific category
@app.route('/catalog/<string:category>/')
@app.route('/catalog/<string:category>/items/')
def show_items(category):
    if session.query(Category).filter_by(name=category).one_or_none():
        categories = session.query(Category).order_by(Category.name)
        items = session.query(Item).filter_by(category_name=category).all()
        length = len(items)
        return render_template('items.html', items=items,
                               categories=categories, length=length,
                               category=category, login_session=login_session)

    else:
        abort(404)


# Show description of a specific item
@app.route('/catalog/<string:category>/items/<string:name>/')
@app.route('/catalog/<string:category>/items/<string:name>/desc/')
def show_description(category, name):
    item = session.query(Item)\
                  .filter_by(category_name=category, name=name).one_or_none()
    if item:
        return render_template('description.html', item=item,
                               login_session=login_session)
    else:
        abort(404)


# Add a new category
@app.route('/catalog/new/', methods=['GET', 'POST'])
def add_category():
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    # View the add category page
    if request.method == 'GET':
        title = "Add"
        url = url_for('add_category')
        return render_template('addEditCategory.html', title=title, url=url,
                               login_session=login_session)
    # Handle the form submit
    if request.method == 'POST':
        # Check if the category already exists
        if session.query(Category)\
                  .filter_by(name=request.form['name']).one_or_none():
            flash('Category already exists!')
            return redirect(url_for('add_category'))
        # Else add it to database
        else:
            category = Category(name=request.form['name'],
                                user_id=login_session['user_id'])
            session.add(category)
            session.commit()
            flash('A category has been created!')
            return redirect(url_for('show_catalog'))


# Edit an existing category
@app.route('/catalog/<string:category>/edit/', methods=['GET', 'POST'])
def edit_category(category):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    # Check if the current user is the original creator
    cat = session.query(Category).filter_by(name=category).one_or_none()
    if cat is not None and login_session['user_id'] != cat.user_id:
        flash("You can only edit the category you've created!")
        return redirect(url_for('show_items', category=cat.name))
    # View the edit category page
    if request.method == 'GET' and session.query(Category)\
                                          .filter_by(name=category)\
                                          .one_or_none():
        title = "Edit"
        url = url_for('edit_category', category=category)
        return render_template('addEditCategory.html', title=title,
                               url=url, category=category,
                               login_session=login_session)
    # Return a 404 error if the url doesn't exist
    elif request.method != 'POST':
        abort(404)
    # Handle the form submit
    if request.method == 'POST':
        # Check if the category already exists
        if session.query(Category)\
                  .filter_by(name=request.form['name']).one_or_none():
            if request.form['name'] == category:
                flash('Nothing changed! Please make some changes!')
                return redirect(url_for('edit_category', category=category))
            else:
                flash('Category already exists!')
                return redirect(url_for('edit_category', category=category))
        # Else edit the category
        else:
            c = session.query(Category).filter_by(name=category).one()
            items = session.query(Item).filter_by(category_name=c.name).all()
            c.name = request.form['name']
            session.add(c)
            session.commit()
            for i in items:
                i.category_name = request.form['name']
                session.add(i)
                session.commit()
            flash('A category has been edited!')
            return redirect(url_for('show_catalog'))


# Delete an existing category
@app.route('/catalog/<string:category>/delete/', methods=['GET', 'POST'])
def delete_category(category):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    # Check if the current user is the original creator
    cat = session.query(Category).filter_by(name=category).one_or_none()
    if cat is not None and login_session['user_id'] != cat.user_id:
        flash("You can only delete the category you've created!")
        return redirect(url_for('show_items', category=cat.name))
    # View the delete category page
    if request.method == 'GET' and session.query(Category)\
                                          .filter_by(name=category)\
                                          .one_or_none():
        return render_template('deleteCategory.html', category=category,
                               login_session=login_session)
    # Return a 404 error if the url doesn't exist
    elif request.method != 'POST':
        abort(404)
    # Handle the form submit
    if request.method == 'POST':
        # Delete the category from the database
        c = session.query(Category).filter_by(name=category).one()
        session.delete(c)
        session.commit()
        # Delete all the items of that category
        session.query(Item).filter_by(category_name=category).delete()
        session.commit()
        flash('A category has been deleted!')
        return redirect(url_for('show_catalog'))


# Add a new item
@app.route('/catalog/<string:category>/items/new/', methods=['GET', 'POST'])
def add_item(category):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    # View the add item page
    if request.method == 'GET' and session.query(Category)\
                                          .filter_by(name=category)\
                                          .one_or_none():
        title = "Add"
        url = url_for('add_item', category=category)
        return render_template('addEditItem.html', title=title, url=url,
                               category=category, login_session=login_session)
    # Return a 404 error if the url doesn't exist
    elif request.method != 'POST':
        abort(404)
    # Handle the form submit
    if request.method == 'POST':
        # Check if the item name already exists for that particular category
        if session.query(Item)\
                  .filter_by(category_name=request.form['category'],
                             name=request.form['name']).one_or_none():
            flash('Item already exists for that category!')
            return redirect(url_for('add_item', category=category))
        # Else add it to the database
        else:
            item = Item(name=request.form['name'],
                        description=request.form['description'],
                        category_name=request.form['category'],
                        user_id=login_session['user_id'])
            session.add(item)
            session.commit()
            flash('An item has been created!')
            return redirect(url_for('show_items', category=item.category_name))


# Edit an existing item
@app.route('/catalog/<string:category>/items/<string:name>/edit/',
           methods=['GET', 'POST'])
def edit_item(category, name):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    # Check if the current user is the original creator
    i = session.query(Item).filter_by(name=name, category_name=category)\
               .one_or_none()
    if i is not None and login_session['user_id'] != i.user_id:
        flash("You can only edit the item you've created!")
        return redirect(url_for('show_description', category=i.category_name,
                                name=name))
    # View the edit item page
    item = session.query(Item).filter_by(category_name=category,
                                         name=name).one_or_none()
    if request.method == "GET" and item:
        title = "Edit"
        url = url_for('edit_item', category=category, name=name)
        categories = session.query(Category).all()
        return render_template('addEditItem.html', title=title, url=url,
                               categories=categories, item=item,
                               login_session=login_session)
    # Return a 404 error if the url doesn't exist
    elif request.method != 'POST':
        abort(404)
    # Handle the form submit
    if request.method == "POST":
        # Check if the item already exists
        if session.query(Item)\
                  .filter_by(category_name=request.form['category'],
                             name=request.form['name']).one_or_none():
            # If we are not making any changes
            if request.form['name'] == name and\
               request.form['category'] == category and\
               request.form['description'] == item.description:
                flash('Nothing changed. Please make some changes!')
                return redirect(url_for('edit_item', category=category,
                                name=name))
            # If we are just changing the description make changes
            elif request.form['name'] == name and\
                    request.form['category'] == category and\
                    request.form['description'] != item.description:
                item.name = request.form['name']
                item.category_name = request.form['category']
                item.description = request.form['description']
                session.add(item)
                session.commit()
                flash('An item has been edited!')
                return redirect(url_for('show_items',
                                category=item.category_name))
            # If the item matches some other item
            else:
                flash('Item already exists for that category!')
                return redirect(url_for('edit_item', category=category,
                                name=name))
        # Else make changes
        else:
            item.name = request.form['name']
            item.category_name = request.form['category']
            item.description = request.form['description']
            session.add(item)
            session.commit()
            flash('An item has been edited!')
            return redirect(url_for('show_items', category=item.category_name))


# Delete an existing item
@app.route('/catalog/<string:category>/items/<string:name>/delete/',
           methods=['GET', 'POST'])
def delete_item(category, name):
    # If user is not logged in redirect to login page
    if 'username' not in login_session:
        return redirect('/login')
    # Check if the current user is the original creator
    i = session.query(Item).filter_by(name=name, category_name=category)\
               .one_or_none()
    if i is not None and login_session['user_id'] != i.user_id:
        flash("You can only delete the item you've created!")
        return redirect(url_for('show_description', category=i.category_name,
                                name=name))
    # View the delete item page
    item = session.query(Item).filter_by(category_name=category,
                                         name=name).one_or_none()
    if request.method == "GET" and item:
        return render_template('deleteItem.html', item=item,
                               login_session=login_session)
    # Return a 404 error if the url doesn't exist
    elif request.method != 'POST':
        abort(404)
    # Handle the form submit
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash('An item has been deleted!')
        return redirect(url_for('show_items', category=item.category_name))


# Create a new user
def create_user(login_session):
    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Get user info
def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Get user id
def get_user_id(email):
    user = session.query(User).filter_by(email=email).one_or_none()
    if user:
        return user.id
    else:
        return None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
