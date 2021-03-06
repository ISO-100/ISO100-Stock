# -*- coding:utf-8 -*- 
#Created on 2015/08/02
#By Teague Xiao
#This script is to calculate and the er data
#Last updated on 20161026

from datetime import date
import MySQLdb
import os
import ConfigParser
import time
    
def cal_co_er():
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    c = con.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS cal_co_er(
            stk_num CHAR(20) PRIMARY KEY,
            stk_name CHAR(20),
            low_range float(10,2),
            high_range float(10,2),
            mid_value float(10,2),
            difference BOOLEAN,
            alert BOOLEAN,
            profit_last_year float(20,2),
            eps_last_year float(10,2),
            low_net_margin_this_year float(20,2),
            high_net_margin_this_year float(20,2),
            low_eps_this_year float(10,2),
            high_eps_this_year float(10,2),
            low_target_price float(10,2),
            high_target_price float(10,2),
            target_price_range CHAR(20)
            )''')
    
    stock = dict()
    c.execute("SELECT stk_num,stk_name from co_er")
    for stk_num ,stk_name in c.fetchall():
        stock[stk_num] = stk_name
        #print stk_num, stk_name
    
    for stk_num in stock:
        stk_name = stock[stk_num]
        print stk_num
        print stk_name
        c.execute("SELECT change_range from co_er where stk_num = %s ORDER BY announce_date DESC LIMIT 1", (stk_num,))
        #!!!!!!!!!!!Should select the newest one
        change_range = c.fetchone()[0]
        print change_range
        
        if change_range == "--": 
            #例子：--
            continue
        elif not "~" in change_range: 
            if change_range.endswith("%"):
                #例子：30%
                low_range = high_range = mid_value = float(change_range[:-1]) / 100
            else:
            #例子：30
                low_range = high_range = mid_value = float(change_range) / 100  
        else:
            #例子：20%~30%
            index = change_range.find('~')
            #print index
            low_range = float(change_range[:index-1]) / 100
            print "low_range", low_range
            high_range = float(change_range[index+1:-1]) / 100
            print "high_range", high_range
            mid_value = (low_range + high_range) / 2
            print "mid_value", mid_value
            
        difference = "TBD"
        alert = "TBD"
        last_year = date.today().year - 1
        quarter = str(last_year) + "-4Q"
        c.execute("SELECT net_profit from co_qr where stk_num =%s and QUARTER = %s", (stk_num,quarter,))
        try:
            profit_last_year = c.fetchone()[0]
            profit_last_year = float(profit_last_year)
            # The unit is 10000 RMB
            print "profit_last_year", profit_last_year
        except: 
            profit_last_year = 0
            print "no corresponding QR for %s" %stk_name
            continue
        c.execute("SELECT EPS from co_qr where stk_num =%s and QUARTER = %s", (stk_num,quarter,))
        eps_last_year = c.fetchone()[0]   
        low_net_margin_this_year = profit_last_year * (1+low_range)
        print "low_net_margin_this_year", low_net_margin_this_year
        high_net_margin_this_year = profit_last_year * (1+high_range)
        print "high_net_margin_this_year", high_net_margin_this_year
        #
        c.execute("SELECT stk_cpt from stk_cpt where stk_num =%s", (stk_num,))
        
        try:
            stk_cpt = c.fetchone()[0]
            stk_cpt = float(stk_cpt)
            print "stk_cpt", stk_cpt
            low_eps_this_year = low_net_margin_this_year / stk_cpt
            print "low_eps_this_year", low_eps_this_year
            high_eps_this_year = high_net_margin_this_year / stk_cpt
            print "high_eps_this_year", high_eps_this_year
        except: 
            stk_cpt = "N/A"
            low_eps_this_year = "N/A"
            high_eps_this_year = "N/A"
            print "no corresponding stock capital for %s \n" %stk_name
            continue
        
        #Suppose PEG = 1, Price = PEG * EPS
        low_target_price = low_eps_this_year
        high_target_price = high_eps_this_year
        target_price_range = "%.2f ~ %.2f" % (low_target_price,high_target_price)
        
        print "low_target_price", low_target_price
        print "high_target_price", high_target_price
        print "target_price_range", target_price_range
        
        print "profit_last_year", profit_last_year
        c.execute('''REPLACE INTO cal_co_er (
                    stk_num, stk_name,low_range,high_range,mid_value,difference,alert,profit_last_year,eps_last_year,low_net_margin_this_year ,high_net_margin_this_year,low_eps_this_year,high_eps_this_year,low_target_price,high_target_price,target_price_range)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (stk_num, stk_name,low_range,high_range,mid_value,difference,alert,profit_last_year,eps_last_year,low_net_margin_this_year ,high_net_margin_this_year,low_eps_this_year,high_eps_this_year,low_target_price,high_target_price,target_price_range))
        con.commit()
        print "\n"
        
    c.close()
    
def main():
    cal_co_er()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))