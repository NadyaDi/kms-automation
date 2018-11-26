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
    # Test Name : Add Remove Featured Media Module
    # Test description:
    # Go to course page -> enable featured media -> go to media gallery - > upload video entry -> Click on 'featured media' icon
    # Go to course page > Check that entry is displayed under featured media
    # Go to media gallery -> Click on 'Featured media' icon again -> Go to course page -> Verify that entry isn't displayed under featured media
    # Go to course page -> disable featured media -> Make sure that 'featured' media isn't displayed anymore
    #================================================================================================================================
    testNum     = "114"
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
    module = "Featured Media Gallery"
    moduleId = "_158_1"
    
    
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
            
#             writeToLog("INFO","Step 1: Going to enable featured media in media gallery")  
#             if self.common.blackBoard.enableDisableCourseModule(self.galleryName, self.module, self.moduleId)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to enable featured media in media gallery")
#                 return 
#             
#             writeToLog("INFO","Step 2: Going to add new media to media gallery")  
#             if self.common.kafGeneric.addNewContentToGallery(self.galleryName, self.uploadEntrieList, isGalleryModerate=False)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED to add new media to media gallery")
#                 return 
            
            writeToLog("INFO","Step 3: Going to navigate media gallery")  
            if self.common.kafGeneric.navigateToGallery(self.galleryName)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate media gallery")
                return 
            
            writeToLog("INFO","Step 4: Going to click on entry's featured media icon")  
            if self.common.blackBoard.clickOnFeaturedMediaIcon(self.entryName)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to click on entry's featured media icon")
                return                   
            
                     
            
            
            
#             writeToLog("INFO","Step 1: Going to enable featured media in media gallery")  
#             if self.common.blackBoard.enableDisableCourseModule(self.galleryName, self.module, self.moduleId, False, False)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to enable featured media in media gallery")
#                 return                          
            
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
#            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')