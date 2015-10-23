# -*- coding:utf-8 -*-
#Update on 2015/08/17
#Version 2.0
#By Cong

from Tkinter import *
import sqlite3
import time 

start_time = time.time()

EPS_R = PEG_R = P_EPS_R = A_EPS_R = pf_R = C_PE_R = Q_PE_R = EE_R = MV_R = ids_R = st_R = ""
EPS_P = PEG_P = P_EPS_P = A_EPS_P = pf_P = C_PE_P = Q_PE_P = EE_P = MV_P = ids_P = st_P = ""

def a():
    global EPS_R, PEG_R, P_EPS_R, A_EPS_R, pf_R, C_PE_R, Q_PE_R, EE_R, MV_R, ids_R, st_R
    EPS_R = E_EPS_R.get()
    PEG_R = E_PEG_R.get()
    P_EPS_R = E_P_EPS_R.get()
    A_EPS_R = E_A_EPS_R.get()
    pf_R = E_pf_R.get()
    C_PE_R = E_C_PE_R.get()
    Q_PE_R = E_Q_PE_R.get()
    EE_R = E_EE_R.get()
    MV_R = E_MV_R.get()
    ids_R = E_ids_R.get()
    st_R = E_st_R.get()
    global EPS_P, PEG_P, P_EPS_P, A_EPS_P, pf_P, C_PE_P, Q_PE_P, EE_P, MV_P, ids_P, st_P
    EPS_P = E_EPS_P.get()
    PEG_P = E_PEG_P.get()
    P_EPS_P = E_P_EPS_P.get()
    A_EPS_P = E_A_EPS_P.get()
    pf_P = E_pf_P.get()
    C_PE_P = E_C_PE_P.get()
    Q_PE_P = E_Q_PE_P.get()
    EE_P = E_EE_P.get()
    MV_P = E_MV_P.get()
    ids_P = E_ids_P.get()
    st_P = E_st_P.get()
    root.destroy()
        
root = Tk()
root.title("输入参数")

Label(root,text = " ").grid(row=0,column=0)
Label(root,text = "13~14EPS增长率大于").grid(row=1,column=0)
Label(root,text = "机构预测PEG小于").grid(row=2,column=0)
Label(root,text = "财报预测EPS大于").grid(row=3,column=0)
Label(root,text = "机构平均14年EPS大于").grid(row=4,column=0)
Label(root,text = "季报利润同比增加%大于").grid(row=5,column=0)
Label(root,text = "机构预测PE小于").grid(row=6,column=0)
Label(root,text = "季报预测PE小于").grid(row=7,column=0)
Label(root,text = "财报预测EPS/机构平均EPS大于").grid(row=8,column=0)
Label(root,text = "总市值小于").grid(row=9,column=0)
Label(root,text = "行业分大于").grid(row=10,column=0)
Label(root,text = "总股本小于").grid(row=11,column=0)

Label(root,text = "筛选标准:",bg="red").grid(row=0,column=1)
Label(root,text = "筛选标准:",bg="pink").grid(row=0,column=2)

E_EPS_R = Entry(root,textvariable="0.4")    #13~14EPS增长率大于,红色,下同
E_PEG_R = Entry(root)    #机构预测PEG小于
E_P_EPS_R = Entry(root)  #财报预测EPS大于
E_A_EPS_R = Entry(root)  #机构平均14年EPS大于
E_pf_R = Entry(root)     #季报利润同比增加%大于
E_C_PE_R = Entry(root)   #机构预测PE小于
E_Q_PE_R = Entry(root)   #季报预测PE小于
E_EE_R = Entry(root)     #财报预测EPS/机构平均EPS大于
E_MV_R = Entry(root)     #总市值小于
E_ids_R = Entry(root)    #行业分大于
E_st_R = Entry(root)     #总股本小于

a1=StringVar()
a2=StringVar()
a3=StringVar()
a4=StringVar()
a5=StringVar()
a6=StringVar()
a7=StringVar()
a8=StringVar()
a1.set(0.4)
E_EPS_R.config(textvariable=a1)
a2.set(0.6)
E_PEG_R.config(textvariable=a2)
a3.set(0.3)
E_P_EPS_R.config(textvariable=a3)
a4.set(0.3)
E_A_EPS_R.config(textvariable=a4)
a5.set(40)
E_pf_R.config(textvariable=a5)
a6.set(20)
E_C_PE_R.config(textvariable=a6)
a7.set(20)
E_Q_PE_R.config(textvariable=a7)
a8.set(1.1)
E_EE_R.config(textvariable=a8)

E_EPS_P = Entry(root)    #13~14EPS增长率大于,粉色,下同
E_PEG_P = Entry(root)    #机构预测PEG小于
E_P_EPS_P = Entry(root)  #财报预测EPS大于
E_A_EPS_P = Entry(root)  #机构平均14年EPS大于
E_pf_P = Entry(root)     #季报利润同比增加%大于
E_C_PE_P = Entry(root)   #机构预测PE小于
E_Q_PE_P = Entry(root)   #季报预测PE小于
E_EE_P = Entry(root)     #财报预测EPS/机构平均EPS大于
E_MV_P = Entry(root)     #总市值小于
E_ids_P = Entry(root)    #行业分大于
E_st_P = Entry(root)     #总股本小于

b1=StringVar()
b2=StringVar()
b3=StringVar()
b4=StringVar()
b5=StringVar()
b6=StringVar()
b7=StringVar()
b8=StringVar()
b1.set(0.3)
E_EPS_P.config(textvariable=b1)
b2.set(0.8)
E_PEG_P.config(textvariable=b2)
b3.set(0.2)
E_P_EPS_P.config(textvariable=b3)
b4.set(0.2)
E_A_EPS_P.config(textvariable=b4)
b5.set(20)
E_pf_P.config(textvariable=b5)
b6.set(40)
E_C_PE_P.config(textvariable=b6)
b7.set(40)
E_Q_PE_P.config(textvariable=b7)
b8.set(1)
E_EE_P.config(textvariable=b8)

E_EPS_R.grid(row=1,column=1)
E_PEG_R.grid(row=2,column=1)
E_P_EPS_R.grid(row=3,column=1)
E_A_EPS_R.grid(row=4,column=1)
E_pf_R.grid(row=5,column=1)
E_C_PE_R.grid(row=6,column=1)
E_Q_PE_R.grid(row=7,column=1)
E_EE_R.grid(row=8,column=1)
E_MV_R.grid(row=9,column=1)
E_ids_R.grid(row=10,column=1)
E_st_R.grid(row=11,column=1)

E_EPS_P.grid(row=1,column=2)
E_PEG_P.grid(row=2,column=2)
E_P_EPS_P.grid(row=3,column=2)
E_A_EPS_P.grid(row=4,column=2)
E_pf_P.grid(row=5,column=2)
E_C_PE_P.grid(row=6,column=2)
E_Q_PE_P.grid(row=7,column=2)
E_EE_P.grid(row=8,column=2)
E_MV_P.grid(row=9,column=2)
E_ids_P.grid(row=10,column=2)
E_st_P.grid(row=11,column=2)

Button(root,text = '确定',command = a).grid(row=3,column=3)

root.mainloop()

print "It will takes few mins, please wait..."

conn = sqlite3.connect('stock.sqlite')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS rst_stk_flt")

creat_sql = '''CREATE TABLE rst_stk_flt(
               color CHAR,
               stk_num CHAR PRIMARY KEY,
               stk_name CHAR,
               current_prc NUM,
               total_value NUM,
               industry_PE NUM,
               industry CHAR,
               forecast_EPS NUM,
               lastyear_yoy NUM,
               forecast_PE NUM,
               target_price NUM,
               mid_value NUM,
               target_price_range NUM,
               eps_y15_evg NUM,
               y14_to_y15_growth NUM,
               org_predict_pe NUM,
               org_predict_peg NUM,
               target_price_peg NUM
               )'''

#Creat table 'rst_stk_flt'
c.execute(creat_sql)

stk_prc_check = ""
stk_idt_check = ""
cal_co_qr_check = ""
cal_co_er_check = ""
cal_int_eps_check = ""

for stk_lst in c.execute("SELECT stk_num,stk_name from stk_lst"):

    stk_num = stk_lst[0]
    stk_name = stk_lst[1]
    color = ""
    current_prc = ""
    total_value = ""
    industry_PE = ""
    industry = ""
    forecast_EPS = ""
    lastyear_yoy = ""
    forecast_PE = ""
    target_price = ""
    mid_value = ""
    target_price_range = ""
    eps_y15_evg = ""
    y14_to_y15_growth = ""
    org_predict_pe = ""
    org_predict_peg = ""
    target_price_peg = ""

    #dd = conn.cursor()
    
    try:
        t1 = conn.cursor()
        t1.execute("SELECT current_prc from stk_prc WHERE stk_num=%s "%(stk_num))
        rows = t1.fetchall()
        if len(rows)>0:
            current_prc = rows[0][0]
        else:
            current_prc = "N/A"
    except:
        stk_prc_check =  "no such table: stk_prc"
        current_prc = "N/A"
        
    total_value = "N/A"  #暂无数据
    
    try:
        t2 = conn.cursor()
        t2.execute("SELECT industry_PE,industry from stk_idt WHERE stk_num=%s "%(stk_num))   #暂无表格：stk_idt
        rows = t2.fetchall()
        if len(rows)>0:
            industry_PE = rows[0][0]
            industry = rows[0][1]
        else:
            industry_PE = industry = "N/A"
    except:
        stk_idt_check =  "no such table: stk_idt"
        industry_PE = industry = "N/A"

    try:
        t3 = conn.cursor()
        t3.execute("SELECT forecast_EPS,lastyear_yoy,forecast_PE,target_price from cal_co_qr WHERE stk_num=%s "%(stk_num))
        rows = t3.fetchall()
        if len(rows)>0:            
            forecast_EPS = rows[0][0]
            lastyear_yoy = rows[0][1]
            forecast_PE = rows[0][2]
            target_price = rows[0][3]
        else:
            forecast_EPS = "N/A"
            lastyear_yoy = "N/A"
            forecast_PE = "N/A"
            target_price = "N/A"
    except:
        cal_co_qr_check =  "no such table: cal_co_qr"
        forecast_EPS = "N/A"
        lastyear_yoy = "N/A"
        forecast_PE = "N/A"
        target_price = "N/A"

    try:
        t4 = conn.cursor()
        t4.execute("SELECT mid_value,target_price_range from cal_co_er WHERE stk_num=%s "%(stk_num))
        rows = t4.fetchall()
        if len(rows)>0:
            mid_value = rows[0][0]
            target_price_range = rows[0][1]
        else:
            mid_value = target_price_range = "N/A"
    except:
        cal_co_er_check =  "no such table: cal_co_er"
        mid_value = target_price_range = "N/A"

    try:
        t5 = conn.cursor()
        t5.execute("SELECT eps_y15_evg,y14_to_y15_growth,org_predict_pe,org_predict_peg,target_price from cal_int_eps WHERE stk_num=%s "%(stk_num))   
        rows = t5.fetchall()
        if len(rows)>0:
            eps_y15_evg = rows[0][0]
            y14_to_y15_growth = rows[0][1]
            org_predict_pe = rows[0][2]
            org_predict_peg = rows[0][3]
            target_price_peg = rows[0][4]
        else:
            eps_y15_evg = "N/A"
            y14_to_y15_growth = "N/A"
            org_predict_pe = "N/A"
            org_predict_peg = "N/A"
            target_price_peg = "N/A"
    except:
        cal_int_eps_check =  "no such table: cal_int_eps"
        eps_y15_evg = "N/A"
        y14_to_y15_growth = "N/A"
        org_predict_pe = "N/A"
        org_predict_peg = "N/A"
        target_price_peg = "N/A"

    #红色组合条件
    try:
        red1 = forecast_EPS/eps_y15_evg > EE_R
        red2 = y14_to_y15_growth > EPS_R
        red3 = org_predict_peg < PEG_R
        red4 = forecast_EPS > P_EPS_R
        red5 = eps_y15_evg > A_EPS_R
        red6 = lastyear_yoy > pf_R
        red7 = org_predict_pe < C_PE_R
        red8 = forecast_PE < Q_PE_R
    except:
        red1 = red2 = red3 = red4 = red5 = red6 = red7 = red8 = False

    #粉色组合条件
    try:
        pink1 = forecast_EPS/eps_y15_evg > EE_P
        pink2 = y14_to_y15_growth > EPS_P
        pink3 = org_ppinkict_peg < PEG_P
        pink4 = forecast_EPS > P_EPS_P
        pink5 = eps_y15_evg > A_EPS_P
        pink6 = lastyear_yoy > pf_P
        pink7 = org_ppinkict_pe < C_PE_P
        pink8 = forecast_PE < Q_PE_P
    except:
        pink1 = pink2 = pink3 = pink4 = pink5 = pink6 = pink7 = pink8 = False

    if red1 and red2 and red3 and red4 and red5 and red6 and red7 and red8:
        color = "RDE"
    elif pink1 and pink2 and pink3 and pink4 and pink5 and pink6 and pink7 and pink8:
        color = "PINK"
    else:
        color = "N/A"

    insert_sql = '''INSERT OR REPLACE INTO rst_stk_flt(    
               color,
               stk_num ,
               stk_name ,
               current_prc ,
               total_value ,
               industry_PE ,
               industry ,
               forecast_EPS ,
               lastyear_yoy ,
               forecast_PE ,
               target_price ,
               mid_value ,
               target_price_range ,
               eps_y15_evg ,
               y14_to_y15_growth ,
               org_predict_pe ,
               org_predict_peg ,
               target_price_peg 
               ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    conn.execute(insert_sql,
              (color,
               stk_num ,
               stk_name ,
               current_prc ,
               total_value ,
               industry_PE ,
               industry ,
               forecast_EPS ,
               lastyear_yoy ,
               forecast_PE ,
               target_price ,
               mid_value ,
               target_price_range ,
               eps_y15_evg ,
               y14_to_y15_growth ,
               org_predict_pe ,
               org_predict_peg ,
               target_price_peg ))
    conn.commit()

c.close()
print stk_prc_check 
print stk_idt_check 
print cal_co_qr_check 
print cal_co_er_check 
print cal_int_eps_check
print "Done!"
print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))