import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
from selenium.webdriver.common.keys import Keys

class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # Test Name : Retake Quiz - Latest score type - All type of questions
    # Test description:
    # Go to editor page and create quiz with option to retake quiz - 3 attempts and all type of questions
    # Go to quiz page and verify that user is able to retake quiz 3 times3 attempts, open-Q doesn't effect the score
    #================================================================================================================================
    testNum = "5105"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text']
    questionNumber3 = ['00:20', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q'] 
    questionNumber4 = ['00:25', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']  
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3,'4':questionNumber4} 
    
    # Attempts #1 answers
    questionNumber1Attempt1 = "question #1 Title"
    answerquestionNumber1Attempt1 = "question #1 option #1"
    
    questionNumber2Attempt1 = "Question Title for True and False"
    answerquestionNumber2Attempt1 = "True text"
    
    questionNumber3Attempt1 = 'Question Title for Open-Q'
    answerquestionNumber3Attempt1 = 'Answer for Open-Q first attempt'
    
    # Attempts #2 answers
    questionNumber1Attempt2 =  "question #1 Title"
    answerquestionNumber1Attempt2 = "question #1 option #2"
    
    questionNumber2Attempt2 = "Question Title for True and False"
    answerquestionNumber2Attempt2 = "False text"
    
    questionNumber3Attempt2 = 'Question Title for Open-Q'
    answerquestionNumber3Attempt2 = 'Answer for Open-Q second attempt'
    
    # Attempts #3 answers
    questionNumber1Attempt3 = "question #1 Title"
    answerquestionNumber1Attempt3 = "question #1 option #1"
    
    questionNumber2Attempt3 = "Question Title for True and False"
    answerquestionNumber2Attempt3 = "False text"
    
    questionNumber3Attempt3 = 'Question Title for Open-Q'
    answerquestionNumber3Attempt3 = 'Answer for Open-Q third attempt'

    quizQuestionDictAttempt1 = {questionNumber1Attempt1:answerquestionNumber1Attempt1, questionNumber2Attempt1:answerquestionNumber2Attempt1, questionNumber3Attempt1:answerquestionNumber3Attempt1}
    quizQuestionDictAttempt2 = {questionNumber1Attempt2:answerquestionNumber1Attempt2, questionNumber2Attempt2:answerquestionNumber2Attempt2, questionNumber3Attempt2:answerquestionNumber3Attempt2}
    quizQuestionDictAttempt3 = {questionNumber1Attempt3:answerquestionNumber1Attempt3, questionNumber2Attempt3:answerquestionNumber2Attempt3, questionNumber3Attempt3:answerquestionNumber3Attempt3}
    
    quizQuestionsDictAllAttempts = [quizQuestionDictAttempt1, quizQuestionDictAttempt2, quizQuestionDictAttempt3]
    
    # Score for each attempt - individual for each attempts
    specificScoreAttempt1 = '100'
    specificScoreAttempt2 = '0'
    specificScoreAttempt3 = '50'
    
    quizSpecificAttemptScore = [specificScoreAttempt1, specificScoreAttempt2, specificScoreAttempt3]
    
    # Score for each attempt - general for all attempts
    generalScoreAttempt1 = '100'
    generalScoreAttempt2 = '0'
    generalScoreAttempt3 = '50'
    
    quizGeneralAttemptsScore = [generalScoreAttempt1, generalScoreAttempt2, generalScoreAttempt3]
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Retake 3 Attempts All types of questions", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Retake 3 Attempts types of questions - Quiz", self.testNum)      

            self.keaScoreType                    = {enums.KEAQuizOptions.QUIZ_SCORE_TYPE:enums.keaQuizScoreType.LATEST.value}
            self.keaNumberOfAllowedAttempts      = {enums.KEAQuizOptions.SET_NUMBER_OF_ATTEMPTS:3}
            self.keaAllowMultipleScore           = {enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:True}
            
            self.keaScoreOptions                 = [self.keaAllowMultipleScore, self.keaNumberOfAllowedAttempts, self.keaScoreType]
            
            self.keaAllScoreOptionsList          = [self.keaScoreOptions]     
            
            self.totalGivenAttempts              = 3
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
                  
            self.common.base.get_body_element().send_keys(Keys.PAGE_DOWN)
                                     
            writeToLog("INFO","Step 2: Going to to navigate to entry page")    
            if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate entry page")
                return
                                     
            writeToLog("INFO","Step 3: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to wait until media end upload process")
                return
                                                                    
            writeToLog("INFO","Step 4 : Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4 : FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return
                  
            writeToLog("INFO","Step 5: Going to navigate to KEA Quiz tab for " + self.quizEntryName)  
            if self.common.kea.initiateQuizFlow(self.quizEntryName, True, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to KEA Quiz tab for " + self.quizEntryName)  
                return 
                  
            i = 6
                  
            for option in self.keaAllScoreOptionsList:
                optionNumber = 0
                while len(option) != optionNumber:
                    writeToLog("INFO","Step " + str(i) + ": Going to edit the " + enums.KEAQuizSection.SCORES.value + " section by modifying the " + next(iter(option[optionNumber])).value)  
                    if self.common.kea.editQuizOptions(enums.KEAQuizSection.SCORES, option[optionNumber]) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to edit the " + enums.KEAQuizSection.SCORES.value + " section by modifying the " + next(iter(option[optionNumber])).value)
                        return
                    else:
                        i = i + 1                     
                        optionNumber = optionNumber + 1
                 
            self.common.base.switch_to_default_content()
           
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.quizEntryName + " page")  
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.quizEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.quizEntryName + " page")
                return
            i = i +1
            
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.quizQuestionsDictAllAttempts, expectedQuizScore=self.quizSpecificAttemptScore, totalGivenAttempts=self.totalGivenAttempts, expectedAttemptGeneralScore=self.quizGeneralAttemptsScore, scoreType=enums.playerQuizScoreType.LATEST) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return             

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Retake quiz - based on latest score include open-Q was created and answered successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.quizEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')