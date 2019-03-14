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
    #  @Author: Inbar Willman
    # Test Name: My Media - Delete - multiple
    #test description: Delete multiple entries
    # The test's Flow: 
    # Login to KMS-> Upload entries -> Go to My Media -> Delete uploaded entries
    #================================================================================================================================
    testNum     = "659"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entriesList = []
    entryDescription = "description"
    entryTags = "tag1,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'  
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
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('deleteMultiple1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('deleteMultiple2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('deleteMultiple3', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3]
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload 3 entries")
            if self.common.upload.uploadMultipleEntries(self.filePath, self.entriesList, self.entryDescription, self.entryTags) == False:
                writeToLog("INFO","Step 1: FAILED to upload 3 entries")
                return
               
            writeToLog("INFO","Step 2: Going to delete uploaded entries")
            if self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList) == False:
                writeToLog("INFO","Step 2: FAILED delete entries")
                return
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Delete multiple entries' was done successfully")
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