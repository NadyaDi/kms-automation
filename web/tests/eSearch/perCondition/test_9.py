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
    #  @Author: Oded Berihon
    # Test Name : Setup test for eSearch
    # Test description:
    # Creating new entries and sort them by media type
    #================================================================================================================================
    testNum = "9"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation.jpg'
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\WhyAutomatedTesting.mp4'
    filePath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\waves.mp3'
    entryName4= None
    entryNameQuiz=None
    youtuebLink = "https://www.youtube.com/watch?v=usNsCeOV4GM"
    QuizQuestion1 = 'First question'
    QuizQuestion1Answer1 = 'First answer'
    QuizQuestion1AdditionalAnswers = ['Second answer', 'Third question', 'Fourth question']
    
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
            self.entryName1 = "Sort by media type - image"
            self.entryName2 = "Sort by media type - video"
            self.entryName3 = "Sort by media type - audio"
            self.entryName4 = "Sort by media type - youtube"
            self.entryNameQuiz = self.entryName2 + " - Quiz"

            
            
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

            ##################### TEST STEPS - MAIN FLOW #############################################################  
            # Create entries and channels for sort by tests
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
                              
            writeToLog("INFO","Step 2: Going to upload Video type entry")            
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry Video")
                return
             
            writeToLog("INFO","Step 3: Going to publish entry1")
            if self.common.myMedia.publishSingleEntry(self.entryName1, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 3: FAILED - could not publish Video to channel")
                return
                        
            writeToLog("INFO","Step 4: Going to upload audio type entry")
            if self.common.upload.uploadEntry(self.filePath2, self.entryName2, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED failed to upload entry audio")
                return 
              
            writeToLog("INFO","Step 5: Going to publish entry1")
            if self.common.myMedia.publishSingleEntry(self.entryName2, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 5: FAILED - could not publish Video to channel")
                return
                 
            writeToLog("INFO","Step 6: Going to upload video type entry")            
            if self.common.upload.uploadEntry(self.filePath3, self.entryName3, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED failed to upload entry video")
                return     
             
            writeToLog("INFO","Step 7: Going to publish entry1")
            if self.common.myMedia.publishSingleEntry(self.entryName3, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 7: FAILED - could not publish Video to channel")
                return            
                                                                          
            writeToLog("INFO","Step 8: Going to navigate to add new video quiz")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to click video quiz")
                return  
                 
            writeToLog("INFO","Step 9: Going to search the uploaded entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryName2, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to find entry and open KEA")
                return  
                 
            writeToLog("INFO","Step 10: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to start quiz and add questions")
                return   
                 
            writeToLog("INFO","Step 11: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to save quiz and navigate to media page")
                return          
               
            writeToLog("INFO","Step 12: Going to publish entry1")
            if self.common.myMedia.publishSingleEntry(self.entryNameQuiz, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 12: FAILED - could not publish Video to channel")
                return      
                  
            writeToLog("INFO","Step 13: Going to upload youtube entry")
            if self.common.upload.clickAddYoutube() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to upload youtube entry")
                return
               
            writeToLog("INFO","Step 14: Going to insert youtube link")
            if self.common.upload.addYoutubeEntry(self.youtuebLink, self.entryName4) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to insert youtube link")
                return  
             
            writeToLog("INFO","Step 15: Going to publish entry4")
            if self.common.myMedia.publishSingleEntry(self.entryName4, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 15: FAILED - could not publish Video to channel")
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