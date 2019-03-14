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
    # Test Name: Watch History - Entry appear in both continue watch & recently watched playlists - Replay
    # Test description:
    # Check that entry that wasn't played until end has 'started' status and is displayed in continue watching list
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to My history and check that entry isn't displayed -> Go to entry page and play entry -> Go to
    # MY History page and make sure that entry's progress bar is started -> Go to home page and make sure entry displayed in continue watching list
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2742"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    continueWatchingPlaylist = 'Continue watching '
    recentlyWatchedPlaylist = 'Recently Watched '
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistoryContinueWatching', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return  
               
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return           
               
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return
                
            writeToLog("INFO","Step 4: Going to Search entry in My History page")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == True:
                writeToLog("INFO","Step 4: FAILED - New entry is displayed in my history page")
                return
            writeToLog("INFO","Step 4: Previous Step Failed as Expected - The entry should not be displayed")
               
            writeToLog("INFO","Step 5: Going to play entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryName, '0:05') == False:
                writeToLog("INFO","Step 5: FAILED to navigate and play entry")
                return  
               
            writeToLog("INFO","Step 6: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                writeToLog("INFO","Step 6: FAILED to switch to default content")
                return  
              
            writeToLog("INFO","Step 7: Going to navigate to My History and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryName) == False:
                writeToLog("INFO","Step 7: FAILED find entry in My History")
                return   
              
            writeToLog("INFO","Step 8: Going to navigate to home page and check entry in continue watching list")
            if self.common.home.checkEntryInHomePlaylist(self.continueWatchingPlaylist, self.entryName) == False:
                writeToLog("INFO","Step 8: FAILED to find entry in continue watching list")
                return      
            
            writeToLog("INFO","Step 9: Going to navigate to home page and check entry in recently list")
            if self.common.home.checkEntryInHomePlaylist(self.recentlyWatchedPlaylist, self.entryName) == False:
                writeToLog("INFO","Step 9: FAILED to find entry in recently watched list")
                return               
            
            writeToLog("INFO","Step 9: Going to navigate to entry page")
            if self.common.entryPage.navigateToEntry(self.entryName, navigateFrom = enums.Location.HOME) == False:
                writeToLog("INFO","Step 9: FAILED to navigate to entry page")
                return   
            
            writeToLog("INFO","Step 10: Going to play entry until the end")
            if self.common.player.clickPlay('0:10') == False:
                writeToLog("INFO","Step 10: FAILED to play entry")
                return 
            
            sleep(10)   
            
            writeToLog("INFO","Step 11: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                writeToLog("INFO","Step 11: FAILED to switch to default content")
                return              
            
            writeToLog("INFO","Step 12: Going to navigate to home page and check entry in recently watched list")
            if self.common.home.checkEntryInHomePlaylist(self.recentlyWatchedPlaylist, self.entryName) == False:
                writeToLog("INFO","Step 12: FAILED to find entry in recently watched list")
                return  
            
#             writeToLog("INFO","Step 13: Going to navigate to home page and check entry in continue watching list")
#             if self.common.home.checkEntryInHomePlaylist(self.continueWatchingPlaylist, self.entryName) == True:
#                 writeToLog("INFO","Step 13: FAILED - Entry that played until the end still displayed in continue watching list")
#                 return   
#             writeToLog("INFO","Step 13: FAILED as expected  - entry shouldn't be displayed in continue watching list")                                              
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
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')