# -*- coding:utf-8 -*- 
#Created on 2015/08/02
#By Tea Shaw
#This script is to calculate and the er data

import sqlite3
import time
from datetime import date

def __init_table__():
    con = sqlite3.connect('stock.sqlite')
    con.execute('''CREATE TABLE IF NOT EXISTS cal_co_er(
            stk_num CHAR PRIMARY KEY,
            stk_name CHAR,
            low_range NUM,
            high_range NUM,
            mid_value NUM,
            difference NUM,
            alert BOOLE,
            profit_last_year NUM,
            eps_last_year NUM,
            low_net_margin_this_year NUM,
            high_net_margin_this_year NUM,
            low_eps_this_year NUM,
            high_eps_this_year NUM,
            low_target_price NUM,
            high_target_price NUM,
            target_price_range NUM
            )''')
    con.close()
    
def cal_co_er():
    stock = dict()
    con = sqlite3.connect('stock.sqlite')
    cur = con.cursor()
    for stk_num, stk_name in cur.execute("SELECT stk_num,stk_name from co_er"):
        stock[stk_num] = stk_name
    
    for stk_num in stock:
        stk_name = stock[stk_num]
        print stk_num
        print stk_name
        #stk_num = "000005"
        #stk_name = "Temp"
        cur.execute("SELECT * from co_er where stk_num = ?", (stk_num,))
        value_range = cur.fetchone()[7]
        print value_range
        if value_range == "--": 
            #例子：--
            continue
        elif not "~" in value_range: 
            if value_range.endswith("%"):
                #例子：30%
                low_range = high_range = mid_value = float(value_range[:-2]) / 100
            else:
            #例子：30
                low_range = high_range = mid_value = float(value_range) / 100  
        else:
            index = value_range.find('~')
            print index
            low_range = float(value_range[:index-1]) / 100
            print low_range
            high_range = float(value_range[index+1:-1]) / 100
            print high_range
            mid_value = (low_range + high_range) / 2
            print mid_value
        difference = "TBD"
        alert = "TBD"
        last_year = date.today().year - 1
        quarter = str(last_year) + "-4Q"
        cur.execute("SELECT net_profit from co_qr where stk_num =? and QUARTER = ?", (stk_num,quarter,))
        try:profit_last_year = cur.fetchone()[0]
        except: 
            print "no corresponding QR for %s" %stk_name
            continue
        cur.execute("SELECT EPS from co_qr where stk_num =? and QUARTER = ?", (stk_num,quarter,))
        eps_last_year = cur.fetchone()[0]   
        low_net_margin_this_year = profit_last_year * (1+low_range)
        print low_net_margin_this_year
        high_net_margin_this_year = profit_last_year * (1+high_range)
        print high_net_margin_this_year
        cur.execute("SELECT stk_cpt from stk_cpt where stk_num =?", (stk_num,))
       # print cur.fetchone()[0]
        #print type(cur.fetchone()[0])
        match = cur.fetchone()
        if not match is None:
            stk_cpt = match[0]
            low_eps_this_year = low_net_margin_this_year / stk_cpt
            high_eps_this_year = high_net_margin_this_year / stk_cpt
            
        #下面三个有待更改函数和添加需要引用的行业PE数据
        low_target_price = "TBD"
        high_target_price = "TBD"
        target_price_range = "TBD"
        con.execute('''INSERT OR REPLACE INTO cal_co_er (
                    stk_num, stk_name,low_range,high_range,mid_value,difference,alert,profit_last_year,eps_last_year,low_net_margin_this_year ,high_net_margin_this_year,low_eps_this_year,high_eps_this_year,low_target_price,high_target_price,target_price_range)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (stk_num, stk_name,low_range,high_range,mid_value,difference,alert,profit_last_year,eps_last_year,low_net_margin_this_year ,high_net_margin_this_year,low_eps_this_year,high_eps_this_year,low_target_price,high_target_price,target_price_range))
        con.commit()
    
def main():
    __init_table__()
    cal_co_er()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))