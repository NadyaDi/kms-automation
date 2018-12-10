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
    # Test Name : Moodle - Delete through my media
    # Test description:
    # Upload video entry -> Go to my media -> Select entry -> Delete entry
    #================================================================================================================================
    testNum     = "2104"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    videoEntryName = None
    audioEntryName = None
    imageEntryName = None
    description = "Description" 
    tags = "Tags,"
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
            self.videoEntryName = clsTestService.addGuidToString("Delete entry through My Media - Video", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload video entry")   
            if self.common.upload.uploadEntry(self.filePathVideo,self.videoEntryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload video entry")
                return
                      
            writeToLog("INFO","Step 2: Going navigate to my media and delete entry")    
            if self.common.myMedia.deleteSingleEntryFromMyMedia(self.videoEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to my media and delete entry")

         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - Delete through my media' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")  
            
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')