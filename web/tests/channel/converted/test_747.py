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
    # Test Name : Channel page - Shared Repository 
    # Test description:
    # create channel and set it as 'Shared Repository':
    #     Verify that :Membership is by invitation only. 
    #     Members can publish content from this channel to any other channel according to their entitlements.
    #================================================================================================================================
    testNum = "747"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    description = "Description"
    tags = "Tags,"
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    channelName1 = "Shared Repository channel"
    channelName2 = "Open Channel"

    
    

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
            self.entryName1 = clsTestService.addGuidToString("Channel page - Shared Repository 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Channel page - Shared Repository 2", self.testNum)
            self.channelName1 = clsTestService.addGuidToString(self.channelName1, self.testNum)
            self.channelName2 = clsTestService.addGuidToString(self.channelName2, self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName1, self.description, self.tags, enums.ChannelPrivacyType.SHAREDREPOSITORY, False, True, True) == False:
                writeToLog("INFO","Step 1: FAILED create new channel: " + self.channelName1)
                return
            
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, self.description, self.tags) == None:
                writeToLog("INFO","Step 2: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 3: Going to add entry to channel: " + self.channelName1)
            if self.common.channel.addExistingContentToChannel(self.channelName1, self.entryName1, False, publishFrom=enums.Location.MY_CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 2: FAILED to add entry '" + self.entryName1 + "' to channel '" + self.channelName1 + "'")
                return
            
            sleep(3)
            writeToLog("INFO","Step 4: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 4: FAILED to logout from main user")
                return  
                            
            writeToLog("INFO","Step 5: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                writeToLog("INFO","Step 5: FAILED to login with " + self.userName1)
                return       
                        
            writeToLog("INFO","Step 6: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName2, self.description, self.tags) == None:
                writeToLog("INFO","Step 6: FAILED to upload entry")
                return    
                        
            writeToLog("INFO","Step 7: Going to add entry to channel: " + self.channelName1)
            if self.common.channel.addExistingContentToChannel(self.channelName1, self.entryName2, False, publishFrom=enums.Location.CHANNELS_PAGE) == True:
                writeToLog("INFO","Step 7: FAILED, user can add content to 'shared repository channel' although the user isn't a member in the channel")
                return              
            writeToLog("INFO","Step 7 failed as expected: user '" + self.userName1 + "' isn't a member in channel '" + self.channelName1 + "' so he isn't able to add content")
                            
            writeToLog("INFO","Step 8: Going to create new channel")            
            if self.common.channel.createChannel(self.channelName2, self.description, self.tags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                writeToLog("INFO","Step 8: FAILED create new channel: " + self.channelName2)
                return               
                            
            sleep(3)
            writeToLog("INFO","Step 9: Going to logout from user: " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 9: FAILED to logout from user: " + self.userName1)
                return  
                            
            writeToLog("INFO","Step 10: Going to login with main user")
            if self.common.loginAsUser()  == False:
                writeToLog("INFO","Step 10: FAILED to login with main user")
                return                 
                            
            writeToLog("INFO","Step 11: Going to add user '" + self.userName1 +"' as member to channel '" + self.channelName1 + "'")
            if self.common.channel.addMembersToChannel(self.channelName1, self.userName1, permission=enums.ChannelMemberPermission.CONTRIBUTOR) == False:
                writeToLog("INFO","Step 11: FAILED to add user '" + self.userName1 + "' as contributor to channel '" + self.channelName1 + "'")
                return               
                            
            sleep(3)
            writeToLog("INFO","Step 12: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 12: FAILED to logout from main user")
                return  
                            
            writeToLog("INFO","Step 13: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                writeToLog("INFO","Step 13: FAILED to login with " + self.userName1)
                return                  
                   
            writeToLog("INFO","Step 14: Going to add entry to channel: " + self.channelName1)
            if self.common.channel.addExistingContentToChannel(self.channelName1, self.entryName2, False, publishFrom=enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 14: FAILED to add entry to channel '" + self.channelName1 + "'")
                return           
            
            writeToLog("INFO","Step 15: Going to add entry to channel: " + self.channelName2 + " from shared repository channel: " + self.channelName1)
            if self.common.channel.addExistingContentToChannel(self.channelName2, self.entryName1, False, publishFrom=enums.Location.CHANNELS_PAGE, channelType=enums.ChannelPrivacyType.SHAREDREPOSITORY, sharedReposiytyChannel=self.channelName1) == False:
                writeToLog("INFO","Step 15: FAILED to add entry from shared repository channel to channel '" + self.channelName2 + "'")
                return              
                            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: 'Channel page - Shared Repository'  was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName2)
            sleep(2) 
            self.common.login.logOutOfKMS()
            self.common.loginAsUser() 
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName1)
            self.common.apiClientSession.startCurrentApiClientSession()
            self.common.apiClientSession.deleteCategory(self.channelName1)
            self.common.apiClientSession.deleteCategory(self.channelName2)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')