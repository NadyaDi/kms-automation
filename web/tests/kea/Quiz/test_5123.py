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
    # Test Name : Quiz - Analytics - Allow specific user retake when retake option is disabled
    # Test description:
    # Go to editor page and create quiz with all type of questions -> Login with different user and answer the quiz - > Login as admin
    # Go to analytics page -> quiz uswrs tab -> delete user's attempts -> login with the user and verify that he is able to take the quiz again
    #================================================================================================================================
    testNum = "5123"
    
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

    quizQuestionDictAttempt1 = {questionNumber1Attempt1:answerquestionNumber1Attempt1, questionNumber2Attempt1:answerquestionNumber2Attempt1, questionNumber3Attempt1:answerquestionNumber3Attempt1}
    
    quizQuestionsDictAllAttempts = [quizQuestionDictAttempt1]
    
    # Score for the attempt
    generalScoreAttempt1 = '100'
    
    quizGeneralAttemptsScore = [generalScoreAttempt1]

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
            self.entryName = clsTestService.addGuidToString("Quiz - Delete user attempt", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz - Delete user attempt - Quiz", self.testNum)      
            self.entryPageURL = None
            self.loginUsername = "ivq_automation_user_1"
            self.userPass = '123456'
            self.userName = 'QA Member 1'
            self.numberOfAttempts = '1/1'
            self.score = '100%'
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
     
            self.common.base.switch_to_default_content()
                
            writeToLog("INFO","Step 5: Going to get entry page URL")
            self.entryPageURL = self.common.base.driver.current_url
                
            writeToLog("INFO","Step 6: Going to publish entry to unlisted")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate(self.quizEntryName, enums.ChannelPrivacyType.UNLISTED, publishFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 6: FAILED failed to publish entry to unlisted")
                return 
                
            writeToLog("INFO","Step 7 : Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7 : FAILED to logout as quiz owner")  
                return 
                
            writeToLog("INFO","Step 8 : Going to login as " + self.userName)  
            if self.common.login.loginToKMS(self.loginUsername, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8 : FAILED to login as " + self.userName)  
                return       
                
            writeToLog("INFO","Step 9: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 9: FAILED to navigate to entry page link")
                return             
                 
            writeToLog("INFO","Step 10 : Going to answer quiz")  
            if self.common.player.answerQuiz(self.quizQuestionDictAttempt1, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10 : FAILED to answer quiz")  
                return    
                 
            self.common.base.switch_to_default_content()
                 
            writeToLog("INFO","Step 11 : Going to logout as " + self.userName)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11 : FAILED to logout as " + self.userName)  
                return  
                
            writeToLog("INFO","Step 12 : Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12 : FAILED to login as quiz owner")  
                return                                                        
               
            writeToLog("INFO","Step 13 : Going to delete quiz attempt") 
            if self.common.quizAnalytics.deleteUserAttempts(self.loginUsername, enums.quizAnlyticsDeleteOption.REMOVE_LAST_ATTEMPT, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13 : FAILED: to delete quiz attempt")
                return
              
            writeToLog("INFO","Step 14 : Going to verify message after deletion") 
            if self.common.quizAnalytics.verifyRemovedAttemptMessage() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14 : FAILED: to verify message after deletion")
                return            
  
            writeToLog("INFO","Step 15 : Going to verify that attempts and score aren't displayed") 
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername, self.userName, self.numberOfAttempts, self.score, enums.playerQuizScoreType.LATEST) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 15 : FAILED to verify that attempts and score aren't displayed")
                return
              
            writeToLog("INFO","Step 15 failed as expected")
             
            writeToLog("INFO","Step 16 : Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16 : FAILED to logout as quiz owner")  
                return 
               
            writeToLog("INFO","Step 17 : Going to login as " + self.userName)  
            if self.common.login.loginToKMS(self.loginUsername, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17 : FAILED to login as " + self.userName)  
                return       
               
            writeToLog("INFO","Step 18: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 18: FAILED to navigate to entry page link")
                return             
                
            writeToLog("INFO","Step 19 : Going to verify that user is able to answer quiz again")  
            if self.common.player.answerQuiz(self.quizQuestionDictAttempt1, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19 : FAILED to verify that user is able to answer quiz again")  
                return   
             
            self.common.base.switch_to_default_content()
            
            writeToLog("INFO","Step 20 : Going to logout as " + self.loginUsername)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20 : FAILED to logout as as " + self.loginUsername)  
                return 
              
            writeToLog("INFO","Step 21 : Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21 : FAILED to login as quiz owner")  
                return  
            
            writeToLog("INFO","Step 22 : Going to verify that user attempt data is displayed in quiz analytics") 
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername, self.userName, self.numberOfAttempts, self.score, enums.playerQuizScoreType.LATEST, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22 : FAILED to verify that user attempt data is displayed in quiz analytics")
                return            

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Delete user attempts was done successfully")
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