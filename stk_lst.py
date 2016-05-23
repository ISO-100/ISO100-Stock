# -*- coding:utf-8 -*- 
#Created on 2015/06/15
#Last modified on 2016/05/04
#By Teague Xiao
#This script is to download the latest Stock list from Eastmoney.com
#Website: http://quote.eastmoney.com/stocklist.html

import urllib
import re
import MySQLdb
import os
import ConfigParser

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
    #con = sqlite3.connect('stock.sqlite')
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    cur = con.cursor()
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
        #Remove the spaces between charaters
        stock_name = stock_name.replace(" ", "")
        cur.execute("REPLACE INTO stk_lst (stk_num, stk_name) VALUES(%s, %s)", (stock_num,stock_name))
        con.commit()
        print stock_num, stock_name
    con.close()
    fopen1.close()

if __name__ == "__main__":
    stk_lst_download()
    stk_lst_re()
#print "stk_lst process done!"