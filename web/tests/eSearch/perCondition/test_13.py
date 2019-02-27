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
    #  @Author: Cus Horia
    # Test Name : Setup test for eSearch
    # Test description:
    # Upload two entries for video, audio and quiz one with captions, one without, and an image and youtube entry
    #================================================================================================================================
    testNum = "13"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\automation.jpg'
    filePath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\waves.mp3'
    filePath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\WhyAutomatedTesting.mp4'
    captionPath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\caption_1.srt'
    navigateFrom = enums.Location.MY_MEDIA
    captionLanguage1 = "English"
    captionLabel1 = "EN"
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
    entryName1 = "Filter by caption - without caption image"
    entryName2 = "Filter by caption - with caption audio"
    entryName3 = "Filter by caption - without caption youtube"
    entryName22 = "Filter by caption - without caption audio2"
    entryName4 = "Filter by caption - with caption video"
    entryName42 = "Filter by caption - without caption video2"
    entryName5 = "Filter by caption - with caption quiz"
    entryName52 = "Filter by caption - without caption quiz2"
    entryNameQuiz1 = "Filter by caption - with caption quiz - Quiz"
    entryNameQuiz2 = "Filter by caption - without caption quiz2 - Quiz"
    audioEntryList = [entryName2, entryName22]
    videoEntryList = [entryName4, entryName42]
    quizEntryMap = {entryName5:entryNameQuiz1, entryName52:entryNameQuiz2}
    captionEntryList = [entryName2, entryName4, entryNameQuiz1]  

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
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
                                
            writeToLog("INFO","Step 2: Going to upload an image entry")            
            if self.common.upload.uploadEntry(self.filePath1, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload an image entry")
                return
                   
            writeToLog("INFO","Step 3: Going to publish an image entry")
            if self.common.myMedia.publishSingleEntry(self.entryName1, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 3: FAILED to publish an image entry")
                return
                 
            for entry in self.audioEntryList:      
                writeToLog("INFO","Step 4: Going to upload an audio entry")
                if self.common.upload.uploadEntry(self.filePath2, entry, self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step 4: FAILED to upload an audio entry")
                    return
     
                writeToLog("INFO","Step 5: Going to publish an audio entry")
                if self.common.myMedia.publishSingleEntry(entry, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                    writeToLog("INFO","Step 5: FAILED to publish an audio type entry")
                    return           
                 
            writeToLog("INFO","Step 6: Going to upload a youtube entry")
            if self.common.upload.clickAddYoutube() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to upload a youtube type entry")
                return
                    
            writeToLog("INFO","Step 7: Going to insert a youtube link")
            if self.common.upload.addYoutubeEntry(self.youtuebLink, self.entryName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to insert a youtube link")
                return  
                  
            writeToLog("INFO","Step 8: Going to publish the youtube entry")
            if self.common.myMedia.publishSingleEntry(self.entryName3, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 8: FAILED to publish the youtube entry")
                return     
                
            for entry in self.videoEntryList:        
                writeToLog("INFO","Step 9: Going to upload a video entry")            
                if self.common.upload.uploadEntry(self.filePath3, entry, self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED to upload a video entry")
                    return    
                      
                writeToLog("INFO","Step 10: Going to publish the specific video entry")
                if self.common.myMedia.publishSingleEntry(entry, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                    writeToLog("INFO","Step 10: FAILED to publish the specific video entry")
                    return
                 
            for entry in self.quizEntryMap:     
                writeToLog("INFO","Step 11: Going to upload a video entry for quiz")
                if self.common.upload.uploadEntry(self.filePath3, entry, self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step 11: FAILED to upload a video entry for quiz")
                    return            
                                                                                
                writeToLog("INFO","Step 12: Going to navigate to add new video quiz")
                if self.common.upload.addNewVideoQuiz() == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 12: FAILED to navigate to the add new video quiz")
                    return  
                       
                writeToLog("INFO","Step 13: Going to search the uploaded entry and open KEA")
                if self.common.kea.searchAndSelectEntryInMediaSelection(entry, False) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 13: FAILED to find the uploaded entry and open KEA")
                    return  
                       
                writeToLog("INFO","Step 14: Going to start quiz and add questions")
                if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 14: FAILED to start quiz and add questions")
                    return   
                       
                writeToLog("INFO","Step 15: Going to save quiz and navigate to media page")
                if self.common.kea.clickDone() == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 15: FAILED to save quiz and navigate to media page")
                    return          
                    
                writeToLog("INFO","Step 16: Going to publish the new quiz entry")
                if self.common.myMedia.publishSingleEntry(self.quizEntryMap[entry], [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                    writeToLog("INFO","Step 16: FAILED to publish the new quiz entry")
                    return 
            
            for entry in self.captionEntryList:
                writeToLog("INFO","Step 17: Going to insert captions to three entries")   
                if self.common.myMedia.navigateToMyMedia(forceNavigate = True) == False:
                    writeToLog("INFO", "Failed to navigate to my media")
                    return
                
                writeToLog("INFO","Step 18: Going to navigate to an entry")                        
                if self.common.entryPage.navigateToEntry(entry, self.navigateFrom) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step 18: FAILED to navigate to the specific entry")
                    return
                 
                writeToLog("INFO", "STEP 19: Going to wait until the media is being processed")
                if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step 19: Failed to process the media file")
                    return
                             
                writeToLog("INFO", "STEP 20: Going to navigate to the edit entry page")
                if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "STEP 20: FAILED to enter in the edit entry page")
                    return 
                 
                writeToLog("INFO", "STEP 21: Going to insert caption  " + self.captionPath1 + " file")
                if self.common.editEntryPage.addCaptions(self.captionPath1, self.captionLanguage1, self.captionLabel1) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step 21: FAILED to add captions to upload " + self.captionPath1 + " file")
                    return     
                   
            writeToLog("INFO","TEST PASSED: All entries were created and published successfully") 
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