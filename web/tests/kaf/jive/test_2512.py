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
    # Test Name : Jive - Embed media in document
    # Test description:
    # upload media -> Click on 'Create' and choose 'Document' -> Click on wysisyg -> Choose media from My media tab -> Save emebed
    # Verify that embed is displayed and played
    #================================================================================================================================
    testNum     = "2512"
    application = enums.Application.JIVE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
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
            self.entryName = clsTestService.addGuidToString("EmbedFromMyMedia", self.testNum)
            self.documentName = clsTestService.addGuidToString("Embed video from My Media", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
                 
#             writeToLog("INFO","Step 1: Going to upload entry")   
#             if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to upload entry")
#                 return
#                       
#             writeToLog("INFO","Step 2: Going navigate to edit entry page")    
#             if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED navigate to edit entry '" + self.entryName + "' page")
#                 return 
#                   
#             writeToLog("INFO","Step 3: Going to to navigate to entry page")    
#             if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED to navigate entry page")
#                 return
#                   
#             writeToLog("INFO","Step 4: Going to to wait until media end upload process")    
#             if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 4: FAILED to wait until media end upload process")
#                 return  
            
            writeToLog("INFO","Step 5: Going to to create embed document")    
            if self.common.jive.createEmbedMedia(self.documentName, 'AutomatedBenefits.jpg', isDiscussion=False, isDocument=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to create embed document")
                return              
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Jive - Embed media in document from My Media ' was done successfully")
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