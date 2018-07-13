import sqlite3
import pymysql
import re
import pandas as pd
#import webbrowser
#from selenium import webdriver
import string
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from parseWeb import parseRute,parseRaku,parsePc

def check_request(results):
    if(results):
        for r in results:
            newwant = check_newtable(r)
            if r[7]==0:
                oldwant = check_oldtable(r)
                newwant = newwant.append(oldwant)
            if(len(newwant) == 0):
                print("request no fit")
            else:
                title,price,website = checkProd(r[3],r[4],newwant)
                if len(title)!=0:
                    context = ""
                    for j in range(len(title)):
                        url = website[j]
                        ti = title[j]
                        context+=str(j+1) + ti + " \t\t (" + url + ") \n"
                    sendemail(r[2],r[1] + "您好" + ", \n\n" + "以下是幫您找到的商品。\n" + context)
                else:
                    print("not found")
        return 1
    else:
        return 0
        
def check_database(DB_name):
    print("GG")
    
#比對newtable    
def check_newtable(r):
    if r[6] == 1:
        DB_name = "pad.sqlite"
    elif r[6] == 2:
        DB_name = "cellphone.sqlite"
    elif r[6] == 3:
        DB_name = "notebook.sqlite"
    dfnew = []
    topPrice = r[4] + r[4]/5
    lowPrice = r[4] - r[4]/5
    conn = sqlite3.connect(DB_name)
    dfnew = pd.read_sql_query("SELECT * FROM new WHERE price < %d and price > %d" %(topPrice,lowPrice), conn)
    conn.close()
    return dfnew
#比對oldtable
def check_oldtable(r):
    if r[6] == 1:
        DB_name = "pad.sqlite"
    elif r[6] == 2:
        DB_name = "cellphone.sqlite"
    elif r[6] == 3:
        DB_name = "notebook.sqlite"
    dfold = []
    topPrice = r[4] + r[4]/5
    lowPrice = r[4] - r[4]/5
    conn = sqlite3.connect(DB_name)
    dfold = pd.read_sql_query("SELECT * FROM old WHERE price < %d and price > %d" %(topPrice,lowPrice), conn)
    conn.close()
    return dfold
    
def checkProd(searchWord,expPrice,df):
    title = []
    price = []
    website = []
    n = 0
    base = expPrice/5                                   #價錢基準化
    for char in string.punctuation:                     #去掉字串中符號
        searchWord = searchWord.replace(char, '')
    searchWord = searchWord.replace(" ","")             #刪掉字串空白
    #print(searchWord)
    b = re.split(r'([\d+])',searchWord,maxsplit=5)
    #print(b)
    for i in range(len(df.values)):                     #查看資料庫所有資料
        for k in range(len(b)):                         #字串切割後的len
            if(b[k]!=""):                               #不看list中空白部分
                if(re.search(b[k],df.values[i][0],re.IGNORECASE)):#比對字串中符合之字串
                    n = n + 1
            else:
                n  = n + 1
        #print(n)
        if(n==len(b)):
            if(df.values[i][1] >= expPrice-base and df.values[i][1] <= expPrice+base):#字串符合比對價錢是否符合
                    title+=[df.values[i][0]]
                    price+=[df.values[i][1]]
                    website+=[df.values[i][2]]
        
        n = 0
    return title, price, website

def sendemail(sendperson,sendcontext):#sendperson要寄的email位置,sendcontext寄信內容
    try:
        #gmail信箱的資訊
        host = "smtp.gmail.com"
        port = 587
        username = "SendingRobotkk@gmail.com"
        password = "52785278"
        from_email = username
        the_msg = MIMEMultipart("alternative")
        to_list = sendperson

        the_msg['Subject'] = "親愛的用戶，找到商品囉"
        the_msg["From"] = from_email
        the_msg["To"] = sendperson

        plain_txt = sendcontext + " \nBest regards,\n"      #內文

        context = MIMEText(plain_txt, 'plain', 'utf-8')     

        the_msg.attach(context)

        # 建立SMTP連線
        email_conn = smtplib.SMTP(host,port)
        #跟Gmail Server溝通
        print(email_conn.ehlo())
        # TTLS安全認證機制
        email_conn.starttls()
        #登錄Gmail
        print(email_conn.login(username,password))
        
        #寄信
        email_conn.sendmail(from_email, to_list, the_msg.as_string())#寄信內容
        #關閉連線
        email_conn.quit()
    except:
        logging.error("Error: email sending error.")
def main():
    #---------------------爬蟲過程------------------
    logging.basicConfig(filename="project.log",format = '%(asctime)s:%(message)')
    try:
	    #爬露天
        rute = parseRute.parseRuten()
        rute.parse()
        #爬樂天
        raku = parseRaku.tablet()
        raku.start_requests()
        #爬PC
        cellphone = parsePc.crawler()
        cellphone.search_items('手機')
        time.sleep(10)
    
        notebook = parsePc.crawler()
        notebook.search_items('筆電')
        time.sleep(10)
    
        pad = parsePc.crawler()
        pad.search_items('平板')
    
        cell = parsePc.database('cellphone')
        cell.conn = sqlite3.connect(cell.db_name)
        cell.cur = cell.conn.cursor()         
        cell.insert_items(cellphone.items, 'new')
        cell.conn.close()

        note = parsePc.database('notebook')
        note.conn = sqlite3.connect(note.db_name)
        note.cur = note.conn.cursor()         
        note.insert_items(notebook.items, 'new')
        note.conn.close()

        paddd = parsePc.database('pad')
        paddd.conn = sqlite3.connect(paddd.db_name)
        paddd.cur = paddd.conn.cursor()         
        paddd.insert_items(pad.items, 'new')
        paddd.conn.close()
        print("STEP 1")
    except:
	    logging.error("Error: parsing error")
    #--------------------接收request----------------
    try:
        db = pymysql.connect(host="192.168.1.102",user="curt",passwd="curt0226",db="example")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM example.test")
        results = cursor.fetchall()
        cursor.execute("UPDATE example.test SET flag = 1") #更改request flag為1
        db.commit()
        db.close()
        print("STEP 2")
    except:
	    logging.error("Error: requests error")
    #-----------------找request相符之商品並寄信-------
    try:
        t = check_request(results)
        if t == 0:
            print("no request today")
        print("STEP 3")
    except:
	    logging.error("Error: check_request error")
if __name__ == "__main__":
    main()