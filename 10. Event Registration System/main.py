'''PYCODE | @_py.code'''

# > 10. Event Registration System

# * Source Code

# ? Importing Libraries
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Class
class Registration(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, primary_key=False)
    email = db.Column(db.String, primary_key=False)
    
# * Base Route
@server.route('/')
def index():
    return render_template('index.html')

# * Route to Register for event
@server.route('/register', methods=['POST'])
def register():
    id = str(uuid4())
    name = request.form['name']
    email = request.form['email']
    
    new_register = Registration(id=id, name=name, email=email)
    db.session.add(new_register)
    db.session.commit()
    return redirect('/')

# * Admin Page to View all Registrations
@server.route('/admin/')
def admin():
    registrations = Registration.query.all()
    return render_template('admin.html', registrations=registrations)

# ? Running the Server 
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)
    
    