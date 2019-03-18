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
    # @Author: Oded.berihon 
    # @Test name : Remove media from channel
    # Test description:
    # Upload entry publish to channel and remove it from the channel
    # 
    #================================================================================================================================
    testNum     = "736"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryDescription = "description"
    entryTags = "tag,"
    channelDescription = "description"
    channelTags = "tag,"
    privacyType = ""
    playlistTag = "playlisttag,"
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
            self.entryName1 = clsTestService.addGuidToString('Video', self.testNum)
            self.channelName = clsTestService.addGuidToString('Remove Entry From Channel', self.testNum)
            ########################## TEST STEPS - MAIN FLOW #######################

            writeToLog("INFO","Step 1: Going to upload entry")            
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                writeToLog("INFO","Step 2: FAILED to create Channel#1")
                return
            
            writeToLog("INFO","Step 3: Going to publish entry1")
            if self.common.myMedia.publishSingleEntry(self.entryName1, [], [self.channelName], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 3: FAILED to publish Video to channel")
                return

            writeToLog("INFO","Step 4: Going to add and remove entry from channel")                                     
            if self.common.channel.removeEntryFromChannel(self.channelName, self.entryName1)== False:    
                writeToLog("INFO","Step 4: FAILED to remove entry form channel")
                return 
            sleep(3)  
             
            writeToLog("INFO","Step 5: Going to verify that entry doesn't display in channel any more")                                     
            if self.common.channel.searchEntryInChannel(self.entryName1) == True:    
                writeToLog("INFO","Step 5: FAILED entry '" + self.entryName1 + "' still display in channel although he was removed")
                return 
            writeToLog("INFO","Step 6: Preview step failed as expected - entry was removed from channel and should not be found")
            #########################################################################
            self.status = "Pass"
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