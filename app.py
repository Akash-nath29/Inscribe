from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_bcrypt import Bcrypt
import os
import datetime
# from werkzeug.security import generate_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://akash_nath29:8LYkOQm7Q9aVTSf9X57S6ml1eaZzXpKW@dpg-cnnitv5jm4es73c29mgg-a.singapore-postgres.render.com/inscribe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'MLXH243rjBDIBibiBIbibIUBImmfrdTWS7FDhdwYF56wPj8'

bcrypt = Bcrypt(app)
# session.init_app(app)
db = SQLAlchemy(app)
#TODO: Create database

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note', backref='author', lazy=True)
    tasks = db.relationship('Task', backref='author', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    notesName = db.Column(db.String(100), nullable=True)
    notesContent = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, notesName, notesContent, user_id):
        self.notesName = notesName
        self.notesContent = notesContent
        self.created_at = datetime.datetime.now()
        self.user_id = user_id
        
#TODO: Create Task Model        
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.String(100), nullable=False)
    taskDescription = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime())
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, taskName, taskDescription, user_id):
        self.taskName = taskName
        self.taskDescription = taskDescription
        self.created_at = datetime.datetime.now()
        self.user_id = user_id
        
        
admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Note, db.session))
admin.add_view(ModelView(Task, db.session))

class RegistrationForm:
    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Example: Check user credentials in the database
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Successful login
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('notes'))
        else:
            # Invalid credentials
            flash('Invalid username or password', 'error')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation (you can add more validation as needed)
        if not username or not email or not password or not confirm_password:
            flash('All fields are required', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        # Check if the username or email already exists in the database
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Username or email already exists', 'error')
            return redirect(url_for('register'))

        # Create a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        user = user = User.query.filter_by(email=email).first()
        session['user_id'] = user.id
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('notes'))

    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session['user_id'] = None
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes')
def notes():
    # notes = Note.query.order_by(desc(Note.created_at)).all()
    notes = Note.query.filter_by(user_id=session['user_id']).order_by(desc(Note.created_at)).all()
    return render_template('notes.html', notes=notes)

@app.route('/tasks')
def tasks():
    tasks = Task.query.order_by(desc(Task.created_at)).all()
    return render_template('tasks.html', tasks = tasks)

@app.route('/createNotes', methods=['GET', 'POST'])
def createNotes():
    if request.method == 'POST':
        notesName = request.form.get('notesName')
        notesContent = request.form.get('notesContent')
        newNotes = Note(notesName=notesName, notesContent=notesContent, user_id=session['user_id'])
        db.session.add(newNotes)
        db.session.commit()
        return redirect('/notes')
    return render_template('createNotes.html')

@app.route('/createTasks', methods=['GET', 'POST'])
def createTasks():
    if request.method == 'POST':
        taskName = request.form.get('taskName')
        taskDescription = request.form.get('taskContent')
        newTask = Task(taskName=taskName, taskDescription=taskDescription, user_id=session['user_id'])
        db.session.add(newTask)
        db.session.commit()
        return redirect('/tasks')
    return render_template('createTasks.html')

@app.route('/<int:id>/viewNote')
def viewNote(id):
    note = Note.query.get(id)
    return render_template('viewNotes.html', note=note)

@app.route('/<int:id>/viewTask')
def viewTask(id):
    task = Task.query.get(id)
    return render_template('viewTasks.html', task=task)

@app.route('/<int:id>/delete')
def delete(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/notes')

@app.route('/<int:id>/deleteTask')
def deleteTask(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/tasks')

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.notesName = request.form.get('notesName')
        note.notesContent = request.form.get('notesContent')
        db.session.commit()
        return redirect('/notes')
    return render_template('editNotes.html', note=note)

@app.route('/<int:id>/editTask', methods=['GET', 'POST'])
def editTask(id):
    task = Task.query.get(id)
    if request.method == 'POST':
        task.taskName = request.form.get('taskName')
        task.taskDescription = request.form.get('taskDescription')
        db.session.commit()
        return redirect('/tasks')
    return render_template('editTasks.html', task=task)


@app.route('/<int:id>/completeTask')
def completeTask(id):
    task = Task.query.get(id)
    task.is_completed = True
    db.session.commit()
    return redirect('/tasks')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')