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
    # Test Name : Entitlements - Open Channel using Global Page 
    # Test description:
    # 1. Create an Open Channel
    # 2. Publish an entry inside the Open Channel
    # 3. Add a member to the Open channel
    # 4. Verify that the Channel owner its able to find the private channel inside global search results
    # 5. Verify that the Anonymous user is unable to find the private channel, entry by tag and entry inside the global search results
    # 6. Verify that Normal KMS users is able to find the private channel, entry by tag and entry inside the global search results
    #================================================================================================================================
    testNum = "5025"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables

    typeTest            = "Entitlements for an Open Channel with Owner, Anonymous and Members users"
    
    anonymousUser       = "Anonymous User"
    normalUser          = "python_normal"
    memberUser          = "python_member"
    userPassword        = "Kaltura1!"
    
    description         = "Description"
    tags                = "Tags,"
    entryName           = None
    entryDescription    = "Open Entry Description"
    
    channelName         = None
    channelDescription  = "Open Channel Description"

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
            self.entryName             = clsTestService.addGuidToString("Entitlements - Open Channel", self.testNum)
            self.channelName           = clsTestService.addGuidToString("Open Channel", self.testNum)
            self.entryTags             = clsTestService.addGuidToString("entry,", self.testNum)
            self.channelTags           = clsTestService.addGuidToString("channel,", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to create " + self.channelName + " channel as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.channel.createChannel(self.channelName, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
                writeToLog("INFO","Step 1: FAILED to create " + self.channelName + " channel as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
              
            writeToLog("INFO","Step 2: Going to add " + self.memberUser + " as member of " + self.channelName)
            if self.common.channel.addMembersToChannel(self.channelName, self.memberUser, enums.ChannelMemberPermission.MEMBER) == False:
                writeToLog("INFO","Step 2: FAILED to add " + self.memberUser + " as member of " + self.channelName)
                return
   
            writeToLog("INFO","Step 3: Going to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 3: FAILED to upload " + self.entryName + " entry as " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME)
                return
        
            writeToLog("INFO","Step 4: Going to publish the " + self.entryName + " to the " + self.channelName)
            if self.common.myMedia.publishSingleEntry(self.entryName, "", self.channelName) == False:
                writeToLog("INFO","Step 4: FAILED to publish the " + self.entryName + " to the " + self.channelName)
                return
                          
            writeToLog("INFO","Step 5: Going to verify that for the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + ", the " + self.channelName + " channel is displayed in global search")
            if self.common.globalSearch.serchAndVerifyChannelInGlobalSearch(self.channelName) == False:
                writeToLog("INFO","Step 5: FAILED, the " + self.channelName + " channel hasn't been found in the global search results while it should")
                return
             
            writeToLog("INFO","Step 6: Going to move to Anonymous user")
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step 6: FAILED to move to Anonymous user")
                return
                          
            writeToLog("INFO","Step 7: Going to verify that for the " + self.anonymousUser + ", the " + self.channelName + " channel is not displayed in global search")
            if self.common.globalSearch.serchAndVerifyChannelInGlobalSearch(self.channelName) != False:
                writeToLog("INFO","Step 7: FAILED, the "+ self.channelName + " channel has been displayed in the global search results while it shouldn't")
                return
             
            writeToLog("INFO","Step 8: Going to verify that for the " + self.anonymousUser + " , the " + self.entryName + " entry is not displayed in global search")
            if self.common.globalSearch.serchAndVerifyEntryInGlobalSearch(self.entryName) != False:
                writeToLog("INFO","Step 8: FAILED, the "+ self.entryName + " entry has been displayed in the global search results while it shouldn't")
                return
            
            writeToLog("INFO","Step 9: Going to verify that the tag: " + self.entryTags + " , doesn't link to the " + self.entryName + " entry, or " + self.channelName + " channel in global search results")
            if self.common.globalSearch.serchAndVerifyTagsInGlobalSearch(self.entryTags, self.entryName, self.channelName) != False:
                writeToLog("INFO","Step 9: FAILED, the "+ self.entryTags + " linked to the " + self.entryName + " entry, or " + self.channelName + " channel in global search results")
                return
             
            writeToLog("INFO","Step 10: Going to authenticate with , " + self.normalUser + " normal KMS user")
            if self.common.login.loginToKMS(self.normalUser, self.userPassword) == False:
                writeToLog("INFO","Step 10: FAILED to authenticate with , " + self.normalUser + " normal KMS user")
                return
              
            writeToLog("INFO","Step 11: Going to verify that for the " + self.normalUser + ", the " + self.channelName + " channel is displayed in global search")
            if self.common.globalSearch.serchAndVerifyChannelInGlobalSearch(self.channelName) == False:
                writeToLog("INFO","Step 11: FAILED, the "+ self.channelName + " channel hasn't been found in the global search results while it should")
                return
             
            writeToLog("INFO","Step 12: Going to verify that for the " + self.normalUser + " , the " + self.entryName + " entry is displayed in global search")
            if self.common.globalSearch.serchAndVerifyEntryInGlobalSearch(self.entryName) == False:
                writeToLog("INFO","Step 12: FAILED, the " + self.entryName + " entry hasn't been found displayed in in the global search results while it should")
                return
            
            writeToLog("INFO","Step 13: Going to verify that the tag: " + self.entryTags + " , linked to the " + self.entryName + " entry, and " + self.channelName + " channel and that it's displayed in global search results")
            if self.common.globalSearch.serchAndVerifyTagsInGlobalSearch(self.entryTags, self.entryName, self.channelName) == False:
                writeToLog("INFO","Step 13: FAILED, the "+ self.channelName + " channel, and " + self.entryName + " entry couldn't be found in  Global Search results, while using " + self.entryTags + " tag")
                return 
            
            writeToLog("INFO","Step 14: Going to log out from " + self.normalUser + " and authenticate with " + self.memberUser)
            if self.common.login.logOutThenLogInToKMS(self.memberUser, self.userPassword) == False:
                writeToLog("INFO","Step 14: FAILED to log out from " + self.normalUser + " and authenticate with " + self.memberUser)
                return
            
            writeToLog("INFO","Step 15: Going to verify that for the " + self.memberUser + ", the " + self.channelName + " channel is displayed in global search")
            if self.common.globalSearch.serchAndVerifyChannelInGlobalSearch(self.channelName) == False:
                writeToLog("INFO","Step 15: FAILED, the " + self.channelName + " channel hasn't been found in the global search results while it should")
                return
             
            writeToLog("INFO","Step 16: Going to verify that for the " + self.memberUser + " , the " + self.entryName + " entry is displayed in global search")
            if self.common.globalSearch.serchAndVerifyEntryInGlobalSearch(self.entryName) == False:
                writeToLog("INFO","Step 16: FAILED, the " + self.entryName + " entry hasn't been found displayed in in the global search results while it should")
                return
            
            writeToLog("INFO","Step 17: Going to verify that the tag: " + self.entryTags + " , linked to the " + self.entryName + " entry, and " + self.channelName + " channel and that it's displayed in global search results")
            if self.common.globalSearch.serchAndVerifyTagsInGlobalSearch(self.entryTags, self.entryName, self.channelName) == False:
                writeToLog("INFO","Step 17: FAILED, the "+ self.channelName + " channel, and " + self.entryName + " entry couldn't be found in  Global Search results, while using " + self.entryTags + " tag")
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
            sleep(3)
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            sleep(3)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')