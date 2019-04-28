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
    # Test Name : Quiz - Analytics - Remove last attempt when more than one user answer the quiz
    # Test description:
    # Go to editor page and create quiz with option to retake quiz - 3 attempts and all type of questions
    # Go to quiz page with different users and answer quiz -> Login with quiz owner -> Quiz analytics page -> Clear all attempts for specific user -> 
    # Verify that user last attempt was removed  and other users row are still displayed
    #================================================================================================================================
    testNum = "5137"
    
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
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']   
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3} 
    
    #UserIDs
    userId1 = 'ivq_automation_user_1'
    userId2 = 'ivq_automation_user_2'
    userId3 = 'ivq_automation_user_3'
    
    userNameUser1 = 'QA Member 1'
    userNameUser2 = 'QA Member 2'
    userNameUser3 = 'QA Member 3'
    
    userPass = '123456'  
    
    # Questions title
    quizQuestionNumber1 = "question #1 Title"
    quizQuestionNumber2 = "question #2 Title"
    quizQuestionNumber3 = "question #3 Title"
     
    # User 1 attempt 1
    answerquestionNumber1Attempt1User1 = "question #1 option #1"
    answerquestionNumber2Attempt1User1 = "question #2 option #1"
    answerquestionNumber3Attempt1User1 = "question #3 option #1"
    
    # User 1 attempt 2
    answerquestionNumber1Attempt2User1 = "question #1 option #1"
    answerquestionNumber2Attempt2User1 = "question #2 option #2"
    answerquestionNumber3Attempt2User1 = "question #3 option #2"
    
    # User 2 attempt 1
    answerquestionNumber1Attempt1User2 = "question #1 option #1"
    answerquestionNumber2Attempt1User2 = "question #2 option #2"
    answerquestionNumber3Attempt1User2 = "question #3 option #1"
    
    # User 3 attempt 1
    answerquestionNumber1Attempt1User3 = "question #1 option #1"
    answerquestionNumber2Attempt1User3 = "question #2 option #2"
    answerquestionNumber3Attempt1User3 = "question #3 option #1"
    
    # User 3 attempt 2
    answerquestionNumber1Attempt2User3 = "question #1 option #1"
    answerquestionNumber2Attempt2User3 = "question #2 option #2"
    answerquestionNumber3Attempt2User3 = "question #3 option #2"
    
    # User 3 attempt 3
    answerquestionNumber1Attempt3User3 = "question #1 option #1"
    answerquestionNumber2Attempt3User3 = "question #2 option #1"
    answerquestionNumber3Attempt3User3 = "question #3 option #1"
    
    # User 1 answers for 2 attempts
    quizAnswersDictAttempt1User1 = {quizQuestionNumber1:answerquestionNumber1Attempt1User1, quizQuestionNumber2:answerquestionNumber2Attempt1User1, quizQuestionNumber3:answerquestionNumber3Attempt1User1}
    quizAnswersDictAttempt2User1 = {quizQuestionNumber1:answerquestionNumber1Attempt2User1, quizQuestionNumber2:answerquestionNumber2Attempt2User1, quizQuestionNumber3:answerquestionNumber3Attempt2User1}
    quizAnswersDictAllAttemptsUser1 = [quizAnswersDictAttempt1User1, quizAnswersDictAttempt2User1]
    
    # User 2 answers for 1 attempt
    quizAnswersDictAttempt1User2 = {quizQuestionNumber1:answerquestionNumber1Attempt1User2, quizQuestionNumber2:answerquestionNumber2Attempt1User2, questionNumber3:answerquestionNumber3Attempt1User2}
    quizAnswersDictAllAttemptsUser2 = [quizAnswersDictAttempt1User2]
    
    # User 3 answers for 3 attempts
    quizAnswersDictAttempt1User3 = {questionNumber1:answerquestionNumber1Attempt1User3, questionNumber2:answerquestionNumber2Attempt1User3, questionNumber3:answerquestionNumber3Attempt1User3}
    quizAnswersDictAttempt2User3 = {questionNumber1:answerquestionNumber1Attempt2User3, questionNumber2:answerquestionNumber2Attempt2User3, questionNumber3:answerquestionNumber3Attempt2User3}
    quizAnswersDictAttempt3User3 = {questionNumber1:answerquestionNumber1Attempt3User3, questionNumber2:answerquestionNumber2Attempt3User3, questionNumber3:answerquestionNumber3Attempt3User3}
    quizAnswersDictAllAttemptsUser3 = [quizAnswersDictAttempt1User3, quizAnswersDictAttempt2User3, quizAnswersDictAttempt3User3] 
    
    # List with question title and user answer
    firstQuestionList = [questionNumber1,answerquestionNumber1Attempt1User1, True]
    secondQuestionList = [questionNumber2, answerquestionNumber2Attempt1User1, False]
    thirdQuestionList = [questionNumber3, answerquestionNumber3Attempt1User1, True]
    
    questionAndAnswerDict = {'1':firstQuestionList, '2':secondQuestionList, '3':thirdQuestionList}
    
    # User 1 score and number of attempts in quiz users tab
    numberOfAttemptsUser1 = '2/3'
    scoreUser1 = '33%'   
    
    # User 2 score and number of attempts in quiz users tab        
    numberOfAttemptsUser2 = '1/3'
    scoreUser2 = '67%'  
    
    # User 3 score and number of attempts in quiz users tab
    numberOfAttemptsUser3 = '3/3'
    scoreUser3 = '100%'   
    
    numberOfAttemptsUser3AfterRemovingLastAttempt = '2/3'
    scoreUser3AfterRemovingLastAttempt = '33%'
    
    user1DataInAnalytics = [userId1, userNameUser1, numberOfAttemptsUser1, scoreUser1]
    user2DataInAnalytics = [userId2, userNameUser2, numberOfAttemptsUser2, scoreUser2]
    user3DataInAnalytics = [userId3, userNameUser3, numberOfAttemptsUser3, scoreUser3]
    user3DataInAnalyticsAfterDeletion = [userId3, userNameUser3 + "   Last Attempt removed", numberOfAttemptsUser3AfterRemovingLastAttempt, scoreUser3AfterRemovingLastAttempt]
    allUsersDataInAnalytics = {'1':user1DataInAnalytics, '2':user2DataInAnalytics, '3':user3DataInAnalytics}
    usersDataInAnalyticsAfterDeletion = {'1':user1DataInAnalytics, '2':user2DataInAnalytics, '3':user3DataInAnalyticsAfterDeletion}
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
            self.entryName = clsTestService.addGuidToString("Quiz - Remove last attempt - more than one user in analytics", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz - Remove last attempt - more than one user in analytics - Quiz", self.testNum)      
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
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.quizAnswersDictAllAttemptsUser1, totalGivenAttempts=self.totalGivenAttempts, scoreType=enums.playerQuizScoreType.LATEST, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return    
                  
            i = i + 1    
            self.common.base.switch_to_default_content()
              
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userNameUser1)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userNameUser1)  
                return  
                 
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to login as " + self.userNameUser2)  
            if self.common.login.loginToKMS(self.userId2, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as " + self.userNameUser2)  
                return 
              
            i = i + 1            
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to entry page link")
                return             
                   
            i = i + 1         
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.quizAnswersDictAllAttemptsUser2, totalGivenAttempts=self.totalGivenAttempts, scoreType=enums.playerQuizScoreType.LATEST, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return    
                  
            i = i + 1    
            self.common.base.switch_to_default_content()
              
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userNameUser2)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userNameUser2)  
                return    
              
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to login as " + self.userNameUser3)  
            if self.common.login.loginToKMS(self.userId3, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as " + self.userNameUser3)  
                return 
              
            i = i + 1            
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to entry page link")
                return             
                   
            i = i + 1         
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.quizAnswersDictAllAttemptsUser3, totalGivenAttempts=self.totalGivenAttempts, scoreType=enums.playerQuizScoreType.LATEST, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return    
                 
            i = i + 1    
            self.common.base.switch_to_default_content()
             
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userNameUser3)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userNameUser3)  
                return     
             
            i = i + 1 
            writeToLog("INFO","Step " + str(i) + ": Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as quiz owner")  
                return                                             
            i=1   
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz attempts and score before clearing all attempts for " + self.userNameUser1)  
            if self.common.quizAnalytics.verifyAllUsersAttemptsAndScore(self.allUsersDataInAnalytics, enums.playerQuizScoreType.LATEST, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score before clearing all attempts for " + self.userNameUser1)  
                return                                                                    
               
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to remove last attempt for " + self.userNameUser3) 
            if self.common.quizAnalytics.deleteUserAttempts(self.userId3, enums.quizAnlyticsDeleteOption.REMOVE_LAST_ATTEMPT) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to clear all quiz attempts" + self.userNameUser3)
                return   
            
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz attempts and score for other users after removing last attempt for " + self.userNameUser3)  
            if self.common.quizAnalytics.verifyAllUsersAttemptsAndScore(self.usersDataInAnalyticsAfterDeletion, enums.playerQuizScoreType.LATEST) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score for other users after removing last attempt for " + self.userNameUser3)  
                return             

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Remove last attempt when when no attempts still left was done successfully")
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