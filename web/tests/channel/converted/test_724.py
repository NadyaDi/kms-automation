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
    # Test description:

    #================================================================================================================================
    testNum = "724"
    
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
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
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
            self.channelName1 = clsTestService.addGuidToString("My Channels - Sort Channels A", self.testNum)
            self.channelName2 = clsTestService.addGuidToString("My Channels - Sort Channels B", self.testNum)
            self.channelName3 = clsTestService.addGuidToString("My Channels - Sort Channels C", self.testNum)
            self.channelName4 = clsTestService.addGuidToString("My Channels - Sort Channels D", self.testNum)
            
            self.entryName1 = clsTestService.addGuidToString("My Channels - Sort Channels 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Channels - Sort Channels 2", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("My Channels - Sort Channels 3", self.testNum)
            
            self.sortByMostRecent = (self.channelName4, self.channelName3, self.channelName2, self.channelName1)
            self.sortByAlphabetical = (self.channelName1, self.channelName2, self.channelName3, self.channelName4)
            self.sortByMembersAndSubscribers = (self.channelName3, self.channelName2, self.channelName1, self.channelName4)
            self.sortByMediaCount = (self.channelName2, self.channelName4, self.channelName1, self.channelName3)
            
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
              
            for i in range(1,5):
                writeToLog("INFO","Step " + str(i+1) + ": Going to create new channel '" + eval('self.channelName'+str(i)))            
                if self.common.channel.createChannel(eval('self.channelName'+str(i)), self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i+1) + ": FAILED create new channel: " + eval('self.channelName'+str(i)))
                    return
                   
            for i in range(1,4):
                writeToLog("INFO","Step " + str(i+5) + ": Going to upload new entey '" + eval('self.entryName'+str(i)))            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i)), self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i+5) + ": FAILED to upload new entry: " + eval('self.entryName'+str(i)))
                    return
                
            writeToLog("INFO","Step 9: Going to publish entry: " + self.entryName1)            
            if self.common.myMedia.publishSingleEntry(self.entryName1, "", (self.channelName1, self.channelName2, self.channelName4)) == False: 
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to publish entry: " + self.entryName1)
                return
              
            writeToLog("INFO","Step 10: Going to publish entry: " + self.entryName2)            
            if self.common.myMedia.publishSingleEntry(self.entryName2, "", (self.channelName2, self.channelName4)) == False: 
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to publish entry: " + self.entryName2)
                return
              
            writeToLog("INFO","Step 11: Going to publish entry: " + self.entryName3)            
            if self.common.myMedia.publishSingleEntry(self.entryName3, "", [(self.channelName2)]) == False: 
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to publish entry: " + self.entryName2)
                return
                  
            writeToLog("INFO","Step 12: Going to add user '" + self.userName2 +"' as member to channel '" + self.channelName2 + "'")
            if self.common.channel.addMembersToChannel(self.channelName2, self.userName2, permission=enums.ChannelMemberPermission.MEMBER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to add user '" + self.userName2 + "' as member to channel '" + self.channelName2 + "'")
                return
              
            writeToLog("INFO","Step 13: Going to add user '" + self.userName2 +"' as manager to channel '" + self.channelName3 + "'")
            if self.common.channel.addMembersToChannel(self.channelName3, self.userName2, permission=enums.ChannelMemberPermission.MEMBER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to add user '" + self.userName2 + "' as member to channel '" + self.channelName3 + "'")
                return
              
            sleep(3)
            writeToLog("INFO","Step 14: Going to logout from " + self.userName1 + " user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to logout from " + self.userName1 + " user")
                return  
                                    
            writeToLog("INFO","Step 15: Going to login with user " + self.userName3)
            if self.common.login.loginToKMS(self.userName3, self.userPass3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to login with " + self.userName3)
                return
              
            writeToLog("INFO","Step 16: Going to add user '" + self.userName3 +"' as channel subscriber in '" + self.channelName1 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName1, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to add user '" + self.userName3 + "' as channel subscriber in '" + self.channelName1 + "'")
                return
            
            sleep(2) 
            writeToLog("INFO","Step 17: Going to add user '" + self.userName3 +"' as channel subscriber in '" + self.channelName2 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName2, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to add user '" + self.userName3 + "' as channel subscriber in '" + self.channelName2 + "'")
                return
              
            writeToLog("INFO","Step 18: Going to add user '" + self.userName3 +"' as channel subscriber in '" + self.channelName3 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName3, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to add user '" + self.userName3 + "' as channel subscriber in '" + self.channelName3 + "'")
                return
              
            sleep(3)
            writeToLog("INFO","Step 19: Going to logout from " + self.userName3)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to logout from " + self.userName3)
                return  
                                   
            writeToLog("INFO","Step 20: Going to login with : " + self.userName4)
            if self.common.login.loginToKMS(self.userName4, self.userPass4) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to login with " + self.userName4)
                return
  
            writeToLog("INFO","Step 21: Going to add user '" + self.userName4 +"' as channel subscriber in '" + self.channelName3 + "'")
            if self.common.channel.subscribeUserToChannel(self.channelName3, "2" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to add user '" + self.userName4 + "' as channel subscriber in '" + self.channelName4 + "'")
                return
                
            sleep(3)
            writeToLog("INFO","Step 22: Going to logout from " + self.userName4)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to logout from " + self.userName4)
                return  
                                  
            writeToLog("INFO","Step 23: Going to login with : " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to login with " + self.userName1)
                return
              
            writeToLog("INFO","Step 24: Going navigate to my channels page")
            if self.common.channel.navigateToMyChannels(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED navigate to my channels page")
                return 
            
            writeToLog("INFO","Step 25: Going verify sort channels by 'Media Count'")
            if self.common.channel.verifySortInMyChannels("Media Count", self.sortByMediaCount) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED sort channels by 'Media Count'")
                return 
             
            writeToLog("INFO","Step 26: Going verify sort channels by 'Most Recent'")
            if self.common.channel.verifySortInMyChannels("Most Recent", self.sortByMostRecent) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED sort channels by 'Most Recent'")
                return 
             
            writeToLog("INFO","Step 27: Going verify sort channels by 'Alphabetical'")
            if self.common.channel.verifySortInMyChannels("Alphabetical", self.sortByAlphabetical) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED sort channels by 'Alphabetical'")
                return 
            
            writeToLog("INFO","Step 28: Going verify sort channels by 'Members & Subscribers'")
            if self.common.channel.verifySortInMyChannels("Members & Subscribers", ("AED7F26C-724-MY CHANNELS - SORT CHANNELS C", "AED7F26C-724-MY CHANNELS - SORT CHANNELS B", "AED7F26C-724-MY CHANNELS - SORT CHANNELS A", "AED7F26C-724-MY CHANNELS - SORT CHANNELS D")) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED sort channels by 'Members & Subscribers'")
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
            self.common.login.loginToKMS(self.userName1, self.userPass1)                   
            for i in range(1,5):
                self.common.channel.deleteChannel(eval('self.channelName'+str(i)))
             
            for i in range(1,4):
                self.common.myMedia.deleteSingleEntryFromMyMedia( eval('self.entryName'+str(i)))   
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')