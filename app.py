#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, url_for, escape, request,render_template
from tools import dbfunc

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    user = request.form['user']
    password = request.form['password']
    if request.form['login'] == u"登录":
        if dbfunc.login_user(user,password):#测试用户是否正确
            session["user"] = user
            return render_template('index.html')
        else:
            return render_template('login.html')
    elif request.form['login'] == u"注册":
        if dbfunc.test_user(user):#测试用户是否存在
            return render_template('login.html')
        else:
            if dbfunc.insert_user(user,password):#添加用户
                session["user"] = user
                return render_template('index.html')
            else:
                return render_template('login.html')

@app.route('/header.html')
def navigation_bar():
    return render_template('header.html')

@app.route('/recommend.html')
def recommend():
    if session.get("user"):
        result = dbfunc.getBooksByUser(session.get("user"))#通过用户名获取浏览记录，通过看过书的标签获取推荐书单
        return render_template('recommend.html', result=result)
    else:
        return render_template('login.html')

@app.route('/introduction',methods=['GET', 'POST'])
def introduction():
    book = request.args.get('book')
    author = request.args.get('author')
    if book == "0":
        result = None#getIntroByAuthor(author)
        return render_template('introduction.html', result=result)#作者介绍界面
    elif author == "0":
        result = dbfunc.getIntroByBook(book)
        return render_template('introduction.html', result=result)
    else:
        return redirect(url_for('recommend'))


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
    result = None#getbooksbyfind(search_con)#通过搜索内容获取书单
    return render_template('result.html',result = result)

if __name__ == '__main__':
    app.run(debug = True)
