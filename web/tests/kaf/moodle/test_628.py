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
    # Test Name : Moodle - Assignment Submission Functionalities
    # Test description:
    # Upload entry -> Edit SR required fields -> Publish entry entry from my media to SR
    # Verify that entry is displayed in SR
    #================================================================================================================================
    testNum     = "628"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_5.png'
    
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
            self.entryName = clsTestService.addGuidToString("Assignment submission test", self.testNum)
            self.galleryName = "New1"
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to enable assignment submission")    
            if self.common.admin.enableDisabledAssignmentSubmission(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to enable assignment submission")
                return              
            
            writeToLog("INFO","Step 2: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return  
            
            writeToLog("INFO","Step 3: Going to create assignment submission")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to upload entry")
                return                        

            
            self.common.base.click(self.common.kafGeneric.KAF_REFRSH_BUTTON)
            sleep(5)
            
            self.common.blackBoard.switchToBlackboardIframe()
            writeToLog("INFO","Step 8: Going to verify entry '" + self.entryName + " in media gallery")
            if self.common.channel.searchEntryInChannel(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to find entry '" + self.entryName + " in media gallery")
                return                                                
         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - Assignment Submission Functionalities' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.admin.enableDisabledAssignmentSubmission(False)
            writeToLog("INFO","**************** Ended: teardown_method *******************")                       
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')