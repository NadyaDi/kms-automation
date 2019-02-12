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
    #  @Author: Inbar Willman
    # Test Name : Sort by - Channels - when no search is made
    # Test description:
    # create several channels and add them member / subscriber/ media
    # go to channels page and sort the channels :
    #    1. Most Recent -  The channels' order should be from the last uploaded video to the first one.
    #    2. Alphabetical A-Z - The channels' order should be alphabetical A-Z
    #    3. Alphabetical Z-A - The channels' order should be alphabetical Z-A
    #    4. Members & Subscribers - The channels' order should be descending by members number
    #    5. Media Count - The channels' order should be the channel with most media first
    #================================================================================================================================
    testNum = "4310"
    
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
    channelName = None
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryDescription = "Description"
    entryTags = "Tags,"
    searchInMyChannels = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    channelDescription = "Description"
    channelTags = "Tags,"
    userName1 = "inbar.willman@kaltura.com"
    userPass1 = "Kaltura1!"
    userName2 = "private"
    userPass2 = "123456"
    userName3 = "admin"
    userPass3 = "123456"
    userName4 = "unmod"
    userPass4 = "123456"
    sortByMostRecent = None
    sortByAlphabetical = None
    sortByMembersAndSubscribers = None
    sortByMediaCount = None
    
    

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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            self.channelName1 = clsTestService.addGuidToString("Channels - Sort Channels A", self.testNum)
            self.channelName2 = clsTestService.addGuidToString("Channels - Sort Channels B", self.testNum)
            self.channelName3 = clsTestService.addGuidToString("Channels - Sort Channels C", self.testNum)
            self.channelName4 = clsTestService.addGuidToString("Channels - Sort Channels D", self.testNum)
            
            self.entryName1 = clsTestService.addGuidToString("Channels - Sort Channels 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("Channels - Sort Channels 2", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("Channels - Sort Channels 3", self.testNum)
            
            self.searchInMyChannels = ("My Channels - Sort Channels")
            
            self.sortByMostRecent = ("My Channels - Sort Channels D", "My Channels - Sort Channels C", "My Channels - Sort Channels B", "My Channels - Sort Channels A")
            self.sortByAlphabetical = ("My Channels - Sort Channels A", "My Channels - Sort Channels B", "My Channels - Sort Channels C", "My Channels - Sort Channels D")
            self.sortByMembersAndSubscribers = ("My Channels - Sort Channels C", "My Channels - Sort Channels B", "My Channels - Sort Channels A", "My Channels - Sort Channels D")
            self.sortByMediaCount = ("My Channels - Sort Channels B", "My Channels - Sort Channels D", "My Channels - Sort Channels A", "My Channels - Sort Channels C")
            self.sortByAlphabeticalZToA = ("My Channels - Sort Channels D", "My Channels - Sort Channels C", "My Channels - Sort Channels B", "My Channels - Sort Channels A")
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
                
            writeToLog("INFO","Step 2: Going navigate to channels page")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_KMS_CHANNELS_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to channels page")
                return 
            
            writeToLog("INFO","Step 3: Going to verify default sort before making a search")
#             if self.common.channel.verifyChannelsDefaultSort(enums.ChannelsSortBy.MEDIA_COUNT_NEWUI) == False:
            if self.common.channel.verifyChannelsDefaultSort(enums.ChannelsSortBy.MEDIA_COUNT) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to displayed correct default sort before making a search")
                return                                 
               
            writeToLog("INFO","Step 4: Going verify sort channels by 'Creation Date'")
            if self.common.channel.verifySortInMyChannels(enums.ChannelsSortBy.CREATION_DATE, self.sortByMostRecent) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED sort channels by 'Creation Date'")
                return 

            writeToLog("INFO","Step 5: Going verify sort channels by 'Media Count'")
#             if self.common.channel.verifySortInMyChannels(enums.ChannelsSortBy.MEDIA_COUNT_NEWUI,  self.sortByMediaCount) == False:
            if self.common.channel.verifySortInMyChannels(enums.ChannelsSortBy.MEDIA_COUNT,  self.sortByMediaCount) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED sort channels by 'Media Count'")
                return 
                  
            writeToLog("INFO","Step 6: Going verify sort channels by 'Alphabetical A-Z'")
            if self.common.channel.verifySortInMyChannels(enums.ChannelsSortBy.ALPHABETICAL_NEWUI, self.sortByAlphabetical) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED sort channels by 'Alphabetical A-Z'")
                return 
                
            writeToLog("INFO","Step 7: Going verify sort channels by 'Alphabetical Z-A'")
            if self.common.channel.verifySortInMyChannels(enums.ChannelsSortBy.ALPHABETICAL_Z_A_NEWUI, self.sortByAlphabeticalZToA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED sort channels by 'Alphabetical Z-A'")
                return 
                 
            writeToLog("INFO","Step 8: Going verify sort channels by 'Members & Subscribers'")
            if self.common.channel.verifySortInMyChannels(enums.ChannelsSortBy.MEMBERS_AND_SUBSCRIBERS, self.sortByMembersAndSubscribers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED sort channels by 'Members & Subscribers'")
                return 
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Channels - Sort Channels without search' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
#             sleep(2)
#             self.common.login.logOutOfKMS()
#             self.common.login.loginToKMS(self.userName1, self.userPass1)                   
#             for i in range(1,5):
#                 self.common.channel.deleteChannel(eval('self.channelName'+str(i)))
#      
#             self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3])   
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')