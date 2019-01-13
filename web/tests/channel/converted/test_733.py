import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from time import strftime
import pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    # @Author: Oded.berihon @Test name : Add Existing Media to channel
    # Test description:
    # Upload entry and 
    # create channel 
    # enter the channel click on the "add media" button > check the entry in the list and click publish 
    # verify that the entry was publish to the channel
    #================================================================================================================================
    testNum     = "733"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    driver = None
    common = None
    # Test variables
    entryDescription = "description"
    entryTags = "tag,"
    channelDescription = "description"
    channelTags = "tag,"
    privacyType = ""
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'

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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('add to', self.testNum)
            self.channelName = clsTestService.addGuidToString('add to media', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to upload Video type entry")            
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry Video")
                return
           
            writeToLog("INFO","Step 2: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create Channel#1")
                return
            
            writeToLog("INFO","Step 3: Going to navigate to channel page")
            if self.common.channel.navigateToChannel(self.channelName, navigateFrom=enums.Location.MY_CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED - could not navigate to channel page")
                return         
           
            writeToLog("INFO","Step 4: Going to add content to channel")            
            if self.common.channel.addExistingContentToChannel(self.channelName, self.entryName1, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add content to channel: '" + self.entryName1 + "'")
                return     
            
            writeToLog("INFO","Step 5: Going navigate to channel page")   
            if self.common.channel.navigateToChannel(self.channelName, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to channel page")
                return  
             
            writeToLog("INFO","Step 6: Going to verify that entry was publish to channel")            
            if self.common.channel.searchEntryInChannel(self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify that entry was publish to channel: '" + self.entryName1 + "'")
                return  
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status, leavePageExpected=True)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1])                 
            self.common.channel.deleteChannel(self.channelName) 
            writeToLog("INFO","**************** Ended: teardown_method *******************")
            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')