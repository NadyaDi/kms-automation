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
    # Enable assignment submission module -> upload entry -> embed entry and create assignment submission
    # -> verify that entry is displayed and played -> upload another entry -> embed entry and don't create assignment submission -> 
    # Verify that entry is displayed and played
    # Replace video for the uploaded entries -> Verify that the embed entry in assignment submission isn't replaced
    # Verify that the embed entry (not assignment submission) is replaced
    #================================================================================================================================
    testNum     = "628"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    filePathVideorReplacment = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4'
    vidoeTimeToStop = "0:07"
    vidoeTimeToStopReplacedMedia = '0:14'
    
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
            self.entryName1 = clsTestService.addGuidToString("Embed_Assignment_submission_entry", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Embed_Not_assignment_submission_entry", self.testNum)
            self.galleryName = "New1"
            self.activityName1 = clsTestService.addGuidToString("Embed - Assignment submission", self.testNum)
            self.activityName2 = clsTestService.addGuidToString("Embed - Not assignment submission", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            if LOCAL_SETTINGS_ENV_NAME == 'ProdNewUI':
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = 'https://1820181-1.kaf.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'Blackboard@kaltura.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
            else: # testing 
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = 'https://2104601-5.kaftest.dev.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'Freetrail@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
            
            writeToLog("INFO","Step 1: Going to enable assignment submission")          
            if self.common.admin.enableDisabledAssignmentSubmission(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to enable assignment submission")
                return              
               
            writeToLog("INFO","Step 2: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return 
               
            writeToLog("INFO","Step 3: Going to to navigate to entry page")    
            if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate entry page")
                return 
               
            writeToLog("INFO","Step 4: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to wait until media end upload process")
                return
             
            writeToLog("INFO","Step 5: Going to create assignment submission - from My media")    
            if self.common.moodle.createEmbedActivity(self.entryName1, self.activityName1, isAssignmentEnable=True, submitAssignment=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to create assignment submission - from My media")
                return     
             
            writeToLog("INFO","Step 6: Going to verify embed assignment submission")    
            if self.common.kafGeneric.verifyEmbedEntry(self.activityName1, '', self.vidoeTimeToStop, application=enums.Application.MOODLE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify embed assignment submission")
                return 
             
            writeToLog("INFO","Step 7: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName2, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to upload entry")
                return 
             
            writeToLog("INFO","Step 8: Going to to navigate to entry page")    
            if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate entry page")
                return 
             
            writeToLog("INFO","Step 9: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to wait until media end upload process")
                return
             
            writeToLog("INFO","Step 10: Going to publish entry to gallery")    
            if self.common.myMedia.publishSingleEntry(self.entryName2, '', '', [self.galleryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to publish entry to gallery")
                return    
             
            writeToLog("INFO","Step 11: Going to create embed, not assignment submission - from media gallery")    
            if self.common.moodle.createEmbedActivity(self.entryName2, self.activityName2, embedFrom=enums.Location.MEDIA_GALLARY,chooseMediaGalleryinEmbed=False, mediaGalleryName=self.galleryName, isAssignmentEnable=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to create embed, not assignment submission - from media gallery")
                return     
             
            writeToLog("INFO","Step 12: Going to verify embed assignment submission")    
            if self.common.kafGeneric.verifyEmbedEntry(self.activityName2, '', self.vidoeTimeToStop, application=enums.Application.MOODLE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to verify embed assignment submission")
                return  
             
            writeToLog("INFO","Step 13: Going to navigate to " + self.entryName1 +" edit entry page")    
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to navigate to " + self.entryName1 +" edit entry page")
                return  
             
            writeToLog("INFO","Step 14: Going to replace video for " + self.entryName1)    
            if self.common.editEntryPage.replaceVideo(self.filePathVideorReplacment) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to navigate to " + self.entryName1 +" edit entry page")
                return   
             
            writeToLog("INFO","Step 15: Going to verify that embedded video " + self.entryName1 + " wasn't replaced")    
            if self.common.kafGeneric.verifyEmbedEntry(self.activityName1, '', self.vidoeTimeToStopReplacedMedia, application=enums.Application.MOODLE, activity=enums.MoodleActivities.KALTURA_VIDEO_RESOURCE, forceNavigate=True) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to verify that embedded video " + self.entryName1 + " wasn't replaced")
                return                     
            writeToLog("INFO","Step 15: FAILED as expected")   
            
            writeToLog("INFO","Step 16: Going to navigate to " + self.entryName2 +" edit entry page")    
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to navigate to " + self.entryName2 +" edit entry page")
                return  
            
            writeToLog("INFO","Step 17: Going to replace video for " + self.entryName2)    
            if self.common.editEntryPage.replaceVideo(self.filePathVideorReplacment) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to navigate to " + self.entryName2 +" edit entry page")
                return   
            
            writeToLog("INFO","Step 18: Going to verify embedded video " + self.entryName2 + " was replaced")    
            if self.common.kafGeneric.verifyEmbedEntry(self.activityName2, '', self.vidoeTimeToStopReplacedMedia, application=enums.Application.MOODLE, activity=enums.MoodleActivities.KALTURA_VIDEO_RESOURCE, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to verify embedded video " + self.entryName2 + " was replaced")
                return 
            
            writeToLog("INFO","Step 19: Going to delete embed kaltura video resource " + self.activityName1)    
            if self.common.moodle.deleteEmbedActivity(self.activityName1)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to delete embed kaltura video resource" + self.activityName1)
                return 
            
            writeToLog("INFO","Step 20: Going to delete embed kaltura video resource " + self.activityName2)    
            if self.common.moodle.deleteEmbedActivity(self.activityName2)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to delete embed kaltura video resource" + self.activityName2)
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
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2])
            self.common.moodle.deleteEmbedActivity(self.activityName1)
            self.common.moodle.deleteEmbedActivity(self.activityName2)
            self.common.admin.enableDisabledAssignmentSubmission(False)
            writeToLog("INFO","**************** Ended: teardown_method *******************")                       
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')