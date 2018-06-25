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
    # Test Name : Channel page - Enable subscription in channel 
    # Test description:
    # create new channel and then go edit page and check the option: 'Enable subscription to channel'. Click on 'Save'
    # login with non-member user of the channel and click on 'Subscribed' - user subscribed to the channel
    # As a contributor in the channel, add new media to the channel - user can add content 
    #================================================================================================================================
    testNum = "741"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    channelName = None
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    userName2 = "Automation_User_2"
    userPass2 = "Kaltura1!"

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
            self.entryName = clsTestService.addGuidToString("Channel page Enable subscription in channel", self.testNum)
            self.channelName = clsTestService.addGuidToString("Channel page Enable subscription in channel", self.testNum)
            #self.channelName= [(self.channelName)]
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
        
            writeToLog("INFO","Step 1: Going to enable channel subscription module")            
            if self.common.admin.enableChannelSubscription(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to enable channel subscription module")
                return
            
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
            
            writeToLog("INFO","Step 3: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName, self.entryDescription, self.entryTags, enums.ChannelPrivacyType.OPEN, False, True, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED create new channel")
                return
             
            writeToLog("INFO","Step 4: Going to add member to channel")
            if self.common.channel.addMembersToChannel(self.channelName, self.userName2, permission = enums.ChannelMemberPermission.MEMBER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add user '" + self.userName2 + "' as member to channel '" + self.channelName + "'")
                return
             
            sleep(2)
            writeToLog("INFO","Step 5: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to logout from main user")
                return  
                                
            writeToLog("INFO","Step 6: Going to login with non member user to subscribe to channel")
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to login with user: " + self.userName1)
                return
             
            writeToLog("INFO","Step 7: Going to add non member user as subscriber to channel")
            if self.common.channel.subscribeUserToChannel(self.channelName, "1", enums.Location.CHANNELS_PAGE) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED, user '" + self.userName1 + "' was able to subscriber to channel '" + self.channelName + "' although channel subscription is disable")
                return 
            writeToLog("INFO","Step 7: This step has failed as expected, channel '" + self.channelName +"' don't have the subscription option") 
            
            sleep(2)
            writeToLog("INFO","Step 8: Going to logout from user: " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to logout from user: " + self.userName1)
                return  
                                
            writeToLog("INFO","Step 9: Going to login with main user")
            if self.common.loginAsUser()   == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to login with main user")
                return
             
            writeToLog("INFO","Step 10: Going to enable channel subscription") 
            if self.common.channel.enableDisableSubscriptionOptionToChannel(self.channelName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to enable channel subscription")
                return
                
            sleep(2)
            writeToLog("INFO","Step 11: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to logout from main user")
                return  
                                
            writeToLog("INFO","Step 12: Going to login with non member user to subscribe to channel")
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to login with user: " + self.userName1)
                return
            
            writeToLog("INFO","Step 13: Going to add non member user as subscriber to channel")
            if self.common.channel.subscribeUserToChannel(self.channelName, "1", enums.Location.CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to add non member user '" + self.userName1 + "' as subscriber to channel '" + self.channelName + "'")
                return
            
            writeToLog("INFO","Step 14: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 14: Going to add entry to channel: " + self.channelName)
            if self.common.channel.addContentToChannel(self.channelName, self.entryName, False, publishFrom=enums.Location.CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to add entry '" + self.entryName + "' to channel '" + self.channelName + "'")
                return
            
            sleep(2)
            writeToLog("INFO","Step 16: Going to logout from user: " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to logout from  user: " + self.userName1)
                return  
                               
            writeToLog("INFO","Step 17: Going to login with member user '" + self.userName2 +"' to subscribe to channel")
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to login with user: " + self.userName2)
                return
            
            writeToLog("INFO","Step 18: Going to add member user as subscriber to channel")
            if self.common.channel.subscribeUserToChannel(self.channelName, "2", enums.Location.CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to add member user '" + self.userName1 + "' as subscriber to channel '" + self.channelName + "'")
                return
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Channel page Enable subscription in channel")
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
            self.common.login.loginToKMS(self.userName1, self.userPass1)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            sleep(2)
            self.common.login.logOutOfKMS()   
            self.common.loginAsUser()                
            self.common.channel.deleteChannel(self.channelName[0])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')