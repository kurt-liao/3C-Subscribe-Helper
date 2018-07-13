
# coding: utf-8

# In[4]:


import time
import datetime
import sqlite3
import requests
import json
from bs4 import BeautifulSoup

# ID = []
# items = []
# prices = []
# urls = []
# main = 'http://24h.pchome.com.tw/prod/'
# commodity = '筆電'
# max_page = 10
# for page in range(1,max_page):
#     GGBB = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + commodity + '&page=' + str(page) + '&sort=rnk/dc'
#     #resp = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E7%AD%86%E9%9B%BB&page=' + str(page) + '&sort=rnk/dc'
#     res = requests.get(GGBB)
#     soup = BeautifulSoup(res.text, "html.parser")
#     data = json.loads(res.text)
#     now =  datetime.datetime.now()
#     for item in data['prods']:
#         itemdata = []
#         itemdata.append(item['name'])  
#         itemdata.append(item['price'])
#         url = main+item['Id']
#         itemdata.append(url)
#         itemdata.append('%s/%s/%s %s:%s:%s' % (now.year,now.month,now.day,now.hour, now.minute, now.second))
#         itemdata.append('0')
#         items.append(itemdata) 


# In[29]:


class database():
    #初始化DB,name是創建資料庫的名字
    def __init__(self, name):
        try:      
            self.db_name = name + '.sqlite'
            self.conn = sqlite3.connect(self.db_name)
            print("%s database create success" % self.db_name)   
            print("Database connected")
            self.cur = self.conn.cursor()             
            self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
            self.cur.execute('create table if not exists old(title text,price integer,website text,date timestamp,flag);')    
            self.conn.close()
#           print("database connect close")
        except sqlite3.Error as e:
            print("Database error: %s" % e)
        except Exception as e:
            print("Exception in _query: %s" % e)
    #插入資料,參數是二維list跟table名字
    def insert_items(self, items, table): 
        self.cur.execute( "select * from new where flag = '3';")
        data = self.cur.fetchall()
        #print(data)
        insert = "INSERT INTO old VALUES (?, ?, ?, ?, ?)"
        self.cur.executemany(insert, data)
        self.cur.execute("delete FROM new where flag = '3';")
        self.conn.commit()
        self.cur.execute('create table if not exists new(title text,price integer,website text,date timestamp,flag);')
            
        self.check_repeat(items, 'old')
        insert = "INSERT INTO new VALUES (?, ?, ?, ?, ?)"
        self.cur.executemany(insert, items)
        self.conn.commit()
        print("Data insert success")
    #檢查新資料與舊資料有沒有重複，把重複的從新資料刪掉
    def check_repeat(self, items, table_name): 
        #sql = 'select * from '+ table_name + ' order by price'
        sql = 'select * from ' + table_name + " where flag = '3';"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        #print(self.cur.fetchall())
        for old_item in data:
            for new_item in items:
                if(old_item[2] == new_item[2]):
                    if(old_item[1] == new_item[1]):
                        self.conn.execute("UPDATE old set date = ? where website = ?",(new_item[3], new_item[2]))
                        items.remove(new_item)
                    else:
                        self.conn.execute("DELETE from ? where website = ?;",(table_name, old_item[2]))
        #print(items)
    def show_data(self, table_name):
        sql = 'select * from '+ table_name + ' order by price'
        self.cur.execute(sql)
        print(self.cur.fetchall())
    def delete (self):
        self.cur.execute('DROP TABLE new')
        self.cur.execute('DROP TABLE old')
        


# In[38]:


class crawler():
    def __init__(self):
        #網站網址
        self.main = ''
        #要搜尋的商品
        self.commodity = ''
        #物品二維LIST
        self.items = []
        self.count = 0
    #將商品爬下並放到items
    def search_items(self, commodity):
        main = 'http://24h.pchome.com.tw/prod/'
        max_page = 10
        mini_page = 1
        for page in range(mini_page,max_page):
            time.sleep(3)
            GGBB = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=' + commodity + '&page=' + str(page) + '&sort=rnk/dc'
            #resp = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E7%AD%86%E9%9B%BB&page=' + str(page) + '&sort=rnk/dc'
            res = requests.get(GGBB)
            soup = BeautifulSoup(res.text, "html.parser")
            #print(res.text)                
            try:
                data = json.loads(res.text)
                now =  datetime.datetime.now()
                for item in data['prods']:
                    itemdata = []
                    itemdata.append(item['name'])  
                    itemdata.append(item['price'])
                    url = main+item['Id']
                    itemdata.append(url)
                    itemdata.append('%s/%s/%s %s:%s:%s' % (now.year,now.month,now.day,now.hour, now.minute, now.second))
                    itemdata.append('3')
                    self.items.append(itemdata) 
                    self.count = self.count + 1
            except :
                pass
        print("%d items searched"%self.count)
    def show_items (self):
        print(self.items)

