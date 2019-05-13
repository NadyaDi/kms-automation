from base64 import b64encode
import base64
from collections import OrderedDict
import json, csv, sys, os
from re import split
import re, requests
from enum import Enum
from localSettings import *
from logger import *
from utilityTestFunc import *
import itertools


#=============================================================================================================
# The class contains functions that manage PraciTest integration with automation framework 
#=============================================================================================================
class clsPractiTest:
    # Update the PractiTest variables by the Project name
    def __init__(self): 
        self.setPractitestVariables() 
            
    # ENUMS
    class TEST_STATUS(Enum):
        def __str__(self):
            return str(self.value)
    
        PASSED          = 'PASSED'
        FAILED          = 'FAILED'       
        BLOCKED         = 'BLOCKED'
        NO_RUN          = 'NO RUN'
        N_A             = 'N/A'
    
    
    class AUTOMATION_STATUS(Enum):
        def __str__(self):
            return str(self.value)
    
        PROCESSED       = 'PROCESSED'
        PENDING         = 'PENDING'       


    #=============================================================================================================
    # Update the PractiTest variables by the Project name 
    #=============================================================================================================   
    def setPractitestVariables(self):
        application = localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST
        
        if application == enums.Application.MEDIA_SPACE:
            localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID                          = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_PROJECT_ID
            localSettings.LOCAL_SETTINGS_PRACTITEST_NIGHT_RUN_FILTER_ID                 = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_NIGHT_RUN_FILTER_ID
            localSettings.LOCAL_SETTINGS_PRACTITEST_ONLY_EXECUTE_AT_NIGHT               = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_ONLY_EXECUTE_AT_NIGHT
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_PLATFORM_FIELD           = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_AUTOMATION_PLATFORM_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_ENV_FIELD                = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_AUTOMATION_ENV_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_RUN_ON_HOSTNAME_FIELD    = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_AUTOMATION_RUN_ON_HOSTNAME_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_RUN_ONLY_FAILED_FIELD    = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_AUTOMATION_RUN_ONLY_FAILED_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_EXECUTE_AUTOMATED                   = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_EXECUTE_AUTOMATED
            localSettings.LOCAL_SETTINGS_PRACTITEST_EXECUTE_AT_NIGHT                    = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_EXECUTE_AT_NIGHT
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_STATUS                   = localSettings.LOCAL_SETTINGS_PRACTITEST_KMS_AUTOMATION_STATUS
        elif application == enums.Application.PITCH:
            localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID                          = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_PROJECT_ID
            localSettings.LOCAL_SETTINGS_PRACTITEST_NIGHT_RUN_FILTER_ID                 = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_NIGHT_RUN_FILTER_ID
            localSettings.LOCAL_SETTINGS_PRACTITEST_ONLY_EXECUTE_AT_NIGHT               = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_ONLY_EXECUTE_AT_NIGHT
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_PLATFORM_FIELD           = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_AUTOMATION_PLATFORM_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_ENV_FIELD                = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_AUTOMATION_ENV_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_RUN_ON_HOSTNAME_FIELD    = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_AUTOMATION_RUN_ON_HOSTNAME_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_RUN_ONLY_FAILED_FIELD    = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_AUTOMATION_RUN_ONLY_FAILED_FIELD
            localSettings.LOCAL_SETTINGS_PRACTITEST_EXECUTE_AUTOMATED                   = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_EXECUTE_AUTOMATED
            localSettings.LOCAL_SETTINGS_PRACTITEST_EXECUTE_AT_NIGHT                    = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_EXECUTE_AT_NIGHT
            localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_STATUS                   = localSettings.LOCAL_SETTINGS_PRACTITEST_PITCH_AUTOMATION_STATUS
    #=============================================================================================================
    # Function that returns all instances of a specific session 
    #=============================================================================================================    
    def getPractiTestSessionInstances(self, prSessionInfo):
        prSessionID = prSessionInfo["sessionSystemID"]
        defaultPlatform = prSessionInfo["setPlatform"]
        runOnlyFailed = prSessionInfo["runOnlyFailed"].lower()
        sessionInstancesDct = {}
        page = 1
         
        while True:
            headers = { 
                'Content-Type': 'application/json',
                'Connection':'close'
            }
                         
            practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + \
                                        "/instances.json?set-ids=" + str(prSessionID) + \
                                        "&developer_email=" + localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL + \
                                        "&page[number]=" + str(page) + \
                                        "&api_token=" + localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN
            # For next iteration
            page = page + 1
             
            r = requests.get(practiTestGetSessionsURL,headers = headers)
            if (r.status_code == 200):
                dctSets = json.loads(r.text)
                if (len(dctSets["data"]) > 0):
                    for testInstance in dctSets["data"]:
                        # '---f-34162' = 'Execute Automated'
                        # testInstance['attributes']['custom-fields']['---f-30772'] - Platform(CH, FF..)
                        # Check if test has specified platform, if not, use default platform
                        try:
                            platform = testInstance['attributes']['custom-fields'][localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_PLATFORM_FIELD]  
                        except Exception:
                            platform = defaultPlatform
                             
                        try:
                            executeAutomated = testInstance['attributes']['custom-fields'][localSettings.LOCAL_SETTINGS_PRACTITEST_EXECUTE_AUTOMATED]  
                        except Exception:
                            executeAutomated = 'No'                        
                         
                        # Run only FAILED tests:
                        toRun = True
                        if runOnlyFailed == 'yes':
                            if not testInstance['attributes']['run-status'].lower() == 'failed':
                                toRun = False
                        
                        # Run only 'No Run' test
                        else:
                            if not testInstance['attributes']['run-status'].lower() == 'no run':
                                toRun = False                             
                                 
                        if executeAutomated == 'Yes' and toRun == True:
                            sessionInstancesDct[testInstance["attributes"]["test-display-id"]] = testInstance["id"] + ";" + platform
                            writeToLog("INFO","Found test with id: " + str(testInstance["attributes"]["test-display-id"]))                                   
                else:
                    writeToLog("INFO","No instances in set. " + r.text)
                    break    
            else:
                writeToLog("INFO","Bad response for get sessions. " + r.text) 
                break
        return sessionInstancesDct    
    
    
    #=====================================================================================================================
    # Function that returns all sessions that are located under the filter "pending for automation" in Media Space Project 
    #=====================================================================================================================
    def getPractiTestAutomationSession(self):
        #FOR DEBUG, DON'T REMOVE
        # PractiTest filter ID:
        # qaKmsFrontEnd = 442156
        filterId = os.getenv('PRACTITEST_FILTER_ID',"")
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/sets.json?" + \
                                    "api_token=" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + \
                                    "&developer_email=" + str(localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL) + \
                                    "&filter-id=" + str(filterId)
        
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
                    prSessionInfo["setPlatform"]      = dctSets["data"][0]["attributes"]["custom-fields"][localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_PLATFORM_FIELD] #PractiTest Field: Automation Platform
                    prSessionInfo["environment"]      = dctSets["data"][0]["attributes"]["custom-fields"][localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_ENV_FIELD] #PractiTest Field: Automation Env
                    prSessionInfo["hostname"]         = dctSets["data"][0]["attributes"]["custom-fields"][localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_RUN_ON_HOSTNAME_FIELD] #PractiTest Field: Run On Hostname
                    prSessionInfo["runOnlyFailed"]    = dctSets["data"][0]["attributes"]["custom-fields"][localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_RUN_ONLY_FAILED_FIELD] #PractiTest Field: Automation Run Only FAILED
                    
                    writeToLog("INFO","Automation set found: " + str(prSessionInfo["sessionDisplayID"]) + " on platform: " + prSessionInfo["setPlatform"])
                else:
                    writeToLog("INFO","No automated sessions found.")
        else:
            writeToLog("INFO","Bad response for get sessions. " + r.text) 
        
        return prSessionInfo
    
    
    #=============================================================================================================
    # Function that returns specific test set by ID 
    #=============================================================================================================
    def getPractiTestSetById(self, testSetId):
#         testSetId = '367544'
        page = '1'
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + \
                                    str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + \
                                    "/instances.json?set-ids=" + str(testSetId) + \
                                    "&developer_email=" + localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL + \
                                    "&page[number]=" + str(page) + \
                                    "&api_token=" + localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN

        headers = {
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if len(dctSets["data"]) != 0:
                writeToLog("INFO","Automation Test Set found, id: '" + str(testSetId)+ "'; Display ID: '" + str(dctSets["data"][0]["attributes"]["set-display-id"]) + "'")
                return dctSets["data"]
            else:
                writeToLog("INFO","No test found in Test Set: '" + str(testSetId) + "'")
        else:
            writeToLog("INFO","Bad response for get PractiTest Set By Id: " + r.text)
            
        return
    
    
    #=============================================================================================================
    # Function go over data (all tests in test set)
    # practiTestFieldId - example: "---f-38302"
    #=============================================================================================================    
    def syncTestSetData(self, testSet, csvPath, practiTestFieldId):
        listCsv = open(csvPath).readlines()
        testSetData = self.getPractiTestSetById(testSet['id'])
        for testPractitest in testSetData:
            testDisplayId = str(testPractitest["attributes"]["test-display-id"])
            for testCsv in listCsv:
                if testDisplayId == testCsv.split(',')[0]:
                    if str(testCsv.split(',')[1]) != '\n':
                        #Update the test: instanceId, customFieldId, customFieldValue
                        self.updateInstanceCustomField(str(testPractitest['id']), practiTestFieldId, str(testCsv.split(',')[1]).replace('\n',''))
                        writeToLog("INFO", "Updated TestSet '" + str(testSet['id']) + "', Test ID '" + testDisplayId + "', Filed ID '" + practiTestFieldId + "', New Value: " + str(testCsv.split(',')[1]))
        return    
    
    #=============================================================================================================
    # Function that returns all tests sets that are located under the given filter 
    #=============================================================================================================
    def getPractiTestTestSetByFilterId(self, filterId, onlyExecuteAtNight=False):
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/sets.json?" + \
                                    "api_token=" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + \
                                    "&developer_email=" + str(localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL) + \
                                    "&filter-id=" + str(filterId)
        
        listTestSet = []    

        headers = {
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if len(dctSets["data"]) != 0:
                for testSet in dctSets["data"]:
                    # Execute test when "Execute at Night", PractiTest TestSet field, is set to True
                    if onlyExecuteAtNight == True:
                        try:
                            #'---f-41840' = "Execute at Night"
                            if testSet['attributes']['custom-fields'][localSettings.LOCAL_SETTINGS_PRACTITEST_EXECUTE_AT_NIGHT] == 'yes':
                                listTestSet.append(testSet)
                                writeToLog("INFO","TestSet name: " + str(testSet['attributes']['name']) + "; ID: " + str(testSet['attributes']['display-id']) + 
                                           " was added to list")
                        # When "Execute at Night" is False        
                        except:
                            writeToLog("INFO","TestSet name: " + str(testSet['attributes']['name']) + "; ID: " + str(testSet['attributes']['display-id']) +
                                       " was skipped")                            
                    # Execute regardless "Execute at Night" PractiTest TestSet field
                    else:
                        listTestSet.append(testSet)
                        writeToLog("INFO","TestSet name: " + str(testSet['attributes']['name']) + "; ID: " + str(testSet['attributes']['display-id']) + 
                                   " was added to list")                        
            else:
                writeToLog("INFO","No Test Sets found under filter id: '" + filterId + "'")
                return False
        else:
            writeToLog("INFO","Bad response for get Test Set: " + r.text)
            return False
        
        return listTestSet
    
    
    #=============================================================================================================
    # Function that retrieves the test Instance of a specific test in the csv file that contains the test list
    #=============================================================================================================
    def getTestInstanceFromTestSetFile(self, testID):
        instance = ""
        case_str = "test_" + testID
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MEDIA_SPACE:
            testSetFilePath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','kms','testSetAuto.csv'))
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.PITCH:
            testSetFilePath = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','pitch','testSetAuto.csv'))
        else:
            writeToLog("INFO","UNSUPPORTED APPLICATION NAME: '" + str(localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST) + "'")          
        
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
        
        practiTestUpdateTestInstanceResultsURL = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/runs.json"
       
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
            auth=(localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL, str(localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN)),
            headers={'Content-type': 'application/json', 'Connection':'close'})    

        if (r.status_code == 200):
            writeToLog("INFO","Updated test: " + testID + " as: " + testStatus) 
            return True
        else:
            writeToLog("INFO","Bad response for update instances. " + r.text)
            return False 
        
        
    #=============================================================================================================
    # Function that update the tests status of entire Testset in practitest
    # testSetList = list of testset instance id
    # testStatus  = self.practiTest.TEST_STATUS
    #============================================================================================================= 
    def setStatusToEntireTestset(self, testSetList, testStatus):
        practiTestUpdateTestInstanceResultsURL = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + "/runs.json"

        # For each Testset under cpecified filter
        for testSet in testSetList:
            # Get Testset Instance ID
            testSetInstanceId = testSet["id"]
            
            page = 1
            while True:
                headers = { 
                    'Content-Type': 'application/json',
                    'Connection':'close'
                }
                             
                practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + \
                                            "/instances.json?set-ids=" + str(testSetInstanceId) + \
                                            "&developer_email=" + localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL + \
                                            "&page[number]=" + str(page) + \
                                            "&api_token=" + localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN
                # For next iteration
                page = page + 1
                 
                r = requests.get(practiTestGetSessionsURL,headers = headers)
                if (r.status_code == 200):
                    dctSets = json.loads(r.text)
                    if (len(dctSets["data"]) > 0):
                        testInstancesList = []
                        
                        # Split tests to 20 items per list
                        for testInstance in dctSets["data"]:
                            testInstancesList.append(testInstance["id"])
                        dataChunks = self.createDataChank(testInstancesList, testStatus , 20)
                        
                        # Set status to each test in each chunk
                        for dataChunk in dataChunks:
                            # Convert data string to variable
                            data = eval(dataChunk)

                            # Send the post to PractiTest API
                            r = requests.post(practiTestUpdateTestInstanceResultsURL,
                                data=json.dumps(data),
                                auth=(localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL, str(localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN)),
                                headers={'Content-type': 'application/json', 'Connection':'close'})    
                      
                            if (r.status_code == 200):
                                writeToLog("INFO","Updated test instance: " + str(testInstance["id"]) + " as: " + str(testStatus)) 
                            else:
                                writeToLog("INFO","Bad response for update instances. " + r.text)
                                return False                            
                    else:
                        writeToLog("INFO","No instances in set. " + r.text)
                        break    
                else:
                    writeToLog("INFO","Bad response for get sessions. " + r.text) 
                    return False
        return True
    

    #=============================================================================================================
    # Function that update the testsets custom fields
    # testSetList = list of testset instance id
    # EXAMPLE: customFiledsDict =  OrderedDict({'---f-30327':'Processed', '---f-38033':'yes'})
    # (Automation Status = ---f-30327
    # Automation Run Only FAILED = ---f-30327)
    #============================================================================================================= 
    def updateTestsetsCustomFields(self, testSetList, customFiledsDict):
        # For each Testset under cpecified filter
        for testSet in testSetList:
            # Get Testset Instance ID
            instanceId = testSet["id"]
            
            if self.updateInstanceCustomFields(instanceId, customFiledsDict) == False:
                writeToLog("INFO","FAILED to update Testet custom filed") 
                return False            
        return True    
    
    
    #=============================================================================================================                
    # Return yield successive n-sized chunks from l. (return iterable of chunks lists) 
    #=============================================================================================================
    def chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
        
        
    #=============================================================================================================                
    # Creates generic data for updating multiple tests by sending one request
    #=============================================================================================================
    def createDataChank(self, instanceIdList, testStatus, maxCount):
        tampleteSuffix = ']}'
        listOfDataChunks = []
        # Divide the list to chunks (PractiTest API can manage maximum of 20 test in one request)
        iterableList = self.chunks(instanceIdList, maxCount)
        
        for maxInstanceList in iterableList:
            data = '{"data": ['
            for instanceId in maxInstanceList:
                data = data + '{ "type": "instances", "attributes":{"instance-id": ' + instanceId + '}, "steps": {"data": [{"name": "Set Test Status As: " + "' + str(testStatus) + '", "expected-results": "This step created automated", "status": "' + str(testStatus) + '"}]}}'
                # if not last, add ',' at the end
                if instanceId != maxInstanceList[-1]:
                    data = data + ','
            data = data + tampleteSuffix 
            listOfDataChunks.append(data)
            
        return listOfDataChunks
        
        
    #=============================================================================================================                
    # Creates generic data for updating multiple custom fileds in testset by sending one request
    #=============================================================================================================
    def createDataForTestsetMultipleCustomFileds(self, customFiledsDict):
        tampleteSuffix = '}}}}'
        data = '{"data": { "type": "sets", "attributes": {"custom-fields": {'
        
        for customField in customFiledsDict:
            data = data + '"' + str(customField) + '": "' + str(customFiledsDict[customField]) + '"'
            # if not last, add ',' at the end
            if customField != list(customFiledsDict.keys())[-1]:
                data = data + ','

        data = data + tampleteSuffix 
        return data       
    
     
    #=============================================================================================================
    # Function that that creates the csv that contains the automation tests to be run
    #=============================================================================================================
    def createAutomationTestSetFile(self, hostname, environment, platform, testIDsDict):
        platformList = ["pc_firefox","pc_chrome","pc_internet explorer","android_chrome"]
            
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MEDIA_SPACE:
            testSetFile  = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','kms','testSetAuto.csv'))
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.PITCH:
            testSetFile  = os.path.abspath(os.path.join(localSettings.LOCAL_SETTINGS_KMS_WEB_DIR,'ini','pitch','testSetAuto.csv'))
        else:
            writeToLog("INFO","UNSUPPORTED APPLICATION NAME: '" + str(localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST) + "'")            
            
        file = open(testSetFile, "w")
        automationTestSetFileHeader = "hostname,environment,case"
        for plat in platformList:
            automationTestSetFileHeader = automationTestSetFileHeader + "," + plat
        automationTestSetFileHeader = automationTestSetFileHeader + ",instanceID\n"
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
                    writeToLog("INFO","Adding: " + "test_" + sTestID + " for platform: " + plat)
                else:           
                    testPlatformLine = testPlatformLine + ",0"
            testPlatformLine = testPlatformLine + "," + str(testIDsDict[testID]).split(";")[0]
            file.write (testPlatformLine + "\n")
        file.close()
       
        
    #=============================================================================================================
    # Function that that set the test set from status pending to status processed in practitest
    #=============================================================================================================
    def setTestSetAutomationStatusAsProcessed (self, prSessionID):
        practiTestSetAutomationStatusAsProcessedUrl = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + \
                                                        "/sets/" + str(prSessionID) + ".json?" + \
                                                        "api_token=" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + \
                                                        "&developer_email=" + str(localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL)
        
        headers = { 
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        data = {"data": { "type": "sets", "attributes": {"custom-fields": { localSettings.LOCAL_SETTINGS_PRACTITEST_AUTOMATION_STATUS: "Processed"}}  } }
        
        r = requests.put(practiTestSetAutomationStatusAsProcessedUrl,headers = headers, data = json.dumps(data))
        if (r.status_code == 200):
                writeToLog("INFO","Session: " + str(prSessionID) + " updated as processed")
                return True
        else:
            writeToLog("INFO","Bad response for get sessions. " + r.text)
            return False   
        
        
    #=============================================================================================================
    # Function that sets the test custom field
    # customFiledId example: "---f-38302"
    #=============================================================================================================
    def updateInstanceCustomField(self, instanceId, customFieldId, customFieldValue):
        practiTestUpdateASpecificInstanceUrl = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + \
                                                "/instances/" + str(instanceId) + ".json?" + \
                                                "api_token=" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + \
                                                "&developer_email=" + str(localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL)
        
        headers = { 
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        data = {"data": { "type": "instances", "attributes": {"custom-fields": { customFieldId: str(customFieldValue)}}}}
        
        r = requests.put(practiTestUpdateASpecificInstanceUrl,headers = headers, data = json.dumps(data))
        if (r.status_code == 200):
                return True
        else:
            writeToLog("INFO","Bad response for get sessions. " + r.text)
            return False
        

    #=============================================================================================================
    # Function that sets the test custom field
    # customFiledId example: "---f-38302"
    #=============================================================================================================
    def updateInstanceCustomFields(self, instanceId, customFiledsDict):
        practiTestUpdateASpecificTestsetInstanceUrl = "https://api.practitest.com/api/v2/projects/" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_PROJECT_ID) + \
                                                        "/sets/" + str(instanceId) + ".json?" + \
                                                        "api_token=" + str(localSettings.LOCAL_SETTINGS_PRACTITEST_API_TOKEN) + \
                                                        "&developer_email=" + str(localSettings.LOCAL_SETTINGS_DEVELOPER_EMAIL) 
        headers = { 
            'Content-Type': 'application/json',
            'Connection':'close'
        }
        data = self.createDataForTestsetMultipleCustomFileds(customFiledsDict)
        # Convert data string to variable
        data = eval(data) 
        r = requests.put(practiTestUpdateASpecificTestsetInstanceUrl,headers = headers, data = json.dumps(data))
        if (r.status_code == 200):
                return True
        else:
            writeToLog("INFO","Bad response for get sessions. " + r.text)
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
        
