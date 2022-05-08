import os
from datetime import datetime

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
