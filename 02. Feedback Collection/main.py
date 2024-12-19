'''PYCODE | @_py.code'''

# > 02. Feedback Collection

# * Source Code
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

class Feedback(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, primary_key = False)
    email = db.Column(db.String, primary_key = False)
    feedback = db.Column(db.String, primary_key = False)    
    
    def __repr__(self):
        return f"{self.username}: {self.email}"
    
@server.route('/')
def index():
    return render_template('index.html')

@server.route('/feedback', methods=['POST'])
def get_feed():
    id = str(uuid4())
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']
    
    new_feed = Feedback(id=id, name=name, email=email, feedback=feedback)
    db.session.add(new_feed)
    db.session.commit()
    return redirect('/')

@server.route('/admin')
def admin():
    feeds = Feedback.query.all()
    return render_template('admin.html', feeds=feeds)

if __name__ == '__main__':
    with server.app_context():
        db.create_all()
    server.run(debug=True)