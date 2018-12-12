#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from tools.html_cleaner import remove_html_tag
from pymongo import MongoClient
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class getauthor():
    def __init__(self):
        self.db = MongoClient('localhost', 27017)
        self.begin_url = "https:"
        self.author_urllist = []

    def start_selenium(self):
        self.browser = webdriver.Chrome()

    def get_author_list(self):
        dbres = self.db.database.book.find()
        for book in dbres:
            self.author_urllist.append(book["author_url"])

    def get_author_page(self, url):
        self.browser.get(url)

    def extract_author(self, html,url):
        soup = BeautifulSoup(html, 'html5lib')
        img_temp = soup.select('div.header-avatar > img')
        if img_temp == []:
            return u"exist"
        if img_temp is None:
            return "img_temp falied"
        img_src = remove_html_tag(img_temp[0].get('src'))
        name_temp = soup.select('div.header-msg > h3')
        if name_temp is None:
            return "name failed"
        name = remove_html_tag(name_temp[0].get_text()).strip()
        pattern = re.compile(r'(\S+)level')
        temp = pattern.findall(name)
        if temp is None:
            name = name
        else:
            name = temp[0]
        tag_temp = soup.select('div.header-avatar > span')
        if tag_temp is None:
            return "tag_temp failed"
        try:
            author_tag = remove_html_tag(tag_temp[0].get_text()).strip()
        except:
            author_tag = u"无"
        if author_tag == u"" or author_tag == u" ":
            author_tag = u"无"
        brief_temp = soup.select('div.header-msg-desc')
        if brief_temp is None:
            return "brief failed"
        try:
            brief = remove_html_tag(brief_temp[0].get_text()).strip()
        except:
            brief = u"无"
        if brief == u"" or brief == u" ":
            brief = u"无"
        count_temp = soup.select('div.header-msg-data > span > strong')
        if len(count_temp) != 3:
            return "count_temp failed"
        book_count = remove_html_tag(count_temp[0].get_text()).strip()
        word_count = remove_html_tag(count_temp[1].get_text()).strip()
        day_count = remove_html_tag(count_temp[2].get_text()).strip()
        author_div = {
            "author":name.strip(),
            "img":img_src,
            "tag":author_tag.strip(),
            "brief":brief.strip(),
            "total_book":book_count.strip(),
            "total_word":word_count.strip()+u"万",
            "total_day":day_count.strip()+u"天",
            "url":url,
        }
        if self.db.database.author.find_one({"author":author_div["author"]}):
            return u"exist"
        self.db.database.author.insert(author_div)

    def run(self):
        self.start_selenium()
        self.get_author_list()
        for url in self.author_urllist:
            self.get_author_page(url)
            html = self.browser.page_source
            flag = self.extract_author(html,url)
            if flag == u"exist":
                continue

if __name__ == '__main__':
    spider = getauthor()
    spider.run()