from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/header.html')
def navigation_bar():
    return render_template('header.html')

@app.route('/recommend.html')
def recommend():
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
    return render_template('recommend.html',result = result)

@app.route('/test.html')
def test():
    return render_template('test.html')

@app.route('/search.html')
def go_search():
    return render_template('search.html')

@app.route('/result',methods=['GET', 'POST'])
def search():
    if request.method!="POST":
        return render_template('recommend.html')
    if request.form['search_con']=="":
        return render_template('recommend.html')
    search_con = request.form['search_con']
    result = [
        {
            'name': 1,
            'author': 2
        }, {
            'name': 2,
            'author': 3
        }, {
            'name': 3,
            'author': 4
        }
    ]
    return render_template('result.html',result = result)

if __name__ == '__main__':
    app.run(debug = True)
