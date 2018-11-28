import sqlite3

class MYSQL_Helper:
    #userid資料庫
    #建useridDB
    def check_useridDB(self):
        stmt = "CREATE TABLE IF NOT EXISTS useridDB (userID text,command int,account_number text,species int,product text)"
        self.conn.execute(stmt)
        self.conn.commit()
    #提取userID和command
    def get_line_useridAndCommand(self):
        stmt="select userID,command,account_number,species,product from useridDB"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #增加line_userid和command
    def insert_line_useridAndCommand(self,userid,command):
        stmt="insert into useridDB (userID,command) values(?,?)"
        args=(userid,command,)
        self.conn.execute(stmt,args)
        self.conn.commit()
    #更改帳號(暫存用)     
    def change_line_account_number(self,userid,account_number):
        stmt="UPDATE useridDB SET account_number=(?) where userID=(?)"
        args=(account_number,userid,)
        self.conn.execute(stmt,args)
        self.conn.commit()
    #更改目前指令狀況
    def change_command(self,userid,command):
        stmt="UPDATE useridDB SET command=(?) WHERE userID=(?)"
        args=(command,userid,)
        self.conn.execute(stmt,args)
        self.conn.commit()
    #更改種類(暫存用)
    def change_line_species(self,userid,species):
        stmt="UPDATE useridDB SET species=(?) WHERE userID=(?)"
        args=(species,userid,)
        self.conn.execute(stmt,args)
        self.conn.commit()
    #更改商品名稱(暫存用)
    def change_line_product(self,userid,product):
        stmt="UPDATE useridDB SET product=(?) WHERE userID=(?)"
        args=(product,userid,)
        self.conn.execute(stmt,args)
        self.conn.commit()
    #--------------------------------------------------------------------------------

    def change_personDB_used(self, used,username):
        stmt="UPDATE personDB SET used=(?) WHERE username=(?)"
        args=(used,username,)
        self.conn.execute(stmt,args)
        self.conn.commit()

    #連線到訂購資料DB
    def connect_mysqlDB(self, dbname="..\\Database\\mysqlDB.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
    #確認人員表在不在
    def check_personDB(self):
        stmt = "CREATE TABLE IF NOT EXISTS personDB (username text,password text,userid text,used int)"
        self.conn.execute(stmt)
        self.conn.commit()
    #確認訂購表在不在
    def check_subDB(self):
        stmt = "CREATE TABLE IF NOT EXISTS subDB (username text,product text,price text,type text,duetime timestamp,is_LineSub int)"
        self.conn.execute(stmt)
        self.conn.commit()
    #提取人員資料   username,password,userid
    def get_person(self):
        stmt="select username,password,userid,used from personDB"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #提取訂閱商品   product,price
    def get_sub(self, username):
        stmt = "select product,price,type from subDB where username=(?)"
        args = (username, )
        self.cur=self.conn.cursor()
        self.cur.execute(stmt, args)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #提取username
    def get_username(self, userid):
        stmt="select username from personDB where userid=(?)"
        args=(userid, )
        self.cur=self.conn.cursor()
        self.cur.execute(stmt, args)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #存userid到personDB
    def update_person(self, username, userid):
        stmt = "UPDATE personDB SET userid=(?) WHERE username=(?)"
        args = (userid, username,)
        self.conn.execute(stmt, args)
        self.conn.commit()
    #新增訂閱
    def add_sub(self, username, product, price, type, duetime,is_LineSub):
        stmt = "INSERT INTO subDB (username,product,price,type,duetime,is_LineSub) VALUES (?,?,?,?,?,?)"
        args = (username, product, price, type, duetime, is_LineSub,)
        self.conn.execute(stmt, args)
        self.conn.commit()
    #刪除訂閱
    def delete_sub(self, username, product, price):
        stmt = "DELETE FROM subDB WHERE username = (?) and product=(?) and price=(?)"
        args = (username, product, price, )
        self.conn.execute(stmt, args)
        self.conn.commit()
    #目前沒用到
    def delete_userid(self,userid):
        stmt = "UPDATE personDB SET userid="" WHERE userid=(?)"
        args = (userid, )
        self.conn.execute(stmt, args)
        self.conn.commit()
    #關閉資料庫連線
    def close_db(self):
        self.conn.close()

#--------------------------------------------------------------------------------
    #從tablet資料庫拿上架商品 #2
    def get_tabletitem_old(self, dbname="..\\Database\\pad.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        #stmt1 = "CREATE TABLE IF NOT EXISTS old_tablet_table (title text,price integer,website text,date timestamp,flag integer)"
        #self.conn.execute(stmt1)
        stmt="select title, price, website from old"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    def get_tabletitem_new(self, dbname="..\\Database\\pad.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        #stmt1 = "CREATE TABLE IF NOT EXISTS old_tablet_table (title text,price integer,website text,date timestamp,flag integer)"
        #self.conn.execute(stmt1)
        stmt="select title, price, website from new"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #從cellphone資料庫拿上架商品 #1
    def get_cellphoneitem_old(self, dbname="..\\Database\\cellphone.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        #stmt1 = "CREATE TABLE IF NOT EXISTS old_cellphone_table (title text,price integer,website text,date timestamp,flag integer)"
        #self.conn.execute(stmt1)
        stmt="select title, price, website from old"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    def get_cellphoneitem_new(self, dbname="..\\Database\\cellphone.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        #stmt1 = "CREATE TABLE IF NOT EXISTS old_cellphone_table (title text,price integer,website text,date timestamp,flag integer)"
        #self.conn.execute(stmt1)
        stmt="select title, price, website from new"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #從notebook資料庫拿上架商品 #3
    def get_notebookitem_old(self, dbname="..\\Database\\notebook.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        #stmt1 = "CREATE TABLE IF NOT EXISTS old_notebook_table (title text,price integer,website text,date timestamp,flag integer)"
        #self.conn.execute(stmt1)
        stmt="select title, price, website from old"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    def get_notebookitem_new(self, dbname="..\\Database\\notebook.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        #stmt1 = "CREATE TABLE IF NOT EXISTS old_notebook_table (title text,price integer,website text,date timestamp,flag integer)"
        #self.conn.execute(stmt1)
        stmt="select title, price, website from new"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
#--------------------------------------------------------------------------------
    #取全部訂閱資料
    def get_ALLsub(self):
        stmt = "select product,price,type from subDB"
        self.cur=self.conn.cursor()
        self.cur.execute(stmt)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #取單一sub的名子
    def get_sub_name(self,product,price):
        stmt="select username from subDB where product=(?) and price=(?)"
        args=(product,price,)
        self.cur=self.conn.cursor()
        self.cur.execute(stmt, args)
        self.conn.commit()
        result=self.cur.fetchall()
        return result
    #用username取userid
    def get_userid(self,username):
        stmt="select userid from personDB where username=(?)"
        args=(username,)
        self.cur=self.conn.cursor()
        self.cur.execute(stmt, args)
        self.conn.commit()
        result=self.cur.fetchall()
        return result