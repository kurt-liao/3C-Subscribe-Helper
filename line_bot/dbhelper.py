import sqlite3


class DBHelper:
    #連線到DB
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
    #確認表在不在
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (userid text,description1 text,description2 text,product_num text)"
        self.conn.execute(stmt)
        self.conn.commit()
    #新增用戶
    def add_user(self, user_id):
        stmt = "INSERT INTO items (userid,product_num) VALUES (?,?)  "
        args = (user_id,0,)
        self.conn.execute(stmt, args)
        self.conn.commit()
    #新增商品
    def add_item1(self, user_id, item_text):
        stmt = "UPDATE items SET description1=(?),product_num=1 WHERE userid=(?) "
        args = (item_text, user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()
    def add_item2(self, user_id, item_text):
        stmt = "UPDATE items SET description2=(?),product_num=2 WHERE userid=(?) "
        args = (item_text, user_id,)
        self.conn.execute(stmt, args)
        self.conn.commit()
    #更新資料
    def update_item(self, user_id,item1_text,item2_text,num):
        stmt = "update items set description1=(?),description2=(?),product_num=(?) WHERE userid=(?)"
        args = (item1_text,item2_text,num,user_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()
    #刪除資料 沒用
    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()
    #拿DB所有資料 沒用
    def get_items(self,user_id):
        db_product_item1=[]
        db_product_item2=[]
        stmt = "SELECT description1,description2 FROM items where userid=(?)"
        #return [x[0] for x in self.conn.execute(stmt)]
        args = (user_id,)
        self.cur = self.conn.cursor()
        self.cur.execute(stmt,args)
        result = self.cur.fetchall()
        for item in result:
            db_product_item1.append(item[0])
            db_product_item2.append(item[1])
        return db_product_item1,db_product_item2
    #關閉資料庫連線
    def close_db(self):
        self.conn.close()
    #看userid存有沒有在資料庫
    def check_db_id(self,user_id):
        stmt = "select * from items where userid=(?)"
        args = (user_id,)
        self.cur = self.conn.cursor()
        self.cur.execute(stmt,args)
        result = self.cur.fetchall()
        if len(result)!=0:
            return 1
        else:
            return 0
    def get_productnum(self,user_id):
        stmt = "select product_num from items where userid=(?)"
        args = (user_id,)
        self.cur = self.conn.cursor()
        self.cur.execute(stmt,args)
        result = self.cur.fetchall()
        db_product=[]
        for item in result:
            a=str(item)
            db_product.append(a[2:-3])
        return db_product
    
