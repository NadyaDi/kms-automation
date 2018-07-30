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
    # Test Name : My Media - Publish to channel - single
    # Test description:
    # Upload entry -> Search entry in My Media -> Check entry checkbox -> Click on 'Action' -> Choose 'publish' -> Choose channel -> Click 'Save'
    #================================================================================================================================
    testNum = "661"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "description"
    entryTags = "tag1,"
    channelName = 'publicChannelMyHistory'
    channelList = [(channelName)]
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
            self.entryName = clsTestService.addGuidToString('publishEntryToChannel', self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################  
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
               
            writeToLog("INFO","Step 2: Going to publish entry to channel from My media page")
            if self.common.myMedia.publishEntriesFromMyMedia(self.entryName, [], self.channelList) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 2: FAILED to publish entry to channel from My Media")
                return    
            
            writeToLog("INFO","Step 3: Going to search entry in channel page")
            if self.common.channel.verifyIfSingleEntryInChannel(self.channelName, self.entryName) == False:
                self.status = "Fail"        
                writeToLog("INFO","Step 3: FAILED to find entry in channel")
                return                         
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Publish to channel - single' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteEntryFromEntryPage(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')