import sqlite3 as lite
import pymysql

usersql = "insert into personDB(username,password,userid,used) values(?,?,?,?)"
requestsql = "insert into subDB(username,product,price,type,duetime) values(?,?,?,?,?)"

dbname_user = "mysqlDB.sqlite"
dbname_requests = "崇恩requests"

mysqldb = "user_infor"
mysqlhost = "140.118.149.205"
mysqluser = "test"
mysqlpwd = "123"

mysql_conn = pymysql.connect(host=mysqlhost, user=mysqluser, passwd=mysqlpwd, db=mysqldb)
mycur = mysql_conn.cursor()
print("success")
mycur.execute('select account from user_infor.userinformation')
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
