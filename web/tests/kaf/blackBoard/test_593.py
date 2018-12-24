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
import ctypes


class Test:
    #================================================================================================================================
    # @Author: Michal Zomper
    # Test Name: BB : Entry page - Add captions And Search - remove caption
    # Test description:
    # Upload entry ->Go to edit entry ->  'Captions' tab -> Upload a captions file -> Fill out the relevant fields-> 
    # Go back to the entry page and search caption
    # Go to edit entry and remove caption
    #================================================================================================================================
    testNum     = "593"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    captionLanguage = "English (American)"
    captionLabel = None
    captionTime1 = '0:06'
    captionTime2 = '00:05'
    captionText = '- Caption search 2'
    expectedCaptionAfterSearch = '- Caption search 1'
    filePathCaption = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\testcaption1.srt'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix, self.application)
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Add captions And Search", self.testNum)
            self.captionLabel = clsTestService.addGuidToString("English", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry")   
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
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
              
            writeToLog("INFO","Step 4: Going to navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to navigate to edit entry page")
                return                
            
            writeToLog("INFO","Step 5: Going to add caption")
            if self.common.editEntryPage.addCaptions(self.filePathCaption, self.captionLanguage, self.captionLabel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add caption")
                return     
            
            writeToLog("INFO","Step 6: Navigate to entry page and play entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryName, self.captionTime1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to upload caption")
                return     
            
            writeToLog("INFO","Step 7: Verify that correct caption text is displayed")
            if self.common.player.verifyCaptionText(self.captionText) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to displayed correct captions text")
                return   
            self.common.blackBoard.switchToBlackboardIframe()
            
            writeToLog("INFO","Step 8: Going to verify that caption display in the caption section in entry page and in the player")
            if self.common.entryPage.verifyAndClickCaptionSearchResult(self.captionTime2, self.captionText, self.expectedCaptionAfterSearch) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to edit entry page")
                return   
            
            self.common.blackBoard.switchToBlackboardIframe()   
            writeToLog("INFO","Step 9: Going navigate to edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED navigate to edit entry page")
                return              
            
            writeToLog("INFO","Step 10: Going to remove added caption")
            if self.common.editEntryPage.removeCaption(self.captionLabel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to remove added caption to entry '" + self.entryName + "'")
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Add captions And Search' was done successfully")
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