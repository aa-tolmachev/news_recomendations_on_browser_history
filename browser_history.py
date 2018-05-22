# file:///C:/Users/Admin/AppData/Local/Google/Chrome/User%20Data/Default/
# go to this link in browser if want to check internal info of google browser

#http://bar-navig.yandex.ru/u?show=31&url=https://www.coursera.org
#on this lick we get xml response about web_site

#https://www.kakprosto.ru/kak-109671-kak-uznat-tematiku-sayta
#on this lick we can get insructions to parse site data

import os
import shutil
import sqlite3
import pandas as pd
from datetime import datetime


data_path = os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default"

srcfile = data_path+'\\History'

try:
    dstroot = 'chrome_history'
    dstdir =  os.path.join(dstroot)
    os.makedirs(dstdir)
except:
    print ('dir already here ')


shutil.copy(srcfile, dstdir)

data_path = dstdir+'\\History'

select_statement = "SELECT * FROM urls, visits WHERE urls.id = visits.url;"
select_statement = "select datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime') as dt_last_visit, * FROM urls ORDER BY last_visit_time DESC"

select_statement = ''.join([
    'SELECT ', 'v.id , v.url as url_id , v.visit_time , v.visit_duration', ' \n'
    , " , datetime(v.visit_time/1000000-11644473600,'unixepoch','localtime') as dt_visit_time", ' \n'
    , ' , u.url , u.title , u.visit_count , u.typed_count , ', ' \n'
    , "datetime(u.last_visit_time/1000000-11644473600,'unixepoch','localtime') as dt_last_visit", ' \n'
    , 'from ', 'visits v', ' \n'
    , 'left join ', 'urls u on v.url = u.id  ', ' \n'
    , 'order by ', ' 2 desc'

])

print(select_statement)


c = sqlite3.connect(data_path)
cursor = c.cursor()



cursor.execute(select_statement)


df_chrome_history = pd.read_sql_query(select_statement, c)

df_chrome_history['dt_last_visit'] =  [ datetime.strptime( x , '%Y-%m-%d %H:%M:%S') for x in df_chrome_history['dt_last_visit'] ]
df_chrome_history['dt_visit_time'] =  [ datetime.strptime( x , '%Y-%m-%d %H:%M:%S') for x in df_chrome_history['dt_visit_time'] ]
df_chrome_history.drop(['visit_time'], axis=1 , inplace = True)

c.close()


print (df_chrome_history.head())