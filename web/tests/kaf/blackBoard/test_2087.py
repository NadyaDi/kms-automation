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
    # Test Name : Embed Media As Standalone From Wysiwyg
    # Test description:
    # Go to course page -> Click content -> click build content - > click create and choose item -> Click on wysiwyg -> mashups -> kaltura mesdia
    # select media from my media > click embed -> make sure embed was created and successfuly played
    # Make the same steps for media gallery
    #================================================================================================================================
    testNum     = "2087"
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
            self.entryName = clsTestService.addGuidToString("feature media entry", self.testNum)  
            self.entryToUpload = UploadEntry(self.filePath, self.entryName, self.description, self.tags, timeout=60, retries=3)
            self.uploadEntrieList = [self.entryToUpload] 
            
            ######################### TEST STEPS - MAIN FLOW #######################
 
#             writeToLog("INFO","Step 1: Going to add new media to media gallery")  
#             if self.common.kafGeneric.addNewContentToGallery(self.galleryName, self.uploadEntrieList, isGalleryModerate=False)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to add new media to media gallery")
#                 return 
            
            writeToLog("INFO","Step 2: Going to create embed entry")  
            if self.common.blackBoard.createEmbedItem(self.galleryName, 'qrcode_middle_4.png')== False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create embed entry")
                return            
            
            #########################################################################
            writeToLog("INFO","TEST PASSED: Add new media to media gallery was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')