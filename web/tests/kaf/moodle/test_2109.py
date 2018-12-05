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
    # Test Name : Moodle - Preview all kinds of media from My Media and Gallery
    # Test description:
    # upload 3 entries : video / Audio / Image
    # Navigate to each entry page and verify player is working  and that the video / audio / image  is correct
    #================================================================================================================================
    testNum     = "2109"
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
             
            writeToLog("INFO","Step 2: Going navigate to My Media not using a url navigation")  
            if self.common.base.wait_visible(self.common.moodle.MOODLE_MY_MEDIA_BUTTON_IN_NAVIGATION_MENU, timeout=10) == False:
                writeToLog("INFO", "Site home isn't open and need to open it")
                if self.common.base.click(self.common.moodle.MOODLE_SITE_HOME_BUTTON) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 2: FAILED to click on site home button in the navigation menu")
                    return

            #click on My Media button        
            if self.common.base.click(self.common.moodle.MOODLE_MY_MEDIA_BUTTON_IN_NAVIGATION_MENU, multipleElements=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to click on site home button in the navigation menu")
                return
                       
            if self.common.base.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 30) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED verify My Media page URL")
                return 
             
            self.common.base.wait_visible(self.common.myMedia.MY_MEDIA_ACTIONS_BUTTON)
            if self.common.kafGeneric.switchToKAFIframeGeneric()== False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED switch to moodle iframe")
                return  
             
            writeToLog("INFO","Step 3: Going navigate to image entry: "+ self.imageEntryName)    
            if self.common.entryPage.navigateToEntry(self.imageEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to entry: " + self.imageEntryName)
                return
                    
            writeToLog("INFO","Step 4: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.IMAGE, "", "", self.ImageQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify the entry '" + self.imageEntryName + "' in player")
                return   
                
            writeToLog("INFO","Step 5: Going navigate to audio entry: "+ self.audioEntryName)    
            if self.common.entryPage.navigateToEntry(self.audioEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to entry: " + self.audioEntryName)
                return 
                            
            writeToLog("INFO","Step 6: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED - New entry is still processing")
                return 
                
            writeToLog("INFO","Step 7: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.AUDIO, self.audioLength, "", "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify the entry '" + self.audioEntryName + "' in player")
                return   
       
            writeToLog("INFO","Step 8: Going navigate to video entry: "+ self.videoEntryName1)    
            if self.common.entryPage.navigateToEntry(self.videoEntryName1, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to entry: " + self.videoEntryName1)
                return 
                      
            writeToLog("INFO","Step 9: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED - New entry is still processing")
                return 
                
            writeToLog("INFO","Step 10: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.VIDEO, self.vidoeLength, self.vidoeTimeToStop, self.videoQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to verify the entry '" + self.videoEntryName1 + "' in player")
                return   
               
            writeToLog("INFO","Step 11: Going to publish entries to gallery")
            if self.common.myMedia.publishEntriesFromMyMedia([self.videoEntryName2,self.audioEntryName,self.imageEntryName], '', '', [self.galleryName], showAllEntries=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to publish entries to gallery")
                return  
            
            writeToLog("INFO","Step 12: Going navigate to Media Gallery not using a url navigation")  
            if self.common.base.wait_visible(self.common.moodle.MOODLE_MEDIA_GALLERY_BUTTON_IN_NAVIGATION_MENU, timeout=10) == False:
                writeToLog("INFO", "My Courses isn't open and need to open it")
             
                #click on course button        
                if self.common.base.click(self.common.moodle.MOODLE_COURSE_BUTTON_IN_MENU_BAR) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 12: FAILED to click on course 'New1' button in the navigation menu")
                    return
                
            #click on Media gallery button        
            if self.common.base.click(self.common.moodle.MOODLE_MEDIA_GALLERY_BUTTON_IN_NAVIGATION_MENU) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to click on media gallery button in the navigation menu")
                return
            
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_GALLERY_NEW1_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED verify Media Gallery page URL")
                return 
            
            self.common.base.wait_visible(self.common.channel.CHANNEL_ACTION_BUTTON)
            if self.common.kafGeneric.switchToKAFIframeGeneric()== False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED switch to moodle iframe")
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
            writeToLog("INFO","TEST PASSED: 'Moodle - Preview all kinds of media from My Media and Gallery' was done successfully")
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