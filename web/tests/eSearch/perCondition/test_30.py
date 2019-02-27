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
    #  @Author: Horia Cus
    # Test Name : Setup test for eSearch
    # Test description:
    # Going to upload six type of entries (video, quiz, audio, image, youtube and webcast)
    # Going to add co-editor permissions to an user for all of the entries
    #================================================================================================================================
    testNum = "30"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryNameVideo      = "Filter by Ownership - secondtype Video"
    entryNameQuiz       = "Filter by Ownership - secondtype Quiz"
    entryNameAudio      = "Filter by Ownership - secondtype Audio"
    entryNameImage      = "Filter by Ownership - secondtype Image"
    entryNameYoutube    = "Filter by Ownership - secondtype Youtube"
    entryNameWebCast    = "Filter by Ownership - secondtype Webcast"
    publishNameQuiz     = "Filter by Ownership - secondtype Quiz - Quiz"

    entryDescription = "filter by ownership"
    entryTags = "tag1,"

    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    youtuebLink = "https://www.youtube.com/watch?v=usNsCeOV4GM"

    entryStartDate = (datetime.datetime.now() + timedelta(days=240)).strftime("%d/%m/%Y")
    entryEndDate = (datetime.datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y")
    entryStartTime = time.time() + (60*60)
    entryStartTime= time.strftime("%I:%M %p",time.localtime(entryStartTime))
    entryEndTime = time.time() + (60*60)
    entryEndTime= time.strftime("%I:%M %p",time.localtime(entryEndTime))

    QuizQuestion1 = 'First question'
    QuizQuestion1Answer1 = 'First answer'
    QuizQuestion1AdditionalAnswers = ['Second answer', 'Third question', 'Fourth question']

    channelTags = "Tags,"
    userName1 = "adminForEsearch" # main user
    userPass1 = "123456"
    
    userName2 = "inbar.willman@kaltura.com"
    userPass2 = "Kaltura1!"

    coEditorUser = "admin"

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
            self.categoryForModerator = "category for eSearch moderator"
            self.categoryForEsearch = 'eSearch category'

            # Channel for tests in channel/ add to channel tabs
            self.channelForModerator = "channel moderator for eSearch"
            self.channelForEsearch  = "Channel for eSearch"

            self.entryPermissionList = [self.entryNameVideo, self.publishNameQuiz, self.entryNameImage, self.entryNameAudio, self.entryNameYoutube, self.entryNameWebCast]
            self.approveEntriesInChannel = [self.entryNameAudio, self.entryNameImage, self.publishNameQuiz, self.entryNameVideo, self.entryNameWebCast, self.entryNameYoutube]
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return

            writeToLog("INFO","Step 2: Going to upload " + self.entryNameVideo + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryNameVideo, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload " + self.entryNameVideo + " entry")
                return
 
            writeToLog("INFO","Step 3: Going to publish the " + self.entryNameVideo +"  entry")
            if self.common.myMedia.publishSingleEntry(self.entryNameVideo, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 3: FAILED to publish the " + self.entryNameVideo +"  entry")
                return
 
            writeToLog("INFO","Step 4: Going to upload " + self.entryNameQuiz + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryNameQuiz, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to upload " + self.entryNameQuiz + " entry")
                return
 
            writeToLog("INFO","Step 5: Going to navigate to " + self.entryNameQuiz + " entry")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to " + self.entryNameQuiz + " entry")
                return
 
            writeToLog("INFO","Step 6: Going to search  " + self.entryNameQuiz + " entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryNameQuiz, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to find  " + self.entryNameQuiz + " entry and open KEA")
                return
 
            writeToLog("INFO","Step 7: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to start quiz and add questions")
                return
 
            writeToLog("INFO","Step 8: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to save quiz and navigate to media page")
                return
 
            writeToLog("INFO","Step 9: Going to publish the " + self.publishNameQuiz +"  entry")
            if self.common.myMedia.publishSingleEntry(self.publishNameQuiz, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 9: FAILED to publish the " + self.publishNameQuiz +"  entry")
                return
 
            writeToLog("INFO","Step 10: Going to upload " + self.entryNameAudio + " entry")
            if self.common.upload.uploadEntry(self.filePathAudio, self.entryNameAudio, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to upload " + self.entryNameAudio + " entry")
                return
 
            writeToLog("INFO","Step 11: Going to publish " + self.entryNameAudio + " entry")
            if self.common.myMedia.publishSingleEntry(self.entryNameAudio, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 11: FAILED to publish " + self.entryNameAudio + " entry")
                return
 
            writeToLog("INFO","Step 12: Going to upload " + self.entryNameImage + " entry")
            if self.common.upload.uploadEntry(self.filePathImage, self.entryNameImage, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to upload " + self.entryNameImage + " entry")
                return
 
            writeToLog("INFO","Step 13: Going to publish " + self.entryNameImage + " entry")
            if self.common.myMedia.publishSingleEntry(self.entryNameImage, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 13: FAILED to publish " + self.entryNameImage + " entry")
                return
 
            writeToLog("INFO","Step 14: Going to navigate to youtube upload page")
            if self.common.upload.clickAddYoutube() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to navigate to youtube upload page")
                return
 
            writeToLog("INFO","Step 15: Going to upload " + self.entryNameYoutube +" entry")
            if self.common.upload.addYoutubeEntry(self.youtuebLink, self.entryNameYoutube) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to upload " + self.entryNameYoutube +"  entry")
                return
 
            writeToLog("INFO","Step 16: Going to publish the " + self.entryNameYoutube +"  entry")
            if self.common.myMedia.publishSingleEntry(self.entryNameYoutube, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 16: FAILED to publish the " + self.entryNameYoutube +"  entry")
                return
 
            writeToLog("INFO","Step 17: Going to upload " + self.entryNameWebCast + " entry")
            if self.common.upload.addWebcastEntry(self.entryNameWebCast, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to upload " + self.entryNameWebCast + " entry")
                return
 
            writeToLog("INFO","Step 18: Going to set a custom time frame for " + self.entryNameWebCast + " entry")
            if self.common.editEntryPage.addPublishingSchedule(startDate=self.entryStartDate, startTime=self.entryStartTime, endDate=self.entryEndDate, endTime=self.entryEndTime, entryName=self.entryNameWebCast)== False:
                writeToLog("INFO","Step 18: FAILED to set a custom time frame for " + self.entryNameWebCast + " entry")
                return
 
            writeToLog("INFO","Step 19: Going to publish " + self.entryNameWebCast + " entry")
            if self.common.myMedia.publishSingleEntry(self.entryNameWebCast, [self.categoryForModerator, self.categoryForEsearch], [self.channelForEsearch, self.channelForModerator], publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 19: FAILED to publish " + self.entryNameWebCast + " entry")
                return

            i = 20
            for entry in self.entryPermissionList:
                i = i

                writeToLog("INFO", "Step " + str(i) + ": Going to navigate to " + entry + " entry")
                if self.common.editEntryPage.navigateToEditEntry(entry) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to navigate to " + entry + " entry")
                    return
                else:
                    i = i + 1

                writeToLog("INFO", "Step " + str(i) + ": Going to add permissions for " + self.coEditorUser + " in " + entry + " entry")
                if self.common.editEntryPage.addCollaborator(entry, userId=self.coEditorUser, isCoEditor=True, isCoPublisher=False) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": FAILED to add permissions for " + self.coEditorUser + " in " + entry + " entry")
                    return
                else:
                    i = i + 1
            sleep(10)
                    
            writeToLog("INFO","Step " + str(i) + ": Going to logout from the " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout from the " + self.userName1)
                return
            
            writeToLog("INFO","Step " + str(i) + ": Going to log in with the " + self.userName2)
            if self.common.login.loginToKMS(self.userName2, self.userPass2) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to log in with the " + self.userName2)
                return
            else:
                i = i + 1
            i = i
            
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.channelForEsearch)
            if self.common.channel.navigateToPendingaTab(self.channelForEsearch, enums.Location.CHANNEL_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.channelForEsearch)
                return
            else:
                i = i + 1
            i = i
            
            writeToLog("INFO","Step " + str(i) + ": Going to approve the entries in " + self.channelForEsearch)
            if self.common.channel.pendingBulkRejectAndApprove(self.approveEntriesInChannel, moderateAction=enums.PendingModerateAction.APPROVE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to approve the entries in " + self.channelForEsearch)
                return
            else:
                i = i + 1
            i = i
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