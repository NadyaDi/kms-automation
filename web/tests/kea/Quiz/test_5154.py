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
    # Test Name : Quiz - Analytics - Verify quiz questions after removing last attempt 
    # Test description:
    # Go to editor page and create quiz with option to retake quiz - 3 attempts and all type of questions
    # Go to quiz page with different user and answer quiz -> Login with quiz owner -> Quiz analytics page -> remove last attempt for specific user-> Go to quiz question tab-> Verify that correct answers of the previous attempt are displayed -> 
    #================================================================================================================================
    testNum = "5154"
    
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
    
    #User data
    userId = 'ivq_automation_user_1'
    userNameUser = 'QA Member 1' 
    userPass = '123456'  
    
    # Questions title
    quizQuestionNumber1 = "question #1 Title"
    quizQuestionNumber2 = "Question Title for True and False"
    quizQuestionNumber3 = "Question Title for Open-Q"
    quizQuestionNumber4 = "Question Title for Reflection Point"
     
    # Answers for first attempt
    answerQuestionNumber1Attempt1 = "question #1 option #1"
    answerQuestionNumber2Attempt1 = "True text"
    answerQuestionNumber3Attempt1 = "Open-Q answer QA_Member_1 attempt 1"
    
    # Answers for second attempt
    answerQuestionNumber1Attempt2 = "question #1 option #2"
    answerQuestionNumber2Attempt2 = "False text"
    answerQuestionNumber3Attempt2 = "Open-Q answer QA_Member_1 attempt 2"
    
    answerQuestionNumber4 = 'Viewed'
    
    # User first attempt
    questionAnswersDictAttempt1 = {quizQuestionNumber1:answerQuestionNumber1Attempt1, quizQuestionNumber2:answerQuestionNumber2Attempt1, quizQuestionNumber3:answerQuestionNumber3Attempt1}
    # User second attempt
    questionAnswersDictAttempt2 = {quizQuestionNumber1:answerQuestionNumber1Attempt2, quizQuestionNumber2:answerQuestionNumber2Attempt2, quizQuestionNumber3:answerQuestionNumber3Attempt2}
    
    questionAnswersAllAttempts = [questionAnswersDictAttempt1, questionAnswersDictAttempt2]

    # Users answers - First attempt
    firstQuestionAnswersAttempt1 = [quizQuestionNumber1, answerQuestionNumber1Attempt1, 'QA Member 1', '1', '0', True]
    secondQuestionAnswersAttempt1 = [quizQuestionNumber2, answerQuestionNumber2Attempt1, 'QA Member 1', '1', '0', True]
    thirdQuestionAnswersAttempt1 = [quizQuestionNumber3, answerQuestionNumber3Attempt1, 'QA Member 1', '1', '0', True]
    FourthQuestionAnswersAttempt1 = [quizQuestionNumber4, answerQuestionNumber4, 'QA Member 1', '1', '0', True]

    firstQuestionUsersAnswersAttempt1 = {'1': firstQuestionAnswersAttempt1}
    secondQuestionAnswersAttempt1 = {'1': secondQuestionAnswersAttempt1}
    thirdQuestionAnswersAttempt1 = {'1': thirdQuestionAnswersAttempt1}
    FourthQuestionAnswersAttempt1 = {'1': FourthQuestionAnswersAttempt1}
    
    answerListAttempt1 = [firstQuestionUsersAnswersAttempt1, secondQuestionAnswersAttempt1, thirdQuestionAnswersAttempt1, FourthQuestionAnswersAttempt1]
    
    # Users answers - Second attempt
    firstQuestionAnswersAttempt2 = [quizQuestionNumber1, answerQuestionNumber1Attempt2, 'QA Member 1', '0', '1', False]
    secondQuestionAnswersAttempt2 = [quizQuestionNumber2, answerQuestionNumber2Attempt2, 'QA Member 1', '0', '1', False]
    thirdQuestionAnswersAttempt2 = [quizQuestionNumber3, answerQuestionNumber3Attempt2, 'QA Member 1', '1', '0', True]
    FourthQuestionAnswersAttempt2 = [quizQuestionNumber4, answerQuestionNumber4, 'QA Member 1', '1', '0', True]

    firstQuestionUsersAnswersAttempt2 = {'1': firstQuestionAnswersAttempt2}
    secondQuestionAnswersAttempt2 = {'1': secondQuestionAnswersAttempt2}
    thirdQuestionAnswersAttempt2 = {'1': thirdQuestionAnswersAttempt2}
    FourthQuestionAnswersAttempt2 = {'1': FourthQuestionAnswersAttempt2}
    
    answerListAttempt2 = [firstQuestionUsersAnswersAttempt2, secondQuestionAnswersAttempt2, thirdQuestionAnswersAttempt2, FourthQuestionAnswersAttempt2]    

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
            self.entryName = clsTestService.addGuidToString("Quiz - Verify quiz questions after removing last attempt", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz - Verify quiz questions after removing last attempt - Quiz", self.testNum)      
            self.keaScoreType                    = {enums.KEAQuizOptions.QUIZ_SCORE_TYPE:enums.keaQuizScoreType.LATEST.value}
            self.keaNumberOfAllowedAttempts      = {enums.KEAQuizOptions.SET_NUMBER_OF_ATTEMPTS:3}
            self.keaAllowMultipleScore           = {enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:True}            
            self.keaScoreOptions                 = [self.keaAllowMultipleScore, self.keaNumberOfAllowedAttempts, self.keaScoreType]           
            self.keaAllScoreOptionsList          = [self.keaScoreOptions]                  
            self.totalGivenAttempts              = 3             
            self.entryPageURL                    = None
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
                          
            writeToLog("INFO","Step 7: Going to navigate to KEA Quiz tab for " + self.quizEntryName)  
            if self.common.kea.initiateQuizFlow(self.quizEntryName, True, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to KEA Quiz tab for " + self.quizEntryName)  
                return 
                          
            i = 8
                          
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
            
            writeToLog("INFO","Step " + str(i) + ": Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as quiz owner")  
                return 
                  
            i = i + 1           
            writeToLog("INFO","Step " + str(i) + ": Going to login as " + self.userNameUser)  
            if self.common.login.loginToKMS(self.userId, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as " + self.userNameUser)  
                return 
                         
            i = i + 1            
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to entry page link")
                return             
                    
            i = i + 1         
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.questionAnswersAllAttempts, totalGivenAttempts=3, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return    
                   
            i = i + 1    
            self.common.base.switch_to_default_content()
               
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userNameUser)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userNameUser)  
                return  
             
            i = i + 1 
            writeToLog("INFO","Step " + str(i) + ": Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as quiz owner")  
                return 

            i = i + 1  
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz questions in quiz analytics before removing last attempt")    
            if self.common.quizAnalytics.verifyQuizAnswersInAnalytics(self.answerListAttempt2, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to verify quiz questions in quiz analytics before removing last attempt")  
                return  
            
            i = i + 1
            writeToLog("INFO","Step " + str(i) + ": Going to click on quiz users tab")    
            if self.common.base.click(self.common.quizAnalytics.QUIZ_ANALYTICS_QUIZ_USERS_TAB) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to click on quiz users tab")  
                return                 
            
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + ": Going to remove user last attempt")  
            if self.common.quizAnalytics.deleteUserAttempts(self.userId, enums.quizAnlyticsDeleteOption.REMOVE_LAST_ATTEMPT) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to remove user last attempt")  
                return  
            
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to clear cache") 
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to clear cache")
                return  
             
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to KMS site")  
            if self.common.login.navigateToLoginPage(verifyUrl=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to KMS site")  
                return             
            
#             i = i + 1
#             writeToLog("INFO","Step " + str(i) + ": Going to click on quiz questions tab")    
#             if self.common.base.click(self.common.quizAnalytics.QUIZ_ANALYTICS_QUIZ_QUESTIONS_TAB) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step " + str(i) + " : FAILED to click on quiz questions tab")  
#                 return             
            
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz questions in quiz analytics after removing last attempt")    
            if self.common.quizAnalytics.verifyQuizAnswersInAnalytics(self.answerListAttempt1, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to verify quiz questions in quiz analytics after removing last attempt")  
                return                                               
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Verify user questions in quiz questions tab after removing last attempt was done successfully")
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