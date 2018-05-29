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
    # Test description:
    # Replace entry media
    # The test's Flow: 
    # Login to KMS-> Upload entry -> Go to entry page > Click on 'Actions'-->'Edit' -> Go to 'Replace video' tab -> Upload new video
    # -> Click 'Approve Replacement' -> Wait until 'Your media was successfully replaced.' -> Check that media has changed
    # Go to entry page and continue play entry (not to the end) -> 
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "703"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTag = "tag1,"
    urationBeforeReplacment = ' / 0:30'
    durationAfterReplacment = ' / 0:10'
    filePathVideo1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    filePathVideo2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10SecQR100109.mp4'
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
            self.entryName = clsTestService.addGuidToString('replaceVideo', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePathVideo1, self.entryName, self.entryDescription, self.entryTag, disclaimer=False) == None:
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

            writeToLog("INFO","Step 4: Going to play and verify entry")
            if self.common.player.clickPlayPauseAndVerify('0:05') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to play and verify entry")
                return       
            
            writeToLog("INFO","Step 5: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to switch to default content")
                return                   
               
            writeToLog("INFO","Step 6: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate to edit entry page")
                return                
                        
            writeToLog("INFO","Step 7: Going to replace entry media")
            if self.common.editEntryPage.replaceVideo(self.filePathVideo2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to replace entry media")
                return             
            
            writeToLog("INFO","Step 8: Verify that video was replaced")
            if self.common.player.clickPauseAndVerify('0:08',clickPlayFromBarline=False, compareToStr='106') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to replace video")
                return                                                                                    
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