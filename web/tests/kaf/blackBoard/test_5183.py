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
    # Test Name : Embed Media As Standalone From Wysiwyg - v2
    # Test description:
    # Go to course page -> Click content -> click build content - > click create and choose item -> Click on wysiwyg -> mashups -> kaltura mesdia
    # select media from my media > click embed -> make sure embed was created and successfuly played
    # Make the same steps for media gallery
    #================================================================================================================================
    testNum     = "5183"
    application = enums.Application.BLACK_BOARD
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    # Test variables
    entryName = None
    description = "Description"
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    galleryName = "New1"
    module = "embed media from wysiwyg"
    itemNameEmbedMyMedia = None
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
            self.entryName = clsTestService.addGuidToString("embedEntryV2", self.testNum)  
            self.itemNameEmbedMyMedia = clsTestService.addGuidToString("EmbedFromMyMediaV2", self.testNum)   
            ######################### TEST STEPS - MAIN FLOW #######################
            if LOCAL_SETTINGS_ENV_NAME != 'ProdNewUI':
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = ' https://1765561-2.kaftest.dev.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'liatv21@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
            else: # testing 
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = ' https://1850231.kaf.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'michal11@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
                
            writeToLog("INFO","Step 1: Going to set enableNewBSEUI to v2")    
            if self.common.admin.enableNewBSEUI('v2') == False:
                writeToLog("INFO","Step 1: FAILED to set enableNewBSEUI to v2")
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
 
            writeToLog("INFO","Step 5: Going to create embed entry from my media")  
            if self.common.blackBoard.createEmbedItem(self.galleryName, self.entryName, self.itemNameEmbedMyMedia,v3=False) == False:
                writeToLog("INFO","Step 5: FAILED to create embed entry from my media")
                return
            
            writeToLog("INFO","Step 6: Going to verify embed media")  
            if self.common.kafGeneric.verifyEmbedEntry(self.itemNameEmbedMyMedia, '', self.delay) == False:
                writeToLog("INFO","Step 6: FAILED to verify embed media")
                return            
            
            writeToLog("INFO","Step 7: Going to delete embed content from my media")  
            if self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedMyMedia) == False:
                writeToLog("INFO","Step 7: FAILED to delete embed content from my media")
                return                         
            
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Create embed media (v2) from my media page was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.blackBoard.deleteEmbedItem(self.galleryName, 'Delete', self.itemNameEmbedMyMedia)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')