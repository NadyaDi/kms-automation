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
    # Test Name : Trimming Audio entry
    # Test description:
    # 
    #================================================================================================================================
    testNum = "4535"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3'
    
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
            self.audioEntryName = clsTestService.addGuidToString("Upload media - Audio", self.testNum)
            expectedEntryDuration = "0:21"
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload entry - to be trimmed")  
            if self.common.upload.uploadEntry(self.filePathVideo, self.audioEntryName, self.description, self.tags) == False:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to trim the entry from 30sec to 20sec")  
            if self.common.kea.trimEntry(self.audioEntryName, "00:10", "00:20", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 2: FAILED to trim the entry from 30sec to 20sec")
                return

            writeToLog("INFO","Step 3: Going to Navigate to entry page")  
            self.QRlist = self.common.entryPage.navigateToEntryPageFromMyMedia(self.audioEntryName)
            if  self.QRlist == False:
                writeToLog("INFO","Step 3: FAILED to Navigate to entry pagem")
                return

            writeToLog("INFO","Step 4: Going to verify the Audio's duration after trim")  
            self.QRlist = self.common.entryPage.verifyEntryViaType(enums.MediaType.AUDIO, expectedEntryDuration)
            if  self.QRlist == False:
                writeToLog("INFO","Step 4: FAILED to verify the Audio's duration after trim")
                return
            #################################################################################################
            self.status = "Pass"   
            writeToLog("INFO","TEST PASSED")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia(self.audioEntryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')