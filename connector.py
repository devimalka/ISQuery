from ast import Not
from calendar import day_abbr
from cmath import inf
from multiprocessing import connection
from operator import index
from sqlite3 import Cursor
from unittest.result import failfast
import mysql.connector
from mysql.connector import errorcode
from numpy import save

import pandas as pd
from requests import NullHandler
from sqlalchemy import false
#importing Queries
from Queries import *

#Location Ip's
from locations import locs

from env import *

startDate='2022-05-01'
endDate='2022-05-15'

from lib import fileChecker,logwriter

    

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


from Test_Variables import location_test as loctest

from lib import fileChecker,logwriter

    

def executor(QUERY):
    dataFrameStack = []

  
    
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
                    cursor.execute(QUERY)
                    df = pd.DataFrame(cursor)
                   
                    print(df)


                    # if not df.empty:
                    #     if dataFrameStack is not None:
                    #         dataFrameStack = dataFrameStack.append(df)

                        
                    # else:
                    #     dataFrameStack = df

                    dataFrameStack.append(df)
                    print("len of dataframestack is {}".format(len(dataFrameStack)))
                      
                 
                    print('\n\n\n\n\n***********************')
                    print(dataFrameStack)
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

    return dataFrameStack
   









def saveToExcel(query,filename):

    fulstack = None

    xlswriter = pd.ExcelWriter("%s.xls"%(filename),engine='openpyxl')
    queryDatas = executor(query)
    for i in queryDatas:
        fulstack = pd.concat([fulstack,i],axis=0,ignore_index=True)

    export = fulstack
    export.to_excel(xlswriter,index=False)
    xlswriter.save()


    print("succes savetoExcel")


saveToExcel(dfcc10,"dffcc10restindex")






