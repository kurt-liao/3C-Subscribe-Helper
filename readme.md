# 3C Subscribe Helper : 幫訂閱者找尋符合商品
## 流程 :
1. Parsing online shopping website(PCHome,Ruten,Rakuten).
2. Check subscriber's requests.
3. If request is new for program(means flag = 0),check new&old table for it,else check new table is OK.
4. If there are some data matching the request,send email to the subscriber. 
## 執行方式 : 
1. The parseWeb folder contains 3 crawler program (PCHome,Ruten,Rakuten). Put them into your anaconda lib or python lib.
2. Open command-line and type "python CrawlOnlineShop.py" to execute main program.
3. If somthing wrong, you can see the logging error in the console.
