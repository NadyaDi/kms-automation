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
    # Test Name : Moodle - Publish after upload
    # Test description:
    # Upload video entry -> publish entry from upload page -> Verify entry is published to the course
    #================================================================================================================================
    testNum     = "2106"
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
    galleryName = 'New1'
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
            self.videoEntryName = clsTestService.addGuidToString("Publish from upload page", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
#             writeToLog("INFO","Step 1: Going to upload video entry")   
#             if self.common.upload.uploadEntry(self.filePathVideo, self.videoEntryName, self.description, self.tags) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to upload video entry")
#                 return
#                       
#             writeToLog("INFO","Step 2: Going to publish entry from upload page")    
#             if self.common.myMedia.publishSingleEntry(self.videoEntryName, '', [self.galleryName], publishFrom = enums.Location.UPLOAD_PAGE) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED to publish entry from upload page")
#                 return
            
            writeToLog("INFO","Step 3: Going to to navigate to gallery page")    
            if self.common.kafGeneric.navigateToGallery(self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to gallery page")
                return            
                     
         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - Publish from upload page' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")  
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.videoEntryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')