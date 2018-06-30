# code follow along via Corey Schafer on Youtube

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '708f3de3453f99ed0ebfd0db0dd899a2'
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) #max 20 characters
    email = db.Column(db.String(120), unique=True, nullable=False) #max 120 characters
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') #will hash image to something unique , will add default image later
    password = db.Column(db.String(60), nullable=False) #password will be hashed to 60 chars
    posts = db.relationship('Post', backref='author', lazy=True) #connects from posts model according to author, referencing Post class not a post

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #not using utcnow() because we dont want time at that moment
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #id of user who authored the post
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
#dummy data
posts = [
    {
        'author': 'Alex Drizos',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'June 26, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'June 27, 2018'
    }
]

testTitle = "Test Title"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title=testTitle)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username / password', 'danger')
    return render_template('login.html', title='Login', form=form)
