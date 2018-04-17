import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','..','lib')))
import pytest
from time import strftime
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
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3' 
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('Audio-entry1')
            self.entryName2 = clsTestService.addGuidToString('Video-entry2')
            self.entryName3 = clsTestService.addGuidToString('Image-entry3')
            self.categoryName = "Apps Automation Category"
            
            self.audioEntry = UploadEntry(self.filePathAudio, self.entryName1, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.videoEntry = UploadEntry(self.filePathVideo, self.entryName2, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.imageEntry = UploadEntry(self.filePathImage, self.entryName3, self.entryDescription, self.entryTags, timeout=60, retries=3)
            uploadEntrieList = [self.audioEntry, self.videoEntry, self.imageEntry]
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3]
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
                        
            writeToLog("INFO","Step 2: Going to upload and publish 3 kind of entries to: " + self.categoryName )
            if self.common.category.addNewContentToCategory(self.categoryName, uploadEntrieList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload and publish 3 kind of entries to: " + self.categoryName)
                return
            
            sleep(30)
            for entry in self.entriesList:
                writeToLog("INFO","Step 2: Going to verify that " + entry + ", is presented inside the category")
                if self.common.entryPage.navigateToEntryPageFromCategoryPage(entry, self.categoryName) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 2: FAILED to verify that " + entry + ", is presented inside the category")
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
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesList)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')