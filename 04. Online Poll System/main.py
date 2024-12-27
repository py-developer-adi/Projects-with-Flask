'''PYCODE | @_py.code'''

# > 04. Online Poll System

# * Source Code

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

# ? Creating Server
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poll.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Class
class Poll(db.Model):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String, primary_key = False)
    user = db.Column(db.String, primary_key = False)

# * Base Route
@server.route('/')
def index():
    return render_template('index.html')

# * Submit Route
@server.route('/submit', methods=['POST'])
def submit():
    id = str(uuid4())
    email = request.form['email']    
    user = request.form['option']
    
    new_poll = Poll(id=id, email=email, user=user)
    db.session.add(new_poll)
    db.session.commit()
    
    return redirect('/results')

# * Results Route
@server.route('/results')
def results():
    results = Poll.query.all()     
    return render_template('results.html', results=results)

# ? Running The Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)