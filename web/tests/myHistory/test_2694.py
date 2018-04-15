from enum import *
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
    # Test description:
    # Search in My History page by entry's description
    # The test's Flow: 
    # Login to KMS-> Upload audio entry-> Go to entry page and play entry -> Go to
    # MY History page and search entry by description
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2694"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName= None
    entryDescription = None
    entryTags = "tag1,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistoryVideoEntry', self.testNum)
            self.entryDescription = clsTestService.addGuidToString('MyHistoryEntryDescription', self.testNum)
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload video entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload audio entry")
                return
                
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return            
               
            writeToLog("INFO","Step 3: Going to play entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryName, '0:05', toVerify=False, timeout=50) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate and play entry")
                return  
               
            writeToLog("INFO","Step 4: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to switch to default content")
                return  
            
            writeToLog("INFO"," Step 5: Going to navigate to my history and search entry by description")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName, self.entryDescription) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED find entry in My History page")
                return        
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)            
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)         
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')