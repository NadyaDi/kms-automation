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
    # Test Name: Watch History - delete entry (Published to channel) from watch list history
    # Test description:
    # Before entry is played, history page doesn't displayed the entry
    # After entry was played, it displayed in history page
    # After entry was deleted from watch list in my history page, it shouldn't displayed in my history anymore
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Publish entry to channel-> Go to My history and check that entry isn't displayed -> Go to entry page and play entry -> Go to
    # MY History page and make sure that entry exists in page -> Delete entry -> Make sure entry isn't displayed in My History page
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2567"
    
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistoryEntry', self.testNum)
            ######################### TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
             
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return           
             
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return
              
            writeToLog("INFO","Step 4: Going to Search entry in My History page")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED - New entry is displayed in my history page")
                return
            writeToLog("INFO","Step 4: Previous Step Failed as Expected - The entry should not be displayed")
             
            writeToLog("INFO","Step 5: Going to play entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryName, '0:05') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate and play entry")
                return  
             
            writeToLog("INFO","Step 6: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to switch to default content")
                return  
            
            writeToLog("INFO","Step 7: Going to navigate to My History and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED find entry in My History")
                return   
            
            writeToLog("INFO","Step 8: Going to delete entry from My History")
            if self.common.myHistory.removeEntryFromWatchListMyHistory(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to delete entry from My History")
                return               
            
            writeToLog("INFO","Step 9: Going to verify that entry isn't displayed in My History")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED - Deleted entry is displayed in My History page")
                return
            writeToLog("INFO","Step 9: Previous Step Failed as Expected - The entry should not be displayed")
              
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)            
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')