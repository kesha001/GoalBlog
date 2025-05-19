from app import app
from flask import url_for, render_template


@app.route('/')
@app.route('/index')
def index():
    print(url_for('index'))

    user = {'username': 'John'}
    # list of goals , think about structure of these goals


    return render_template('index.html')