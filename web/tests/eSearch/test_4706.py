import time, pytest
import sys,os
from _ast import Num
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
    # Test Name : Filter by Channel Membership - no search - My Channels page
    # Test description:
    # Verify that proper channels are displayed while filtering them by manager,member,subscriber and shared
    #================================================================================================================================
    testNum = "4706"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    channelNameManager         = "Channel Membership - Manager"
    channelNameSR              = "Channel Membership - Shared"
    channelNameMember          = "Channel Membership - Member"
    channelNameSubscriber      = "Channel Membership - Subscriber"
    
    searchPage       = "My Channels Page - no search"
    searchTerm       = "Channel Membership"
    navigatePage     = "My Channels Page"

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
            
            self.channelListManager      = {self.channelNameManager:True, self.channelNameSR:True, self.channelNameMember:False, self.channelNameSubscriber:False}
            self.channelListMember       = {self.channelNameManager:True, self.channelNameSR:True, self.channelNameMember:True, self.channelNameSubscriber:False}
            self.channelListSubscriber   = {self.channelNameManager:False, self.channelNameSR:False, self.channelNameMember:False, self.channelNameSubscriber:True}
            self.channelListSR           = {self.channelNameManager:False, self.channelNameSR:True, self.channelNameMember:False, self.channelNameSubscriber:False}
            
            self.enumManager         = enums.ChannelsSortByMembership.MANAGER_NEWUI
            self.enumMember          = enums.ChannelsSortByMembership.MEMBER_NEWUI
            self.enumSubscriber      = enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI
            self.enumSR              = enums.ChannelsSortByMembership.SHAREDREPOSITORIES_NEWUI

            self.channelMap = {self.enumManager:[self.channelListManager, enums.ChannelsSortByMembership.MANAGER_NEWUI.value], self.enumMember:[self.channelListMember, enums.ChannelsSortByMembership.MEMBER_NEWUI.value], self.enumSubscriber:[self.channelListSubscriber, enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI.value], self.enumSR:[self.channelListSR, enums.ChannelsSortByMembership.SHAREDREPOSITORIES_NEWUI.value]}
            ##################### TEST STEPS - MAIN FLOW #####################         
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.navigatePage)
            if self.common.channel.navigateToMyChannels(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.navigatePage)
                return
            else:
                i = i + 1
            i = i
            
            for channel in self.channelMap:
                i = i
                writeToLog("INFO", "Step " + str(i) + ": Going to filter " + self.searchPage + " entries by: " + self.channelMap[channel][1] + "'")
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CHANNEL_MEMBERSHIP, channel) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to filter " + self.searchPage + " entries  by '" + self.channelMap[channel][1] + "'")
                    return
                else:
                    i = i + 1
                    
                writeToLog("INFO", "Step " + str(i) + ": Going to verify filter for " + self.searchPage + " entries by: " + self.channelMap[channel][1])
                if self.common.channel.verifyChannelIsPresent(self.channelMap[channel][0]) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to verify filter for " + self.searchPage + " entries by: " + self.channelMap[channel][1])
                    return
                else:
                    i = i + 1
                i = i
            
                writeToLog("INFO", "Step " + str(i) + ": Going to clear the filter search menu")
                if self.common.myMedia.filterClearAllWhenOpened() == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": Failed to clear the search menu")
                    return
                else:
                    i = i + 1
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the channels were properly displayed in " + self.searchPage + " while filtering them by manager,member, subscriber and shared")
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