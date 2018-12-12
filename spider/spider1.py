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

skip_list = [
    u'玄幻',
    u"奇幻",
    u"武侠",
    u"仙侠",
    u"都市",
    u"现实",
    u"军事",
    u"历史",
]


__author__ = "chenshengyuan"

class spider():

    def __init__(self):
        self.origin_url = "http://www.qidian.com"
        self.encoding = "utf-8"
        self.sum = 0
        self.page = 0
        self.begin_url = "https:"
        self.db = MongoClient('localhost', 27017)
        self.type_list = []
        self.book_list = []

    def start_selenium(self):
        self.browser = webdriver.Chrome()

    def initial_list(self):
        self.browser.get("http://www.qidian.com/all")
        html = self.browser.page_source
        soup = BeautifulSoup(html,'lxml')
        temp1 = soup.select('ul.row-1 > li')
        temp2 = soup.select('ul.row-2 > li')
        temp3 = soup.select('ul.row-3 > li')
        # temp4 = []
        # temp4.append(temp2[-1])
        temp = temp1+ temp2 + temp3
        # temp = temp4 + temp3
        if temp is None:
            print "error"
        for li in temp:
            a = li.select('a')
            if a[0].get_text() == u"全部":
                continue
            href = a[0].get('href')
            if href is None:
                print "error"
            url = self.begin_url + href
            self.type_list.append(url)

    def get_list(self,url):
        self.browser.get(url)

    def get_pagesource(self):
        return self.browser.page_source

    def extract_list(self,html1):
        soup = BeautifulSoup(html1,'html5lib')
        type_temp = soup.select('div.selected > p > a')
        if type_temp is None:
            return
        self.book_type = remove_html_tag(type_temp[0].get_text())
        if self.book_type in skip_list:
            return u"skip"
        temp1 = soup.select('div.book-mid-info > h4 > a')
        if temp1 is None:
            return
        for a in temp1:
            href = a.get('href')
            if href is None:
                continue
            url = "https:"+href
            self.book_list.append(url)

    def change_page(self,pagenumber):
        try:
            input = self.browser.find_element_by_css_selector('#PAGINATION-INPUT')
            submit = self.browser.find_element_by_css_selector('#PAGINATION-BUTTON')
        except Exception as e:
            return e.message
        try:
            input.clear()
            input.send_keys(pagenumber)
            submit.click()
        except:
            clicksubmit = self.browser.find_element_by_css_selector('body > div:nth-child(13) > div')
            clicksubmit.click()
        try:
            input.clear()
            input.send_keys(pagenumber)
            submit.click()
        except:
            pass

    def get_detail(self,url):
        self.browser.get(url)
        sleep(2)
        return self.browser.page_source

    def extract_detail(self,html,url):
        update_flag = -1
        if u"连载" in html:
            update_flag = 1
        elif u"完结" in html:
            update_flag = 0
        if update_flag == -1:
            return "update_flag get failed"
        soup = BeautifulSoup(html,'html5lib')
        title_temp = soup.select('div.book-info > h1 > em')
        if title_temp is None:
            return "title get failed"
        image_temp = soup.select('#bookImg > img')
        if image_temp is None:
            return "get image falied"
        image = remove_html_tag(image_temp[0].get('src'))
        title = remove_html_tag(title_temp[0].get_text())
        author_temp = soup.select('div.book-info > h1 > span > a.writer')
        if author_temp is None:
            return "author get failed"
        author = remove_html_tag(author_temp[0].get_text())
        author_url = u"https:"+remove_html_tag(author_temp[0].get('href'))
        brief_temp = soup.select('div.book-intro > p')
        if brief_temp is None:
            brief = ""
        else:
            brief = remove_html_tag(brief_temp[0].get_text())
        test = soup.select('#readBtn')
        if test is None:
            return "word count get failed"
        href = "https:"+remove_html_tag(test[0].get('href'))
        moncount_temp = soup.select('#monthCount')
        if moncount_temp is None:
            return "moncount get failed"
        try:
            moncount = remove_html_tag(moncount_temp[0].get_text())
        except:
            moncount = "0"
        reccount_temp = soup.select('#recCount')
        if reccount_temp is None:
            return "reccount get failed"
        reccount = remove_html_tag(reccount_temp[0].get_text())
        bookscore_temp = soup.select('#j_bookScore')
        if bookscore_temp is None:
            return "bookscore get failed"
        bookscore = remove_html_tag(bookscore_temp[0].get_text())
        usercount_temp = soup.select('#j_userCount > span')
        if usercount_temp is None:
            return "usercoount get failed"
        try:
            usercount = remove_html_tag(usercount_temp[0].get_text())
        except:
            usercount = 0
        rewardnum_temp = soup.select('#rewardNum')
        if rewardnum_temp is None:
            return "bookscore get failed"
        try:
            rewardnum = remove_html_tag(rewardnum_temp[0].get_text())
        except:
            rewardnum = 0
        self.browser.get(href)
        html1 = self.browser.page_source
        if u'万' not in html1:
            self.browser.get(href)
            html1 = self.browser.page_source
        soup1 = BeautifulSoup(html1,'html5lib')
        wordcount_temp = soup1.select('div.info-list.cf > ul > li:nth-of-type(3) > p > em')
        wordcount = remove_html_tag(wordcount_temp[0].get_text())+u"万"
        book = {
            "title": title,
            "image":image,
            "brief":brief,
            "wordcount":wordcount,
            "author":author,
            "author_url":author_url,
            "reccount":reccount,
            "moncount":moncount,
            "bookscore":bookscore,
            "rewardnum":rewardnum,
            "usercount":usercount,
            "updateflag":update_flag,
            "flag":self.book_type,
            "url":url
        }
        if self.db.database.book.find_one({"title": title}):
            return
        self.db.database.book.insert(book)

    def run(self):
        self.start_selenium()
        self.initial_list()
        for url in self.type_list:
            self.get_list(url)
            for i in range(2,11):
                html = self.get_pagesource()
                flag = self.extract_list(html)
                self.change_page(i)
            if flag == u"skip":
                continue
            for book_url in self.book_list:
                html = self.get_detail(book_url)
                self.extract_detail(html,book_url)
            self.book_list = []




if __name__ == '__main__':
    spider = spider()
    spider.run()
