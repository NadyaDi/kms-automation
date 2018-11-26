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
    # Test Name : BlackBoard: Adding media to Faculty Repository From My Media
    # Test description:
    # 1. upload 3 entries (image/ video/ audio) - fill in the nested filters
    # 2. publish entries to  Faculty Repository 
    # 3. verify entries was added to Faculty Repository 
    #================================================================================================================================
    testNum     = "222"
    application = enums.Application.BLACK_BOARD
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
    galleryName = "Shared Repository"
    SR_RequiredField = "Humanities"

    
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
            self.videoEntryName = clsTestService.addGuidToString("Publish To SR From My Media - Video", self.testNum)
            self.audioEntryName = clsTestService.addGuidToString("Publish To SR From My Media - Audio", self.testNum)
            self.imageEntryName = clsTestService.addGuidToString("Publish To SR From My Media - Image", self.testNum)
            
            self.entriesToUpload = {
            self.videoEntryName: self.filePathVideo, 
            self.audioEntryName: self.filePathAudio,
            self.imageEntryName: self.filePathImage }

            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to add shared repository module")     
            if self.common.blackBoard.addRemoveSharedRepositoryModule(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to add shared repository module")
             
             
            writeToLog("INFO","Step 2: Going to upload 3 entries: Video / Audio / Image")   
            if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 3 entries")
                return
            
            writeToLog("INFO","Step 3: Going to publish multiple entries to shared repository")
            if self.common.myMedia.publishEntriesFromMyMedia([self.videoEntryName, self.audioEntryName, self.imageEntryName], '', '', [self.galleryName], showAllEntries=True) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED entries were publish to shared repository although the entries doesn't completed the required fields in order to publish to shared repository")
                return
            writeToLog("INFO","Step 3: preview step failed as expected - entries completed the required fields in order to publish to shared repository")
            
            writeToLog("INFO","Step 4: Going to verify that message to completed the required fields in order to publish is display") 
            if self.common.base.wait_visible(self.common.blackBoard.BB_SHARED_REPOSITORY_DISCLAIMER_MSG_BEFOR_PUBLISH) == False:
                writeToLog("INFO","Step 4: FAILED, shared repository alert (before publish) massage don't display")
                return False
            
            writeToLog("INFO","Step 5: Going to completed the required fields in entry '" + self.imageEntryName + "' order to publish")
            if self.common.blackBoard.addSharedRepositoryMetadata(self.imageEntryName, self.SR_RequiredField) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add required fields to entry '" + self.imageEntryName)
                return
             
            writeToLog("INFO","Step 6: Going to completed the required fields in entry '" + self.audioEntryName + "' order to publish")
            if self.common.blackBoard.addSharedRepositoryMetadata(self.audioEntryName, self.SR_RequiredField) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to add required fields to entry '" + self.audioEntryName)
                return
            
            writeToLog("INFO","Step 7: Going to completed the required fields in entry '" + self.videoEntryName + "' order to publish")
            if self.common.blackBoard.addSharedRepositoryMetadata(self.videoEntryName, self.SR_RequiredField) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to add required fields to entry '" + self.videoEntryName)
                return
            
            writeToLog("INFO","Step 8: Going to publish multiple entries to shared repository")
            if self.common.myMedia.publishEntriesFromMyMedia([self.videoEntryName, self.audioEntryName, self.imageEntryName], '', '', [self.galleryName], showAllEntries=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to publish entries to shared repository")
                return
            
            writeToLog("INFO","Step 9: Going navigate to shared repository gallery")
            if self.common.blackBoard.navigateToSharedRepositoryInBB() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED navigate to shared repository gallery")
                return
            
            writeToLog("INFO","Step 10: Going to verify entry '" + self.imageEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.imageEntryName) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to find entry '" + self.imageEntryName + "' shared repository gallery")
                return
            
            writeToLog("INFO","Step 11: Going to clear search textbox")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to clear search textbox")
                return
        
            writeToLog("INFO","Step 12: Going to verify entry '" + self.audioEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.audioEntryName) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to find entry '" + self.audioEntryName + "' shared repository gallery")
                return
            
            writeToLog("INFO","Step 13: Going to clear search textbox")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to clear search textbox")
                return
            
            writeToLog("INFO","Step 14: Going to verify entry '" + self.videoEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.videoEntryName) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to find entry '" + self.videoEntryName + "' shared repository gallery")
                return
            
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'BlackBoard: Adding media to Faculty Repository From My Media' was done successfully")
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