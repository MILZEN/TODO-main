from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from authlib.integrations.flask_client import OAuth
from app import mongo, google
from psycopg2 import Error
import secrets
from app.utils import create_connection, gen_hash, check_hash

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
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

@bp.route('/login', methods=['GET', 'POST'])
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

@bp.route('/login/google') # Login using Google OAuth
def login_google():
    # Generate a random nonce
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce  # Save nonce in session

    # Redirect Google for auth
    redirect_uri = url_for('auth_callback', _external=True)
    print(f"Redirect URI: {redirect_uri}")  # Verify generated URL
    return google.authorize_redirect(redirect_uri, nonce=nonce)

@bp.route('/login/callback')
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

# Ruta de logout
@bp.route('/logout')
def logout():
    session.pop('username', None)  # Delete username of session
    return redirect(url_for('index'))
