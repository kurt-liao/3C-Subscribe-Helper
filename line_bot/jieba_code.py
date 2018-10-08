import sqlite3 as lite
import re
import pandas as pd
import string
#import parseR
import jieba
#結巴分詞
def none_empty(s):
    return s and s.strip()
def checkProd(searchWord,expPrice,database):
    df=pd.DataFrame(database)
    cutWord = []
    n = 0
    title = []
    price = []
    website = []
    base = expPrice/5
    for char in string.punctuation:                     #去掉字串中符號
        searchWord = searchWord.replace(char, '')
    wordlist = jieba.cut_for_search(searchWord)         #利用結巴斷詞
    #print(wordlist)
    for i in wordlist:
        cutWord += [i]
    res = filter(none_empty, cutWord)                   #去掉list中空白部分
    cutWord = []
    for i in res:
        cutWord += [i]
    print(cutWord)
    for i in range(len(df.values)):
        for k in range(len(cutWord)):
            if(re.search(cutWord[k],df.values[i][0],re.IGNORECASE)):#比對字串中符合之字串
                n = n + 1
        if(n==len(cutWord)):
            if(df.values[i][1] >= expPrice-base and df.values[i][1] <= expPrice+base):#字串符合比對價錢是否符合
                    title+=[df.values[i][0]]
                    price+=[df.values[i][1]]
                    website+=[df.values[i][2]]
        n = 0
    return title, price, website
def check_is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
