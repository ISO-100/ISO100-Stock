# -*- coding:utf-8 -*- 
#Created on 2015/07/30
#Version 1.0
#By Cong

import urllib
import sqlite3
import time 

start_time = time.time()
ltime=time.time()-86400
tYear=time.strftime("%Y", time.localtime(ltime))
#print tYear
lYear="%i"%(int(tYear)-1)
#print lYear

conn = sqlite3.connect('stock.sqlite')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS cal_co_qr")

#e.g.
#R_2014_1Q: 季报营收
#P_2014_1Q：季报利润
#P_rate_1Q：利润率
#FR_2015_4Q：预测营收
#FP_2015_3Q：预测利润
#forecast_EPS：预测EPS
#lastyear_yoy：季报利润增加同比
#forecast_PE：预测PE
#target_price：目标价位
creat_sql = '''CREATE TABLE cal_co_qr(
               stk_num CHAR PRIMARY KEY,
               stk_name CHAR,
               %s NUM,%s NUM,P_rate_1Q NUM,
               %s NUM,%s NUM,P_rate_2Q NUM,
               %s NUM,%s NUM,P_rate_3Q NUM,
               %s NUM,%s NUM,P_rate_4Q NUM,
               %s NUM,%s NUM,P_rate_5Q NUM,
               %s NUM,%s NUM,P_rate_6Q NUM,
               %s NUM,%s NUM,P_rate_7Q NUM,
               %s NUM,%s NUM,
               %s NUM,%s NUM,
               forecast_EPS NUM,
               lastyear_yoy NUM,
               forecast_PE NUM,
               target_price NUM
               )'''%("R_"+lYear+"_1Q","P_"+lYear+"_1Q",
                     "R_"+lYear+"_2Q","P_"+lYear+"_2Q",
                     "R_"+lYear+"_3Q","P_"+lYear+"_3Q",
                     "R_"+lYear+"_4Q","P_"+lYear+"_4Q",
                     "R_"+tYear+"_1Q","P_"+tYear+"_1Q",
                     "R_"+tYear+"_2Q","P_"+tYear+"_2Q",
                     "R_"+tYear+"_3Q","P_"+tYear+"_3Q",
                     "FR_"+tYear+"_4Q","FP_"+tYear+"_4Q",
                     "R_"+tYear+"_4Q","P_"+tYear+"_4Q")

#Creat table 'cal_co_qr'
c.execute(creat_sql)

def query_lst(arg1,arg2,arg3):
    dd = conn.cursor()
    dd.execute("SELECT operation_revenue,net_profit from CO_QR WHERE stk_num=%s AND QUARTER='%s'"% (arg1,arg2+arg3))
    rows = dd.fetchall()
    return rows

stk_cpt_check = ""
stk_idt_check = ""
print "It will takes few mins, please wait..."
    
for stk_lst in c.execute("SELECT stk_num,stk_name from stk_lst"):
    stk_num = stk_lst[0]
    stk_name = stk_lst[1]
    #print stk_num
    R_lYear_1Q = P_lYear_1Q = ""
    R_lYear_2Q = P_lYear_2Q = ""
    R_lYear_3Q = P_lYear_3Q = ""
    R_lYear_4Q = P_lYear_4Q = ""
    R_tYear_1Q = P_tYear_1Q = ""
    R_tYear_2Q = P_tYear_2Q = ""
    R_tYear_3Q = P_tYear_3Q = ""
    R_tYear_4Q = P_tYear_4Q = ""
    FR_tYear_4Q = FP_tYear_4Q = ""
    forecast_EPS = lastyear_yoy = forecast_PE = target_price = ""

    temp = query_lst(stk_num,lYear,"-1Q")
    if len(temp)>0:
        R_lYear_1Q = temp[0][0]
        P_lYear_1Q = temp[0][1]
        try:P_rate_1Q = P_lYear_1Q/R_lYear_1Q
        except:P_rate_1Q = "N/A"
    else:
        R_lYear_1Q = "N/A"
        P_lYear_1Q = "N/A"
        P_rate_1Q = "N/A"
            
    temp = query_lst(stk_num,lYear,"-2Q")
    if len(temp)>0:
        R_lYear_2Q = temp[0][0]
        P_lYear_2Q = temp[0][1]
        try:P_rate_2Q = P_lYear_2Q/R_lYear_2Q
        except:P_rate_2Q = "N/A"
    else:
        R_lYear_2Q = "N/A"
        P_lYear_2Q = "N/A"
        P_rate_2Q = "N/A"

    temp = query_lst(stk_num,lYear,"-3Q")
    if len(temp)>0:
        R_lYear_3Q = temp[0][0]
        P_lYear_3Q = temp[0][1]
        try:P_rate_3Q = P_lYear_3Q/R_lYear_3Q
        except:P_rate_3Q = "N/A"
    else:
        R_lYear_3Q = "N/A"
        P_lYear_3Q = "N/A"
        P_rate_3Q = "N/A"

    temp = query_lst(stk_num,lYear,"-4Q")
    if len(temp)>0:
        R_lYear_4Q = temp[0][0]
        P_lYear_4Q = temp[0][1]
        try:P_rate_4Q = P_lYear_4Q/R_lYear_4Q
        except:P_rate_4Q = "N/A"
    else:
        R_lYear_4Q = "N/A"
        P_lYear_4Q = "N/A"
        P_rate_4Q = "N/A"

    temp = query_lst(stk_num,tYear,"-1Q")
    if len(temp)>0:
        R_tYear_1Q = temp[0][0]
        P_tYear_1Q = temp[0][1]
        try:P_rate_5Q = P_tYear_1Q/R_tYear_1Q
        except:P_rate_5Q = "N/A"
    else:
        R_tYear_1Q = "N/A"
        P_tYear_1Q = "N/A"
        P_rate_5Q = "N/A"

    temp = query_lst(stk_num,tYear,"-2Q")
    if len(temp)>0:
        R_tYear_2Q = temp[0][0]
        P_tYear_2Q = temp[0][1]
        try:P_rate_6Q = P_tYear_2Q/R_tYear_2Q
        except:P_rate_6Q = "N/A"
    else:
        R_tYear_2Q = "N/A"
        P_tYear_2Q = "N/A"
        P_rate_6Q = "N/A"

    temp = query_lst(stk_num,tYear,"-3Q")
    if len(temp)>0:
        R_tYear_3Q = temp[0][0]
        P_tYear_3Q = temp[0][1]
        try:P_rate_7Q = P_tYear_3Q/R_tYear_3Q
        except:P_rate_7Q = "N/A"
    else:
        R_tYear_3Q = "N/A"
        P_tYear_3Q = "N/A"
        P_rate_7Q = "N/A"

    temp = query_lst(stk_num,tYear,"-4Q")
    if len(temp)>0:
        R_tYear_4Q = temp[0][0]
        P_tYear_4Q = temp[0][1]
    else:
        R_tYear_4Q = "N/A"
        P_tYear_4Q = "N/A"

#'stk_cpt' table unavailable
    c_temp = conn.cursor()
    try:
        c_temp.execute("SELECT stk_cpt from stk_cpt WHERE stk_num=%s"%stk_num)
    except:
        stk_cpt_check = "no such table: stk_cpt"    
    temp = c_temp.fetchall()
    if len(temp)>0:
        stk_cpt = temp[0][0]
    else:
        stk_cpt = "N/A"

    c_temp = conn.cursor()
    c_temp.execute("SELECT year_on_year2 from CO_QR WHERE stk_num=%s AND QUARTER='%s'"%(stk_num,lYear+"-4Q"))
    temp = c_temp.fetchall()
    if len(temp)>0:
        lastyear_yoy = temp[0][0]
    else:
        lastyear_yoy = "N/A"

    c_temp = conn.cursor()
    c_temp.execute("SELECT current_prc from stk_prc WHERE stk_num=%s"%stk_num)
    temp = c_temp.fetchall()
    if len(temp)>0:
        current_prc = temp[0][0]
    else:
        current_prc = "N/A"

#'stk_idt' table unavailable 
    c_temp = conn.cursor()
    try:
        c_temp.execute("SELECT avg_pe from stk_idt WHERE stk_num=%s"%stk_num)
    except:
        stk_idt_check = "no such table: stk_idt"
    temp = c_temp.fetchall()
    if len(temp)>0:
        avg_pe = temp[0][0]
    else:
        avg_pe = "N/A"

    #排除上年4Q无数据股票
    if R_lYear_4Q != "N/A":
        #使用3Q计算
        if R_tYear_3Q != "N/A":
            if R_lYear_3Q != "N/A":
                if R_lYear_3Q != "0":
                    FR_tYear_4Q = R_lYear_4Q / R_lYear_3Q * R_tYear_3Q
                else:
                    FR_tYear_4Q = "N/A"
            else:
                FR_tYear_4Q = "N/A"
                
            if P_lYear_3Q != "N/A":
                if P_lYear_3Q != "0":
                    FP_tYear_4Q = P_lYear_4Q / P_lYear_3Q * P_tYear_3Q
                else:
                    FP_tYear_4Q = "N/A"
            else:
                FP_tYear_4Q = "N/A"

        #使用2Q计算
        elif R_tYear_2Q != "N/A":
            if R_lYear_2Q != "N/A":
                if R_lYear_2Q != "0":
                    FR_tYear_4Q = R_lYear_4Q / R_lYear_2Q * R_tYear_2Q
                else:
                    FR_tYear_4Q = "N/A"
            else:
                FR_tYear_4Q = "N/A"
                
            if P_lYear_2Q != "N/A":
                if P_lYear_2Q != "0":
                    FP_tYear_4Q = P_lYear_4Q / P_lYear_2Q * P_tYear_2Q
                else:
                    FP_tYear_4Q = "N/A"
            else:
                FP_tYear_4Q = "N/A"

        #使用1Q计算
        elif R_tYear_1Q != "N/A":
            if R_lYear_1Q != "N/A":
                if R_lYear_1Q != "0":
                    FR_tYear_4Q = R_lYear_4Q / R_lYear_1Q * R_tYear_1Q
                else:
                    FR_tYear_4Q = "N/A"
            else:
                FR_tYear_4Q = "N/A"
                
            if P_lYear_1Q != "N/A":
                if P_lYear_1Q != "0":
                    FP_tYear_4Q = P_lYear_4Q / P_lYear_1Q * P_tYear_1Q
                else:
                    FP_tYear_4Q = "N/A"
            else:
                FP_tYear_4Q = "N/A"

        else:
            FR_tYear_4Q = "N/A"
            FP_tYear_4Q = "N/A"

    #计算财报预测EPS
    if FP_tYear_4Q != "N/A" and stk_cpt != "N/A":
        forecast_EPS = "%i"%(int(FP_tYear_4Q) / int(stk_cpt))
    else:
        forecast_EPS = "N/A"

    #计算季报预测PE
    if current_prc != "N/A" and forecast_EPS != "N/A":
        forecast_PE = "%i"%(int(current_prc) / int(forecast_EPS))
    else:
        forecast_PE = "N/A"

    #计算目标价位
    if avg_pe != "N/A" and forecast_EPS != "N/A":
        target_price = "%i"%(int(avg_pe) * int(forecast_EPS))
    else:
        target_price = "N/A"

    insert_sql = '''INSERT OR REPLACE INTO cal_co_qr(    
               stk_num, stk_name,
               %s ,%s ,P_rate_1Q,
               %s ,%s ,P_rate_2Q,
               %s ,%s ,P_rate_3Q,
               %s ,%s ,P_rate_4Q,
               %s ,%s ,P_rate_5Q,
               %s ,%s ,P_rate_6Q,
               %s ,%s ,P_rate_7Q,
               %s ,%s ,
               %s ,%s ,
               forecast_EPS ,
               lastyear_yoy ,
               forecast_PE ,
               target_price 
               )VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''%("R_"+lYear+"_1Q","P_"+lYear+"_1Q",                                                                                           
                     "R_"+lYear+"_2Q","P_"+lYear+"_2Q",
                     "R_"+lYear+"_3Q","P_"+lYear+"_3Q",
                     "R_"+lYear+"_4Q","P_"+lYear+"_4Q",
                     "R_"+tYear+"_1Q","P_"+tYear+"_1Q",
                     "R_"+tYear+"_2Q","P_"+tYear+"_2Q",
                     "R_"+tYear+"_3Q","P_"+tYear+"_3Q",
                     "FR_"+tYear+"_4Q","FP_"+tYear+"_4Q",
                     "R_"+tYear+"_4Q","P_"+tYear+"_4Q")
    #print insert_sql
    conn.execute(insert_sql,              
             (stk_num,stk_name,
              R_lYear_1Q,P_lYear_1Q,P_rate_1Q,
              R_lYear_2Q,P_lYear_2Q,P_rate_2Q,
              R_lYear_3Q,P_lYear_3Q,P_rate_3Q,
              R_lYear_4Q,P_lYear_4Q,P_rate_4Q,
              R_tYear_1Q,P_tYear_1Q,P_rate_5Q,
              R_tYear_2Q,P_tYear_2Q,P_rate_6Q,
              R_tYear_3Q,P_tYear_3Q,P_rate_7Q,
              FR_tYear_4Q,FP_tYear_4Q,
              R_tYear_4Q,P_tYear_4Q,
              forecast_EPS,lastyear_yoy,forecast_PE,target_price))
    conn.commit()
        
c.close()
print stk_cpt_check
print stk_idt_check 
print "Done!"
print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))