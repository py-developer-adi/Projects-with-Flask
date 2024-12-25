'''PYCODE | @_py.code'''

# > 02. To-do List App

# * Source Code

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Model
class Todo(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, primary_key = False)
    desc = db.Column(db.String, primary_key = False)
    is_done = db.Column(db.Boolean, default = False, primary_key = False)
    
    def __repr__(self):
        return f"{self.title}: {self.is_done}"
    
# * Base Route
@server.route('/')
def index():
    todos = Todo.query.all()
    print(todos)
    return render_template('index.html', todos=todos)

# * Route to add new todo
@server.route('/add-todo')
def add_todo():
    return render_template('add.html')

# * Route to save todo
@server.route('/save-todo', methods=['POST'])
def save_todo():
    id = str(uuid4())
    title = request.form['title']
    desc = request.form['desc']
    
    new_todo = Todo(id=id, title=title, desc=desc)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')

# * Route to filter done and pending
@server.route('/filter/<query>')
def filter(query):
    if query == 'done':
        todos = Todo.query.filter_by(is_done=True).all()
    elif query == 'pending':
        todos = Todo.query.filter_by(is_done=False).all()
    return render_template('index.html', todos=todos)

# * Route to edit Todo
@server.route('/edit/<todo_id>')
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    return render_template('edit.html', todo=todo)

# * Route to save changes to edited todo
@server.route('/save/<todo_id>', methods=['POST'])
def save(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.title = request.form['title']
    todo.desc = request.form['desc']
    db.session.commit()
    return redirect('/')

# * Route to delete a todo
@server.route('/delete/<todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    
# * Route to delete a todo
@server.route('/mark/<todo_id>')
def mark(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.is_done = True
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)