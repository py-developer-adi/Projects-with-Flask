'''PYCODE | @_py.code'''

# > 06. Basic E-commerce Catalog

# * Source Code

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
server.config['SQLALCHEMY_TRACK_MOFIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Model
class Product(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, primary_key = False)
    desc = db.Column(db.String, primary_key = False)
    price = db.Column(db.Float, primary_key = False)
    
# * Base Route
@server.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# * Admin Route
@server.route('/admin')
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products)

# * Route to Add Product
@server.route('/admin/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        id = str(uuid4())
        title = request.form['title']
        desc = request.form['desc']
        price = request.form['price']
        
        new_product = Product(id=id, title=title, desc=desc, price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/admin')
    
# * Route to Edit Product
@server.route('/admin/edit/<product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if request.method == 'GET':
        return render_template('edit.html', product=product)
    else:
        product.title = request.form['title']    
        product.desc = request.form['desc']    
        product.price = request.form['price']
        db.session.commit()
        return redirect('/admin')
    
# * Route to Delete Product
@server.route('/admin/delete/<product_id>')
def delete(product_id):
    product = Product.query.filter_by(id=product_id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect('/admin')

# ? Running the Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)