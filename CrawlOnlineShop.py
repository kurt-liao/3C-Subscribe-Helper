import re
import time
import sched
import string
import logging
import pymysql
import smtplib
import datetime
import threading
import CrawlFunc
import webbrowser
import sqlite3 as lite
from datetime import datetime
from selenium import webdriver
from line_bot import ConvertData
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from parseWeb import parseRute,parseRaku,parsePc
def main():
	def job(num):
		if num == 0:
			rute = parseRute.parseRuten()
			rute.parse()
		elif num == 1:
			raku = parseRaku.tablet()
			raku.start_requests()
			pass
		elif num == 2:
			cellphone = parsePc.crawler()
			cellphone.search_items('手機')
			time.sleep(5)
			notebook = parsePc.crawler()
			notebook.search_items('筆電')
			time.sleep(5)
			pad = parsePc.crawler()
			pad.search_items('平板')
			cell = parsePc.database('cellphone')
			cell.conn = lite.connect(cell.db_name)
			cell.cur = cell.conn.cursor()         
			cell.insert_items(cellphone.items, 'new')
			cell.conn.close()
			note = parsePc.database('notebook')
			note.conn = lite.connect(note.db_name)
			note.cur = note.conn.cursor()         
			note.insert_items(notebook.items, 'new')
			note.conn.close()
			paddd = parsePc.database('pad')
			paddd.conn = lite.connect(paddd.db_name)
			paddd.cur = paddd.conn.cursor()         
			paddd.insert_items(pad.items, 'new')
			paddd.conn.close()
	def func():
		try:
			t1 = threading.Thread(target=job,args = (0,),name='test1')
			t2 = threading.Thread(target=job,args = (1,),name='test2')
			t3 = threading.Thread(target=job,args = (2,),name='test3')
			#thread 沒被 kill，所以用同一 thread 工作
			if t1.isAlive() is False:
				t1 = threading.Thread(target=job,args = (0,),name='test1')
				t1.start()
				
			if t2.isAlive() is False:
				t2 = threading.Thread(target=job,args = (1,),name='test2')
				t2.start()
				
			if t3.isAlive() is False:
				t3 = threading.Thread(target=job,args = (2,),name='test3')
				t3.start()
			#join確定所有 thread 都執行完，再繼續主執行緒
			t1.join()
			t2.join()
			t3.join()
		except:
			logging.error("Error: parse error")
		#-----------------連接 Database------------------
		try:
			db = pymysql.connect(host="140.118.155.126",user="test",passwd="123",db="user_infor")
			cursor = db.cursor()
			cursor.execute("SELECT * FROM user_infor.searchtable")   
			results = cursor.fetchall()
			cursor.execute("delete From user_infor.searchtable where dueTime = DATE(NOW());")
			db.commit()
			db.close()
			print("STEP 2")
		except:
			logging.error("Error: mysql connected error")
		#-----------找request相符之商品並寄信------------
		try:
			t = CrawlFunc.check_request(results)
			if t ==0:
				print("no request today")
			print("STEP 3")
		except:
			logging.error("Error: check_request error")
		timer = threading.Timer(180, func) #每3分鐘執行一次
		timer.start()
	def getMysql():
		conn = lite.connect('./Database/mysqlDB.sqlite') 
		cur = conn.cursor()
		cur.execute("SELECT * FROM subDB")
		db = pymysql.connect(host="140.118.155.126",user="test",passwd="123",db="user_infor") #ip要改
		cursor = db.cursor()
		cursor.execute("SELECT * FROM user_infor.searchtable")
		prodData = cursor.fetchall()
		cursor.execute("SELECT * FROM user_infor.userinformation")
		userData = cursor.fetchall()
		lineSub = cur.fetchall()
		#-------------檢查 mysql, sqlite 有無更動------------
		global productC,userC, lineC
		if productC!=len(prodData) or userC!=len(userData) or lineC!=len(lineSub):
			ConvertData.passDatabase()
		else:
			print("continue")
		userC = len(userData)
		lineC = len(lineSub)
		productC = len(prodData)
		print(userC)
		print(productC)
		print(lineC)
		db.close()
		conn.close()
		threading.Timer(10,getMysql).start() #每10秒執行一次
	conn = lite.connect('./Database/mysqlDB.sqlite') 
	cur = conn.cursor()
	db = pymysql.connect(host="140.118.155.126",user="test",passwd="123",db="user_infor") #ip要改
	cursor = db.cursor()
	cur.execute("SELECT * FROM subDB")
	cursor.execute("SELECT * FROM user_infor.searchtable")
	cursor.execute("SELECT * FROM user_infor.userinformation")
	prodData = cursor.fetchall()
	userData = cursor.fetchall()
	lineSub = cur.fetchall()
	db.close()
	conn.close()
	global productC, userC, lineC
	productC = len(prodData)
	userC = len(userData)
	lineC = len(lineSub)
	threads = []
	#初始化 threads, target 分別是 job0, job1, job2
	for i in range(3):
		threads.append(threading.Thread(target = job, args = (i,)))
	func()
	getMysql()
if __name__ == "__main__":
	main()