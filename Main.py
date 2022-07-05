from cProfile import run
import mysql.connector
from mysql.connector import errorcode
import xlwt
import pandas as pd
from mysql.connector.locales.eng import client_error
from threading import Thread

from MyLib import *
from env import *
from locations import LocationDictionary as LocationDict
from dataFramesLib import ExcelSaver


class MySQLImporter():
    def __init__(self,Query,Filename,choices,FileExtension,IterativeOrNot):
        self.DataFramesStack = []
        self.Filename = Filename
        self.choices = choices
        self.IterativeOrNot = IterativeOrNot
        self.LocationDictionary = LocationDict
        self.IPLists = AllLocsIPToList(self.LocationDictionary,self.choices)
        self.IPLists.reverse()
        self.Query = Query
        self.FileExtension = FileExtension
        self.FailedLocationList = []

        self.ADA_List = []
        self.SC_List  = []
        self.SR_List  = []
        self.FC_List  = []

    def CenterListDfAppend(self,df,CenterType):
        if CenterType == 'ad':
            self.ADA_List.append(df)
        elif CenterType == 'sc':
            self.SC_List.append(df)
        elif CenterType == 'sr':
            self.SR_List.append(df)
        elif CenterType == 'fc':
            self.FC_List.append(df)

    def AddFailedIp(self,ip):
        if ip not in self.FailedLocationList:
            self.FailedLocationList.append(ip)
    def RmFailedIp(self,ip):
        if ip in self.FailedLocationList:
            self.FailedLocationList.remove(ip)

    def SqlConnector(self):
       
        FolderCreate(self.Filename)
        for ip in reversed(self.IPLists):
            CenterAndLocationName = ReturnCenter_Type_Name(ip,self.LocationDictionary)
            Center_Type = CenterAndLocationName[0]
            Location_Name = CenterAndLocationName[1]
            CenterWiseFolderCreate(self.Filename,Center_Type)
            try:
                cnx = mysql.connector.connect(user=usr,password=passwd,host=ip,database=db,port=3306)


                if cnx.is_connected():
                    print("\nConnection Succesfull {} : {}".format(Location_Name,Center_Type))
                    print("Remaining Location Count {}".format(len(self.IPLists)-1))
                    print("Failed Location Count {}\n".format(len(self.FailedLocationList)))
                    self.RmFailedIp(ip)
                    LocationCode = cnx.cursor(buffered=True)
                    LocationCode.execute("select char_val from rms_sys_parameters where para_code='DEFLOC'")
                    LocationCode = LocationCode.fetchone()[0]
                   


                    QueryCursor = cnx.cursor()
                    QueryCursor.execute(self.Query)

                    df = pd.DataFrame(QueryCursor.fetchall())
                    df = df.reset_index(drop=True)

                    Location_Name_Excel = self.Filename + '/' + Center_Type + '/' + LocationCode + '.' + self.FileExtension

                    if not df.empty:
                        self.DataFramesStack.append(df)
                        self.CenterListDfAppend(df,Center_Type)
                        Field_Names =[ i[0] for i in  QueryCursor.description]
                        df.columns = Field_Names
                        ExcelSaver(df,Location_Name_Excel,self.FileExtension)
                    self.IPLists.remove(ip)
                    cnx.close()

            except mysql.connector.Error as err:
                self.AddFailedIp(ip)
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something Wrong With Your Username Or Password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("DATABASE Does Not Exist")
                else:
                    print(err)

        if len(self.FailedLocationList)!=0:
            self.WriteFailedLocations()
        return [self.DataFramesStack,[self.ADA_List,self.SC_List,self.SR_List,self.FC_List],self.FailedLocationList]
    
    def WriteFailedLocations(self):
        self.file = open(self.Filename+'/FailedLocations.txt','w')
        for ip in self.FailedLocationList:
            self.file.write('{}\n'.format(ip))
        self.file.close()
            

    def IterativeOrNotRun(self):
        if self.IterativeOrNot == True:
            while len(self.IPLists) != 0:
                return(self.SqlConnector())
        elif self.IterativeOrNot == False:
            return(self.SqlConnector())
            




def SaveToExcel(query,filename,choices,fileExtension,iterativeornot):

    testobj = MySQLImporter(query,filename,choices,fileExtension,iterativeornot)
    queryDatas = testobj.IterativeOrNotRun()
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
    print("******** SAVING SUCCESSFULL ********")
    QueryToFilesaver(Folder,query)
  


