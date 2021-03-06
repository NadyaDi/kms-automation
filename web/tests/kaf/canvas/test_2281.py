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
    # Test Name : Canvas - Publish after upload
    # Test description:
    # 1. Enter my media and click on "add new"
    # 2. Choose a file to upload and click save
    # 3. After entry was finished upload - Click publish and choose a course to publish the media (from upload page)
    # 4. Go the course and verify that the entry was published
    #================================================================================================================================
    testNum     = "2281"
    application = enums.Application.CANVAS
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    galleryName = "New1"
    
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
            self.entryName = clsTestService.addGuidToString("Publish from upload page", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry")  
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry' " + self.entryName)
                return 
                                 
            writeToLog("INFO","Step 2: Going to publish entry from upload page")  
            if self.common.myMedia.publishSingleEntry(self.entryName, "", "", [self.galleryName], publishFrom = enums.Location.UPLOAD_PAGE, disclaimer=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to publish entry' " + self.entryName + " to gallery upload page")
                return 
            sleep(3)
            writeToLog("INFO","Step 3: Going navigate to gallery page")
            if self.common.kafGeneric.navigateToGallery(self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to gallery: " + self.galleryName)
                return
                
            writeToLog("INFO","Step 4: Going to verify entry published to category ")
            if self.common.channel.searchEntryInChannel(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to find entry ' " + self.entryName + "' in gallery: " + self.galleryName)
                return 
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Canvas - Publish after upload' was done successfully")
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