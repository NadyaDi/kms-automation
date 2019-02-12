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
    # Test Name :  Quiz - Youtube based entry: Submitted Quiz with many Quiz Questions (15 questions)
    # Test description:
    # Verify that the user is able to start and submit a youtube entry, with  15 'Multiple Choice', 'True and False' and 'Reflection Point' quiz question types 
    # Verify that the user is able to answer to all the quiz question types
    # Verify that the submitted screen, proper displays the result score and why
    # Verify the answers, and 'Hint' from Quiz Question screen
    #================================================================================================================================
    testNum = "4814"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description     = "Description" 
    tags            = "Tags,"
    filePathYotubue = 'https://www.youtube.com/watch?v=W2D2EGRw5-E'
    typeTest        = 'Quiz Youtube Entry New State with Media Owner user'
            
    # Each list is used in order to create a different Quiz Question Type
    questionMultipleOne         = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice One', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalseTwo     = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False Two', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflectionThree     = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point Three']
    questionMultipleFour        = ['00:25', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice Four', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalseFive    = ['00:30', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False Five', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflectionSix       = ['00:35', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point Six']
    questionMultipleSeven       = ['00:40', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice Seven', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalseEight   = ['00:45', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False Eight', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflectionNine      = ['00:50', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point Nine']
    questionMultipleTen         = ['00:55', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice Ten', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalseEleven  = ['00:60', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False Eleven', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflectionTwelve    = ['00:65', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point Twelve']
    questionMultipleThirteen    = ['00:70', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice Thirteen', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalseFourteen= ['00:75', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False Fourteen', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflectionFifteen   = ['00:80', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point Fifteen']

    # Each list is used in order to verify that all the Quiz Question types are answered
    questionAnswerOne           = ['Question Title for Multiple Choice One', 'question #1 option #1', True]
    questionAnswerTwo           = ['Question Title for True and False Two', 'True text', True]
    questionAnswerThree         = ['Question Title for Reflection Point Three', '', True]
    questionAnswerFour          = ['Question Title for Multiple Choice Four', 'question #1 option #1', True]
    questionAnswerFive          = ['Question Title for True and False Five', 'True text', True]
    questionAnswerSix           = ['Question Title for Reflection Point Six', '', True]
    questionAnswerSeven         = ['Question Title for Multiple Choice Seven', 'question #1 option #1', True]
    questionAnswerEight         = ['Question Title for True and False Eight', 'True text', True]
    questionAnswerNine          = ['Question Title for Reflection Point Nine', '', True]
    questionAnswerTen           = ['Question Title for Multiple Choice Ten', 'question #1 option #1', True]
    questionAnswerEleven        = ['Question Title for True and False Eleven', 'True text', True]
    questionAnswerThirteen      = ['Question Title for Reflection Point Thirteen', '', True]
    questionAnswerFourteen      = ['Question Title for Multiple Choice Fourteen', 'question #1 option #1', True]
    questionAnswerFifteen       = ['Question Title for True and False Fifteen', 'True text', True]
    
    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizStateNew     = {'1':questionAnswerOne,'2':questionAnswerTwo, '3':questionAnswerThree} 

    # This Dictionary is used in order to create all the Quiz Question types within a single call
    questionDict             = {'1':questionMultipleOne,'2':questionTrueAndFalseTwo,'3':questionReflectionThree, '4':questionMultipleFour,'5':questionTrueAndFalseFive,'6':questionReflectionSix, '7':questionMultipleSeven,'8':questionTrueAndFalseEight,'9':questionReflectionNine, '10':questionMultipleTen,'11':questionTrueAndFalseEleven,'12':questionReflectionTwelve, '13':questionMultipleThirteen,'14':questionTrueAndFalseFourteen,'15':questionReflectionFifteen}    
    # This values are used in order to find and answer to the quiz questions
    questionName1            = "Question Title for Multiple Choice"
    answerText1              = "question #1 option #1"
    
    questionName2            = "Question Title for True and False"
    answerText2              = "True text"
        
    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be present in the Question Name
    answersDict = {questionName1:answerText1,
                   questionName2:answerText2} 
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
            self.entryName       = clsTestService.addGuidToString("Quiz - Youtube Entry New", self.testNum)
            self.newEntryName    = clsTestService.addGuidToString("Quiz - Youtube Entry New - Quiz", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            i = 1 
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to youtube upload page")
            if self.common.upload.clickAddYoutube() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to youtube upload page")
                return
            else:
                i = i + 1

            writeToLog("INFO","Step " + str(i) + ": Going to upload " + self.entryName +" entry")
            if self.common.upload.addYoutubeEntry(self.filePathYotubue, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to upload " + self.entryName +"  entry")
                return
                return  
            else:
                i = i + 1
                                              
            writeToLog("INFO","Step " + str(i) + ": Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
            else:
                i = i + 1
                    
            writeToLog("INFO","Step " + str(i) + ": Going to answer to all the Quiz Questions from the " + self.newEntryName + " entry")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='') == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer to all the Quiz Questions from the " + self.newEntryName + " entry")  
                return  
            else:
                i = i + 1            
                 
            writeToLog("INFO","Step " + str(i) + ": Going to resume from the beginning the " + self.newEntryName + " entry")  
            if self.common.player.resumeFromBeginningQuiz(enums.Location.ENTRY_PAGE, timeOut=1, forceResume=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to resume from the beginning the " + self.newEntryName + " entry")
                return  
            else:
                i = i + 1
            
            writeToLog("INFO","Step " + str(i) + ": Going to verify that all the available quiz questions from the " + self.newEntryName + " entry remained answered")  
            if self.common.player.quizVerification(self.questionDict, self.expectedQuizStateNew, submittedQuiz=True, resumeQuiz=False, newQuiz=False, expectedQuizScore=str(100), location=enums.Location.ENTRY_PAGE, timeOut=60) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that all the available quiz questions from the " + self.newEntryName + " entry remained answered")
                return  
            else:
                i = i + 1
            ##################################################################
            writeToLog("INFO","TEST PASSED: Entry Page has been successfully verified for a " + self.typeTest)
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