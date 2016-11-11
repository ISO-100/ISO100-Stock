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
    
    #c.execute("DROP TABLE IF EXISTS rst_stk_flt")
    
    c.execute('''CREATE TABLE IF NOT EXISTS rst_stk_flt(
                stk_num CHAR(20) PRIMARY KEY,
                stk_name CHAR(20),
                current_prc float,
                cpt_price float(20,2),
                idt_class CHAR(20),
                idt CHAR(20),
                forecast_EPS float,
                lastyear_yoy float,
                forecast_PE float,
                qr_target_price float,
                mid_value float(10,2),
                target_price_range float(10,2),
                eps_y16_evg float(5,2),
                y15_to_y16_growth float(6,4),
                org_predict_pe float(10,2),
                org_predict_peg float(10,2),
                eps_target_price float(5,2)
                )''')

    c.execute("SELECT stk_num,stk_name from stk_lst")
    stk_num_name = c.fetchall()
    stock = dict()
    
    for stk_num ,stk_name in stk_num_name:
        #if not (stk_num.startswith("6") or stk_num.startswith("0")): continue
        stock[stk_num] = stk_name
        stk_name = stock[stk_num]
        
        #Initialize 
        current_prc = cpt_price = idt_class = idt = forecast_EPS = lastyear_yoy = forecast_PE = qr_target_price = "N/A"
        eps_y16_evg = y15_to_y16_growth = org_predict_pe = org_predict_peg = eps_target_price = mid_value = target_price_range = "N/A"
        
        c.execute("SELECT current_prc from stk_prc where stk_num = %s", (stk_num,))
        fetch = c.fetchone()
        if not fetch is None:
            current_prc = fetch[0]
            print "current_prc", current_prc
        
        c.execute("SELECT stk_cpt from stk_cpt where stk_num = %s", (stk_num,))
        fetch = c.fetchone()
        if not fetch is None:
            stk_cpt = fetch[0]
        
        if current_prc != "N/A" and stk_cpt != "N/A":
            cpt_price = float(current_prc) * float(stk_cpt) / 10000
        #Unit is 100 million Yuan
        
        print "cpt_price", cpt_price
        
        #Idt table has not been created yet
        idt_class = idt = "N/A"
        
        c.execute("SELECT forecast_EPS,lastyear_yoy,forecast_PE,target_price from cal_co_qr where stk_num = %s", (stk_num,))
        fetch = c.fetchone()
        
        if not fetch is None: 
            forecast_EPS = fetch[0]
            lastyear_yoy = fetch[1]
            forecast_PE = fetch[2]
            qr_target_price = fetch[3]
            print "forecast_EPS",forecast_EPS
            print "lastyear_yoy",lastyear_yoy
            print "forecast_PE",forecast_PE
            print "qr_target_price",qr_target_price
        
        c.execute("SELECT eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,target_price from cal_int_eps where stk_num = %s", (stk_num,))
        fetch = c.fetchone()
        if not fetch is None: 
            eps_y16_evg = fetch[0]
            y15_to_y16_growth = fetch[1]
            org_predict_pe = fetch[2]
            org_predict_peg = fetch[3]
            eps_target_price = fetch[4]
            
            print "eps_y16_evg", eps_y16_evg
            print "y15_to_y16_growth", y15_to_y16_growth
            print "org_predict_pe", org_predict_pe
            print "org_predict_peg", org_predict_peg
            print "eps_target_price", eps_target_price
            
        c.execute("SELECT mid_value, target_price_range from cal_co_er where stk_num = %s", (stk_num,))
        fetch = c.fetchone()
        
        if not fetch is None:
            mid_value = fetch[0]
            target_price_range = fetch[1]
            print "mid_value", mid_value
            print "target_price_range", target_price_range
            
        c.execute('''REPLACE INTO rst_stk_flt (
                stk_num,stk_name,current_prc,cpt_price,idt_class,idt,forecast_EPS,lastyear_yoy,forecast_PE,qr_target_price,mid_value,target_price_range,eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,eps_target_price)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (stk_num,stk_name,current_prc,cpt_price,idt_class,idt,forecast_EPS,lastyear_yoy,forecast_PE,qr_target_price,mid_value,target_price_range,eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,eps_target_price))
        #print stk_num,stk_name,eps_y16_evg,y15_to_y16_growth,org_predict_pe,org_predict_peg,eps_target_price
    con.commit()    
    c.close()
    

if __name__ == "__main__":  
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))