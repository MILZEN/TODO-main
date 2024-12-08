'''
    Título: TASKED
    Autor: Miguel Romo
    Proyecto de Pruebas de Software
    Fecha de actualización: 08/12/2024 12:31PM
'''

# LIBRERÍAS
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  # Para manejar ObjectId de MongoDB
from mysql.connector import Error
import bcrypt
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os
import secrets
import psycopg2
from psycopg2 import Error
import logging
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Cargar variables de entorno
load_dotenv()

# Usar 'dev' como valor predeterminado de entorno
environment = os.getenv('FLASK_ENV', 'development')

# Seleccionar entorno
if environment == 'development':
    # Variables de entorno locales (development)
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'task')
else:
    # Variables de entorno de Render (deployment)
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

# Inicialización de Flask y OAuth
app = Flask(__name__)
app.secret_key = 'tas^kedpas!sword?'  # Necesario para flash messages
app.logger.setLevel(logging.DEBUG)

app.logger.debug(f"GOOGLE_CLIENT_ID: {os.getenv('GOOGLE_CLIENT_ID')}")
app.logger.debug(f"GOOGLE_CLIENT_SECRET: {os.getenv('GOOGLE_CLIENT_SECRET')}")

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = os.getenv('GOOGLE_DISCOVERY_URL')
GOOGLE_SCOPES = os.getenv('GOOGLE_SCOPES', 'openid profile email')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=GOOGLE_DISCOVERY_URL,
    client_kwargs={
        'scope': GOOGLE_SCOPES  # Usar el scope definido previamente
    }
)

# Conexión a la base de datos MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/todolist")
mongo = PyMongo(app)

# Conexión a la base de datos SQL (Postgre en Deployment)
def create_connection():
    connection = None
    try:
        # Usar DATABASE_URL para PostgreSQL en producción
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            connection = psycopg2.connect(database_url, sslmode='require')
        else:
            # Si no se encuentra DATABASE_URL, intenta con las variables de entorno locales
            connection = psycopg2.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                sslmode='require'  # Usamos SSL para conexiones seguras en Render
            )
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    
    return connection

# Funciones de hash para contraseñas
def gen_hash(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_hash(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Función para obtener los eventos de Google Calendar
def get_google_calendar_events():
    if 'google_token' not in session:
        flash('You need to be logged in with Google to view calendar events', 'danger')
        return None

    google_token = session['google_token']
    
    # Verificar si el token tiene todos los campos necesarios
    if not all(key in google_token for key in ('refresh_token', 'client_id', 'client_secret')):
        flash("Your session has expired or the token is incomplete. Please log in again.", 'danger')
        return redirect(url_for('login_google'))

    try:
        credentials = Credentials.from_authorized_user_info(info=google_token)
    except ValueError as e:
        flash(f"Token error: {str(e)}", "danger")
        return redirect(url_for('login_google'))

    try:
        # Construir el servicio de la API de Google Calendar
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(
            calendarId='primary', timeMin='2024-12-01T00:00:00Z', maxResults=10, singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # Si no hay eventos
        if not events:
            return None

        return events
    except Exception as e:
        flash(f'Error retrieving calendar events: {e}', 'danger')
        return None

# Rutas y lógica de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        hashed_pwd = gen_hash(password)
        connection = create_connection()

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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = create_connection()

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

@app.route('/login/google')
def login_google():
    # Generar un nonce aleatorio
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce  # Guardar el nonce en la sesión

    # Redirigir a Google para autenticación
    redirect_uri = url_for('auth_callback', _external=True)
    print(f"Redirect URI: {redirect_uri}")  # Verificar la URL generada
    return google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/login/callback')
def auth_callback():
    # Recuperar el nonce de la sesión
    nonce = session.pop('nonce', None)

    try:
        # Obtener el token de acceso de Google
        token = google.authorize_access_token()
        print("Token de acceso recibido:", token)  # Depuración: Imprimir el token recibido
        session['google_token'] = token

        # Intentar parsear el ID token con el nonce
        user = google.parse_id_token(token, nonce=nonce)
        if user is None:
            raise ValueError("El ID token es None")
        
        print("Perfil de usuario:", user)  # Depuración: Imprimir el perfil del usuario

    except Exception as e:
        flash(f"Error al obtener el perfil del usuario: {e}", "danger")
        return redirect(url_for('login'))

    # Conectar a la base de datos
    connection = create_connection()
    cursor = connection.cursor()

    # Comprobar si el usuario ya existe en la base de datos
    cursor.execute("SELECT username FROM users WHERE email=%s", (user['email'],))
    result = cursor.fetchone()

    if result:
        username = result[0]
    else:
        # Si el usuario no existe, crear uno nuevo
        username = user['given_name']  # Usar el nombre proporcionado por Google
        hashed_pwd = gen_hash('defaultpassword')  # Asignar una contraseña temporal

        cursor.execute(
            "INSERT INTO users (username, email, password_hash, first_name, last_name) "
            "VALUES (%s, %s, %s, %s, %s)",
            (username, user['email'], hashed_pwd, user['given_name'], user['family_name'])
        )
        connection.commit()

    cursor.close()
    connection.close()

    # Almacenar el username en la sesión
    session['username'] = username

    # Redirigir al usuario a la página de home con el nombre de usuario
    return redirect(url_for('home', username=username))

@app.route('/home/<username>')
def home(username):
    if 'username' in session:
        username = session['username']
    
    tasks = mongo.db.tasks.find({"username": username})
    
    # Obtener los eventos del calendario de Google
    calendar_events = get_google_calendar_events()
    
    return render_template('home.html', tasks=tasks, username=username, calendar_events=calendar_events)

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
    session.pop('username', None)  # Eliminar el username de la sesión
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
