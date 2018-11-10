from dbhelper import DBHelper
from datetime import timedelta
#第一次
#db = DBHelper()

from mysql_db import MYSQL_Helper
db=MYSQL_Helper()

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.models import *
app = Flask(__name__)

from jieba_code import *

import json
import time
line_bot_api = LineBotApi('QQpkRGOU3788WyfkQWxOnNQCyFeyQ146uwPBYTKssTePFJQIUGiu2gbW9QNWAKZnoAgiK/V+kAZBZ72CQ937sQfR1ewIigLxJj8RwLSm4D+n/PBJjNkOxyPQyxLj9W3vfior+9lAzXF906S8TGw97wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5452cb66344cc531747d23bc02579e8f')

#import schedule
import datetime
import sched

#取商品資料庫
cellphone_items=db.get_cellphoneitem_new()
print(cellphone_items[0])
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
    each_push_text=""
    num=0
    for temp in each_website:
        print(temp)
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

        line_bot_api.push_message(fixed_each_userid,TextSendMessage(text=each_push_text))                     
        db.delete_sub(each_sub_name,each_sub[0],each_sub[1])
        db.close_db() 
db.close_db() 





@app.route("/", methods=['GET'])
def hello():
    return "Hello World!!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    if event.message.text=="a":
        #取商品資料庫
        tablet_items=db.get_tabletitem_new()
        print(str(tablet_items[0])+"***************")
        db.close_db()
        #訂閱者商品資料庫
        db.connect_mysqlDB()
        db.check_useridDB()
        db.check_personDB()
        db.check_subDB()
        ALLsub=db.get_ALLsub()
        for each_sub in ALLsub:  
            if(int(each_sub[2])==2):
                print(int(each_sub[1]))
                each_title, each_price, each_website=checkProd(str(each_sub[0]),int(each_sub[1]),tablet_items)  
                print(str(len(each_title))+"///////////////") 
        db.close_db()
    
    msg = event.message.text
    #print(msg)
    #msg = msg.encode('utf-8')
    userID=event.source.user_id
    print(userID)
#---------------------------------------------------------------------------------------------
    #每次打指令看每個手機帳戶目前COMMAND狀態
    LINE_COMMAND=-1
    account_number=""
    species=""
    line_product=""
    db.connect_mysqlDB()
    line_user=db.get_line_useridAndCommand()
    for everyone_data in line_user:
        print(everyone_data[0]+"**")
        if everyone_data[0]==userID:
            LINE_COMMAND=everyone_data[1]
            account_number=everyone_data[2]
            species=everyone_data[3]
            line_product=everyone_data[4]
            break
    #新增新人員的userID和初始化COMMAND為0
    if LINE_COMMAND==-1:
        db.insert_line_useridAndCommand(userID,0)
        LINE_COMMAND=0
    db.close_db()
#---------------------------------------------------------------------------------------------
    #"指令"每個人都可以用
    if event.message.text=="指令":
        reply_text=""
        reply_text+="登入 : 登入帳戶\n"
        reply_text+="登出 : 登出帳戶\n"
        reply_text+="訂閱 : 訂購需求商品\n"
        reply_text+="查看 : 查看訂閱商品\n"
        reply_text+="刪除 : 刪除訂閱商品"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
#---------------------------------------------------------------------------------------------
    #"登入"只有LINE_COMMAND=0才能用
    elif event.message.text=="登入" and LINE_COMMAND==0:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入帳號"))
        db.connect_mysqlDB()
        LINE_COMMAND=1
        db.change_command(userID,LINE_COMMAND)
        db.close_db()
    elif event.message.text=="登入" and LINE_COMMAND>2:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您已登入系統"))
    elif LINE_COMMAND==1:#輸入帳號
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入密碼"))
        db.connect_mysqlDB()
        LINE_COMMAND=2
        db.change_command(userID,LINE_COMMAND)
        #先暫存帳號到LINE_userID裡
        db.change_line_account_number(userID,event.message.text)
        db.close_db()
    elif LINE_COMMAND==2:#輸入密碼
        check_person=False 
        repeat_login=False  
        db.connect_mysqlDB()
        result=db.get_person()
        for person in result:
            if person[0]==account_number and person[1]==event.message.text:
                if person[3]==1:
                    repeat_login=True
                    break
                check_person=True
                USERNAME=person[0]
                break
        if repeat_login==True:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="帳戶已在另一裝置登入"))
            LINE_COMMAND=0
            db.change_command(userID,LINE_COMMAND)
            #帳號刪掉
            db.change_line_account_number(userID,"")
        elif check_person==False:#登入失敗，初始化為0
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤，請重新登入"))
            LINE_COMMAND=0
            db.change_command(userID,LINE_COMMAND)
            #帳號刪掉
            db.change_line_account_number(userID,"")
        else:#登入成功，LINE_COMMAND=3
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="登入成功!!"))
            db.update_person(USERNAME,userID)
            LINE_COMMAND=3
            db.change_command(userID,LINE_COMMAND)
            db.change_personDB_used(1,account_number)
        db.close_db()
    elif LINE_COMMAND<1:
        reply_text="請先登入帳戶"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
#---------------------------------------------------------------------------------------------
    #command:3
    if  LINE_COMMAND>=3:
        if event.message.text=="登出" and LINE_COMMAND==3:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="登出成功!!"))
            LINE_COMMAND=0
            db.connect_mysqlDB()
            db.change_command(userID,LINE_COMMAND)
            db.change_personDB_used(0,account_number)          
            db.close_db()
#---------------------------------------------------------------------------------------------
        elif event.message.text=="查看" and LINE_COMMAND==3:
            db.connect_mysqlDB()

            SUB=db.get_sub(account_number)
            
            i=0
            items_text="訂購商品\n"
            
            for data in SUB:
                i+=1
                if int(data[2])==1:
                    items_text+=str(i)+".手機: "+data[0]+" $"+data[1]+"\n"
                elif int(data[2])==2:
                    items_text+=str(i)+".平板: "+data[0]+" $"+data[1]+"\n"
                elif int(data[2])==3:
                    items_text+=str(i)+".筆電: "+data[0]+" $"+data[1]+"\n"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=items_text))
            db.close_db()
#---------------------------------------------------------------------------------------------
        elif event.message.text=="刪除" and LINE_COMMAND==3:
            db.connect_mysqlDB()

            SUB=db.get_sub(account_number)
            #print(test)
            #print(SUB)
            i=0
            items_text="請輸入刪除編號\n"  
            for data in SUB:
                i+=1
                if int(data[2])==1:
                    items_text+=str(i)+".手機: "+data[0]+" $"+data[1]+"\n"
                elif int(data[2])==2:
                    items_text+=str(i)+".平板: "+data[0]+" $"+data[1]+"\n"
                elif int(data[2])==3:
                    items_text+=str(i)+".筆電: "+data[0]+" $"+data[1]+"\n"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=items_text))
            LINE_COMMAND=4
            db.change_command(userID,LINE_COMMAND)
            db.close_db()
        elif LINE_COMMAND==4:
            db.connect_mysqlDB()
 
            SUB=db.get_sub(account_number)
            is_number=check_is_number(event.message.text)
            if is_number==True:
                if int(event.message.text)<=len(SUB) and int(event.message.text)>0:
                    db.delete_sub(account_number,SUB[int(event.message.text)-1][0],SUB[int(event.message.text)-1][1])
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="刪除成功"))
                else:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="編號輸入錯誤，請重新輸入指令"))
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="編號為阿拉伯數字，請重新輸入指令"))
            LINE_COMMAND=3
            db.change_command(userID,LINE_COMMAND)
            db.close_db()
#---------------------------------------------------------------------------------------------
        elif event.message.text=="訂閱" and LINE_COMMAND==3:
            #reply_text="請輸入種類編號\n"+"1: 手機\n"+"2: 平板\n"+"3: 筆電"
            #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_text))
            buttons_template = TemplateSendMessage(
                alt_text='Buttons Template',
                template=ButtonsTemplate(
                    title='商品訂閱',
                    text='請點選種類',
                    #thumbnail_image_url='',
                    actions=[
                        MessageTemplateAction(
                            label='1: 手機',
                            text='1'
                        ),
                        MessageTemplateAction(
                            label='2: 平板',
                            text='2'
                        ),
                        MessageTemplateAction(
                            label='3: 筆電',
                            text='3'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, buttons_template)
            db.connect_mysqlDB()
            LINE_COMMAND=5
            db.change_command(userID,LINE_COMMAND)
            db.close_db()          
        elif LINE_COMMAND==5:
            db.connect_mysqlDB()
            is_number=check_is_number(event.message.text)
            if is_number==True:
                if int(event.message.text)<=3 and int(event.message.text)>=1:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入商品名稱"))
                    LINE_COMMAND=6
                    db.change_command(userID,LINE_COMMAND)
                    db.change_line_species(userID,event.message.text)
                else:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="編號輸入錯誤，請重新輸入指令"))
                    LINE_COMMAND=3
                    db.change_command(userID,LINE_COMMAND)
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="編號為阿拉伯數字，請重新輸入指令"))
                LINE_COMMAND=3
                db.change_command(userID,LINE_COMMAND)           
            db.close_db()
        elif LINE_COMMAND==6:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入商品預算"))
            db.connect_mysqlDB()
            LINE_COMMAND=7
            db.change_command(userID,LINE_COMMAND)
            db.change_line_product(userID,event.message.text)
            db.close_db()
        elif LINE_COMMAND==7:
            db.connect_mysqlDB()

            is_number=check_is_number(event.message.text)
            if is_number==False:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="價錢輸入錯誤，請重新輸入指令"))
                LINE_COMMAND=3
                db.change_command(userID,LINE_COMMAND)
            else:
                now = datetime.datetime.now()
                aDay = timedelta(days=14)
                now = now + aDay
                time_text=now.strftime('%Y-%m-%d')
                db.add_sub(account_number,line_product,event.message.text,species,time_text,1)
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="訂閱成功"))
                db.close_db()
                

                #直接找，找到再刪除訂閱商品
                if int(species)==1:
                    items=db.get_cellphoneitem_old()
                    title, price, website=checkProd(line_product,int(event.message.text),items)      
                    push_text=""
                    i=0
                    for temp in website:
                        index=i+1            
                        if i<10:  
                            push_text+=str(index)+". "+str(title[i])+" $"+str(price[i])+" "+temp+"\n"
                        i+=1
                    db.close_db()

                    items_new=db.get_cellphoneitem_new()
                    title_new, price_new, website_new=checkProd(line_product,int(event.message.text),items_new)  
                    j=0    
                    for temp in website_new:
                        index=i+1            
                        if i<10:  
                            push_text+=str(index)+". "+str(title_new[j])+" $"+str(price_new[j])+" "+temp+"\n"
                        i+=1
                        j+=1
                    db.close_db()

                    if i!=0:
                        line_bot_api.push_message(userID,TextSendMessage(text=push_text))
                        db.connect_mysqlDB()                        
                        db.delete_sub(account_number,line_product,event.message.text)
                        db.close_db()
                elif int(species)==2:
                    items=db.get_tabletitem_old()
                    title, price, website=checkProd(line_product,int(event.message.text),items)      
                    push_text=""
                    i=0
                    for temp in website:
                        index=i+1            
                        if i<10:  
                            push_text+=str(index)+". "+str(title[i])+" $"+str(price[i])+" "+temp+"\n"
                        i+=1
                    db.close_db()

                    items_new=db.get_tabletitem_new()
                    title_new, price_new, website_new=checkProd(line_product,int(event.message.text),items_new)  
                    j=0    
                    for temp in website_new:
                        index=i+1            
                        if i<10:  
                            push_text+=str(index)+". "+str(title_new[j])+" $"+str(price_new[j])+" "+temp+"\n"
                        i+=1
                        j+=1
                    db.close_db()

                    if i!=0:
                        line_bot_api.push_message(userID,TextSendMessage(text=push_text))
                        db.connect_mysqlDB()
                        db.check_subDB()                          
                        db.delete_sub(account_number,line_product,event.message.text)
                        db.close_db()
                elif int(species)==3:
                    items=db.get_notebookitem_old()
                    title, price, website=checkProd(line_product,int(event.message.text),items)      
                    push_text=""
                    i=0
                    for temp in website:
                        index=i+1            
                        if i<10:  
                            push_text+=str(index)+". "+str(title[i])+" $"+str(price[i])+" "+temp+"\n"
                        i+=1
                    db.close_db()

                    items_new=db.get_notebookitem_new()
                    title_new, price_new, website_new=checkProd(line_product,int(event.message.text),items_new)  
                    j=0    
                    for temp in website_new:
                        index=i+1            
                        if i<10:  
                            push_text+=str(index)+". "+str(title_new[j])+" $"+str(price_new[j])+" "+temp+"\n"
                        i+=1
                        j+=1
                    db.close_db()

                    if i!=0:
                        line_bot_api.push_message(userID,TextSendMessage(text=push_text))
                        db.connect_mysqlDB()
                        db.check_subDB()                          
                        db.delete_sub(account_number,line_product,event.message.text)
                        db.close_db()
                db.connect_mysqlDB()
                LINE_COMMAND=3
                db.change_command(userID,LINE_COMMAND)
            db.close_db()

if __name__ == "__main__":
    app.run(debug=True,port=5000)
