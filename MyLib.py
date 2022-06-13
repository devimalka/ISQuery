import os
from datetime import datetime
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


#create folder
def FileSaver(Filename):
    if Filename not in os.listdir():
        os.makedirs(Filename)
    elif Filename in os.listdir():
        os.remove(Filename)