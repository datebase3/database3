#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session, redirect, url_for, escape, request,render_template
from tools import dbfunc

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

@app.route('/')
@app.route('/index.html')
def index():
    books = dbfunc.getBooksFromFirst()
    return render_template('index.html',books = books,recbook = books,user_status = 0)

@app.route('/login',methods=['GET', 'POST'])
def login():#完成
    user = request.form['user']
    password = request.form['password']
    books = dbfunc.getBooksFromFirst()
    if dbfunc.login_user(user,password):#测试用户是否正确
        session["user"] = user
        recbook = dbfunc.getBooksByUser(session['user'])
        return render_template('index.html', books=books, recbook=recbook,user_status = 1,user = user)
    else:
        return render_template('index.html', books=books, recbook=books,user_status = 0)

@app.route('/regist',methods=['GET', 'POST'])
def regist():#完成
    user = request.form['user']
    password = request.form['password']
    prefer_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0,13):
        name = "type"+str(i)
        if request.form.get(name):
            prefer_list[i] = 1
    books = dbfunc.getBooksFromFirst()
    if dbfunc.test_user(user):  # 测试用户是否存在
        return render_template('index.html', books=books, recbook=books,user_status = 0)
    else:
        if dbfunc.insert_user(user, password,prefer_list):  # 添加用户
            session["user"] = user
            recbook = dbfunc.getBooksByUser(session['user'])
            return render_template('index.html', books=books, recbook=recbook,user_status = 1,user = user)

@app.route('/authors')
def authorList():
    allauthors = dbfunc.getAllAuthors()
    if session.get("user"):
        recauthors = dbfunc.recauthors(session['user'])
    else:
        recauthors = allauthors
    return render_template('authorList.html',recauthors = recauthors,allauthors = allauthors)

@app.route('/authorDetail/<name>',methods=['GET','POST'])
def authorDetail(name):
    author = dbfunc.getAuthorByName(name)
    author_list = dbfunc.getAllAuthors()
    books = dbfunc.getBookByAuthor(name)
    return render_template('authorDetail.html', author = author,author_list = author_list,books = books)

@app.route('/novelDetail/<title>',methods=['GET','POST'])
def novelDetail(title):
    book = dbfunc.getBookByTitle(title)
    book_list = dbfunc.getBookListByTitle(title,book['flag'])
    if session.get("user"):
        dbfunc.updateUser(session['user'],book['flag'])
    return render_template('novalDetail.html', book = book,book_list = book_list)

@app.route('/rankByType/<flag>',methods=['GET','POST'])
def rankByType(flag):
    books = dbfunc.getBookByTypeFlag(50,int(flag))
    return render_template('classify.html', books = books,type = dbfunc.getType(int(flag)))

if __name__ == '__main__':
    app.run(debug = True)
