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
    # Test Name : BB - Edit entry page - Thumbnail tab 
    # Test description:
    # Login to KMS, and upload a media
    # Navigate Edit Entry Page
    # under thumbnail tab change thumnbnail in 3 different ways : Upload, Capture, Auto-Generate
    #================================================================================================================================
    testNum     = "594"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    uploadThumbnailExpectedResult = 5
    timeToStopPlayer = "0:07"
    captureThumbnailExpectedResult = 7
    autoGenerateSliceNumber = 6
    autoGenerateThumbnailExpectedResult = 6
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10secQrMidLeftSmall.mp4'
    uploadThumbnailFliePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_5.png'
    
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix, self.application)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Edit entry - thumbnail tab", self.testNum)
            
            ######################### TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                return
               
            writeToLog("INFO","Step 3: Going to upload thumbnail in edit Entry Page")
            if self.common.editEntryPage.uploadThumbnail(self.uploadThumbnailFliePath, self.uploadThumbnailExpectedResult) == False:
                writeToLog("INFO","Step 3: FAILED to upload thumbnail")
                return
                                
            writeToLog("INFO","Step 4: Going to navigate to entry page")            
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName, leavePage=True) == False:
                writeToLog("INFO","Step 4: FAILED navigate to entry page '" + self.entryName + "'")
                return
            sleep(4)
              
            writeToLog("INFO","Step 5: Going to check the entry thumbnail in the player")
            if self.common.player.verifyThumbnailInPlayer(self.uploadThumbnailExpectedResult) == False:
                writeToLog("INFO","Step 5: FAILED failed to logout from main user")
                return  
             
            self.common.switch_to_default_iframe_generic()
            writeToLog("INFO","Step 6: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 6: FAILED to navigate to edit entry page")
                return                  
               
            writeToLog("INFO","Step 7: Going to capture thumbnail")            
            if self.common.editEntryPage.captureThumbnail(self.timeToStopPlayer, self.captureThumbnailExpectedResult, playFromBarline=False) == False:
                writeToLog("INFO","Step 7: FAILED to capture thumbnail")
                return                                
                                 
            sleep(2)     
            writeToLog("INFO","Step 8: Going to navigate to entry page")            
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 8: FAILED navigate to entry page '" + self.entryName + "'")
                return
               
            writeToLog("INFO","Step 9: Going to check the entry thumbnail in the player")
            if self.common.player.verifyThumbnailInPlayer(self.captureThumbnailExpectedResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED failed to logout from main user")
                return                      
                                
            writeToLog("INFO","Step 10: Going to navigate to edit Entry Page")
            self.common.switch_to_default_iframe_generic()
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 10: FAILED to navigate to edit entry page")
                return                  
               
            writeToLog("INFO","Step 11: Going to chose auto generate  thumbnail")            
            if self.common.editEntryPage.chooseAutoGthumbnail(self.autoGenerateSliceNumber, self.autoGenerateThumbnailExpectedResult) == False:
                writeToLog("INFO","Step 11: FAILED to choose auto generate thumbnail")
                return                                
                                 
            sleep(2)     
            writeToLog("INFO","Step 12: Going to navigate to entry page")            
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                writeToLog("INFO","Step 12: FAILED navigate to entry page '" + self.entryName + "'")
                return
               
            writeToLog("INFO","Step 13: Going to check the entry thumbnail in the player")
            if self.common.player.verifyThumbnailInPlayer(self.autoGenerateThumbnailExpectedResult) == False:
                writeToLog("INFO","Step 13: FAILED failed to logout from main user")
                return                                         
            
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Edit entry - thumbnail tab' was done successfully")
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