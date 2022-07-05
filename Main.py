import mysql.connector
from mysql.connector import errorcode
import xlwt
import pandas as pd
from mysql.connector.locales.eng import client_error
from threading import Thread

from MyLib import *
from env import *
from Queries import *
from locations import locations as loccopy



from dataFramesLib import ExcelSaver




       
class MyExcutor():
    def __init__(self)-> None:
         pass       

    def executor(self,QUERY,FOLDERNAME,fileExtension,choicelist):
        failedlist = []
        dataFrameStack = []
        loccopyf = loccopy
        FailedLocs = {}
        
        #Inside List --When Function finised the Lists are Cleared--
        ADA_DATA = []
        SC_DATA = []
        SR_DATA = []
        FC_DATA = []
        
        connected = 0
        failed =0

        FolderCreate(FOLDERNAME)
        
        IpList = AllLocsIPToList(loccopyf,choicelist)
        IpList.reverse()
        
        while len(IpList )!= 0:
            for ip in reversed(IpList):
                print("IP list len " + str(len(IpList)))
                CenterAndLocName = ReturnCenter_Type_Name(ip,loccopy)
                locName = CenterAndLocName[1]
                CenterType = CenterAndLocName[0]
                CenterWiseFolderCreate(FOLDERNAME,CenterType)

                try:
                        cnx = mysql.connector.connect(user=usr, password=passwd,host=ip, database=db,port=3306)

                        if cnx.is_connected():
                            if ip in failedlist:
                                failedlist.remove(ip)
                            print("Connection Succesfull to {}-{}".format(locName,CenterType))
                            connected +=1
                            print('conected ' +str(connected))
                            print('failed ' + str(failed))

                            location = cnx.cursor(buffered=True)
                            # location.execute("SELECT loccod FROM docparameters d limit 1")
                            location.execute("select char_val from rms_sys_parameters where para_code='DEFLOC'")

                            loc = location.fetchone()[0]

                            cursor = cnx.cursor()
                            cursor.execute(QUERY)
                            df = pd.DataFrame(cursor.fetchall())
                            df = df.reset_index(drop=True)

                            LocationExcel = FOLDERNAME+'/'+CenterType+'/'+loc+'.'+fileExtension
                            
                            if not df.empty:
                            
                                if CenterType == 'ad':
                                    ADA_DATA.append(df)
                                if CenterType == 'sc':
                                    SC_DATA.append(df)
                                if CenterType == 'sr':
                                    SR_DATA.append(df)
                                if CenterType == 'fc':
                                    FC_DATA.append(df)



                            field_names = [ i[0] for i in  cursor.description]

                            if not df.empty:

                                df.columns = field_names
                            
                                ExcelSaver(df,LocationExcel,fileExtension)
                        
                            else:
                                cnx.close()
                            IpList.remove(ip)

                except mysql.connector.Error as err:
                        failed +=1
                        print("failed " + str(failed))

                        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                            print("Something wrong with your username or password")
                        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                            print("DATABASE does not exist")
                        else:
                            
                            print(err)
                            print("Connection Failed to %s"%(locName))
                            if ip not in failedlist:
                                failedlist.append(ip)
                            if CenterType not in FailedLocs:
                                FailedLocs[CenterType] = {}
                                FailedLocs[CenterType][ip] = locName
                            else:
                                FailedLocs[CenterType][ip]= locName

                        

        print("last len of list " + str(len(IpList)))
        dataFrameStack.append(ADA_DATA)
        dataFrameStack.append(SC_DATA)
        return [listappend(dataFrameStack),FailedLocs,[ADA_DATA,SC_DATA,SR_DATA,FC_DATA],failedlist]








def saveToExcel(query,filename,fileExtension,choicelist):
    
    ExcutorObj = MyExcutor()
    queryDatas = ExcutorObj.executor(query,filename,fileExtension,choicelist)
    export = dfConcat(queryDatas[0])
    Daily_Df =dfConcat(queryDatas[2][0])
    Super_Df = dfConcat(queryDatas[2][1])
    Showroom_Df = dfConcat(queryDatas[2][2])
    Furniture_Df = dfConcat(queryDatas[2][3])
    Folder = filename+'/'+filename
    FolderCreate(Folder)
    adfilename = Folder+'/'+'ADA.xls'
    scfilename = Folder+'/'+'SC.xls'
    Fullfile = Folder+'/'+filename+'.xls'
    ExcelSaver(Daily_Df,adfilename,fileExtension)
    ExcelSaver(Super_Df,scfilename,fileExtension)
    ExcelSaver(export,Fullfile,fileExtension)
    locdetailswrite(filename,queryDatas[1])
    print("******** SAVING SUCCESSFULL ********")
    QueryToFilesaver(Folder,query)
    loclistwrite(filename,queryDatas[3])
    



