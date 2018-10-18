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
    # Test Name : My Media - Publish to channel - multiple
    # Test description:
    # Upload entries -> Search entries in My Media -> Check entries checkbox -> Click on 'Action' -> Choose 'publish' -> Choose channel -> Click 'Save'
    #================================================================================================================================
    testNum = "663"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entriesName = []
    entryDescription = "description"
    entryTags = "tag1,"
    channelName = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'

    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('publishEntryToChannel1', self.testNum)
            self.entryName2 = clsTestService.addGuidToString('publishEntryToChannel2', self.testNum)
            self.entryName3 = clsTestService.addGuidToString('publishEntryToChannel3', self.testNum)
            self.entriesName = [self.entryName1, self.entryName2, self.entryName3]
            self.channelName = clsTestService.addGuidToString("'My Media - Publish to channel-multiple", self.testNum) 
            ##################### TEST STEPS - MAIN FLOW #####################  
            writeToLog("INFO","Step 1: Going to upload entries")
            if self.common.upload.uploadMultipleEntries(self.filePath, self.entriesName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entries")
                return
            
            writeToLog("INFO","Step 2: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.entryDescription, self.entryTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED create new channel: " + self.channelName)
                return
               
            writeToLog("INFO","Step 3: Going to publish entries to channel from My media page")
            if self.common.myMedia.publishEntriesFromMyMedia(self.entriesName, "", [self.channelName]) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 3: FAILED to publish entries to channel from My Media")
                return    
            
            writeToLog("INFO","Step 4: Going to search entries in channel page")
            if self.common.channel.verifyIfMultipleEntriesInChannel(self.channelName, self.entriesName) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 4: FAILED to find entries in channel")
                return                         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Search in my media' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesName)
            self.common.channel.deleteChannel(self.channelName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')