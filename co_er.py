# -*- coding:utf-8 -*- 
#Created on 2015/07/14
#By Tea Shaw
#http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/performance/index.phtml?s_i=&s_a=&s_c=&s_type=&reportdate=2015&quarter=2&p=1&num=60

from bs4 import BeautifulSoup
import sqlite3
import urllib2
import re
import time

def main():
    i = 1
    while True:
        year = raw_input("Please input the year (2014,2015):")
        quarter = raw_input("Please input the quarter (1,2,3,4):")
        try:
            if int(year) <= 2015 and int(quarter) in [1,2,3,4]:
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
    soup = BeautifulSoup(html,from_encoding="gb18030")
    tb = soup.find("table",id="dataTable")
    j = 4
    reslut = list()
    while j <= 116:
        try:
            tr = tb.contents[j]
            stk_num = tb.contents[j].contents[1].string
            stk_name = tb.contents[j].contents[3].string
            type = tb.contents[j].contents[5].string
            announce_date = tb.contents[j].contents[7].string
            report_date = tb.contents[j].contents[9].string
            summary = tb.contents[j].contents[11].string
            eps_last_year = tb.contents[j].contents[13].string
            change_range = tb.contents[j].contents[15].string
            j = j + 2
            co_er_store([stk_num,stk_name,type,announce_date,report_date,summary,eps_last_year,change_range])
        except IndexError:
            return False
    return True
            
def co_er_store(list):
    con = sqlite3.connect('stock.sqlite')
    #con.execute('DROP TABLE co_er')
    con.execute('''CREATE TABLE IF NOT EXISTS co_er(
                    stk_num CHAR,
                    stk_name CHAR,
                    type CHAR,
                    announce_date TEXT,
                    report_date TEXT,
                    summary CHAR,
                    eps_last_year CHAR,
                    change_range CHAR,
                    PRIMARY KEY (stk_num,announce_date)
                    )''')

    con.execute('''INSERT OR REPLACE INTO co_er (
                stk_num,stk_name,type,announce_date,report_date,summary,eps_last_year,change_range) 
                VALUES (?,?,?,?,?,?,?,?)''',
                (list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7]))
    con.commit()   
    con.close()
              
if __name__ == "__main__":  
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))