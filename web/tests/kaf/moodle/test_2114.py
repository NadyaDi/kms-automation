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
    # Test Name : Moodle - Search Media (by entry name)
    # Test description:
    # Upload 3 entries (video/audio/image) -> Go to 'My Media' and search for each of the entries
    #================================================================================================================================
    testNum     = "2114"
    application = enums.Application.MOODLE
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    videoEntryName = None
    audioEntryName = None
    imageEntryName = None
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\audio.mp3'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    galleryName = 'New1'
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
            self.videoEntryName = clsTestService.addGuidToString("Upload media and verify in player - Video", self.testNum)
            self.audioEntryName = clsTestService.addGuidToString("Upload media and verify in player - Audio", self.testNum)
            self.imageEntryName = clsTestService.addGuidToString("Upload media and verify in player - Image", self.testNum)
            
            self.entriesToUpload = {
            self.videoEntryName: self.filePathVideo,
            self.audioEntryName: self.filePathAudio,
            self.imageEntryName: self.filePathImage }
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload 3 entries: Video / Audio / Image")   
            if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 3 entries")
                return    
            
            writeToLog("INFO","Step 2: Going to search for " + self.videoEntryName)   
            if self.common.myMedia.searchEntryMyMedia(self.videoEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to search for " + self.videoEntryName)
                return       
                     
            writeToLog("INFO","Step 3: Going to clear search")   
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to clear search")
                return 
            
            writeToLog("INFO","Step 4: Going to search for " + self.imageEntryName)   
            if self.common.myMedia.searchEntryMyMedia(self.imageEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to search for " + self.imageEntryName)
                return       
                     
            writeToLog("INFO","Step 5: Going to clear search")   
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to clear search")
                return     
            
            writeToLog("INFO","Step 6: Going to search for " + self.audioEntryName)   
            if self.common.myMedia.searchEntryMyMedia(self.audioEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to search for " + self.audioEntryName)
                return                                         
         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Moodle - Search Media (by entry name)' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")  
            self.common.myMedia.deleteEntriesFromMyMedia([self.videoEntryName1, self.videoEntryName2,  self.audioEntryName, self.imageEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')