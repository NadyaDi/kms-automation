import csv, pytest,os.path
import datetime
import time
import re
from selenium import webdriver
from timeit import Timer
from openpyxl import load_workbook
from openpyxl.styles import colors
from openpyxl.styles import Font
from localSettings import *
from logger import *
import localSettings

class clsAPI:
    
    #===========================================================================
    #the class contains functions that process player V2 API events. 
    #===========================================================================

        def removeUnnecessaryEvents(self,allEvents):
            finalEvents=allEvents.copy() #from finalEvents we are going to remove the unnecessary events
            i=0 
            while (i != len(finalEvents)):
                eventStr=finalEvents[i][9:]
                if((eventStr.startswith("playerStateChange: buffering") == True) or (eventStr.startswith("switchingChangeComplete") == True)
                    or (eventStr.startswith("switchingChangeStarted") == True) or (eventStr.startswith("videoMetadataReceived") == True)) :
                    finalEvents.remove(finalEvents[i])
                else:
                    i+=1
                #    writeToLog("DEBUG",eventStr)
                
            
            return finalEvents
        
        #===============================================================================
        # the function checks if the number of times an "replay" event jumped from the API events equal to expectedNum
        #===============================================================================
        def findReplayEvents(self,apiEvents,expectedNum):
            cnt=0
            for i in range (0,len(apiEvents)):
                eventStr = apiEvents[i][9:]
                if(eventStr.startswith("replay") == True):
                    cnt += 1
            if(cnt == expectedNum):
                return True
            else:
                return False
        
        def removeUnnecessaryStatsEvents(self,allEvents):
            finalEvents=allEvents.copy() #from finalEvents we are going to remove the unnecessary events
            i = 0 
            while (i!=len(allEvents)):
                eventStr=allEvents[i][9:]
                if((eventStr.startswith("bufferProgress NaN sec,  buffered: NaN") == True) or (eventStr.startswith("bytesDownloadedChange: NaN") == True) 
                    or (eventStr.startswith("monitorEvent") == True)):
                    finalEvents.remove(allEvents[i])
                #else:
                #    writeToLog("DEBUG",eventStr)
                i+=1
            
            return finalEvents
        
        #===============================================================================
        # The function verify the API events by comparing the expected
        # events from the test and the actual events we captures during it.
        # If you want to compare with regular expression, add "{regex}" string before the expected sting.
        #===============================================================================
        def verifyApiEvents(self,test, expectedApiEventsDict, apiEvents, driverFix):
            
            if(len(expectedApiEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                expectedApiEvents = expectedApiEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
            else:
                expectedApiEvents = expectedApiEventsDict["shared"]
            actualApiEvents = test.api.removeUnnecessaryEvents(apiEvents)
            writeToLog("INFO","verify API events")
            ret = test.api.compareApiEvents(expectedApiEvents,actualApiEvents,test)
            if (ret != True):
                test.status = "Fail"
            return test.status
        
        #===============================================================================
        # This function same as "verifyApiEvents", but without remove unnecessary events
        # The function verify the API events by comparing the expected
        # events from the test and the actual events we captures during it.
        # If you want to compare with regular expression, add "{regex}" string before the expected sting.
        #===============================================================================
        def verifyApiEventsFull(self,test, expectedApiEventsDict, apiEvents, driverFix):
            
            if(len(expectedApiEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                expectedApiEvents = expectedApiEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
            else:
                expectedApiEvents = expectedApiEventsDict["shared"]
            writeToLog("INFO","Going to verify API events")
            ret = test.api.compareApiEvents(expectedApiEvents,apiEvents,test)
            if (ret != True):
                test.status = "Fail"
            return test.status        
        
        #===============================================================================
        # The function verify the expected API events contain in the actual
        # If you want to compare with regular expression, add "{regex}" string before the expected sting.
        #===============================================================================
        def verifyContainApiEvents(self,test, expectedApiEvents, apiEvents, driverFix):
            actualApiEvents = test.api.removeUnnecessaryEvents(apiEvents)
            writeToLog("INFO","verify API events - contain")
            ret=test.api.isContainApiEvents(expectedApiEvents,actualApiEvents,test)
            if (ret != True):
                test.status = "Fail"
            return test.status
        
        #===============================================================================
        # The function verify the expected API Statistics events contain in the actual
        # If you want to compare with regular expression, add "{regex}" string before the expected sting.
        #===============================================================================
        def verifyContainApiStatistics(self,test, expectedApiEvents, apiEvents, driverFix):
            actualApiEvents=test.api.removeUnnecessaryStatsEvents(apiEvents)
            writeToLog("INFO","verify API Statistics events - contain")
            ret = test.api.isContainApiEvents(expectedApiEvents,actualApiEvents,test)
            if (ret != True):
                test.status = "Fail"
            return test.status       
        
        #===============================================================================
        # The function verify the expected API events comparing an expected results set
        #===============================================================================
        
        def compareApiEvents(self,expected,actual,test):
            ret = True
            if (len(expected) != len (actual)):
                    writeToLog("INFO","Number of events don't match. Expected: " +  str(len(expected)) + ", Actual: " + str(len(actual)));
                    ret=False
                    for i in range (0,min(len(expected),len(actual))):
                        writeToLog("INFO","expected   : " + str(i) + " " + expected[i])
                        writeToLog("INFO","Actual     : " + str(i) + " " + actual[i][9:])
                    if(len(expected)<len(actual)):
                        for i in range (len(expected),len(actual)):
                            writeToLog("INFO","Actual     : " + str(i) + " " + actual[i][9:])
                    elif(len(expected)>len(actual)):
                        for i in range (len(actual),len(expected)):
                            writeToLog("INFO","expected   : " + str(i) + " " + expected[i])
            else:
                for i in range (0,len(expected)):
                    if "{regex}" in expected[i]:
                        expected[i] = expected[i].replace("{regex}", "")
                        if(re.search(expected[i], actual[i][9:]))==None:
                            expected[i] = "{regex}" + expected[i]
                            writeToLog("INFO","In line " + str(i)+": " + "Expected: " +  expected[i] + ", Actual: " + actual[i][9:]);
                    else:    
                        if(actual[i][9:]!=expected[i]):
                            ret = False
                            writeToLog("INFO","In line " + str(i)+": " + "Expected: " +  expected[i] + ", Actual: " + actual[i][9:]);
            return ret 
        
        
        #===============================================================================================================        
        # the function verify that expected api events appear in the actual set. Order or num instances is not verified.
        #===============================================================================================================
        
        def isContainApiEvents(self,expected,actual,test):

            ret = True
            if (len(expected) > 0):
                #Concatenate all Actual events to one string
                strActualEvents = ""
                j = 0
                for j in range (0,len(actual)):
                    strActualEvents = strActualEvents + "\n" + actual[j][9:]
                writeToLog("INFO","Actual events: \n" + strActualEvents) 
                
                for i in range (0,len(expected)):
                    if "{regex}" in expected[i]:
                        expected[i] = expected[i].replace("{regex}", "")
                        if(re.search(expected[i], strActualEvents))==None:
                            expected[i] = "{regex}" + expected[i]
                            writeToLog("INFO","In line " + str(i)+": " + "Expected: " +  expected[i]);
                    else: 
                        if expected[i] not in strActualEvents:
                            ret = False
                            writeToLog("INFO","In line " + str(i)+": " + "Expected: " +  expected[i]);
            else:
                writeToLog("INFO","No expected API events!")
                ret = False
            return ret
        
        #===============================================================================    
        # the function verify that playback started by verifying bufferProgress event
        #===============================================================================
        def verifyPlayerBufferProgress(self,driver,testPage):
            ret = False
            timer = 0
            bufferedSec = list()
            TIMEOUT_TO_START_PLAYBACK = 60
            
            while (ret == False and timer < TIMEOUT_TO_START_PLAYBACK):            
                statsEvents = testPage.getStatisticsEvents(driver)
                for event in statsEvents:
                    seconds = re.search("\d+ sec", event)
                    if (seconds != None):
                        bufferedSec.append(int(seconds.group()[:-4]))
            
                if (len(bufferedSec) > 0):
                    numIncrementsViewed = 0
                    for i in range(0,len(bufferedSec) - 1):
                        if (bufferedSec[i + 1] - bufferedSec[i] > 1):
                            numIncrementsViewed = numIncrementsViewed + 1
                            if (numIncrementsViewed == 2): 
                                ret = True
                                break;
                                           
                time.sleep(1)
                timer = timer + 1
            
            return ret    
        
