# -*- coding:utf-8 -*- 
#Created on 2015/07/20
#By Eva Lam
#This script is to download the stock capital for each stock
#Sample: http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/000002.phtml
#Last modified at 2016/10/27 by Teague Xiao

import urllib2
import re
import MySQLdb
import os
import ConfigParser
import time

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	   
def stk_cpt_download(i):
    result = dict()
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/'
    url = url + str(i) + '.phtml'
    print 'Assecing url %s' %str(url)

    url=urllib2.Request(url,headers=hdr)
    html = urllib2.urlopen(url).read()
    file_stk = open('cpt_temp.txt','w')
    file_stk.write(html)
    file_stk.close()
    file_stk=open('cpt_temp.txt')

    for line in file_stk:
        cpt = 0
        cpt_temp = re.findall('TotalStock.*?<td>([0-9.]*)',line)
        if len(cpt_temp) >0:
            try:
				cpt = float(cpt_temp[0])
				result[0] = cpt
				print cpt
            except:
                print 'Error:cpt is not a number'
            break
        result[0] = cpt
        
    for line in file_stk:
        date = "N/A"
        date_tmp = re.findall('<td width.*?>.*?</td><td>(.{10})',line)
        if len(date_tmp) > 0:
            date = date_tmp[0]
            result[1] = date
            print date
            break
        result[1] = date
        
    return result

Config = ConfigParser.ConfigParser()
Config.read("settings.ini")
con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
c = con.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stk_cpt(
                stk_num CHAR(20) PRIMARY KEY,
                stk_name CHAR(20),
                stk_cpt float(20,3),
                date TEXT
                )''')
c.execute("SELECT stk_num,stk_name from stk_lst")

for stk_num ,stk_name in c.fetchall():
    print stk_num, stk_name
    if not (stk_num.startswith("6") or stk_num.startswith("0")): continue

    result = stk_cpt_download(stk_num)
    stk_cpt = result[0]
    date = result[1]
    c.execute('''REPLACE INTO stk_cpt (
                stk_num,stk_name,stk_cpt,date) 
                VALUES (%s,%s,%s,%s)''',
                (stk_num,stk_name,stk_cpt,date))
    con.commit()
    
        
   
c.close() 
		
print 'done'