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
    # Test Name : Canvas Embed on BSE from shared repository
    # Test description:
    # Upload entry
    # Go course -> Go to 'Announcements' tab -> Add new announcement -> In announcement, click on wysiwyg and choose media to embed from 'SR'
    # Verify that the embed was created successfully 
    # Verify that the embed was deleted successfully
    #================================================================================================================================
    testNum     = "2295"
    application = enums.Application.CANVAS
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_5.png'
    uploadThumbnailExpectedResult = 5
    galleryName = "Shared Repository"
    sharedRepositoryMetadataValue = "math"
    
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
            self.entryName = clsTestService.addGuidToString("EmbedFromSR", self.testNum)
            self.announcementName = clsTestService.addGuidToString("EmbedAnnouncementFromSR", self.testNum)
            
            ######################### TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == None:
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
            if self.common.canvas.addSharedRepositoryMetadataCanvas(self.entryName, self.sharedRepositoryMetadataValue) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add required metadata fields for SR")
                return 
             
            writeToLog("INFO","Step 5: Going to publish entry to SR")    
            if self.common.myMedia.publishSingleEntry(self.entryName, '', '', [self.galleryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish entry to SR")
                return                                     
             
            writeToLog("INFO","Step 6: Going to to create embed announcement from SR")    
            if self.common.canvas.createEmbedAnnouncements(self.announcementName, self.entryName, embedFrom=enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to create embed announcement from SR")
                return  
             
            writeToLog("INFO","Step 7: Going to to verify embed announcement")    
            if self.common.kafGeneric.verifyEmbedEntry(self.announcementName, self.uploadThumbnailExpectedResult, '', enums.Application.CANVAS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify embed announcement")
                return     
            
            writeToLog("INFO","Step 8: Going to to delete embed announcement")    
            if self.common.canvas.deleteAnnouncemnt(self.announcementName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to delete embed announcement")
                return                                          
            
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Embed on BSE from SR' was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.canvas.deleteAnnouncemnt(self.announcementName, True)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')