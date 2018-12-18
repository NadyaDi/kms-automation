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
    # @Author: Inbar Willman
    # Test Name : Moodle - Embed media in site blogs from my media
    # Test description:
    # Upload entry -> Go to site page -> Go to site blog -> Click on kaltura media -> Click on 'My media' tab
    # Select video -> Embed -> Verify that entry was embedded and played
    #================================================================================================================================
    testNum     = "2127"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    videoQrCodeResult = "7"
    vidoeLength = "0:10"
    vidoeTimeToStop = "0:07"
    categoryName = None
    
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
            self.entryName = clsTestService.addGuidToString("Embed media in site blog from my media - video", self.testNum)
            self.siteBlogTitle = clsTestService.addGuidToString("site blog from my media - video", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
             
            writeToLog("INFO","Step 2: Going to to navigate to entry page")    
            if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate entry page")
                return
             
            writeToLog("INFO","Step 3: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to wait until media end upload process")
                return
             
            writeToLog("INFO","Step 4: Going to create embed site blog from 'My Media'")    
            if self.common.moodle.createEmbedSiteBlog(self.entryName, self.siteBlogTitle)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to create embed site blog from 'My Media'")
                return 
            
            writeToLog("INFO","Step 5: Going to verify embed site blog")    
            if self.common.kafGeneric.verifyEmbedEntry(self.siteBlogTitle, '', self.vidoeTimeToStop, application=enums.Application.MOODLE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify embed site blog")
                return  
            
            writeToLog("INFO","Step 6: Going to delete embed site blog")    
            if self.common.moodle.deleteEmbedSiteBlog(self.siteBlogTitle)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to delete embed site blog")
                return                                         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Upload media from desktop and verify player' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.moodle.deleteEmbedSiteBlog(self.siteBlogTitle, True)
            writeToLog("INFO","**************** Ended: teardown_method *******************")                       
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')