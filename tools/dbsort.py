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
    10:"kehuan",
    11:"lingyi",
    12:"erciyaun"
}
client = pymongo.MongoClient(MONGO_SERVER['server'], MONGO_SERVER['port'])
flag = 0

for each in type:
    count = 1
    list2 = []
    collection = name[flag]
    db = client.database
    dbcol = db[collection]
    for book in client.database.book.find({"flag":type[each]}):
        new_book = {
            "title":book['title'],
            "moncount":book["moncount"]
        }
        list2.append(new_book)
    while len(list2) != 0:
        mongth_count = 0
        for book2 in list2:
            if int(book2["moncount"]) >= mongth_count:
                mongth_count = int(book2["moncount"])
                title = book2["title"]
        del_count = 0
        for book3 in list2:
            if book3["title"] == title:
                break
            del_count = del_count + 1
        del list2[del_count]
        div = {
            "title": title,
            "number": count,
        }
        dbcol.insert(div)
        count = count + 1
    flag = flag + 1