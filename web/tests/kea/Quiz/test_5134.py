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
    # Test Name : Quiz - Analytics - Clear all attempts when attempts still left
    # Test description:
    # Go to editor page and create quiz with option to retake quiz - 3 attempts and all type of questions
    # Go to quiz page with different user and answer quiz, don't take all attempts-> Login with quiz owner -> Quiz analytics page -> Clear all attempts -> 
    # Verify that user row was deleted -> Verify that user is able to answer quiz from begining and that he has 3 attempts
    #================================================================================================================================
    testNum = "5134"
    
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
    
    # Attempts #1 answers - Before clreaing attempts
    questionNumber1Attempt1 = "question #1 Title"
    answerquestionNumber1Attempt1 = "question #1 option #1"
    
    questionNumber2Attempt1 = "question #2 Title"
    answerquestionNumber2Attempt1 = "question #2 option #1"
    
    questionNumber3Attempt1 = "question #3 Title"
    answerquestionNumber3Attempt1 = "question #3 option #1"

    
    # Attempts #2 answers - Before clearing attempts
    questionNumber1Attempt2 = "question #1 Title"
    answerquestionNumber1Attempt2 = "question #1 option #1"
    
    questionNumber2Attempt2 = "question #2 Title"
    answerquestionNumber2Attempt2 = "question #2 option #2"
    
    questionNumber3Attempt2 = "question #3 Title"
    answerquestionNumber3Attempt2 = "question #3 option #2"
    
    # Attempts #1 answers
    questionNumber1Attempt3 = "question #1 Title"
    answerquestionNumber1Attempt3 = "question #1 option #2"
    
    questionNumber2Attempt3 = "question #2 Title"
    answerquestionNumber2Attempt3 = "question #2 option #2"
    
    questionNumber3Attempt3 = "question #3 Title"
    answerquestionNumber3Attempt3 = "question #3 option #2"    

    quizQuestionDictAttempt1BeforeClearingAttempts = {questionNumber1Attempt1:answerquestionNumber1Attempt1, questionNumber2Attempt1:answerquestionNumber2Attempt1, questionNumber3Attempt1:answerquestionNumber3Attempt1}
    quizQuestionDictAttempt2BeforeClearingAttempts = {questionNumber1Attempt2:answerquestionNumber1Attempt2, questionNumber2Attempt2:answerquestionNumber2Attempt2, questionNumber3Attempt2:answerquestionNumber3Attempt2}
    quizQuestionDictAttempt1AfterClearingAttempts = {questionNumber1Attempt2:answerquestionNumber1Attempt3, questionNumber2Attempt3:answerquestionNumber2Attempt3, questionNumber3Attempt3:answerquestionNumber3Attempt3}
    
    quizQuestionsDictAttemptsBeforeClearingAttempts = [quizQuestionDictAttempt1BeforeClearingAttempts, quizQuestionDictAttempt2BeforeClearingAttempts]
    quizQuestionsDictAttemptsAfterClearingAllAttempts = [quizQuestionDictAttempt1AfterClearingAttempts]
    
    # Score for each attempt - individual for each attempts - before clearing attempts
    specificScoreAttempt1BeforeClearingAttempts = '100'
    specificScoreAttempt2BeforeClearingAttempts = '67'
    
    quizSpecificAttemptScoreBeforeClearingAttempts = [specificScoreAttempt1BeforeClearingAttempts, specificScoreAttempt2BeforeClearingAttempts]
    
    # Score for each attempt - general for all attempts - before clearing attempts
    generalScoreAttempt1BeforeClearingAttempts = '100'
    generalScoreAttempt2BeforeClearingAttempts = '67'

    quizGeneralAttemptsScoreBeforeClearingAttempts = [generalScoreAttempt1BeforeClearingAttempts, generalScoreAttempt2BeforeClearingAttempts]
    
    # Score for each attempt - individual for each attempts - after clearing attempts
    specificScoreAttempt1AfterClearingAttempts = '0'
    
    quizSpecificAttemptScoreAfterClearingAttempts = [specificScoreAttempt1AfterClearingAttempts]
    
    # Score for each attempt - general for all attempts - after clearing attempts
    generalScoreAttempt1AfterClearingAttempts = '0'
    
    quizGeneralAttemptsScoreAfterClearingAllAttempts = [generalScoreAttempt1AfterClearingAttempts]
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
            self.entryName = clsTestService.addGuidToString("Quiz - Clear all attempts when no attempts still left", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz - Clear all attempts when no attempts still left - Quiz", self.testNum)      
 
            self.keaScoreType                    = {enums.KEAQuizOptions.QUIZ_SCORE_TYPE:enums.keaQuizScoreType.LATEST.value}
            self.keaNumberOfAllowedAttempts      = {enums.KEAQuizOptions.SET_NUMBER_OF_ATTEMPTS:3}
            self.keaAllowMultipleScore           = {enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:True}
             
            self.keaScoreOptions                 = [self.keaAllowMultipleScore, self.keaNumberOfAllowedAttempts, self.keaScoreType]
             
            self.keaAllScoreOptionsList          = [self.keaScoreOptions]     
             
            self.totalGivenAttempts              = 3
             
            self.entryPageURL                    = None
             
            self.loginUsername = "ivq_automation_user_1"
            self.userPass = '123456'
            self.userName = 'QA Member 1'
             
            self.numberOfAttemptsBeforeDeletion = '3/3'
            self.scoreBeforeDeletion = '67%'   
            
            self.numberOfAttemptsAfterRetaking = '1/3'
            self.scoreAfterRetaking = '0%'  
                
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
                                         
            writeToLog("INFO","Step 4: Going to to wait until media end upload process")    
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to wait until media end upload process")
                return
                                                                        
            writeToLog("INFO","Step 5 : Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5 : FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return
                
            self.common.base.switch_to_default_content()
                    
            writeToLog("INFO","Step 6: Going to get entry page URL")
            self.entryPageURL = self.common.base.driver.current_url
                    
            writeToLog("INFO","Step 7: Going to publish entry to unlisted")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate(self.quizEntryName, enums.ChannelPrivacyType.UNLISTED, publishFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 7: FAILED failed to publish entry to unlisted")
                return 
                      
            writeToLog("INFO","Step 8: Going to navigate to KEA Quiz tab for " + self.quizEntryName)  
            if self.common.kea.initiateQuizFlow(self.quizEntryName, True, 1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to navigate to KEA Quiz tab for " + self.quizEntryName)  
                return 
                      
            i = 9
                      
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
                
            i = i + 1    
            self.common.base.switch_to_default_content()
           
            writeToLog("INFO","Step " + str(i) + ": Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as quiz owner")  
                return 
                
            i = i + 1 
                       
            writeToLog("INFO","Step " + str(i) + ": Going to login as " + self.userName)  
            if self.common.login.loginToKMS(self.loginUsername, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as " + self.userName)  
                return 
                      
            i = i + 1  
                      
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to entry page link")
                return             
                 
            i = i + 1         
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.quizQuestionsDictAllAttempts, expectedQuizScore=self.quizSpecificAttemptScoreBeforeClearingAttempts, totalGivenAttempts=self.totalGivenAttempts, expectedAttemptGeneralScore=self.quizGeneralAttemptsScoreBeforeClearingAttempts, scoreType=enums.playerQuizScoreType.LATEST) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return    
                
            i = i + 1    
            self.common.base.switch_to_default_content()
            
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userName)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userName)  
                return  
               
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as quiz owner")  
                return 
               
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz attempts and score before clearing all attempts")  
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername, self.userName, self.numberOfAttemptsBeforeDeletion, self.scoreBeforeDeletion, enums.playerQuizScoreType.LATEST, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score before clearing all attempts")  
                return                                                                    
               
            i = i + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to clear all quiz attempts") 
            if self.common.quizAnalytics.deleteUserAttempts(self.loginUsername, enums.quizAnlyticsDeleteOption.CLEAR_ALL_ATTEMPTS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to clear all quiz attempts")
                return  
              
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to verify message after removing all attempt")  
            if self.common.quizAnalytics.verifyRemovedAttemptMessage() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify message after removing all attempt")  
                return  
            
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to verify that quiz attempts and score aren't displayed anymore")  
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername, self.userName, self.numberOfAttemptsBeforeDeletion, self.scoreBeforeDeletion, enums.playerQuizScoreType.LATEST, self.quizEntryName, True) == True:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score aren't displayed anymore")  
                return 
            writeToLog("INFO","Step " + str(i) + ": Failed as expected")             
             
            i = i + 1   
            writeToLog("INFO","Step " + str(i) + ": Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as quiz owner")  
                return 
              
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to login as " + self.userName)  
            if self.common.login.loginToKMS(self.loginUsername, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as " + self.userName)  
                return       
              
            i = i + 1        
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to entry page link")
                return             
              
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to answer quiz " + self.quizEntryName)  
            if self.common.player.verifyQuizAttempts(self.quizQuestionsDictAttemptsAfterClearingAllAttempts, expectedQuizScore=self.quizSpecificAttemptScoreAfterClearingAttempts, totalGivenAttempts=self.totalGivenAttempts, expectedAttemptGeneralScore=self.quizGeneralAttemptsScoreAfterClearingAllAttempts, scoreType=enums.playerQuizScoreType.LATEST) == False:     
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to answer quiz " + self.quizEntryName)
                return     
              
            i = i + 1    
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step " + str(i) + ": Going to logout as " + self.userName)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to logout as " + self.userName)  
                return  
              
            i = i + 1         
            writeToLog("INFO","Step " + str(i) + ": Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to login as quiz owner")  
                return 
 
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz attempts and score after retaking quiz")  
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername, self.userName, self.numberOfAttemptsAfterRetaking, self.scoreAfterRetaking, enums.playerQuizScoreType.LATEST, self.quizEntryName, True) == False:
                 
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score after retaking quiz")  
                return                                                                               

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Clear all attempts when when no attempts still left was done successfully")
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