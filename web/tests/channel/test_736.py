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
    # @Author: Oded.berihon @Test name : Remove media from channel

    # Test description:
    # Upload entry publish to channel and remove it from the channel
    # 
    #================================================================================================================================
    testNum     = "736"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    driver = None
    common = None
    # Test variables
    entryName1 = None
#     entryName2 = None
#     entryName3 = None
    entryDescription = "description"
    entryTags = "tag,"
    entriesNames = None
    channelName = "9437BD9A_this Is My New Channel"
    channelDescription = "description"
    channelTags = "tag,"
    privacyType = ""
    playlisTitle = None
    playlistDescription = "playlist description"
    playlistTag = "playlisttag,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\waves.mp3'
    filePath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    
    
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
            self.entryName1 = clsTestService.addGuidToString('Video', self.testNum)
#             self.entryName2 = clsTestService.addGuidToString('Audio', self.testNum)
#             self.entryName3 = clsTestService.addGuidToString('Video2', self.testNum)
            self.channelName = clsTestService.addGuidToString('Channel playlist', self.testNum)
#             self.playlisTitle = clsTestService.addGuidToString('Channel playlist', self.testNum)
#             self.entriesNames = [self.entryName1, self.entryName2, self.entryName3]
            ########################## TEST STEPS - MAIN FLOW #######################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return    
            
            writeToLog("INFO","Step 2: Going to upload Video type entry")            
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry Video")
                return
           
            writeToLog("INFO","Step 3: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create Channel#1")
                return
           
            writeToLog("INFO","Step 4: Going to publish entry1")
            if self.common.myMedia.publishSingleEntry(self.entryName1, [], [self.channelName], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 4: FAILED - could not publish Video to channel")
                return
            
            writeToLog("INFO","Step 5: Going to add and remove entry from channel")                                     
            if self.common.channel.removeEntryFromChannel(self.channelName, self.entryName1)== False:    
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED failed to create channel playlist")
                return 
            sleep(3)   
            
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