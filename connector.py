import mysql.connector
from mysql.connector import errorcode 
import xlwt
import pandas as pd
import openpyxl


from MyLib import *
from env import *
from Queries import *
from locations import *


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
                    df = pd.DataFrame(cursor.fetchall())
                    df = df.reset_index(drop=True)              
                    print(df)


                    if not df.empty:
                        dataFrameStack.append(df)
             
                 
                                    
                    field_names = [ i[0] for i in  cursor.description]
                    print(field_names)
                        
                    xlswriter = pd.ExcelWriter('{}/{}.xls'.format(type,loc),engine='openpyxl')

                    if not df.empty:
                       
                        df.columns = field_names
                        df = df.reset_index(drop=True)
                        df.to_excel(xlswriter,index=False)

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


    queryDatas = executor(query)
    
    export = dfConcat(queryDatas)
    FileSaver(filename)
    xlswriter = pd.ExcelWriter("%s/%s.xls"%(filename,filename),engine='openpyxl')

    export.to_excel(xlswriter,index=False)
    xlswriter.save()


    print("succes savetoExcel")


saveToExcel(dfcc10,"dffcc10 test2")






