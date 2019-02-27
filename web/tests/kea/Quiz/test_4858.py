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
    # Test Name : Quiz - Deleted Questions inside a Quiz entry - Submitted in Entry Page
    # Test description:
    # Verify that the user is able to create a Quiz entry that contains Five Questions
    # 1. Verify that all the Questions are displayed as answered in the entry page
    # Verify that the user is able to edit the Quiz entry by deleting two Questions
    # 1. Enter in KEA Editor and delete two Questions
    # 2. Verify that the KEA Editor timeline was changed properly
    # 3. Verify that only the remained Questions are displayed in the Entry Page
    # 4. Verify that the user is able to answer to all of the available questions
    # 5. Verify that the submitted score matches with the expected score
    #================================================================================================================================
    testNum = "4858"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    typeTest = 'Quiz Entry with five questions and two of them deleted'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_60sec.mp4'
        
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:20', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:30', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']
    questionNumber4 = ['00:40', enums.QuizQuestionType.Multiple, 'question #4 Title', 'question #4 option #1', 'question #4 option #2', 'question #4 option #3', 'question #4 option #4']
    questionNumber5 = ['00:50', enums.QuizQuestionType.Multiple, 'question #5 Title', 'question #5 option #1', 'question #5 option #2', 'question #5 option #3', 'question #5 option #4']

    # This dictionary is used in order to create the quiz questions
    dictQuestions         = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3, '4':questionNumber4, '5':questionNumber5}
    
    dictQuestionsUpdated  = {'1':questionNumber2,'2':questionNumber3,'3':questionNumber4}    

    # Each list is used in order to verify that all the Quiz Question types were unanswered
    questionAnswerOne        = ['question #1 Title', '', False]
    questionAnswerTwo        = ['question #2 Title', '', False]
    questionAnswerThree      = ['question #3 Title', '', False]
    questionAnswerFour       = ['question #4 Title', '', False]
    questionAnswerFive       = ['question #5 Title', '', False]
    
    # This variables are used in order to find and answer to the quiz questions
    questionName1            = "question #2 Title"
    answerText1              = "question #2 option #1"
    
    questionName2            = "question #3 Title"
    answerText2              = "question #3 option #1"
    
    questionName3            = "question #4 Title"
    answerText3              = "question #4 option #4"
    
    # Each list is used in order to verify that the remained Questions were properly answered
    
    questionAnswerTwoAnswered        = ['question #2 Title', 'question #2 option #1', True]
    questionAnswerThreeAnswered      = ['question #3 Title', 'question #3 option #1', True]
    questionAnswerFourAnswered       = ['question #4 Title', 'question #4 option #4', False]
        
    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be present in the Question Name
    answersDict = {questionName1:answerText1,
                   questionName2:answerText2,
                   questionName3:answerText3
                   } 
    
    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedInitialQuizState         = {'1':questionAnswerOne,'2':questionAnswerTwo, '3':questionAnswerThree, '4':questionAnswerFour, '5':questionAnswerFive}
    expectedAfterDeleteQuizState     = {'1':questionAnswerTwo, '2':questionAnswerThree, '3':questionAnswerFour}
    expectedSubmittedScreenResults   = {'1':questionAnswerTwoAnswered, '2':questionAnswerThreeAnswered, '3':questionAnswerFourAnswered}
    
    # This list is used in order to delete Quiz Questions
    questionDeleteList = ['question #1 Title', 'question #5 Title']
    
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
            self.entryName           = clsTestService.addGuidToString("Quiz - Deleted Questions and Submit in Entry Page", self.testNum)
            self.entryNameQuiz       = clsTestService.addGuidToString("Quiz - Deleted Questions and Submit in Entry Page - Quiz", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to create a new entry, " + self.entryName)  
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create a new entry, " + self.entryName)  
                return
                        
            writeToLog("INFO","Step 2: Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return
            sleep(5)
                 
            writeToLog("INFO","Step 3: Going to verify that all the available quiz questions from the " + self.entryNameQuiz + " entry are displayed")  
            if self.common.player.quizVerification(self.dictQuestions, self.expectedInitialQuizState, submittedQuiz=False, resumeQuiz=False, newQuiz=True, expectedQuizScore='', location=enums.Location.ENTRY_PAGE, timeOut=60) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: to verify that all the available quiz questions from the " + self.entryNameQuiz + " entry are displayed")  
                return  
  
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 4: Going to navigate to " + self.entryNameQuiz + " entry KEA Editor")  
            if self.common.kea.launchKEA(self.entryNameQuiz, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to navigate to " + self.entryNameQuiz + " entry KEA Editor")  
                return
             
            writeToLog("INFO","Step 5: Going to delete two Questions from " + self.entryNameQuiz + " entry")  
            if self.common.kea.deleteQuestions(self.questionDeleteList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to delete two Questions from " + self.entryNameQuiz + " entry")
                return
             
            writeToLog("INFO","Step 6: Going to navigate to " + self.entryNameQuiz + " Entry page")  
            if self.common.kea.navigateToEntryPageFromKEA(self.entryNameQuiz) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate to " + self.entryNameQuiz + " Entry page")  
                return
              
            writeToLog("INFO","Step 7: Going to verify that only the remaining Questions from " + self.entryNameQuiz + " entry are displayed")  
            if self.common.player.quizVerification(self.dictQuestionsUpdated, self.expectedAfterDeleteQuizState, submittedQuiz=False, resumeQuiz=False, newQuiz=True, expectedQuizScore='', location=enums.Location.ENTRY_PAGE, timeOut=60) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: to verify that only the remaining Questions from " + self.entryNameQuiz + " entry are displayed") 
                return      
                       
            writeToLog("INFO","Step 8: Going to answer to all the Quiz Questions from the " + self.entryNameQuiz + " entry")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to answer to all the Quiz Questions from the " + self.entryNameQuiz + " entry")  
                return             
                    
            writeToLog("INFO","Step 9: Going to resume from the beginning the " + self.entryNameQuiz + " entry")  
            if self.common.player.resumeFromBeginningQuiz(enums.Location.ENTRY_PAGE, timeOut=1, forceResume=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to resume from the beginning the " + self.entryNameQuiz + " entry")
                return  
               
            writeToLog("INFO","Step 10: Going to verify that all the available quiz questions from the " + self.entryNameQuiz + " entry remained answered and the Expected Score is displayed in the Submitted screen")  
            if self.common.player.quizVerification(self.dictQuestionsUpdated, self.expectedSubmittedScreenResults, submittedQuiz=True, resumeQuiz=False, newQuiz=False, expectedQuizScore=str(67), location=enums.Location.ENTRY_PAGE, timeOut=60) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to verify that all the available quiz questions from the " + self.entryNameQuiz + " entry remained answered and the Expected Score is displayed in the Submitted screen")  
                return  
            ##################################################################
            writeToLog("INFO","TEST PASSED: Entry page has been successfully verified for a " + self.typeTest)
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.entryNameQuiz])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')