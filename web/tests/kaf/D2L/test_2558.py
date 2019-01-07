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
from upload import UploadEntry

class Test:
    #================================================================================================================================
    # @Author: Inbar Willman
    # Test Name : D2L - Upload Media From Media Gallery Page
    # Test description:
    # Upload entry
    # Go to course page > Click tool - media gallery -> Upload media -> Verify entry display in media gallery
    #================================================================================================================================
    testNum     = "2558"
    application = enums.Application.D2L
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3'
    galleryName = "New1"
    
    
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
            self.entryName = clsTestService.addGuidToString("upload entry to media gallery", self.testNum)  
            self.entryToUpload = UploadEntry(self.filePath, self.entryName, self.description, self.tags, timeout=60, retries=3)
            self.uploadEntrieList = [self.entryToUpload] 
            
            ######################### TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to add new media to media gallery")  
            if self.common.kafGeneric.addNewContentToGallery(self.galleryName, self.uploadEntrieList, isGalleryModerate=False)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to add new media to media gallery")
                return 
            
            writeToLog("INFO","Step 2: Going to navigate media gallery")  
            if self.common.kafGeneric.navigateToGallery(self.galleryName)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate media gallery")
                return     
                    
            self.common.base.click(self.common.kafGeneric.KAF_REFRSH_BUTTON)
            sleep(5)
            writeToLog("INFO","Step 3: Going to make a search in media gallery and verify that entry is displayed in media gallery")  
            if self.common.channel.searchEntryInChannel(self.entryName)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to make a search in media gallery and verify that entry is displayed in media gallery")
                return 
             
            #########################################################################
            writeToLog("INFO","TEST PASSED: D2L - Add new media to media gallery was done successfully")
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