# -*- coding:utf-8 -*- 
#Created on 2015/07/30
#Version 1.0
#By Cong

import urllib
import sqlite3
import time 

ltime=time.time()-86400
tYear=time.strftime("%Y", time.localtime(ltime))
#print tYear
lYear="%i"%(int(tYear)-1)
#print lYear

conn = sqlite3.connect('stock.sqlite')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS cal_co_qr")

#字段说明示例：
#R_2014_1Q: 季报营收
#P_2014_1Q：季报利润
#P_rate_1Q：利润率
#FR_2015_4Q：预测营收
#FP_2015_3Q：预测利润
#forecast_EPS：预测EPS
#lastyear_yoy：季报利润增加同比
#forecast_PE：预测PE
#target_price：目标价位
str_sql = '''CREATE TABLE cal_co_qr(
               stk_num CHAR PRIMARY KEY,
               stk_name CHAR,
               %s NUM,
               %s NUM,
               P_rate_1Q NUM,
               %s NUM,
               %s NUM,
               P_rate_2Q NUM,
               %s NUM,
               %s NUM,
               P_rate_3Q NUM,
               %s NUM,
               %s NUM,
               P_rate_4Q NUM,
               %s NUM,
               %s NUM,
               P_rate_5Q NUM,
               %s NUM,
               %s NUM,
               P_rate_6Q NUM,
               %s NUM,
               %s NUM,
               P_rate_7Q NUM,
               %s NUM,
               %s NUM,
               %s NUM,
               %s NUM,
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

c.execute(str_sql)


#for stk_num in c.execute("SELECT stk_num from stk_lst"):
    #stk_num = stk_num[0]



c.close()
print "Process Done."