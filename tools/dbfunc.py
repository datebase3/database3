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
    12:"二次元"
}
type1 = {
    0:u"玄幻",
    1:u"奇幻",
    2:u"武侠",
    3:u"仙侠",
    4:u"都市",
    5:u"现实",
    6:u"军事",
    7:u"历史",
    8:u"游戏",
    9:u"体育",
    10:u"科幻",
    11:u"灵异",
    12:u"二次元"
}
name = {
    0:"xuanhuan",
    1:"qihuan",
    2:"wuxia",
    3:"xianxia",
    4:"dushi",
    5:"xianshi",
    6:"junshi",
    7:"lishi",
    8:"youxi",
    9:"tiyu",
    10:"kehaun",
    11:"lingyi",
    12:"erciyaun"
}

client = pymongo.MongoClient(MONGO_SERVER['server'], MONGO_SERVER['port'])

def getFlagByType(type_name):
    flag = -1
    for i in range(0, 13):
        if type[i] == type_name:
            flag = i
            break
    if flag == -1:
        for i in range(0, 13):
            if type1[i] == type_name:
                flag = i
                break
    return flag

def login_user(user,password):#完成
    if client.database.user.find_one({"user": user,"password": password}):
        return True
    else:
        return False

def test_user(user):#完成
    if client.database.user.find_one({"user": user}):
        return True
    else:
        return False

def insert_user(user,password,prefer_list):#未完成
    user_info = {
        "user":user,
        "password":password,
        "record":prefer_list
    }
    try:
        client.database.user.insert(user_info)
        return True
    except Exception:
        return False

def getBookByType(number,type_name):#完成
    if number == 0:
        return []
    books = []
    flag = getFlagByType(type_name)
    if flag == -1:
        return []
    collection = name[flag]
    db = client.database
    dbcol = db[collection]
    for each in dbcol.find().limit(number):
        books.append(client.database.book.find_one({'title':each['title']}))
    return books

def getBooksByUser(user):
    books = []
    user_info = client.database.user.find_one({"user": user})
    user_record = user_info["record"]
    total = 0
    for each in user_record:
        total = total+each
    if total!=0:
        for key,value in type.items():
            number = int(8*user_record[key]/total)
            if number == 0:
                continue
            type_name = value
            if getBookByType(number,type_name)==[]:
                continue
            for book in getBookByType(number,type_name):
                books.append(book)
    empty_num = 8-len(books)
    if empty_num!=0:
        for new_book in client.database.book.find().limit(empty_num):
            books.append(new_book)
    return books

def recauthors(user):
    authors = []
    flag = 0
    for author in client.database.author.find().sort("total_word",pymongo.DESCENDING):
        authors.append(author)
        flag = flag+1
        if flag>=6:
            break
    return authors

def getAllAuthors():
    authors = []
    flag = 0
    for author in client.database.author.find().sort("total_day", pymongo.DESCENDING):
        authors.append(author)
        flag = flag + 1
        if flag >= 18:
            break
    return authors

def getBookByTitle(title):
    return client.database.book.find_one({"title":title})

def getBookListByTitle(title,type):
    books = getBookByType(13,type)
    flag = -1
    for i in range(0,13):
        if books[i]['title']==title:
            flag = i
            break
    if flag == -1:
        books.pop(12)
    else:
        books.pop(flag)
    return books

def updateUser(user,type_name):
    flag = getFlagByType(type_name)
    if flag == -1:
        return
    user_info = client.database.user.find_one({"user": user})
    user_record = user_info["record"]
    user_record[flag] = user_record[flag]+1
    client.database.user.update({'user': user}, {'$set': {'record': user_record}})

def getBooksFromFirst():
    books = []
    for i in range(0,13):
        number = 0
        collection = name[i]
        db = client.database
        dbcol = db[collection]
        for book in dbcol.find():
            books.append(client.database.book.find_one({"title":book["title"]}))
            number = number + 1
            if number>2:
                break
    return books

def getAuthorByName(name):
    return client.database.author.find_one({"author":name})

def getBookByAuthor(name):
    relation = client.database.book_author.find_one({"author":name})
    books = []
    for each in relation["book"]:
        books.append(client.database.book.find_one({"title":each}))
    return books

def getBookByTypeFlag(number,flag):
    return getBookByType(number,type[flag])

def getType(flag):
    return type1[flag]

def test_book(name):
    if client.database.book.find_one({"title": name}):
        return True
    else:
        return False

def test_author(name):
    if client.database.author.find_one({"author":name}):
        return True
    else:
        return False