import socket
import mysql.connector 
from locations import LocationDictionary

from var import bcolors
import time

import os

os.system('color')

# def serverDownOrUp(iplist):

#     while True:
#         for tp,ip_info in iplist.items():

#             for ip,name in ip_info.items():

#                 try:
                    

#                 except:
                    

# def ping_server(server:str,port:int,timeout=3):
#     try:
#         socket.setdefaulttimeout(timeout)
#         s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         s.connect((server,port))
#         print("successs")
#     except OSError as error:
#         return False
#     else:
#         s.close()
#         return True







# ping_server('192.9.236.1',3306)

class serverUPorDown():
    def __init__(self,iplist):
        self.iplist = iplist
        self.failedlist = []
        self.active = []

    def serverDownOrUp(self):

        while True:
            for tp,ip_info in self.iplist.items():

                for ip,name in ip_info.items():

                    try:
                        connection = mysql.connector.connect(user='supun.c',password='spn.c',host=ip,database='marksys') 
                        if connection.is_connected():
                            self.appendtolist(ip,'active')
                            self.removefromlist(ip,'failed')
                            print("Connection success to {:^15}{:<20} All Active count [{:<2}] Failed Count [{:>2}]".format(name,tp,len(self.active),len(self.failedlist)))
                            connection.close()
                            time.sleep(1)

                    except:
                        self.appendtolist(ip,'failed')
                        self.removefromlist(ip,'active')
                        # print("f{bcolors.FAIL}connection failed to %s %s{bcolors.ENDC}"%(name,tp))
                        print(bcolors.FAIL+"Connection Failed  to {:^15}{:<20} All Active count [{:<2}] Failed Count [{:>2}]".format(name,tp,len(self.active),len(self.failedlist))+bcolors.ENDC)


    def appendtolist(self,ip,listype):
        if listype == 'failed':
            if ip not in self.failedlist:
                self.failedlist.append(ip)
        else:
            if ip not in self.active:
                self.active.append(ip)
            
    def removefromlist(self,ip,listype):
        if listype == 'failed':
            if ip in self.failedlist:
                self.failedlist.remove(ip) 
        else:
            if ip in self.active:
                self.active.remove(ip)     
                
                
runipcheck = serverUPorDown(LocationDictionary)
runipcheck.serverDownOrUp()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           