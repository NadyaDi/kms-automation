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
    # Test Name : Jive - Embed media in document - v3
    # Test description:
    # upload media -> Click on 'Create' and choose 'Document' -> Click on wysisyg -> Choose media from My media tab -> Save emebed
    # Verify that embed is displayed and played
    #================================================================================================================================
    testNum     = "2512"
    application = enums.Application.JIVE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    entryName = None
    description = "Description" 
    tags = "Tags,"
    documentName = None
    timeToStop = "0:07"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'

    
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
            self.entryName = clsTestService.addGuidToString("EmbedDocumentFromMyMediaV3", self.testNum)
            self.documentName = clsTestService.addGuidToString("Embed document from My Media v3", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            if LOCAL_SETTINGS_ENV_NAME != 'ProdNewUI':
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = 'https://1765561-3.kaftest.dev.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'liatv21@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
            else: # testing 
                localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = 'https://1665211-1.kaf.kaltura.com/admin'
                localSettings.LOCAL_SETTINGS_ADMIN_USERNAME = 'liat@mailinator.com'
                localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD = 'Kaltura1!'
                
            writeToLog("INFO","Step 1: Going to set enableNewBSEUI to v3")    
            if self.common.admin.enableNewBSEUI('v3') == False:
                writeToLog("INFO","Step 1: FAILED to set enableNewBSEUI to v3")
                return
                             
            writeToLog("INFO","Step 2: Going to upload entry")   
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return
                        
            writeToLog("INFO","Step 3: Going navigate to edit entry page")    
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 3: FAILED navigate to edit entry '" + self.entryName + "' page")
                return 
                    
            writeToLog("INFO","Step 4: Going to to navigate to entry page")    
            if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName) == False:
                writeToLog("INFO","Step 4: FAILED to navigate entry page")
                return
                    
            writeToLog("INFO","Step 5: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 5: FAILED to wait until media end upload process")
                return  
              
            writeToLog("INFO","Step 6: Going to to create embed document")    
            if self.common.jive.createEmbedMedia(self.documentName, self.entryName, isDiscussion=False, isDocument=True) == False:
                writeToLog("INFO","Step 6: FAILED to create embed document")
                return
             
            writeToLog("INFO","Step 7: Going to to verify embed document")    
            if self.common.jive.verifyEmbedMedia(self.documentName, '', self.timeToStop) == False:
                writeToLog("INFO","Step 7: FAILED to verify embed document")
                return 
            
#             writeToLog("INFO","Step 7: Going to to delete embed document")    
#             if self.common.jive.deleteEmbedMedia('2565D2ED-2512-Embed video from My Media') == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 7: FAILED to delete embed document")
#                 return                                                                     
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Jive - Embed media (v3) in document from My Media ' was done successfully")
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