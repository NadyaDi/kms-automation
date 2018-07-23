import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : General - Search Media
    # Test description:
    # upload and publish new entry 
    # In the header - global search enter an existing word to the text box and click on search: 
    #     Search results page should be opened successfully.
    #     The title should be "Search for: "
    #     the searched word- 
    #     Appropriate entries should be displayed in the list. 
    #     For each entry thumbnail and metadata should be displayed
    #     The word you have searched for should be marked in the results. 

    #================================================================================================================================
    testNum = "638"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entryName5 = None
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    categoryName = [("Apps Automation Category")]

    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Global search - Search Media", self.testNum)

            ##################### TEST STEPS - MAIN FLOW ##################### 


            writeToLog("INFO","Step 1: Going to upload entry")            
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload new entry: " + self.entryName)
                return
    
            writeToLog("INFO","Step 2: Going to published entry")  
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryName, "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to publish entry '" + self.entryName + "'")
                return 

            writeToLog("INFO","Step 3: Going to search entry in global search")
            if self.common.general.SerchInGlobalSearch(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to search entry'" + self.entryName + "' in global search")
                return 
                
            writeToLog("INFO","Step 4: Going to verify that search entry was found after global search")
                
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Global search - Search Media' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')