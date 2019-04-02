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
    # Test Name : Quiz - Retake quiz - Average score type
    # Test description:
    # Go to editor page and create quiz with option to retake quiz - 3 attempts and first score type
    # Go to quiz page and verify that user is able to retake quiz 3 times and score is based on first score
    #================================================================================================================================
    testNum = "5100"
    
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
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']   
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3} 
    
    # Attempts #1 answers
    questionNumber1Attempt1 = "question #1 Title"
    answerquestionNumber1Attempt1 = "question #1 option #1"
    
    questionNumber2Attempt1 = "question #2 Title"
    answerquestionNumber2Attempt1 = "question #2 option #2"
    
    questionNumber3Attempt1 = "question #3 Title"
    answerquestionNumber3Attempt1 = "question #3 option #2"

    
    # Attempts #2 answers
    questionNumber1Attempt2 = "question #1 Title"
    answerquestionNumber1Attempt2 = "question #1 option #1"
    
    questionNumber2Attempt2 = "question #2 Title"
    answerquestionNumber2Attempt2 = "question #2 option #1"
    
    questionNumber3Attempt2 = "question #3 Title"
    answerquestionNumber3Attempt2 = "question #3 option #2"
    
    # Attempts #3 answers
    questionNumber1Attempt3 = "question #1 Title"
    answerquestionNumber1Attempt3 = "question #1 option #1"
    
    questionNumber2Attempt3 = "question #2 Title"
    answerquestionNumber2Attempt3 = "question #2 option #1"
    
    questionNumber3Attempt3 = "question #3 Title"
    answerquestionNumber3Attempt3 = "question #3 option #1"    

    quizQuestionDictAttempt1 = {questionNumber1Attempt1:answerquestionNumber1Attempt1, questionNumber2Attempt1:answerquestionNumber2Attempt1, questionNumber3Attempt1:answerquestionNumber3Attempt1}
    quizQuestionDictAttempt2 = {questionNumber1Attempt2:answerquestionNumber1Attempt2, questionNumber2Attempt2:answerquestionNumber2Attempt2, questionNumber3Attempt2:answerquestionNumber3Attempt2}
    quizQuestionDictAttempt3 = {questionNumber1Attempt2:answerquestionNumber1Attempt3, questionNumber2Attempt3:answerquestionNumber2Attempt3, questionNumber3Attempt3:answerquestionNumber3Attempt3}
    
    quizQuestionsDictAllAttempts = [quizQuestionDictAttempt1, quizQuestionDictAttempt2, quizQuestionDictAttempt3]
    
    # Score for each attempt - individual for each attempts
    specificScoreAttempt1 = '33'
    specificScoreAttempt2 = '67'
    specificScoreAttempt3 = '100'
    
    quizSpecificAttemptScore = [specificScoreAttempt1, specificScoreAttempt2, specificScoreAttempt3]
    
    # Score for each attempt - general for all attempts
    generalScoreAttempt1 = '33'
    generalScoreAttempt2 = '50'
    generalScoreAttempt3 = '67'
    
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
            self.entryName = clsTestService.addGuidToString("Retake 3 Attempts Average score", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Retake 3 Attempts Average score - Quiz", self.testNum)  
            self.questionAnswer = "Answer for open question"    

            self.keaScoreType                    = {enums.KEAQuizOptions.QUIZ_SCORE_TYPE:enums.keaQuizScoreType.AVERAGE.value}
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
            
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.quizQuestionsDictAllAttempts, expectedQuizScore=self.quizSpecificAttemptScore, totalGivenAttempts=self.totalGivenAttempts, expectedAttemptGeneralScore=self.quizGeneralAttemptsScore, scoreType=enums.playerQuizScoreType.AVERAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return             

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Retake quiz - based on Average score was created and answered successfully")
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