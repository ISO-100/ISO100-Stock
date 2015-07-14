#Created on 2015/06/15
#By Tea Shaw
#This script is aim to download the current price of a specific stock from SINA Stock 
#The info of each column is: stock number, stock name, opening price today, closing price today, current price, highest price today,lowest price today,don't know, don't know,stock dealed, price dealed today, date, time
#Sample 1#: http://hq.sinajs.cn/list=sh601003
#Sample 2#: http://hq.sinajs.cn/list=sz000002

import urllib
import sqlite3

#stock_num = raw_input('Please enter the stock number(6 digits): ')
#example stock_num = '000002'

conn = sqlite3.connect('stock.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stk_prc(
                stk_num CHAR PRIMARY KEY,
                stk_name CHAR,
                open_prc NUM,
                close_prc NUM,
                current_prc NUM,
                highese_prc NUM,
                lowest_prc NUM,
                buy1 NUM,
                sell1 NUM,
                stock_dealed INT,
                price_dealed INT,
                date TEXT,
                time CHAR
                )''')
for stk_num in c.execute("SELECT stk_num from stk_lst"):
    stk_num = stk_num[0]
    if stk_num.startswith('6'):
        url = 'http://hq.sinajs.cn/list=sh' + stk_num
    elif stk_num.startswith('0'):
        url = 'http://hq.sinajs.cn/list=sz' + stk_num
    else:
        print 'Invalid stock number!'
        continue
    try:
        html = urllib.urlopen(url).read()
    except:
        print 'Invalid stock number!'
        continue
        
    l = html.split(',')
    start = l[0]
    #stk_name = start[-8:].decode('gb2312','ignore')
    stk_name = start[21:].decode('gb2312','ignore')
    #print len(html)
    if len(html) == 24:
        continue
    else:
        open_prc = l[1]
        close_prc = l[2]
        current_prc = l[3]
        highest_prc = l[4]
        lowest_prc = l[5]
        buy1 = l[6]
        sell1 = l[7]
        stock_dealed = l[8]
        price_dealed = l[9]
        date = l[10]
        time = l[11]
        #print stk_name,open_prc,close_prc,current_prc,highest_prc,lowest_prc,buy1,sell1
        conn.execute('''INSERT OR REPLACE INTO stk_prc (
                    stk_num, stk_name, open_prc, close_prc, current_prc, highese_prc, lowest_prc, buy1, sell1, stock_dealed, price_dealed, date, time) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (stk_num,stk_name,open_prc,close_prc,current_prc,highest_prc,lowest_prc,buy1,sell1,stock_dealed,price_dealed,date,time))
        conn.commit()                
c.close()
#print "stk_prc process done!"