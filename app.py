'''
    Title: TASKED
    Author: Miguel Romo
    Software Testing Project
    Last Update: 09/12/2024 02:25 PM
'''

# LIBRARIES
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import mysql.connector
from mysql.connector import Error
import bcrypt
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os
import secrets
import psycopg2
from psycopg2 import Error
import logging

# Load Environment Variables
load_dotenv()

# Use 'dev' as default environment
environment = os.getenv('FLASK_ENV', 'development')

# Select environment
if environment == 'development':
    # Local Environment Variables (development)
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'task')
else:
    # Render Environment Variables (deployment)
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Flask and OAuth init
app = Flask(__name__) # Init Flask
app.secret_key = 'tas^kedpas!sword?'  # Flash messages
app.logger.setLevel(logging.DEBUG)

app.logger.debug(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID')}")
app.logger.debug(f"GOOGLE_CLIENT_SECRET: {os.getenv('GOOGLE_CLIENT_SECRET')}")

# Recovery Google data from environment variables
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = os.getenv('GOOGLE_DISCOVERY_URL')
PEOPLE_API_SCOPE = os.getenv('PEOPLE_API_SCOPE')

# Init OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID, # Google Client ID
    client_secret=GOOGLE_CLIENT_SECRET, # Google Client Secret
    server_metadata_url=GOOGLE_DISCOVERY_URL,  # Discovery Endpoint
    client_kwargs={
        'scope': 'openid profile email'  # Access to user profile and email
    }
)

# MongoDB connection
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/todolist")
mongo = PyMongo(app)

# SQL connection (PostgreSQL)
def create_connection():
    connection = None
    try:
        # Use DATABASE_URL for PostgreSQL in deployment
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            connection = psycopg2.connect(database_url, sslmode='require')
        else:
            # If don't find DATABASE_URL, try local environment variables
            connection = psycopg2.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                sslmode='require'  # SSL for secure Render connections
            )
    except Error as e:
        print(f"Error connecting the database: {e}")
    
    return connection

# Hash functions for passwrds
def gen_hash(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_hash(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# App routes and logic
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Pick data from html form
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        hashed_pwd = gen_hash(password) # Hash password
        
        connection = create_connection() # DB connection

        # Push user login data into DB
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO users (username, email, password_hash, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (username, email, hashed_pwd, first_name, last_name))
                connection.commit()
                return redirect(url_for('login'))
            except Error as e:
                flash(f'Sign in error: {e}', 'danger')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Unable to connect to database', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Pick data from html form
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = create_connection()

        # Check user email and password
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "SELECT password_hash, username FROM users WHERE email=%s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                if result:
                    stored_hash = result[0]
                    if check_hash(password, stored_hash):
                        return redirect(url_for('home', username=result[1]))
                    else:
                        flash('Wrong Username or Password', 'danger')
                else:
                    flash('User not found', 'danger')

            except Error as e:
                flash(f'Login error: {e}', 'danger')
            finally:
                cursor.close()
                connection.close()
        else:
            flash('Unable to connect to database', 'danger')

    return render_template('login.html')

@app.route('/login/google') # Login using Google OAuth
def login_google():
    # Generate a random nonce
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce  # Save nonce in session

    # Redirect Google for auth
    redirect_uri = url_for('auth_callback', _external=True)
    print(f"Redirect URI: {redirect_uri}")  # Verify generated URL
    return google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/login/callback')
def auth_callback():
    # Recovery session nonce
    nonce = session.pop('nonce', None)

    try:
        # Obtain Google access token
        token = google.authorize_access_token()
        print("Received access token:", token)  # Print the received token

        # Parse ID token with nonce
        user = google.parse_id_token(token, nonce=nonce)
        if user is None:
            raise ValueError("ID token is None")
        
        print("User profile:", user)  # Print user profile

    except Exception as e:
        flash(f"Error obtaining user profile: {e}", "danger")
        return redirect(url_for('login'))

    # Database connection
    connection = create_connection()
    cursor = connection.cursor()

    # Check if the user exists
    cursor.execute("SELECT username FROM users WHERE email=%s", (user['email'],))
    result = cursor.fetchone()

    if result:
        username = result[0]
    else:
        # If user doesn't exist, create 
        username = user['given_name']  # Use the Google given name
        hashed_pwd = gen_hash('defaultpassword')  # Temp password

        cursor.execute(
            "INSERT INTO users (username, email, password_hash, first_name, last_name) "
            "VALUES (%s, %s, %s, %s, %s)",
            (username, user['email'], hashed_pwd, user['given_name'], user['family_name'])
        )
        connection.commit()

    cursor.close()
    connection.close()

    # Store username in session
    session['username'] = username

    # Redirect user to home page with username
    return redirect(url_for('home', username=username))

@app.route('/home/<username>')
def home(username):
    # Obtain username in session
    if 'username' in session:
        username = session['username']
    tasks = mongo.db.tasks.find({"username": username}) # Tasks that user created
    return render_template('home.html', tasks=tasks, username=username)

@app.route('/add/<username>', methods=['POST'])
def add_task(username):
    # Data from form
    title = request.form.get('title')
    priority = request.form.get('priority')

    # Insert in MongoDB new task
    if title:
        mongo.db.tasks.insert_one({
            'title': title,
            'priority': priority,
            'username': username,
            'completed': False
        })

    tasks = mongo.db.tasks.find({"username": username})
    return render_template('home.html', tasks=tasks, username=username) # Render home again, will show the new task too

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_task(id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_priority = request.form.get('priority')
        mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {'title': new_title, 'priority': new_priority}})
        return redirect(url_for('home', username=task['username']))
    return render_template('edit.html', task=task)

@app.route('/update-completion/<id>', methods=['POST'])
def update_completion(id):
    data = request.get_json()
    is_completed = data.get('completed')
    if is_completed is not None:
        mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {'completed': is_completed}})
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/delete/<id>')
def delete_task(id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    if task:
        mongo.db.tasks.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('home', username=task['username']))
    return redirect(url_for('home', username='default'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Delete username of session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))