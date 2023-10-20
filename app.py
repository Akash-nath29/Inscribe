from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
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
        self.created_at = datetime.datetime.utcnow()

@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        notesName = request.form.get('notesName')
        notesContent = request.form.get('notesContent')
        newNotes = Note(notesName=notesName, notesContent=notesContent)
        db.session.add(newNotes)
        db.session.commit()
        return redirect('/')
    return render_template('createNotes.html')

@app.route('/<int:id>/viewNote')
def viewNote(id):
    note = Note.query.get(id)
    return render_template('viewNotes.html', note=note)

@app.route('/<int:id>/delete')
def delete(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.notesName = request.form.get('notesName')
        note.notesContent = request.form.get('notesContent')
        db.session.commit()
        return redirect('/')
    return render_template('editNotes.html', note=note)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')