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
    #  @Author: Tzachi Guetta
    # Test Name : 
    # Test description:
    # 
    #================================================================================================================================
    testNum = "2869"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
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
            self.videoEntryName = clsTestService.addGuidToString("Upload media - Video", self.testNum)
            self.audioEntryName = clsTestService.addGuidToString("Upload media  - Audio", self.testNum)
            self.imageEntryName = clsTestService.addGuidToString("Upload media - Image", self.testNum)
            
            self.entriesToUpload = {
            self.videoEntryName: self.filePathVideo, 
            self.audioEntryName: self.filePathAudio,
            self.imageEntryName: self.filePathImage }
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry - to be trimmed")  
            if self.common.upload.uploadEntry(self.filePathVideo, self.videoEntryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to Launch KEA for the uploaded entry")  
            if self.common.kea.launchKEA(self.videoEntryName, enums.Location.ENTRY_PAGE, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to Launch KEA for the uploaded entry")
                return

        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.videoEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')