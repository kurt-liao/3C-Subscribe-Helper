import sqlite3 as lite
import pymysql
import time
import datetime
from datetime import timedelta

def passDatabase():
	insertsql = "insert into subDB(username,product,price,type,duetime,is_LineSub,isInSql) values(?,?,?,?,?,?,?)"
	mysqldb = "user_infor"
	mysqlhost = "140.118.155.126"
	mysqluser = "test"
	mysqlpwd = "123"

	mysql_conn = pymysql.connect(host=mysqlhost, user=mysqluser, passwd=mysqlpwd, db=mysqldb)
	mycur = mysql_conn.cursor()
	print("success")

	#明軒 database

	mycur.execute("SELECT * FROM user_infor.searchtable")
	pyresults = mycur.fetchall()
	#崇恩 database
	conn = lite.connect('line_bot\mysqlDB.sqlite')
	cur = conn.cursor()
	cur.execute('create table if not exists subDB(username text,product text,price text,type text,duetime timestamp,is_LineSub int);')
	cur.execute('select * from subDB')
	results = cur.fetchall()


	#明軒 in 崇恩
	for i in range(len(pyresults)):
		count = 0						#count 用來決定是否要存 1不存 0存
		if(pyresults[i][9] == 0):   #判斷是否是從賴過來的，如果是就不用再存
			for j in range(len(results)):	
				if(pyresults[i][1] == results[j][0] and pyresults[i][3] == results[j][1] and pyresults[i][4] == int(results[j][2]) ):   #判斷是否存在
					count = 1
		else:
			count = 1
		if(count != 1):
			cur.execute(insertsql, (pyresults[i][1], pyresults[i][3], pyresults[i][4], pyresults[i][6], pyresults[i][8],0,1))
			conn.commit()

	#崇恩 in 明軒
	for i in range(len(results)):
		if(results[i][6] != 1): #isInSql 表示 mysql 上面存在，無須再存
			mycur.execute("INSERT INTO user_infor.searchtable (userName, product, price, type, flag, dueTime, line) VALUES (%s,%s,%s,%s,%s,%s,%s)",
			(results[i][0],results[i][1] , int(results[i][2]), int(results[i][3]),int(0), results[i][4], results[i][5]))
			mysql_conn.commit()
		else:
			print("it's already exist")
		cur.execute('UPDATE subDB SET isInSql = 1')
		conn.commit()
	#刪掉不存在的商品
	for i in range(len(pyresults)):
		count = 0
		if(pyresults[i][9] == 1):
			for j in range(len(results)):
				if(pyresults[i][1] == results[j][0] and pyresults[i][3] == results[j][1] and pyresults[i][4] == results[j][2] and pyresults[i][6] == results[j][3]):
					count = 1
			print(count)
			if(count == 0):
				mycur.execute("delete from user_infor.searchtable where id = '%s' " %int(pyresults[i][0]))
				mysql_conn.commit()
				print("Request '%s' was not exist")
	conn.close()
	mysql_conn.close()
