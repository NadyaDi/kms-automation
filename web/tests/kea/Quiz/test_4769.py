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
    # Test Name : Quiz Scores section in Entry Page - Default
    # Test description:
    # Verify that all the KEA Quiz Scores options have proper functionality by:
    # Verifying that the "Do not Show Scores", "Show Scores" and "Include Answers" have proper states
    #================================================================================================================================
    testNum = "4769"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None

    # Test variables
    description = "Description"
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'

    showScoreEnabledWithIncludedAnswersEnabled       = "You completed the quiz and your score is 100 %\nPress any question to review how you performed"
    showScoreEnabledWithIncludedAnswersDisabled      = "You completed the quiz and your score is 100 %"
    showScoreDisabledWithIncludeAnswerDisabled       = "You completed the quiz"

    userName = "python_automation"
    password = "Kaltura1!"

    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4']
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4']
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3}

    questionName1 = "question #1 Title"
    answerText1   = "question #1 option #1"

    questionName2 = "question #2 Title"
    answerText2   = "question #2 option #1"

    questionName3 = "question #3 Title"
    answerText3   = "question #3 option #1"

    entryUrl = ''

    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be present in the Question Name
    questionDict = {questionName1:answerText1,
                    questionName2:answerText2,
                    questionName3:answerText3}

    #this dictionary is used in order to verify that proper elements are present in the include answer screen
    includeAnswersDict = {questionName1:{'correct':answerText1, 'given':answerText1},
                          questionName2:{'correct':answerText2, 'given':answerText2},
                          questionName3:{'correct':answerText3, 'given':answerText3}}
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
            ##################################################################
            self.entryName          = clsTestService.addGuidToString("Quiz - Score Default", self.testNum)
            self.newEntryName       = clsTestService.addGuidToString("Quiz - Score Default - Quiz", self.testNum)
            # this dictionary is used in order to verify the options
            self.doNotShowShowScoreDefaultList      = [enums.KEAQuizOptions.DO_NOT_SHOW_SCORES, self.showScoreEnabledWithIncludedAnswersEnabled]
            self.showScoresDefaultList              = [enums.KEAQuizOptions.SHOW_SCORES, self.showScoreEnabledWithIncludedAnswersEnabled]
            self.includeAnswersDefaultList          = [enums.KEAQuizOptions.INCLUDE_ANSWERS, self.includeAnswersDict]

            self.scoreOptionDefaultList             = [self.doNotShowShowScoreDefaultList, self.showScoresDefaultList, self.includeAnswersDefaultList]
            ##################### TEST STEPS - MAIN FLOW #####################
            i = 1
            writeToLog("INFO","Step " + str(i) + ": Going to create a new entry, " + self.entryName)
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new entry, " + self.entryName)
                return
            else:
                i = i + 1

            writeToLog("INFO","Step " + str(i) + ": Going to create a new Quiz for the " + self.entryName + " entry")
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new Quiz for the " + self.entryName + " entry")
                return
            else:
                i = i + 1
            self.entryUrl = self.common.base.driver.current_url

            writeToLog("INFO","Step " + str(i) + ": Going to publish the " + self.entryName +" entry as unlisted ")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate(self.newEntryName, enums.ChannelPrivacyType.UNLISTED, alreadyPublished=False, publishFrom=enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step " + str(i) + ": FAILED to publish the " + self.entryName + " entry as unlisted")
                return
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to log out from the " + self.userName + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from the " + self.userName + " account")   
                return
            else:
                i = i + 1

            self.common.base.navigate(self.entryUrl)
            writeToLog("INFO","Step " + str(i) + ": Going to answer to all of the available Quiz while using a Guest account")
            if self.common.player.answerQuiz(self.questionDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='') == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer to all of the available Quiz while using a Guest account")
                return
            else:
                i = i + 1

            for option in self.scoreOptionDefaultList:
                writeToLog("INFO","Step " + str(i) + ":Going to verify the KEA Section " + enums.KEAQuizSection.SCORES.value + " changes for " + next(iter(option)).value + " that are properly displayed in the " + self.newEntryName + " entry page")
                if self.common.entryPage.verifyQuizOptionsInEntryPage(enums.KEAQuizSection.SCORES, option[0], option[1], keaOptionEnabled=True, navigateToEntryPageFromKEA=True, entryName=self.newEntryName) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to verify the KEA Section " + enums.KEAQuizSection.SCORES.value + " changes for " + next(iter(option)).value + " that are properly displayed in the " + self.newEntryName + " entry page")
                    return
                else:
                    i = i + 1

            writeToLog("INFO","Step " + str(i) + ": Going to authenticate using " + self.userName + " account")
            if self.common.login.loginToKMS(self.userName, self.password) == False:
                writeToLog("INFO", "Step " + str(i) + ":FAILED to authenticate using " + self.userName + " account")
                return
            else:
                i = i + 1
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the KEA Score options were properly displayed with default state and verified in KEA Entry Page")
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.newEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')