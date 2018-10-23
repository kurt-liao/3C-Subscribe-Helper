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
	def func():
		try:
			for i in range(2):
				threads.append(threading.Thread(target = job, args = (i,)))
				threads[i].start()   
			for i in range(2):
				threads[i].join()
		except:
			logging.error("Error: parse error")
		try:
			db = pymysql.connect(host="140.118.155.126",user="test",passwd="123",db="user_infor") #ip要改
			cursor = db.cursor()
			cursor.execute("SELECT * FROM user_infor.searchtable")   
			results = cursor.fetchall()
			cursor.execute("delete From user_infor.searchtable where dueTime = DATE(NOW());")
			db.commit()
			db.close()
			print("STEP 2")
		except:
			logging.error("Error: mysql connected error")
		#-----------------找request相符之商品並寄信-------
		try:
			t = CrawlFunc.check_request(results)
			if t ==0:
				print("no request today")
			print("STEP 3")
		except:
			logging.error("Error: check_request error")
		#如果需要循环调用，就要添加以下方法
		timer = threading.Timer(180, func)
		timer.start()
	def getMysql():
		conn = lite.connect('./Database/mysqlDB.sqlite') 
		cur = conn.cursor()
		cur.execute("SELECT * FROM subDB")
		db = pymysql.connect(host="140.118.155.126",user="test",passwd="123",db="user_infor") #ip要改
		cursor = db.cursor()
		cursor.execute("SELECT * FROM user_infor.searchtable")
		cursor.execute("SELECT * FROM user_infor.userinformation")
		prodData = cursor.fetchall()
		userData = cursor.fetchall()
		lineSub = cur.fetchall()
		global productC,userC, lineC
		if productC!=len(prodData) or userC!=len(userData) or lineC!=len(lineSub):
			ConvertData.passDatabase()
		else:
			print("continue")
		productC = len(prodData)
		print(productC)
		db.close()
		threading.Timer(10,getMysql).start()
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
	global productC, userC, lineC
	threads = []
	productC = len(prodData)
	userC = len(userData)
	lineC = len(lineSub)
	func()
	getMysql()
if __name__ == "__main__":
	main()