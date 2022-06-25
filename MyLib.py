import os
from datetime import datetime
import shutil
import pandas as pd

logfailedls = 'logfailed.txt'
logsuccessls = 'logsuccess.txt'


def fileChecker(ctype):
    if not os.path.isdir("{}/".format(ctype)):
        os.makedirs("{}/".format(ctype))

    lsdir = os.listdir('{}/'.format(ctype))

    if logfailedls in lsdir:
        os.remove("%s/%s"%(ctype,logfailedls))
    
    if logsuccessls in lsdir:
        os.remove("%s/%s"%(ctype,logsuccessls))
        


def logwriter(ctype,ip,locName,status):
       if status == True:
        logsuccess = open('{}/{}'.format(ctype,logsuccessls),'a')
        logsuccess.write('{}  : {}-{}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),ip,locName))
        logsuccess.close()
       elif status == False:
        logfailed = open("{}/{}".format(ctype,logfailedls),'a')
        logfailed.write('{}  : {}-{}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),ip,locName))
        logfailed.close()




#conatanating dataframe list and stacking verticaly
def dfConcat(dflist):
    concatedDf = pd.DataFrame()
    for i in dflist:
        concatedDf = pd.concat([concatedDf,i],axis=0,ignore_index=True)
    return concatedDf



#save the current query to text file
def QueryToFilesaver(Filename,query):
    queryFile = open('{}/query.txt'.format(Filename),'a')
    queryFile.write(query)
    queryFile.close()

    

#create folder
def FolderCreate(Filename,query):
    if os.path.exists(Filename):
        shutil.rmtree(Filename)
    os.makedirs(Filename)

    QueryToFilesaver(Filename,query)



def locdetailswrite(Filename,loclist):
    if (len(loclist) != 0):
        locationsfile = open('{}/failed.txt'.format(Filename),'w')
        for key,info in loclist.items():
            for key,value in info.items():
                locationsfile.write('{}-{}'.format(key,value))
        locationsfile.close()
        