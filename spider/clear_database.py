#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import re

db = MongoClient('localhost', 27017)
temp1 = db.database.book.find()
for book1 in temp1:
    book = book1["title"]
    flag = book1["flag"].strip()
    pattern = re.compile(r"(\S\S)")
    flag = pattern.findall(flag)[0]
    if u"二次" in flag:
        flag = u"二次元"
    book_temp = book1["title"].strip()
    db.database.book.update({"title":book},{"$set":{"flag":flag}})