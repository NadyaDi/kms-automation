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
    # Upload three Quiz entries and filter them by scheduling in: Past, Future and In Scheduling
    #================================================================================================================================
    testNum = "18"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Description"
    entryTags = "Tags,"
    navigateFrom = enums.Location.MY_MEDIA

    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!"

    entryName1 = "Filter by Scheduling - Quiz future"
    entryName2 = "Filter by Scheduling - Quiz past"
    entryName3 = "Filter by Scheduling - Quiz In Scheduling"
    publishName1 = "Filter by Scheduling - Quiz future - Quiz"
    publishName2 = "Filter by Scheduling - Quiz past - Quiz"
    publishName3 = "Filter by Scheduling - Quiz In Scheduling - Quiz"

    entryPath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\WhyAutomatedTesting.mp4'
    QuizQuestion1 = 'First question'
    QuizQuestion1Answer1 = 'First answer'
    QuizQuestion1AdditionalAnswers = ['Second answer', 'Third question', 'Fourth question']

    entryPastStartDate = (datetime.datetime.now() + timedelta(days=-1)).strftime("%d/%m/%Y")
    entryTodayStartDate = datetime.datetime.now().strftime("%d/%m/%Y")
    entryFutureStartDate = (datetime.datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")

    entryFutureStartTime = time.time() + (60*60)
    entryFutureStartTime= time.strftime("%I:%M %p",time.localtime(entryFutureStartTime))

    entryPastStartTime = time.time() - (60*60)
    entryPastStartTime= time.strftime("%I:%M %p",time.localtime(entryPastStartTime))

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
            ##################### TEST STEPS - MAIN FLOW #############################################################
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return

            writeToLog("INFO","Step 2: Going to upload " + self.entryName1 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName1, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload " + self.entryName1 + " entry")
                return            
                                                                           
            writeToLog("INFO","Step 3: Going to navigate to " + self.entryName1 + " entry")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to " + self.entryName1 + " entry")
                return  
                  
            writeToLog("INFO","Step 4: Going to search  " + self.entryName1 + " entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryName1, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to find  " + self.entryName1 + " entry and open KEA")
                return  
                  
            writeToLog("INFO","Step 5: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to start quiz and add questions")
                return  
                              
            writeToLog("INFO","Step 6: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to save quiz and navigate to media page")
                return 
                  
            writeToLog("INFO","Step 7: Going to publish the " + self.publishName1 +"  entry")
            if self.common.myMedia.publishSingleEntry(self.publishName1, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 7: FAILED to publish the " + self.publishName1 +"  entry")
                return

            writeToLog("INFO","Step 8: Going to set Future time-frame publishing to " + self.publishName1 + " entry")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryFutureStartDate, startTime=self.entryFutureStartTime, entryName=self.publishName1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to set Future time-frame publishing to " + self.publishName1 + " entry")
                return

            writeToLog("INFO","Step 9: Going to upload " + self.entryName2 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName2, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to upload " + self.entryName2 + " entry")
                return            
                                                                           
            writeToLog("INFO","Step 10: Going to navigate to " + self.entryName2 + " entry")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to navigate to " + self.entryName2 + " entry")
                return  
                  
            writeToLog("INFO","Step 11: Going to search  " + self.entryName2 + " entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryName2, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to find  " + self.entryName2 + " entry and open KEA")
                return  
                  
            writeToLog("INFO","Step 12: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to start quiz and add questions")
                return 
                              
            writeToLog("INFO","Step 13: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to save quiz and navigate to media page")
                return  
                  
            writeToLog("INFO","Step 14: Going to publish the " + self.publishName2 +"  entry")
            if self.common.myMedia.publishSingleEntry(self.publishName2, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 14: FAILED to publish the " + self.publishName2 +"  entry")
                return
 
            writeToLog("INFO","Step 15: Going to set Past time-frame publishing to " + self.publishName2 + " entry")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryPastStartDate, endTime=self.entryPastStartTime, entryName=self.publishName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to set Past time-frame publishing to " + self.publishName2 + " entry")
                return
 
            writeToLog("INFO","Step 16: Going to upload " + self.entryName3 + " entry")
            if self.common.upload.uploadEntry(self.entryPath, self.entryName3, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to upload " + self.entryName3 + " entry")
                return            
                                                                           
            writeToLog("INFO","Step 17: Going to navigate to " + self.entryName3 + " entry")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to navigate to " + self.entryName3 + " entry")
                return  
                  
            writeToLog("INFO","Step 18: Going to search  " + self.entryName2 + " entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryName3, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to find  " + self.entryName3 + " entry and open KEA")
                return  
                  
            writeToLog("INFO","Step 19: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to start quiz and add questions")
                return   
                              
            writeToLog("INFO","Step 20: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to save quiz and navigate to media page")
                return  
                  
            writeToLog("INFO","Step 21: Going to publish the " + self.publishName3 +"  entry")
            if self.common.myMedia.publishSingleEntry(self.publishName3, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 21: FAILED to publish the " + self.publishName3 +"  entry")
                return
 
            writeToLog("INFO","Step 22: Going to set In Scheduling time-frame publishing to " + self.publishName3 + " entry")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryPastStartDate, startTime=self.entryPastStartTime, endDate=self.entryFutureStartDate,endTime=self.entryFutureStartTime, entryName=self.publishName3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to set Future time-frame publishing to " + self.publishName3 + " entry")
                return

            writeToLog("INFO","TEST PASSED: All the video entries were properly created with Scheduling conditions and published successfully")
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
