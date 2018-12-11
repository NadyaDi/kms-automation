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
    # Test Name : Embed Media As Standalone From Kaltura media
    # Test description:
    # Go to course page -> Click content -> click build content - > click kaltura media -> 
    # select media from media gallery > click embed -> make sure embed was created and successfully played
    # Make the same steps for media gallery
    #================================================================================================================================
    testNum     = "109"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    galleryName = "New1"
    module = "embed media from wysiwyg"
    itemNameEmbedMediaGallery = None
    delay = "0:08"
    
    
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
            self.entryName = clsTestService.addGuidToString("embed entry", self.testNum)  
            self.entryToUpload = UploadEntry(self.filePath, self.entryName, self.description, self.tags, timeout=60, retries=3)
            self.uploadEntrieList = [self.entryToUpload] 
            self.itemNameEmbedMediaGallery = clsTestService.addGuidToString("Embed from media gallery page", self.testNum) 
            ######################### TEST STEPS - MAIN FLOW #######################
 
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
            if self.common.kafGeneric.addMediaToGallery(self.galleryName, self.entryName, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to publish entry to gallery")
                return

            writeToLog("INFO","Step 5: Going to create embed kaltura media from media gallery")  
            if self.common.blackBoard.createEmbedKalturaMedia(self.galleryName, self.entryName, self.itemNameEmbedMediaGallery, '', '0:08')== False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to create embed kaltura media from media gallery")
                return   
            
            writeToLog("INFO","Step 6: Going to create embed kaltura media from media gallery")  
            if self.common.kafGeneric.verifyEmbedEntry('', '0:08')== False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to create embed kaltura media from media gallery")
                return              
            
            writeToLog("INFO","Step 7: Going to delete embed content from media gallery")  
            if self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedMediaGallery) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to delete embed content from my media")
                return                      
            
            #########################################################################
            writeToLog("INFO","TEST PASSED: Create embed kaltura media from media gallery page was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedMediaGallery)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')