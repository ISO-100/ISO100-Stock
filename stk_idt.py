# -*- coding:utf-8 -*- 
#Created on 20161112
#By Teague Xiao
#This script is to download stock industry infomation from TuShare API
#Last modified at 2016/11/12 by Teague Xiao

import MySQLdb
import os
import ConfigParser
import time
import tushare as ts

def get_stk_idt(con):
    
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stk_idt(
                stk_num CHAR(20) PRIMARY KEY,
                stk_name CHAR(20),
                stk_idt CHAR(20),
                pe float(10,2),
                avt_pe float(10,2)
                )''')
                
    result = ts.get_industry_classified()
    
    for i in range(0,len(result)-1):
        c.execute("SELECT stk_name from stk_lst where stk_num = %s",(result["code"][i],))
        fetch = c.fetchone()
        if fetch != None:
            stk_name = fetch[0]
            stk_num = result["code"][i]
            stk_idt = result["c_name"][i]
            
            print "stk_num", stk_num
            print "stk_name",stk_name
            print "stk_idt",stk_idt
            
            c.execute('''REPLACE INTO stk_idt (
                stk_num,stk_name,stk_idt) 
                VALUES (%s,%s,%s)''',
                (stk_num,stk_name,stk_idt))
                
            con.commit()
    
def cal_idt_pe(con):
    
    c = con.cursor()
    stock = dict()
    idt_lst = list()
    c.execute("SELECT stk_num,stk_idt from stk_idt")
    for stk_num ,stk_idt in c.fetchall():
        stock[stk_num] = stk_idt
    
    c.execute("SELECT distinct stk_idt from stk_idt")
    #Select all the different stock industry in DB
    for item in c.fetchall():
        idt_lst.append(item)
    print idt_lst    
        
    for stk_idt in idt_lst:
        stk_idt = stk_idt[0]
        c.execute("SELECT stk_num from stk_idt where stk_idt = %s", (stk_idt,))
        pe_lst = list()
        for stock in c.fetchall():
            stock = stock[0]
            print "stk_num",stock
            c.execute("SELECT current_prc from stk_prc where stk_num = %s", (stock,))
            try: price = c.fetchone()[0]
            except: price = 0
            print "price",price
            c.execute("SELECT EPS from co_qr where stk_num = %s ORDER BY QUARTER DESC LIMIT 1", (stock,))
            #Fetch the newest eps of specific stock
            try: eps = c.fetchone()[0]
            except: eps = 0
            print "eps",eps
            if float(eps) != 0.0 and eps != "N/A":
                pe = price / eps
            else:
                pe = 0
            print "pe",pe
            
            pe_lst.append(pe)
            c.execute("UPDATE stk_idt SET pe = %s WHERE stk_num = %s", (pe, stock))
            #c.execute('''UPDATE stk_idt (stk_num, pe) VALUES (%s,%s)''', (stock,pe))

            con.commit()
        print "pe_lst",pe_lst
        
        for item in pe_lst:
            if item == 0: pe_lst.remove(item)
            
        avt_pe = reduce(lambda x, y: x + y, pe_lst) / len(pe_lst)
        
        c.execute("SELECT stk_num from stk_idt where stk_idt = %s", (stk_idt,))

        for stock in c.fetchall():
            stock = stock[0]
            #c.execute('''UPDATE stk_idt (stk_num, avt_pe) VALUES (%s,%s)''', (stock, avt_pe))
            c.execute("UPDATE stk_idt SET avt_pe = %s WHERE stk_num = %s", (avt_pe, stock))
            con.commit()
            
            
def main():
    
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    get_stk_idt(con)
    cal_idt_pe(con)
    con.close
    
if __name__ == "__main__":
    
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))