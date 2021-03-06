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
from time import strftime

class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # Test Name : Quiz - Analytics - Open-Q feedback
    # Test description:
    # Go to editor page and create quiz with open-Q only
    # Go to quiz page and answer open-Q -> Go to Quiz Analytics -> Go to Quiz Question tab -> Add feedback to open-Q -> 
    # Edit feedback -> Delete feedback
    #================================================================================================================================
    testNum = "5111"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    questionOpen = ['00:25', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q']
    
    # This Dictionary is used in order to create all the Quiz Question types within a single call
    questionDict = {'1':questionOpen} 
    
    questionName1 = 'Question Title for Open-Q'
    answerText1   = 'Answer for Open-Q'
    
    # This dictionary contains all the questions and answers
    quizQuestionDict = {questionName1:answerText1}
    
    questionAnswerOneSubmitted = ['Question Title for Open-Q', 'Answer for Open-Q', True]

    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizStateSubmitted = {'1':questionAnswerOneSubmitted} 
    

    feedbackText = 'Good answer'   
    newFeedbackText = 'Not good enough'  
    feedbackOwner = 'QA ADMIN'
    feedbackDate =  datetime.datetime.now().strftime("%m/%d/%Y")
    
    openQuestionFeedbackToAdd = [questionName1, feedbackText, feedbackOwner, feedbackDate] 
    
    openQuestionFeedbackToEdit = [questionName1, feedbackText, newFeedbackText, feedbackOwner, feedbackDate]
    
    openQuestionFeedbackToDelete = [questionName1, newFeedbackText, feedbackOwner, feedbackDate]
    
    # This dictionary contains all the questions that need to be added
    addedFeedbackList = {'1':openQuestionFeedbackToAdd}
    
    # This dictionary contains all the questions that need to be edited
    editedFeedbackList = {'1':openQuestionFeedbackToEdit}
    
    deletedFeedbackList = {'1':openQuestionFeedbackToDelete}
    
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
            self.entryName = clsTestService.addGuidToString("IVQ - Open-Q - Feedback", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("IVQ - Open-Q - Feedback - Quiz", self.testNum)       
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
            if self.common.kea.quizCreation(self.entryName, self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4 : FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return
                
            writeToLog("INFO","Step 5 : Going to answer quiz open question")  
            if self.common.player.answerQuiz(self.quizQuestionDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='100') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5 : FAILED to answer quiz open question")  
                return  
              
            self.common.base.switch_to_default_content()
             
            writeToLog("INFO","Step 6 : Going to add feedback to the quiz open-Q")  
            if self.common.quizAnalytics.addFeedbackToOpenQuestion(self.addedFeedbackList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6 : FAILED to add feedback to the quiz open-Q")  
                return    
             
            writeToLog("INFO","Step 7 : Going to edit feedback to the quiz open-Q")  
            if self.common.quizAnalytics.editOpenQuestionFeedback(self.editedFeedbackList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7 : FAILED to edit feedback to the quiz open-Q")  
                return 

            writeToLog("INFO","Step 8 : Going to delete feedback to the quiz open-Q")  
            if self.common.quizAnalytics.deleteOpenQuestionFeedback(self.deletedFeedbackList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8 : FAILED to delete feedback to the quiz open-Q")  
                return                                                                        
               
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Open-Q is added sucssefully")
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