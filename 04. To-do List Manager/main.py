'''PYCODE | @_py.code'''

# > 04. To-do List Manager

# * Source Code

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import time
from uuid import uuid4

# ? Creating Server/Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Creating Database Model
class Todo(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, primary_key = False)
    desc = db.Column(db.String, primary_key = False)
    is_done = db.Column(db.Boolean, default=False, primary_key = False)
    date = db.Column(db.String, default=time.strftime("%d:%m:%Y"), primary_key = False)
    
# * Base Route
@server.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

# * Route to add a new todo
@server.route('/add-todo')
def add():
    return render_template('add.html')

# * Route to save todo
@server.route('/save-todo', methods=['POST'])
def save():
    id = str(uuid4())
    title = request.form['title']
    desc = request.form['desc']
    
    new_todo = Todo(id=id, title=title, desc=desc)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')

# * Route to delete a todo
@server.route('/delete/<todo_id>')
def delelte(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

# * Route to mark a todo
@server.route('/mark/<todo_id>')
def mark(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.is_done = True
    db.session.commit()
    return redirect('/')

# ? Running the App
if __name__ == '__main__':
    with server.app_context():
        db.create_all()
    server.run(debug=True)