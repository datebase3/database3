#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

db = MongoClient('localhost', 27017)
count = 1
list1 = db.database.book.find()
list2 = []
list3 = []
for book in list1:
    div = {
        "title":book["title"],
        "moncount":book["moncount"],
    }
    list2.append(div)
    list3.append(div)
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
        del_count = del_count +1
    del list2[del_count]
    div = {
        "title":title,
        "number":count,
    }
    db.database.mon_sort.insert(div)
    count = count+1