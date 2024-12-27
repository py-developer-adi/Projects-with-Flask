'''PYCODE | @_py.code'''

# > 06. RESTful API for Books

# * Source Code

# ? Importing Libraries
from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
import sqlite3, json

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# | Paths
database_file = 'instance/books.db'
output_file = 'books.json'

# Connect to the SQLite database
conn = sqlite3.connect(database_file)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute an SQL query to fetch data from a table (change 'Book' to your table name)
cursor.execute('SELECT * FROM Book')

# Fetch all rows from the query result
rows = cursor.fetchall()

# Get the column names from the cursor description
column_names = [description[0] for description in cursor.description]

# Create a list to store the data
data = []

# Iterate through the rows and convert them to dictionaries
for row in rows:
    data.append(dict(zip(column_names, row)))

# Close the cursor and database connection
cursor.close()
conn.close()

with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)

# ? Database Class
# Title, Author, ISBN, Published Year, Availability
class Book(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, primary_key=True)
    author = db.Column(db.String, primary_key=True)
    isbn = db.Column(db.String(13), primary_key=True)
    published = db.Column(db.String, default=datetime.utcnow, primary_key=True)
    stock = db.Column(db.Integer, primary_key=True)
    
# * API Route
@server.route('/api')
def api():
    with open(output_file, 'r') as f:
        return jsonify(json.load(f))   

# * Base Route
@server.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

# * Route to add Book
@server.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        id = str(uuid4())
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        published = request.form['published']
        stock = request.form['stock']
        
        new_book = Book(id=id, title=title, author=author, isbn=isbn, published=published, stock=stock)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/')
        
    else:
        return render_template('add.html')

# * Route to edit book
@server.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.published = request.form['published']
        book.stock = request.form['stock']
        
        db.session.commit()
        return redirect('/')
        
    else:
        return render_template('edit.html', book=book)

# * Route to delete book
@server.route('/delete/<book_id>')
def delete(book_id):
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/')

# ? Running the Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)