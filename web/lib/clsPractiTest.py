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
    def getPractiTestSessionInstances(self,prSessionID):
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/instances.json?set-ids=" + str(prSessionID) + "&developer_email=" + LOCAL_SETTINGS_DEVELOPER_EMAIL + "&api_token=" + LOCAL_SETTINGS_PRACTITEST_API_TOKEN
        sessionInstancesDct = {}
        headers = { 
            'Content-Type': 'application/json'
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if (len(dctSets["data"]) > 0):
                for testInstance in dctSets["data"]:
                    sessionInstancesDct[testInstance["attributes"]["test-display-id"]] = testInstance["id"]
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
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/sets.json?" + "api_token=" + str(LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + "&developer_email=" + str(LOCAL_SETTINGS_DEVELOPER_EMAIL) + "&filter-id=" + str(LOCAL_SETTINGS_PRACTITEST_AUTOMATED_SESSION_FILTER_ID)
        
        prSessionInfo = {
            "sessionSystemID"   : -1,
            "sessionDisplayID"  : -1,
            "setPlatform"       : "",
            "environment"       : ""
        }

        headers = {
            'Content-Type': 'application/json',
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if (dctSets["data"][0]["attributes"]["instances-count"] > 0):
                prSessionInfo["sessionSystemID"]  = dctSets["data"][0]["id"]
                prSessionInfo["sessionDisplayID"] = dctSets["data"][0]["attributes"]["display-id"]
                prSessionInfo["setPlatform"]      = dctSets["data"][0]["attributes"]["custom-fields"]['---f-30772'] #PractiTest Field: Automation Platform
                prSessionInfo["environment"]      = dctSets["data"][0]["attributes"]["custom-fields"]['---f-30761'] #PractiTest Field: Automation Env
                
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
#         LOG_FOLDER_PREFIX = ""
#         if (os.getenv('BUILD_ID',"") != ""):
#             LOG_FOLDER_PREFIX = '/' + os.getenv('BUILD_ID',"") + '/'
#         TEST_LOG_FILE_FOLDER_PATH = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'logs' + LOG_FOLDER_PREFIX + "/" + str(runningTestNum)))
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
            headers={'Content-type': 'application/json'})        

        if (r.status_code == 200):
            writeToLog("DEBUG","Updated test: " + testID + " as: " + testStatus) 
            return True
        else:
            writeToLog("DEBUG","Bad response for update instances. " + r.text)
            return False 
        
    
    #=============================================================================================================
    # Function that that creates the csv that contains the automation tests to be run
    #=============================================================================================================
    def createAutomationTestSetFile(self, environment, platform, testIDsDict):
        platformList = ["pc_firefox","pc_chrome","pc_internet explorer","android_chrome"]
        testSetFile  = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','testSetAuto.csv'))
        automationTestSetFileHeader = "environment,case"
        for plat in platformList:
            automationTestSetFileHeader = automationTestSetFileHeader + "," + plat
        automationTestSetFileHeader = automationTestSetFileHeader + ",instanceID\n"
        file = open(testSetFile, "w")
        file.write (automationTestSetFileHeader)
        for testID in testIDsDict:
            sTestID = str(testID)
            testPlatformLine = environment + ",test_" + sTestID
            for plat in platformList:
                if plat == platform:
                    testPlatformLine = testPlatformLine + ",1"
                    writeToLog("DEBUG","Adding: " + "test_" + sTestID.rjust(4,"0") + " for platform: " + plat)
                else:           
                    testPlatformLine = testPlatformLine + ",0"
            testPlatformLine = testPlatformLine + "," + testIDsDict[testID]
            file.write (testPlatformLine + "\n")
        file.close()
       
        
    #=============================================================================================================
    # Function that that set the test set from status pending to status processed in practitest
    #=============================================================================================================
    def setTestSetAutomationStatusAsProcessed (self, prSessionID):
        practiTestSetAutomationStatusAsProcessedUrl = "https://api.practitest.com/api/v2/projects/" + str(LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/sets/" + str(prSessionID) + ".json?" + "api_token=" + str(LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + "&developer_email=" + str(LOCAL_SETTINGS_DEVELOPER_EMAIL)
        
        headers = { 
            'Content-Type': 'application/json',
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
        files = []
        fileList =  os.listdir(path)
        for file in fileList:
            with open(os.path.abspath(os.path.join(path,file)), "rb") as fileObj:
                fileBase64Utf8 = base64.b64encode(fileObj.read()).decode('utf-8') 
                files.append({"filename": fileObj.name.split("\\")[len(fileObj.name.split("\\")) - 1], "content_encoded": fileBase64Utf8})
        return files
