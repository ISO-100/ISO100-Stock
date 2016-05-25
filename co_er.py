# -*- coding:utf-8 -*- 
#Created on 2015/07/14
#By Tea Shaw
#Last updated on 2016/05/13: Modify from using SQLite to Mysql - Teague Xiao
#http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/performance/index.phtml?s_i=&s_a=&s_c=&s_type=&reportdate=2015&quarter=2&p=1&num=60
#Usage: python co_er.py 2016 1

from bs4 import BeautifulSoup
#import sqlite3
import MySQLdb
import urllib2
import re
import time

import os
import ConfigParser
import sys

#For fixing 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128) ERROR
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    i = 1
    while True:
        #year = raw_input("Please input the year (2015,2016):")
        #quarter = raw_input("Please input the quarter (1,2,3,4):")
        #for development
        #year = '2016'
        #quarter = '1'
        if sys.argv[1] == "help":
            print "For getting co_er for year 2016 quater 1: \n python co_er.py 2016 1"
            exit()
        year = sys.argv[1]
        quarter = sys.argv[2]
        
        try:
            if int(year) <= 2016 and int(quarter) in [1,2,3,4]:
                break
            else:
                print "Wrong input, please try again"
                continue
        except ValueError:
            print "Wrong input, please try again"
            continue
    while co_er_download(i,year,quarter):
        i = i + 1
    
def co_er_download(i,year,quarter):
    url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/performance/index.phtml?s_i=&s_a=&s_c=&s_type=&reportdate=%s&quarter=%s&p=%s&num=60' %(year, quarter, i)
    print "Accessing %s" %url
    try: html = urllib2.urlopen(url).read()
    except urllib2.HTTPError: print "Invalid URL"
    #soup = BeautifulSoup(html,from_encoding="gb18030")
    soup = BeautifulSoup(html,"html.parser",from_encoding="gb18030")
    tb = soup.find("table",id="dataTable")
    j = 4
    reslut = list()
    #tb = tb.contents[4]
    #print tbcontents[4].contents[3].string
    
    while j <= 116:
        try:
            #tr = tb.contents[j]
            stk_num = tb.contents[j].contents[1].string
            stk_name = tb.contents[j].contents[3].string
            type = tb.contents[j].contents[5].string
            announce_date = tb.contents[j].contents[7].string
            report_date = tb.contents[j].contents[9].string
            summary = tb.contents[j].contents[11].string
            eps_last_year = tb.contents[j].contents[13].string
            change_range = tb.contents[j].contents[15].string
            j = j + 2
            print stk_num
            print stk_name
            co_er_store([stk_num,stk_name,type,announce_date,report_date,summary,eps_last_year,change_range])
        except IndexError:
            return False
    return True
            
def co_er_store(list):
    #con = sqlite3.connect('stock.sqlite')
    #con.execute('DROP TABLE co_er')
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS co_er(
                    stk_num CHAR(20),
                    stk_name CHAR(20),
                    type CHAR(20),
                    announce_date CHAR(20),
                    report_date CHAR(20),
                    summary TEXT,
                    eps_last_year float,
                    change_range CHAR(20),
                    PRIMARY KEY (stk_num,announce_date)
                    )''')
    c.execute('''REPLACE INTO co_er (
                stk_num,stk_name,type,announce_date,report_date,summary,eps_last_year,change_range) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
                (list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7]))
    con.commit()   
    c.close()
              
if __name__ == "__main__":  
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))