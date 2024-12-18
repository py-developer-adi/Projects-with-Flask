'''PYCODE'''

# > 01. Contact Management

# * Source code
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import requests

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

class Contact(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, primary_key = False)
    email = db.Column(db.String, primary_key = False)
    phone = db.Column(db.String, primary_key = False)
    
    def __repr__(self):
        return f"Name: {self.name}"
    
@server.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@server.route('/new-contact')
def new():
    return render_template('add.html')  

@server.route('/add-contact', methods=['POST'])
def add():
    id = str(uuid4())
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    
    new_contact = Contact(id=id, name=name, email=email, phone=phone)
    db.session.add(new_contact)
    db.session.commit()
    return redirect('/')

@server.route('/delete-contact/<contact>')
def delete(contact):
    contacts = Contact.query.filter_by(id=contact).first()
    db.session.delete(contacts)
    db.session.commit()
    return redirect('/')

@server.route('/find', methods=['GET', 'POST'])
def find():
    query = request.args.get('search')
    contacts = Contact.query.filter_by(name=query).all()
    return render_template('user.html', contacts=contacts, title={"title": query})

if __name__ == '__main__':
    with server.app_context():
        db.create_all()
    server.run(debug=True)