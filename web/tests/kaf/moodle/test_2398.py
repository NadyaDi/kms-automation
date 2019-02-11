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
    # Test Name : Moodle - upload and Embed media in kaltura video resource
    # Test description:
    # Go to course page -> Turn editing on -> Click 'Add activity or resource' -> Choose 'kaltura video resource' and click 'Add' -> Click on 'Add media'
    # Click on 'Upload' -> Upload image -> Embed -> Verify that entry was embedded and played
    #================================================================================================================================
    testNum     = "2398"
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
            self.entryName = clsTestService.addGuidToString("Embed media in kaltura video resource from upload - image", self.testNum)
            self.activityTitle = clsTestService.addGuidToString("kaltura video resource from upload - image", self.testNum)
            
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
            
            writeToLog("INFO","Step 1: Going to create embed kaltura video resource from upload page")    
            if self.common.moodle.createEmbedActivity(self.entryName, self.activityTitle, embedFrom=enums.Location.UPLOAD_PAGE_EMBED, filePath=self.filePath, description=self.description, tags=self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create embed kaltura video resourcefrom upload page")
                return 
             
            writeToLog("INFO","Step 2: Going to verify embed kaltura video resource")    
            if self.common.kafGeneric.verifyEmbedEntry(self.activityTitle, self.uploadThumbnailExpectedResult, '', application=enums.Application.MOODLE, activity=enums.MoodleActivities.KALTURA_VIDEO_RESOURCE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify embed kaltura video resource")
                return  
            
            writeToLog("INFO","Step 3: Going to delete embed kaltura video resource")    
            if self.common.moodle.deleteEmbedActivity(self.activityTitle)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to delete embed kaltura video resource")
                return                          
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - upload and Embed media in kaltura video resource' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.moodle.deleteEmbedActivity(self.activityTitle)
            writeToLog("INFO","**************** Ended: teardown_method *******************")                       
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')