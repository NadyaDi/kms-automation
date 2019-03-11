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
    # Test Name : Quiz - Player preview Sanity Check for an existing Quiz Entry
    # Test description:
    # Verify that the user is able to launch the Player Preview screen while being in the Quiz Tab from KEA Editor
    # Verify that the user is able to skip the quiz welcome screen, answer to all of the Question types 
    # Verify that the Submitted screen is properly displayed with the expected results
    # Verify that the user is able to dismiss the Player Preview screen
    #================================================================================================================================
    testNum = "4954"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description   = "Description" 
    tags          = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    typeTest      = 'Quiz Entry where we performed a Sanity Check for the Player Preview'
            
    # Each list is used in order to create a different Quiz Question Type
    questionMultiple         = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalse     = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflection       = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']
    
    # This Dictionary is used in order to create all the Quiz Question types within a single call
    questionDict             = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection}
    
    # This values are used in order to find and answer to the quiz questions
    questionName1            = "Question Title for Multiple Choice"
    answerText1              = "question #1 option #1"
    
    questionName2            = "Question Title for True and False"
    answerText2              = "True text"
        
    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be presented in the Question Name
    answersDict = {questionName1:answerText1,
                   questionName2:answerText2}
    
    # Each list is used in order to verify that all the Quiz Question types are answered
    questionAnswerOneSubmitted        = ['Question Title for Multiple Choice', 'question #1 option #1', True]
    questionAnswerTwoSubmitted        = ['Question Title for True and False', 'True text', True]
    questionAnswerThreeSubmitted      = ['Question Title for Reflection Point', '', True]
    
    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizStateSubmitted = {'1':questionAnswerOneSubmitted,'2':questionAnswerTwoSubmitted, '3':questionAnswerThreeSubmitted} 
    
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
            self.entryName       = clsTestService.addGuidToString("Quiz - Player Preview Sanity", self.testNum)
            self.quizEntryName   = clsTestService.addGuidToString("Quiz - Player Preview Sanity - Quiz", self.testNum)
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
            if self.common.kea.quizCreation(self.entryName, self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
            else:
                i = i + 1
                   
            writeToLog("INFO","Step " + str(i) + ": Going to verify the " + self.quizEntryName + " quiz entry when auto play its enabled")
            if self.common.kea.initiateQuizFlow(self.quizEntryName, True, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify the " + self.quizEntryName + " quiz entry when auto play its enabled")
                return
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to verify that the preview screen for " + self.quizEntryName + " quiz entry can be opened")
            if self.common.kea.openKEAPreviewScreen() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that the preview screen for " + self.quizEntryName + " quiz entry can be opened")
                return
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to answer to all the Quiz Questions from the " + self.quizEntryName + " entry")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.KEA_PAGE, timeOut=3, expectedQuizScore='', embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer to all the Quiz Questions from the " + self.quizEntryName + " entry")  
                return  
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to verify that " + self.quizEntryName + " entry submitted screen is properly displayed")  
            if self.common.player.verifySubmittedScreen(str(100), enums.Location.KEA_PAGE, self.questionDict, self.expectedQuizStateSubmitted, 5, embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that " + self.quizEntryName + " entry submitted screen is properly displayed") 
                return  
            else:
                i = i + 1
                   
            writeToLog("INFO","Step " + str(i) + ": Going to verify that the preview screen for " + self.quizEntryName + " quiz entry can be closed")
            if self.common.kea.closeKEAPreviewScreen() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that the preview screen for " + self.quizEntryName + " quiz entry can be closed")
                return
            else:
                i = i + 1           
            ##################################################################
            writeToLog("INFO","TEST PASSED: KEA Editor has been successfully verified for a " + self.typeTest)
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