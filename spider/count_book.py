#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

db = MongoClient('localhost', 27017)

list1 = db.database.book.find()
tag_list = []
for a in list1:
    if a["flag"] in tag_list:
        continue
    tag_list.append(a["flag"])
div = {}
for tag in tag_list:
    list2 = db.database.book.find({"flag":tag})
    count = 0
    for a in list2:
        count = count+1
    div[tag] = count
db.database.type_count.insert(div)
