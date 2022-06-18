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

FailedLocs = {}

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

    return dataFrameStack





def ExcelSaver(df,filename):
    xlswriter = pd.ExcelWriter('{}/{}excels55hhhjaver.xls'.format(filename,filename),engine='openpyxl')
    df.to_excel(xlswriter,index=False)
    xlswriter.save()




def saveToExcel(query,filename):


    queryDatas = executor(query)

    export = dfConcat(queryDatas)
    ad =dfConcat(adlist)
    sc = dfConcat(sclist)


    FolderCreate(filename,query)


    xlswriter = pd.ExcelWriter("%s/%s.xls"%(filename,filename),engine='openpyxl')
    export.to_excel(xlswriter,index=False)
    xlswriter.save()

    xlswritersc = pd.ExcelWriter("%s/%ssc.xls"%(filename,filename),engine='openpyxl')
    sc.to_excel(xlswritersc,index=False)
    xlswritersc.save()
    xlswriterad = pd.ExcelWriter("%s/%sad.xls"%(filename,filename),engine='openpyxl')
    ad.to_excel(xlswriterad,index=False)
    xlswriterad.save()

    ExcelSaver(ad,filename)


    print("Succes savetoExcel")


saveToExcel(ntb25,'NTB')



