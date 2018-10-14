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
    # @Author: Oded.berihon @Test name : Enable/Disable comments in channel

    # Test description:
    # Upload entry publish it to channel edit channel and enable comment go to entry in the channel and add comment 
    # go back to edit channel and disable comment go to entry and try to add comment.
    # 
    #================================================================================================================================
    testNum = "740"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryDescription = "description"
    entryTags = "tag,"
    channelName = "9437BD9A_this Is My New Channel"
    channelDescription = "description"
    channelTags = "tag,"
    privacyType = ""
    comment = "Comment 1"
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName1 = clsTestService.addGuidToString('Video', self.testNum)
            self.channelName = clsTestService.addGuidToString('Enable/Disable comments in channel', self.testNum)
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
            
            writeToLog("INFO","Step 5: Going to add comment to entry")                                     
            if self.common.channel.addCommentToEntryFromChannel(self.channelName, self.entryName1, self.comment) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add comment to entry")
                return 
            
            writeToLog("INFO","Step 6: Going navigate to edit channel page") 
            if self.common.channel.navigateToEditChannelPage(self.channelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate to edit channel page")
                return  

            writeToLog("INFO","Step 7: Going to enable and disable comments in channel")                                     
            if self.common.channel.enableDisableCommentsInChannel(self.channelName, False) == False:    
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to add and disable comments in channel")
                return 
            
            writeToLog("INFO","Step 8: Going to navigate to entry from channel page")      
            if self.common.channel.navigateToEntryFromChannel(self.channelName, self.entryName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to edit channel page")
                return False
            
            writeToLog("INFO","Step 9: Going to verify user can't add comment")
            if self.common.entryPage.checkEntryCommentsSection(self.comment, True, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9:FAILED to verify user can't add comment") 
                return False
            
            sleep(3)   
            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Enable/Disable comments in channel' was done successfully")
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