from fileinput import filename
from operator import index
import mysql.connector
from mysql.connector import errorcode
from numpy import save
import xlwt
import pandas as pd
import openpyxl


from MyLib import *
from env import *
from Queries import *
from locations import *


adlist =[]
sclist = []
srlist = []
fclist = []

def storeViseappend(type,df):
    if type=='ad':
        adlist.append(df)
    elif type=='sc':
        sclist.append(df)
    elif type=='sr':
        srlist.append(df)
    elif type=='fc':
        fclist.append(df)





def executor(QUERY):

    dataFrameStack = []
    loccopy = locs
    FailedLocs = {}


    for type,info in loccopy.items():
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
                    # print(df)

                    
                    
                    if not df.empty:
                        dataFrameStack.append(df)
                        storeViseappend(type,df)



                    field_names = [ i[0] for i in  cursor.description]
                    # print(field_names)

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
                    print("Connectin Failed to %s"%(locName))
                    logwriter(type,ip,locName,False)
                    if type not in FailedLocs:
                       FailedLocs[type] = {}
                       FailedLocs[type][ip] = locName
                    else:
                     FailedLocs[type][ip]= locName



            else:
                cnx.close()

    return [dataFrameStack,FailedLocs]





def ExcelSaver(df,filename,loctype):
    xlswriter = pd.ExcelWriter('{}/{}.xls'.format(filename,loctype),engine='openpyxl')
    df.to_excel(xlswriter,index=False)
    xlswriter.save()




def saveToExcel(query,filename):


    queryDatas = executor(query)

    export = dfConcat(queryDatas[0])
    ad =dfConcat(adlist)
    sc = dfConcat(sclist)


    FolderCreate(filename,query)

    ExcelSaver(ad,filename,'ADA')
    ExcelSaver(sc,filename,'SALE')
    ExcelSaver(export,filename,filename)
    
    locdetailswrite(filename,queryDatas[1])
    


  

    print("Succes savetoExcel")
    print(queryDatas)


saveToExcel(Seylan_10_Debit_CARD,'SEYLAN 10% Debit Card Promo 17-06-2022')

