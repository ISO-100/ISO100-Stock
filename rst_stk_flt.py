#Created on 2016/10/24, last modified on 2016/10/24
#By Teague Xiao
#This script is aim to display all the basic information for each stock 

import MySQLdb
import os
import ConfigParser
import time

def main():
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    c = con.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS rst_stk_flt(
                stk_num CHAR(20) PRIMARY KEY,
                stk_name CHAR(20),
                eps_y16_evg float(5,2),
                y15_to_y16_growth float(6,4),
                org_predict_pe float(10,2),
                org_predict_peg float(10,2),
                target_price float(5,2)
                )''')

    c.execute("SELECT stk_num,stk_name from stk_lst")
    stk_num_name = c.fetchall()
    stock = dict()
    
    for stk_num ,stk_name in stk_num_name:
        if not (stk_num.startswith("6") or stk_num.startswith("0")): continue
        stock[stk_num] = stk_name
        stk_name = stock[stk_num]
        c.execute("SELECT eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,target_price from cal_int_eps where stk_num = %s", (stk_num,))
        fetch = c.fetchone()
        print fetch
        if not fetch is None: 
            eps_y16_evg = fetch[0]
            y15_to_y16_growth = fetch[1]
            org_predict_pe = fetch[2]
            org_predict_peg = fetch[3]
            target_price = fetch[4]
            c.execute('''REPLACE INTO rst_stk_flt (
                    stk_num,stk_name,eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,target_price)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                    (stk_num,stk_name,eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,target_price))
            print stk_num,stk_name,eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,target_price
    con.commit()    
    c.close()
    

if __name__ == "__main__":  
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))