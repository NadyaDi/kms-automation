from datetime import datetime 
from collections import OrderedDict
# from clsAnalytics import clsAnalytics
from localSettings import *
import browsermobproxy
import re
import json
import os
import requests
from logger import *


class clsBrowserMobCapture:
    
    #===========================================================================
    # the class allows us to capture the HTTP traffic from the remote machine that we are running the tests on.
    # we create a browser mob proxy for the remote selenium webdriver, the server is the hub and the client is the computer with the tests. 
    # need to activate the server using "./browsermob-proxy -port 9090" in the server computer.
    # we save a HAR file in specific directory for debug, and compare the expected results with the actual results we captured     
    #===========================================================================
    
    def __init__(self,testNum,testBrowser):
        
            runningTestNum    = os.getenv('RUNNING_TEST_ID',"")
            LOG_FOLDER_PREFIX = ""
            if (os.getenv('BUILD_ID',"") != ""):
                LOG_FOLDER_PREFIX = '/' + os.getenv('BUILD_ID',"") + '/'
        
            self.testNum = testNum
            self.testBrowser = testBrowser
            self.harPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','logs' + LOG_FOLDER_PREFIX + "/" + runningTestNum + "/","test_" + runningTestNum + "_" + self.testBrowser + '.har'))
   
    #the function creates a new client to the proxy 'browser proxy'
    def createProxyClient(self,proxyUrl):
        
        client = browsermobproxy.Client(proxyUrl)
        
        return client
    
    #the function sends delete request to a specific proxy server to shut it down 
    def shutDownProxy(self,proxyURL,proxyPort):
    
        url = "http://" + proxyURL + "/proxy/" + str(proxyPort)
        try:
            response = requests.delete(url)
        except Exception as inst:
            writeToLog("INFO","Unable to shutdown mobile web proxy")
            
    #the function creates new HAR file (erase the previous if exist)
    def createNewCapture(self):
        if os.path.exists(self.harPath):
            os.remove(self.harPath)
    
    #the function saves the HAR results in file (json format)
    def saveHar(self,harFile):
        self.createNewCapture()
        har_data = json.dumps(harFile, indent=4)
        save_har = open(self.harPath, 'w')
        save_har.write(har_data)
        save_har.close()

#     #the function run over the HAR file, add the relevant google analytics events to a dictionary and return it.
#     def createHttpGoogleAnalyticsDict(self,harFile):
#         analytics   = clsAnalytics()
#         actualHttpEvents = [] # will contain all the events parsed
#         for ent in harFile['log']['entries']:
#             currEvent = ent['request']['url']
#             if('utm.gif' in currEvent): #we ensure this is a google analytics event 
#                 currEventDic = analytics.gaParseHTTPLine(currEvent)
#                 if(currEventDic != -1): # we don't add the packet to the dictionary if one of the values ['utme','utmhn','utmt','utmsr','utmvp','utmdt','utmac','optval'] is missing
#                     currEventDic['Time'] = ent['startedDateTime']
#                     actualHttpEvents.append(currEventDic)
#         return actualHttpEvents
    
    #The function run over the HAR file, filters the request URL, add to dictionary and return it.
    def createFilteredRequestUrlDict(self, harFile, filterString):
        actualHttpEvents = [] # will contain all the events parsed
        for ent in harFile['log']['entries']:
            currEvent = ent['request']['url']
            if(filterString in currEvent): #Filter
                    actualHttpEvents.append(currEvent)
        return actualHttpEvents
    
    #the function run over the HAR file, add the relevant plugin events to a dictionary and return it.
    def createHttpAnalyticsDict(self,harFile,requiredParams,filterURLList,analyticsPluginName = None):
            
            urlFound = False
            actualHttpEventsRequests  = [] # will contain all the events requests parsed
            actualHttpEventsResponses = [] # will contain all events responses parsed
            try:
                for ent in harFile['log']['entries']:
                    queryStringParameters  = {}
                    reposnseParameters     = {}
                    for url in filterURLList:
                        if (url in ent['request']['url']):
                            urlFound = True
                    if(urlFound == True):
                        if (ent['response']['status'] == 200): #we ensure this is event and that the request got http success
                            currEvent = ent['request']['queryString']
                            for param in currEvent:
                                if (param["name"] not in requiredParams):
                                    queryStringParameters[param["name"]] = param["value"]
                            if (analyticsPluginName == "youbora"):
                                event = {}
                                action = ent['request']['url'][ent['request']['url'][:37].rfind("/")+1:ent['request']['url'].index("?")]
                                event[action] = queryStringParameters
                                actualHttpEventsRequests.append (event)
                            else:
                                actualHttpEventsRequests.append(queryStringParameters)
                            reposnseParameters["code"] = ent["response"]["status"]
                        else:
                            writeToLog("DEBUG","Found matching request in har file that received http error code " + str(ent['response']['status']) + " " + ent['request']['url'])
                        urlFound = False
                        
            except Exception as inst:
                    log_exception(inst)
                    raise 
                
            return actualHttpEventsRequests 
    