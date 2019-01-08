import sys,os
from enums import Location
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
    # Test Name : Canvas: Embed on BSE from upload
    # Test description:
    # Upload entry
    # Go course -> Go to 'Announcements' tab -> Add new announcement -> In announcement, click on wysiwyg and choose media to embed from upload page
    # Verify that the embed was created successfully 
    # Verify that the embed was deleted successfully
    #================================================================================================================================
    testNum     = "2310"
    application = enums.Application.CANVAS
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
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Embed from upload", self.testNum)
            self.announcementName = clsTestService.addGuidToString("Embed announcement from upload", self.testNum)
            
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to to create embed announcement from upload")    
            if self.common.canvas.createEmbedAnnouncements(self.announcementName, self.entryName, embedFrom=Location.UPLOAD_PAGE_EMBED, filePath=self.filePath, description=self.description, tags=self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create embed announcement from upload")
                return  
             
            writeToLog("INFO","Step 2: Going to to verify embed announcement")    
            if self.common.kafGeneric.verifyEmbedEntry(self.announcementName, self.uploadThumbnailExpectedResult, '', enums.Application.CANVAS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify embed announcement")
                return     
            
            writeToLog("INFO","Step 3: Going to to delete embed announcement")    
            if self.common.canvas.deleteAnnouncemnt(self.announcementName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to delete embed announcement")
                return                                          
            
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Embed on BSE from upload page' was done successfully")
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