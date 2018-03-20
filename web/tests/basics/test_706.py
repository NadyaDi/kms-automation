from time import strftime
import pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from upload import UploadEntry
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    # @Author: Tzachi Guetta
    # Test description:
    # 
    #================================================================================================================================
    testNum     = "706"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    categoryName = None   
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"   
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg' 
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\audio.mp3' 
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4' 
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,capture,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('Audio-entry1')
            self.entryName2 = clsTestService.addGuidToString('Video-entry2')
            self.entryName3 = clsTestService.addGuidToString('Image-entry3')
            self.categoryName = "KMS-Automation"
            
            self.audioEntry = UploadEntry(self.filePathAudio, self.entryName1, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.videoEntry = UploadEntry(self.filePathVideo, self.entryName2, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.imageEntry = UploadEntry(self.filePathImage, self.entryName3, self.entryDescription, self.entryTags, timeout=60, retries=3)
            uploadEntrieList = [self.audioEntry, self.videoEntry, self.imageEntry] 
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
                        
            writeToLog("INFO","Step 2: Going to upload 5 entries")
            if self.common.category.addNewContentToCategory(self.categoryName, uploadEntrieList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 5 entries")
                return
            
            writeToLog("INFO","Step 2: Going to")
            if self.common.entryPage.navigateToEntryPageFromCategoryPage(self.entryName1, self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED ")
                return
            
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)           
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia(self.entryName1, self.entryName2, self.entryName3)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')