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
    # Test Name : Moodle - Trim video
    # Test description:
    # Upload entry
    # Open kea and trim entry - > verify that entry was trimmed
    #================================================================================================================================
    testNum     = "2125"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
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
            self.videoEntryName = clsTestService.addGuidToString("Upload media - Video", self.testNum)
            expectedEntryDuration = "00:20"
        
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
#             writeToLog("INFO","Step 1: Going to upload entry - to be trimmed")  
#             if self.common.upload.uploadEntry(self.filePathVideo, self.videoEntryName, self.description, self.tags) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to upload entry")
#                 return
#             
#             writeToLog("INFO","Step 2: Going to to navigate to entry page")    
#             if self.common.upload.navigateToEntryPageFromUploadPage(self.videoEntryName) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED to navigate entry page")
#                 return            
#                
#             writeToLog("INFO","Step 3: Going to to wait until media end upload process")    
#             if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED to wait until media end upload process")
#                 return            
            
            writeToLog("INFO","Step 2: Going to trim the entry from 30sec to 20sec")  
            if self.common.kea.trimEntry('9C164333-2125-Upload media - Video', "00:10", "00:20", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to trim the entry from 30sec to 20sec")
                return

            writeToLog("INFO","Step 3: Going to collect the new entry's QR codes")  
            self.captionList = self.common.player.collectQrTimestampsFromPlayer(self.videoEntryName)
            if  self.captionList == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to collect the new entry's QR codes")
                return
            
            self.isExist = ["5", "7", "22", "28"];
            self.isAbsent = ["12", "13", "15", "17"];
            writeToLog("INFO","Step 4: Going to verify the entry duration (using QR codes)")  
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.QR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify the entry duration (using QR codes)")
                return                     
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - Trim video' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.videoEntryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")               
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')