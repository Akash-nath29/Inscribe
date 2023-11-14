from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'MLXH243rjBDIBibiBIbibIUBImmfrdTWS7FDhdwYF56wPj8'

db = SQLAlchemy(app)
#TODO: Create database
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    notesName = db.Column(db.String(100), nullable=True)
    notesContent = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime())
    
    def __init__(self, notesName, notesContent):
        self.notesName = notesName
        self.notesContent = notesContent
        self.created_at = datetime.datetime.now()
        
#TODO: Create Task Model        
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    taskName = db.Column(db.String(100), nullable=False)
    taskDescription = db.Column(db.Text(1000), nullable=True)
    created_at = db.Column(db.DateTime())
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    
    def __init__(self, taskName, taskDescription):
        self.taskName = taskName
        self.taskDescription = taskDescription
        self.created_at = datetime.datetime.now()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes')
def notes():
    notes = Note.query.order_by(desc(Note.created_at)).all()
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
        newNotes = Note(notesName=notesName, notesContent=notesContent)
        db.session.add(newNotes)
        db.session.commit()
        return redirect('/notes')
    return render_template('createNotes.html')

@app.route('/createTasks', methods=['GET', 'POST'])
def createTasks():
    if request.method == 'POST':
        taskName = request.form.get('taskName')
        taskDescription = request.form.get('taskContent')
        newTask = Task(taskName=taskName, taskDescription=taskDescription)
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