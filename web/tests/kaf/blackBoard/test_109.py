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
    # Test Name : Embed Media As Standalone From Kaltura media - v2
    # Test description:
    # Go to course page -> Click content -> click build content - > click kaltura media -> 
    # select media from media gallery > click embed -> make sure embed was created and successfully played
    # Make the same steps for media gallery
    #================================================================================================================================
    testNum     = "109"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    # Test variables
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    galleryName = "New1"
    module = "embed media from wysiwyg"
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
            self.entryName = clsTestService.addGuidToString("embedEntryV3", self.testNum)  
            self.entryToUpload = UploadEntry(self.filePath, self.entryName, self.description, self.tags, timeout=60, retries=3)
            self.uploadEntrieList = [self.entryToUpload] 
            self.itemNameEmbedMediaGallery = clsTestService.addGuidToString("EmbedFromMediaGalleryV3", self.testNum) 
            
            ######################### TEST STEPS - MAIN FLOW #######################
            if LOCAL_SETTINGS_ENV_NAME != 'ProdNewUI':
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = ' https://1765561-2.kaftest.dev.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'liatv21@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
            else: # testing 
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = ' https://1850231.kaf.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'michal11@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
                
            writeToLog("INFO","Step 1: Going to set enableNewBSEUI to v3")    
            if self.common.admin.enableNewBSEUI('v3') == False:
                writeToLog("INFO","Step 1: FAILED to set enableNewBSEUI to v3")
                return
                        
            writeToLog("INFO","Step 2: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return
              
            writeToLog("INFO","Step 3: Going to to navigate to entry page")    
            if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName) == False:
                writeToLog("INFO","Step 3: FAILED to navigate entry page")
                return
              
            writeToLog("INFO","Step 4: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 4: FAILED to wait until media end upload process")
                return
              
            writeToLog("INFO","Step 5: Going to PUBLISH entry to gallery")    
            if self.common.kafGeneric.addMediaToGallery(self.galleryName, self.entryName, False) == False:
                writeToLog("INFO","Step 5: FAILED to PUBLISH entry to gallery")
                return
 
            writeToLog("INFO","Step 6: Going to CREATE embed kaltura media from media gallery")  
            if self.common.blackBoard.createEmbedKalturaMedia(self.galleryName, self.entryName, self.itemNameEmbedMediaGallery)== False:
                writeToLog("INFO","Step 6: FAILED to CREATE embed kaltura media from media gallery")
                return   
            
            writeToLog("INFO","Step 7: Going to VERIFY embed kaltura media from media gallery")  
            if self.common.kafGeneric.verifyEmbedEntry(self.itemNameEmbedMediaGallery,'', '0:08')== False:
                writeToLog("INFO","Step 7: FAILED to VERIFY embed kaltura media from media gallery")
                return              
            
            writeToLog("INFO","Step 8: Going to DELETE embed content from media gallery")  
            if self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedMediaGallery) == False:
                writeToLog("INFO","Step 8: FAILED to DELETE embed content from my media")
                return                      
            
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Create embed kaltura (v3) media from media gallery page was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.kafGeneric.switchToKAFIframeGeneric()
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