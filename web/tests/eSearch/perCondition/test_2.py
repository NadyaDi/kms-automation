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
    # Test Name : Setup test for eSearch
    # Test description:
    # Creating new channels for sort by in channels/my channels
    #================================================================================================================================
    testNum = "2"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    filePathForSortBy = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    channelDescription = "Description"
    channelTags = "Tags,"
    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!"
    userName2 = "private"
    userPass2 = "123456"
    userName3 = "admin"
    userPass3 = "123456"
    userName4 = "unmod"
    userPass4 = "123456"
    userName5 = "adminForEsearch"
    userPass5 = "123456" 
    userName6 = "privateForEsearch"
    userPass6 = "123456"    
    userName7 = "unmodForEsearch"
    userPass7 = "123456"  
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
            #Channels for sort by in Channels/My channels
            self.channelName1 = "My Channels - Sort Channels A"
            self.channelName2 = "My Channels - Sort Channels B"
            self.channelName3 = "My Channels - Sort Channels C"
            self.channelName4 = "My Channels - Sort Channels D"
            
            # Entries to publish to channels for sort by in Channels/My channels 
            self.entryName1 = "My Channels - Sort Channels 1"
            self.entryName2 = "My Channels - Sort Channels 2"
            self.entryName3 = "My Channels - Sort Channels 3"
            
            # Search for sort by in channels/my channels
            self.searchInMyChannels = "My Channels - Sort Channels"
            
            # List of expected sort by order in sort by in channels/my channels/galleries
            self.sortByMostRecent = (self.channelName4, self.channelName3, self.channelName2, self.channelName1)
            self.sortByAlphabetical = (self.channelName1, self.channelName2, self.channelName3, self.channelName4)
            self.sortByMembersAndSubscribers = (self.channelName3, self.channelName2, self.channelName1, self.channelName4)
            self.sortByMediaCount = (self.channelName2, self.channelName4, self.channelName1, self.channelName3)
            self.sortByAlphabeticalZToA = (self.channelName4, self.channelName3, self.channelName2, self.channelName1)
            ##################### TEST STEPS - MAIN FLOW #############################################################  
            # Create channels for sort by in channels/My channels
            writeToLog("INFO","Creating channels for sort by in channels/My channels")
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
                writeToLog("INFO","Step " + str(i+5) + ": Going to upload new entry '" + eval('self.entryName'+str(i)))            
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
 
            writeToLog("INFO","Channels for sort by in channels/My channels tests were uploaded successfully")
            #################################################################################

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