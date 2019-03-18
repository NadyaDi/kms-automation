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
    # Test Name : Upload From Embed As Standalone
    # Test description:
    # Go to course page -> Click content -> Click on bulid content - > click on kaltura media -> upload new media
    # select new media > click embed -> make sure embed was created and successfully played
    # Make the same steps for media gallery
    #================================================================================================================================
    testNum     = "2088"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_5.png'
    galleryName = "New1"
    itemNameEmbedUpload = None
    galleryNameSharedrepository = "Shared Repository"
    SR_RequiredField = "Humanities"
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
            self.entryName = clsTestService.addGuidToString("embedEntry", self.testNum)  
            self.itemNameEmbedUpload = clsTestService.addGuidToString("EmbedFromUploadPage", self.testNum) 
            ######################### TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to create embed item media from upload entry")  
            if self.common.blackBoard.createEmbedItem(self.galleryName, self.entryName, self.itemNameEmbedUpload, embedFrom=enums.Location.UPLOAD_PAGE_EMBED, filePath=self.filePath, description=self.description, tags=self.tags)== False:
                writeToLog("INFO","Step 1: FAILED to create embed item media from upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to verify embed media")  
            if self.common.kafGeneric.verifyEmbedEntry(self.itemNameEmbedUpload, self.uploadThumbnailExpectedResult, '') == False:
                writeToLog("INFO","Step 2: FAILED to verify embed media")
                return               
            
            writeToLog("INFO","Step 3: Going to delete embed content from media gallery")  
            if self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedUpload) == False:
                writeToLog("INFO","Step 3: FAILED to delete embed content from my media")
                return                      
            
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Create embed announcements from SR page was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedUpload)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')