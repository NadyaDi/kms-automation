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
    # Test Name : D2L: Discussions Upload And Embed From BSE Page
    # Test description:
    # Go to discussions -> Create new discussion -> click on wysisyg -> Click on 'Add new' and upload new media
    # Verify that embed is displayed and played 
    #================================================================================================================================
    testNum     = "2906"
    application = enums.Application.D2L
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    discussionName = None
    galleryName = "New1"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_5.png'
    uploadThumbnailExpectedResult = 5
    
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
            self.entryName = clsTestService.addGuidToString("EmbedFromUpload", self.testNum)
            self.discussionName = clsTestService.addGuidToString("Embed video from upload", self.testNum)
            self.entryToUpload = UploadEntry(self.filePath, self.entryName, self.description, self.tags)
            ##################### TEST STEPS - MAIN FLOW ##################### 
                 
            writeToLog("INFO","Step 1: Going to create embed discussion")    
            if self.common.d2l.createEmbedDiscussion(self.discussionName, self.entryName, self.galleryName, embedFrom=enums.Location.UPLOAD_PAGE_EMBED, filePath=self.filePath, description=self.description, tags=None, isTagsNeeded=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create embed discussion")
                return             
              
            writeToLog("INFO","Step 2: Going to to verify embed announcement")    
            if self.common.kafGeneric.verifyEmbedEntry(self.entryName, self.uploadThumbnailExpectedResult, '', enums.Application.D2L) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify embed announcement")
                return     
             
            writeToLog("INFO","Step 3: Going to to delete embed announcement")    
            if self.common.d2l.deleteDiscussion(self.discussionName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to delete embed announcement")
                return              
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Create embed discussion from new upload ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.d2l.deleteDiscussion(self.discussionName, True)     
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')