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
    # Test Name : My Channels - Filter view
    # Test description:
    # create several channel (with different users) and add them member / subscriber/ managers
    # go to my channel page and filter the channel :
    # 1. In the View field, choose 'View Channels I Mannage' - Only channels you manage should be dusplayed. Each channel should have 'Edit' link
    # 2. In the View field, choose 'View Channels I am member of' -  Only Channels you are member of should be displayed
    # 3. In the View field, choose 'View Channels I am subscribed to' - Only Channels you are subscribed to should be displayed
    # 4. In the View field, choose 'View Shared Repositories I am member of' 

    #================================================================================================================================
    testNum = "726"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    channelName1 = None
    channelName2 = None
    channelName3 = None
    channelName4 = None
    channelName5 = None
    channelDescription = "Description"
    channelTags = "Tags,"
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    userName2 = "Automation_User_2"
    userPass2 = "Kaltura1!"
    userName3 = "Automation_User_3"
    userPass3 = "Kaltura1!"
    userName4 = "Automation_User_4"
    userPass4 = "Kaltura1!"
    channelsIManage = None
    channelsIAmAMemberOf = None
    channelsIAmSubscribedTo = None
    ChannelsSharedRepositoriesIAmAMemberOf = None
    
    

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
            self.channelName1 = clsTestService.addGuidToString("My Channels - Filter view 1", self.testNum)
            self.channelName2 = clsTestService.addGuidToString("My Channels - Filter view 2", self.testNum)
            self.channelName3 = clsTestService.addGuidToString("My Channels - Filter view 3", self.testNum)
            self.channelName4 = clsTestService.addGuidToString("My Channels - Filter view 4", self.testNum)
            self.channelName5 = clsTestService.addGuidToString("My Channels - Filter view 5", self.testNum)
            
            # each dictionary  get a list of channels and bool parameter that indicate if the channel need to be display in the list filter or not
            self.channelsIManage = [(self.channelName1, False), (self.channelName2, True), (self.channelName3, True), (self.channelName4, False), (self.channelName5, False)]
            self.channelsIAmAMemberOf = [(self.channelName1, False), (self.channelName2, True), (self.channelName3, True), (self.channelName4, False), (self.channelName5, True)]
            self.channelsIAmSubscribedTo = [(self.channelName1, True), (self.channelName2, False), (self.channelName3, False), (self.channelName4, True), (self.channelName5, True)]
            self.ChannelsSharedRepositoriesIAmAMemberOf = [(self.channelName1, False), (self.channelName2, True), (self.channelName3, False), (self.channelName4, False), (self.channelName5, True)]
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            self.get_element(self.common.channel.CHANNELS_PAGE_ALL_CHANNELS_LIST).text
            writeToLog("INFO","Step 1: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName1, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED create new channel: " + self.channelName1)
                return
             
            sleep(3)
            writeToLog("INFO","Step 2: Going to logout from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to logout from " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " user")
                return  
                                  
            writeToLog("INFO","Step 3: Going to login with user " + self.userName2)
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to login with " + self.userName2)
                return
               
            writeToLog("INFO","Step 4: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName3, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED create new channel: " + self.channelName3)
                return
              
            writeToLog("INFO","Step 5: Going to add user '" + self.userName1 +"' as manager to channel '" + self.channelName3 + "'")
            if self.common.channel.addMembersToChannel(self.channelName3, self.userName1, permission=enums.ChannelMemberPermission.MANAGER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to add user '" + self.userName1 + "' as manager to channel '" + self.channelName3 + "'")
                return
              
            sleep(3)
            writeToLog("INFO","Step 6: Going to logout from " + self.userName2 + " user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to logout from " + self.userName2 + " user")
                return  
                                  
            writeToLog("INFO","Step 7: Going to login with user " + self.userName3)
            if self.common.login.loginToKMS(self.userName3, self.userPass3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to login with " + self.userName3)
                return
              
            writeToLog("INFO","Step 8: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName4, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED create new channel: " + self.channelName4)
                return
  
            sleep(3)
            writeToLog("INFO","Step 9: Going to logout from " + self.userName3)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to logout from " + self.userName3)
                return  
                                 
            writeToLog("INFO","Step 10: Going to login with : " + self.userName4)
            if self.common.login.loginToKMS(self.userName4, self.userPass4) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to login with " + self.userName4)
                return
              
            writeToLog("INFO","Step 11: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName5, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.SHAREDREPOSITORY, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED create new channel: " + self.channelName5)
                return
  
            writeToLog("INFO","Step 12: Going to add user '" + self.userName1 +"' as manager to channel '" + self.channelName5 + "'")
            if self.common.channel.addMembersToChannel(self.channelName5, self.userName1, permission=enums.ChannelMemberPermission.MEMBER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to add user '" + self.userName1 + "' as manager to channel '" + self.channelName5 + "'")
                return
              
            sleep(3)
            writeToLog("INFO","Step 13: Going to logout from " + self.userName4)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to logout from " + self.userName4)
                return  
                                
            writeToLog("INFO","Step 14: Going to login with : " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to login with " + self.userName1)
                return
             
            writeToLog("INFO","Step 15: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName2, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.SHAREDREPOSITORY, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED create new channel: " + self.channelName2)
                return
             
            writeToLog("INFO","Step 16: Going navigate to my channels page")
            if self.common.channel.navigateToChannels(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED navigate to my channels page")
                return 
             
            writeToLog("INFO","Step 17: Going to add user '" + self.userName1 +"' as channel subscriber in '" + self.channelName1 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName1, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to add user '" + self.userName1 + "' as channel subscriber in '" + self.channelName1 + "'")
                return
             
            writeToLog("INFO","Step 18: Going to add user '" + self.userName1 +"' as channel subscriber in '" + self.channelName4 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName4, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to add user '" + self.userName1 + "' as channel subscriber in '" + self.channelName4 + "'")
                return
             
            writeToLog("INFO","Step 19: Going to add user '" + self.userName1 +"' as channel subscriber in '" + self.channelName5 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName5, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to add user '" + self.userName1 + "' as channel subscriber in '" + self.channelName5 + "'")
                return
            
            writeToLog("INFO","Step 20: Going navigate to my channels page")
            if self.common.channel.navigateToMyChannels() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED navigate to my channels page")
                return 
            
            writeToLog("INFO","Step 21: Going to filter view channel by 'Channels I Manage' and verify that only the correct channels display")
            if self.common.channel.verifyChannelsViaFilter("I Manage", self.channelsIManage) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to filter  and verify view channels by: channels I Manage")
                return 
            
            writeToLog("INFO","Step 22: Going to filter view channel by 'Channels I am a member of' and verify that only the correct channels display")
            if self.common.channel.verifyChannelsViaFilter("I am a member of", self.channelsIAmAMemberOf) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to filter and verify view channels by: Channels I am a member of")
                return 
            
            writeToLog("INFO","Step 23: Going to filter view channel by 'Channels I am subscribed to' and verify that only the correct channels display")
            if self.common.channel.verifyChannelsViaFilter("I am subscribed to", self.channelsIAmSubscribedTo) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to filter and verify  view channels by: Channels I am subscribed to")
                return 
            
            writeToLog("INFO","Step 24: Going to filter view channel by 'Shared Repositories I am a member of' and verify that only the correct channels display")
            if self.common.channel.verifyChannelsViaFilter("Shared Repositories I am a member of", self.ChannelsSharedRepositoriesIAmAMemberOf) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to filter and verify view channels by: Shared Repositories I am a member of")
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
            self.common.channel.deleteChannel(self.channelName2)
            sleep(2) 
            self.common.login.logOutOfKMS()
            self.common.loginAsUser() 
            self.common.channel.deleteChannel(self.channelName1)
            sleep(2)
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(self.userName2, self.userPass2)                   
            self.common.channel.deleteChannel(self.channelName3)
            sleep(2)
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(self.userName3, self.userPass3) 
            self.common.channel.deleteChannel(self.channelName4)
            sleep(2)
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(self.userName4, self.userPass4) 
            self.common.channel.deleteChannel(self.channelName5)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')