
# coding: utf-8

# In[6]:


from bs4 import BeautifulSoup 
import scrapy
from selenium import webdriver
import time 
import lxml 
import sys 
from scrapy.selector import Selector 
import requests 
import shutil 
import sqlite3 as lite
import os
import json
import re
import string
import datetime
import numpy as np
def strclear(text,newsign =''):
        signtext = string.punctuation + newsign
        signrepl = '@'*len(signtext)
        signtable = str.maketrans(signtext,signrepl)
        return text.translate(signtable).replace('@','')
class parseRuten(scrapy.Spider):
    name = 'parseRuten'
    domain = ['http://www.ruten.com.tw/']
    start_urls = [
         'http://class.ruten.com.tw/category/sub00.php?c=00210001&p=', #手機空機 
         'http://class.ruten.com.tw/category/sub00.php?c=00110002&p=', #筆記電腦
         'http://class.ruten.com.tw/category/sub00.php?c=00110013&p=' #平板
    ]
    sql = "insert into old(title,price,website,date,flag) values(?,?,?,?,?)"
    sqlnew = "insert into new(title,price,website,date,flag) values(?,?,?,?,?)"
    urlclass = "new"
    databaseclass = "old"
    urlclasscount = 0
    urlpage = 0
    
    db_title =[]
    db_price = []
    db_web = []
    db_date = []
    db_flag = []
    db_intitle =[]
    db_inprice = []
    db_inweb = []
    db_indate = []
    db_inflag = []
    db_incheck = []
    flag = 0
    count =0
    Header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    def __init__(self):
        self.conn = lite.connect('cellphone.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag);')
        self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
        self.conn.close()
        #print("init cellphone")
        self.conn = lite.connect('notebook.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag);')
        self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
        self.conn.close()
        #print("init notebook")
        self.conn = lite.connect('pad.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag);')
        self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
        self.conn.close()
        print("init")
        self.urlclasscount = 0
    def initFunc(self):
        try:
            if(self.urlclasscount ==1):
                self.conn = lite.connect('cellphone.sqlite')
                self.cur = self.conn.cursor()                       
                self.cur.execute("SELECT * FROM new where flag = '1';")
                self.urlclasscount = 1
            elif(self.urlclasscount==2):
                self.conn = lite.connect('notebook.sqlite')
                self.cur = self.conn.cursor()                       
                self.cur.execute("SELECT * FROM new where flag = '1';")
                self.urlclasscount = 2
            elif(self.urlclasscount==3):
                self.conn = lite.connect('pad.sqlite')
                self.cur = self.conn.cursor()                       
                self.cur.execute("SELECT * FROM new where flag = '1';")
                self.urlclasscount = 3
            results = []
            results = self.cur.fetchall()
            #print(results)
            print("select item from new success")
            if(len(results)!=0):
                print("exist")
                #print(self.urlclass[self.urlclasscount-1])
                self.cur.execute("delete FROM new where flag ='1';")              #拿出之後把new裡面的商品都刪掉
                self.conn.commit()
                print("delete current new success")
                for i in range(len(results)):                       #將商品放進cellphone
                    self.cur.execute(self.sql,(results[i][0],results[i][1],results[i][2],results[i][3],'1')) 
                    self.conn.commit()
                print("success insert data from new to cellphone")
                self.conn.close() 
            if(self.urlclasscount ==1):
                self.conn = lite.connect('cellphone.sqlite')             #檢查new裡面有無商品，若有就拿出
                self.cur = self.conn.cursor()                       
                self.cur.execute("SELECT * FROM old where flag='1';")
                self.urlclasscount = 1
                #self.conn.close()
            elif(self.urlclasscount==2):
                self.conn = lite.connect('notebook.sqlite')
                self.cur = self.conn.cursor()                       
                self.cur.execute("SELECT * FROM old where flag='1';")
                self.urlclasscount = 2
                #self.conn.close()
            elif(self.urlclasscount==3):
                self.conn = lite.connect('pad.sqlite')
                self.cur = self.conn.cursor()                       
                self.cur.execute("SELECT * FROM old where flag='1';")
                self.urlclasscount = 3
            nowProd = self.cur.fetchall()
            #print(len(nowProd))
            for product in nowProd:
                self.db_intitle.append(product[0])                 
                self.db_inprice.append(product[1])                 
                self.db_inweb.append(product[2])                 
                self.db_indate.append(product[3])
                self.db_incheck.append(0)
            #print(len(self.db_inweb))                                #目前資料總數
            #print("success select all data from database")
        except:             
            print("Error: can't take product from database")         
        self.conn.close()         
        print("database close") 
    def parse(self):
        chrome_path = "D:\chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_path) #chromedriver  
        for start in self.start_urls:
            self.urlclasscount += 1
            #print(self.urlclasscount)
            parseRuten.initFunc(self)
            for page in range(0,1):#how many pages want spider                 
                url = start + str(page+1)                 
                self.driver.get(url)   
                sp = BeautifulSoup(self.driver.page_source, "lxml")
                date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
                for items in sp.select('.prod_name'):
                    self.db_web.append(items.select('a')[0]['href'])
                    self.db_title.append(items.select('a')[0])
                for items in sp.select('.price_box'):
                    self.db_price.append(items.select('.price'))
                for i in range(len(self.db_title)):
                    web_temp = self.db_web[i]
                    title_temp = self.db_title[i]
                    price_temp = self.db_price[i]
                    pric = "'" + "','".join(map(str, price_temp)) + "'"
                    title = "'" + "','".join(map(str, title_temp)) + "'"     #title
                    #website = "'" + "','".join(map(str, web_temp)) + "'"     #website
                    website = web_temp
                    m = re.search('\'<span class="price">(.*?)</span>\'',pric)
                    price = m.group(1)
                    price = int(strclear(price,','))                         #price
                    if(len(self.db_inweb)==0):                            #第一次執行，cellphone裡面沒任何資料
                        if(self.urlclasscount==1):
                            self.conn = lite.connect('cellphone.sqlite')
                        elif(self.urlclasscount==2):
                            self.conn = lite.connect('notebook.sqlite')
                        elif(self.urlclasscount==3):
                            self.conn = lite.connect('pad.sqlite')
                        self.cur = self.conn.cursor()
                        self.cur.execute(self.sqlnew,(title,price,website,date,'1'))
                        self.conn.commit()
                    elif(len(self.db_inweb)!=0):
                        for fi in range(len(self.db_inweb)):
                            if(website == self.db_inweb[fi]):
                                self.db_incheck[fi] = 1             
                                self.count =1
                                if(price != self.db_inprice[fi]):         #同筆資料，價錢更改
                                    if(self.urlclasscount==1):
                                        self.conn = lite.connect('cellphone.sqlite')
                                        self.cur = self.conn.cursor()
                                        print(self.urlclasscount)
                                    elif(self.urlclasscount==2):
                                        self.conn = lite.connect('notebook.sqlite')
                                        self.cur = self.conn.cursor()
                                        print(self.urlclasscount)
                                    elif(self.urlclasscount==3):
                                        self.conn = lite.connect('pad.sqlite')             
                                        self.cur = self.conn.cursor()
                                        print(self.urlclasscount)
                                    self.cur.execute(self.sqlnew,(title,price,website,date,'1'))   #insert into new
                                    self.cur.execute("delete from old where website = '%s' " %website)#delete from cellphone
                                    print("the item %s price has been changed" % self.db_intitle[fi])
                                    self.conn.commit()
                        if(self.count ==0):
                            if(self.urlclasscount==1):
                                self.conn = lite.connect('cellphone.sqlite')
                                self.cur = self.conn.cursor()
                            elif(self.urlclasscount==2):
                                self.conn = lite.connect('notebook.sqlite')
                                self.cur = self.conn.cursor()
                            elif(self.urlclasscount==3):
                                self.conn = lite.connect('pad.sqlite')
                                self.cur = self.conn.cursor()
                            self.cur.execute(self.sqlnew,(title,price,website,date,'1'))
                            
                            self.conn.commit()
                            self.count = 0
                        else:
                            self.count = 0
                self.db_title.clear()                                    #初始化暫存
                self.db_price.clear()
                self.db_web.clear()
                self.db_date.clear()
                self.db_flag.clear()
            self.conn.close()
            print('db close')
            if(len(self.db_inweb)!=0):            
                for i in range(len(self.db_inweb)):                                        #若資料庫資料完全沒被比對到，就刪除那筆資料
                    if(self.db_incheck[i]==0):
                        if(self.urlclasscount==1):
                            self.conn = lite.connect('cellphone.sqlite')
                            self.cur = self.conn.cursor()
                        elif(self.urlclasscount==2):
                            self.conn = lite.connect('notebook.sqlite')
                            self.cur = self.conn.cursor()
                        elif(self.urlclasscount==3):
                            self.conn = lite.connect('pad.sqlite')
                            self.cur = self.conn.cursor()      
                        #print(self.databaseclass[self.urlclasscount-1])
                        self.cur.execute("delete from old where website = '%s' " %self.db_inweb[i])
                        self.conn.commit()
                        #print("the item %s was not exist" % self.db_intitle[i])
            self.db_intitle.clear()
            self.db_inprice.clear()
            self.db_inweb.clear()
            self.db_indate.clear()
            self.db_inflag.clear()
            self.db_incheck.clear()
            self.conn.close()
            print("end of program")
        self.driver.close()

