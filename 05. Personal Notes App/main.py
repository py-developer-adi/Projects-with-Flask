'''PYCODE | @_py.code'''

# > 05. Personal Notes App

# * Source Code

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Model
class Note(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# * Base Route
@server.route('/')
def index():
    # Query notes in ascending chronological order
    notes = Note.query.order_by(Note.date.asc()).all()
    return render_template("index.html", notes=notes)

# * Add Route
@server.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        id = str(uuid4())
        title = request.form['title']
        content = request.form['content']
        
        new_note = Note(id=id, title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add.html')
    
# * Edit Route
@server.route('/edit/<note_id>')
def edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    return render_template('edit.html', note=note)

# * Save Route
@server.route('/save/<note_id>', methods=['POST'])
def save(note_id):
    note = Note.query.filter_by(id=note_id).first()
    note.title = request.form['title']
    note.content = request.form['content']
    db.session.commit()
    return redirect('/')

# * Delete Route
@server.route('/delete/<note_id>')
def delete(note_id):
    note = Note.query.filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

# * Route to see notes in fullscreen
@server.route('/notes/<note_id>')
def check_notes(note_id):
    note = Note.query.filter_by(id=note_id).first()
    return render_template('note.html', note=note)

# ? Running the Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)
