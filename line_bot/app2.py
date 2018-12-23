import schedule
import time
import datetime
from jieba_code import *

from mysql_db import MYSQL_Helper
db=MYSQL_Helper()
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
def daily_push():
    #取商品資料庫
    cellphone_items=db.get_cellphoneitem_new()
    #print(cellphone_items[0])
    db.close_db()
    tablet_items=db.get_tabletitem_new()
    db.close_db()
    notebook_items=db.get_notebookitem_new()
    db.close_db()
    #訂閱者商品資料庫
    db.connect_mysqlDB()
    db.check_useridDB()
    db.check_personDB()
    db.check_subDB()
    ALLsub=db.get_ALLsub()
    for each_sub in ALLsub:
        if(int(each_sub[2])==1):
            each_title, each_price, each_website=checkProd(str(each_sub[0]),int(each_sub[1]),cellphone_items)         
        elif(int(each_sub[2])==2):
            each_title, each_price, each_website=checkProd(str(each_sub[0]),int(each_sub[1]),tablet_items)  
        elif(int(each_sub[2])==3):  
            each_title, each_price, each_website=checkProd(str(each_sub[0]),int(each_sub[1]),notebook_items)   
        each_push_text="符合需求的商品:\n"
        num=0
        for temp in each_website:
            #print(temp)
            index=num+1            
            if num<10:  
                each_push_text+=str(index)+". "+str(each_title[num])+" $"+str(each_price[num])+" "+temp+"\n"
            num+=1
        db.close_db()
        if num!=0:
            db.connect_mysqlDB()
            db.check_subDB()    
            sub_name=db.get_sub_name(each_sub[0],each_sub[1])
            sub_name_text=str(sub_name)
            each_sub_name=sub_name_text[2:-3]
            each_sub_name=each_sub_name.replace('\'','')

            db.check_personDB()
            each_userid=db.get_userid(each_sub_name)
            each_userid_text=str(each_userid)
            fixed_each_userid=each_userid_text[2:-3]
            fixed_each_userid=fixed_each_userid.replace('\'','')
            if(len(fixed_each_userid)==33):
                line_bot_api.push_message(fixed_each_userid,TextSendMessage(text=each_push_text))                     
                db.delete_sub(each_sub_name,each_sub[0],each_sub[1],each_sub[2])
            db.close_db() 
    db.close_db() 

CHANNEL_ACCESS_TOKEN = "QQpkRGOU3788WyfkQWxOnNQCyFeyQ146uwPBYTKssTePFJQIUGiu2gbW9QNWAKZnoAgiK/V+kAZBZ72CQ937sQfR1ewIigLxJj8RwLSm4D+n/PBJjNkOxyPQyxLj9W3vfior+9lAzXF906S8TGw97wdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

schedule.every().seconds.do(daily_push)
while True:
    schedule.run_pending()
    time.sleep(1)