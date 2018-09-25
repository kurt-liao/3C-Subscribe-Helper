
# coding: utf-8

# In[1]:


import sqlite3 as lite
import pymysql


# In[7]:


#define needed variable
usersql = "insert into personDB(username,password,userid,used) values(?,?,?,?)"
requestsql = "insert into subDB(username,product,price,type,duetime) values(?,?,?,?,?)"

dbname_user = "崇恩user"
dbname_requests = "崇恩requests"

mysqldb = "user_infor"
mysqlhost = "192.168.50.166"
mysqluser = "curt"
mysqlpwd = "curt0226"


# In[9]:


#明軒 database user info
mysql_conn = pymysql.connect(host=mysqlhost, user=mysqluser, passwd=mysqlpwd, db=mysqldb)
mycur = mysql_conn.cursor()
mycur.execute('select username from user_infor.userinformation')
list_of_myuser = mycur.fetchall()    #帳號
mycur.execute('select password from user_infor.userinformation')
list_of_mypwd = mycur.fetchall()    #密碼
mysql_conn.close()


# In[8]:


#崇恩 database user info
sql_conn = lite.connect(dbname_user)
sqlcur = sql_conn.cursor()
sqlcur.execute('create table if not exists personDB(username text,password text,userid text,used integer);')

#明軒 data 放進崇恩 database
for i in range(len(list_of_myuser)):
    sqlcur.execute(usersql,(list_of_myuser[i][0],list_of_mypwd[i][0],0,0))
sql_conn.commit()
sql_conn.close()


# In[ ]:


#明軒 database requests
mysql_conn = pymysql.connect(host=mysqlhost, user=mysqluser, passwd=mysqlpwd, db=mysqldb)
mycur = mysql_conn.cursor()
mycur.execute('select * from user_infor.searchtable')
results = mycur.fetchall()


# In[ ]:


#崇恩 database requests
sql_conn = lite.connect(dbname_requests)
sqlcur = sql_conn.cursor()
sqlcur.execute('create table if not exists subDB(username text,product text,price text,type text,duetime text);')

#崇恩 data 放進明軒 database
'''
'''

#明軒 data 放進崇恩 database
for i in range(len(results)):
    sqlcur.execute(requestsql,(results[i][1], results[i][3], results[i][4], results[i][6], results[i][8]))
sql_conn.commit()
sql_conn.close()

