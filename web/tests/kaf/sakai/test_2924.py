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
    # @Author: Michal Zomper
    # Test Name : Sakai - Publish from my media (single and multiple)
    # Test description:
    # upload 3 entries (video / audio /image )
    # In my media check one entry and then publish it  - go and check in the published gallery that the entry display
    # In my media check the 2 other entries and publish them to - go and check in the published gallery that the entries display
    #================================================================================================================================
    testNum     = "2924"
    application = enums.Application.SAKAI
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
    galleryName = "New1"
    
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
            self.videoEntryName = clsTestService.addGuidToString("Publish from my media - Video", self.testNum)
            self.audioEntryName = clsTestService.addGuidToString("Publish from my media - Audio", self.testNum)
            self.imageEntryName = clsTestService.addGuidToString("Publish from my media - Image", self.testNum)
            
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
            
            writeToLog("INFO","Step 2: Going to publish single entry from my media")      
            if self.common.myMedia.publishSingleEntry(self.imageEntryName, "", "", [self.galleryName],  publishFrom = enums.Location.MY_MEDIA) == False: 
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to publish single entry from my media")
                return   
                
            writeToLog("INFO","Step 3: Going navigate to gallery page")         
            if self.common.kafGeneric.navigateToGallery(self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to gallery page")
                return  
            
            writeToLog("INFO","Step 4: Going to verify that entry '" + self.imageEntryName + "' display in gallery")
            if self.common.channel.searchEntryInChannel(self.imageEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED verify that entry '" + self.imageEntryName + "' display in gallery")
                return 
              
            writeToLog("INFO","Step 5: Going to publish multiple entries to gallery")
            if self.common.myMedia.publishEntriesFromMyMedia([self.videoEntryName, self.audioEntryName], '', '', [self.galleryName], showAllEntries=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to publish multiple entries to gallery")
                return  
             
            writeToLog("INFO","Step 6: Going navigate to gallery page")         
            if self.common.kafGeneric.navigateToGallery(self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate to gallery page")
                return  
            
            writeToLog("INFO","Step 7: Going to verify that entry '" + self.audioEntryName + "' display in gallery")
            if self.common.channel.searchEntryInChannel(self.audioEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED verify that entry '" + self.audioEntryName + "' display in gallery")
                return 
            
            writeToLog("INFO","Step 8: Going to clear search bar in gallery")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to clear search bar in gallery")
                return 
                
            writeToLog("INFO","Step 9: Going to verify that entry '" + self.videoEntryName + "' display in gallery")
            if self.common.channel.searchEntryInChannel(self.videoEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED verify that entry '" + self.videoEntryName + "' display in gallery")
                return 
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Sakai - Publish from my media (single and multiple)' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteEntriesFromMyMedia([self.videoEntryName, self.audioEntryName, self.imageEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')