import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : preview all kinds of media from My Media and Category
    # Test description:
    # upload 3 entries : video / Audio / Image
    #  Navigate to each entry page and verify player is working  and that the video / audio / image  is correct
    # Publish the entries to category. navigate to entries form the category and verify the player  
    #================================================================================================================================
    testNum = "644"
    
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
    categoryName = None
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.videoEntryName = clsTestService.addGuidToString("Upload media and verify in player - Video", self.testNum)
            self.audioEntryName = clsTestService.addGuidToString("Upload media and verify in player - Audio", self.testNum)
            self.imageEntryName = clsTestService.addGuidToString("Upload media and verify in player - Image", self.testNum)
            self.categoryName = clsTestService.addGuidToString('Upload media and verify in player category', self.testNum)
            
            self.entriesToUpload = {
            self.videoEntryName: self.filePathVideo, 
            self.audioEntryName: self.filePathAudio,
            self.imageEntryName: self.filePathImage }
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create parent category") 
            self.common.apiClientSession.startCurrentApiClientSession()
            parentId = self.common.apiClientSession.getParentId('galleries') 
            if self.common.apiClientSession.createCategory(parentId, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, self.categoryName, self.description) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create parent category")
                return
             
            writeToLog("INFO","Step 2: Going to clear cache")            
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to clear cache")
                return
            
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 4: Going to upload 3 entries: Video / Audio / Image")   
            if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to upload 3 entries")
                return
                    
            writeToLog("INFO","Step 5: Going navigate to image entry: "+ self.imageEntryName)    
            if self.common.entryPage.navigateToEntry(self.imageEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to entry: " + self.imageEntryName)
                return 
                
            writeToLog("INFO","Step 6: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.IMAGE, "", "", self.ImageQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify the entry '" + self.imageEntryName + "' in player")
                return   
            
            writeToLog("INFO","Step 7: Going navigate to audio entry: "+ self.audioEntryName)    
            if self.common.entryPage.navigateToEntry(self.audioEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED navigate to entry: " + self.audioEntryName)
                return 
                        
            writeToLog("INFO","Step 8: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED - New entry is still processing")
                return 
            
            writeToLog("INFO","Step 9: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.AUDIO, self.audioLength, "", "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify the entry '" + self.audioEntryName + "' in player")
                return   
   
            writeToLog("INFO","Step 10: Going navigate to video entry: "+ self.videoEntryName)    
            if self.common.entryPage.navigateToEntry(self.videoEntryName, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED navigate to entry: " + self.videoEntryName)
                return 
                  
            writeToLog("INFO","Step 11: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED - New entry is still processing")
                return 
            
            writeToLog("INFO","Step 12: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.VIDEO, self.vidoeLength, self.vidoeTimeToStop, self.videoQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to verify the entry '" + self.videoEntryName + "' in player")
                return   
            
            writeToLog("INFO","Step 13: Going to publish entries to category")
            if self.common.myMedia.publishEntriesFromMyMedia([self.videoEntryName,self.audioEntryName,self.imageEntryName], [self.categoryName], '', showAllEntries=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to publish entries to category")
                return  
            
            writeToLog("INFO","Step 14: Going navigate to image entry: '" + self.imageEntryName + "' from category page")    
            if self.common.entryPage.navigateToEntry(self.imageEntryName, enums.Location.CATEGORY_PAGE, categoryName=self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED navigate to entry: " + self.imageEntryName + " from category page")
                return 
                
            writeToLog("INFO","Step 15: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.IMAGE, "", "", self.ImageQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to verify the entry '" + self.imageEntryName + "' in player")
                return   
            
            writeToLog("INFO","Step 16: Going navigate to audio entry: '" + self.audioEntryName + "' from category page")    
            if self.common.entryPage.navigateToEntry(self.audioEntryName, enums.Location.CATEGORY_PAGE, categoryName=self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED navigate to entry: " + self.audioEntryName + " from category page")
                return 
            
            writeToLog("INFO","Step 17: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.AUDIO, self.audioLength, "", "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to verify the entry '" + self.audioEntryName + "' in player")
                return   
            
            writeToLog("INFO","Step 18: Going navigate to video entry: '"+ self.videoEntryName + "' from category page")    
            if self.common.entryPage.navigateToEntry(self.videoEntryName, enums.Location.CATEGORY_PAGE, categoryName=self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 101: FAILED navigate to entry: " + self.videoEntryName + " from category page")
                return 
            
            writeToLog("INFO","Step 19: Going to verify the entry in player")            
            if self.common.entryPage.verifyEntryViaType(enums.MediaType.VIDEO, self.vidoeLength, self.vidoeTimeToStop, self.videoQrCodeResult) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to verify the entry '" + self.videoEntryName + "' in player")
                return 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Preview all kinds of media from My Media and category' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")      
            self.common.myMedia.deleteEntriesFromMyMedia([self.videoEntryName, self.audioEntryName, self.imageEntryName])
            self.common.apiClientSession.deleteCategory(self.categoryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')