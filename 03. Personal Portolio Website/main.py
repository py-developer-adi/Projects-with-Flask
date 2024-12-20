'''PYCODE | @_py.code'''

# > 03. Personal Portfolio Website

# * Source Code
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from uuid import uuid4

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
mail = Mail(server)

class Project(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, primary_key=True)
    description = db.Column(db.String, primary_key=True)
    keywords = db.Column(db.String, primary_key=True)
    
@server.route('/')
def index():
    return render_template('index.html')

@server.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@server.route('/contact')
def contact():
    return render_template('contact.html')

@server.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    title = request.form['title']
    message = request.form['message']
    
    server.config['MAIL_SERVER']='smtp.gmail.com'
    server.config['MAIL_PORT'] = 465
    server.config['MAIL_USERNAME'] = email
    server.config['MAIL_PASSWORD'] = password
    server.config['MAIL_USE_TLS'] = False
    server.config['MAIL_USE_SSL'] = True
    mail = Mail(server) 
    
    msg = Message(
        title,
        sender=email,
        recipients=['adiprofitcoder@gmail.com']
    )
    msg.body = message
    mail.send(msg)
    return redirect('/')

@server.route('/admin')
def admin():
    return render_template('admin.html')

@server.route('/admin/add-project')
def add_project():
    return render_template('add.html')

@server.route('/save-post', methods=['POST'])
def save_post():
    id = str(uuid4())
    title = request.form['title']
    description = request.form['description']
    keywords = request.form['keywords']
    
    new_post = Project(id=id, title=title, description=description, keywords=keywords)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/admin')

if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)