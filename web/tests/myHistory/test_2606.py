import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
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
    # After entry is deleted from KMS, he shouldn't displayed in My History
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to My history and check that entry isn't displayed -> Go to entry page and play entry -> Go to
    # MY History page and make sure that entry exists in page -> 
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2606"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistory', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
             
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 3: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to entry page")
                return           
            
            writeToLog("INFO","Step 4: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED - New entry is still processing")
                return
             
            writeToLog("INFO","Step 5: Going to Search entry in My History page")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED - New entry is displayed in my history page")
                return
            writeToLog("INFO","Step 5: Previous Step Failed as Expected - The entry should not be displayed")
            
            writeToLog("INFO","Step 6: Going to play entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryName, '0:05') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate and play entry")
                return  
            
            writeToLog("INFO","Step 7: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to switch to default content")
                return  
            
            writeToLog("INFO","Step 8: Going to navigate to my history and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED find entry in my history")
                return     
            
            writeToLog("INFO","Step 9: Going to delete entry from My Media")
            if self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to delete entry from My Media")
                return   
            
            writeToLog("INFO","Step 10: Going to Search entry in My History page")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED - New entry is displayed in my history page")
                return
            writeToLog("INFO","Step 10: Previous Step Failed as Expected - The entry should not be displayed")                       
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
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')