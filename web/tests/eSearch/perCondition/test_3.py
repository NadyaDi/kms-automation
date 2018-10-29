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
    # Creating new entries and channels for sort by eSearch tests
    #================================================================================================================================
    testNum = "3"
    
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
            
            # Entries for sort by in my media/global search/add to channel/channel/gallery/new video quiz
            self.entryForSortBy1 = "Sort by - Sort A"
            self.entryForSortBy2 = "Sort by - Sort B"
            self.entryForSortBy3 = "Sort by - Sort C"
            self.entryForSortBy4 = "Sort by - Sort D"
            self.entryForSortBy5 = "Sort by - Sort E"
            self.entryForSortBy6 = "Sort by - Sort F"
            self.entryForSortBy7 = "Sort by - Sort G"
            self.entryForSortBy8 = "Sort by - Sort H"
            self.entryForSortBy9 = "Sort by Scheduling - Future"
            self.entryForSortBy10 = "Sort by Scheduling - In scheduling"
            self.entryForSortBy11 = "Sort by Scheduling - Past"
            
            # Dates and time to set scheduling in entries for scheduling filter/sort
            self.entryPastStartDate = (datetime.datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
            self.entryTodayStartDate = datetime.datetime.now().strftime("%d/%m/%Y")
            self.entryFutureStartDate = (datetime.datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y")
        
            self.entryFutureStartTime = time.time() + (60*60)
            self.entryFutureStartTime= time.strftime("%I:%M %p",time.localtime(self.entryFutureStartTime))
             
            self.entryPastStartTime = time.time() - (60*60)
            self.entryPastStartTime= time.strftime("%I:%M %p",time.localtime(self.entryPastStartTime))
            
            # Category tests in gallery/add to gallery tabs 
            self.categoryForEsearch = 'eSearch category'
            self.categoryForModerator = 'category for eSearch moderator' 
            
            # Channel for tests in channel/ add to channel tabs
            self.channelForEsearch  = "Channel for eSearch"
            self.channelForModerator = 'channel moderator for eSearch'
            self.SrChannelForEsearch = "SR-Channel for eSearch"
            
            self.channelForEsearchDescription = "channel for eSearch tests"
            self.channelForEsearchTags = 'channel tag,'
            self.channelForEsearchPrivacy = 'open'

            # List of expected results for entries sort by
            self.sortEntriesByCreationDateDescending = (self.entryForSortBy8, self.entryForSortBy7, self.entryForSortBy6,self.entryForSortBy5, self.entryForSortBy4, 
                                                        self.entryForSortBy3, self.entryForSortBy2, self.entryForSortBy1)
            self.sortEntriesByCreationDateAscending  = (self.entryForSortBy1, self.entryForSortBy2, self.entryForSortBy3, self.entryForSortBy4, self.entryForSortBy5,
                                                        self.entryForSortBy6, self.entryForSortBy7, self.entryForSortBy8)
            self.sortEntriesByUpdateDateDescending   = ()
            self.sortEntriesByUpdateDateAscending    = ()
            self.sortEntriesByAlphabeticalAToZ       = (self.entryForSortBy1, self.entryForSortBy2, self.entryForSortBy3, self.entryForSortBy4, self.entryForSortBy4,
                                                        self.entryForSortBy5, self.entryForSortBy6, self.entryForSortBy7, self.entryForSortBy8)
            self.sortEntriesByAlphabeticalZToA       = (self.entryForSortBy8, self.entryForSortBy7, self.entryForSortBy6,self.entryForSortBy5, self.entryForSortBy4, 
                                                        self.entryForSortBy3, self.entryForSortBy2, self.entryForSortBy1)
            self.sortEntriesByLikes                  = (self.entryForSortBy6, self.entryForSortBy4, self.entryForSortBy8, self.entryForSortBy7, self.entryForSortBy3,
                                                        self.entryForSortBy5, self.entryForSortBy1, self.entryForSortBy2)
            self.sortEntriesByComments               = (self.entryForSortBy7, self.entryForSortBy6, self.entryForSortBy3, self.entryForSortBy5, self.entryForSortBy2,
                                                         self.entryForSortBy1, self.entryForSortBy4, self.entryForSortBy8)
            self.sortEntriesBySchedulingAscending    = (self.entryForSortBy9, self.entryForSortBy10, self.entryForSortBy11)
            self.sortEntriesBySchedulingDescending   = (self.entryForSortBy11, self.entryForSortBy10, self.entryForSortBy9)
            ##################### TEST STEPS - MAIN FLOW #############################################################  
            # Create entries and channels for sort by tests
            writeToLog("INFO","Step 1: Going to enable like module")            
            if self.common.admin.enablelike(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to enable like module")
                return
                      
            writeToLog("INFO","Step 2: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to home page")
                return
               
            writeToLog("INFO","Step 3: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to login with " + self.userName1)
                return
                            
            writeToLog("INFO","Step 4: Going to create open channel")            
            if self.common.channel.createChannel(self.channelForEsearch, self.channelForEsearchDescription, self.channelForEsearchTags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to create open channel")
                return  
     
            writeToLog("INFO","Step 5: Going to create SR channel")
            if self.common.channel.createChannel(self.SrChannelForEsearch, self.channelDescription, self.channelTags, enums.ChannelPrivacyType.SHAREDREPOSITORY, False, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to create SR channel")
                return         
                
            step = 6
                     
            for i in range(1,12):
                writeToLog("INFO","Step " + str(step) + ": Going to upload new entry '" + eval('self.entryForSortBy'+str(i)))            
                if self.common.upload.uploadEntry(self.filePathForSortBy, eval('self.entryForSortBy'+str(i)), self.entryDescription, self.entryTags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry " + eval('self.entryForSortBy'+str(i)))
                    return
                    
                step = step + 1
                    
                writeToLog("INFO","Step " + str(step) + ": Going to publish entry '" + eval('self.entryForSortBy'+str(i)) + " to eSearch categories and channels")            
                if self.common.myMedia.publishSingleEntry(eval('self.entryForSortBy'+str(i)), [self.categoryForEsearch, self.categoryForModerator], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.UPLOAD_PAGE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry " + eval('self.entryForSortBy'+str(i)))
                    return
                    
                step = step + 1
                    
            writeToLog("INFO","Step 28: Going to add future scheduling to '" + self.entryForSortBy9 + "'")    
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryFutureStartDate, startTime=self.entryFutureStartTime, entryName=self.entryForSortBy9) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED to add future scheduling to" + self.entryForSortBy9)
                return 
              
            writeToLog("INFO","Step 29: Going to add present scheduling to '" + self.entryForSortBy10 + "'")    
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryFutureStartDate,endTime=self.entryFutureStartTime, entryName=self.entryForSortBy10) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED to add present scheduling to: " + self.entryForSortBy10)
                return  
              
            writeToLog("INFO","Step 30: Going to add past scheduling to '" + self.entryForSortBy11 + "'")    
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryPastStartDate, endTime=self.entryPastStartTime, entryName=self.entryForSortBy11) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 30: FAILED to past scheduling to: " + self.entryForSortBy11)
                return                                                    
                                 
            writeToLog("INFO","TEST PASSED: All entries and channels for sort by were created successfully") 
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