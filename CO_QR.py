#coding=utf-8
#Created on 2015/07/18
#By Cong
#This script is aim to download the Quarter Report from SINA Stock 

import sys
import os
import urllib
import urllib2
#需要自行安装 bs4
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('stock.sqlite')
c = conn.cursor()

#字段说明：
#EPS: 每股收益（元）
#operation_revenue：营业收入（万元）
#year_on_year：同比（%）
#NAPS：每股净资产（元）
#ROE：Rate of Return on Common Stockholders’Equity,净资产收益率
#CFPS: Cash flow per share,每股现金流量（元）
#GPR: Gross Profit Rate,毛利率（%）
c.execute('''CREATE TABLE IF NOT EXISTS CO_QR(
                stk_num CHAR PRIMARY KEY, 
                stk_name CHAR,
                publication_date TEXT, 
                EPS NUM, 
                operation_revenue NUM,
                year_on_year1 NUM,
                net_profit NUM,
                year_on_year2 NUM,
                NAPS NUM,
                ROE NUM,
                CFPS NUM,
                GPR NUM              
                )''')

year = raw_input("Input Year Likes 2014:")
quarter = raw_input("Input Quarter Likes 3:")
quar = "?"
if quarter=="1":
    quar="-03-31"
elif quarter=="2":
    quar="-06-30"
elif quarter=="3":
    quar="-09-30"
elif quarter=="4":
    quar="-12-31"
    
for link_num in range(1,20):
    link = "http://finance.sina.com.cn/realstock/income_statement/"+year+quar+"/issued_pdate_ac_"+'%d'%link_num+".html"
    #print link
    #req = urllib2.Request(link)
    #res = urllib2.urlopen(req)
    try:
        req = urllib2.Request(link)
        res = urllib2.urlopen(req)        
    except:
        print link
        print 'Invalid Html Link!'
        continue

    #req = urllib2.Request(link)
    #res = urllib2.urlopen(req)
    html = res.read()
    soup= BeautifulSoup(html,from_encoding="gb18030")
    #找到表格的根节点
    trs=soup.find("div",id="box")
    try:
        root=trs.contents[1].contents[3]
    except:
        print "Error Mark:"+link
        print 'System Error!Try again!!!'
        break

    rows = len(root)
    #print rows
    for x in range(1,rows-3):
        #print root.contents[x].contents[0].string
        stk_num = root.contents[x].contents[0].string
        stk_name = root.contents[x].contents[1].string
        publication_date = root.contents[x].contents[2].string
        EPS = root.contents[x].contents[3].string
        operation_revenue = root.contents[x].contents[4].string
        year_on_year1 = root.contents[x].contents[5].string
        net_profit = root.contents[x].contents[6].string
        year_on_year2 = root.contents[x].contents[7].string
        NAPS = root.contents[x].contents[8].string
        ROE = root.contents[x].contents[9].string
        CFPS = root.contents[x].contents[10].string
        GPR = root.contents[x].contents[11].string
        conn.execute('''INSERT OR REPLACE INTO CO_QR(
                    stk_num, stk_name, publication_date, EPS, operation_revenue, year_on_year1, net_profit, year_on_year2, NAPS, ROE, CFPS, GPR) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (stk_num,stk_name,publication_date,EPS,operation_revenue,year_on_year1,net_profit,year_on_year2,NAPS,ROE,CFPS,GPR))
        conn.commit()
         
c.close()

print "QR"+year+quar
#print "Process Done."