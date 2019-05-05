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
    # Test Name : Quiz - Analytics - Export quiz questions - after clearing all attempts
    # Test description:
    # Go to editor page and create quiz with all type of questions with option to retake -> Login user answer the quiz (2 attempts) - > Login as admin
    # Go to analytics page -> quiz users tab -> Clear all user attempts -> Go to quiz question tab and export csv -> Take the quiz again -> Login as admin and navigate to analytics page =? quiz questions tab -> Export csv
    #================================================================================================================================
    testNum = "5163"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathEntry = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'

    filePathQuizQuestionsAfterClearingAttempts = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\templates\quiz_questions_after_clearing_attempt_5163.csv'
    filePathExoprtedQuizQuestionsAfterClearingAttempts = localSettings.LOCAL_SETTINGS_JENKINS_NODE_MEDIA_PATH + '/quiz_questions.csv'
    
#    Next line is for local running     
#    filePathExoprtedQuizQuestionsAfterClearingAttempts = 'C:\\Users\\inbar.willman\\eclipse-workspace\\kms-automation\\web\\temp\\downloads\\quiz_questions.csv'
    
    filePathQuizQuestionsAfterRetakingQuiz = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\templates\quiz_questions_after_retaking_quiz_5163.csv'
    filePathExoprtedQuizQuestionsAfterRetakingQuiz = localSettings.LOCAL_SETTINGS_JENKINS_NODE_MEDIA_PATH + '/quiz_questions(1).csv'
    
#    Next line is for local running     
#    filePathExoprtedQuizQuestionsAfterRetakingQuiz = 'C:\\Users\\inbar.willman\\eclipse-workspace\\kms-automation\\web\\temp\\downloads\\quiz_questions(1).csv'
    
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text']
    questionNumber3 = ['00:20', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q'] 
    questionNumber4 = ['00:25', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']  
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3,'4':questionNumber4} 
    
    #UserIDs
    userId1 = 'ivq_automation_user_1'
    userNameUser1 = 'QA Member 1'  
    userPass = '123456'  
    
    # Questions title
    quizQuestionNumber1 = "question #1 Title"
    quizQuestionNumber2 = "Question Title for True and False"
    quizQuestionNumber3 = "Question Title for Open-Q"
    quizQuestionNumber4 = "Question Title for Reflection Point"
    
    # User 1 attempt 1
    answerquestionNumber1Attempt1User1 = "question #1 option #1"
    answerquestionNumber2Attempt1User1 = "True text"
    answerquestionNumber3Attempt1User1 = "Open-Q answer QA_Member_1 attempt 1"
    
    # User 1 attempt 2
    answerquestionNumber1Attempt2User1 = "question #1 option #2"
    answerquestionNumber2Attempt2User1 = "True text"
    answerquestionNumber3Attempt2User1 = "Open-Q answer QA_Member_1 attempt 2"
    
    # User 1 attempt 3
    answerquestionNumber1Attempt3User1 = "question #1 option #3"
    answerquestionNumber2Attempt3User1 = "False text"
    answerquestionNumber3Attempt3User1 = "Open-Q answer QA_Member_1 attempt 3"
    
    # User 1 answers for 2 attempts
    quizAnswersDictAttempt1User1 = {quizQuestionNumber1:answerquestionNumber1Attempt1User1, quizQuestionNumber2:answerquestionNumber2Attempt1User1, quizQuestionNumber3:answerquestionNumber3Attempt1User1}
    quizAnswersDictAttempt2User1 = {quizQuestionNumber1:answerquestionNumber1Attempt2User1, quizQuestionNumber2:answerquestionNumber2Attempt2User1, quizQuestionNumber3:answerquestionNumber3Attempt2User1}
    quizAnswersDictAttempt3User1 = {quizQuestionNumber1:answerquestionNumber1Attempt3User1, quizQuestionNumber2:answerquestionNumber2Attempt3User1, quizQuestionNumber3:answerquestionNumber3Attempt3User1}
    quizAnswersDictAllAttemptsUser1 = [quizAnswersDictAttempt1User1, quizAnswersDictAttempt2User1]
    
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
            self.entryName = clsTestService.addGuidToString("Quiz - Analytics - Export quiz questions - Clear all attempts", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz - Analytics - Export quiz questions - Clear all attempts - Quiz", self.testNum)      
            self.keaScoreType                    = {enums.KEAQuizOptions.QUIZ_SCORE_TYPE:enums.keaQuizScoreType.LATEST.value}
            self.keaNumberOfAllowedAttempts      = {enums.KEAQuizOptions.SET_NUMBER_OF_ATTEMPTS:3}
            self.keaAllowMultipleScore           = {enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:True}            
            self.keaScoreOptions                 = [self.keaAllowMultipleScore, self.keaNumberOfAllowedAttempts, self.keaScoreType]           
            self.keaAllScoreOptionsList          = [self.keaScoreOptions]                  
            self.totalGivenAttempts              = 3             
            self.entryPageURL                    = None

            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePathEntry, self.entryName, self.description, self.tags) == False:
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
               
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + ": Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as quiz owner")  
                return 
              
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to login as " + self.userNameUser1)  
            if self.common.login.loginToKMS(self.userId1, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as " + self.userNameUser1)  
                return       
              
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to entry page link")
                return             
              
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz as " + self.userNameUser1)  
            if self.common.player.verifyQuizAttempts(self.quizAnswersDictAllAttemptsUser1, totalGivenAttempts=self.totalGivenAttempts, scoreType=enums.playerQuizScoreType.LATEST, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer quiz as " + self.userNameUser1)  
                return    
                     
            self.common.base.switch_to_default_content()
              
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userNameUser1)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userNameUser1)  
                return  
              
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + " : Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to login as quiz owner")  
                return 
              
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to clear all attempts for " + self.userNameUser1) 
            if self.common.quizAnalytics.deleteUserAttempts(self.userId1, enums.quizAnlyticsDeleteOption.CLEAR_ALL_ATTEMPTS, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to clear all attempts for " + self.userNameUser1)
                return 
             
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to clear cache") 
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to clear cache")
                return  
             
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to KMS site")  
            if self.common.login.navigateToLoginPage() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to KMS site")  
                return                                                   
             
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + " : Going to export question csv file")  
            if self.common.quizAnalytics.exportCsvFileQuizAnalyticsPage(enums.quizAnalytics.QUIZ_QUESTIONS, self.quizEntryName, True)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to export question csv file")  
                return
             
            sleep(10)
           
            i = i + 1 
            writeToLog("INFO","Step " + str(i) + " : Going to verify that quiz questions csv files is download correctly")  
            if self.common.compareBetweenTwoCsvFiles(self.filePathExoprtedQuizQuestionsAfterClearingAttempts, self.filePathQuizQuestionsAfterClearingAttempts)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to verify that quiz questions csv files is download correctly")  
                return   
             
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + ": Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as quiz owner")  
                return 
              
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to login as " + self.userNameUser1)  
            if self.common.login.loginToKMS(self.userId1, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as " + self.userNameUser1)  
                return       
              
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to entry page link")
                return             
              
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz as " + self.userNameUser1)  
            if self.common.player.answerQuiz(self.quizAnswersDictAttempt3User1, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer quiz as " + self.userNameUser1)  
                return    
                     
            self.common.base.switch_to_default_content()
              
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userNameUser1)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userNameUser1)  
                return  
              
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to clear cache") 
            if self.common.admin.clearCache() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to clear cache")
                return                                                    
 
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + " : Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to login as quiz owner")  
                return 
            
            i = i + 1  
            writeToLog("INFO","Step " + str(i) + " : Going to export question csv file")  
            if self.common.quizAnalytics.exportCsvFileQuizAnalyticsPage(enums.quizAnalytics.QUIZ_QUESTIONS, self.quizEntryName, True)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to export question csv file")  
                return
            
            sleep(10)
            
            i = i + 1 
            writeToLog("INFO","Step " + str(i) + " : Going to verify that quiz questions csv files is download correctly")  
            if self.common.compareBetweenTwoCsvFiles(self.filePathExoprtedQuizQuestionsAfterRetakingQuiz, self.filePathQuizQuestionsAfterRetakingQuiz)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + " : FAILED to verify that quiz questions csv files is download correctly")  
                return                                                                                                         

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Verify exoperted CSV after clearing all attempts successfully")
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