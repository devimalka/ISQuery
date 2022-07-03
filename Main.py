import mysql.connector
from mysql.connector import errorcode
import xlwt
import pandas as pd

from threading import Thread

from MyLib import *
from env import *
from Queries import *
from locations import locations as loccopy



from dataFramesLib import ExcelSaver




       
class MyExcutor():
    def __init__(self)-> None:
         pass       

    def executor(self,QUERY,FOLDERNAME):
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
        
        IpList = AllLocsIPToList(loccopyf,['sc','ad'])
        
        while len(IpList )!= 0:
            for ip in reversed(IpList):
                print("IP list len " + str(len(IpList)))
                CenterAndLocName = ReturnCenter_Type_Name(ip,loccopy)
                locName = CenterAndLocName[1]
                CenterType = CenterAndLocName[0]
                CenterWiseFolderCreate(FOLDERNAME,CenterType)

                try:
                        cnx = mysql.connector.connect(user=usr, password=passwd,host=ip, database=db)

                        if cnx.is_connected():
                            if ip in failedlist:
                                failedlist.remove(ip)
                            print("Connection Succesfull to {}-{}".format(locName,CenterType))
                            connected +=1
                            print('conected ' +str(connected))
                            print('failed ' + str(failed))

                            location = cnx.cursor(buffered=True)
                            location.execute("SELECT loccod FROM docparameters d limit 1")

                            loc = location.fetchone()[0]

                            cursor = cnx.cursor()
                            cursor.execute(QUERY)
                            df = pd.DataFrame(cursor.fetchall())
                            df = df.reset_index(drop=True)

                            LocationExcel = FOLDERNAME+'/'+CenterType+'/'+loc+'.xls'
                            
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
                            
                                ExcelSaver(df,LocationExcel)
                        
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








def saveToExcel(query,filename):
    
    ExcutorObj = MyExcutor()
    queryDatas = ExcutorObj.executor(query,filename)
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
    ExcelSaver(Daily_Df,adfilename)
    ExcelSaver(Super_Df,scfilename)
    ExcelSaver(export,Fullfile)
    locdetailswrite(filename,queryDatas[1])
    print("******** SAVING SUCCESSFULL ********")
    QueryToFilesaver(Folder,query)
    loclistwrite(filename,queryDatas[3])
    




thread1 = Thread(target=saveToExcel,args=(dfcc15percent,"DFCC 15"))
thread2 = Thread(target=saveToExcel,args=(combank10,"Combank 10"))
thread3 = Thread(target=saveToExcel,args=(ndbbank,"NDB bank"))
thread4 = Thread(target=saveToExcel,args=(poeple10,"people 10"))
thread5 = Thread(target=saveToExcel,args=(seylan10billvalue,"seylan 10 bill value"))
thread6 = Thread(target=saveToExcel,args=(seylandebitcard,'seylan debit card'))

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()


