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
    # Test Name : Quiz - Analytics - Verify quiz questions - Multiple users
    # Test description:
    # Go to editor page and create quiz with option all type of questions -> Login with different users and answer the quiz -> login as quiz owner
    # Go to quiz analytics -> Quiz Questions -> Verify that correct user answer with correct number of right and wrong answer is displayed
    #================================================================================================================================
    testNum = "5117"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    #UserIDs
    userId1 = 'ivq_automation_user_1'
    userId2 = 'ivq_automation_user_2'
    userId3 = 'ivq_automation_user_3'
    userId4 = 'ivq_automation_user_4'
    userId5 = 'ivq_automation_user_5'
    
    userPass = '123456'
    
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text']
    questionNumber3 = ['00:20', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q'] 
    questionNumber4 = ['00:25', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']  
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3,'4':questionNumber4} 
    
    # All questions with users answers
    questionNumber1 = "question #1 Title"
    answerQuestionNumber1User1 = "question #1 option #1"
    answerQuestionNumber1User2 = "question #1 option #1"
    answerQuestionNumber1User3 = "question #1 option #2"
    answerQuestionNumber1User4 = "question #1 option #2"
    answerQuestionNumber1User5 = "question #1 option #1"
    
    questionNumber2 = "Question Title for True and False"
    answerQuestionNumber2User1 = "False text"
    answerQuestionNumber2User2 = "False text"
    answerQuestionNumber2User3 = "False text"
    answerQuestionNumber2User4 = "True text"
    answerQuestionNumber2User5 = "False text"
    
    questionNumber3 = 'Question Title for Open-Q'
    answerQuestionNumber3User1 = 'Answer for Open-Q user number 1'
    answerQuestionNumber3User2 = 'Answer for Open-Q user number 2'
    answerQuestionNumber3User3 = 'Answer for Open-Q user number 3'
    answerQuestionNumber3User4 = 'Answer for Open-Q user number 4'
    answerQuestionNumber3User5 = 'Answer for Open-Q user number 5'
    
    questionNumber4 = 'Question Title for Reflection Point'
    answerQuestionNumber4 = 'Viewed'

    quizQuestionDictUser1 = {questionNumber1:answerQuestionNumber1User1, questionNumber2:answerQuestionNumber2User1, questionNumber3:answerQuestionNumber3User1}
    quizQuestionDictUser2 = {questionNumber1:answerQuestionNumber1User2, questionNumber2:answerQuestionNumber2User2, questionNumber3:answerQuestionNumber3User2}
    quizQuestionDictUser3 = {questionNumber1:answerQuestionNumber1User3, questionNumber2:answerQuestionNumber2User3, questionNumber3:answerQuestionNumber3User3}
    quizQuestionDictUser4 = {questionNumber1:answerQuestionNumber1User4, questionNumber2:answerQuestionNumber2User4, questionNumber3:answerQuestionNumber3User4}
    quizQuestionDictUser5 = {questionNumber1:answerQuestionNumber1User5, questionNumber2:answerQuestionNumber2User5, questionNumber3:answerQuestionNumber3User5}
    
    # All users first question answer data
    firstQuestionUser1Answers = [questionNumber1, answerQuestionNumber1User1, 'QA Member 1', '3', '2', True]
    firstQuestionUser2Answers = [questionNumber1, answerQuestionNumber1User2, 'QA Member 2', '3', '2', True]
    firstQuestionUser3Answers = [questionNumber1, answerQuestionNumber1User3, 'QA Member 3', '3', '2', False]
    firstQuestionUser4Answers = [questionNumber1, answerQuestionNumber1User4, 'QA Member 4', '3', '2', False]
    firstQuestionUser5Answers = [questionNumber1, answerQuestionNumber1User5, 'QA Member 5', '3', '2', True]
   
    # Dictionary with all users first question answers
    firstQuestionAnswersDict = {'1': firstQuestionUser1Answers, '2':firstQuestionUser2Answers, '3':firstQuestionUser3Answers, '4':firstQuestionUser4Answers, '5':firstQuestionUser5Answers}
    
    # All users second question answer data
    secondQuestionUser1Answers = [questionNumber2, answerQuestionNumber2User1, 'QA Member 1', '1', '4', False]
    secondQuestionUser2Answers = [questionNumber2, answerQuestionNumber2User2, 'QA Member 2', '1', '4', False]
    secondQuestionUser3Answers = [questionNumber2, answerQuestionNumber2User3, 'QA Member 3', '1', '4', False]
    secondQuestionUser4Answers = [questionNumber2, answerQuestionNumber2User4, 'QA Member 4', '1', '4', True]
    secondQuestionUser5Answers = [questionNumber2, answerQuestionNumber2User5, 'QA Member 5', '1', '4', False]
   
    # Dictionary with all users second question answers
    secondQuestionAnswersDict = {'1': secondQuestionUser1Answers, '2':secondQuestionUser2Answers, '3':secondQuestionUser3Answers, '4':secondQuestionUser4Answers, '5':secondQuestionUser5Answers}
    
    # All users third question answer data
    thirdQuestionUser1Answers = [questionNumber3, answerQuestionNumber3User1, 'QA Member 1', '5', '0', True]
    thirdQuestionUser2Answers = [questionNumber3, answerQuestionNumber3User2, 'QA Member 2', '5', '0', True]
    thirdQuestionUser3Answers = [questionNumber3, answerQuestionNumber3User3, 'QA Member 3', '5', '0', True]
    thirdQuestionUser4Answers = [questionNumber3, answerQuestionNumber3User4, 'QA Member 4', '5', '0', True]
    thirdQuestionUser5Answers = [questionNumber3, answerQuestionNumber3User5, 'QA Member 5', '5', '0', True]
   
    # Dictionary with all users third question answers
    thirdQuestionAnswersDict = {'1': thirdQuestionUser1Answers, '2':thirdQuestionUser2Answers, '3':thirdQuestionUser3Answers, '4':thirdQuestionUser4Answers, '5':thirdQuestionUser5Answers}
    
    # All users fourth question answer data
    fourthQuestionUser1Answers = [questionNumber4, answerQuestionNumber4, 'QA Member 1', '5', '0', True]
    fourthQuestionUser2Answers = [questionNumber4, answerQuestionNumber4, 'QA Member 2', '5', '0', True]
    fourthQuestionUser3Answers = [questionNumber4, answerQuestionNumber4, 'QA Member 3', '5', '0', True]
    fourthQuestionUser4Answers = [questionNumber4, answerQuestionNumber4, 'QA Member 4', '5', '0', True]
    fourthQuestionUser5Answers = [questionNumber4, answerQuestionNumber4, 'QA Member 5', '5', '0', True]
   
    # Dictionary with all users third question answers
    fourthQuestionAnswersDict = {'1': thirdQuestionUser1Answers, '2':thirdQuestionUser2Answers, '3':thirdQuestionUser3Answers, '4':thirdQuestionUser4Answers}
    
    #List With all the questions and users answers
    answersList = [firstQuestionAnswersDict, secondQuestionAnswersDict, thirdQuestionAnswersDict, fourthQuestionAnswersDict]
    
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
            self.entryName = clsTestService.addGuidToString("Quiz Analytics - Verify answers - Multiple users", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz Analytics - Verify answers - Multiple users - Quiz", self.testNum)      
            self.entryPageURL = ''
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
               
            writeToLog("INFO","Step 6 : Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6 : FAILED to logout as quiz owner")  
                return                 
                      
            writeToLog("INFO","Step 7 : Going to login with " + self.userId1)  
            if self.common.login.loginToKMS(self.userId1, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7 : FAILED to login with " + self.userId1)  
                return            
             
            writeToLog("INFO","Step 8: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 8: FAILED to navigate to entry page link")
                return             
             
            writeToLog("INFO","Step 9 : Going to answer quiz open question")  
            if self.common.player.answerQuiz(self.quizQuestionDictUser1, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9 : FAILED to answer quiz open question")  
                return    
             
            self.common.base.switch_to_default_content()
             
            writeToLog("INFO","Step 10 : Going to logout as " + self.userId1)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10 : FAILED to logout as " + self.userId1)  
                return                 
                      
            writeToLog("INFO","Step 11 : Going to login with " + self.userId2)  
            if self.common.login.loginToKMS(self.userId2, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11 : FAILED to login with " + self.userId2)  
                return            
             
            writeToLog("INFO","Step 12: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 12: FAILED to navigate to entry page link")
                return             
             
            writeToLog("INFO","Step 13 : Going to answer quiz open question")  
            if self.common.player.answerQuiz(self.quizQuestionDictUser2, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13 : FAILED to answer quiz open question")  
                return    
             
            self.common.base.switch_to_default_content()
             
            writeToLog("INFO","Step 14 : Going to logout as " + self.userId2)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14 : FAILED to logout as " + self.userId2)  
                return                 
                      
            writeToLog("INFO","Step 15 : Going to login with " + self.userId3)  
            if self.common.login.loginToKMS(self.userId3, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15 : FAILED to login with " + self.userId3)  
                return            
             
            writeToLog("INFO","Step 16: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 16: FAILED to navigate to entry page link")
                return             
             
            writeToLog("INFO","Step 17 : Going to answer quiz open question")  
            if self.common.player.answerQuiz(self.quizQuestionDictUser3, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17 : FAILED to answer quiz open question")  
                return    
             
            self.common.base.switch_to_default_content()  
             
            writeToLog("INFO","Step 18 : Going to logout as " + self.userId3)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18 : FAILED to logout as " + self.userId3)  
                return                 
                      
            writeToLog("INFO","Step 19 : Going to login with " + self.userId4)  
            if self.common.login.loginToKMS(self.userId4, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19 : FAILED to login with " + self.userId4)  
                return            
             
            writeToLog("INFO","Step 20: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 20: FAILED to navigate to entry page link")
                return             
             
            writeToLog("INFO","Step 21 : Going to answer quiz open question")  
            if self.common.player.answerQuiz(self.quizQuestionDictUser4, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21 : FAILED to answer quiz open question")  
                return    
             
            self.common.base.switch_to_default_content()    
             
            writeToLog("INFO","Step 22 : Going to logout as " + self.userId4)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22 : FAILED to logout as " + self.userId4)  
                return                 
                      
            writeToLog("INFO","Step 23 : Going to login with " + self.userId5)  
            if self.common.login.loginToKMS(self.userId5, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23 : FAILED to login with " + self.userId5)  
                return            
             
            writeToLog("INFO","Step 24: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 24: FAILED to navigate to entry page link")
                return             
             
            writeToLog("INFO","Step 25 : Going to answer quiz open question")  
            if self.common.player.answerQuiz(self.quizQuestionDictUser5, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25 : FAILED to answer quiz open question")  
                return    
             
            self.common.base.switch_to_default_content()   
             
            writeToLog("INFO","Step 26 : Going to logout as " + self.userId5)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26 : FAILED to logout as " + self.userId5)  
                return                 
                      
            writeToLog("INFO","Step 27 : Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27 : FAILED to login as quiz owner")  
                return                         
            
            writeToLog("INFO","Step 28 : Going to verify quiz answers in quiz analytics")  
            if self.common.quizAnalytics.verifyQuizAnswersInAnalytics(self.answersList, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28 : FAILED to verify quiz answers in quiz analytics")  
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