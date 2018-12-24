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
    # Test Name : BlackBoard: Upload new media to Faculty Repository and then publish entries to course
    # Test description:
    # 1. upload 3 entries (image/ video/ audio) to Faculty Repository - fill in the nested filters
    # 2. publish entries to course
    # 3. verify entries was added to the course
    #================================================================================================================================
    testNum     = "1648"
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
    sharedRepositoryGalleryName = "Shared Repository"
    galleryName = 'New1'
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
            self.videoEntryName = clsTestService.addGuidToString("Upload To SR From My Media - Video", self.testNum)
            self.audioEntryName = clsTestService.addGuidToString("Upload To SR From My Media - Audio", self.testNum)
            self.imageEntryName = clsTestService.addGuidToString("Upload To SR From My Media - Image", self.testNum)
            
            self.entriesToUpload = {
            self.videoEntryName: self.filePathVideo, 
            self.audioEntryName: self.filePathAudio,
            self.imageEntryName: self.filePathImage }

            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to add shared repository module")     
            if self.common.blackBoard.addRemoveSharedRepositoryModule(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to add shared repository module")
 
            writeToLog("INFO","Step 2: Going to navigate to upload media page in SR")
            if self.common.blackBoard.navigateToUploadMediaInSR() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to upload media page in SR")
                return               
 
            writeToLog("INFO","Step 3: Going to upload image media")
            if self.common.upload.uploadEntry(self.filePathImage, self.imageEntryName, self.description, self.tags, uploadFrom=enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to upload image media")
                return  
     
            writeToLog("INFO","Step 4: Going to completed the required fields in entry '" + self.imageEntryName + "' order to publish")
            if self.common.blackBoard.addSharedRepositoryMetadata(self.imageEntryName, self.SR_RequiredField, enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add required fields to entry '" + self.imageEntryName)
                return
             
            writeToLog("INFO","Step 5: Going to navigate to upload media page in SR")
            if self.common.blackBoard.navigateToUploadMediaInSR() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to upload media page in SR")
                return 
             
            writeToLog("INFO","Step 6: Going to upload video media")
            if self.common.upload.uploadEntry(self.filePathVideo, self.videoEntryName, self.description, self.tags, uploadFrom=enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to upload video media")
                return  
     
            writeToLog("INFO","Step 7: Going to completed the required fields in entry '" + self.videoEntryName + "' order to publish")
            if self.common.blackBoard.addSharedRepositoryMetadata(self.videoEntryName, self.SR_RequiredField, enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to add required fields to entry '" + self.videoEntryName)
                return   
             
            writeToLog("INFO","Step 8: Going to navigate to upload media page in SR")
            if self.common.blackBoard.navigateToUploadMediaInSR() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to upload media page in SR")
                return 
             
            writeToLog("INFO","Step 9: Going to upload audio media")
            if self.common.upload.uploadEntry(self.filePathAudio, self.audioEntryName, self.description, self.tags, uploadFrom=enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to upload audio media")
                return  
     
            writeToLog("INFO","Step 10: Going to completed the required fields in entry '" + self.audioEntryName + "' order to publish")
            if self.common.blackBoard.addSharedRepositoryMetadata(self.audioEntryName, self.SR_RequiredField, enums.Location.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add required fields to entry '" + self.audioEntryName)
                return                       
             
            writeToLog("INFO","Step 11: Going navigate to shared repository gallery")
            if self.common.blackBoard.navigateToSharedRepositoryInBB() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED navigate to shared repository gallery")
                return
              
            self.common.blackBoard.switchToBlackboardIframe()
            writeToLog("INFO","Step 12: Going to verify entry '" + self.imageEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.imageEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to find entry '" + self.imageEntryName + "' shared repository gallery")
                return
              
            writeToLog("INFO","Step 13: Going to clear search textbox")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to clear search textbox")
                return
          
            writeToLog("INFO","Step 14: Going to verify entry '" + self.audioEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.audioEntryName) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to find entry '" + self.audioEntryName + "' shared repository gallery")
                return
              
            writeToLog("INFO","Step 15: Going to clear search textbox")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to clear search textbox")
                return
              
            writeToLog("INFO","Step 16: Going to verify entry '" + self.videoEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.videoEntryName) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to find entry '" + self.videoEntryName + "' shared repository gallery")
                return
            
            writeToLog("INFO","Step 17: Going to publish entries from SR to media gallery")
            if self.common.kafGeneric.addSharedRepositoryMedieToMediaGallery(self.galleryName, [self.videoEntryName, self.audioEntryName, self.imageEntryName]) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to publish entries from SR to media gallery")
                return     
            
            writeToLog("INFO","Step 18: Going to navigate to " + self.galleryName)
            if self.common.blackBoard.navigateToGalleryBB(self.galleryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to navigate to to " + self.galleryName)
                return
            
            self.common.base.click(self.common.kafGeneric.KAF_REFRSH_BUTTON)
            sleep(5)
            
            self.common.blackBoard.switchToBlackboardIframe()
            writeToLog("INFO","Step 19: Going to verify entry '" + self.imageEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.imageEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to find entry '" + self.imageEntryName + "' shared repository gallery")
                return
             
            writeToLog("INFO","Step 20: Going to clear search textbox")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to clear search textbox")
                return
         
            writeToLog("INFO","Step 21: Going to verify entry '" + self.audioEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.audioEntryName) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to find entry '" + self.audioEntryName + "' shared repository gallery")
                return
             
            writeToLog("INFO","Step 22: Going to clear search textbox")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to clear search textbox")
                return
             
            writeToLog("INFO","Step 23: Going to verify entry '" + self.videoEntryName + "' display in shared repository gallery")
            if self.common.channel.searchEntryInChannel(self.videoEntryName) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to find entry '" + self.videoEntryName + "' shared repository gallery")
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