from logger import *
from utilityTestFunc import *
import localSettings
from collections import OrderedDict
from re import split
import enums
import re
import json, urllib.parse
from openpyxl.chart.data_source import StrVal

class clsAnalytics:

    #=============================================================================================================
    #the class contains functions that relates to tests that checks the analytics events (like google analytics).
    #it contains some parsers for checking API events and HTTP events
    #=============================================================================================================

        def kalturaParseAnalyticsLine(self,events):      
                
            eventsArr  = []
            for event in events:
                try:            
                    event = json.loads(event[9:])
                except Exception as inst:
                    writeToLog("INFO","Fail to parse JSON " + event)
                    log_exception(inst)
                    raise
                eventsArr.append (event)
                
            return eventsArr
        
        def kalturaCompareHTTPEvents(self,test,expectedHttpEventsDict, actualEventsCapture,expectedHttpLiveEventsDict = None):
                
                writeToLog("INFO","verify Analytics HTTP events")    
                
                ret         = True     
                retTag      = True      
                retLine     = True    
                tagsCountDict = {  "1"  : [0,0],
                                   "2"  : [0,0],
                                   "3"  : [0,0],
                                   "4"  : [0,0],
                                   "5"  : [0,0],
                                   "6"  : [0,0],
                                   "7"  : [0,0],
                                   "12"  : [0,0],                                  
                                   "13"  : [0,0],
                                   "17"  : [0,0]
                                   } 
                ignoreParams     = ["event:sessionId","event:eventTimestamp","kalsig","event:historyEvents"]
                filterURL        = ['qa-apache-php7.dev.kaltura.com/api_v3/index.php?service=stats']
                ignoreParamsLive = ["event:eventTimestamp","kalsig","event:historyEvents"]
                filterURLLive    = ["il-coreqa-live4.dev.kaltura.com/api_v3/index.php?service"]
                
                actualEventsCapture.saveHar(test.myProxy.har)
                actualEvents = actualEventsCapture.createHttpAnalyticsDict(test.myProxy.har,ignoreParams,filterURL)
                if (expectedHttpLiveEventsDict != None):
                    actualEventsLive = actualEventsCapture.createHttpAnalyticsDict(test.myProxy.har,ignoreParamsLive,filterURLLive)
                
                if(len(expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                    expectedEvents = expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                else:
                    expectedEvents = expectedHttpEventsDict["shared"]
                
                if (expectedHttpLiveEventsDict != None):
                    if(len(expectedHttpLiveEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                        expectedEventsLive = expectedHttpLiveEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                    else:
                        expectedEventsLive = expectedHttpLiveEventsDict["shared"]
                
                for i in range (0,len(expectedEvents)):
                    if (expectedEvents[i]["event:eventType"] in tagsCountDict):
                        tagsCountDict[expectedEvents[i]["event:eventType"]][0] = tagsCountDict[expectedEvents[i]["event:eventType"]][0] + 1 
                    else: 
                        ret = False
                        writeToLog("INFO","found an unknown event, event " + expectedEvents[i]["event:eventType"] + " in expected results set at event " + str (i)) 
                        raise Exception("found an unknown event, event " + expectedEvents[i]["event:eventType"] + " in expected results set at event " + str (i))
                for i in range (0,len(actualEvents)):
                    if (actualEvents[i]["event:eventType"] in tagsCountDict):
                        tagsCountDict[actualEvents[i]["event:eventType"]][1] = tagsCountDict[actualEvents[i]["event:eventType"]][1] + 1 
                    else: 
                        ret = False
                        writeToLog("INFO","found an unknown event, event " + expectedEvents[i]["event:eventType"] + " in actual results set at event " + str (i)) 
                        raise Exception("found an unknown event, event " + expectedEvents[i]["event:eventType"] + " in actual results set at event " + str (i))
                
                # remove buffer events
                i=0 
                while (i < len(expectedEvents)):
                    if ("12" in expectedEvents[i]["event:eventType"] or "13" in expectedEvents[i]["event:eventType"]):
                        expectedEvents.remove(expectedEvents[i])
                    else:
                        i = i + 1
                i=0 
                while (i < len(actualEvents)):
                    if ("12" in actualEvents[i]["event:eventType"] or "13" in actualEvents[i]["event:eventType"]):
                        actualEvents.remove(actualEvents[i])
                    else:
                        i = i + 1
               
                ret = self.compareLengthOfActualVsExpectedDict(actualEvents,expectedEvents)
                if (ret == True):
                    for i in range (0,len(expectedEvents)):
                                if (len(expectedEvents[i]) == len(actualEvents[i])):
                                    for tag in actualEvents[i]:
                                        if (tag == "startedDateTime" or tag == "startedDateEpoc"):
                                            pass
                                        elif (tag == "event:currentPoint"):
                                            currentPointDif = int (int(actualEvents[i][tag]) /1000) - int (int(expectedEvents[i][tag]) /1000)
                                            if (  currentPointDif > 1 or currentPointDif < -1):
                                                retTag = False
                                                retLine = False
                                        elif (tag == "event:duration"):                                                
                                            if (int(float(actualEvents[i][tag])) != int(float(expectedEvents[i][tag]))):
                                                retTag = False
                                                retLine = False
                                        elif (actualEvents[i][tag] != expectedEvents[i][tag]):
                                                retTag = False
                                                retLine = False
                                        if (retTag == False):
                                            writeToLog("INFO","Expected : " + str(i) + " " + tag + " " + str(expectedEvents[i][tag]))
                                            writeToLog("INFO","Actual   : " + str(i) + " " + tag + " " + str(actualEvents[i][tag]))
                                            retTag = True
                                    if (retLine == False):
                                        writeToLog("INFO","Expected : " + str(i) + " " + json.dumps(OrderedDict(sorted(expectedEvents[i].items()))))
                                        writeToLog("INFO","Actual   : " + str(i) + " " + json.dumps(OrderedDict(sorted(actualEvents[i].items()))))
                                        ret = False
                                        retLine = True
                                else:
                                    writeToLog("INFO","Number of tags doesn't match")
                                    writeToLog("INFO","Expected : " + str(i) + " " + json.dumps(OrderedDict(sorted(expectedEvents[i].items()))))
                                    writeToLog("INFO","Actual   : " + str(i) + " " + json.dumps(OrderedDict(sorted(actualEvents[i].items()))))
                                    self.writeToLogDifBetweenDictioanries(expectedEvents[i],actualEvents[i])
                                    ret = False                                     
                
                if (ret == False):
                    expectedVSActual = ""
                    newLine = ""
                    for tag in tagsCountDict:
                        if (tagsCountDict[tag][0] != tagsCountDict[tag][1]):
                            if (expectedVSActual != ""):
                                newLine = "\n"    
                            expectedVSActual = expectedVSActual + newLine + " expected event " + tag + " count: " + str(tagsCountDict[tag][0]) + ", " + "actual: " + str(tagsCountDict[tag][1])
                    if (expectedVSActual != ""):
                                writeToLog("INFO","Events count:\n" + expectedVSActual)
                
                if (expectedHttpLiveEventsDict != None):
                     
                    retTag      = True      
                    retLine     = True    
                    retBitrate  = False

                    if (len(actualEventsLive) == 0):
                        writeToLog("INFO","No live statistics events requests captured")
                        ret = False
                        writeToLog("INFO","Expected live stats base event  : " + str(i) + " " + json.dumps(OrderedDict(sorted(expectedEventsLive[0].items()))))
                    else:
                        if (re.match("[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}", actualEventsLive[0]["event:sessionId"]) == None):
                            writeToLog("INFO","Session id is not in known format : " + str(i) + " " + actualEventsLive[i]["event:sessionId"])
                            ret = False
                        else:
                            for i in range (0,len(actualEventsLive)):
                                    if (len(actualEventsLive[i]) != len(expectedEventsLive[0])):
                                        writeToLog("INFO","Number of tags is not equal. Expected: " + str(len(expectedEventsLive[0]))   + " Actual: " + str(len(actualEventsLive[i])))
                                        writeToLog("INFO","Actual   : " + str(i) + " " + json.dumps(OrderedDict(sorted(actualEventsLive[i].items()))))
                                        ret = False
                                    else:
                                        for tag in actualEventsLive[i]:
                                            if (tag == "startedDateTime" or tag == "startedDateEpoc" or tag == "event:bufferTime" or tag == "event:startTime"):
                                                pass
                                            elif (tag == "event:eventIndex"):
                                                if (actualEventsLive[i][tag] != str(i + 1)):
                                                    writeToLog("INFO","Expected : " + str(i) + " " + tag + " " + str(expectedEventsLive[0][tag]))
                                                    writeToLog("INFO","Actual   : " + str(i) + " " + tag + " " + str(actualEventsLive[i][tag]))
                                                    retLine = False
                                                    ret = False
                                            elif (tag == "event:sessionId"):
                                                if (actualEventsLive[i][tag] != actualEventsLive[0][tag]):
                                                    writeToLog("INFO","Expected : " + str(i) + " " + tag + " " + str(actualEventsLive[0][tag]))
                                                    writeToLog("INFO","Actual   : " + str(i) + " " + tag + " " + str(actualEventsLive[i][tag]))
                                                    retLine = False
                                                    ret = False
                                            elif (tag == "event:bitrate"):
                                                if (float(actualEventsLive[i][tag]) > 0):
                                                    retBitrate = True    
                                            elif (actualEventsLive[i][tag] != expectedEventsLive[0][tag]):
                                                writeToLog("INFO","Expected : " + str(i) + " " + tag + " " + str(expectedEventsLive[0][tag]))
                                                writeToLog("INFO","Actual   : " + str(i) + " " + tag + " " + str(actualEventsLive[i][tag]))
                                                retLine = False
                                                ret = False
                                        if (retLine == False):
                                            writeToLog("INFO","Actual   : " + str(i) + " " + json.dumps(OrderedDict(sorted(actualEventsLive[i].items()))))
                                            ret = False
                                            retLine = True
                            if (retBitrate == False):
                                writeToLog("INFO","Bitrate not reported threw the viewing session")
                                ret = False
                                                                  
                return ret       
        
        def kalturaCompareAPIEvents(self,test,expectedAnalyticsEventsDict,actual):
            
                ret               = True
                lineRet           = True
                adsCount          = [0,0]
                
                
                tagsCountDict = {  "MEDIA_LOADED"  : [0,0],
                                   "WIDGET_LOADED"  : [0,0],
                                   "PLAY"  : [0,0],
                                   "SEEK"  : [0,0],
                                   "PLAY_REACHED_25"  : [0,0],
                                   "PLAY_REACHED_50"  : [0,0],
                                   "PLAY_REACHED_75"  : [0,0],
                                   "PLAY_REACHED_100"  : [0,0]                                  
                                   } 
                
                writeToLog("INFO","verify Analytics events")
                
                try:
                
                    if(len(expectedAnalyticsEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                        expected = expectedAnalyticsEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                    else:
                        expected = expectedAnalyticsEventsDict["shared"]   
                    
                    actual = self.kalturaParseAnalyticsLine (actual)
                    
                    for event in expected:
                        if (event["name"] in tagsCountDict):
                            tagsCountDict[event["name"]][0] = tagsCountDict[event["name"]][0] + 1
                        else:
                            ret = False
                            writeToLog("INFO","found an unknown tag in expected results set : " + event["name"])
                            raise Exception("found an unknown tag in actual results set : " + event["name"])
                    for event in actual:
                            tagsCountDict[event["name"]][1] = tagsCountDict[event["name"]][1] + 1
                    
                    ret = self.compareLengthOfActualVsExpectedDict(actual,expected)
                    if (ret == True):
                        for i in range (0,len(expected)):
                            if (expected[i]["name"] !=  actual[i]["name"]):
                                    ret = False   
                                    writeToLog("INFO","Expected   : " + str(i) + " action : " + expected[i]["name"])
                                    writeToLog("INFO","Actual     : " + str(i) + " action : " + actual[i]["name"])
                                    writeToLog("INFO","Expected   : " + str(i) + " " + json.dumps(OrderedDict(sorted(expected[i].items()))))
                                    writeToLog("INFO","Actual     : " + str(i) + " " + json.dumps(OrderedDict(sorted(actual[i].items()))))
                            else:
                                for param in expected[i]:
                                    if (param == "eventTimestamp"):
                                        pass
                                    elif (param == "currentPoint"):
                                        difCurrentPoint = int(int(expected[i][param]) / 1000) - int(int(actual[i][param]) / 1000)
                                        if ( difCurrentPoint > 1 or difCurrentPoint < -1  ):
                                            ret = False
                                            lineRet = False
                                            writeToLog("INFO","Expected   : " + str(i) + " " + param + " : " + expected[i][param])
                                            writeToLog("INFO","Actual     : " + str(i) + " " + param + " : " + actual[i][param]) 
                                    elif (param == "duration"):
                                        if ( int(float(expected[i][param])) != int(float(actual[i][param]))):
                                            ret = False
                                            lineRet = False
                                            writeToLog("INFO","Expected   : " + str(i) + " " + param + " : " + expected[i][param])
                                            writeToLog("INFO","Actual     : " + str(i) + " " + param + " : " + actual[i][param])
                                    else:
                                        if (expected[i][param] != actual[i][param]):
                                            ret = False
                                            lineRet = False
                                            writeToLog("INFO","Expected   : " + str(i) + " " + param + " : " + expected[i][param])
                                            writeToLog("INFO","Actual     : " + str(i) + " " + param + " : " + actual[i][param])
                                if (lineRet == False):
                                        writeToLog("INFO","Expected   : " + str(i) + " " + json.dumps(OrderedDict(sorted(expected[i].items()))))
                                        writeToLog("INFO","Actual     : " + str(i) + " " + json.dumps(OrderedDict(sorted(actual[i].items()))))
                                        lineRet = True   
                    
                    if (ret == False):
                        expectedVSActual = ""
                        newLine = ""
                        for tag in tagsCountDict:
                                if (tagsCountDict[tag][0] != tagsCountDict[tag][1]):
                                    if (expectedVSActual != ""):
                                        newLine = "\n"    
                                    expectedVSActual = expectedVSActual + newLine + "expected count : " + tag + " " + str(tagsCountDict[tag][0]) + ", " + "actual: " + str(tagsCountDict[tag][1])
                        if (adsCount[0] != adsCount[1]):
                            if (expectedVSActual != ""):
                                newLine = "\n"   
                            expectedVSActual = expectedVSActual + newLine + "expected ads: " + str(adsCount[0]) + ", " + "actual ads: " + str(adsCount[1])
                        if (expectedVSActual != ""):
                            writeToLog("INFO","Events count:\n" + expectedVSActual)

                except Exception as inst:
                    log_exception(inst)
                    raise
                    
                return ret
        
        def comScoreStreamingTagCompareHTTPEvents(self,test,expectedHttpEventsDict, actualEventsCapture):
                
                writeToLog("INFO","verify Analytics HTTP events")    
                
                cValueEqual = True
                ret         = True               
                tagsCountDict = { 
                                   "play"  : [0,0],
                                   "hb"    : [0,0],
                                   "end"   : [0,0],
                                   "pause" : [0,0]
                                   }  
                
                ignoreParams   = ["ns_st_bt","ns_st_an","ns_st_ppc","ns_st_br","ns_st_smv","ns_st_skt","accessControlId", "ns_st_an","ns_st_dskc","ns_st_dpc","ns_st_pp","ns_st_pb", "ns_st_asq","ns_st_psq","ns_st_tp","ns_st_bc","ns_st_sv","ns_st_lt","ns_st_dbt","ns_st_pa","ns_st_dbc","ns_st_it","ns_st_sc","capabilities","totalRank","ns_st_skc","ns_type","entitledUsersEdit","ns_st_sq","version","ns_st_ty","entitledUsersPublish","ns_st_ub","replacementStatus","displayInSearch","operationAttributes","rank","ns_st_pc","partnerSortValue","ns_st_ki","votes","ns_st_rt","licenseType","ns_st_skd","ns_st_ska","ns_st_sp", "ns_st_spc", "ns_st_apc", "ns_st_dskt","ns_st_dska","ns_st_dpt","ns_st_dupc","ns_st_dlpa","ns_st_dlpc","ns_st_dupa","ns_st_id","ns_st_upc","ns_st_iupa","ns_st_bp","ns_st_iupc","ns_st_dupa","ns_st_id","ns_ts","ns_st_upa","ns_st_ipt","ns_st_lpc","ns_st_lpa","ns_st_det"]
                filterURL      = ['b.scorecardresearch.com/p']
                skipableEvents = ['play','pause','hb','end']
                
                actualEventsCapture.saveHar(test.myProxy.har)
                actualEvents = actualEventsCapture.createHttpAnalyticsDict(test.myProxy.har,ignoreParams,filterURL)
                
                if(len(expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                    expectedEvents = expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                else:
                    expectedEvents = expectedHttpEventsDict["shared"]
                
                try:
                
                    for i in range (0,len(expectedEvents)):
                            action = expectedEvents[i]["ns_st_ev"]
                            if (action in tagsCountDict):
                                tagsCountDict[action][0] = tagsCountDict[action][0] + 1 
                            else: 
                                    ret = False
                                    writeToLog("INFO","found an unknown tag in expected results set : " + action + " at event " + str (i)) 
                                    raise Exception("found an unknown tag in actual results set : " + action + " at event " + str (i))
                    
                    for i in range (0,len(actualEvents)):
                        if ("ns_st_ev" in actualEvents[i]):
                            action = actualEvents[i]["ns_st_ev"]
                            if (action in tagsCountDict):
                                tagsCountDict[action][1] = tagsCountDict[action][1] + 1
                            else:
                                ret = False 
                                writeToLog("INFO","found an unknown tag in actual results set : " + action)
                                raise Exception("found an unknown tag in actual results set : " + action + " " + actualEvents[i])
                        else:
                            ret = False 
                            writeToLog("INFO","ns_st_ev tag wasn't found in event : " + action  + " " + json.dumps(OrderedDict(sorted(actualEvents[i].items()))))
                            raise Exception("ns_st_ev tag wasn't found in action : " + action + " " + json.dumps(OrderedDict(sorted(actualEvents[i].items()))))
                            
                    ret = self.compareLengthOfActualVsExpectedDict(actualEvents,expectedEvents)
                    actualI = 0
                    expectedI = 0
                    while (actualI < len(actualEvents) and expectedI < len(expectedEvents)):
                        if (actualI < len(actualEvents) - 1 and expectedI < len(expectedEvents) - 1):
                                if (expectedEvents[expectedI]["ns_st_ev"] == "play" and actualEvents[actualI + 1]["ns_st_ev"] == "play" and expectedEvents[expectedI + 1]["ns_st_ev"] == "end" and actualEvents[actualI]["ns_st_ev"] == "end"):
                                    temp = actualEvents[actualI]
                                    actualEvents[actualI] = actualEvents[actualI + 1]
                                    actualEvents[actualI + 1] = temp
                                    writeToLog("DEBUG","Performed swap between " + actualEvents[actualI]["ns_st_ev"] + " at " + str(actualI) + " and " + actualEvents[actualI + 1]["ns_st_ev"] + " at " + str(actualI+1))
                                    continue
                        actualAction   = actualEvents[actualI]["ns_st_ev"]
                        expectedAction = expectedEvents[expectedI]["ns_st_ev"]
                        if (actualAction == expectedAction):
                            if (len(expectedEvents[expectedI]) == len(actualEvents[actualI])):
                                for cValue in actualEvents[actualI]:
                                    if (cValue == "startedDateTime" or cValue == "startedDateEpoc"):
                                        pass
                                    elif (actualEvents[actualI][cValue] != expectedEvents[expectedI][cValue]):
                                        if ("ns_st_po" in cValue or "ns_st_pa" in cValue or "ns_st_pt" in cValue or "ns_st_et" in cValue or "ns_st_cl" in cValue):
                                            actualCValue = int(int(actualEvents[actualI][cValue]) /1000)
                                            expectedCValue = int(int (expectedEvents[expectedI][cValue]) / 1000)
                                            if (abs (actualCValue - expectedCValue) > 9):
                                                cValueEqual = False
                                        elif ("ns_st_bt" in cValue or "plays" in cValue or "views" in cValue):
                                            actualCValue = int(actualEvents[actualI][cValue])
                                            expectedCValue = int (expectedEvents[expectedI][cValue])
                                            if (actualCValue <= 0):
                                                cValueEqual = False
                                        elif ("lastPlayedAt" in cValue):
                                            actualCValue = int(actualEvents[actualI][cValue])
                                            if (actualCValue < 1498134910):
                                                cValueEqual = False
                                        else:
                                            cValueEqual = False
                                        if (cValueEqual == False):
                                            cValueEqual = True
                                            ret = False
                                            writeToLog("INFO","Expected : " + str(expectedI) + " " + cValue + " " + str(expectedEvents[expectedI][cValue]))
                                            writeToLog("INFO","Actual   : " + str(actualI) + " " + cValue + " " + str(actualEvents[actualI][cValue]))
                                            writeToLog("INFO","Expected : " + str(expectedI) + " " + json.dumps(OrderedDict(sorted(expectedEvents[expectedI].items()))))
                                            writeToLog("INFO","Actual   : " + str(actualI) + " " + json.dumps(OrderedDict(sorted(actualEvents[actualI].items()))))
                            else:
                                writeToLog("INFO","Number of C tags doesn't match")
                                writeToLog("INFO","Expected : " + str(expectedI) + " " + json.dumps(OrderedDict(sorted(expectedEvents[expectedI].items()))))
                                writeToLog("INFO","Actual   : " + str(actualI) + " " + json.dumps(OrderedDict(sorted(actualEvents[actualI].items()))))
                                self.writeToLogDifBetweenDictioanries(expectedEvents[expectedI],actualEvents[actualI])
                                ret = False
                        elif (actualAction in skipableEvents):
                            writeToLog("DEBUG","Expected : action at line " + str(expectedI) + " " + expectedAction + " . Actual: "  + actualAction + " at line " + str(actualI))
                            writeToLog("DEBUG","Trying to skip event at actual set")
                            actualI += 1
                            continue
                        else:
                            writeToLog("INFO","Expected action : " + str(expectedI) + " " +  actualAction +  " " + json.dumps(OrderedDict(sorted(expectedEvents[expectedI].items()))))
                            writeToLog("INFO","Actual action   : " + str(actualI) +  " " + expectedAction + " " + json.dumps(OrderedDict(sorted(actualEvents[actualI].items()))))
                            ret = False

                        actualI += 1 
                        expectedI += 1                            
    
                    if (ret == False):
                        expectedVSActual = ""
                        newLine = ""
                        for tag in tagsCountDict:
                            if (tagsCountDict[tag][0] != tagsCountDict[tag][1]):
                                if (expectedVSActual != ""):
                                    newLine = "\n"    
                                expectedVSActual = expectedVSActual + newLine + " expected " + tag + " count: " + str(tagsCountDict[tag][0]) + ", " + "actual: " + str(tagsCountDict[tag][1])
                        if (expectedVSActual != ""):
                                    writeToLog("INFO","C tags count:\n" + expectedVSActual)
                
                except Exception as inst:
                    log_exception(inst)
                    raise
                                        
                return ret
        
        def comScoreStreamingTagCompareAPIEvents(self,test,expectedAnalyticsEventsDict,actual):
            
                ret             = True
                tempRet         = True
                adsCount        = [0,0]
                
                tagsCountDict = { 
                                   'notifyChangeVolume'    : [0,0],
                                   'createPlaybackSession' : [0,0],
                                   'setAsset'              : [0,0],
                                   'notifyBufferStart'     : [0,0], 
                                   'notifyBufferStop'      : [0,0],  
                                   'notifyPlay'            : [0,0],
                                   'notifyPause'           : [0,0],  
                                   'notifyEnd'             : [0,0],
                                   'notifySeekStart'       : [0,0]
                                   } 
                
                writeToLog("INFO","verify Analytics events")
                
                try:
                
                    if(len(expectedAnalyticsEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                        expected = expectedAnalyticsEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                    else:
                        expected = expectedAnalyticsEventsDict["shared"]               
                    
                    #Count tags 
                    for i in range (0,len(expected)):
                        expectedJson = expected[i]
                        if (expectedJson[0] in tagsCountDict):
                            tagsCountDict[expectedJson[0]][0] = tagsCountDict[expectedJson[0]][0] + 1
                        else:
                            ret = False
                            writeToLog("INFO","found an unknown tag in expected results set : " + expectedJson[0])
                            writeToLog("INFO",expected[i][0])
                            raise Exception("found an unknown tag in actual results set : " + expectedJson[0] + " " + expected[i])
                        if ("setAsset" in expectedJson[0]):
                            if ("ns_st_ad" in expectedJson[1].keys()):
                                if (expectedJson[1]["ns_st_ad"] == "1"):            
                                    adsCount[0] = adsCount[0] + 1    
                    for i in range (0,len(actual)):
                        actualJson   = json.loads(actual[i][9:])
                        tagsCountDict[actualJson[0]][1] = tagsCountDict[actualJson[0]][1] + 1
                        if ("setAsset" in actualJson[0]):
                            if ("ns_st_ad" in actualJson[1].keys()): 
                                if (actualJson[1]["ns_st_ad"] == "1"):
                                    adsCount[1] = adsCount[1] + 1

                    ret = self.compareLengthOfActualVsExpectedDict(actual,expected)
                    if (ret == True):
                        for i in range (0,len(expected)):
                            expectedJson = expected[i]
                            try:            
                                actualJson   = json.loads(actual[i][9:])
                            except Exception as inst:
                                writeToLog("INFO","Fail to parse JSON " + actual[i][9:])
                                log_exception(inst)
                                raise    
                              
                            if (actualJson[0] != expectedJson[0]):
                                    ret = False
                                    writeToLog("INFO","Expected   : " + str(i) + " action : " + expectedJson[0])
                                    writeToLog("INFO","Actual     : " + str(i) + " action : " + actualJson[0])
                                    writeToLog("INFO","Expected   : " + str(i) + " " + json.dumps(expectedJson))
                                    writeToLog("INFO","Actual     : " + str(i) + " " + json.dumps(actualJson))
                            else:
                                if (len(actualJson) == 2 and len(expectedJson) == 2):                                
                                    if (isinstance( actualJson[1], dict) and isinstance( expectedJson[1], dict)):
                                        if (len(actualJson[1]) == len(expectedJson[1])):
                                            for key in actualJson[1]:
                                                if (key in expectedJson[1].keys()):
                                                    actualValue = self.getStringValue(actualJson[1][key])
                                                    expectedValue = self.getStringValue(expectedJson[1][key])
                                                    if ("ns_st_ad" in actualJson[1].keys()):
                                                        if (key == "ns_st_ci"):    
                                                            if (re.match("\d+", actualJson[1][key]) == None):
                                                                continue
                                                    elif ("notifyEnd" in actualJson[1].keys()):
                                                        if (int(actualValue / 1000) != int(expectedValue)):
                                                            writeToLog("INFO","Expected   : " + str(i) + " Key value "  + actualJson[0] + " " + self.getStringValue(expectedValue))
                                                            writeToLog("INFO","Actual     : " + str(i) + " Key value "  + expectedJson[0] + " " + self.getStringValue(actualValue))                                            
                                                            tempRet = False
                                                            ret = False
                                                    elif (expectedValue != actualValue):
                                                        writeToLog("INFO","Expected   : " + str(i) + " Key value "  + key + " " + expectedValue)
                                                        writeToLog("INFO","Actual     : " + str(i) + " Key value "  + key + " " + actualValue)                                            
                                                        tempRet = False
                                                        ret = False
                                                else:
                                                    writeToLog("INFO","Expected   : " + str(i) + " Key "  + key + " doesn't exist in actual")
                                                    tempRet = False
                                                    ret = False
                                        else:
                                            writeToLog("INFO","Number of tags in the event are not equal")
                                            tempRet = False
                                            ret = False
                                    else:
                                        actualValue   = actualJson[1]
                                        expectedValue = expectedJson[1]
                                        if (actualJson[0] == "notifyPause" or actualJson[0] == "notifyEnd" or actualJson[0] == "notifyPlay" or actualJson[0] == "notifyBufferStart" or actualJson[0] == "notifyBufferStop"):
                                            if (int(actualJson[1] / 1000) < int(expectedJson[1]/1000) - 2 or int(actualJson[1] / 1000) > int(expectedJson[1]/1000) + 2):
                                                writeToLog("INFO","Expected   : " + str(i) + " Key value "  + actualJson[0] + " " + self.getStringValue(expectedValue))
                                                writeToLog("INFO","Actual     : " + str(i) + " Key value "  + expectedJson[0] + " " + self.getStringValue(actualValue))                                            
                                                tempRet = False
                                                ret = False
                                        elif (expectedValue != actualValue):
                                            writeToLog("INFO","Expected   : " + str(i) + " Key value "  + actualJson[0] + " " + self.getStringValue(expectedValue))
                                            writeToLog("INFO","Actual     : " + str(i) + " Key value "  + expectedJson[0] + " " + self.getStringValue(actualValue))                                            
                                            tempRet = False
                                            ret = False
                                elif (len(actualJson) != len(expectedJson)):
                                    writeToLog("INFO","Expected   : " + str(i) + " tags at event "  + json.dumps(actualJson))
                                    writeToLog("INFO","Actual     : " + str(i) + " tags at event "  + json.dumps(expectedJson))                                            
                                    tempRet = False
                                    ret = False
                            if (tempRet == False):
                                writeToLog("INFO","Expected   : " + str(i) + " " + json.dumps(expectedJson))
                                writeToLog("INFO","Actual     : " + str(i) + " " + json.dumps(actualJson))
                                tempRet = True
                    else:
                        pass                                             
                    if (ret == False):
                        expectedVSActual = ""
                        newLine = ""
                        for tag in tagsCountDict:
                                if (tagsCountDict[tag][0] != tagsCountDict[tag][1]):
                                    if (expectedVSActual != ""):
                                        newLine = "\n"    
                                    expectedVSActual = expectedVSActual + newLine + "expected count : " + tag + " " + str(tagsCountDict[tag][0]) + ", " + "actual: " + str(tagsCountDict[tag][1])
                        if (adsCount[0] != adsCount[1]):
                            if (expectedVSActual != ""):
                                        newLine = "\n"   
                            expectedVSActual = expectedVSActual + newLine + "expected ads: " + str(adsCount[0]) + ", " + "actual ads: " + str(adsCount[1])
                        if (expectedVSActual != ""):
                                    writeToLog("INFO","C tags count:\n" + expectedVSActual)
                
                except Exception as inst:
                    log_exception(inst)
                    raise 
                   
                return ret       
                
        #extract the google events different values from the API event string    
        def gaParseAPILine(self,eventStr):      
            values = [0, 0, 0, 0, 0]
            params=["Category: "," Action: "," Opt_label: "," Opt_value: "] #the fifth val is for time
            
            eventStr = split(params[0], eventStr)
            values[4]=eventStr[0]
            eventStr = eventStr[1]
            eventStr = split(params[1], eventStr)
            values[0] = eventStr[0]
            eventStr = eventStr[1]
            eventStr = split(params[2], eventStr)
            values[1] = eventStr[0]
            eventStr = eventStr[1]
            eventStr = split(params[3], eventStr)
            values[2] = eventStr[0]
            values[3] = eventStr[1]
            return values

        #extract the google events different values from the HTTP traffic event string, returns a dictionary with the keys and extracted values. returns -1 if one of the requested values was missing.   
        def gaParseHTTPLine(self,eventStr):
            keys = ['utme','utmhn','utmt','utmsr','utmvp','utmdt','utmac','optval']
            myDict = {}
            for key in keys:
                if(key != 'optval'):
                    val = ""
                    currStr = key + "="
                    index=eventStr.find(currStr) #looks for a string formated like "utmhn="
                    if(index == -1):
                        return -1
                    curIndex = index + len(currStr)
                    next_char = eventStr[curIndex]
                    while(next_char != '&'): #collect the full value char by char
                        val = val + next_char
                        curIndex = curIndex + 1
                        next_char = eventStr[curIndex]
                    myDict[key] = val
                else: #we want to get the opt value when exist, if not we put 'undefined' value. we cut the opt value part put of the utme value
                    line = myDict.get('utme')
                    index = len(line)-1
                    c = line[index] #we start from the end of the line
                    possibleOptVal = ""
                    while(c != '%' and c != '('):
                        if(c.isdigit() == True):
                            possibleOptVal = c + possibleOptVal
                        index = index - 1 #we want to move to the left
                        c = line[index]
                    if(c == '('):
                        myDict['utme'] = myDict.get('utme')[0:index] #slice the opt value
                        myDict['optval'] = possibleOptVal #  update the opt value
                    else:
                        myDict['optval'] = 'undefined'
            return myDict

        #compare the expected and actual API events for google analytics tests. driverFix is the browser the test ran on.
        def gaCompareAPIEvents(self,test,expectedDict,actual):
            
                ret            = True
                params         = ["Category","Action","Opt_label","Opt_value"]
                actualParams   = []
                expectedParams = []
                
                writeToLog("INFO","verify Analytics events")
                
                if(len(expectedDict[localSettings.LOCAL_RUNNING_BROWSER])):
                    expected = expectedDict[localSettings.LOCAL_RUNNING_BROWSER]
                else:
                    expected = expectedDict["shared"]      
                
                #count number of events
                eventsCount = {
                        "100_pct_watched" : [0,0],
                        "25_pct_watched" : [0,0],
                        "50_pct_watched" : [0,0],
                        "75_pct_watched" : [0,0],
                        "AdSupport_EndAdPlayback" : [0,0],
                        "AdSupport_StartAdPlayback" : [0,0],
                        "adEnd" : [0,0],
                        "adStart" : [0,0],
                        "changeMedia" : [0,0],
                        "doPause" : [0,0],
                        "doSeek" : [0,0],
                        "kdpReady" : [0,0],
                        "mediaReady" : [0,0],
                        "midSequenceComplete" : [0,0],
                        "midSequenceStart" : [0,0],
                        "playerPlayEnd" : [0,0],
                        "playerPlayed" : [0,0],
                        "postSequenceComplete" : [0,0],
                        "postSequenceStart" : [0,0],
                        "preSequenceComplete" : [0,0],
                        "preSequenceStart" : [0,0],
                        "playing adOpportunity": [0,0],
                        "doPlay" : [0,0],
                        "adOpportunity": [0,0]
                }    
                
                for i in range (0,len(expected)):
                    expectedActionI = expected[i].find ("Action")
                    expectedA       = expected[i][expectedActionI + 9 :].find ("'")
                    expectedAction  = expected[i][expectedActionI+9: expectedA + expectedActionI + 9]
                    if (expectedAction in eventsCount):
                        eventsCount[expectedAction][0] = eventsCount[expectedAction][0] + 1
                    else:
                        writeToLog("INFO","found an expected action that doesn't exist in events list: " + expectedAction)
                for i in range (0,len(actual)):
                    actualActionI   = actual[i].find ("Action")
                    actualA         = actual[i][actualActionI + 9 :].find ("'")
                    actualAction    = actual[i][actualActionI+9: actualA + actualActionI + 9]
                    if (actualAction in eventsCount):
                        eventsCount[actualAction][1] = eventsCount[actualAction][1] + 1
                    else:
                        writeToLog("INFO","found an actual action that doesn't exist in events list: " + actualAction)

                ## Remove doSeekEvent should be done only for hlsJS!!!
                if (abs(eventsCount["doSeek"][0] - eventsCount["doSeek"][1]) <= 2 and abs(eventsCount["doSeek"][0] - eventsCount["doSeek"][1]) > 0
                    or
                    abs(eventsCount["doPause"][0] - eventsCount["doPause"][1]) <= 2 and abs(eventsCount["doPause"][0] - eventsCount["doPause"][1]) > 0                    
                    ):
                    writeToLog("INFO","Removing doSeek and doPause Events.")
                    i=0 
                    while (i < len(actual)):
                        if ("doSeek" in actual[i] or "doPause" in actual[i] ):
                            actual.remove(actual[i])
                        else:
                            i = i + 1
                    ## Remove doSeekEvent should be done only for hlsJS!!!
                    i=0 
                    while (i < len(expected)):
                        if ("doPause" in expected[i] or "doSeek" in expected[i]):
                            expected.remove(expected[i])
                        else:
                            i = i + 1
                       
                ##parse actual events##
                for i in range (0,len(actual)):
                    actualParams.append(self.gaParseAPILine(actual[i]))
                ##parse expected events##
                for i in range (0,len(expected)):
                    expectedParams.append(self.gaParseAPILine(expected[i]))
                
                ##check if the events match##
                if (len(expected) != len (actual)):
                        writeToLog("INFO","Number of events don't match. Expected : " +  str(len(expected)) + ", Actual: " + str(len(actual)))
                        ret=False
                        
                        for i in range (0,(len(expected))):
                            writeToLog("INFO","expected   : " + str(i) + " \"" + expected[i] + "\",")
                        for i in range (0,len(actual)):
                            writeToLog("INFO","Actual     : " + str(i) + " \"" + actual[i][9:] + "\",") # + " Time: " +actualParams[i][4])
                else:
                    for i in range (0,len(expected)):
                        for j in range (0,4):
                            if(expectedParams[i][j] != actualParams[i][j]):
                                if(j == 3): #we compare the Opt_value +-1
                                    if((expectedParams[i][j] != "'undefined'")and(actualParams[i][j] != "'undefined'")):
                                        if((int(actualParams[i][j].replace("'",""))) == (int(expectedParams[i][j].replace("'","")) + 1) or int(actualParams[i][j].replace("'","")) == int(expectedParams[i][j].replace("'","")) - 1):
                                            continue
                                ret = False
                                writeToLog("INFO","In line " + str(i) + ": " + params[j] + " don't match. Expected: " +  expectedParams[i][j] + ", Actual: " + actualParams[i][j])
                
                if (ret == False):
                    expectedVSActual = ""
                    newLine = "\n"
                    for action in eventsCount:
                        if (eventsCount[action][0] != eventsCount[action][1]):
                            if (expectedVSActual != ""):
                                    newLine = "\n"    
                            expectedVSActual = expectedVSActual + newLine + "Expected count " + str(eventsCount[action][0]) + " Actual count " + str(eventsCount[action][1]) +" of " + action
                    if (expectedVSActual != ""):
                                writeToLog("INFO","Events Summary:" + expectedVSActual)
                return ret

        def gaCompareHTTPEvents(self,test,expectedHttpEventsDict, actualEventsCapture):
                  
            ret = True
            
            writeToLog("INFO","verify Analytics HTTP events")
            
            #count number of events
            eventsCount = {
                        "100_pct_watched" : [0,0],
                        "25_pct_watched" : [0,0],
                        "50_pct_watched" : [0,0],
                        "75_pct_watched" : [0,0],
                        "AdSupport_EndAdPlayback" : [0,0],
                        "AdSupport_StartAdPlayback" : [0,0],
                        "adEnd" : [0,0],
                        "adStart" : [0,0],
                        "changeMedia" : [0,0],
                        "doPause" : [0,0],
                        "doSeek" : [0,0],
                        "kdpReady" : [0,0],
                        "mediaReady" : [0,0],
                        "midSequenceComplete" : [0,0],
                        "midSequenceStart" : [0,0],
                        "playerPlayEnd" : [0,0],
                        "playerPlayed" : [0,0],
                        "postSequenceComplete" : [0,0],
                        "postSequenceStart" : [0,0],
                        "preSequenceComplete" : [0,0],
                        "preSequenceStart" : [0,0],
                        "playing adOpportunity": [0,0],
                        "doPlay" : [0,0],
                        "adOpportunity": [0,0]
                }    
            
            try:
                
                actualEventsCapture.saveHar(test.myProxy.har)
                actualEvents = actualEventsCapture.createHttpGoogleAnalyticsDict(test.myProxy.har)                
                    
                if(len(expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                    expectedEvents = expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                else:
                    expectedEvents = expectedHttpEventsDict["shared"]
                
                for i in range (0,len(expectedEvents)):
                        firstAsterisk = expectedEvents[i]['utme'].index("*")
                        secondAsterik = expectedEvents[i]['utme'][firstAsterisk + 1:].index("*")
                        expectedAction = expectedEvents[i]['utme'][firstAsterisk + 1 :secondAsterik + firstAsterisk + 1]
                        if (expectedAction in eventsCount):
                            eventsCount[expectedAction][0] = eventsCount[expectedAction][0] + 1
                        else:
                            writeToLog("INFO","found an expected action that doesn't exist in events list: " + expectedAction)
                for i in range (0,len(actualEvents)):
                        firstAsterisk = actualEvents[i]['utme'].index("*")
                        secondAsterik = actualEvents[i]['utme'][firstAsterisk + 1:].index("*")
                        actualAction = actualEvents[i]['utme'][firstAsterisk + 1 :secondAsterik + firstAsterisk + 1]
                        if (actualAction in eventsCount):
                            eventsCount[actualAction][1] = eventsCount[actualAction][1] + 1
                        else:
                            writeToLog("INFO","found an actual action that doesn't exist in events list: " + actualAction)
                    
                
                ## Remove doSeekEvent should be done only for hlsJS!!!
                if (abs(eventsCount["doSeek"][0] - eventsCount["doSeek"][1]) <= 2 and abs(eventsCount["doSeek"][0] - eventsCount["doSeek"][1]) > 0
                    or
                    abs(eventsCount["doPause"][0] - eventsCount["doPause"][1]) <= 2 and abs(eventsCount["doPause"][0] - eventsCount["doPause"][1]) > 0                    
                    ):
                    writeToLog("INFO","Removing doSeek and doPause Events.")
                    i=0 
                    while (i < len(actualEvents)):
                        if ("doSeek" in actualEvents[i]['utme'] or "doPause" in actualEvents[i]['utme']):
                            actualEvents.remove(actualEvents[i])
                        else:
                            i = i + 1            
                    ## Remove doSeekEvent should be done only for hlsJS!!!
                    i=0 
                    while (i < len(expectedEvents)):
                        if ("doSeek" in expectedEvents[i]['utme'] or "doPause" in expectedEvents[i]['utme']):
                            expectedEvents.remove(expectedEvents[i])
                        else:
                            i = i + 1
                
                if (len(expectedEvents) != len (actualEvents)): #check if the expected and actual event number are equal, if not print the 'utme' of the events
                    writeToLog("INFO","Number of events don't match. Expected: " +  str(len(expectedEvents)) + ", Actual: " + str(len(actualEvents)))
                    
                    for i in range (0,len(expectedEvents)):
                        writeToLog("INFO","expected   : " + str(i) + " {'utme':'" +  expectedEvents[i].get('utme') + "','utmhn':'" +  expectedEvents[i].get('utmhn') + "','utmt':'" + expectedEvents[i].get('utmt') + "','utmsr':'" + expectedEvents[i].get('utmsr') + "','utmvp':'" + expectedEvents[i].get('utmvp') + "','utmdt':'" + expectedEvents[i].get('utmdt')  + "','utmac':'" + expectedEvents[i].get('utmac')   + "','optval':'" + expectedEvents[i].get('optval') + "'},")
                        
                    for i in range (0,len(actualEvents)):
                        writeToLog("INFO","actual   : " + str(i) + " {'utme':'" +  actualEvents[i].get('utme') + "','utmhn':'" +  actualEvents[i].get('utmhn') + "','utmt':'" + actualEvents[i].get('utmt') + "','utmsr':'" + actualEvents[i].get('utmsr') + "','utmvp':'" + actualEvents[i].get('utmvp') + "','utmdt':'" + actualEvents[i].get('utmdt')  + "','utmac':'" + actualEvents[i].get('utmac')   + "','optval':'" + actualEvents[i].get('optval') + "'},")
                    ret = False
                else:
                    for i in range (0,len(expectedEvents)): # if the events number is equal run over all the events in the dictionary 
                        swap = False # we want to make a swap one time at most
                        currActual = actualEvents[i]
                        currExpected = expectedEvents[i]
                        keys=OrderedDict(sorted(expectedEvents[i].items(), key=lambda t: len(t[0]))).keys()
                        for key in keys: # check if the expected and actual value of a key are the same in specific event i
                            if(key == 'Time'): # we are not matching the actual and expected time
                                continue
                            if (currExpected.get(key) != currActual.get(key)):
                                if ((key == 'utme')and(swap == False)):
                                        # events can appear one place before or after what we expected 
                                    if ((len(expectedEvents)>i+1) and(swap==False) and (currActual.get(key)==expectedEvents[i+1].get(key))):
                                            currExpected=expectedEvents[i+1]
                                            swap=True
                                            continue
                                    if ((0<i) and(swap == False) and (currActual.get(key) == expectedEvents[i-1].get(key))):
                                            currExpected = expectedEvents[i-1]
                                            swap=True
                                            continue
                                        #if((currExpected.get(key)=='kdpReady')or(currExpected.get(key)=='changeMedia')or(currExpected.get(key)=='mediaReady')):  #for the next 3 events we allow 2 place swap instead of 1
                                        # events can appear 2 places before or after what we expected 
                                    if ((len(expectedEvents)>i+2) and(swap==False) and (currActual.get(key) == expectedEvents[i+2].get(key))):
                                            currExpected = expectedEvents[i+2]
                                            swap=True
                                            continue
                                    if ((0<i-1) and(swap == False) and (currActual.get(key) == expectedEvents[i-2].get(key))):
                                            currExpected = expectedEvents[i-2]
                                            swap=True
                                            continue
                                        # events can appear 3 places before or after what we expected
                                    if ((len(expectedEvents)>i+3) and(swap==False) and (currActual.get(key)==expectedEvents[i+3].get(key))):
                                            currExpected = expectedEvents[i+3]
                                            swap=True
                                            continue
                                    if ((0<i-2) and(swap==False) and (currActual.get(key)==expectedEvents[i-3].get(key))):
                                            currExpected = expectedEvents[i-3]
                                            swap=True
                                            continue
                                if (key == 'optval'): # check if the expected opt value equals to +-1 the actual value
                                    if((currExpected.get(key)!="undefined")and(currActual.get(key)!="undefined")): # check that both of the values are numbers
                                        if((int(currActual.get(key))==(int(currExpected.get(key))+1) or (int(currActual.get(key))==int(currExpected.get(key))-1))):
                                                continue
                                if (key == "utmsr"):
                                        if (re.match("\d.+x\d.+", currActual.get(key)) != None):
                                            continue
                                writeToLog("INFO",key + " doesn't match in event " + str(i) + ". expected: " + expectedEvents[i].get(key)+ " actual: " + actualEvents[i].get(key))
                                ret = False
                                
                if (ret == False):
                        expectedVSActual = ""
                        newLine = "\n"
                        for action in eventsCount:
                            if (eventsCount[action][0] != eventsCount[action][1]):
                                if (expectedVSActual != ""):
                                        newLine = "\n"    
                                expectedVSActual = expectedVSActual + newLine + "Expected count " + str(eventsCount[action][0]) + " Actual count " + str(eventsCount[action][1]) +" of " + action
                        if (expectedVSActual != ""):
                                    writeToLog("INFO","Events Summary:" + expectedVSActual)
            except Exception as inst:
                    log_exception(inst)
                    raise
                            
            return ret
        
        def compareLengthOfActualVsExpectedDict(self,actualEvents,expectedEvents):
            
            ret = True
            
            if (len(expectedEvents) != len (actualEvents)):
                writeToLog("INFO","Number of events don't match. Expected " +  str(len(expectedEvents)) + ", Actual " + str(len(actualEvents)))
                ret = False
                for i in range (0,len(expectedEvents)):
                    if (isinstance(expectedEvents[i], list ) == True):
                        s = json.dumps(expectedEvents[i])
                    else:
                        s = json.dumps(OrderedDict(sorted(expectedEvents[i].items())))
                    writeToLog("INFO","Expected   : " + str(i) + " " + s)
                for i in range (0,len(actualEvents)):
                    if (isinstance(actualEvents[i], list ) == True):
                        s = json.dumps(actualEvents[i])
                    elif (isinstance(actualEvents[i], str ) == True):
                        s = json.dumps(actualEvents[i][9:])
                    else:
                        s = json.dumps(OrderedDict(sorted(actualEvents[i].items())))
                    writeToLog("INFO","Actual   : " + str(i) + " " + s)     
            return ret        
            
        def compareLengthOfActualVsExpectedArrays(self,actual,expected):
            
            ret = True
            
            if (len(expected) != len (actual)):
                writeToLog("INFO","Number of events don't match. Expected " +  str(len(expected)) + ", Actual " + str(len(actual)))
                ret = False
                for i in range (0,len(expected)):
                    writeToLog("INFO","expected   : " + str(i) + " " + expected[i])
                for i in range (0,len(actual)):
                    writeToLog("INFO","Actual     : " + str(i) + " " + actual[i][9:])
            
            return ret
                
        def youboraCompareResource(self,expectedEventIndex,actualEventIndex,actualResource,expctedResource):
                                        
            ret = True
            
            actualResourceParams          = urllib.parse.parse_qs(actualResource[actualResource.index("?") + 1:])
            expectedResourceParams        = urllib.parse.parse_qs(expctedResource[expctedResource.index("?") + 1:])
            actualResourceURL             = actualResource[:actualResource.index("?")]
            expectedResourceURL           = expctedResource[:expctedResource.index("?")]
            if (len(actualResourceParams) != len(expectedResourceParams)):
                writeToLog("INFO","Expected: Number of properties at event (resource details) " + str(len(expectedResourceParams)) + ". Actual: "  + str(len(actualResourceParams)))
                self.writeToLogDifBetweenDictioanries(expectedResourceParams,actualResourceParams)
                ret = False
            if (actualResourceURL != expectedResourceURL):
                    writeToLog("INFO","Expected: at line " + str(expectedEventIndex) + " url " + expectedResourceURL + " . Actual: " + actualResourceURL + " at line " + str(actualEventIndex))
                    ret = False
            for p in actualResourceParams:
                if (p == "playSessionId" or p == "ks"):
                    ksRegExp = "[a-zA-Z0-9]+"
                    playSessionIDRegExp = "[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}"
                    if (p == "ks"):
                        regexp = ksRegExp
                    else:
                        regexp = playSessionIDRegExp
                    if (re.match(regexp, actualResourceParams[p][0]) == None):
                        writeToLog("INFO","Expected: at line " + str(expectedEventIndex) + ", " + p + " at resource " + actualResourceParams[p][0] + ". Actual : " + regexp + " at line " + str(actualEventIndex))
                        ret = False
                    continue
                try:
                    if (actualResourceParams[p][0] != expectedResourceParams[p][0]):
                        expectedStrValue = self.getStringValue(expectedResourceParams[p][0])
                        actualStrValue   = self.getStringValue(actualResourceParams[p][0])
                        writeToLog("INFO","Expected: at line " + str(expectedEventIndex) + " " + p + " at resource " + expectedStrValue + ". Actual: " + actualStrValue + " at line " + str(actualEventIndex))
                        ret = False
                except KeyError as inst:
                        writeToLog("INFO","Expected: at line " + str(expectedEventIndex) + " " + p + " at resource doesn't exist in the Expected resource"  + " at line " + str(actualEventIndex))
            
            return ret
        
        def youboraCompareEntryDetails(self,expectedEventIndex,actualEventIndex,actualEntryDetails,expectedEntryDetails):
            
            ret = True
            
            try:
                for key in actualEntryDetails:
                    if (key == "sessionId"):
                        playSessionIDRegExp = "[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}"
                        if (re.match(playSessionIDRegExp, actualEntryDetails[key]) == None):
                            writeToLog("INFO","Expected: at line " + str(expectedEventIndex) + ", session ID is not in the expected format. Actual: " + actualEntryDetails[key] + " at line " + str(actualEventIndex))
                            ret = False
                    elif (actualEntryDetails[key] != expectedEntryDetails[key]):
                        expectedStrValue = self.getStringValue(expectedEntryDetails[key])
                        actualStrValue   = self.getStringValue(actualEntryDetails[key])
                        writeToLog("INFO","Expected : at line " + str(expectedEventIndex) + " " + key + " " + expectedStrValue + ". Actual " + actualStrValue + " at line " + str(actualEventIndex))
                        ret = False
            except KeyError as inst:
                    writeToLog("INFO","The following property " + key + " doens't exist in expected start event")
                    log_exception(inst)
                                                        
            return ret
        
        def youboraCompareStartOrErrorEvent(self,expectedEventIndex,actualEventIndex,actualStartStopEvent,expectedStartStopEvent):
                                
            ret = True
                                
            for key in actualStartStopEvent:
                if (key == "code" or key == "properties"):
                        continue
                elif (key == "resource"):
                    ret = self.youboraCompareResource(expectedEventIndex,actualEventIndex,actualStartStopEvent[key],expectedStartStopEvent[key])
                elif (key == "live"):
                    if (actualStartStopEvent[key] != expectedStartStopEvent[key] and self.getStringValue(expectedStartStopEvent[key]).lower() != self.getStringValue(actualStartStopEvent[key]).lower()):
                        writeToLog("INFO","Expected: at line " + str(expectedEventIndex) + " " + key + " " + self.getStringValue(expectedStartStopEvent[key]) + ". Actual " + self.getStringValue(actualStartStopEvent[key]) + " at line " + str(actualEventIndex))
                        ret = False
                elif (key == "timemark"):
                    pass
                elif (actualStartStopEvent[key] != expectedStartStopEvent[key]):
                    expectedStrValue = self.getStringValue(expectedStartStopEvent[key])
                    actualStrValue   = self.getStringValue(actualStartStopEvent[key])
                    writeToLog("INFO","Expected: at line " + str(expectedEventIndex) + " " + key + " " + expectedStrValue + ". Actual " + actualStrValue + " at line " + str (actualEventIndex))
                    ret = False
                            
            return ret 
        
        def youboraRemoveBufferEvents(self,events):
    
                    temp = []
                    
                    for event in events:
                        actionTemp = event[9:]
                        actualAction   = actionTemp[:actionTemp.index(":")]
                        if ("bufferUnderrun" in actualAction):
                            pass
                        else:
                            temp.append(event)
                    return temp
        
        def youboraCompareEvents(self,test,expected,actual,entryType,adType = None):
                
                ret             = True
                eventsCountDict = { 
                                "data"             : [0,0],
                                "start"            : [0,0],
                                "ping"             : [0,0],
                                "joinTime"         : [0,0],
                                "resume"           : [0,0],
                                "pause"            : [0,0],
                                "stop"             : [0,0],
                                "bufferUnderrun"   : [0,0],
                                "error"            : [0,0],
                                "adStart"          : [0,0], 
                                "adJoinTime"       : [0,0],  
                                "adStop"           : [0,0],
                                "adPause"          : [0,0],
                                "adBufferUnderrun" : [0,0],
                                "seek"             : [0,0]
                }
                
                entryIndex = -2
                code       = ""
                
                try:

                        #count number of events at expected array. 
                        for event in expected:
                            expectedAction = list(event.keys())[0]
                            if (expectedAction in eventsCountDict):
                                eventsCountDict[expectedAction][0] += 1
                            else:
                                ret = False 
                                writeToLog("INFO","found an unknown tag in expected results set : " + expectedAction)
                                writeToLog("INFO",json.dumps(event))
                                raise Exception("found an unknown tag in expected results set : " + expectedAction + " " + json.dumps(event)) 

                        #count number of events at actual array. 
                        for event in actual:
                            actualAction = list(event.keys())[0]
                            if (actualAction in eventsCountDict):
                                eventsCountDict[actualAction][1] += 1
                            else:
                                ret = False 
                                writeToLog("INFO","found an unknown tag in actual results set : " + actualAction)
                                writeToLog("INFO",json.dumps(event))
                                raise Exception("found an unknown tag in actual results set : " + actualAction + " " + json.dumps(event))
                        
                        #verify expected count of events
                        for event in eventsCountDict:
                            if (eventsCountDict[event][1] != eventsCountDict[event][0]):
                                writeToLog("INFO","Actual count " + str(eventsCountDict[event][1]) + " of event: " + event + " exceeds or less then the number of expected " + str(eventsCountDict[event][0]))
                                ##! ret = False
                        
                        # start comparing if size of actual and expected are the same
                        if (ret == True):
                            
                            expectedI = 0
                            actualI   = 0
                            adIsPlaying = False
                            
                            while (actualI < len(actual) and expectedI < len (expected)):
                                actualEvent    = list(actual[actualI].values())[0]
                                actualAction   = list(actual[actualI].keys())[0]
                                expectedEvent  = list(expected[expectedI].values())[0]
                                expectedAction = list(expected[expectedI].keys())[0]
                                if (expectedAction != actualAction):
                                    writeToLog("INFO","Expected : action at line " + str(expectedI) + " " + expectedAction + " . Actual: "  + actualAction + " at line " + str(actualI))                            
                                    skipEvents = ["adBufferUnderrun","ping","bufferUnderrun","pause","resume"]
                                    if (actualAction in skipEvents):
                                        writeToLog("DEBUG","Trying to skip event at actual set")
                                        actualI += 1
                                    elif (expectedAction in skipEvents):
                                        writeToLog("DEBUG","Trying to skip event at expected set")
                                        expectedI += 1
                                    else:
                                        actualI += 1
                                        expectedI += 1
                                        ret = False
                                    continue
                                if (len(actualEvent) != len(expectedEvent)):
                                    writeToLog("INFO","Expected : At line " + str(expectedI) + " Number of values at " + actualAction + " event doesn't match. " + str(len(expectedEvent)) + ". Actual: "  + str(len(actualEvent)) + " at line " + str(actualI))  
                                    self.writeToLogDifBetweenDictioanries(expectedEvent,actualEvent)
                                    ret = False
                                    expectedI += 1
                                    actualI   += 1
                                    continue
                                
                                #verify correct data of event start
                                
                                if (actualAction == "adStart"):
                                    adIsPlaying = True
                                elif (actualAction == "adStop"):
                                    adIsPlaying = False
                                elif (actualAction == "start"):
                                    
                                    entryIndex += 2
                                         
                                    code = actualEvent["code"]
                                    if (code.endswith("_" + str(entryIndex)) != True):
                                        writeToLog("INFO","Expected : at line " + str(expectedI) + " Code suffix is not as expected for event start, entry number " + str(entryIndex) + ". Actual code is " + code + " at line " + str(actualI))
                                        ret = False
                                    
                                    if ("properties" in expectedEvent and "properties" in actualEvent):
                                        try:
                                            expecetdStartProperties = json.loads(expectedEvent["properties"]) 
                                            expecetdKalturaInfo  = expecetdStartProperties["kalturaInfo"]
                                        except Exception as inst:
                                                ret = False
                                                writeToLog("INFO","youboraCompareAPIEvents() Fail to parse JSON " + json.dumps(expected[expectedI]))
                                                log_exception(inst)
                                                raise
                                        try:
                                            actualStartProperties  = json.loads(actualEvent["properties"])
                                            actualKalturaInfo = actualStartProperties["kalturaInfo"]
                                        except Exception as inst:
                                            writeToLog("INFO","youboraCompareAPIEvents() Fail to parse JSON " + actualEvent["properties"])
                                            log_exception(inst)
                                            raise
                                        if (len(actualKalturaInfo) != len(expecetdKalturaInfo)):
                                            writeToLog("INFO","Expected: Number of properties at start event (kaltura info) " + str(len(expecetdKalturaInfo)) + ". Actual: "  + str(len(actualKalturaInfo)))
                                            self.writeToLogDifBetweenDictioanries(expecetdKalturaInfo,actualKalturaInfo)
                                            ret = False
                                            expectedI += 1
                                            actualI   += 1
                                            continue                                    
                                        if (self.youboraCompareStartOrErrorEvent(expectedI,actualI,actualEvent,expectedEvent) != True):
                                            ret = False
                                        if (self.youboraCompareEntryDetails(expectedI,actualI,actualKalturaInfo,expecetdKalturaInfo) != True):
                                            ret = False                                                                    
                                    
                                #verify correct data of event ping
                                elif (actualAction == "ping"):
                                    for key in actualEvent:
                                        if (key == "pingTime"):
                                            pingTime = int (actualEvent[key]) 
                                            if (pingTime != 5):
                                                writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", first ping pingTime should be 5 and not " + self.getStringValue(actualEvent[key]) + " at line " + str(actualI)) 
                                                ret = False
                                        elif (key == "bitrate"):
                                            if (adIsPlaying == False):
                                                try:
                                                    bitrate = float(actualEvent[key])
                                                    if (entryType == enums.entryType.ENTRY_TYPE_AUDIO):
                                                        if (bitrate != -1):
                                                            writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", bitrate for the audio entry should be -1 and not " + self.getStringValue(actualEvent[key])  + " at line " + str(actualI))
                                                            ret = False
                                                    elif (bitrate <= 0):
                                                        writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", should be a number greater then 0 and not " + self.getStringValue(actualEvent[key])  + " at line " + str(actualI))
                                                        ret = False
                                                except TypeError as inst:
                                                    if (str(inst) != "float() argument must be a string or a number, not 'NoneType'" and entryType != enums.entryType.ENTRY_TYPE_AUDIO):
                                                        ret = False
                                                        raise
                                                except Exception as inst:
                                                    ret = False
                                                    raise
                                        elif (key == "time"):
                                            if (adIsPlaying == False):
                                                if (self.getStringValue(actualEvent[key]) == "0"):
                                                    writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", ping time should not be 0"  + " at line " + str(actualI))
                                                    ret = False
                                        elif (key == "diffTime"):
                                                if (self.getIntValue(actualEvent[key]) > 6000):
                                                    writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", difTime in ping should be less then 5000 and not " + self.getStringValue(actualEvent[key])  + " at line " + str(actualI)) 
                                                    ret = False

                                #verify correct data of event stop                
                                elif (actualAction == "stop"):
                                    for key in actualEvent:
                                        if (key == "diffTime"):
                                            if (self.getIntValue(actualEvent[key]) > 5000):
                                                writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", difTime in ping should be less then 5000 and not " + self.getStringValue(actualEvent[key])  + " at line " + str(actualI)) 
                                                ret = False
                                        
                                #verify correct data of event bufferUnderrun
                                elif (actualAction == "bufferUnderrun"):
                                    pass
                                
                                #verify correct data of event resume
                                elif (actualAction == "resume"):
                                    pass
                            
                                #verify correct data of event error
                                elif (actualAction == "error"):
                                    if (len(expected) == 2 ):
                                        entryIndex = -1  
                                    code = actualEvent["code"]
                                    if (code.endswith("_" + str(entryIndex)) != True):
                                        writeToLog("INFO","Expected : at line " + str(expectedI) + " Code suffix is not as expected for event start, entry number " + str(entryIndex) + ". Actual code is " + code  + " at line " + str(actualI))
                                        ret = False
                                    try:
                                        expectedErrorProperties = json.loads(expected[expectedI]["error"]["properties"])
                                        expectedErrorKalturaInfo = expectedErrorProperties["kalturaInfo"]
                                    except Exception as inst:
                                            ret = False
                                            writeToLog("INFO","youboraCompareAPIEvents() Fail to parse JSON " + json.dumps(expectedEvent["properties"]))
                                            log_exception(inst)
                                            raise
                                    try:
                                        actualErrorProperties  = json.loads(actualEvent["properties"])
                                        actualErrorKalturaInfo = actualErrorProperties["kalturaInfo"]
                                    except Exception as inst:
                                        writeToLog("INFO","youboraCompareAPIEvents() Fail to parse JSON " + actualEvent["properties"])
                                        log_exception(inst)
                                        raise
                                    if (len(expectedErrorKalturaInfo) != len(actualErrorKalturaInfo)):
                                            writeToLog("INFO","Expected : Number of properties at error event " + str(len(expectedErrorKalturaInfo)) + ". Actual: "  + str(len(actualErrorKalturaInfo)))  
                                            self.writeToLogDifBetweenDictioanries(expectedErrorKalturaInfo,actualErrorKalturaInfo)
                                            ret = False
                                            expectedI += 1
                                            actualI   += 1
                                            continue
                                    if (self.youboraCompareStartOrErrorEvent(expectedI,actualI,actualEvent,expectedEvent) != True):
                                        ret = False
                                    if (self.youboraCompareEntryDetails(expectedI,actualI,actualErrorKalturaInfo,expectedErrorKalturaInfo) != True):
                                        ret = False                                                                    
                                    expectedI += 1
                                    actualI   += 1
                                    continue 
                                        
                                #verify correct data of event joinTime
                                elif (actualAction == "joinTime"):  
                                    for key in actualEvent:   
                                        if (key == "eventTime"):
                                            if (self.getIntValue(actualEvent[key]) > 5):
                                                writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", eventTime should be less then 5 and not " + self.getStringValue(actualEvent[key]) + " at line " + str(actualI))
                                                ret = False
                                        elif (key == "time"):
                                            if (self.getIntValue(actualEvent[key]) > 5000):
                                                writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + ", time should be less then 60 and not " + self.getStringValue(actualEvent[key]) + " at line " + str(actualI)) 
                                                ret = False
                                elif (actualAction == "data"): 
                                    for key in actualEvent:   
                                        if (actualEvent[key] != expectedEvent[key]):
                                            writeToLog("INFO","Expected : at line " + str(expectedI) + " " + key + " " + expectedEvent[key] + ". Actual " + actualEvent[key] + " at line " + str(actualI))
                                    expectedI += 1
                                    actualI   += 1
                                    continue
                                            
                                if (actualEvent["code"] != code): 
                                    ret = False   
                                    writeToLog("INFO","Expected : at line " + str (expectedI) + " Code " + actualEvent["code"] + " is not consistent during playback of an entry in event. Expected code: " + code + " for entry number " + str(entryIndex) + " at line " + str(actualI))
                                
                                expectedI += 1
                                actualI   += 1
                            if (actualI < len(actual) or expectedI < len (expected)): 
                                ret = False
                                writeToLog("INFO","Actual and expected don't have the same size. Expected: " + str(len(expected)) + " Actual: " + str(len(actual)))
                                
                except Exception as inst:
                    log_exception(inst)
                    writeToLog("INFO","Expected events summary:")
                    for i in range (0,len(expected)):
                        writeToLog("INFO","Expected event " + str (i) + " : " + json.dumps(expected[i]))
                    writeToLog("INFO","Actual events summary:")
                    for i in range (0,len(actual)):
                        writeToLog("INFO","Actual event " + str (i) + " : " + json.dumps(actual[i]))
                    raise
                        
                if (ret == False):
                    writeToLog("INFO","Expected events summary:")
                    for i in range (0,len(expected)):
                        writeToLog("INFO","Expected event " + str (i) + " : " + json.dumps(expected[i]))
                    writeToLog("INFO","Actual events summary:")
                    for i in range (0,len(actual)):
                        writeToLog("INFO","Actual event " + str (i) + " : " + json.dumps(actual[i]))
                        
                
                return ret
        
        def youboraCompareAPIEvents(self,test,expectedAnalyticsEventsDict,actualAnalyticsEventsDict,entryType,adType = None):
                
                actual = []
                
                for event in actualAnalyticsEventsDict:
                    e = json.loads(event[9:])
                    actual.append(e)
                
                writeToLog("INFO","verify Analytics events")
                
                if(len(expectedAnalyticsEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                    expected = expectedAnalyticsEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                else:
                    expected = expectedAnalyticsEventsDict["shared"]
                
                
                ret = self.youboraCompareEvents(test,expected,actual,entryType,adType)
                
                return ret                
                
        def youboraCompareHTTPEvents(self,test,expectedHttpEventsDict, actualEventsCapture,entryType,adType = None):
                
                writeToLog("INFO","verify Analytics HTTP events")    
                
                ignoreParams       = ["bufferDuration"]
                filterURLList      = ["nqs.nice264.com","debug-nqs-lw2.nice264.com","nqs-nl2.youboranqs01.com","nqs-nl1-c10.youboranqs01.com","nqs-wdc3.youboranqs01.com"]
                
                actualEventsCapture.saveHar(test.myProxy.har)
                actualEvents = actualEventsCapture.createHttpAnalyticsDict(test.myProxy.har,ignoreParams,filterURLList,"youbora")
                
                if(len(expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                    expected = expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                else:
                    expected = expectedHttpEventsDict["shared"]
                
                ret = self.youboraCompareEvents(test,expected,actualEvents,entryType,adType)
                
                return ret
            
        def comscoreCompareEvents(self,test,expectedHttpEventsDict, actualEvents):
                
                ret = True               
                tagsCountDict = { 
                                   "c1"  : [0,0],
                                   "c2"  : [0,0],
                                   "c3"  : [0,0],
                                   "c4"  : [0,0],
                                   "c5"  : [0,0],
                                   "c6"  : [0,0],
                                   "c7"  : [0,0],
                                   "c8"  : [0,0],
                                   "c9"  : [0,0],
                                   "c10"  : [0,0]
                                   }
                
                if(len(expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER])):
                    expectedEvents = expectedHttpEventsDict[localSettings.LOCAL_RUNNING_BROWSER]
                else:
                    expectedEvents = expectedHttpEventsDict["shared"]
                
                for i in range (0,len(expectedEvents)):
                    for tag in expectedEvents[i]:
                        if (tag in tagsCountDict):
                            tagsCountDict[tag][0] = tagsCountDict[tag][0] + 1 
                        else: 
                                writeToLog("INFO","found an unknown tag in expected results set : " + tag + " at event " + str (i)) 
                                raise Exception("found an unknown tag in actual results set : " + tag + " at event " + str (i))
                for i in range (0,len(actualEvents)):
                    for tag in actualEvents[i]:
                        if (tag in tagsCountDict):
                            tagsCountDict[tag][1] = tagsCountDict[tag][1] + 1
                        else:
                            writeToLog("INFO","found an unknown tag in actual results set : " + tag)
                            raise Exception("found an unknown tag in actual results set : " + tag + " " + json.dumps(OrderedDict(sorted(actualEvents[i].items()))))
                ret = self.compareLengthOfActualVsExpectedDict(actualEvents,expectedEvents)
                if (ret == True):
                        retEvent = True
                        for i in range (0,len(expectedEvents)):
                                if (len(expectedEvents[i]) == len(actualEvents[i])):
                                    for cValue in actualEvents[i]:
                                        if (actualEvents[i][cValue] != expectedEvents[i][cValue]):
                                            writeToLog("INFO","Expected : " + str(i) + " " + cValue + " " + str(expectedEvents[i][cValue]))
                                            writeToLog("INFO","Actual   : " + str(i) + " " + cValue + " " + str(actualEvents[i][cValue]))
                                            retEvent = False
                                            ret = False
                                else: 
                                    writeToLog("INFO","Number of C tags doesn't match")
                                    retEvent = False
                                    ret = False
                                if (retEvent == False):
                                    writeToLog("INFO","Expected : " + str(i) + " " + json.dumps(OrderedDict(sorted(expectedEvents[i].items()))))
                                    writeToLog("INFO","Actual   : " + str(i) + " " + json.dumps(OrderedDict(sorted(actualEvents[i].items()))))
                                    retEvent = True

                if (ret == False):
                    expectedVSActual = ""
                    newLine = ""
                    for tag in tagsCountDict:
                        if (tagsCountDict[tag][0] != tagsCountDict[tag][1]):
                            if (expectedVSActual != ""):
                                newLine = "\n"    
                            expectedVSActual = expectedVSActual + newLine + " expected " + tag + " count: " + str(tagsCountDict[tag][0]) + ", " + "actual: " + str(tagsCountDict[tag][1])
                    if (expectedVSActual != ""):
                                writeToLog("INFO","Events count:\n" + expectedVSActual)
                
                return ret
                
        def comscoreCompareHTTPEvents(self,test,expectedHttpEventsDict, actualEventsCapture):
                
                writeToLog("INFO","verify Analytics HTTP events")    
                
                ret = True               
                
                ignoreParams = ['rn','cv']
                #requiredParams = ['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10']
                filterURL      = ['b.scorecardresearch.com/p']
                
                actualEventsCapture.saveHar(test.myProxy.har)
                actualEvents = actualEventsCapture.createHttpAnalyticsDict(test.myProxy.har,ignoreParams,filterURL)          
                
                ret = self.comscoreCompareEvents (test,expectedHttpEventsDict, actualEvents)
                
                return ret    
        
        #compare the expected and actual API events for comscore analytics tests. driverFix is the browser the test ran on.
        def comscoreCompareAPIEvents(self,test,expectedAnalyticsEventsDict,actualEvents):
            
                ret    = True
                actual = []
                
                writeToLog("INFO","verify Analytics events")
                
                for event in actualEvents:
                    e = json.loads(event[9:])
                    actual.append(e)
                    
                ret = self.comscoreCompareEvents (test,expectedAnalyticsEventsDict, actual)
                                
                return ret
            
        def getStringValue(self, value):
            
            if (isinstance( value, int ) == True or isinstance(value, float) or isinstance(value, bool)):
                return str (value)
            else:
                return value
            
        def getIntValue(self, value):
            
            if (isinstance( value, str ) == True):
                return int(float(value))
            elif (isinstance(value, float)):
                return int (value)
            else:
                return value
            
        def getFloatValue(self, value):
            
            if (isinstance( value, str ) == True or isinstance(value, int)):
                return float (value)
            else:
                return value
            
        def writeToLogDifBetweenDictioanries(self,expected,actual): 
            
            for tag in expected.keys() - actual.keys():
                writeToLog("INFO","Missing tag from actual set : " + tag)
            for tag in actual.keys() - expected.keys():
                writeToLog("INFO","Missing tag from expected set : " + tag)
                
            