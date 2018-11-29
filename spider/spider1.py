#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from tools.html_cleaner import remove_html_tag
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


__author__ = "chenshengyuan"

class spider():

    def __init__(self):
        self.origin_url = "http://www.qidian.com"
        self.encoding = "utf-8"
        self.sum = 0
        self.page = 0
        self.begin_url = "https:"
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
        temp = temp1 +temp2 + temp3
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
        return self.browser.page_source

    def extract_list(self,html1):
        soup = BeautifulSoup(html1,'html5lib')
        type_temp = soup.select('div.selected > p > a')
        if type_temp is None:
            return
        self.book_type = remove_html_tag(type_temp[0].get_text())
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
            # input = EC.presence_of_element_located((By.CSS_SELECTOR,'#PAGINATION-INPUT'))
            # submit = EC.element_to_be_clickable((By.CSS_SELECTOR, '#PAGINATION-BUTTON'))
            input = self.browser.find_element_by_css_selector('#PAGINATION-INPUT')
            submit = self.browser.find_element_by_css_selector('#PAGINATION-BUTTON')
        except Exception as e:
            return e.message
        input.click()
        input.clear()
        input.send_keys(pagenumber)
        submit.click()

    def get_detail(self,url):
        self.browser.get(url)
        return self.browser.page_source

    def extract_detail(self,html):
        html.encode(self.encoding)
        print html
        soup = BeautifulSoup(html,'html5lib')
        print soup
        title_temp = soup.select('div.book-info > h1 > em')
        if title_temp is None:
            return "title get failed"
        title = remove_html_tag(title_temp[0].get_text())
        author_temp = soup.select('div.book-info > h1 > span > a.writer')
        if author_temp is None:
            return "author get failed"
        author = remove_html_tag(author_temp[0].get_text())
        brief_temp = soup.select('p.intro')
        if brief_temp is None:
            brief = ""
        else:
            brief = remove_html_tag(brief_temp[0].get_text())
        count_temp = soup.select('div.book-info > p > em > span')
        if count_temp is None or len(count_temp) != 3:
            return "get count failed"
        word_count = remove_html_tag(count_temp[0].get_text())
        click_count = remove_html_tag(count_temp[1].get_text())
        recommend_count = remove_html_tag(count_temp[2].get_text())

    def run(self):
        self.start_selenium()
        self.initial_list()
        for url in self.type_list:
            for i in range(2,3):
                html = self.get_list(url)
                self.extract_list(html)
                self.change_page(i)
            for book_url in self.book_list:
                html = self.get_detail(book_url)
                self.extract_detail(html)
            self.book_list = []




if __name__ == '__main__':
    spider = spider()
    spider.run()
