
# coding: utf-8

# In[32]:


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

def cmp(a,b):
    return (a > b) - (a < b)
class tablet(scrapy.Spider):
    name = 'tablet'
    start_urls = [
        'https://www.rakuten.com.tw/category/346/?h=3&l-id=tw_display_more_60',#手機 
        'https://www.rakuten.com.tw/category/124/?h=3&l-id=tw_display_more_60', #筆電
        'https://www.rakuten.com.tw/category/7956/?h=3&l-id=tw_display_more_60' #平板  
    ]

    old_sql = "insert into old(title,price,website,date,flag) values(?,?,?,?,?)"
    new_sql = "insert into new(title,price,website,date,flag) values(?,?,?,?,?)"
    
    CLASS_SWITCH=0
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
    
    old_intitle =[]
    old_inprice = []
    old_inweb = []
    old_indate = []
    old_inflag = []
    flag = 0
    count =0
    
    old_check_exist=[]
         
    def __init__(self):
        try:
            self.conn = lite.connect('cellphone.sqlite') 
            self.cur = self.conn.cursor()
            self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag);')
            self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
            self.conn.close()         

            self.conn = lite.connect('notebook.sqlite') 
            self.cur = self.conn.cursor()
            self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag);')
            self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
            self.conn.close() 

            self.conn = lite.connect('pad.sqlite')
            self.cur = self.conn.cursor()
            self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag);')
            self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
            self.conn.close() 
            
            print("init step")
        except:
            print("can not init.")       
    
    def start_requests(self):
        for category in range(0,3):
            self.CLASS_SWITCH=category
            try:            
                #開new資料庫
                if(self.CLASS_SWITCH==0):
                    self.conn = lite.connect('cellphone.sqlite') 
                elif(self.CLASS_SWITCH==1):
                    self.conn = lite.connect('notebook.sqlite') 
                elif(self.CLASS_SWITCH==2):
                    self.conn = lite.connect('pad.sqlite') 
                self.cur = self.conn.cursor()
                self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag integer);')
                self.cur.execute("SELECT * FROM new where flag = '2';")
                
                results = []
                results = self.cur.fetchall()
                #print(results)
                print("select item from new success")
                if(len(results)!=0):
                    print("exist")
                    #print(self.urlclass[self.urlclasscount-1])
                    self.cur.execute("delete FROM new where flag ='2';")              #拿出之後把new裡面的商品都刪掉
                    self.conn.commit()
                    print("delete current new success")
                for i in range(len(results)):                       #將商品放進cellphone
                    self.cur.execute(self.old_sql,(results[i][0],results[i][1],results[i][2],results[i][3],'2')) 
                    self.conn.commit()
                print("success insert data from new to cellphone")
                self.conn.close()       
                #print("new table database close")

                #抓old資料庫的資料
                if(self.CLASS_SWITCH==0):
                    self.conn = lite.connect('cellphone.sqlite') 
                elif(self.CLASS_SWITCH==1):
                    self.conn = lite.connect('notebook.sqlite') 
                elif(self.CLASS_SWITCH==2):
                    self.conn = lite.connect('pad.sqlite')             
                self.cur = self.conn.cursor() 
                self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag integer);')
                self.cur.execute("SELECT * FROM old where flag='2';")
                
                results = self.cur.fetchall()#抓資料庫的資料
                #print(results)
                for record in results:
                    self.old_intitle.append(record[0])     
                    self.old_inprice.append(record[1])                 
                    self.old_inweb.append(record[2])                 
                    self.old_indate.append(record[3])
                    self.old_inflag.append(record[4])
                    self.old_check_exist.append(0)
                print("old table success") 
                self.conn.close()         
                #print("old table database close")
            except:             
                print("can't connect sqlite")         
            #chrome的路徑
            chrome_path = "D:\\chromedriver.exe"
            self.driver = webdriver.Chrome(chrome_path)         
            self.driver.get(self.start_urls[self.CLASS_SWITCH])
            #開始爬蟲
            tablet.parse(self)
            self.CLASS_SWITCH+=1
    #爬蟲    
    def parse(self):
        temp=0
        #算有幾頁
        sp1 = BeautifulSoup(self.driver.page_source, "lxml")
        for items in sp1.select('.b-tabs-utility'):
                str1=items.text.split('，')
                str1=str1[1].split('共 ')
                str1=str1[1].split(' 筆')
                page_count=int(str1[0])/60    
                temp=int(str1[0])%60
                if(int(str1[0])%60!=0):
                    page_count=int(int(str1[0])/60+1)
                else:
                    page_count=int(int(str1[0])/60)
        str1.clear()
        #print(len(self.old_check_exist))
        #print(len(self.old_inweb))
        for page in range(0,2):#爬幾頁 頁數改page_count
            sp = BeautifulSoup(self.driver.page_source, "lxml")
            date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") 
            
            for items in sp.select('.b-tabs-utility'):
                str1=items.text.split('，')
                str1=str1[1].split('共 ')
                str1=str1[1].split(' 筆')
                temp=int(str1[0])%60
                if(int(str1[0])%60!=0):
                    page_count=int(int(str1[0])/60+1)
                else:
                    page_count=int(int(str1[0])/60)
            str1.clear()
            
            
            #抓取網址和標題
            for items in sp.select('.product-name'):
                self.db_web.append(items['href'])
                self.db_title.append(items.text)             
            #抓取價錢
            for items in sp.select('.product-price'):
                #分割'元'和'-'
                a=items.text
                a=a.split('元',1)
                a=a[0].split('-',1)
                self.db_price.append(a[0])
            
            if(page!=page_count-1):
                page_commodity=60
            else:
                page_commodity=temp
            #print(page_commodity)
            #一頁商品數量為60
            for i in range(0,page_commodity):
                title_temp = self.db_title[i]
                price_temp = self.db_price[i].replace(",", "")
                web_temp = self.db_web[i]                        
                title = "'" + title_temp + "'"              #標題
                price = price_temp                          #價錢
                website = " https://www.rakuten.com.tw" + web_temp                          #網址
                    
                if(len(self.old_inweb)==0):#資料庫沒有東西，加入第一個商品
                    if(self.CLASS_SWITCH==0):
                        self.conn = lite.connect('cellphone.sqlite') 
                    elif(self.CLASS_SWITCH==1):
                        self.conn = lite.connect('notebook.sqlite') 
                    elif(self.CLASS_SWITCH==2):
                        self.conn = lite.connect('pad.sqlite') 
                    self.cur = self.conn.cursor()
                    self.cur.execute(self.new_sql,(title,price,website,date,'2'))
                    #self.cur.execute(self.old_sql,(title,price,website,date,'2'))
                    self.conn.commit()
                    self.conn.close()
                elif(len(self.old_inweb)!=0):
                    for fi in range(len(self.old_inweb)):#抓資料庫的網址來比對新資料
                        if(website == self.old_inweb[fi]):#和舊商品網址一樣  改
                            self.count =1
                            self.old_check_exist[fi]=1
                            if(int(price)!=self.old_inprice[fi]):#不一樣價格   
                                if(self.CLASS_SWITCH==0):
                                    self.conn = lite.connect('cellphone.sqlite') 
                                elif(self.CLASS_SWITCH==1):
                                    self.conn = lite.connect('notebook.sqlite') 
                                elif(self.CLASS_SWITCH==2):
                                    self.conn = lite.connect('pad.sqlite')
                                self.cur = self.conn.cursor()
                                self.cur.execute(self.new_sql,(title,price,website,date,'2'))#將改動價格的商品加到new db
                                self.cur.execute("delete from old where website = '%s' " %website)
                                self.conn.commit()                                   
                                print("change price success.") 
                    if(self.count ==0):#新增新的商品
                        if(self.CLASS_SWITCH==0):
                            self.conn = lite.connect('cellphone.sqlite') 
                        elif(self.CLASS_SWITCH==1):
                            self.conn = lite.connect('notebook.sqlite') 
                        elif(self.CLASS_SWITCH==2):
                            self.conn = lite.connect('pad.sqlite')
                        self.cur = self.conn.cursor()
                        self.cur.execute(self.new_sql,(title,price,website,date,'2'))
                        #self.cur.execute(self.old_sql,(title,price,website,date,'2'))
                        self.conn.commit()
                        self.conn.close()
                        self.count = 0
                    else:
                        self.count = 0
                           
            self.db_title.clear()
            self.db_price.clear()
            self.db_web.clear()
            self.db_date.clear()                
            self.db_flag.clear()           
            
            #print('db update')
            #換頁
            if(page!=page_count-1):
                #print(page)
                self.driver.find_element_by_xpath("//a[contains(text(),'»')]").click()    
            else:
                break;
        
        if(self.CLASS_SWITCH==0):
            self.conn = lite.connect('cellphone.sqlite') 
        elif(self.CLASS_SWITCH==1):
            self.conn = lite.connect('notebook.sqlite') 
        elif(self.CLASS_SWITCH==2):
            self.conn = lite.connect('pad.sqlite') 
        self.cur = self.conn.cursor()
        
        #print(page_count)
        #print(len(self.old_inflag))
        #print(len(self.old_check_exist))
        #print(len(self.old_inweb))
        if(len(self.old_check_exist)!=0):#資料庫沒有東西，加入第一個商品
            for fi in range(len(self.old_check_exist)):#刪除下架商品
                if(self.old_check_exist[fi]==0):
                    self.cur.execute("DELETE from old where website = '%s' " %(self.old_inweb[fi])) 
                    self.conn.commit() 
        
        self.old_intitle.clear()
        self.old_inprice.clear()
        self.old_inweb.clear()
        self.old_indate.clear()
        self.old_inflag.clear()
        self.old_check_exist.clear()  
        self.conn.close()
        #print('db close')
        self.driver.quit()

    def db_closed(self):   
        self.conn.close()

