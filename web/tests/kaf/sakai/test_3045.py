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
    # Test Name : Sakai - Announcment Upload And Embed From BSE Page Sakai
    # Test description:
    # Go to course -> Click on 'Announcemnt' -> Click 'Add' -> Click on 'Kaltura Media' -> Click 'Add new' and upload new media
    # Click 'Save' -> Verify that embed is displayed and played
    #================================================================================================================================
    testNum     = "3045"
    application = enums.Application.SAKAI
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    description = "Description" 
    tags = "Tags,"
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
            self.entryName = clsTestService.addGuidToString("EmbedAnnoncemntFromUpload", self.testNum)
            self.announcementName = clsTestService.addGuidToString("Embed announcement from Upload", self.testNum)

            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create embed announcement")    
            if self.common.sakai.createEmbedAnnouncement(self.announcementName, self.entryName, embedFrom=enums.Location.UPLOAD_PAGE_EMBED, filePath=self.filePath, description=self.description, isTagsNeeded=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create embed announcement")
                return 
            
            writeToLog("INFO","Step 2: Going to verify embed announcement")    
            if self.common.sakai.verifyEmbedAnnouncement(self.announcementName, self.uploadThumbnailExpectedResult, '') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify embed announcement")
                return 
            
            writeToLog("INFO","Step 3: Going to delete embed announcement")    
            if self.common.sakai.deleteAnnouncement(self.announcementName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to delete embed announcement")
                return                                                                                     
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Sakai -  Announcment BSE From upload' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.sakai.deleteAnnouncement(self.announcementName, True)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')