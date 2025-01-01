'''PYCODE | @_py.code'''

# > 09. Mini Social Media Feed

# * Source Code

# ? Importing Libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feed.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Class
class Feed(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, primary_key=False)
    post = db.Column(db.String, primary_key=False)
    keywords = db.Column(db.String, primary_key=False)
    
# * Base Route
@server.route('/')
def index():
    feeds = Feed.query.all()   
    return render_template('index.html', feeds=feeds)

# * Route to Add New Feed
@server.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('new.html')
    
    else:
        id = str(uuid4())
        title = request.form['title']
        post = request.form['post']
        keywords = request.form['keywords']
        
        new_feed = Feed(id=id, title=title, post=post, keywords=keywords)
        db.session.add(new_feed)
        db.session.commit()
        return redirect('/')
    
# * Route to Search a Post
@server.route('/search')
def search():
    query = request.args.get('query')
    results = []
    feeds = Feed.query.all()
    for feed in feeds:
        if query in feed.keywords.split(" | "):
            results.append(feed)
    return render_template('index.html', feeds=results)
    
# ? Running The Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)