import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Tsvika Knirsh
    # test Name: Add webcast event - KS restriction
    # Test description: publish entry to category from entry page
    # The test's Flow: 
    # Login to KMS-> Create WC entry ->  Open KMC > Click on 'Actions' -Publish -> choose category to publish to -> Click save
    # -> Check that entry is displayed in category
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "3130"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryNameWebCast                  = "Webcast regression"
    entryDescription                  = "Webcast regression"
    entryTags                         = "Webcast_regression_tag,"
    wcAccsesControlKS_settings        = ["launchapplication","startliveevent","monitoring"]
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)

            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to set webcast settings file")
            if self.common.webcast.setWebcastSetting(self.wcAccsesControlKS_settings)== False:
                writeToLog("INFO","Step 1: FAILED to set webcast settings file")
                return
            
            writeToLog("INFO","Step 2: Going to create " + self.entryNameWebCast + " entry")
            if self.common.upload.addWebcastEntry(self.entryNameWebCast, self.entryDescription, self.entryTags) == False:
                writeToLog("INFO","Step 2: FAILED to create " + self.entryNameWebCast + " entry")
                return
            
            writeToLog("INFO","Step 3: Open Edit Webcast Event page from create webcast page")
            if self.common.webcast.editWebCastEvent() == False:
                writeToLog("INFO","Step 3: FAILED to open " + self.entryNameWebCast + " edit page")
                return
            
            writeToLog("INFO","Step 4: Login to partner KMC")
            if self.common.webcast.loginToKMC() == False:
                writeToLog("INFO","Step 4: FAILED to open KMC page")
                return 
            
            writeToLog("INFO","Step 5: Running Webcast Sikulix script")
            if self.common.webcast.startSikulixScript() == False:
                writeToLog("INFO","Step 5: FAILED to run sikulix webcast script")    
                return
            
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Webcast access control KS' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')