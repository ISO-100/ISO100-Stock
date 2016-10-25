# -*- coding:utf-8 -*- 
#Created on 2015/07/28
#By Teague Xiao
#Last updated on 2016/05/14: Modify from using SQLite to Mysql - Teague Xiao
#This script is to calculate and average all the eps predicted by every organization
#Last Modified on 2016/10/25

#import sqlite3
import MySQLdb
import time
import os
import ConfigParser
import sys

#For fixing 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128) ERROR
reload(sys)
sys.setdefaultencoding('utf-8')
def __init_table__():
    #con = sqlite3.connect('stock.sqlite')
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cal_int_eps(
            stk_num CHAR(20) PRIMARY KEY,
            stk_name CHAR(20),
            eps_y15_evg float(5,2),
            eps_y16_evg float(5,2),
            eps_y17_evg float(5,2),
            eps_y18_evg float(5,2),
            y15_to_y16_growth float(6,4),
            y16_to_y17_growth float(6,4),
            y17_to_y18_growth float(6,4),
            avg_growth_rate float(6,4),
            compound_growth_rate float(6,4),
            org_predict_pe float(10,2),
            org_predict_peg float(10,2),
            target_price float(5,2)
            )''')
    con.close()
    
def eps_everage():
    #con = sqlite3.connect('stock.sqlite')
    #cur = con.cursor()
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    c = con.cursor()
    stock = dict()
    k = 0
    c.execute("SELECT stk_num,stk_name from stk_lst")
    for stk_num ,stk_name in c.fetchall():
        if not (stk_num.startswith("6") or stk_num.startswith("0")): continue
        stock[stk_num] = stk_name
    
    for stk_num in stock:
        k = k +1
        print "%s times" %k
        stk_name = stock[stk_num]
        print stk_num
        print stk_name
        eps_y15_lst = list()
        eps_y16_lst = list()
        eps_y17_lst = list()
        eps_y18_lst = list()
        i = 0
        c.execute("SELECT COUNT(*) from int_eps where stk_num = %s", (stk_num,))
        number = c.fetchone()[0]
        if number == 0: continue
        print number
        c.execute("SELECT * from int_eps where stk_num = %s", (stk_num,))
        
        while i < number:
            item = c.fetchone()
            eps_y15_lst.append(item[2])
            eps_y16_lst.append(item[3])
            eps_y17_lst.append(item[4])
            eps_y18_lst.append(item[5])
            i = i + 1
        eps_y15_lst = filter(lambda a: a != "--", eps_y15_lst)
        eps_y16_lst = filter(lambda a: a != "--", eps_y16_lst)
        eps_y17_lst = filter(lambda a: a != "--", eps_y17_lst)
        eps_y18_lst = filter(lambda a: a != "--", eps_y18_lst)
        if len(eps_y15_lst) > 0:
            eps_y15_evg = reduce(lambda x, y: x + y, eps_y15_lst) / len(eps_y15_lst)
        else:
            eps_y15_evg = "--"
        if len(eps_y16_lst) > 0:
            eps_y16_evg = reduce(lambda x, y: x + y, eps_y16_lst) / len(eps_y16_lst)
        else:
            eps_y16_evg = "--"
        if len(eps_y17_lst) > 0:
            eps_y17_evg = reduce(lambda x, y: x + y, eps_y17_lst) / len(eps_y17_lst)
        else:
            eps_y17_evg = "--"
        if len(eps_y18_lst) > 0:
            eps_y18_evg = reduce(lambda x, y: x + y, eps_y18_lst) / len(eps_y18_lst)
        else:
            eps_y18_evg = "--"
            
        print eps_y15_evg
        print eps_y16_evg
        print eps_y17_evg
        print eps_y18_evg
        
        try:
            y15_to_y16_growth = (eps_y16_evg - eps_y15_evg) / eps_y15_evg
        except (TypeError, ZeroDivisionError):
            y15_to_y16_growth = "--"
        try:
            y16_to_y17_growth = (eps_y17_evg - eps_y16_evg) / eps_y16_evg
        except (TypeError, ZeroDivisionError):
            y16_to_y17_growth = "--"
        try:
            y17_to_y18_growth = (eps_y18_evg - eps_y17_evg) / eps_y17_evg
        except (TypeError, ZeroDivisionError):
            y17_to_y18_growth = "--"
            
        print y15_to_y16_growth
        print y16_to_y17_growth
        print y17_to_y18_growth
        
        eps_everage_lst = filter(lambda a: a != "--", [eps_y15_evg, eps_y16_evg,eps_y17_evg,eps_y18_evg])
        #print eps_everage_lst
        try:
            avg_growth_rate = (eps_everage_lst[-1] / eps_everage_lst[0] - 1) / len(eps_everage_lst)
        except (IndexError, ZeroDivisionError):
            avg_growth_rate = "--"
        
        try:
            compound_growth_rate = (eps_everage_lst[-1] / eps_everage_lst[0]) ** (1.0 / len(eps_everage_lst))
        except (IndexError, ValueError,ZeroDivisionError):
            compound_growth_rate = "--"
           
        print avg_growth_rate
        print compound_growth_rate
        
        c.execute("SELECT current_prc FROM stk_prc where stk_num = %s", (stk_num,))
        try:
            stk_price = c.fetchone()[0]
        except TypeError:
            print "%s - %s has no current price" %(stk_num,stk_name)
            continue
        
        #PE = Price / EPS
        try:
            org_predict_pe = stk_price / eps_y16_evg
        except (TypeError, ZeroDivisionError):
            org_predict_pe = "--"
            
        #PEG = PE / 14to15 Grow Rate
        try:
            org_predict_peg = org_predict_pe / y15_to_y16_growth
        except (TypeError, ZeroDivisionError):
            org_predict_peg ="--"
        
        #Price = PE * 14to15 Grow Rate
        try:
            target_price = eps_y16_evg * y15_to_y16_growth * 100
        except TypeError:
            target_price = "--"
        c.execute('''REPLACE INTO cal_int_eps (
                stk_num,stk_name,eps_y15_evg,eps_y16_evg,eps_y17_evg,eps_y18_evg,y15_to_y16_growth,y16_to_y17_growth,y17_to_y18_growth,avg_growth_rate,compound_growth_rate,org_predict_pe,org_predict_peg,target_price)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (stk_num,stk_name,eps_y15_evg,eps_y16_evg,eps_y17_evg,eps_y18_evg,y15_to_y16_growth,y16_to_y17_growth,y17_to_y18_growth,avg_growth_rate,compound_growth_rate,org_predict_pe,org_predict_peg,target_price))
        con.commit()
        
    c.close()
    
def main():
    __init_table__()
    eps_everage()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))