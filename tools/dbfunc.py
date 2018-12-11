#!/usr/bin/env python
# -*- coding:utf8 -*-
import pymongo

MONGO_SERVER = {
    # 'server': '10.80.94.84',
    'server': 'localhost',
    'port':27017,
    'db': 'db',
    'collection': 'url_filter',
    'user': 'root',
    'password': '1234'
}
type = {
    0:"玄幻",
    1:"奇幻"
}

client = pymongo.MongoClient(MONGO_SERVER['server'], MONGO_SERVER['port'])

def login_user(user,password):
    if client.db.news.find({"user": user,"password": password}):
        return True
    else:
        return False

def test_user(user):
    if client.db.news.find({"user": user}):
        return True
    else:
        return False

def insert_user(user,password):
    user_info = {
        "user":user,
        "password":password,
        "record":[0,0,0,0,0,0,0,0]
    }
    try:
        client.db.news.insert(user_info)
        return True
    except Exception:
        return False

def getBookByType(number,type_name):
    books = client.db.news.find({"type": type_name})
    new_books = []
    if len(books)>number:
        for i in range(0,number-1):
            new_books.append(books[i])
    return new_books

def getBooksByUser(user):
    books = []
    user_info = client.db.news.find({"user": user})
    user_record = user_info["record"]
    total = 0
    for each in user_record:
        total = total+each
    for key,value in type:
        number = 100*user_record[key]/total
        type_name = value
        books.append(getBookByType(number,type_name))
    return books