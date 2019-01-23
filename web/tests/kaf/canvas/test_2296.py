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
    # Test Name : Canvas - Publish to course galleries from SR
    # Test description:
    # Upload entry -> Edit SR required fields -> Publish entry from my media to SR
    # Go to media gallery > click add media > select SR > select media > publish
    # Verify that entry is displayed in media gallery
    #================================================================================================================================
    testNum     = "2296"
    application = enums.Application.CANVAS
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    sharedRepositoryMetadataValue = "math"
    
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
            self.entryName = clsTestService.addGuidToString("publish entry to SR", self.testNum)
            self.fieldText = "metadata"
            self.gallerySRName = "Shared Repository"
            self.galleryName = "New1"
            
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
             
            writeToLog("INFO","Step 4: Going to add required metadata fields for SR")    
            if self.common.canvas.addSharedRepositoryMetadataCanvas(self.entryName, self.sharedRepositoryMetadataValue) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add required metadata fields for SR")
                return 
             
            writeToLog("INFO","Step 5: Going to publish entry to SR")    
            if self.common.myMedia.publishSingleEntry(self.entryName, '', '', [self.gallerySRName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish entry to SR")
                return  
             
            writeToLog("INFO","Step 6: Going to publish entry :" + self.entryName + " from SR to media gallery")
            if self.common.kafGeneric.addSharedRepositoryMedieToMediaGallery(self.galleryName, [self.entryName]) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to publish entry :" + self.entryName + " from SR to media gallery")
                return     
            
            writeToLog("INFO","Step 7: Going to navigate to " + self.galleryName)
            if self.common.kafGeneric.navigateToGallery(self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to to " + self.galleryName)
                return
            
            self.common.base.click(self.common.kafGeneric.KAF_REFRSH_BUTTON)
            sleep(5)
            
            self.common.canvas.switchToCanvasIframe()
            writeToLog("INFO","Step 8: Going to verify entry '" + self.entryName + " in media gallery")
            if self.common.channel.searchEntryInChannel(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to find entry '" + self.entryName + " in media gallery")
                return                                                
         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Canvas - Publish to course galleries from shared repository' was done successfully")
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