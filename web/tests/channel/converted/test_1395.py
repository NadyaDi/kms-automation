import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
from upload import UploadEntry


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test Name : Channel Type (Open / Restricted / Private)
    # Test description:
    # Create 3 Channels : Open / Restricted / Private
    # For open channel : Membership is open ans non-members can view content and participate.
    #                     Everyone can view and add content
    # For restricted channel : Non-members can view content, but users must be invited to participate.
    #                           Everyone can view content, but only members (contributors and above) can add content.
    # For private channel: Membership is by invitation only and only members can view content and participate.
    #                       Only members can view and add content.
    #                       Non-members cannot see and search for the channel.
    #================================================================================================================================
    testNum = "1395"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    description = "Description"
    tags = "Tags,"
    openChannelName = None
    restrictedChannelName = None
    privateChannelName = None
    filePath= localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg' 
    userName = "Automation_User_1"
    userPass = "Kaltura1!"

    
    
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
            self.openChannelName = clsTestService.addGuidToString("Channels Type - Open Channel", self.testNum)
            self.restrictedChannelName = clsTestService.addGuidToString("Channels Type - Restricted Channel", self.testNum)
            self.privateChannelName = clsTestService.addGuidToString("Channels Type - Private Channel", self.testNum)
            self.entryName1 = clsTestService.addGuidToString("Channels Type - Open Channel", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Channels Type - Restricted Channel", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("Channels Type - Private Channel", self.testNum)
            self.entry1 = UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
            self.entry2 = UploadEntry(self.filePath, self.entryName2, self.description, self.tags, timeout=60, retries=3)
            self.entry3 = UploadEntry(self.filePath, self.entryName3, self.description, self.tags, timeout=60, retries=3)            
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create open channel") 
            if self.common.channel.createChannel(self.openChannelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, False) == False:
                writeToLog("INFO","Step 1: FAILED to create open channel")
                return
             
            writeToLog("INFO","Step 2: Going to create restricted channel") 
            if self.common.channel.createChannel(self.restrictedChannelName, self.description, self.tags, enums.ChannelPrivacyType.RESTRICTED, False, True, False) == False:
                writeToLog("INFO","Step 2: FAILED to create restricted channel")
                return
             
            writeToLog("INFO","Step 3: Going to create private channel") 
            if self.common.channel.createChannel(self.privateChannelName, self.description, self.tags, enums.ChannelPrivacyType.PRIVATE, False, True, False) == False:
                writeToLog("INFO","Step 3: FAILED to create private channel")
                return
            
            sleep(2)
            writeToLog("INFO","Step 4: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 4: FAILED to logout from main user")
                return  
                              
            writeToLog("INFO","Step 5: Going to login with user " + self.userName)
            if self.common.login.loginToKMS(self.userName, self.userPass) == False:
                writeToLog("INFO","Step 5: FAILED to login with " + self.userName)
                return       
             
            writeToLog("INFO","Step 6: Going to add media to open channel with non member user")
            if self.common.channel.addNewContentToChannel(self.openChannelName, self.entry1, navigateFrom=enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 6: FAILED to add media to open channel")
                return
            sleep(3)
                        
            writeToLog("INFO","Step 7: Going to verify entry found in channel")
            if self.common.channel.searchEntryInChannel(self.entryName1) == False:
                writeToLog("INFO","Step 7: FAILED to find entry '" + self.entryName1 + "' in channel: " + self.openChannelName)
                return
             
            writeToLog("INFO","Step 8: Going to add content to restricted channel with non member user")
            if self.common.channel.addNewContentToChannel(self.restrictedChannelName, self.entry2, navigateFrom=enums.Location.CHANNELS_PAGE) == True:
                writeToLog("INFO","Step 8: FAILED, user is non member in restricted channel and should NOT have permission to add content")
                return
            writeToLog("INFO","Step 8: preview step failed as expected: user is non member in restricted channel and should NOT have permission to add content")
             
            writeToLog("INFO","Step 9: Going to add content to private channel with non member user")
            if self.common.channel.addNewContentToChannel(self.privateChannelName, self.entry3, navigateFrom=enums.Location.CHANNELS_PAGE) == True:
                writeToLog("INFO","Step 9: FAILED, user is non member in private channel and should NOT have permission to add content")
                return
            writeToLog("INFO","Step 9: preview step failed as expected: user is non member in private channel and can NOT find the channel")
             
            sleep(2)
            writeToLog("INFO","Step 10: Going to logout from '" + self.userName + "' user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 10: FAILED to logout from '" + self.userName + "' user")
                return  
             
            writeToLog("INFO","Step 11: Going to login with main user")
            if self.common.loginAsUser()== False:
                writeToLog("INFO","Step 11: FAILED to login with main user")
                return 
             
            writeToLog("INFO","Step 12: Going to add user as member in channel: " + self.restrictedChannelName)
            if self.common.channel.addMembersToChannel(self.restrictedChannelName, self.userName, permission=enums.ChannelMemberPermission.CONTRIBUTOR) == False:
                writeToLog("INFO","Step 12: FAILED to add user '"+ self.userName + "' as a member in channel: " + self.restrictedChannelName)
                return
            
            writeToLog("INFO","Step 13: Going to add user as member in channel: " + self.privateChannelName)
            if self.common.channel.addMembersToChannel(self.privateChannelName, self.userName, permission=enums.ChannelMemberPermission.CONTRIBUTOR) == False:
                writeToLog("INFO","Step 13: FAILED to add user '"+ self.userName + "' as a member in channel: " + self.privateChannelName)
                return
            
            sleep(2)
            writeToLog("INFO","Step 14: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 14: FAILED to logout from main user")
                return  
                              
            writeToLog("INFO","Step 15: Going to login with user " + self.userName)
            if self.common.login.loginToKMS(self.userName, self.userPass) == False:
                writeToLog("INFO","Step 15: FAILED to login with " + self.userName)
                return       
             
            writeToLog("INFO","Step 18: Going to add media to restricted channel with member user")
            if self.common.channel.addNewContentToChannel(self.restrictedChannelName, self.entry2, navigateFrom=enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 18: FAILED, user is a member in restricted channel and should have permission to add content")
                return
            sleep(3)
            
            writeToLog("INFO","Step 19: Going to verify entry found in channel")
            if self.common.channel.searchEntryInChannel(self.entryName2, ) == False:
                writeToLog("INFO","Step 19: FAILED to find entry '" + self.entryName2 + "' in channel: " + self.restrictedChannelName)
                return
             
            writeToLog("INFO","Step 20: Going to add media to private channel with member user")
            if self.common.channel.addNewContentToChannel(self.privateChannelName, self.entry3, navigateFrom=enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 20: FAILED, user is a member in private channel and should have permission to add content")
                return
            sleep(3)
            
            writeToLog("INFO","Step 21: Going to verify entry found in channel")
            if self.common.channel.searchEntryInChannel(self.entryName3) == False:
                writeToLog("INFO","Step 21: FAILED to find entry '" + self.entryName3 + "' in channel: " + self.privateChannelName)
                return
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Channels Type' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")        
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(self.userName, self.userPass)
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3])   
            self.common.login.logOutOfKMS()
            self.common.loginAsUser()
            self.common.channel.deleteChannel(self.openChannelName)
            self.common.channel.deleteChannel(self.restrictedChannelName)
            self.common.channel.deleteChannel(self.privateChannelName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')