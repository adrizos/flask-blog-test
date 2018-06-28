from flask import Flask, render_template, url_for
app = Flask(__name__)


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

testTitle = "Test Tile"


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title=testTitle)


@app.route("/about")
def about():
    return render_template('about.html')
