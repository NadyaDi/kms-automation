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
    # Test Name: Watch History - delete multiple entries from watch list history
    # Test description:
    # Before entry is played, history page doesn't displayed the entry
    # After entry was played, it displayed in history page
    # After few entries were deleted from watch list in my history page, they shouldn't displayed in my history anymore
    # The test's Flow: 
    # Login to KMS-> Upload 3 entries -> Go to My history and check that entries aren't displayed -> Go to each entry page and play entry -> Go to
    # My History page and make sure that entries exists in page -> Delete each entry -> Make sure entries aren't displayed in My History page
    #================================================================================================================================
    testNum     = "2568"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entriesNames = None
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
            self.entryName1 = clsTestService.addGuidToString('MyHistoryEntry1')
            self.entryName2 = clsTestService.addGuidToString('MyHistoryEntry2')
            self.entryName3 = clsTestService.addGuidToString('MyHistoryEntry3')
            self.entriesNames = [self.entryName1, self.entryName2, self.entryName3]
            ######################### TEST STEPS - MAIN FLOW ####################### 
            step = 1
            for entry in self.entriesNames:
                writeToLog("INFO" ,"Step " + str(step) + ": Going to upload " + entry)
                if self.common.upload.uploadEntry(self.filePath, entry, self.entryDescription, self.entryTags, disclaimer=False) == None:
                    writeToLog("INFO" ,"Step " + str(step) + ": FAILED to upload " + entry)
                    return   
                
                step = step + 1
                
                writeToLog("INFO" ,"Step " + str(step) + ": Going to navigate to uploaded " + entry)
                if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                    writeToLog("INFO" ,"Step " + str(step) + ": FAILED to navigate to "  + entry)
                    return   
                         
                step = step + 1
                
                writeToLog("INFO", "Step " + str(step) + ": Going to wait until " +  entry + " will finish processing")
                if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO", "Step " + str(step) + ": FAILED - New entry " +  entry + "  is still processing")
                    return 
                
                step = step + 1  
                
                writeToLog("INFO", "Step " + str(step) + ": Going to Search " + entry + " in My History page")
                if self.common.myHistory.waitTillLocatorExistsInMyHistory(entry) == True:
                    writeToLog("INFO","Step " + str(step) + ": FAILED - New entry " + entry + " is displayed in my history page")
                    return 
                writeToLog("INFO","Step " + str(step) + ": Previous Step Failed as Expected - The entry should not be displayed")      
                
                step = step + 1
                
                writeToLog("INFO","Step " + str(step) + ": Going to play " + entry)
                if self.common.player.navigateToEntryClickPlayPause(entry, '0:05') == False:
                    writeToLog("INFO","Step " + str(step) + ": FAILED to navigate and play " + entry)
                    return               
  
                step = step + 1
            
                writeToLog("INFO","Step " + str(step) + ": Going to switch to default content")
                if self.common.base.switch_to_default_content() == False:
                    writeToLog("INFO","Step " + str(step) + ": FAILED to switch to default content")
                    return      
                
                step = step + 1 
            
            for entry in self.entriesNames:
                writeToLog("INFO","Step " + str(step) + ": Going to navigate to My History and check for " + entry)
                if self.common.myHistory.waitTillLocatorExistsInMyHistory(entry) == False:
                    writeToLog("INFO","Step " + str(step) + ": FAILED find " + entry + " in My History")
                    return 
                
                step = step + 1   
                
                writeToLog("INFO","Step " + str(step) + ": Going to delete " + entry + " from My History")
                if self.common.myHistory.removeEntryFromWatchListMyHistory(entry) == False:
                    writeToLog("INFO","Step " + str(step) + ": FAILED to delete " + entry + " from My History")
                    return 
                
                step = step + 1   
            
                writeToLog("INFO","Step " + str(step) + ": Going to navigate to My History and check for " + entry)
                if self.common.myHistory.waitTillLocatorExistsInMyHistory(entry) == True:
                    writeToLog("INFO","Step " + str(step) + ": FAILED to delete " + entry + " from My History")
                    return
                writeToLog("INFO","Step " + str(step) + ": Previous Step Failed as Expected - The entry should not be displayed")
                
                step = step + 1  
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesNames)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')