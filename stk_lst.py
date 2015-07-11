# -*- coding:utf-8 -*- 
#Created on 2015/06/15
#By Tea Shaw
#This script is to download the latest Stock list from Eastmoney.com
#Website: http://quote.eastmoney.com/stocklist.html

import urllib
import re
#from bs4 import BeautifulSoup
import sqlite3

def stk_lst_download():
    url = 'http://quote.eastmoney.com/stocklist.html'
    html = urllib.urlopen(url).read()
    #soup = BeautifulSoup(html)
    #for link in soup.find_all('a'):
    #for link in soup.get_text().decode('gbk').encode('utf-8'):
    #stock_name = re.findall('.*_blank">())',link)
    #a = soup.get_text()
    #link.decode('gb2312','ignore').encode('utf-8')
    fopen = open("stk_lst_page.txt",'w')
    fopen.write(html)
    fopen.close()
    
def stk_lst_re():
    fopen1 = open("stk_lst_page.txt")
    #fopen2 = open("stk_lst_final.txt","w")
    con = sqlite3.connect('stock.sqlite')
    #cur = con.cursor()
    for line in fopen1:
        stock_num_re = re.findall('">.*\(([0-9]*)', line)
        #print stock_num_re
        if len(stock_num_re)>0:
            stock_num = stock_num_re[0].decode('gb2312','ignore')
        else:
            continue
        stock_name_re = re.findall('">(.*)\([0-9].*\)', line)
        if len(stock_name_re) > 0:
            stock_name = stock_name_re[0].decode('gb2312','ignore')
        else:
            continue
        con.execute("CREATE TABLE IF NOT EXISTS stk_lst(stk_num CHAR PRIMARY KEY,stk_name CHAR)")
        con.execute("INSERT OR REPLACE INTO stk_lst (stk_num, stk_name) VALUES(?,?)",(stock_num,stock_name))
        con.commit()
        #print stock_num, stock_name
        #fopen2.write(stock_num)
        #fopen2.write('\t')
        #fopen2.write(stock_name)
        #fopen2.write('\n')
    #fopen1.close()    
    #fopen2.close()
    con.close()
   
stk_lst_download()
stk_lst_re()
#print "stk_lst process done!"