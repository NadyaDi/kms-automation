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
    # Test Name : Quiz - Analytics - Verify quiz answers - One user
    # Test description:
    # Go to editor page and create quiz with option all type of questions
    # Go to quiz page and answer all questions -> Go to quiz analytics -> Quiz Questions -> Verify that correct open-Q is displayed and correct number of 
    # wrong and correct answers is displayed
    #================================================================================================================================
    testNum = "5116"
    
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
    answerquestionNumber2Attempt1 = "False text"
    
    questionNumber3Attempt1 = 'Question Title for Open-Q'
    answerquestionNumber3Attempt1 = 'Open-Q answer - One'
    
    questionNumber4Attempt1 = 'Question Title for Reflection Point'
    answerquestionNumber4Attempt1 = 'Viewed'

    quizQuestionDictAttempt1 = {questionNumber1Attempt1:answerquestionNumber1Attempt1, questionNumber2Attempt1:answerquestionNumber2Attempt1, questionNumber3Attempt1:answerquestionNumber3Attempt1}
    
    # Score for each attempt - individual for each attempts
    quizScore = '67'
    
    firstQuestionAnswers = [questionNumber1Attempt1, answerquestionNumber1Attempt1, 'QA ADMIN', '1', '0', True]
    secondQuestionAnswers = [questionNumber2Attempt1, answerquestionNumber2Attempt1, 'QA ADMIN', '0', '1', False]
    thirdQuestionAnswers = [questionNumber3Attempt1, answerquestionNumber3Attempt1, 'QA ADMIN', '1', '0', True]
    FourthQuestionAnswers = [questionNumber4Attempt1, answerquestionNumber4Attempt1, 'QA ADMIN', '1', '0', True]
#     # List with all answers
#     answersDict = {'1':firstQuestionAnswers,'2':secondQuestionAnswers, '3': thirdQuestionAnswers, '4':FourthQuestionAnswers}
    firstQuestionUsersAnswers = {'1': firstQuestionAnswers}
    secondQuestionAnswers = {'1': secondQuestionAnswers}
    thirdQuestionAnswers = {'1': thirdQuestionAnswers}
    FourthQuestionAnswers = {'1': FourthQuestionAnswers}
    
    answerList = [firstQuestionUsersAnswers, secondQuestionAnswers, thirdQuestionAnswers, FourthQuestionAnswers]
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
            self.entryName = clsTestService.addGuidToString("Quiz Analytics - Verify answers", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz Analytics - Verify answers - Quiz", self.testNum)      

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
              
            writeToLog("INFO","Step 5 : Going to answer quiz open question")  
            if self.common.player.answerQuiz(self.quizQuestionDictAttempt1, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='50') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5 : FAILED to answer quiz open question")  
                return    
             
            self.common.base.switch_to_default_content()
            
            writeToLog("INFO","Step 6 : Going to verify quiz answers in quiz analytics")  
            if self.common.quizAnalytics.verifyQuizAnswersInAnalytics(self.answerList, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6 : FAILED to verify quiz answers in quiz analytics")  
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