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
    #  @Author: Horia Cus
    # Test Name : Setup test for eSearch
    # Test description:
    # Going to create four channels in order to be able to filter them by manager / shared / member and subscriber
    #================================================================================================================================
    testNum = "33"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    channelNameManager         = "Channel Membership - Manager"
    channelNameSR              = "Channel Membership - Shared"
    channelNameMember          = "Channel Membership - Member"
    channelNameSubscriber      = "Channel Membership - Subscriber"
    channelDescription         = "Channel Membership"
    channelTags                = "filter,"

    userName1 = "inbar.willman@kaltura.com"
    userPass1 = "Kaltura1!"

    userName2 = "admin"
    userPass2 = "123456"

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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)

            self.userName1Channels = {self.channelNameManager:enums.ChannelPrivacyType.OPEN, self.channelNameSR:enums.ChannelPrivacyType.SHAREDREPOSITORY}
            self.userName2Channels = {self.channelNameMember:enums.ChannelPrivacyType.OPEN, self.channelNameSubscriber:enums.ChannelPrivacyType.OPEN}
            ########################## TEST STEPS - MAIN FLOW #######################
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login with " + self.userName1)
                return
            else:
                i = i + 1
            i = i
  
            for entry in self.userName1Channels:
                i = i
                writeToLog("INFO","Step " + str(i) + ": Going to create " + entry + " channel for " + self.userName1)
                if self.common.channel.createChannel(entry, self.channelDescription, self.channelTags, self.userName1Channels[entry], True, True, True) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": Failed to create " + entry + " channel for " + self.userName1)
                    return
                else:
                    i = i + 1
                i = i
  
            writeToLog("INFO","Step " + str(i) + ": Going to log out from " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from " + self.userName1)
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to login with user " + self.userName2)
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login with " + self.userName2)
                return
            else:
                i = i + 1
            i = i
 
            for entry in self.userName2Channels:
                i = i
                writeToLog("INFO","Step " + str(i) + ": Going to create " + entry + " channel for " + self.userName1)
                if self.common.channel.createChannel(entry, self.channelDescription, self.channelTags, self.userName2Channels[entry], True, True, True) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": Failed to create " + entry + " channel for " + self.userName1)
                    return
                else:
                    i = i + 1
                i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to add " + self.userName1 + " as member for " + self.channelNameManager + " channel")
            if self.common.channel.addMembersToChannel(self.channelNameMember, self.userName1, permission=enums.ChannelMemberPermission.MEMBER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": Failed to add " + self.userName1 + " as member for " + self.channelNameManager + " channel")
                return
            else:
                i = i + 1
            i = i
 
            writeToLog("INFO","Step " + str(i) + ": Going to log out from " + self.userName2)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from " + self.userName2)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login with " + self.userName1)
                return
            else:
                i = i + 1
            i = i

            writeToLog("INFO","Step " + str(i) + ": Going to add " + self.userName1 + " as member for " + self.channelNameManager + " channel")
            if self.common.channel.subscribeUserToChannel(self.channelNameSubscriber,  "1" , navigateFrom=enums.Location.CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": Failed to add " + self.userName1 + " as member for " + self.channelNameManager + " channel")
                return
            else:
                i = i + 1
            i = i
            #################################################################################

        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)

    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')