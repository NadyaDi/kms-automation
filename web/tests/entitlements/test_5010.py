import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections


class Test:

    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Entitlements - Restricted Channel using Channels Page 
    # Test description:
    # 1. Create a Restricted Channel
    # 2. Publish an entry inside the Private Channel
    # 3. Add a member and a contributor to the Restricted channel
    # 4. Verify that the Channel owner has full control over the Restricted channel
    # 5. Verify that the Anonymous user is unable to enter to the Restricted Channel
    # 6. Verify that Logged in KMS users are able to access the Restricted Channel
    # 7. Verify that Member users are able to access the Restricted Channel but unable to add new content
    # 8. Verify that Contributor users are able to access the Restricted Channel and add new content
    #================================================================================================================================
    testNum = "5010"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables

    typeTest            = "Entitlements of a Restricted Channel with Owner, Anonymous, Members and Contributor users"
    
    normalUser          = "python_normal"
    memberUser          = "python_member"
    contributorUser     = "python_contributor"
    userPassword        = "Kaltura1!"
    
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "Restricted Entry Description"
    entryTags           = "restricted,"
    
    channelName         = None
    channelDescription  = "Restricted Channel Description"
    channelTags         = "restricted,"

    # Variables used in order to create a video entry with Slides and Captions
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'    
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
            # Variables used in order to proper create the Entry
            self.entryName             = clsTestService.addGuidToString("Entitlements - Restricted Channel", self.testNum)
            self.channelName           = clsTestService.addGuidToString("Restricted Channel", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to create " + self.channelName + " channel as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.RESTRICTED, True, True, True) == False:
                writeToLog("INFO","Step 1: FAILED to create " + self.channelName + " channel as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
              
            writeToLog("INFO","Step 2: Going to add " + self.memberUser + " as member of " + self.channelName)
            if self.common.channel.addMembersToChannel(self.channelName, self.memberUser, enums.ChannelMemberPermission.MEMBER) == False:
                writeToLog("INFO","Step 2: FAILED to add " + self.memberUser + " as member of " + self.channelName)
                return
             
            writeToLog("INFO","Step 3: Going to add " + self.contributorUser + " as contributor of " + self.channelName)
            if self.common.channel.addMembersToChannel(self.channelName, self.contributorUser, enums.ChannelMemberPermission.CONTRIBUTOR) == False:
                writeToLog("INFO","Step 3: FAILED to add " + self.contributorUser + " as contributor of " + self.channelName)
                return
   
            writeToLog("INFO","Step 4: Going to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 4: FAILED to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
        
            writeToLog("INFO","Step 5: Going to publish the " + self.entryName + " to the " + self.channelName)
            if self.common.myMedia.publishSingleEntry(self.entryName, "", self.channelName) == False:
                writeToLog("INFO","Step 5: FAILED to publish the " + self.entryName + " to the " + self.channelName)
                return
                          
            writeToLog("INFO","Step 6: Going to navigate as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " to the " + self.channelName + " channel from Channels Page and access the Add To Channel Tab")
            if self.common.channel.navigateToAddToChannel(self.channelName, enums.Location.MY_CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 6: FAILED to navigate as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " to the " + self.channelName + " channel from Channels Page and access the Add To Channel Tab")
                return
             
            writeToLog("INFO","Step 7: Going to move to Anonymous user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 7: FAILED to move to Anonymous user")
                return
             
            writeToLog("INFO","Step 8: Going to verify that Anonymous user is able to access the Channels Page")
            if self.common.channel.navigateToChannels() == False:
                writeToLog("INFO","Step 8: FAILED to verify that Anonymous user is able to access the Channels Page")
                return  
             
            writeToLog("INFO","Step 9: Going to verify that Anonymous user is unable to access " + self.channelName)
            if self.common.channel.navigateToChannel(self.channelName, enums.Location.CHANNELS_PAGE) == True:
                writeToLog("INFO","Step 9: FAILED to verify that Anonymous user is unable to access " + self.channelName)
                return
             
            writeToLog("INFO","Step 10: Going to authenticate with , " + self.normalUser + " normal KMS user")
            if self.common.login.loginToKMS(self.normalUser, self.userPassword) == False:
                writeToLog("INFO","Step 10: FAILED to authenticate with , " + self.normalUser + " normal KMS user")
                return
             
            writeToLog("INFO","Step 11: Going to verify that Normal user " + self.normalUser + "  is able to access " + self.channelName + " and enter in " + self.entryName)
            if self.common.channel.navigateToEntryFromChannel(self.channelName, self.entryName, enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 11: FAILED to verify that Normal user " + self.normalUser + "  is able to access " + self.channelName + " and enter in " + self.entryName)
                return
            
            writeToLog("INFO","Step 12: Going to verify that Normal user " + self.normalUser + "  is unable to access the 'Add Media Tab' from" + self.channelName)
            if self.common.channel.navigateToAddToChannel(self.channelName, enums.Location.CHANNELS_PAGE) == True:
                writeToLog("INFO","Step 12: FAILED to verify that Normal user " + self.normalUser + "  is unable to access the 'Add Media Tab' from " + self.channelName)
                return
            
            writeToLog("INFO","Step 13: Going to log out from " + self.normalUser)
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 13: FAILED to log out from " + self.normalUser)
                return
            
            writeToLog("INFO","Step 14: Going to authenticate with , " + self.memberUser + " member KMS user")
            if self.common.login.loginToKMS(self.memberUser, self.userPassword) == False:
                writeToLog("INFO","Step 14: FAILED to authenticate with , " + self.memberUser + " member KMS user")
                return
            
            writeToLog("INFO","Step 15: Going to verify that Member user " + self.memberUser + "  is able to access " + self.channelName + " and enter in " + self.entryName)
            if self.common.channel.navigateToEntryFromChannel(self.channelName, self.entryName, enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 15: FAILED to verify that Member user " + self.memberUser + "  is able to access " + self.channelName + " and enter in " + self.entryName)
                return
            
            writeToLog("INFO","Step 16: Going to verify that Member user " + self.memberUser + "  is unable to access the 'Add Media Tab' from" + self.channelName)
            if self.common.channel.navigateToAddToChannel(self.channelName, enums.Location.CHANNELS_PAGE) == True:
                writeToLog("INFO","Step 16: FAILED to verify that Member user " + self.memberUser + "  is unable to access the 'Add Media Tab' from" + self.channelName)
                return
            
            writeToLog("INFO","Step 17: Going to log out from " + self.memberUser)
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 17: FAILED to log out from " + self.memberUser)
                return
            
            writeToLog("INFO","Step 18: Going to authenticate with , " + self.contributorUser + " normal KMS user")
            if self.common.login.loginToKMS(self.contributorUser, self.userPassword) == False:
                writeToLog("INFO","Step 18: FAILED to authenticate with , " + self.contributorUser + " normal KMS user")
                return
            
            writeToLog("INFO","Step 19: Going to verify that Contributor user " + self.contributorUser + "  is able to access " + self.channelName + " and enter in " + self.entryName)
            if self.common.channel.navigateToEntryFromChannel(self.channelName, self.entryName, enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 19: FAILED to verify that Contributor user " + self.contributorUser + "  is able to access " + self.channelName + " and enter in " + self.entryName)
                return
            
            writeToLog("INFO","Step 20: Going to verify that Contributor user " + self.contributorUser + "  is able to access the 'Add Media Tab' from" + self.channelName)
            if self.common.channel.navigateToAddToChannel(self.channelName, enums.Location.CHANNELS_PAGE) == False:
                writeToLog("INFO","Step 20: FAILED to verify that Contributor user " + self.contributorUser + "  is able to access the 'Add Media Tab' from " + self.channelName)
                return
            ##################################################################
            self.status="Pass"
            writeToLog("INFO","TEST PASSED: " + self.typeTest)
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.login.logOutOfKMS()
            self.common.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
            self.common.channel.deleteChannel(self.channelName)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')