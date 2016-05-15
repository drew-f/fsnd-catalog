from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import make_response
import requests
import json
app = Flask(__name__)
app.secret_key = 'the_secret_key'

# Imports for database usage
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from dbsetup import Base, User, Category, Book

# Imports for sessions
from flask import session
import random, string

# Imports for Google auth
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

# Load Google CLIENT_ID for app
CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

# Create database session
engine = create_engine('postgresql://catalog:cat123@127.0.0.1/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=True)
db = DBSession()

# Functions for interacting with users in database
def get_user_id(email):
    try:
        user = db.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def get_user_info(user_id):
    user = db.query(User).filter_by(id=user_id).one()
    return user

def create_user(session):
    new_user = User(name = session['username'],
                    email = session['email'],
                    picture = session['picture'])
    db.add(new_user)
    db.commit()
    return new_user.id

@app.route('/login/')
def show_login():
    # Create anti-forgery token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/connect', methods=['POST'])
def connect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid State'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain auth code from user session
    code = request.data
    # Use the one time code to obtain credentials
    try:
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to get credentials.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=%s'
           % access_token)
    token = requests.get(url).json()
    # Abort if error in access token
    if token.get('error') is not None:
        response = make_response(json.dumps(token.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that token is for this app, otherwise abort
    if token['aud'] != CLIENT_ID:
        response = make_response(json.dumps("Token is not valid for this app."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that token is for correct user, otherwise abort
    if token['sub'] != credentials.id_token['sub']:
        response = make_response(json.dumps("Token is not valid for this user."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is already connected / authorised
    if session.get('credentials') is not None and credentials.id_token['sub'] == session.get('google_id'):
        response = make_response(json.dumps("User is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in session
    session['credentials'] = credentials.access_token
    session['google_id'] = credentials.id_token['sub']

    # Get user info from Google APIs
    user_data = requests.get("https://www.googleapis.com/oauth2/v3/userinfo",
                            params = {'access_token': credentials.access_token,
                             'alt': 'json'}).json()

    # Store user data in session
    session['username'] = user_data['name']
    session['picture'] = user_data['picture']
    session['email'] = user_data['email']

    # Create the user if it doesn't already exist
    user_id = get_user_id(session['email'])
    if user_id is None:
        user_id = create_user(session)
    session['user_id'] = user_id

    flash("Logged in as: %s" % session['username'])

    response = make_response(json.dumps("Logged in as: %s" % session['username']), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/disconnect', methods=['POST'])
def disconnect():
    if session:
        credentials = session.get('credentials')
    else:
        credentials = None

    # Check if user is logged in
    if credentials is None:
        response = make_response(json.dumps("Current user not connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke token for logged in user
    access_token = credentials
    revoke_token = requests.get("https://accounts.google.com/o/oauth2/revoke",
                                params = {'token': access_token})
    if revoke_token.status_code == 200:
        # Reset the session
        session.clear()
        response = make_response(json.dumps("User disconnected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # Response is somehow invalid
        response = make_response(json.dumps("Failed to revoke token."), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

# Json API to view categories, books in category, and book details
@app.route('/categories/JSON')
def categories_json():
    categories = db.query(Category).all()
    return jsonify(Categories = [cat.serialize for cat in categories])

@app.route('/categories/<int:category_id>/JSON')
def category_json(category_id):
    category = db.query(Category).filter_by(id=category_id).one()
    books = db.query(Book).filter_by(category_id=category_id).all()
    return jsonify(Books = [book.serialize for book in books])

@app.route('/book/<int:book_id>/JSON')
def book_json(book_id):
    book = db.query(Book).filter_by(id=book_id).one()
    return jsonify(Book = book.serialize)

# Show all categories
@app.route('/')
@app.route('/categories/')
def show_categories():
    categories = db.query(Category).order_by(asc(Category.name)).all()
    return render_template('show_categories.html', categories=categories)

# Display list of books in specified category
@app.route('/categories/<int:category_id>/')
def show_category(category_id):
    category = db.query(Category).filter_by(id=category_id).one()
    books = db.query(Book).filter_by(category_id=category_id).all()
    return render_template('show_category.html', category=category, books=books)

# Add a new category
@app.route('/categories/new/', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        if session['user_id'] is not None:
            category = Category(name=request.form['name'])
            db.add(category)
            db.commit()
            flash('Created category: %s' % category.name)
        else:
            flash('You must be logged in to create a category.')
        return redirect(url_for('show_category', category_id=category.id))
    else:
        return render_template('new_category.html')

# Edit details of specified category
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
    category = db.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if session['user_id'] is not None:
            if request.form['name']:
                category.name = request.form['name']
                db.add(category)
                db.commit()
                flash('Edited category: %s' % category.name)
            else:
                flash("Category name cannot be empty.")
        else:
            flash('You must be logged in to edit a category.')
        return redirect(url_for('show_category', category_id=category_id))
    else:
        return render_template('edit_category.html', category=category)

# Delete category
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    category = db.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        # Check to see if category is empty - do not delete if not empty
        books = db.query(Book).filter_by(category_id=category_id).all()
        if not books and session['user_id'] is not None:
            db.delete(category)
            flash('Deleted category: %s' % category.name)
            db.commit()
        else:
            flash("Couldn't delete category %s. Category must be empty."
                  % category.name)
        return redirect(url_for('show_categories'))
    else:
        return render_template('delete_category.html', category=category)

# Display details of specified book
@app.route('/book/<int:book_id>/')
def show_book(book_id):
    book = db.query(Book).filter_by(id=book_id).one()
    return render_template('show_book.html', book=book)

# Add a new book
@app.route('/category/<int:category_id>/newbook/', methods=['GET', 'POST'])
def new_book(category_id):
    if request.method == 'POST':
        if session['user_id'] is not None:
            new_book = Book(title=request.form['title'],
                            author=request.form['author'],
                            isbn=request.form['isbn'],
                            image=request.form['image'],
                            description=request.form['description'],
                            owner_id=session['user_id'],
                            category_id=category_id)
            db.add(new_book)
            db.commit()
            flash('Added new book: %s' % new_book.title)
        else:
            flash("Must be logged in to add a book.")
        return redirect(url_for('show_category',
                                    category_id=category_id))
    else:
        category = db.query(Category).filter_by(id=category_id).one()
        return render_template('new_book.html', category=category)

# Edit specified book
@app.route('/book/<int:book_id>/edit/', methods=['GET', 'POST'])
def edit_book(book_id):
    book = db.query(Book).filter_by(id = book_id).one()
    if request.method == 'POST':
        if session['user_id'] == book.owner_id:
            if request.form['title']:
                book.title = request.form['title']
            book.author = request.form['author']
            book.isbn = request.form['isbn']
            book.image = request.form['image']
            book.description = request.form['description']
            db.add(book)
            db.commit()
            flash('Edited book details: %s' % book.title)
        else:
            flash("You must be the owner of the book to edit.")
        return redirect(url_for('show_book', book_id=book_id))
    else:
        return render_template('edit_book.html', book=book)

# Delete specified book
@app.route('/book/<int:book_id>/delete/', methods=['GET', 'POST'])
def delete_book(book_id):
    book = db.query(Book).filter_by(id=book_id).one()
    category_id = book.category_id
    if request.method == 'POST':
        if session['user_id'] == book.owner_id:
            db.delete(book)
            flash('Deleted book: %s' % book.title)
            db.commit()
        else:
            flash("You must be the owner of the book to delete.")
        return redirect(url_for('show_category', category_id=category_id))
    else:
        return render_template('delete_book.html', book=book)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'the_secret_key' # Change to secure password for production
    app.run(host='0.0.0.0',port=5000)
