import socket
import mysql.connector 
from locations import locs

from var import bcolors


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



def serverDownOrUp(iplist):

    while True:
        for tp,ip_info in iplist.items():

            for ip,name in ip_info.items():

                try:
                    connection = mysql.connector.connect(user='supun.c',password='spn.c',host=ip,database='marksys') 
                    if connection.is_connected():
                        print("Connection successfull to {} {}".format(name,tp))
                        connection.close()

                except:
                    print(f"{bcolors.FAIL}connection failed to %s %s{bcolors.ENDC}"%(name,tp))


serverDownOrUp(locs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          