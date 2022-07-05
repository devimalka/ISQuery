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

       
class MySQLImporter():
    def __init__(self,Query,Filename,choices,IterativeOrNot,LocationDictionary,FileExtension):
        self.DataFramesStack = []
        self.Filename = Filename
        self.choices = choices
        self.IterativeOrNot = IterativeOrNot
        self.LocationDictionary = LocationDictionary
        self.IPLists = AllLocsIPToList(self.LocationDictionary,self.choices)
        self.IPLists.reverse()
        self.Query = Query
        self.FileExtension = FileExtension
        
        self.ADA_List = []
        self.SC_List = []
        self.SR_List = []
        self.FC_List = []
        
    def CenterListDfAppend(self,df,CenterType):
        if CenterType == 'ad':
            self.ADA_List.append(df)
        elif CenterType == 'sc':
            self.SC_List.append(df)
        elif CenterType == 'sr':
            self.SR_List.append(df)
        elif CenterType == 'fc':
            self.FC_List.append(df)

    def SqlConnector(self):
        FolderCreate(self.Filename)
        for ip in reversed(self.IPLists):
            CenterAndLocationName = ReturnCenter_Type_Name(ip,self.LocationDictionary)
            Center_Type = CenterAndLocationName[0]
            Location_Name = CenterAndLocationName[1]
            CenterWiseFolderCreate(self.Filename,Center_Type)
            print(len(self.IPLists))
            try:
                cnx = mysql.connector.connect(user=usr,password=passwd,host=ip,database=db,port=3306)
               
                
                if cnx.is_connected():
                    print("Connection Succesfull {} : {}".format(Location_Name,Center_Type))
                    
                    LocationCode = cnx.cursor(buffered=True)
                    LocationCode.execute("select char_val from rms_sys_parameters where para_code='DEFLOC'")
                    LocationCode = LocationCode.fetchone()[0]
                    print(LocationCode)
                    print(len(self.IPLists))                  
                    
                    
                    QueryCursor = cnx.cursor()
                    QueryCursor.execute(self.Query)
                    
                    df = pd.DataFrame(QueryCursor.fetchall())
                    df = df.reset_index(drop=True)
                    
                    Location_Name_Excel = self.Filename + '/' + Center_Type + LocationCode + '.' + self.FileExtension
                    
                    if not df.empty:
                        self.DataFramesStack.append(df)
                        self.CenterListDfAppend(df,Center_Type)
                        Field_Names =[ i[0] for i in  QueryCursor.description]
                        df.columns = Field_Names
                        ExcelSaver(df,Location_Name_Excel,self.FileExtension)
                    self.IPLists.remove(ip)
                    cnx.close()
                    
            except mysql.connector.Error as err:
                 if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                            print("Something Wrong With Your Username Or Password")
                 elif err.errno == errorcode.ER_BAD_DB_ERROR:
                            print("DATABASE Does Not Exist")
                 else:
                            print(err)
                            
        return [self.DataFramesStack,[self.ADA_List,self.SC_List,self.SR_List,self.FC_List]]  
                          
    def IterativeOrNotRun(self):
        if self.IterativeOrNot == True:
            while len(self.IPLists) != 0:
                data=self.SqlConnector()
        elif self.IterativeOrNot == False:
            data=self.SqlConnector()
        return data
            
                
               
            
           
        
        
    
    # def executor(self,QUERY,FOLDERNAME,fileExtension,choicelist):
    #     failedlist = []
    #     dataFrameStack = []
    #     loccopyf = loccopy
    #     FailedLocs = {}
        
    #     #Inside List --When Function finised the Lists are Cleared--
    #     ADA_DATA = []
    #     SC_DATA = []
    #     SR_DATA = []
    #     FC_DATA = []
        
    #     connected = 0
    #     failed =0

    #     FolderCreate(FOLDERNAME)
        
    #     self.IpList = AllLocsIPToList(loccopyf,choicelist)
    #     self.IpList.reverse()
        
    #     while len(self.IpList )!= 0:
    #         for ip in reversed(self.IpList):
    #             print("IP list len " + str(len(self.IpList)))
    #             CenterAndLocName = ReturnCenter_Type_Name(ip,loccopy)
    #             locName = CenterAndLocName[1]
    #             CenterType = CenterAndLocName[0]
    #             CenterWiseFolderCreate(FOLDERNAME,CenterType)

    #             try:
    #                     cnx = mysql.connector.connect(user=usr, password=passwd,host=ip, database=db,port=3306)

    #                     if cnx.is_connected():
    #                         if ip in failedlist:
    #                             failedlist.remove(ip)
    #                         print("Connection Succesfull to {}-{}".format(locName,CenterType))
    #                         connected +=1
    #                         print('conected ' +str(connected))
    #                         print('failed ' + str(failed))

    #                         location = cnx.cursor(buffered=True)
    #                         # location.execute("SELECT loccod FROM docparameters d limit 1")
    #                         location.execute("select char_val from rms_sys_parameters where para_code='DEFLOC'")

    #                         loc = location.fetchone()[0]

    #                         cursor = cnx.cursor()
    #                         cursor.execute(QUERY)
    #                         df = pd.DataFrame(cursor.fetchall())
    #                         df = df.reset_index(drop=True)

    #                         LocationExcel = FOLDERNAME+'/'+CenterType+'/'+loc+'.'+fileExtension
                            
    #                         if not df.empty:
    #                             dataFrameStack.append(df)
                            
    #                             if CenterType == 'ad':
    #                                 ADA_DATA.append(df)
    #                             if CenterType == 'sc':
    #                                 SC_DATA.append(df)
    #                             if CenterType == 'sr':
    #                                 SR_DATA.append(df)
    #                             if CenterType == 'fc':
    #                                 FC_DATA.append(df)



    #                         field_names = [ i[0] for i in  cursor.description]

    #                         if not df.empty:

    #                             df.columns = field_names
                            
    #                             ExcelSaver(df,LocationExcel,fileExtension)
                        
    #                         else:
    #                             cnx.close()
    #                         self.IpList.remove(ip)

    #             except mysql.connector.Error as err:
    #                     failed +=1
    #                     print("failed " + str(failed))

    #                     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #                         print("Something wrong with your username or password")
    #                     elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #                         print("DATABASE does not exist")
    #                     else:
                            
    #                         print(err)
    #                         print("Connection Failed to %s"%(locName))
    #                         if ip not in failedlist:
    #                             failedlist.append(ip)
    #                         if CenterType not in FailedLocs:
    #                             FailedLocs[CenterType] = {}
    #                             FailedLocs[CenterType][ip] = locName
    #                         else:
    #                             FailedLocs[CenterType][ip]= locName

                        

    #     print("last len of list " + str(len(self.IpList)))
    #     return [dataFrameStack,FailedLocs,[ADA_DATA,SC_DATA,SR_DATA,FC_DATA],failedlist]








def saveToExcel(query,filename,fileExtension,choicelist):
    
    ExcutorObj = MySQLImporter(query,filename,choicelist,False,loccopy,fileExtension)
    queryDatas = ExcutorObj.IterativeOrNotRun()
    export = dfConcat(queryDatas[0])
    Daily_Df =dfConcat(queryDatas[1][0])
    Super_Df = dfConcat(queryDatas[1][1])
    Showroom_Df = dfConcat(queryDatas[1][2])
    Furniture_Df = dfConcat(queryDatas[1][3])
    Folder = filename+'/'+filename
    FolderCreate(Folder)
    adfilename = Folder+'/'+'ADA.xls'
    scfilename = Folder+'/'+'SC.xls'
    Fullfile = Folder+'/'+filename+'.xls'
    ExcelSaver(Daily_Df,adfilename,fileExtension)
    ExcelSaver(Super_Df,scfilename,fileExtension)
    ExcelSaver(export,Fullfile,fileExtension)
    # locdetailswrite(filename,queryDatas[1])
    print("******** SAVING SUCCESSFULL ********")
    QueryToFilesaver(Folder,query)
    # loclistwrite(filename,queryDatas[3])
    



saveToExcel('show tables;','testimfdportermysql','csv',['sc'])