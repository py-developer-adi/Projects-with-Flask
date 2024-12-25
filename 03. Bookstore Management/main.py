'''PYCODE | @_py.code'''

# > 03. Bookstore Management

# * Source Code

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Model
class Book(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, primary_key = False)
    author = db.Column(db.String, primary_key = False)
    price = db.Column(db.Float, primary_key = False)
    stock = db.Column(db.Integer, primary_key = False)
    
# * Base Route
@server.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

# * Route to Search Books
@server.route('/search')
def search():
    query = request.args.get('query')
    books = Book.query.filter_by(title=query).all()
    return render_template('index.html', books=books)

# * Admin Page
@server.route('/admin')
def admin():
    books = Book.query.all()
    return render_template('admin.html', books=books)

# * Route to Add book
@server.route('/admin/add-book', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        id = str(uuid4())
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        stock = request.form['stock']
        
        new_book = Book(id=id, title=title, author=author, price=float(price), stock=int(stock))
        db.session.add(new_book)
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('add.html')
    
# * Route to Edit book
@server.route('/admin/edit-book/<book_id>', methods=['GET', 'POST'])
def edit(book_id):
    if request.method == 'POST':
        book = Book.query.filter_by(id=book_id).first()
        book.title = request.form['title']
        book.author = request.form['author']
        book.price = float(request.form['price'])
        book.stock = int(request.form['stock'])
        db.session.commit()
        return redirect('/admin')
        
    else:
        book = Book.query.filter_by(id=book_id).first()
        return render_template('edit.html', book=book)
    
# * Route to Delete book
@server.route('/admin/remove-book/<book_id>')
def delete(book_id):
    book = Book.query.filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/admin')

# ? Running The Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)