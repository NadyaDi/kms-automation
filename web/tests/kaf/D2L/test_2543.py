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
    # Test Name : D2L - Preview all kinds of media from My Media and Gallery
    # Test description:
    # upload 3 entries : video / Audio / Image
    # Navigate to each entry page and verify player is working  and that the video / audio / image  is correct
    #================================================================================================================================
    testNum     = "2543"
    application = enums.Application.D2L
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
    videoQrCodeResult = "7"
    ImageQrCodeResult = "4"
    vidoeLength = "0:10"
    audioLength = "0:30"
    vidoeTimeToStop = "0:07"
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
            self.videoEntryName1 = clsTestService.addGuidToString("Upload media and verify in player - Video1", self.testNum)
            self.videoEntryName2 = clsTestService.addGuidToString("Upload media and verify in player - Video2", self.testNum)
            self.audioEntryName = clsTestService.addGuidToString("Upload media and verify in player - Audio", self.testNum)
            self.imageEntryName = clsTestService.addGuidToString("Upload media and verify in player - Image", self.testNum)
            
            self.entriesToUpload = {
            self.videoEntryName1: self.filePathVideo,
            self.videoEntryName2: self.filePathVideo, 
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
                       
                       
            writeToLog("INFO","Step 3: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.IMAGE, "", "", self.ImageQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to verify the entry '" + self.imageEntryName + "' in player")
                return   
                   
            writeToLog("INFO","Step 4: Going navigate to audio entry: "+ self.audioEntryName)    
            if self.common.entryPage.navigateToEntry(self.audioEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to entry: " + self.audioEntryName)
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
          
            writeToLog("INFO","Step 7: Going navigate to video entry: "+ self.videoEntryName1)    
            if self.common.entryPage.navigateToEntry(self.videoEntryName1, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED navigate to entry: " + self.videoEntryName1)
                return 
                         
            writeToLog("INFO","Step 8: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED - New entry is still processing")
                return 
                   
            writeToLog("INFO","Step 9: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.VIDEO, self.vidoeLength, self.vidoeTimeToStop, self.videoQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify the entry '" + self.videoEntryName1 + "' in player")
                return   
                
            writeToLog("INFO","Step 10: Going to publish entries to gallery")
            if self.common.myMedia.publishEntriesFromMyMedia([self.videoEntryName2,self.audioEntryName,self.imageEntryName], '', '', [self.galleryName], showAllEntries=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to publish entries to gallery")
                return  
            
            writeToLog("INFO","Step 11: Going to approve entries in gallery")
            if self.common.kafGeneric.handlePendingEntriesIngallery(self.galleryName, '', [self.videoEntryName2,self.audioEntryName,self.imageEntryName] , navigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to approve entries in gallery")
                return 
            
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 12: Going navigate to Media Gallery NOT using a url navigation")  
            if self.common.base.click(self.common.d2l.D2L_SELECT_COURSES_BUTTON, timeout=20) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to click on 'select Courses' button in the navigation menu")
                return   
            
            if self.common.base.click(self.common.d2l.D2L_SELECT_COURSE_NEW1_BUTTON, timeout=20) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to click on course 'New1' button in courses list")
                return 
            
            if self.common.kafGeneric.switchToKAFIframeGeneric()== False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED switch to D2L iframe")
                return 
            
            if self.common.base.wait_visible(self.common.kafGeneric.KAF_MEDIA_GALLERY_TITLE, timeout=30) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to verify Media Galley page display")
                return 
            
            writeToLog("INFO","Step 13: Going navigate to image entry: '" + self.imageEntryName + "' from gallery page")    
            if self.common.kafGeneric.navigateToEntryPageFromGalleryPage(self.imageEntryName, self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED navigate to entry: " + self.imageEntryName + " from gallery page")
                return 
                 
            writeToLog("INFO","Step 14: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.IMAGE, "", "", self.ImageQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to verify the entry '" + self.imageEntryName + "' in player")
                return   
             
            writeToLog("INFO","Step 15: Going navigate to audio entry: '" + self.audioEntryName + "' from gallery page")    
            if self.common.kafGeneric.navigateToEntryPageFromGalleryPage(self.audioEntryName, self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED navigate to entry: " + self.audioEntryName + " from gallery page")
                return 
             
            writeToLog("INFO","Step 16: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.AUDIO, self.audioLength, "", "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to verify the entry '" + self.audioEntryName + "' in player")
                return   
            
            writeToLog("INFO","Step 17: Going navigate to video entry: '"+ self.videoEntryName2 + "' from gallery page")    
            if self.common.kafGeneric.navigateToEntryPageFromGalleryPage(self.videoEntryName2, self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED navigate to entry: " + self.videoEntryName2 + " from gallery page")
                return 
            sleep(5)
            
            writeToLog("INFO","Step 18: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.VIDEO, self.vidoeLength, self.vidoeTimeToStop, self.videoQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to verify the entry '" + self.videoEntryName2 + "' in player")
                return 
              
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'D2L - Preview all kinds of media from My Media and Gallery' was done successfully")
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