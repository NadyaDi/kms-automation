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
    # Test Name : Blackboard ultra- Upload media from desktop
    # Test description:
    # Test description:
    # upload 3 entries : video / Audio / Image
    # Navigate to each entry page and verify player is working 
    #================================================================================================================================
    testNum     = "4872"
    application = enums.Application.BLACKBOARD_ULTRA
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    
    status = "Pass"
    timeout_accured = "False"
    # Test variables
    videoEntryName = None
    audioEntryName = None
    imageEntryName = None
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\audio.mp3'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    videoQrCodeResult = "7"
    ImageQrCodeResult = "4"
    vidoeLength = "0:10"
    audioLength = "0:30"
    vidoeTimeToStop = "0:07"
    categoryName = None

    
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
                    
            writeToLog("INFO","Step 2: Going navigate to image entry: "+ self.imageEntryName)    
            if self.common.entryPage.navigateToEntry(self.imageEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to entry: " + self.imageEntryName)
                return 
                
            writeToLog("INFO","Step 3: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.IMAGE, "", "", self.ImageQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to verify the entry '" + self.imageEntryName + "' in player")
                return   
            
            writeToLog("INFO","Step 4: Going navigate to audio entry: "+ self.audioEntryName)    
            if self.common.entryPage.navigateToEntry(self.audioEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 47: FAILED navigate to entry: " + self.audioEntryName)
                return 
                        
            writeToLog("INFO","Step 5: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED - New entry is still processing")
                return 
            
            writeToLog("INFO","Step 6: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.AUDIO, self.audioLength, "", "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify the entry '" + self.audioEntryName + "' in player")
                return   
   
            writeToLog("INFO","Step 7: Going navigate to video entry: "+ self.videoEntryName)    
            if self.common.entryPage.navigateToEntry(self.videoEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED navigate to entry: " + self.videoEntryName)
                return 
                  
            writeToLog("INFO","Step 8: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED - New entry is still processing")
                return 
            
            writeToLog("INFO","Step 9: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.VIDEO, self.vidoeLength, self.vidoeTimeToStop, self.videoQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify the entry '" + self.videoEntryName + "' in player")
                return   
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Blackboard - Upload media from desktop and verify player' was done successfully")
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