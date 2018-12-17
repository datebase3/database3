#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, url_for, escape, request,render_template
from tools import dbfunc

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

@app.route('/')
@app.route('/index.html')
def index():
    books = dbfunc.getBookByType(18,"玄幻")
    return render_template('index.html',books = books,recbook = books)

@app.route('/login',methods=['GET', 'POST'])
def login():
    user = request.form['user']
    password = request.form['password']
    books = dbfunc.getBookByType(18, "玄幻")
    if dbfunc.login_user(user,password):#测试用户是否正确
        session["user"] = user
        recbook = dbfunc.getBooksByUser(session['user'])
        return render_template('index.html', books=books, recbook=recbook)
    else:
        return render_template('index.html', books=books, recbook=books)

@app.route('/regist',methods=['GET', 'POST'])
def regist():#缺少偏好列表
    user = request.form['user']
    password = request.form['password']
    books = dbfunc.getBookByType(18, "玄幻")
    if dbfunc.test_user(user):  # 测试用户是否存在
        return render_template('index.html', books=books, recbook=books)
    else:
        if dbfunc.insert_user(user, password):  # 添加用户
            session["user"] = user
            recbook = dbfunc.getBooksByUser(session['user'])
            return render_template('index.html', books=books, recbook=recbook)

@app.route('/authors')
def authorList():
    if session.get("user"):
        recauthors = dbfunc.recauthors(session['user'])
    else:
        recauthors = dbfunc.recauthors("???")
    allauthors = dbfunc.getAllAuthors()
    return render_template('authorList.html',recauthors = recauthors,allauthors = allauthors)

@app.route('/novelDetail/<title>',methods=['GET','POST'])
def novelDetail(title):
    book = dbfunc.getBookByTitle(title)
    book_list = dbfunc.getBookListByTitle(title,book['flag'])
    if session.get("user"):
        dbfunc.updateUser(session['user'],book['flag'])
    return render_template('novalDetail.html', book = book,book_list = book_list)

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
