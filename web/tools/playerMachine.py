import winreg
import re
import csv
import sys
import time
import os
import cgi
import urllib.parse
import subprocess
import time
import threading
import http.client, urllib.parse,urllib.request
from time import gmtime, strftime
from collections import defaultdict
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from base64 import decodestring
from subprocess import check_output

#----------------------------------------------------------------

SERVER_NAME    = ""
SERVER_PORT    = 0

class myHandler(BaseHTTPRequestHandler):
    
        cpuUsage      = ""
        response      = ""
        returnCode    = 200
    
        def do_GET(self):

            if (self.path.find("resetMachineProxy")>=0):
                
                keyVal = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
                
                try:
                    print ("Open Reg key for editing")
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "ProxyHttp1.1", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                    print ("Open Reg key for reading and verifying changed value")
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyVal, 0, winreg.KEY_READ)
                    value, regtype = winreg.QueryValueEx(key, "ProxyEnable")
                    if (value != 0):
                        print ("Failed setting ProxyEnable to 0")
                        self.returnCode = 500
                    value, regtype = winreg.QueryValueEx(key, "ProxyHttp1.1")
                    if (value != 0):
                        print ("Failed setting ProxyHttp1.1 to 0")
                        self.returnCode = 500
                    winreg.CloseKey(key)
                except Exception as inst:
                    print (str(type(inst)))
                    print (str(inst))
                    self.returnCode = 500
                
                self.send_response(self.returnCode)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(bytes(str(self.response),'UTF-8'))

            return    

def print_usage():
    
        print ('the usage is : server.pys <server ip> <port numuber>')

def sizeOfArgsArrayargList(argList):
    
        sizeOfArgsList = len(argList)
        return sizeOfArgsList

#----------------------------------------------------------------

if sizeOfArgsArrayargList(sys.argv) == 1 :
    print_usage()
else:
    SERVER_NAME = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    try:
        print ("Starting server")
        server = HTTPServer(('', SERVER_PORT), myHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()
       
