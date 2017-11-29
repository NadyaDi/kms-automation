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

class stream:

    streamName         = ''
    streamURL          = ''
    streamUser         = ''
    streamPassword     = ''
    entry_id           = ''    
    streamStartUpTime  = 0
    streamUpTime       = 0
    plannedUpTime      = 0
    pID                = 0
    isUniversal        = False

    def timeToRestart(self):

        if ( (int(time.time()) - self.streamStartUpTime) >=  self.plannedUpTime):
            return True
        else:
            return False        
    
    def setStartUpTime(self):

        self.streamStartUpTime = int(time.time())

    def __init__(self, streamName, streamURL, streamUser, streamPassword, plannedUpTime, isUniversal, entry_id):

        self.streamName       = streamName
        self.streamURL        = streamURL
        self.streamUser       = streamUser
        self.streamPassword   = streamPassword
        self.isUniversal      = isUniversal
        self.plannedUpTime    = plannedUpTime
        self.entry_id         = entry_id

class streamsList:

    streamsList = []

    def getStreamByStreamName (self, streamName):

        for stream in self.streamsList:
            if (streamName == stream.streamName):
                return stream

        return None

    def getStreamByStreamURL (self,streamURL):
        
        for stream in self.streamsList:
            if (streamURL == stream.streamURL):
                return stream

        return None

    def __init__ (self):

        fmlestreams  = [
                        {
                            'streamName': "automation_universal_live_with_dvr_172678_6e63764b",
                            'streamURL': "rtmp://p.ep410462.i.akamaientrypoint.net/EntryPoint+0brtjn55t_1_1@410462",
                            'streamUser': "172678",
                            'streamPassword': "6e63764b",
                            'streamUpTime': 86400,
                            'isUniversal': True,
                            'entry_id': "0_evdutd28"
                        },
                         {
                            'streamName': "automation_universal_live_172678_6169ca85",
                            'streamURL': "rtmp://p.ep147138.i.akamaientrypoint.net/EntryPoint+0k7ahqm2b_1_1@147138",
                            'streamUser': "172678",
                            'streamPassword': "6169ca85",
                            'streamUpTime': 86400,
                            'isUniversal': True,
                            'entry_id': "0_k7ahqm2b"
                        }
        ]

        for fmlestream in fmlestreams:
            s = stream(fmlestream["streamName"], fmlestream["streamURL"], fmlestream["streamUser"], fmlestream["streamPassword"], fmlestream["streamUpTime"], fmlestream["isUniversal"],fmlestream["entry_id"])
            self.streamsList.append (s)

profileRestartTimout = 600

threads = []

#----------------------------------------------------------------

class fmle:

    live                = True;
    activeStreams       = []
    profilePIDmap       = {}
    restartStatus       = ""
    activeStreamsStatus = ""
    cpuUsage            = ""

    def getCPUUsage(self):

        #Get CPU usage by parsing WMIC output
        writeLog ("Thread: getCPUUsage()")
        
        command = "WMIC CPU GET LoadPercentage /value"
        
        while (self.live):
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
            output = process.communicate()
            temp = str (output[0])
            percentReg = re.compile('\d+')
            percentRegResults  = percentReg.findall(temp)
            self.cpuUsage =  percentRegResults[0]
            time.sleep(5)

        writeLog ("Thread: getCPUUsage() - exit")          

    def getFmlePIDs(self):

        #Get FMLE instances PID by parsing WMIC output
        
        profilePIDMap = {}
        command       = 'C:\Windows\\System32\\wbem\\WMIC PROCESS get Commandline,Processid /format:csv | find "fmlecmd"'
        process       = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        output        = process.communicate()
        poutput       = str(output)
        cleanOutput   = poutput.split("\\r\\n")

        for line in cleanOutput:
            if (line.find("/p")>0):
                profileReg = re.compile('/p.*xml')
                pidReg = re.compile(',\d+')
                profileRegResults  = profileReg.findall(line)
                pidRegResults =  pidReg.findall(line)
                if (len(profileRegResults)>0):
                    profilePIDMap[profileRegResults[0][3:len(profileRegResults[0])-4]]=pidRegResults[0][1:]

        return profilePIDMap

    def restartStreams(self):

        #Stop any stream after a period of time (set in profileUptime) for a period of time (set in profileRestartTimout)
        writeLog ("Thread: restartStreams()")

        while (self.live):
            self.restartStatus = "<b> Restart streams status </b><br>"
            if (len(self.activeStreams)>0):
                for activeStream in self.activeStreams:
                    qaStream = qaStreams.getStreamByStreamURL(activeStream)
                    if (qaStream.streamStartUpTime == 0):
                        qaStream.setStartUpTime()
                    elif ((int(time.time()) - qaStream.streamStartUpTime >=  qaStream.plannedUpTime)):
                        self.restartStatus = self.restartStatus + "stop: " + qaStream.streamName + "<br>"
                        writeLog ("Thread: restartStreams() stop:" + qaStream.streamName)
                        writeLog ("Thread: restartStreams() sleep:" + str (profileRestartTimout) + " minutes - " + qaStream.streamName)
                        self.fmleStop (qaStream.streamName)
                        self.restartStatus = self.restartStatus + "sleep: " + qaStream.streamName + "<br>"
                        time.sleep(profileRestartTimout)
                        self.restartStatus = self.restartStatus + "start: " + qaStream.streamName + "<br>"
                        writeLog ("Thread: restartStreams() start:" + qaStream.streamName)                         
                        request = 'http://' + SERVER_NAME + ':' + str(SERVER_PORT) + '/fmlestart?stream=' + qaStream.streamName + '&user=' +  qaStream.streamUser + '&password=' + qaStream.streamPassword
                        response = urllib.request.urlopen(request)
                        html = response.read()
                        response.close()
                        qaStream.setStartUpTime()
                    else:
                        writeLog ("Thread: restartStreams() restart in " +  str( qaStream.plannedUpTime + qaStream.streamStartUpTime - int(time.time())) + " seconds: " + qaStream.streamName)
                        self.restartStatus = self.restartStatus + "restart in " +  str( qaStream.plannedUpTime + qaStream.streamStartUpTime - int(time.time())) + " seconds: " + qaStream.streamName + "<br>"
                        
            time.sleep(5)

        writeLog ("Thread: restartStreams() - exit")
        
        return

    def monitorStreamsPageMainRequests(self):

            page = "<br><br><table border='1'>"
            page = page + "<tr><th colspan='2'>Stream</th><th colspan='2'>Available actions</th>"
            for stream in qaStreams.streamsList:
                page = page + "<tr>"
                page = page + '<td>' +  stream.streamName  + '</td>'
                page = page + '<td>' +  stream.entry_id  + '</td>'
                page = page + '<td><a href="http://' + SERVER_NAME + ':' + str(SERVER_PORT) + '/fmlestart?stream=' +  stream.streamName + '&user=' +  stream.streamUser +'&password=' + stream.streamPassword + '">Start</a></td>'
                page = page + '<td><a href="http://' + SERVER_NAME + ':' + str(SERVER_PORT) + '/fmlestop?stream=' + stream.streamName + '">Stop ' +  '</a></td>'
                page = page + "</tr>"
            page = page + "</table>"
            return page
      
    def monitorStreams(self):

        #Monitor and report which streams are active by crossing getFmlePIDs and getActiveStreams outputs
        writeLog ("Thread: monitorStreams()")

        response = ""
        while (self.live):
            self.activeStreamsStatus = "<b> Monitor streams status </b><br>"
            self.activeStreams = self.getActiveStreams()
            print (self.activeStreams)
            self.profilePIDmap = self.getFmlePIDs()
            print (self.profilePIDmap)
            if (len(self.activeStreams)>0):
                for activeStream in self.activeStreams:
                    qaStream = qaStreams.getStreamByStreamURL(activeStream)
                    if (qaStream.streamName in self.profilePIDmap.keys()):
                        writeLog ("Thread: monitorStreams() " + qaStream.streamName + " active")
                        self.activeStreamsStatus = self.activeStreamsStatus + qaStream.streamName + " active <br>" 
                    else:
                        self.activeStreamsStatus = self.activeStreamsStatus + qaStream.streamName + " not active, sending start request<br>" 
                        writeLog ("Thread: monitorStreams() " + qaStream.streamName + " not active, sending start request") 
                        request = 'http://' + SERVER_NAME + ':' + str(SERVER_PORT) + '/fmlestart?stream=' + qaStream.streamName + '&user=' +  qaStream.streamUser + '&password=' + qaStream.streamUser
                        writeLog ("Thread: monitorStreams() " +  request)
                        response = urllib.request.urlopen(request)
                        html = response.read()
                        response.close()
            time.sleep(5)

        writeLog ("Thread: monitorStreams() - exit")
        
        return

    def fmleStart(self,streamName):

        #Start FMLE instance by calling FMLECmd /p

        stream = qaStreams.getStreamByStreamName(streamName)
        executionPath = "C:\QASources\\fmlestart.bat " + stream.streamName + " " + stream.streamUser + " " + stream.streamPassword + " > logs/" + stream.streamName + ".log 2>&1"
        
        writeLog ("User request: fmleStart() , stream: " + stream.streamName + " user: " + stream.streamUser + " password: " + stream.streamPassword)

        os.system(executionPath)
        
        writeLog ("User request: fmleStart() stream: " + stream.streamName + " - exit")
        
        return

    def fmleStop(self,streamName):

        stream = qaStreams.getStreamByStreamName(streamName)

        #Stop FMLE instance by calling FMLECmd /s
        writeLog ("User request: fmleStop() " + stream.streamName)

        os.system('C:\QASources\\fmlestop.bat "' + stream.streamURL + '"')

        return

    #------------------------------------------------------
    def fmleClearSessions(self):
        
        # Clear FMLE session by deleting fmesessions.dat
        writeLog ("User request: fmleClearSessions()")

        os.system("C:\QASources\\fmleclearsessions.bat")

        return

    #------------------------------------------------------
    def getActiveStreams(self):

        # Get active streams by parsing "FMLECmd" /s output
        writeLog ("Auto request: getActiveStreams()")
        
        command = "C:\QASources\\fmlestatus.bat"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        output = process.communicate()
        temp = str (output[0])
        if (temp.find("FMLE sessions are")>=0):
            temp = temp [temp.find("FMLE sessions are:")+22:len(temp)-9]
            return temp.split("\\r\\n")
        else:
            return []

class myHandler(BaseHTTPRequestHandler):

        # HTTP server http handler for fmlestart,fmlestop,fmleclearsessions and fmlestatus requests
        response      = ""
        returnCode    = 200
        activeStreams = []
       
        def do_GET(self):

            redirectHeader   = '<html><head><META http-equiv="refresh" content="5;URL=http://' + SERVER_NAME + ':' + str(SERVER_PORT) + '/fmlestatus" </head> <body> Redirecting...'
            statusPageHeader = '<html><head> <meta http-equiv="refresh" content="5" > </head> <body><b>Server: ' + SERVER_NAME + ' <br> CPU usage: ' + fmlemanager.cpuUsage + '</b><br><br>'
            statusPageFooter = "</body></html>"

            if (self.path.find("fmlestart")>=0):
                qs = urllib.parse.parse_qs(self.path[self.path.find("?")+1:])
                t = threading.Thread(target=fmlemanager.fmleStart, args=(''.join (qs["stream"]),))
                t.start()
                threads.append(t)
                self.response = redirectHeader
            elif (self.path.find("fmlestop")>=0):
                qs = urllib.parse.parse_qs(self.path[self.path.find("?")+1:])
                t = threading.Thread(target=fmlemanager.fmleStop, args=(''.join (qs["stream"]),))
                t.start()
                threads.append(t)
                self.response = redirectHeader
            elif (self.path.find("fmleclearsessions")>=0):
                t = threading.Thread(target=fmlemanager.fmleClearSessions)
                t.start()
                threads.append(t)
                self.response = redirectHeader
            elif (self.path=="/fmlestatus"):
                writeLog ("User request: fmlestatus")
                self.activeStreams = fmlemanager.getActiveStreams ()
                if (len(self.activeStreams)>0):
                    self.response = statusPageHeader + fmlemanager.activeStreamsStatus + fmlemanager.restartStatus
                else:
                    self.response = statusPageHeader
                self.response = self.response + fmlemanager.monitorStreamsPageMainRequests()
            else:
                self.returnCode=500

            self.response = self.response  + statusPageFooter
            self.send_response(self.returnCode)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(str(self.response),'UTF-8'))

            return    

def writeLog (log):
    
        print (log)
        
        f = open("C:\QASources\main.log",'a')
        f.write(strftime("%Y-%m-%d %H:%M:%S") + " " + log)
        f.write('\n')
        f.close()

def print_usage():
    
        print ('the usage is : server.pys <server ip> <port numuber>')

def sizeOfArgsArrayargList(argList):
    
        sizeOfArgsList = len(argList)
        return sizeOfArgsList

#----------------------------------------------------------------

# Run server and launch monitorStreams annd restartStreams threads

qaStreams = streamsList()
fmlemanager = fmle()
if sizeOfArgsArrayargList(sys.argv) == 1 :
    print_usage()
else:
    SERVER_NAME = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
    try:
        server = HTTPServer(('', SERVER_PORT), myHandler)
        writeLog ('Started httpserver on port ' + str (SERVER_PORT))
        t = threading.Thread(target=fmlemanager.monitorStreams)
        t.start()
        threads.append(t)
        t = threading.Thread(target=fmlemanager.restartStreams)
        t.start()
        threads.append(t)
        t = threading.Thread(target=fmlemanager.getCPUUsage)
        t.start()
        threads.append(t)
        server.serve_forever()
    except KeyboardInterrupt:
        writeLog ('^C received, shutting down the web server')
        fmlemanager.live = False
        server.socket.close()
       
