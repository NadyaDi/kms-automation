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
    # Test Name : Moodle - Embed media in site blogs from media gallery
    # Test description:
    # Upload image entry -> publish to media gallery -> Go to site blog -> Click on kaltura media -> Click on 'media gallery' tab
    # Select video -> Embed -> Verify that entry was embedded and played
    #================================================================================================================================
    testNum     = "2397"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_5.png'
    galleryName = "New1"
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
            self.entryName = clsTestService.addGuidToString("EmbedMediaInSiteBlogFromMediaGallery", self.testNum)
            self.siteBlogTitle = clsTestService.addGuidToString("siteBlogFromMediaGallery-Image", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            #disable assignment submission in admin
            if LOCAL_SETTINGS_ENV_NAME == 'ProdNewUI':
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = 'https://1820181-1.kaf.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'Blackboard@kaltura.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
            else: # testing 
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = 'https://2104601-5.kaftest.dev.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'Freetrail@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
            self.common.admin.enableDisabledAssignmentSubmission(False)
            
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
               
            writeToLog("INFO","Step 4: Going to publish entry to gallery")    
            if self.common.myMedia.publishSingleEntry(self.entryName, '', '', [self.galleryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to publish entry to gallery")
                return         
              
            writeToLog("INFO","Step 5: Going to create embed site blog from 'My Media'")    
            if self.common.moodle.createEmbedSiteBlog(self.entryName, self.siteBlogTitle, embedFrom=enums.Location.MEDIA_GALLARY,chooseMediaGalleryinEmbed=True, mediaGalleryName=self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to create embed site blog from 'My Media'")
                return 
             
            writeToLog("INFO","Step 6: Going to verify embed site blog")    
            if self.common.kafGeneric.verifyEmbedEntry(self.siteBlogTitle, self.uploadThumbnailExpectedResult, '', application=enums.Application.MOODLE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify embed site blog")
                return  
             
            writeToLog("INFO","Step 7: Going to delete embed site blog")    
            if self.common.moodle.deleteEmbedSiteBlog(self.siteBlogTitle)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to delete embed site blog")
                return
            
            writeToLog("INFO","Step 8: Going to verify deletion of embed site blog")    
            if self.common.moodle.verifyDeletionOfSiteBlogFromSiteBlogsPage(self.siteBlogTitle)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify deletion of embed site blog")
                return                             
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - Embed media in site blogs from media gallery' was done successfully")
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