import mysql.connector
from mysql.connector import errorcode
import xlwt
import pandas as pd

from MyLib import *
from env import *
from Queries import *
from locations import locs as loccopy

adlist =[]
sclist = []
srlist = []
fclist = []

def listClear():
    global adlist 
    adlist= []
    global sclist
    sclist= []
    global srlist 
    srlist= []
    global fclist 
    fclist= []


def storeViseappend(type,df):
    if type=='ad':
        adlist.append(df)
    elif type=='sc':
        sclist.append(df)
    elif type=='sr':
        srlist.append(df)
    elif type=='fc':
        fclist.append(df)



def ExcelSaver(df,filename):
    xlswriter = pd.ExcelWriter(filename,engine='xlsxwriter')
    df.to_excel(xlswriter,index=False)
    xlswriter.save()

def listappend(lists):
    mainlist = []
    for index in lists:
        for listitme in index:
            mainlist.append(listitme)
            
    return mainlist

def executor(QUERY,FOLDERNAME):

    dataFrameStack = []
    loccopyf = loccopy
    FailedLocs = {}
    AdList = []
    ScList = []
    FcList = []
    SrList = []

    FolderCreate(FOLDERNAME)
    IpList = AllLocsIPToList(loccopyf,['ad','sr'])
    #  for ip in IpList:
        
    #     CenterWiseFolderCreate(FOLDERNAME,type)
    for ip in IpList:
        CenterAndLocName = ReturnCenter_Type_Name(ip,loccopy)
        locName = CenterAndLocName[1]
        CenterType = CenterAndLocName[0]
        CenterWiseFolderCreate(FOLDERNAME,CenterType)

        try:
                cnx = mysql.connector.connect(user=usr, password=passwd,host=ip, database=db)

                if cnx.is_connected():
                    print("Connection Succesfull to {}-{}".format(locName,CenterType))


                    location = cnx.cursor(buffered=True)
                    location.execute("SELECT loccod FROM docparameters d limit 1")


                    loc = location.fetchone()[0]


                    cursor = cnx.cursor()
                    cursor.execute(QUERY)
                    df = pd.DataFrame(cursor.fetchall())
                    df = df.reset_index(drop=True)
                    # print(df)

                    LocationExcel = FOLDERNAME+'/'+CenterType+'/'+loc+'.xls'
                    
                    if not df.empty:
                       
                        storeViseappend(CenterType,df)



                    field_names = [ i[0] for i in  cursor.description]
                    # print(field_names)


                    if not df.empty:

                        df.columns = field_names
                       
                        ExcelSaver(df,LocationExcel)

                    else:
                        cnx.close()

        except mysql.connector.Error as err:

                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something wrong with your username or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("DATABASE does not exist")
                else:
                    
                    print(err)
                    print("Connection Failed to %s"%(locName))
                    if CenterType not in FailedLocs:
                       FailedLocs[CenterType] = {}
                       FailedLocs[CenterType][ip] = locName
                    else:
                     FailedLocs[CenterType][ip]= locName



         

    dataFrameStack.append(sclist)
    dataFrameStack.append(adlist)
    return [listappend(dataFrameStack),FailedLocs]








def saveToExcel(query,filename):

    queryDatas = executor(query,filename)

    export = dfConcat(queryDatas[0])
    ad =dfConcat(adlist)
    sc = dfConcat(sclist)

    Folder = filename+'/'+filename
    
    FolderCreate(Folder)
    
    adfilename = Folder+'/'+'ADA.xls'
    scfilename = Folder+'/'+'SC.xls'
    Fullfile = Folder+'/'+filename+'.xls'
    ExcelSaver(ad,adfilename)
    ExcelSaver(sc,scfilename)
    ExcelSaver(export,Fullfile)
    locdetailswrite(filename,queryDatas[1])




    
    locdetailswrite(filename,queryDatas[1])
    listClear()
    print("******** SAVING SUCCESSFULL ********")




saveToExcel('show tables','test two for ipit')