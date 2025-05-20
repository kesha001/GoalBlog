from app import app
from flask import url_for, render_template


@app.route('/')
@app.route('/index')
def index():
    print(url_for('index'))

    user = {'username': 'John'}
    # list of goals , think about structure of these goals
    # it should be a group of goals with title and goals inside
    goals = [
    
    {
        "author": {'username': 'John'},
        "title": "Make a goal",
        "body": "make that goal is on webpage"
    },
    {
        "author": {'username': 'Susan'},
        "title": "Find a job",
        "body": "learn, get skills, pass intervju"
    },
    ]


    return render_template('index.html', user=user, goals=goals)