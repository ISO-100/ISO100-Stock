# -*- coding:utf-8 -*-
#Create on 2015/08/13
#Version 1.0
#By Cong

from Tkinter import *

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

print EPS_R, PEG_R, P_EPS_R, A_EPS_R, pf_R, C_PE_R, Q_PE_R, EE_R, MV_R, ids_R, st_R
print EPS_P, PEG_P, P_EPS_P, A_EPS_P, pf_P, C_PE_P, Q_PE_P, EE_P, MV_P, ids_P, st_P
