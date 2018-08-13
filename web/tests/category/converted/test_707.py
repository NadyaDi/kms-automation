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
    #  @Author: Inbar Willman
    # Test Name : Categories - Add new media from my media to category
    # Test description:
    # Create new category -> Upload 3 entries -> publishe entries to category from my media 0-> check that entries are displayed in category
    # test cleanup: deleting the uploaded files
    #================================================================================================================================
    testNum = "707"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 =None
    entryName2 =None
    entryName3 = None
    categoryName = 'Apps Automation Category'
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3'
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
            self.entryName1 = clsTestService.addGuidToString('publishVideoToCategory', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('publishImageToCategory', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('publishAUdioToCategory', self.testNum)
            self.entriesList = [self.entryName1, self.entryName2, self.entryName3]
            self.entriesToUpload = {
                self.entryName1: self.filePathVideo, 
                self.entryName2: self.filePathImage,
                self.entryName3: self.filePathAudio}
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload 3 entries")            
            if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return

            writeToLog("INFO","Step 2: Going to publish entries to category from my media")
            if self.common.myMedia.publishEntriesFromMyMedia(self.entriesList, [self.categoryName], "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to publish entries to category from my media")
                return 
            
            writeToLog("INFO","Step 3: Going to search entries in category")
            if self.common.category.searchEntriesInCategory(self.entriesList, self.categoryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to find entries in category")
                return  
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Add new media from my media to category' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
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