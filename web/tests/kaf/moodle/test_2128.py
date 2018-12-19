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
    # Test Name : Moodle - Embed video resource from SR
    # Test description:
    # Upload entry -> Go to course -> Turn editing on -> Add an activity or resource -> Choose kalture video resource -< Fill name
    # Select video from SR -> Embed -> Verify that entry was embedded and played
    #================================================================================================================================
    testNum     = "2128"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    vidoeTimeToStop = "0:08"
    
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
            self.entryName = clsTestService.addGuidToString("Embed kaltura video resource from SR - video", self.testNum)
            self.activityTitle = clsTestService.addGuidToString("Embed kaltura video resource", self.testNum)
            self.fieldText = "metadata"
            self.galleryName = "Shared Repository"
            ##################### TEST STEPS - MAIN FLOW ##################### 
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
            
            writeToLog("INFO","Step 4: Going to to add required metadata fields for SR")    
            if self.common.moodle.addSharedRepositoryMetadataMoodle(self.entryName, self.fieldText) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add required metadata fields for SR")
                return 
            
            writeToLog("INFO","Step 5: Going to publish entry to SR")    
            if self.common.myMedia.publishSingleEntry(self.entryName, '', '', [self.galleryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish entry to SR")
                return                                     
              
            writeToLog("INFO","Step 6: Going to create embed video resource from 'SR'")    
            if self.common.moodle.createEmbedActivity(self.entryName, self.activityTitle, embedFrom=enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to create embed video resource from 'SR'")
                return 
             
            writeToLog("INFO","Step 7: Going to verify embed kaltura video resource")    
            if self.common.kafGeneric.verifyEmbedEntry(self.activityTitle, '', self.vidoeTimeToStop, application=enums.Application.MOODLE, activity=enums.MoodleActivities.KALTURA_VIDEO_RESOURCE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify embed kaltura video resource")
                return  
            
            writeToLog("INFO","Step 8: Going to delete embed kaltura video resource")    
            if self.common.moodle.deleteEmbedActivity(self.activityTitle)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to delete embed kaltura video resource")
                return 
                                                                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - Embed video resource from SR' was done successfully")
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