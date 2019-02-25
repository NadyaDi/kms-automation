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
    # Test Name : Quiz - Submitting Quiz with Answer order changed - Entry Page
    # Test description:
    # Verify that the user is able to change the Quiz Question type's answer order
    # Verify that the user is able to submit a Quiz Question
    # Verify that the answer order changes is reflected in the Entry Page and the right expected quiz score is displayed
    #================================================================================================================================
    testNum = "4855"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    typeTest = 'Quiz Entry with three quiz question that contain a different answer order'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
        
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']
    
    # This list is used in order to change the answer order using drag and drop
    # index 0 = question title that must be found while hovering over the quiz question bubble
    # index 1 = question answer that we want to move to a different location
    # index 2 = question location where we want to move index 1
    answerOrderTwo        = ['question #2 Title', 1, 2]   
    answerOrderThree      = ['question #3 Title', 1, 4]
    
    # This list is used in order to verify that the answer options are displayed in the desired order
    answerListOrderTwo    = ['question #2 option #2', 'question #2 option #1', 'question #2 option #3', 'question #2 option #4']   
    answerListOrderThree  = ['question #3 option #2', 'question #3 option #3', 'question #3 option #4', 'question #3 option #1']   
    
    # This dictionary is used in order to create the quiz questions
    dictQuestions         = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3}
    
    # This dictionary is used in order to change the answer list order
    changeAnswerOrderDict = {'2':answerOrderTwo, '3':answerOrderThree} 
    
    # This dictionary is used in order to verify the answer list order
    expectedAnswerListDict = {'2':answerListOrderTwo, '3':answerListOrderThree}

    # Each list is used in order to verify that all the Quiz Question types were answered
    questionAnswerOne        = ['question #1 Title', 'question #1 option #1', True]
    questionAnswerTwo        = ['question #2 Title', 'question #2 option #1', True]
    questionAnswerThree      = ['question #3 Title', 'question #3 option #4', False]
    
    # This variables are used in order to find and answer to the quiz questions
    questionName1            = "question #1 Title"
    answerText1              = "question #1 option #1"
    
    questionName2            = "question #2 Title"
    answerText2              = "question #2 option #1"
    
    questionName3            = "question #3 Title"
    answerText3              = "question #3 option #4"
        
    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be present in the Question Name
    answersDict = {questionName1:answerText1,
                   questionName2:answerText2,
                   questionName3:answerText3
                   } 
    
    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizSubmittedScreenResults     = {'1':questionAnswerOne,'2':questionAnswerTwo, '3':questionAnswerThree} 
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
            self.entryName           = clsTestService.addGuidToString("Quiz - Submitting with Changed Answer Order in Entry Page", self.testNum)
            self.entryNameQuiz       = clsTestService.addGuidToString("Quiz - Submitting with Changed Answer Order in Entry Page - Quiz", self.testNum)
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
            writeToLog("INFO","Step 3: Going to navigate to " + self.entryNameQuiz + " entry editor")  
            if self.common.kea.launchKEA(self.entryNameQuiz, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to " + self.entryNameQuiz + " entry editor") 
                return
               
            writeToLog("INFO","Step 4: Going to change the answer order for " + self.entryNameQuiz + " entry")  
            if self.common.kea.changeAnswerOrder(self.changeAnswerOrderDict, self.expectedAnswerListDict)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to change the answer order for " + self.entryNameQuiz + " entry")
                return
             
            writeToLog("INFO","Step 5: Going to navigate to " + self.entryNameQuiz + " Entry page")  
            if self.common.kea.navigateToEntryPageFromKEA(self.entryNameQuiz) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to " + self.entryNameQuiz + " Entry page")  
                return         
                     
            writeToLog("INFO","Step 6: Going to answer to all the Quiz Questions from the " + self.entryNameQuiz + " entry")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to answer to all the Quiz Questions from the " + self.entryNameQuiz + " entry")  
                return             
                  
            writeToLog("INFO","Step 7: Going to resume from the beginning the " + self.entryNameQuiz + " entry")  
            if self.common.player.resumeFromBeginningQuiz(enums.Location.ENTRY_PAGE, timeOut=1, forceResume=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to resume from the beginning the " + self.entryNameQuiz + " entry")
                return  
             
            writeToLog("INFO","Step 8: Going to verify that all the available quiz questions from the " + self.entryNameQuiz + " entry remained answered and the Expected Score is displayed in the Submitted screen")  
            if self.common.player.quizVerification(self.dictQuestions, self.expectedQuizSubmittedScreenResults, submittedQuiz=True, resumeQuiz=False, newQuiz=False, expectedQuizScore=str(67), location=enums.Location.ENTRY_PAGE, timeOut=60) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify that all the available quiz questions from the " + self.entryNameQuiz + " entry remained answered and the Expected Score is displayed in the Submitted screen")  
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