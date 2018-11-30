from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    if 'search' in session:
        result = "???"
    else:
        result = "!!!"
    result = [
        {
            'name': 1,
            'author': 2
        },{
            'name': 2,
            'author': 3
        },{
            'name': 3,
            'author': 4
        }
    ]
    return render_template('index.html',result = result)


if __name__ == '__main__':
    app.run(debug = True)
