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
    # Test Name : Embed Media From SR - Add New Announcements - v3
    # Test description:
    # Go to course page -> Click content -> click on tools - > click 'More Tools' -> Click 'Announcements'
    # select media from SR > click embed -> make sure embed was created and successfully played
    # Make the same steps for media gallery
    #================================================================================================================================
    testNum     = "113"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_5.png'
    galleryName = "New1"
    itemNameEmbedSharedRepository = None
    delay = "0:08"
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
            self.entryName = clsTestService.addGuidToString("embedEntryV3", self.testNum)  
            self.itemNameEmbedSharedRepository = clsTestService.addGuidToString("EmbedFromSharedRepositoryPageV3", self.testNum) 
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
                        
            writeToLog("INFO","Step 2: Going to add shared repository module")     
            if self.common.blackBoard.addRemoveSharedRepositoryModule(True) == False:
                writeToLog("INFO","Step 2: FAILED to add shared repository module")
                  
            writeToLog("INFO","Step 3: Going to upload entry")   
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                writeToLog("INFO","Step 3: FAILED to upload entry")
                return
              
            writeToLog("INFO","Step 4: Going to completed the required fields order to publish")
            if self.common.blackBoard.addSharedRepositoryMetadata(self.entryName, self.SR_RequiredField) == False:
                writeToLog("INFO","Step 4: FAILED to add required fields")
                return
   
            writeToLog("INFO","Step 5: Going to publish entry from upload page")  
            if self.common.myMedia.publishSingleEntry(self.entryName, "", "", [self.galleryNameSharedrepository], publishFrom = enums.Location.MY_MEDIA, disclaimer=False) == False:
                writeToLog("INFO","Step 5: FAILED to publish entry' " + self.entryName + " to gallery upload page")
                return
             
            writeToLog("INFO","Step 6: Going to create embed kaltura media from media gallery")  
            if self.common.blackBoard.createEmbedAnnouncemnets(self.galleryName, self.entryName, self. itemNameEmbedSharedRepository, self.uploadThumbnailExpectedResult, mediaType=enums.MediaType.IMAGE)== False:
                writeToLog("INFO","Step 6: FAILED to create embed kaltura media from media gallery")
                return 
            
            writeToLog("INFO","Step 7: Going to verify embed media")  
            if self.common.kafGeneric.verifyEmbedEntry(self.itemNameEmbedSharedRepository, self.uploadThumbnailExpectedResult, '') == False:
                writeToLog("INFO","Step 7: FAILED to verify embed media")
                return               
            
            writeToLog("INFO","Step 8: Going to delete embed content from media gallery")  
            if self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedSharedRepository, embedOption=enums.BBContentPageMenusOptions.ANNOUNCEMENTS) == False:
                writeToLog("INFO","Step 8: FAILED to delete embed content from my media")
                return                      
            
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Create embed announcements (v3) from SR page was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedSharedRepository, embedOption=enums.BBContentPageMenusOptions.ANNOUNCEMENTS)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')