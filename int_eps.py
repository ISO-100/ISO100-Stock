# -*- coding:utf-8 -*- 
#Created on 2015/07/14
#By Tea Shaw
#Last updated on 2016/05/14: Modify from using SQLite to Mysql - Teague Xiao
#This script is to download expected EPS for different organization
#Sample URL: http://vip.stock.finance.sina.com.cn/q/go.php/vPerformancePrediction/kind/eps/index.phtml?num=60&p=1

import urllib
#import sqlite3
import MySQLdb
import re
import time

import os
import ConfigParser
import sys

#For fixing 'ascii' codec can't encode characters in position 0-2: ordinal not in range(128) ERROR
reload(sys)
sys.setdefaultencoding('utf-8')

def int_eps_download(i,filename):
    url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vPerformancePrediction/kind/eps/index.phtml?num=60&p='
    url = url + str(i)
    print "Accessing %s" %url
    html = urllib.urlopen(url).read()
    fopen = open(filename,'w')
    fopen.write(html)
    fopen.close()
    
def int_eps_re(filename):
    fopen = open(filename)
    eps_data = []
    for line in fopen:
        stk_num = re.findall("\<td.*\>s[zh]([0-9]{6})",line)
        if len(stk_num) > 0:
            #print stk_num[0]
            eps_data.append(stk_num[0])
        stk_name = re.findall("<td.*><.*biz.finance.sina.com.cn.*>([^s].*)<\/a>",line)
        if len(stk_name) > 0:
            #print stk_name[0].decode('gb2312','ignore')
            eps_data.append(stk_name[0].decode('gb2312','ignore'))
        eps = re.findall("<td>([-]?[0-9]*\.[0-9][0-9])<\/td>|<td>(--)<\/td>",line)
        if len(eps) > 0:
            if eps[0][0] != '':
                #print eps[0][0]
                eps_data.append(eps[0][0])
            if eps[0][1] != '':
                #print eps[0][1]
                eps_data.append(eps[0][1])
        date = re.findall("<td.*>(\d{4}-\d{2}-\d{2})<\/td>",line)
        if len(date) >0:
            eps_data.append(date[0])
        
        org_name = re.findall("<td.*><.*orgname.*>(.*)<\/a>",line)
        if len(org_name) > 0:
            #print org_name[0].decode('gb2312','ignore')  
            eps_data.append(org_name[0].decode('gb2312','ignore'))
        author = re.findall("<td.*><.*author.*>(.*)<\/a>",line)
        if len(author) > 0:
            #print author[0].decode('gb2312','ignore')  
            eps_data.append(author[0].decode('gb2312','ignore'))
    return eps_data
    
def int_eps_store(eps_data):
    #con = sqlite3.connect('stock.sqlite')
    #con.execute("DROP TABLE IF EXISTS int_eps")
    Config = ConfigParser.ConfigParser()
    Config.read("settings.ini")
    con = MySQLdb.connect( Config.get('mysql', 'host'), Config.get('mysql', 'username'), Config.get('mysql', 'password'), Config.get('mysql', 'DB'), charset="utf8" )
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS int_eps(
            stk_num CHAR(20),
            stk_name CHAR(20),
            eps_y15 float,
            eps_y16 float,
            eps_y17 float,
            eps_y18 float,
            date CHAR(20),
            org_name CHAR(20),
            author CHAR(20),
            PRIMARY KEY (stk_num,date,org_name)
            )''')
    while len(eps_data) > 0:
        c.execute('''REPLACE INTO int_eps (stk_num,stk_name,eps_y15,eps_y16,eps_y17,eps_y18,date,org_name,author) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
        (eps_data[0],eps_data[1],eps_data[2],eps_data[3],eps_data[4],eps_data[5],eps_data[6],eps_data[7],eps_data[8]))
        con.commit()
        eps_data = eps_data[9:]
    c.close()
    
def main():
    page = 1
    filename = "int_eps_download.txt"
    while True:
        eps_data =[]
        int_eps_download(page,filename)
        eps_data = int_eps_re(filename)
        if len(eps_data) == 0:
            print "Reach the last page, quiting......"
            break
        int_eps_store(eps_data)
        page = page + 1
    print "Congratulation! All pages finished!"
    
if __name__ == "__main__":
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))