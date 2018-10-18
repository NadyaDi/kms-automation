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
    # Creating new entries and channels for eSearch test
    #================================================================================================================================
    testNum = "1"
    
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
    filePathForSortBy = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
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
            ######## Setting channels/my channels/galleries sort by data #########
            self.channelName1 = clsTestService.addGuidToString("My Channels - Sort Channels A", self.testNum)
            self.channelName2 = clsTestService.addGuidToString("My Channels - Sort Channels B", self.testNum)
            self.channelName3 = clsTestService.addGuidToString("My Channels - Sort Channels C", self.testNum)
            self.channelName4 = clsTestService.addGuidToString("My Channels - Sort Channels D", self.testNum)
            
            self.entryName1 = clsTestService.addGuidToString("My Channels - Sort Channels 1", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Channels - Sort Channels 2", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("My Channels - Sort Channels 3", self.testNum)
            
            self.searchInMyChannels = clsTestService.addGuidToString("My Channels - Sort Channels", self.testNum)
            
            self.sortByMostRecent = (self.channelName4, self.channelName3, self.channelName2, self.channelName1)
            self.sortByAlphabetical = (self.channelName1, self.channelName2, self.channelName3, self.channelName4)
            self.sortByMembersAndSubscribers = (self.channelName3, self.channelName2, self.channelName1, self.channelName4)
            self.sortByMediaCount = (self.channelName2, self.channelName4, self.channelName1, self.channelName3)
            self.sortByAlphabeticalZToA = (self.channelName4, self.channelName3, self.channelName2, self.channelName1)
            ####################################################################
            
            ######## Setting entries, categories and channels for sort by tests #########
            self.entryForSortBy1 = clsTestService.addGuidToString("Sort by - Sort A", self.testNum)
            self.entryForSortBy2 = clsTestService.addGuidToString("Sort by - Sort B", self.testNum)
            self.entryForSortBy3 = clsTestService.addGuidToString("Sort by - Sort C", self.testNum)
            self.entryForSortBy4 = clsTestService.addGuidToString("Sort by - Sort D", self.testNum)
            self.entryForSortBy5 = clsTestService.addGuidToString("Sort by - Sort E", self.testNum)
            self.entryForSortBy6 = clsTestService.addGuidToString("Sort by - Sort F", self.testNum)
            self.entryForSortBy7 = clsTestService.addGuidToString("Sort by - Sort G", self.testNum)
            self.entryForSortBy8 = clsTestService.addGuidToString("Sort by - Sort H", self.testNum)
            self.entryForSortBy9 = clsTestService.addGuidToString("Sort by - Sort I", self.testNum)
            self.entryForSortBy10 = clsTestService.addGuidToString("Sort by - Sort J", self.testNum)
            self.entryForSortBy11 = clsTestService.addGuidToString("Sort by Scheduling - Future", self.testNum)
            self.entryForSortBy12 = clsTestService.addGuidToString("Sort by Scheduling - In scheduling", self.testNum)
            self.entryForSortBy13 = clsTestService.addGuidToString("Sort by Scheduling - Past", self.testNum)
            
            # For sort in channel/ gallery/ add to channel/gallery pages
            self.categoryForEsearch = 'Apps Automation Category'
            self.channelForEsearch  = clsTestService.addGuidToString("Channel for sort by", self.testNum)
            self.channelForEsearchDescription = "channel for eSearch sort by tests"
            self.channelForEsearchTags = 'channel tag,'
            self.channelForEsearchPrivacy = 'open'
            
            # For sort by in pending tab in channel and category
            self.categoryForModerator = 'category for eSearch moderator'
            self.channelForModerator = clsTestService.addGuidToString("channel moderator for eSearch", self.testNum)
            
            # For sort in add to channel/gallery SR tab
            self.SrChannelForEsearch = clsTestService.addGuidToString("SR Channel for eSearch", self.testNum)
            
            self.entryPastStartDate = (datetime.datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
            self.entryTodayStartDate = datetime.datetime.now().strftime("%d/%m/%Y")
            self.entryFutureStartDate = (datetime.datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y")
        
            self.entryFutureStartTime = time.time() + (60*60)
            self.entryFutureStartTime= time.strftime("%I:%M %p",time.localtime(self.entryFutureStartTime))
             
            self.entryPastStartTime = time.time() - (60*60)
            self.entryPastStartTime= time.strftime("%I:%M %p",time.localtime(self.entryPastStartTime))
            
            self.sortEntriesByCreationDateDescending = (self.entryForSortBy10, self.entryForSortBy9, self.entryForSortBy8, self.entryForSortBy7, self.entryForSortBy6,
                                                        self.entryForSortBy5, self.entryForSortBy4, self.entryForSortBy3, self.entryForSortBy2, self.entryForSortBy1)
            self.sortEntriesByCreationDateAscending = (self.entryForSortBy1, self.entryForSortBy2, self.entryForSortBy3, self.entryForSortBy4, self.entryForSortBy4,
                                                       self.entryForSortBy5, self.entryForSortBy6, self.entryForSortBy7, self.entryForSortBy8, self.entryForSortBy9, self.entryForSortBy10)
            ##################### TEST STEPS - MAIN FLOW ############################################################# 
            ############### Create categories for pending tests##############################  
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return  
            
            writeToLog("INFO","Step 2 : Going to create new channel '" + self.channelForModerator)            
            if self.common.channel.createChannel(self.channelForModerator, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED create new channel: " + self.channelForModerator)
                return   
            
            writeToLog("INFO","Step 3 : Going to add member to channel:" + self.userName1)            
            if self.common.channel.addMembersToChannel(self.channelForModerator, self.userName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to add member to channel:" + self.userName1)
                return   
            ######### Creating channels for Sort by in channels/My channels/galleries tests: 3901, 4309 and 4310 #####
#             writeToLog("INFO","Creating channels data for the next tests: 3901, 4309, 4310")
#             writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
#             if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
#                 return
#                  
#             for i in range(1,5):
#                 writeToLog("INFO","Step " + str(i+1) + ": Going to create new channel '" + eval('self.channelName'+str(i)))            
#                 if self.common.channel.createChannel(eval('self.channelName'+str(i)), self.channelDescription, self.channelTags, enums.ChannelPrivacyType.OPEN, False, True, True) == False:
#                     self.status = "Fail"
#                     writeToLog("INFO","Step " + str(i+1) + ": FAILED create new channel: " + eval('self.channelName'+str(i)))
#                     return
#                        
#             for i in range(1,4):
#                 writeToLog("INFO","Step " + str(i+5) + ": Going to upload new entry '" + eval('self.entryName'+str(i)))            
#                 if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i)), self.entryDescription, self.entryTags) == None:
#                     self.status = "Fail"
#                     writeToLog("INFO","Step " + str(i+5) + ": FAILED to upload new entry: " + eval('self.entryName'+str(i)))
#                     return
#                     
#             writeToLog("INFO","Step 9: Going to publish entry: " + self.entryName1)            
#             if self.common.myMedia.publishSingleEntry(self.entryName1, "", (self.channelName1, self.channelName2, self.channelName4)) == False: 
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 9: FAILED to publish entry: " + self.entryName1)
#                 return
#                   
#             writeToLog("INFO","Step 10: Going to publish entry: " + self.entryName2)            
#             if self.common.myMedia.publishSingleEntry(self.entryName2, "", (self.channelName2, self.channelName4)) == False: 
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 10: FAILED to publish entry: " + self.entryName2)
#                 return
#                   
#             writeToLog("INFO","Step 11: Going to publish entry: " + self.entryName3)            
#             if self.common.myMedia.publishSingleEntry(self.entryName3, "", [(self.channelName2)]) == False: 
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 11: FAILED to publish entry: " + self.entryName2)
#                 return
#                       
#             writeToLog("INFO","Step 12: Going to add user '" + self.userName2 +"' as member to channel '" + self.channelName2 + "'")
#             if self.common.channel.addMembersToChannel(self.channelName2, self.userName2, permission=enums.ChannelMemberPermission.MEMBER) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 12: FAILED to add user '" + self.userName2 + "' as member to channel '" + self.channelName2 + "'")
#                 return
#                   
#             writeToLog("INFO","Step 13: Going to add user '" + self.userName2 +"' as manager to channel '" + self.channelName3 + "'")
#             if self.common.channel.addMembersToChannel(self.channelName3, self.userName2, permission=enums.ChannelMemberPermission.MEMBER) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 13: FAILED to add user '" + self.userName2 + "' as member to channel '" + self.channelName3 + "'")
#                 return
#                   
#             sleep(3)
#             writeToLog("INFO","Step 14: Going to logout from " + self.userName1 + " user")
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 14: FAILED to logout from " + self.userName1 + " user")
#                 return  
#                                         
#             writeToLog("INFO","Step 15: Going to login with user " + self.userName3)
#             if self.common.login.loginToKMS(self.userName3, self.userPass3) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 15: FAILED to login with " + self.userName3)
#                 return
#                   
#             writeToLog("INFO","Step 16: Going to add user '" + self.userName3 +"' as channel subscriber in '" + self.channelName1 + "'")
#             if self.common.channel.subscribeUserToChannel(self.channelName1, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 16: FAILED to add user '" + self.userName3 + "' as channel subscriber in '" + self.channelName1 + "'")
#                 return
#                 
#             sleep(2) 
#             writeToLog("INFO","Step 17: Going to add user '" + self.userName3 +"' as channel subscriber in '" + self.channelName2 + "'")
#             if self.common.channel.subscribeUserToChannel(self.channelName2, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 17: FAILED to add user '" + self.userName3 + "' as channel subscriber in '" + self.channelName2 + "'")
#                 return
#                   
#             writeToLog("INFO","Step 18: Going to add user '" + self.userName3 +"' as channel subscriber in '" + self.channelName3 + "'")
#             if self.common.channel.subscribeUserToChannel(self.channelName3, "1" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 18: FAILED to add user '" + self.userName3 + "' as channel subscriber in '" + self.channelName3 + "'")
#                 return
#                   
#             sleep(3)
#             writeToLog("INFO","Step 19: Going to logout from " + self.userName3)
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 19: FAILED to logout from " + self.userName3)
#                 return  
#                                        
#             writeToLog("INFO","Step 20: Going to login with : " + self.userName4)
#             if self.common.login.loginToKMS(self.userName4, self.userPass4) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 20: FAILED to login with " + self.userName4)
#                 return
#       
#             writeToLog("INFO","Step 21: Going to add user '" + self.userName4 +"' as channel subscriber in '" + self.channelName3 + "'")
#             if self.common.channel.subscribeUserToChannel(self.channelName3, "2" , navigateFrom=enums.Location.CHANNELS_PAGE)== False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 16: FAILED to add user '" + self.userName4 + "' as channel subscriber in '" + self.channelName4 + "'")
#                 return
#                     
#             sleep(3)
#             writeToLog("INFO","Step 22: Going to logout from " + self.userName4)
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 22: FAILED to logout from " + self.userName4)
#                 return

#           writeToLog("INFO","Channels for sort by tests were uploaded successfully")
            ###########################################################################################
            
            ##################### Creating entries for Sort by tests: 4311#############################
#             writeToLog("INFO","Step 1: Going to enable like module")            
#             if self.common.admin.enablelike(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to enable like module")
#                 return
#                   
#             writeToLog("INFO","Step 2: Going navigate to home page")            
#             if self.common.home.navigateToHomePage(forceNavigate=True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED navigate to home page")
#                 return
#             
#             writeToLog("INFO","Step 3: Going to login with user " + self.userName1)
#             if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED to login with " + self.userName1)
#                 return
#                          
#             writeToLog("INFO","Step 4: Going to create open channel")            
#             if self.common.channel.createChannel(self.channelForEsearch, self.channelForEsearchDescription, self.channelForEsearchTags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 4: FAILED to create open channel")
#                 return  
#  
#             writeToLog("INFO","Step 5: Going to create SR channel")
#             if self.common.channel.createChannel(self.SrChannelForEsearch, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.SHAREDREPOSITORY, False, True, True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 5: FAILED to create SR channel")
#                 return         
#              
#             step = 6
#                   
#             for i in range(1,14):
#                 writeToLog("INFO","Step " + str(step) + ": Going to upload new entry '" + eval('self.entryForSortBy'+str(i)))            
#                 if self.common.upload.uploadEntry(self.filePathForSortBy, eval('self.entryForSortBy'+str(i)), self.entryDescription, self.entryTags) == False:
#                     self.status = "Fail"
#                     writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry " + eval('self.entryForSortBy'+str(i)))
#                     return
#                  
#                 step = step + 1
#                  
#                 writeToLog("INFO","Step " + str(step) + ": Going to publish entry '" + eval('self.entryForSortBy'+str(i)) + "to category and channel")            
#                 if self.common.myMedia.publishSingleEntry(eval('self.entryForSortBy'+str(i)), [self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch], publishFrom = enums.Location.UPLOAD_PAGE) == False:
#                     self.status = "Fail"
#                     writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry " + eval('self.entryForSortBy'+str(i)))
#                     return
#                  
#                 step = step + 1
#                   
#             writeToLog("INFO","Step 31: Going to add future scheduling to '" + "C160E832-1-Sort by Scheduling - Future" + "'")    
#             if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryFutureStartDate, startTime=self.entryFutureStartTime, entryName="C160E832-1-Sort by Scheduling - Future") == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 31: FAILED to add future scheduling to" + self.entryForSortBy11)
#                 return 
#             
#             writeToLog("INFO","Step 32: Going to add present scheduling to '" + self.entryForSortBy12 + "'")    
#             if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryFutureStartDate,endTime=self.entryFutureStartTime, entryName="C160E832-1-Sort by Scheduling - In scheduling") == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 32: FAILED to add present scheduling to: " + self.entryForSortBy12)
#                 return  
#             
#             writeToLog("INFO","Step 33: Going to add past scheduling to '" + self.entryForSortBy13 + "'")    
#             if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryPastStartDate, endTime=self.entryPastStartTime, entryName="C160E832-1-Sort by Scheduling - Past") == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 33: FAILED to past scheduling to: " + self.entryForSortBy13)
#                 return                                                    
#                                 
#             writeToLog("INFO","Step 31: Going navigate to entry '" + self.entryForSortBy1 + "'")    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy1, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 25: FAILED navigate to entry: " + self.entryForSortBy1)
#                 return 
#                        
#             writeToLog("INFO","Step 26: Going to like entry: " + self.entryForSortBy1)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 26: FAILED to like entry: " + self.entryForSortBy1)
#                 return   
#                      
#             sleep(2) 
#             writeToLog("INFO","Step 27: Going to add comments to entry: " + self.entryForSortBy1)  
#             if self.common.entryPage.addComments(["Comment 1", "Comment 2"]) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 27: FAILED to add comments to entry: " + self.entryForSortBy1)
#                 return    
#                     
#             writeToLog("INFO","Step 28: Going navigate to entry: " + self.entryForSortBy2)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy2, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 28: FAILED navigate to entry: " + self.entryForSortBy2)
#                 return 
#                     
#             writeToLog("INFO","Step 30: Going to like entry: " + self.entryForSortBy2)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 30: FAILED to like entry: " + self.entryForSortBy2)
#                 return   
#                     
#             writeToLog("INFO","Step 31: Going navigate to entry: " + self.entryForSortBy3)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy3, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 31: FAILED navigate to entry: " + self.entryForSortBy3)
#                 return 
#                     
#             sleep(2) 
#             writeToLog("INFO","Step 32: Going to add comments to entry: " + self.entryForSortBy3)  
#             if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3"]) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 32: FAILED to add comments to entry: " + self.entryForSortBy3)
#                 return    
#                     
#             writeToLog("INFO","Step 33: Going navigate to entry: " + self.entryForSortBy4)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy4, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 33: FAILED navigate to entry: " + self.entryForSortBy4)
#                 return 
#                     
#             writeToLog("INFO","Step 34: Going to like entry: " + self.entryForSortBy4)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 34: FAILED to like entry: " + self.entryForSortBy4)
#                 return 
#                     
#             sleep(2) 
#             writeToLog("INFO","Step 35: Going to add comment to entry: " + self.entryForSortBy4)  
#             if self.common.entryPage.addComment(["Comment 1"]) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 35: FAILED to add comment to entry: " + self.entryForSortBy4)
#                 return   
#             
#             writeToLog("INFO","Step 36: Going navigate to entry: " + self.entryForSortBy5)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy5, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 36: FAILED navigate to entry: " + self.entryForSortBy5)
#                 return     
#             
#             writeToLog("INFO","Step 37: Going to like entry: " + self.entryForSortBy5)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 37: FAILED to like entry: " + self.entryForSortBy5)
#                 return 
#                     
#             sleep(2) 
#             writeToLog("INFO","Step 38: Going to add comment to entry: " + self.entryForSortBy5)  
#             if self.common.entryPage.addComment(["Comment 1", "Comment 2", "Comment 3", "Comment 4", "Comment 5"]) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 38: FAILED to add comment to entry: " + self.entryForSortBy5)
#                 return
#             
#             writeToLog("INFO","Step 39: Going navigate to entry: " + self.entryForSortBy7)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy7, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 39: FAILED navigate to entry: " + self.entryForSortBy7)
#                 return     
#             
#             writeToLog("INFO","Step 40: Going to like entry: " + self.entryForSortBy7)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 40: FAILED to like entry: " + self.entryForSortBy7)
#                 return 
#                     
#             writeToLog("INFO","Step 41: Going navigate to entry " + self.entryForSortBy8)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy8, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 41: FAILED navigate to entry: " + self.entryForSortBy8)
#                 return 
#                        
#             writeToLog("INFO","Step 42: Going to like entry: " + self.entryForSortBy8)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 42: FAILED to like entry: " + self.entryForSortBy8)
#                 return   
#                      
#             sleep(2) 
#             writeToLog("INFO","Step 43: Going to add comments to entry: " + self.entryForSortBy8)  
#             if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3", "Comment 4", "Comment 5", "Comment 6"]) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 43: FAILED to add comments to entry: " + self.entryForSortBy8)
#                 return         
#                     
#             writeToLog("INFO","Step 44: Going navigate to entry " + self.entryForSortBy9)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy9, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 44: FAILED navigate to entry: " + self.entryForSortBy9)
#                 return 
#                        
#             writeToLog("INFO","Step 45: Going to like entry: " + self.entryForSortBy9)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 45: FAILED to like entry: " + self.entryForSortBy9)
#                 return   
#                      
#             sleep(2) 
#             writeToLog("INFO","Step 46: Going to add comments to entry: " + self.entryForSortBy9)  
#             if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3", "Comment 4"]) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 46: FAILED to add comments to entry: " + self.entryForSortBy9)
#                 return                             
#                     
#             writeToLog("INFO","Step 47: Going navigate to entry " + self.entryForSortBy10)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy10, enums.Location.MY_MEDIA) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 47: FAILED navigate to entry: " + self.entryForSortBy10)
#                 return 
#                        
#             writeToLog("INFO","Step 48: Going to like entry: " + self.entryForSortBy10)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 48: FAILED to like entry: " + self.entryForSortBy10)
#                 return   
#                      
#             sleep(2) 
#             writeToLog("INFO","Step 49: Going to add comments to entry: " + self.entryForSortBy10)  
#             if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3", "Comment 4","Comment 5", "Comment 6", "Comment 7","Comment 8"]) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 49: FAILED to add comments to entry: " + self.entryForSortBy10)
#                 return                     
#                    
#             sleep(3)
#             writeToLog("INFO","Step 50: Going to logout from main user")
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 50: FAILED to logout from main user")
#                 return  
#                                            
#             writeToLog("INFO","Step 51: Going to login with user " + self.userName2)
#             if self.common.login.loginToKMS(self.userName2, self.userPass1) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 51: FAILED to login with " + self.userName2)
#                 return
#                        
#             writeToLog("INFO","Step 51: Going navigate to entry: "+ self.entryForSortBy2)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy2, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 51: FAILED navigate to entry: " + self.entryForSortBy2)
#                 return 
#                        
#             writeToLog("INFO","Step 52: Going to like entry: " + self.entryForSortBy2)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 52: FAILED to like entry: " + self.entryForSortBy2)
#                 return    
#                        
#             writeToLog("INFO","Step 53: Going navigate to entry: "+ self.entryForSortBy4)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy4, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 53: FAILED navigate to entry: " + self.entryForSortBy4)
#                 return 
#                        
#             writeToLog("INFO","Step 54: Going to like entry: " + self.entryForSortBy4)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 54: FAILED to like entry: " + self.entryForSortBy4)
#                 return  
#                        
#             writeToLog("INFO","Step 55: Going navigate to entry: "+ self.entryForSortBy5)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy5, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 55: FAILED navigate to entry: " + self.entryForSortBy5)
#                 return 
#                        
#             writeToLog("INFO","Step 56: Going to like entry: " + self.entryForSortBy5)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 56: FAILED to like entry: " + self.entryForSortBy5)
#                 return                        
#       
#             writeToLog("INFO","Step 57: Going navigate to entry: "+ self.entryForSortBy7)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy7, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 57: FAILED navigate to entry: " + self.entryForSortBy7)
#                 return 
#                        
#             writeToLog("INFO","Step 58: Going to like entry: " + self.entryForSortBy7)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 58: FAILED to like entry: " + self.entryForSortBy7)
#                 return      
#             
#             writeToLog("INFO","Step 59: Going navigate to entry: "+ self.entryForSortBy8)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy8, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 59: FAILED navigate to entry: " + self.entryForSortBy8)
#                 return 
#                        
#             writeToLog("INFO","Step 60: Going to like entry: " + self.entryForSortBy8)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 60: FAILED to like entry: " + self.entryForSortBy8)
#                 return  
#             
#             writeToLog("INFO","Step 61: Going navigate to entry: "+ self.entryForSortBy9)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy9, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 61: FAILED navigate to entry: " + self.entryForSortBy9)
#                 return 
#                        
#             writeToLog("INFO","Step 62: Going to like entry: " + self.entryForSortBy9)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 62: FAILED to like entry: " + self.entryForSortBy9)
#                 return  
#             
#             writeToLog("INFO","Step 63: Going navigate to entry: "+ self.entryForSortBy10)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy10, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 63: FAILED navigate to entry: " + self.entryForSortBy10)
#                 return 
#                        
#             writeToLog("INFO","Step 64: Going to like entry: " + self.entryForSortBy10)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 64: FAILED to like entry: " + self.entryForSortBy10)
#                 return                                  
#                          
#             sleep(3)
#             writeToLog("INFO","Step 65: Going to logout from main user")
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 65: FAILED to logout from main user")
#                 return  
#                                            
#             writeToLog("INFO","Step 66: Going to login with user " + self.userName3)
#             if self.common.login.loginToKMS(self.userName3, self.userPass2) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 66: FAILED to login with " + self.userName3)
#                 return    
#             
#             writeToLog("INFO","Step 67: Going navigate to entry: "+ self.entryForSortBy4)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy4, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 67: FAILED navigate to entry: " + self.entryForSortBy4)
#                 return 
#                        
#             writeToLog("INFO","Step 68: Going to like entry: " + self.entryForSortBy4)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 68: FAILED to like entry: " + self.entryForSortBy4)
#                 return 
#             
#             writeToLog("INFO","Step 69: Going navigate to entry: "+ self.entryForSortBy7)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy7, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 69: FAILED navigate to entry: " + self.entryForSortBy7)
#                 return 
#                        
#             writeToLog("INFO","Step 70: Going to like entry: " + self.entryForSortBy7)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 70: FAILED to like entry: " + self.entryForSortBy7)
#                 return              
#             
#             writeToLog("INFO","Step 71: Going navigate to entry: "+ self.entryForSortBy8)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy8, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 71: FAILED navigate to entry: " + self.entryForSortBy8)
#                 return 
#                        
#             writeToLog("INFO","Step 72: Going to like entry: " + self.entryForSortBy8)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 72: FAILED to like entry: " + self.entryForSortBy8)
#                 return    
#             
#             writeToLog("INFO","Step 73: Going navigate to entry: "+ self.entryForSortBy9)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy9, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 73: FAILED navigate to entry: " + self.entryForSortBy9)
#                 return 
#                        
#             writeToLog("INFO","Step 74: Going to like entry: " + self.entryForSortBy9)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 74: FAILED to like entry: " + self.entryForSortBy9)
#                 return   
#             
#             writeToLog("INFO","Step 75: Going navigate to entry: "+ self.entryForSortBy10)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy10, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 75: FAILED navigate to entry: " + self.entryForSortBy10)
#                 return 
#                        
#             writeToLog("INFO","Step 76: Going to like entry: " + self.entryForSortBy10)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 76: FAILED to like entry: " + self.entryForSortBy10)
#                 return              
#             
#             sleep(3)
#             writeToLog("INFO","Step 77: Going to logout from main user")
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 77: FAILED to logout from main user")
#                 return  
#                                            
#             writeToLog("INFO","Step 78: Going to login with user " + self.userName4)
#             if self.common.login.loginToKMS(self.userName4, self.userPass3) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 78: FAILED to login with " + self.userName4)
#                 return    
#             
#             writeToLog("INFO","Step 79: Going navigate to entry: "+ self.entryForSortBy7)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy7, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 79: FAILED navigate to entry: " + self.entryForSortBy7)
#                 return 
#                        
#             writeToLog("INFO","Step 80: Going to like entry: " + self.entryForSortBy7)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 80: FAILED to like entry: " + self.entryForSortBy7)
#                 return 
#             
#             writeToLog("INFO","Step 81: Going navigate to entry: "+ self.entryForSortBy8)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy8, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 81: FAILED navigate to entry: " + self.entryForSortBy8)
#                 return 
#                        
#             writeToLog("INFO","Step 82: Going to like entry: " + self.entryForSortBy8)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 82: FAILED to like entry: " + self.entryForSortBy8)
#                 return              
#             
#             writeToLog("INFO","Step 83: Going navigate to entry: "+ self.entryForSortBy9)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy9, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 83: FAILED navigate to entry: " + self.entryForSortBy9)
#                 return 
#                        
#             writeToLog("INFO","Step 84: Going to like entry: " + self.entryForSortBy9)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 84: FAILED to like entry: " + self.entryForSortBy9)
#                 return    
#             
#             writeToLog("INFO","Step 85: Going navigate to entry: "+ self.entryForSortBy10)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy10, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 85: FAILED navigate to entry: " + self.entryForSortBy10)
#                 return 
#                        
#             writeToLog("INFO","Step 86: Going to like entry: " + self.entryForSortBy10)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 86: FAILED to like entry: " + self.entryForSortBy10)
#                 return   
#                         
#             sleep(3)
#             writeToLog("INFO","Step 87: Going to logout from main user")
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 87: FAILED to logout from main user")
#                 return  
#                                            
#             writeToLog("INFO","Step 88: Going to login with user " + self.userName5)
#             if self.common.login.loginToKMS(self.userName5, self.userPass4) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 88: FAILED to login with " + self.userName5)
#                 return    
#             
#             writeToLog("INFO","Step 89: Going navigate to entry: "+ self.entryForSortBy8)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy8, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 89: FAILED navigate to entry: " + self.entryForSortBy8)
#                 return 
#                        
#             writeToLog("INFO","Step 90: Going to like entry: " + self.entryForSortBy8)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 90: FAILED to like entry: " + self.entryForSortBy8)
#                 return 
#             
#             writeToLog("INFO","Step 91: Going navigate to entry: "+ self.entryForSortBy9)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy9, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 91: FAILED navigate to entry: " + self.entryForSortBy9)
#                 return 
#                        
#             writeToLog("INFO","Step 92: Going to like entry: " + self.entryForSortBy9)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 92: FAILED to like entry: " + self.entryForSortBy9)
#                 return              
#             
#             writeToLog("INFO","Step 93: Going navigate to entry: "+ self.entryForSortBy10)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy10, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 93: FAILED navigate to entry: " + self.entryForSortBy10)
#                 return 
#                        
#             writeToLog("INFO","Step 94: Going to like entry: " + self.entryForSortBy10)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 94: FAILED to like entry: " + self.entryForSortBy10)
#                 return    
# 
#             sleep(3)
#             writeToLog("INFO","Step 95: Going to logout from main user")
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 95: FAILED to logout from main user")
#                 return  
#                                            
#             writeToLog("INFO","Step 96: Going to login with user " + self.userName6)
#             if self.common.login.loginToKMS(self.userName6, self.userPass5) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 96: FAILED to login with " + self.userName6)
#                 return    
#             
#             writeToLog("INFO","Step 97: Going navigate to entry: "+ self.entryForSortBy9)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy9, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 97: FAILED navigate to entry: " + self.entryForSortBy9)
#                 return 
#                        
#             writeToLog("INFO","Step 98: Going to like entry: " + self.entryForSortBy9)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 98: FAILED to like entry: " + self.entryForSortBy9)
#                 return 
#             
#             writeToLog("INFO","Step 99: Going navigate to entry: "+ self.entryForSortBy10)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy10, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 99: FAILED navigate to entry: " + self.entryForSortBy10)
#                 return 
#                        
#             writeToLog("INFO","Step 100: Going to like entry: " + self.entryForSortBy10)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 100: FAILED to like entry: " + self.entryForSortBy10)
#                 return              
#                         
#             sleep(3)
#             writeToLog("INFO","Step 101: Going to logout from main user")
#             if self.common.login.logOutOfKMS() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 101: FAILED to logout from main user")
#                 return  
#                                            
#             writeToLog("INFO","Step 102: Going to login with user " + self.userName7)
#             if self.common.login.loginToKMS(self.userName7, self.userPass6) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 102: FAILED to login with " + self.userName7)
#                 return    
#             
#             writeToLog("INFO","Step 103: Going navigate to entry: "+ self.entryForSortBy10)    
#             if self.common.entryPage.navigateToEntry(self.entryForSortBy10, enums.Location.CATEGORY_PAGE, self.categoryForEsearch) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 103: FAILED navigate to entry: " + self.entryForSortBy10)
#                 return 
#                        
#             writeToLog("INFO","Step 103: Going to like entry: " + self.entryForSortBy10)            
#             if self.common.entryPage.LikeUnlikeEntry(True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 103: FAILED to like entry: " + self.entryForSortBy10)
#                 return  
            #################################################################################
                                                                            
            #################################################################################
            writeToLog("INFO","TEST PASSED: 'My Channels - Sort Channels with search' was done successfully")
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