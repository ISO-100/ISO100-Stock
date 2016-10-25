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
    
    
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS rst_stk_info(
                stk_num CHAR(20) PRIMARY KEY,
                stk_name CHAR(20),
                open_prc float,
                close_prc float,
                current_prc float,
                highest_prc float,
                lowest_prc float,
                buy1 float,
                sell1 float,
                stock_dealed float,
                price_dealed float,
                date CHAR(20),
                time CHAR(20)
                )''')

c.execute("SELECT current_prc FROM stk_prc where stk_num = %s", (stk_num,))


if __name__ == "__main__":  
    start_time = time.time()
    main()
    print "\nCongrats! All done!"
    print("--- This program costs %0.2f seconds ---" % (time.time() - start_time))