#Created on 2015/07/20
#By Eva Lam
#This script is to download the stock capital for each stock
#Sample: http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/000002.phtml

import urllib2
import sqlite3
import re

#i='000002'
#i = '166105'
#i = '000523'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	   
def stk_cpt_download(i):

    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/'
    url = url + str(i) + '.phtml'
    print 'Assecing url %s' %str(url)

    url=urllib2.Request(url,headers=hdr)
    html = urllib2.urlopen(url).read()
    file_stk = open('cpt_temp.txt','w')
    file_stk.write(html)
    file_stk.close()
#	print 'finished url reading'

    file_stk=open('cpt_temp.txt')
#	print 'checking file'
    for line in file_stk:
        cpt = 0
        cpt_temp = re.findall('TotalStock.*?<td>([0-9.]*)',line)
        if len(cpt_temp) >0:
            try:
				cpt = float(cpt_temp[0])
            except:
                print 'Error:cpt is not a number'
            break
    return cpt
	
#	print 'done cpt'

####
date = 'TBD'
conn = sqlite3.connect('stock.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stk_cpt(
                stk_num CHAR PRIMARY KEY,
                stk_cpt NUM,
                date TEXT
                )''')

# loop
for stk_num in c.execute("SELECT stk_num from stk_lst"):
	
#	c.execute("SELECT stk_name from stk_lst")
#	stk_name = c.fetchone
	stk_num = stk_num[0]
	#print stk_num
	if not (stk_num.startswith("6") or stk_num.startswith("0")): continue
    #Added by Tea
	try:
		stk_cpt = stk_cpt_download(stk_num)
	except:
		print 'missing %s' %stk_num
	conn.execute('''INSERT OR REPLACE INTO stk_cpt (
                    stk_num,  stk_cpt,date) 
                    VALUES (?,?,?)''',
                    (stk_num,stk_cpt,date))
	conn.commit()
    
c.close() 
		
print 'done'

