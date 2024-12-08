from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  # Para manejar ObjectId de MongoDB
import mysql.connector
from mysql.connector import Error
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'tas^kedpas!sword?'  # Necesario para flash messages

# Conexión a la base de datos MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/todolist"
mongo = PyMongo(app)

# Conexión a la base de datos SQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="task"
        )
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    
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
                INSERT INTO user (username, email, password_hash, first_name, last_name)
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
                query = "SELECT password_hash, username FROM user WHERE email=%s"
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

if __name__ == '__main__':
    app.run(debug=True)
