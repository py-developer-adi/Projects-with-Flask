'''PYCODE | @_py.code'''

# > 08. Feedback Form App

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Creating Database Class
class Feed(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, primary_key=False)
    feed = db.Column(db.String, primary_key=False)
    
# * Base Route
@server.route('/')
def index():
    return render_template('index.html')

# * Route to handle Feedback
@server.route('/feed', methods=['POST'])
def feed():
    id = str(uuid4())
    email = request.form['email']
    feed = request.form['feed']
    
    new_feed = Feed(id=id, email=email, feed=feed)
    db.session.add(new_feed)
    db.session.commit()
    return redirect('/')

# * Route to see all feedbacks
@server.route('/all-feeds')
def show_feeds():
    feeds = Feed.query.all()
    return render_template('feed.html', feeds=feeds)

# ? Running the Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)