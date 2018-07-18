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
    #  @Author: Michal Zomper
    # Test Name : My Channels - Search as subscriber
    # Test description:
    # create several channel (with different users) and add one user (different one that those how created channel) as a channel subscriber
    # login with the user that was added as subscriber -> go to my channels page and  Filter by 'Channels I am subscribed to'
    # Search for an existing channel - The channel you have searched for should be displayed
    # Search for a channel that does not exist - No channel should be displayed. The following message should be received: "Your search for "X did not match any channels. Make sure you spelled the word correctly
    # Try a different search term"
    #================================================================================================================================
    testNum = "729"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    channelName1 = None
    channelName2 = None
    channelName3 = None
    channelDescription = "Description"
    channelTags = "Tags,"
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    userName2 = "Automation_User_2"
    userPass2 = "Kaltura1!"
    #filterBy = "I am subscribed to"

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
            self.channelName1 = clsTestService.addGuidToString("My Channels - Search as subscriber  1", self.testNum)
            self.channelName2 = clsTestService.addGuidToString("My Channels - Search as subscriber  2", self.testNum)
            self.channelName3 = clsTestService.addGuidToString("My Channels - Search as subscriber  3", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
        
            writeToLog("INFO","Step 1: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName1, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED create new channel: " + self.channelName1)
                return
              
            writeToLog("INFO","Step 2: Going to add user '" + self.userName2 +"' as subscriber to channel '" + self.channelName1 + "'")
            if self.common.channel.addMembersToChannel(self.channelName1, self.userName2, permission=enums.ChannelMemberPermission.MEMBER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to add user '" + self.userName2 + "' as manager to channel '" + self.channelName1 + "'")
                return
             
            sleep(3)
            writeToLog("INFO","Step 3: Going to logout from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to logout from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " user")
                return  
                                 
            writeToLog("INFO","Step 4: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to login with " + self.userName1)
                return
              
            writeToLog("INFO","Step 5: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName2, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED create new channel: " + self.channelName2)
                return
             
            writeToLog("INFO","Step 6: Going to add user '" + self.userName2 +"' as manager to channel '" + self.channelName2 + "'")
            if self.common.channel.addMembersToChannel(self.channelName2, self.userName2, permission=enums.ChannelMemberPermission.MANAGER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to add user '" + self.userName2 + "' as manager to channel '" + self.channelName2 + "'")
                return
             
            writeToLog("INFO","Step 7: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName3, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED create new channel: " + self.channelName3)
                return
 
            sleep(3)
            writeToLog("INFO","Step 8: Going to logout from " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to logout from " + self.userName1)
                return  
                                
            writeToLog("INFO","Step 9: Going to login with : " + self.userName2)
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to login with " + self.userName2)
                return
             
            writeToLog("INFO","Step 10: Going to add user '" + self.userName2 +"' as channel subscriber in '" + self.channelName1 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName1, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add user '" + self.userName2 + "' as channel subscriber in '" + self.channelName1 + "'")
                return
             
            writeToLog("INFO","Step 11: Going to add user '" + self.userName2 +"' as channel subscriber in '" + self.channelName3 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName3, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to add user '" + self.userName2 + "' as channel subscriber in '" + self.channelName3 + "'")
                return
            
            writeToLog("INFO","Step 12 Going navigate to my channels page")
            if self.common.channel.navigateToMyChannels() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED navigate to my channels page")
                return 
            
            writeToLog("INFO","Step 13: Going to filter view channel by 'Channels i'm " + enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI.value + "'")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.channel.selectViewChannelFilterInMyChannelsPage(enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 13: FAILED to filter view channels by: 'Channels i'm " + enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI.value)
                    return 
            else:
                if self.common.channel.selectViewChannelFilterInMyChannelsPage(enums.ChannelsSortByMembership.SUBSCRIBER_OLDUI) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 13: FAILED to filter view channels by: " + enums.ChannelsSortByMembership.SUBSCRIBER_OLDUI.value)
                    return 
                
            writeToLog("INFO","Step 14: Going to search for channel that i'm subscribed to by using filter 'channels i'm " + enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI.value +"'")
            if self.common.channel.searchAChannelInMyChannels(self.channelName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to find channel '" + self.channelName1 + "' using filter 'channels i'm " + enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI.value + "'")
                return
            self.common.base.click(self.common.channel.CHANNEL_REMOVE_SEARCH_ICON , multipleElements=True)
            self.common.general.waitForLoaderToDisappear()
            
            writeToLog("INFO","Step 15: Going to search for channel that i'm NOT subscribe by using filter 'channels i'm " + enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI.value +"'")
            if self.common.channel.searchAChannelInMyChannels(self.channelName2, needToBeFound=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED,channel '" + self.channelName2 + "'was found in search using filter 'channels i'm " + enums.ChannelsSortByMembership.SUBSCRIBER_NEWUI.value + "' although i'm not the manager of this channel")
                return
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'My Channels - Search as subscriber' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            sleep(2) 
            self.common.login.logOutOfKMS()
            self.common.loginAsUser() 
            self.common.channel.deleteChannel(self.channelName1)
            sleep(3)
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(self.userName1, self.userPass1)                   
            self.common.channel.deleteChannel(self.channelName2)
            self.common.channel.deleteChannel(self.channelName3)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')