#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

db = MongoClient('localhost', 27017)
div = {
    "author":"",
    "book":[],
}
list1 = db.database.book.find()
author_list = []
for item in list1:
#     if item["author"] in author_list:
#         continue
#     author_list.append(item["author"])
# count = 0
# for author in author_list:
#     count = count +1
# print count
    # if item["author"] == u"爱潜水的乌贼":
    #     print item
    if db.database.book_author.find_one({"author":item["author"]}):
        continue
    list2 = db.database.book.find({"author":item["author"]})
    for a in list2:
        book_list = []
        book_list.append(a["title"])
    div["author"] = item["author"]
    div["book"] = book_list
    db.database.book_author.insert(div)
    div = {
        "author":"",
        "book":[],
    }