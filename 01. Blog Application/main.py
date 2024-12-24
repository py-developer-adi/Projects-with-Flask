'''PYCODE | @_py.code'''

# > 01. Blog Application

# * Source Code

# ? Importing Libraries
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

# ? Creating Server and Database
server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

# ? Database Model
class Blog(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, primary_key = False)
    content = db.Column(db.String, primary_key = False)
    stamp = db.Column(db.DateTime, default = datetime.utcnow, primary_key = False)
    
# * Base Route
@server.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('index.html', blogs=blogs)

# * Route to Add Blog
@server.route('/admin/add-blog')
def add_blog():
    return render_template('add.html')

# * Route to Save Blog
@server.route('/admin/save-blog', methods=['POST'])
def save_blog():
    id = str(uuid4())
    title = request.form['title']
    content = request.form['content']

    new_blog = Blog(id=id, title=title, content=content)
    db.session.add(new_blog)
    db.session.commit()
    return redirect('/')

# * Route to Show Blog
@server.route('/blogs/<blog_id>')
def show_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog:
        return render_template('blog.html', blog=blog)
    else:
        return "Blog Not Found", 404
    
# * Route to edit blog
@server.route('/admin/edit/<blog_id>')
def edit(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    return render_template('edit.html', blog=blog)

# * Route to save changes of edited blog
@server.route('/save-changes/<blog_id>', methods=['POST'])
def save_changes(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    blog.title = request.form['title']
    blog.content = request.form['content']
    db.session.commit()
    return redirect('/')

# * Route to delete a blog
@server.route('/admin/delete/<blog_id>')  
def delete_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect('/')

# ? Running the Server
if __name__ == "__main__":
    with server.app_context():
        db.create_all()
    server.run(debug=True)