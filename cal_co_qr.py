# -*- coding:utf-8 -*- 
#Update on 2015/08/04
#Version 2.0
#By Cong
#Last modified by Teague Xiao on 20161107


from datetime import date
import MySQLdb
import os
import ConfigParser
import time

start_time = time.time()
#ltime=time.time()-86400
#tYear=time.strftime("%Y", time.localtime(ltime))
#print tYear
#lYear="%i"%(int(tYear)-1)
#print lYear
tYear = str(date.today().year)
lYear = str(date.today().year - 1)

Config = ConfigParser.ConfigParser()
Config.read("settings.ini")
con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
c = con.cursor()
#c.execute("DROP TABLE IF EXISTS cal_co_qr")

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
creat_sql = '''CREATE TABLE IF NOT EXISTS cal_co_qr(
               stk_num CHAR(20) PRIMARY KEY,
               stk_name CHAR(20),
               %s float,%s float,P_rate_1Q float,
               %s float,%s float,P_rate_2Q float,
               %s float,%s float,P_rate_3Q float,
               %s float,%s float,P_rate_4Q float,
               %s float,%s float,P_rate_5Q float,
               %s float,%s float,P_rate_6Q float,
               %s float,%s float,P_rate_7Q float,
               %s float,%s float,
               %s float,%s float,
               forecast_EPS float,
               lastyear_yoy float,
               forecast_PE float,
               target_price float
               )''' %("R_"+lYear+"_1Q","P_"+lYear+"_1Q",
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
    dd = con.cursor()
    print arg1,arg2,arg3
    dd.execute("SELECT operation_revenue,net_profit from co_qr WHERE stk_num=%s AND quarter=%s", (arg1,arg2+arg3,))
    rows = dd.fetchall()
    list = [1,2,3]
    if len(rows)>0:
        list[0] = rows[0][0]
        list[1] = rows[0][1]
        try:list[2] = list[1]/list[0]
        except:list[2] = "N/A"
    else:
        list[0] = "N/A"
        list[1] = "N/A"
        list[2] = "N/A"
        
    print list[0],list[1],list[2]
    return list

stk_cpt_check = ""
stk_idt_check = ""
print "It will takes few mins, please wait..."
    
c.execute("SELECT stk_num,stk_name from stk_lst")

for stk_lst in c.fetchall():

    #stk_lst = ["202003","RC003"]
    stk_num = stk_lst[0]
    stk_name = stk_lst[1]
    print stk_num, stk_name
    #print stk_num
    R_lYear_1Q = P_lYear_1Q = P_rate_1Q = ""
    R_lYear_2Q = P_lYear_2Q = P_rate_2Q = ""
    R_lYear_3Q = P_lYear_3Q = P_rate_3Q = ""
    R_lYear_4Q = P_lYear_4Q = P_rate_4Q = ""
    R_tYear_1Q = P_tYear_1Q = P_rate_5Q = ""
    R_tYear_2Q = P_tYear_2Q = P_rate_6Q = ""
    R_tYear_3Q = P_tYear_3Q = P_rate_7Q = ""
    R_tYear_4Q = P_tYear_4Q = P_rate_8Q = ""
    FR_tYear_4Q = FP_tYear_4Q = ""
    forecast_EPS = lastyear_yoy = forecast_PE = target_price = ""

    list_temp=query_lst(stk_num,lYear,"-1Q")
    R_lYear_1Q=list_temp[0]
    P_lYear_1Q=list_temp[1]
    P_rate_1Q=list_temp[2]
    #print R_lYear_1Q,P_lYear_1Q,P_rate_1Q
            
    list_temp=query_lst(stk_num,lYear,"-2Q")
    R_lYear_2Q=list_temp[0]
    P_lYear_2Q=list_temp[1]
    P_rate_2Q=list_temp[2]

    list_temp=query_lst(stk_num,lYear,"-3Q")
    R_lYear_3Q=list_temp[0]
    P_lYear_3Q=list_temp[1]
    P_rate_3Q=list_temp[2]

    list_temp=query_lst(stk_num,lYear,"-4Q")
    R_lYear_4Q=list_temp[0]
    P_lYear_4Q=list_temp[1]
    P_rate_4Q=list_temp[2]

    list_temp=query_lst(stk_num,tYear,"-1Q")
    R_tYear_1Q=list_temp[0]
    P_tYear_1Q=list_temp[1]
    P_rate_5Q=list_temp[2]

    list_temp=query_lst(stk_num,tYear,"-2Q")
    R_tYear_2Q=list_temp[0]
    P_tYear_2Q=list_temp[1]
    P_rate_6Q=list_temp[2]

    list_temp=query_lst(stk_num,tYear,"-3Q")
    R_tYear_3Q=list_temp[0]
    P_tYear_3Q=list_temp[1]
    P_rate_7Q=list_temp[2]

    list_temp=query_lst(stk_num,tYear,"-4Q")
    R_tYear_4Q=list_temp[0]
    P_tYear_4Q=list_temp[1]
    P_rate_8Q=list_temp[2]

#'stk_cpt' table unavailable
    c_temp = con.cursor()
    try:
        c_temp.execute("SELECT stk_cpt from stk_cpt WHERE stk_num=%s",(stk_num,))
    except:
        stk_cpt_check = "no such table: stk_cpt"    
    temp = c_temp.fetchall()
    if len(temp)>0:
        stk_cpt = temp[0][0]
    else:
        stk_cpt = "N/A"

    c_temp = con.cursor()
    c_temp.execute("SELECT year_on_year2 from co_qr WHERE stk_num=%s AND quarter=%s", (stk_num,lYear+"-4Q",))
    temp = c_temp.fetchall()
    if len(temp)>0:
        lastyear_yoy = temp[0][0]
        #The unit is %. So the raw data 100 means 100%.
        lastyear_yoy = float(lastyear_yoy) / 100
        print "lastyear_yoy", lastyear_yoy
    else:
        lastyear_yoy = "N/A"
        print "lastyear_yoy", lastyear_yoy

    c_temp = con.cursor()
    c_temp.execute("SELECT current_prc from stk_prc WHERE stk_num=%s",(stk_num,))
    temp = c_temp.fetchall()
    if len(temp)>0:
        current_prc = temp[0][0]
    else:
        current_prc = "N/A"
    
    
    c_temp = con.cursor()
    try:
        c_temp.execute("SELECT avt_pe from stk_idt WHERE stk_num=%s",(stk_num,))
    except:
        stk_idt_check = "no such table: stk_idt"
    temp = c_temp.fetchall()
    if len(temp)>0:
        avt_pe = temp[0][0]
    else:
        avt_pe = 0
    
    print "avt_pe", avt_pe
    
    #排除上年4Q无数据股票
    if R_lYear_4Q != "N/A":
        #使用3Q计算
        if R_tYear_3Q != "N/A":
            if R_lYear_3Q != "N/A":
                if R_lYear_3Q != 0:
                    print "R_lYear_3Q",R_lYear_3Q
                    print "R_tYear_3Q",R_tYear_3Q
                    print "R_lYear_4Q",R_lYear_4Q
                    
                    FR_tYear_4Q = float(R_lYear_4Q) / float(R_lYear_3Q) * float(R_tYear_3Q)
                else:
                    FR_tYear_4Q = "N/A"
            else:
                FR_tYear_4Q = "N/A"
                
            if P_lYear_3Q != "N/A":
                if P_lYear_3Q != 0:
                    FP_tYear_4Q = P_lYear_4Q / P_lYear_3Q * P_tYear_3Q
                else:
                    FP_tYear_4Q = "N/A"
            else:
                FP_tYear_4Q = "N/A"

        #使用2Q计算
        elif R_tYear_2Q != "N/A":
            if R_lYear_2Q != "N/A":
                if R_lYear_2Q != 0:
                    FR_tYear_4Q = R_lYear_4Q / R_lYear_2Q * R_tYear_2Q
                else:
                    FR_tYear_4Q = "N/A"
            else:
                FR_tYear_4Q = "N/A"
                
            if P_lYear_2Q != "N/A":
                if P_lYear_2Q != 0:
                    FP_tYear_4Q = P_lYear_4Q / P_lYear_2Q * P_tYear_2Q
                else:
                    FP_tYear_4Q = "N/A"
            else:
                FP_tYear_4Q = "N/A"

        #使用1Q计算
        elif R_tYear_1Q != "N/A":
            if R_lYear_1Q != "N/A":
                if R_lYear_1Q != 0:
                    FR_tYear_4Q = R_lYear_4Q / R_lYear_1Q * R_tYear_1Q
                else:
                    FR_tYear_4Q = "N/A"
            else:
                FR_tYear_4Q = "N/A"
                
            if P_lYear_1Q != "N/A":
                if P_lYear_1Q != 0:
                    FP_tYear_4Q = P_lYear_4Q / P_lYear_1Q * P_tYear_1Q
                else:
                    FP_tYear_4Q = "N/A"
            else:
                FP_tYear_4Q = "N/A"

        else:
            FR_tYear_4Q = "N/A"
            FP_tYear_4Q = "N/A"
    else:
        FR_tYear_4Q = "N/A"
        FP_tYear_4Q = "N/A"

    #计算财报预测EPS
    if FP_tYear_4Q != "N/A" and stk_cpt != "N/A":
        forecast_EPS = "%.2f"%(float(FP_tYear_4Q) / float(stk_cpt))
    else:
        forecast_EPS = "N/A"

    #计算季报预测PE
    if current_prc != "N/A" and forecast_EPS != "N/A" and float(forecast_EPS) != 0.0:
        print "forecast_EPS",forecast_EPS
        #print type(forecast_EPS)
        forecast_PE = "%.2f"%(float(current_prc) / float(forecast_EPS))
    else:
        forecast_PE = "N/A"

    #计算目标价位
    if avt_pe != 0 and forecast_EPS != "N/A":
        target_price = "%.2f"%(float(avt_pe) * float(forecast_EPS))
        print "target_price",target_price
    else:
        target_price = "N/A"
        print "target_price",target_price

    sql_forehead = '''REPLACE INTO cal_co_qr(stk_num,stk_name,%s,%s,P_rate_1Q,%s,%s,P_rate_2Q,%s,%s,P_rate_3Q,%s,%s,P_rate_4Q,%s,%s,P_rate_5Q,%s,%s,P_rate_6Q,%s,%s,P_rate_7Q,%s,%s,%s,%s,forecast_EPS,lastyear_yoy,forecast_PE,target_price)''' %("R_"+lYear+"_1Q","P_"+lYear+"_1Q","R_"+lYear+"_2Q","P_"+lYear+"_2Q","R_"+lYear+"_3Q","P_"+lYear+"_3Q","R_"+lYear+"_4Q","P_"+lYear+"_4Q","R_"+tYear+"_1Q","P_"+tYear+"_1Q","R_"+tYear+"_2Q","P_"+tYear+"_2Q","R_"+tYear+"_3Q","P_"+tYear+"_3Q","FR_"+tYear+"_4Q","FP_"+tYear+"_4Q","R_"+tYear+"_4Q","P_"+tYear+"_4Q")
    #print insert_sql
    
    #print sql_forehead
    
    sql_tail = '''VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")''' %(stk_num,stk_name,R_lYear_1Q,P_lYear_1Q,P_rate_1Q,R_lYear_2Q,P_lYear_2Q,P_rate_2Q,R_lYear_3Q,P_lYear_3Q,P_rate_3Q,R_lYear_4Q,P_lYear_4Q,P_rate_4Q,R_tYear_1Q,P_tYear_1Q,P_rate_5Q,R_tYear_2Q,P_tYear_2Q,P_rate_6Q,R_tYear_3Q,P_tYear_3Q,P_rate_7Q,FR_tYear_4Q,FP_tYear_4Q,R_tYear_4Q,P_tYear_4Q,forecast_EPS,lastyear_yoy,forecast_PE,target_price)
    
    #print sql_tail
    
    insert_sql = sql_forehead + sql_tail
    
    #print insert_sql
    
    c.execute(insert_sql)
    con.commit()
        
c.close()
print stk_cpt_check
print stk_idt_check 
print "Done!"
print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))