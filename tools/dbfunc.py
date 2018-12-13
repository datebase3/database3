#!/usr/bin/env python
# -*- coding:utf8 -*-
import pymongo
from bson.objectid import ObjectId

MONGO_SERVER = {
    'server': 'localhost',
    'port':27017,
}
type = {
    0:"玄幻",
    1:"奇幻",
    2:"武侠",
    3:"仙侠",
    4:"都市",
    5:"现实",
    6:"军事",
    7:"历史",
    8:"游戏",
    9:"体育",
    10:"科幻",
    11:"灵异",
    #12:"二次元",
    #13:"短篇",
}

client = pymongo.MongoClient(MONGO_SERVER['server'], MONGO_SERVER['port'])

def login_user(user,password):
    if client.database.user.find_one({"user": user,"password": password}):
        return True
    else:
        return False

def test_user(user):
    if client.database.user.find_one({"user": user}):
        return True
    else:
        return False

def insert_user(user,password):
    user_info = {
        "user":user,
        "password":password,
        "record":[1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    }
    try:
        client.database.user.insert(user_info)
        return True
    except Exception:
        return False

def getBookByType(number,type_name):
    books = []
    for book in client.database.book.find({"flag":type_name}):
        books.append(book)
    if books == [] or len(books)<number:
        return
    new_books = []
    for i in range(0,number-1):
        new_books.append(books[i])
    return new_books

def getBooksByUser(user):
    books = []
    user_info = client.database.user.find_one({"user": user})
    user_record = user_info["record"]
    #total = 0
    #for each in user_record:
        #total = total+each
    total = 12
    for key,value in type.items():
        number = 100*user_record[key]/total
        type_name = value
        if getBookByType(number,type_name)==[]:
            continue
        for book in getBookByType(number,type_name):
            books.append(book)
    return books

def getIntroByBook(book):
    result = client.database.book.find_one({"_id": ObjectId(book)})
    return result

def prefer_add(user,flag):
    change_num = -1
    for key, value in type.items():
        if flag == value:
            change_num = key
    if change_num == -1:
        return False
    try:
        user_info = client.database.user.find_one({"user": user})
        record = user_info['record']
        record[change_num] = record[change_num]+2
        client.database.user.update({'user': user}, {'$set': {'record': record}})
        return True
    except Exception:
        return False