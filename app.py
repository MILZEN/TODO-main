'''
    Título: TASKED
    Autor: Miguel Romo
    Proyecto de Pruebas de Software
    Fecha de actualización: 08/12/2024 10:20AM
'''

# LIBRERÍAS
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  # Para manejar ObjectId de MongoDB
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
PEOPLE_API_SCOPE = os.getenv('PEOPLE_API_SCOPE')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=GOOGLE_DISCOVERY_URL,  # Endpoint de descubrimiento
    client_kwargs={
        'scope': 'openid profile email'  # Permisos para acceder al perfil y email del usuario
    }
)

# Conexión a la base de datos MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/todolist")
mongo = PyMongo(app)

# Verificar la conexión a MongoDB
@app.before_first_request
def verify_mongo_connection():
    try:
        mongo.db.command('ping')  # Comando para hacer ping a la base de datos
        app.logger.debug("Conexión a MongoDB exitosa.")
    except Exception as e:
        app.logger.error(f"Error al conectar con MongoDB: {e}")

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
        app.logger.error(f"Error al conectar a la base de datos: {e}")
    
    return connection

# Funciones de hash para contraseñas
def gen_hash(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_hash(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

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

@app.route('/home/<username>')
def home(username):
    if 'username' in session:
        username = session['username']
    tasks = mongo.db.tasks.find({"username": username})
    return render_template('home.html', tasks=tasks, username=username)

@app.route('/add/<username>', methods=['POST'])
def add_task(username):
    title = request.form.get('title')
    priority = request.form.get('priority')

    if title:
        mongo.db.tasks.insert_one({
            'title': title,
            'priority': priority,
            'username': username,
            'completed': False
        })

    tasks = mongo.db.tasks.find({"username": username})
    return render_template('home.html', tasks=tasks, username=username)

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
