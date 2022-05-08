from cmath import inf
from multiprocessing import connection
from operator import index
from sqlite3 import Cursor
from unittest.result import failfast
import mysql.connector
from mysql.connector import errorcode

import pandas as pd
from sqlalchemy import false
#importing Queries
from Queries import *

#Location Ip's
from locations import locs

from env import *

startDate='2022-04-01'
endDate='2022-04-30'

from lib import fileChecker,logwriter

    

def executor(QUERY):
    alldf = None
    
    for type,info in locs.items():
        fileChecker(type)

        for ip,locName in info.items():

            try:
                cnx = mysql.connector.connect(user=usr, password=passwd,host=ip, database=db)

                if cnx.is_connected():
                    print("Connection Succesfull to {}".format(locName))
                    logwriter(type,ip,locName,True)


                    location = cnx.cursor(buffered=True)
                    location.execute("SELECT loccod FROM docparameters d limit 1")

        
                    loc = location.fetchone()[0]
        
                    
                    cursor = cnx.cursor()
                    cursor.execute("SELECT * FROM rms_pospromohead r where promid='3101';")
                    df = pd.DataFrame(cursor.fetchall())
                    
                    if alldf is not None:
                        alldf = alldf.append(df)
                    else:
                        alldf = df
                
                    print(df)
                    field_names = [ i[0] for i in  cursor.description]
                    print(field_names)
                        
                    xlswriter = pd.ExcelWriter('{}/{}.xls'.format(type,loc),engine='openpyxl')

                    if not df.empty:
                        df.columns = field_names  
                      
                        df.to_excel(xlswriter,index=false)

                        xlswriter.save()
                    else:
                        cnx.close()
   
            except mysql.connector.Error as err:

                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something wrong with your username or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("DATABASE does not exist")
                else:
                    print(err)
                    print("Connectin Failed to %s"%(loc))
                    logwriter(type,ip,locName,False)

                   
            else:
                cnx.close()

   









def saveToExcel(query,filename):

    xlswriter = pd.ExcelWriter("%s.xls"%(filename),engine='openpyxl')
    queryDatas = executor(query)
    export = queryDatas[0]
    export.columns = queryDatas[1]
    export.to_excel(xlswriter,index=False)
    xlswriter.save()



executor(doctally)


