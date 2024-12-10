from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from app import mongo
from bson.objectid import ObjectId

bp = Blueprint('tasks', __name__)

@bp.route('/home/<username>')
def home(username):
    # Obtain username in session
    if 'username' in session:
        username = session['username']
    tasks = mongo.db.tasks.find({"username": username}) # Tasks that user created
    return render_template('home.html', tasks=tasks, username=username)

@bp.route('/add/<username>', methods=['POST'])
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

@bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit_task(id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_priority = request.form.get('priority')
        mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {'title': new_title, 'priority': new_priority}})
        return redirect(url_for('tasks.home', username=task['username']))
    return render_template('edit.html', task=task)

@bp.route('/update-completion/<id>', methods=['POST'])
def update_completion(id):
    data = request.get_json()
    is_completed = data.get('completed')
    if is_completed is not None:
        mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {'completed': is_completed}})
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@bp.route('/delete/<id>')
def delete_task(id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    if task:
        mongo.db.tasks.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('tasks.home', username=task['username']))
    return redirect(url_for('tasks.home', username='default'))