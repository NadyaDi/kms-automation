from base64 import b64encode
import base64
from collections import OrderedDict
import json, csv, sys, os
from re import split
import re, requests

from localSettings import *
from logger import *
from utilityTestFunc import *


#=============================================================================================================
#the class contains functions that manage practitest integration with automation framework 
#=============================================================================================================
class clsPractiTest:

    #=============================================================================================================
    # Function that returns all instances of a specific session 
    #=============================================================================================================    
    def getPractiTestSessionInstances(self, prSessionInfo):
        prSessionID = prSessionInfo["sessionSystemID"]
        defaultPlatform = prSessionInfo["setPlatform"]
        runOnlyFailed = prSessionInfo["runOnlyFailed"].lower()
        
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/instances.json?set-ids=" + str(prSessionID) + "&developer_email=" + LOCAL_SETTINGS_DEVELOPER_EMAIL + "&api_token=" + LOCAL_SETTINGS_PRACTITEST_API_TOKEN
        sessionInstancesDct = {}
        headers = { 
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if (len(dctSets["data"]) > 0):
                for testInstance in dctSets["data"]:
                    # '---f-34162' = 'Execute Automated'
                    # testInstance['attributes']['custom-fields']['---f-30772'] - Platform(CH, FF..)
                    # Check if test has specified platform, if not, use default platform
                    try:
                        platform = testInstance['attributes']['custom-fields']['---f-30772']  
                    except Exception:
                        platform = defaultPlatform
                        
                    try:
                        executeAutomated = testInstance['attributes']['custom-fields']['---f-34162']  
                    except Exception:
                        executeAutomated = 'No'                        
                    
                    # Run only FAILED tests:
                    toRun = True
                    if runOnlyFailed == 'yes':
                        if not testInstance['attributes']['run-status'].lower() == 'failed':
                            toRun = False
                            
                    if executeAutomated == 'Yes' and toRun == True:
                        sessionInstancesDct[testInstance["attributes"]["test-display-id"]] = testInstance["id"] + ";" + platform
                        writeToLog("DEBUG","Found test with id: " + str(testInstance["attributes"]["test-display-id"]))                                   
            else:
                writeToLog("DEBUG","No instances in set. " + r.text)        
        else:
            writeToLog("DEBUG","Bad response for get sessions. " + r.text) 
        
        return sessionInstancesDct
    
    
    #=============================================================================================================
    # Function that returns all sessions that are located under the filter "pending for automation"  
    #=============================================================================================================
    def getPractiTestAutomationSession(self):
        #FOR DEBUG, DON'T REMOVE
        # PractiTest filter ID:
        # qaKmsFrontEnd = 326139
        filterId = os.getenv('PRACTITEST_FILTER_ID',"")
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/sets.json?" + "api_token=" + str(LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + "&developer_email=" + str(LOCAL_SETTINGS_DEVELOPER_EMAIL) + "&filter-id=" + str(filterId)
        
        prSessionInfo = {
            "sessionSystemID"       : -1,
            "sessionDisplayID"      : -1,
            "setPlatform"           : "",
            "environment"           : "",
            "hostname"              : "",
            "runOnlyFailed"         : ""
        }

        headers = {
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if len(dctSets["data"]) != 0:
                if (dctSets["data"][0]["attributes"]["instances-count"] > 0):
                    prSessionInfo["sessionSystemID"]  = dctSets["data"][0]["id"]
                    prSessionInfo["sessionDisplayID"] = dctSets["data"][0]["attributes"]["display-id"]
                    prSessionInfo["setPlatform"]      = dctSets["data"][0]["attributes"]["custom-fields"]['---f-30772'] #PractiTest Field: Automation Platform
                    prSessionInfo["environment"]      = dctSets["data"][0]["attributes"]["custom-fields"]['---f-30761'] #PractiTest Field: Automation Env
                    prSessionInfo["hostname"]         = dctSets["data"][0]["attributes"]["custom-fields"]['---f-34785'] #PractiTest Field: Run On Hostname
                    prSessionInfo["runOnlyFailed"]    = dctSets["data"][0]["attributes"]["custom-fields"]['---f-38033'] #PractiTest Field: Automation Run Only FAILED
                    
                    writeToLog("DEBUG","Automation set found: " + str(prSessionInfo["sessionDisplayID"]) + " on platform: " + prSessionInfo["setPlatform"])
                else:
                    writeToLog("DEBUG","No automated sessions found.")
        else:
            writeToLog("DEBUG","Bad response for get sessions. " + r.text) 
        
        return prSessionInfo
    
    
    #=============================================================================================================
    # Function that retrievs the test Instance of a specific test in the csv file that contains the test list
    #=============================================================================================================
    def getTestInstanceFromTestSetFile(self, testID):
        instance = ""
        
        case_str = "test_" + testID
        testSetFilePath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testSetAuto.csv'))
        with open(testSetFilePath, 'r') as csv_mat: #windows
                platform_matrix = csv.DictReader(csv_mat)
                for row in platform_matrix:
                    if (row['case'] == case_str):
                        instance = row['instanceID']
                        break    
        return instance    
    
    
    #=============================================================================================================
    # Function that update the test results of a specific test run in practitest
    #============================================================================================================= 
    def setPractitestInstanceTestResults(self,testStatus,testID):
        runningTestNum    = os.getenv('RUNNING_TEST_ID',"")
        TEST_LOG_FILE_FOLDER_PATH = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'logs',str(runningTestNum)))
        
        practiTestUpdateTestInstanceResultsURL = "https://api.practitest.com/api/v2/projects/" + str(LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/runs.json"
       
        if (testStatus == "Pass"):
            exit_code = "0"
        else:
            exit_code = "1"
        
        # upload test results with a file attachment
        fileList = self.getFilesInTestLogFolder(TEST_LOG_FILE_FOLDER_PATH)  
        instance = self.getTestInstanceFromTestSetFile(testID)  
        data_json = json.dumps({'data':{'type': 'instances','attributes': {'instance-id': instance, 'exit-code': exit_code}, "files": {"data": fileList}  }  })          

        r = requests.post(practiTestUpdateTestInstanceResultsURL,
            data=data_json,
            auth=(LOCAL_SETTINGS_DEVELOPER_EMAIL, str(LOCAL_SETTINGS_PRACTITEST_API_TOKEN)),
            headers={'Content-type': 'application/json', 'Connection':'close'})    

        if (r.status_code == 200):
            writeToLog("DEBUG","Updated test: " + testID + " as: " + testStatus) 
            return True
        else:
            writeToLog("DEBUG","Bad response for update instances. " + r.text)
            return False 
        
    
    #=============================================================================================================
    # Function that that creates the csv that contains the automation tests to be run
    #=============================================================================================================
    def createAutomationTestSetFile(self, hostname, environment, platform, testIDsDict):
        platformList = ["pc_firefox","pc_chrome","pc_internet explorer","android_chrome"]
        testSetFile  = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testSetAuto.csv'))
        automationTestSetFileHeader = "hostname,environment,case"
        for plat in platformList:
            automationTestSetFileHeader = automationTestSetFileHeader + "," + plat
        automationTestSetFileHeader = automationTestSetFileHeader + ",instanceID\n"
        file = open(testSetFile, "w")
        file.write (automationTestSetFileHeader)
        for testID in testIDsDict:
            sTestID = str(testID)
            sTestPlatform = str(testIDsDict[testID]).split(";")[1]
            if sTestPlatform != '':
                platform = sTestPlatform            
            testPlatformLine = hostname + "," + environment + ",test_" + sTestID
            for plat in platformList:
                if plat == platform:
                    testPlatformLine = testPlatformLine + ",1"
                    writeToLog("DEBUG","Adding: " + "test_" + sTestID + " for platform: " + plat)
                else:           
                    testPlatformLine = testPlatformLine + ",0"
            testPlatformLine = testPlatformLine + "," + str(testIDsDict[testID]).split(";")[0]
            file.write (testPlatformLine + "\n")
        file.close()
       
        
    #=============================================================================================================
    # Function that that set the test set from status pending to status processed in practitest
    #=============================================================================================================
    def setTestSetAutomationStatusAsProcessed (self, prSessionID):
        practiTestSetAutomationStatusAsProcessedUrl = "https://api.practitest.com/api/v2/projects/" + str(LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/sets/" + str(prSessionID) + ".json?" + "api_token=" + str(LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + "&developer_email=" + str(LOCAL_SETTINGS_DEVELOPER_EMAIL)
        
        headers = { 
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        data = {"data": { "type": "sets", "attributes": {"version": "1.5", "custom-fields": { "---f-30327": "Processed"}}  } }
       
        
        r = requests.put(practiTestSetAutomationStatusAsProcessedUrl,headers = headers, data = json.dumps(data))
        if (r.status_code == 200):
                writeToLog("DEBUG","Session: " + str(prSessionID) + " updated as processed")
                return True
        else:
            writeToLog("DEBUG","Bad response for get sessions. " + r.text)
            return False       
    
    
    #=============================================================================================================
    # Function that gets all the file names in a given folder
    #=============================================================================================================
    def getFilesInTestLogFolder(self,path):
        # Check on which platform we run
        if 'win' in sys.platform:
            delimiter = "\\"
        else:
            delimiter = "/" 
        files = []
        fileList =  os.listdir(path)
        for file in fileList:
            with open(os.path.abspath(os.path.join(path,file)), "rb") as fileObj:
                fileBase64Utf8 = base64.b64encode(fileObj.read()).decode('utf-8') 
                files.append({"filename": self.getDateAndTime() + '__' + fileObj.name.split(delimiter)[len(fileObj.name.split(delimiter)) - 1], "content_encoded": fileBase64Utf8})
        return files
    
    
    #=============================================================================================================
    # Return current date and time using strftime, for example: 21-02-2018_16:34
    #=============================================================================================================
    def getDateAndTime(self):
        now = datetime.datetime.now()
        return now.strftime("%d-%m-%Y_%H:%M")
        