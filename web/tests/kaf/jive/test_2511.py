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
    # Test Name : Jive - Discussions Upload And Embed From BSE Page
    # Test description:
    # upload media -> Click on 'Create' and choose 'Discussion' -> Click on wysisyg -> Click on 'Add new' -> Upload new media -> Save emebed
    # Verify that embed is displayed and played
    #================================================================================================================================
    testNum     = "2511"
    application = enums.Application.JIVE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    description = "Description" 
    tags = "Tags,"
    discussionName = None
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
            self.entryName = clsTestService.addGuidToString("EmbedDiscussionFromUpload", self.testNum)
            self.discussionName = clsTestService.addGuidToString("Embed discussion from upload", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
                
            writeToLog("INFO","Step 1: Going to to create embed discussion")    
            if self.common.jive.createEmbedMedia(self.discussionName, self.entryName, embedFrom=enums.Location.UPLOAD_PAGE_EMBED, filePath=self.filePath, description=self.description, isTagsNeeded=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create embed discussion")
                return
               
            writeToLog("INFO","Step 2: Going to to verify embed discussion")    
            if self.common.jive.verifyEmbedMedia(self.discussionName, self.uploadThumbnailExpectedResult, '') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify embed discussion")
                return 
            
            writeToLog("INFO","Step 3: Going to to delete embed discussion")    
            if self.common.jive.deleteEmbedMedia(self.discussionName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to delete embed discussion")
                return                                                                     
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Jive - Embed media in document from My Media ' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.jive.deleteEmbedMedia(self.discussionName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')