# -*- coding:utf-8 -*- 
#Created on 2015/07/28
#By Tea Shaw
#This script is to calculate and average all the eps predicted by every organization

import sqlite3
import time

def __init_table__():
    con = sqlite3.connect('stock.sqlite')
    con.execute('''CREATE TABLE IF NOT EXISTS cal_int_eps(
            stk_num CHAR PRIMARY KEY,
            stk_name CHAR,
            eps_y14_evg NUM,
            eps_y15_evg NUM,
            eps_y16_evg NUM,
            eps_y17_evg NUM,
            y14_to_y15_growth NUM,
            y15_to_y16_growth NUM,
            y16_to_y17_growth NUM,
            avg_growth_rate NUM,
            compound_growth_rate NUM,
            org_predict_pe NUM,
            org_predict_peg NUM,
            target_price NUM
            )''')
def eps_everage():
    con = sqlite3.connect('stock.sqlite')
    cur = con.cursor()
    stock = dict()
    k = 0
    for stk_num, stk_name in cur.execute("SELECT stk_num,stk_name from stk_lst"):
        if not (stk_num.startswith("6") or stk_num.startswith("0")): continue
        stock[stk_num] = stk_name
    
    for stk_num in stock:
        k = k +1
        print "%s times" %k
        stk_name = stock[stk_num]
        print stk_num
        print stk_name
        eps_y14_lst = list()
        eps_y15_lst = list()
        eps_y16_lst = list()
        eps_y17_lst = list()
        i = 0
        cur.execute("SELECT COUNT(*) from int_eps where stk_num = ?", (stk_num,))
        number = cur.fetchone()[0]
        if number == 0: continue
        print number
        cur.execute("SELECT * from int_eps where stk_num = ?", (stk_num,))
        
        while i < number:
            item = cur.fetchone()
            eps_y14_lst.append(item[2])
            eps_y15_lst.append(item[3])
            eps_y16_lst.append(item[4])
            eps_y17_lst.append(item[5])
            i = i + 1
        eps_y14_lst = filter(lambda a: a != "--", eps_y14_lst)
        eps_y15_lst = filter(lambda a: a != "--", eps_y15_lst)
        eps_y16_lst = filter(lambda a: a != "--", eps_y16_lst)
        eps_y17_lst = filter(lambda a: a != "--", eps_y17_lst)
        if len(eps_y14_lst) > 0:
            eps_y14_evg = reduce(lambda x, y: x + y, eps_y14_lst) / len(eps_y14_lst)
        else:
            eps_y14_evg = "--"
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
            
        print eps_y14_evg
        print eps_y15_evg
        print eps_y16_evg
        print eps_y17_evg
        
        try:
            y14_to_y15_growth = (eps_y15_evg - eps_y14_evg) / eps_y14_evg
        except (TypeError, ZeroDivisionError):
            y14_to_y15_growth = "--"
        try:
            y15_to_y16_growth = (eps_y16_evg - eps_y15_evg) / eps_y15_evg
        except (TypeError, ZeroDivisionError):
            y15_to_y16_growth = "--"
        try:
            y16_to_y17_growth = (eps_y17_evg - eps_y16_evg) / eps_y16_evg
        except (TypeError, ZeroDivisionError):
            y16_to_y17_growth = "--"
            
        print y14_to_y15_growth
        print y15_to_y16_growth
        print y16_to_y17_growth
        
        eps_everage_lst = filter(lambda a: a != "--", [eps_y14_evg, eps_y15_evg,eps_y16_evg,eps_y17_evg])
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
        
        cur.execute("SELECT current_prc FROM stk_prc where stk_num = ?", (stk_num,))
        try:
            stk_price = cur.fetchone()[0]
        except TypeError:
            print "%s - %s has no current price" %(stk_num,stk_name)
            continue
        
        #PE = Price / EPS
        try:
            org_predict_pe = stk_price / eps_y15_evg
        except (TypeError, ZeroDivisionError):
            org_predict_pe = "--"
            
        #PEG = PE / 14to15 Grow Rate
        try:
            org_predict_peg = org_predict_pe / y14_to_y15_growth
        except (TypeError, ZeroDivisionError):
            org_predict_peg ="--"
        
        #Price = PE * 14to15 Grow Rate
        try:
            target_price = eps_y15_evg * y14_to_y15_growth * 100
        except TypeError:
            target_price = "--"
        con.execute('''INSERT OR REPLACE INTO cal_int_eps (
                stk_num,stk_name,eps_y14_evg,eps_y15_evg,eps_y16_evg,eps_y17_evg,y14_to_y15_growth,y15_to_y16_growth,y16_to_y17_growth,avg_growth_rate,compound_growth_rate,org_predict_pe,org_predict_peg,target_price)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (stk_num,stk_name,eps_y14_evg,eps_y15_evg,eps_y16_evg,eps_y17_evg,y14_to_y15_growth,y15_to_y16_growth,y16_to_y17_growth,avg_growth_rate,compound_growth_rate,org_predict_pe,org_predict_peg,target_price))
        con.commit()
        
    con.close()
    
def main():
    __init_table__()
    eps_everage()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))