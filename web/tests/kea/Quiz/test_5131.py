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
    # Test Name : Quiz - Analytics - Remove Last attempts - Highest score type
    # Test description:
    # Go to editor page and create quiz with option to retake quiz - 3 attempts and all type of questions
    # Go to quiz page with different user and answer quiz -> Login with quiz owner -> Delete last attempt -> Go to quiz page as the user that answer the quiz and verify that he is able to answer the quiz again
    # and that number of attempts is updated and correct
    #================================================================================================================================
    testNum = "5131"
    
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
    
    # Attempts #1 answers
    questionNumber1Attempt1 = "question #1 Title"
    answerquestionNumber1Attempt1 = "question #1 option #1"
    
    questionNumber2Attempt1 = "question #2 Title"
    answerquestionNumber2Attempt1 = "question #2 option #2"
    
    questionNumber3Attempt1 = "question #3 Title"
    answerquestionNumber3Attempt1 = "question #3 option #2"

    
    # Attempts #2 answers
    questionNumber1Attempt2 = "question #1 Title"
    answerquestionNumber1Attempt2 = "question #1 option #1"
    
    questionNumber2Attempt2 = "question #2 Title"
    answerquestionNumber2Attempt2 = "question #2 option #1"
    
    questionNumber3Attempt2 = "question #3 Title"
    answerquestionNumber3Attempt2 = "question #3 option #2"
    
    # Attempts #3 answers
    questionNumber1Attempt3 = "question #1 Title"
    answerquestionNumber1Attempt3 = "question #1 option #2"
    
    questionNumber2Attempt3 = "question #2 Title"
    answerquestionNumber2Attempt3 = "question #2 option #2"
    
    questionNumber3Attempt3 = "question #3 Title"
    answerquestionNumber3Attempt3 = "question #3 option #2"    

    quizQuestionDictAttempt1 = {questionNumber1Attempt1:answerquestionNumber1Attempt1, questionNumber2Attempt1:answerquestionNumber2Attempt1, questionNumber3Attempt1:answerquestionNumber3Attempt1}
    quizQuestionDictAttempt2 = {questionNumber1Attempt2:answerquestionNumber1Attempt2, questionNumber2Attempt2:answerquestionNumber2Attempt2, questionNumber3Attempt2:answerquestionNumber3Attempt2}
    quizQuestionDictAttempt3 = {questionNumber1Attempt3:answerquestionNumber1Attempt3, questionNumber2Attempt3:answerquestionNumber2Attempt3, questionNumber3Attempt3:answerquestionNumber3Attempt3}
    
    quizQuestionsDict2FirstAttempts = [quizQuestionDictAttempt1, quizQuestionDictAttempt2]
    QuizQuestionDictAfterRemovingLastAttempt = [quizQuestionDictAttempt3]
    
    # Score for each attempt - individual for each attempts
    specificScoreAttempt1 = '33'
    specificScoreAttempt2 = '67'
    specificScoreAttempt3 = '0'
    
    quizSpecificAttemptScore = [specificScoreAttempt1, specificScoreAttempt2]
    
    # Score for each attempt - general for all attempts
    generalScoreAttempt1 = '33'
    generalScoreAttempt2 = '67'
    generalScoreAttempt3 = '33'
    
    quizGeneral2FirstAttemptsScore = [generalScoreAttempt1, generalScoreAttempt2]
    
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
            self.entryName = clsTestService.addGuidToString("Quiz - Remove last attempt - Highest score", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz - Remove last attempt - Highest score - Quiz", self.testNum)      
 
            self.keaScoreType                    = {enums.KEAQuizOptions.QUIZ_SCORE_TYPE:enums.keaQuizScoreType.HIGHEST.value}
            self.keaNumberOfAllowedAttempts      = {enums.KEAQuizOptions.SET_NUMBER_OF_ATTEMPTS:3}
            self.keaAllowMultipleScore           = {enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:True}
             
            self.keaScoreOptions                 = [self.keaAllowMultipleScore, self.keaNumberOfAllowedAttempts, self.keaScoreType]
             
            self.keaAllScoreOptionsList          = [self.keaScoreOptions]     
             
            self.totalGivenAttempts              = 3
             
            self.entryPageURL                    = None
             
            self.loginUsername = "ivq_automation_user_1"
            self.userPass = '123456'
            self.userName = 'QA Member 1'
             
            self.numberOfAttemptsBeforeDeletion = '2/3'
            self.scoreBeforeDeletion = '67%'   
             
            self.numberOfAttemptsAfterDeletion = '1/3'
            self.scoreAfterDeletion = '33%'   
            
            self.numberOfAttemptsAfterRetaking = '2/3'
            self.scoreAfterRetaking = '33%'  
            
            self.currentAttempt = 2    
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
            if self.common.player.verifyQuizAttempts(self.quizQuestionsDict2FirstAttempts, expectedQuizScore=self.quizSpecificAttemptScore, totalGivenAttempts=self.totalGivenAttempts, expectedAttemptGeneralScore=self.quizGeneral2FirstAttemptsScore, scoreType=enums.playerQuizScoreType.HIGHEST) == False:
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
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz attempts and score before removing last attempt")  
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername, self.userName, self.numberOfAttemptsBeforeDeletion, self.scoreBeforeDeletion, enums.playerQuizScoreType.HIGHEST, self.quizEntryName, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score before removing last attempt")  
                return                                                                    
               
            i = + 1       
            writeToLog("INFO","Step " + str(i) + ": Going to delete quiz attempt") 
            if self.common.quizAnalytics.deleteUserAttempts(self.loginUsername, enums.quizAnlyticsDeleteOption.REMOVE_LAST_ATTEMPT) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED: to delete quiz attempt")
                return  
              
            i = i + 1    
            writeToLog("INFO","Step " + str(i) + ": Going to verify quiz attempts and score after removing last attempt")  
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername , self.userName + "   Last Attempt removed", self.numberOfAttemptsAfterDeletion, self.scoreAfterDeletion, enums.playerQuizScoreType.HIGHEST) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score after removing last attempt")  
                return  
     
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
            if self.common.player.verifyQuizAttemptsAfterRemovingLastAttempt(self.QuizQuestionDictAfterRemovingLastAttempt, expectedQuizScore=[self.specificScoreAttempt3],currentAttempt=self.currentAttempt, totalGivenAttempts=self.totalGivenAttempts, expectedAttemptGeneralScore=[self.generalScoreAttempt3], scoreType=enums.playerQuizScoreType.HIGHEST) == False:
                
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
            if self.common.quizAnalytics.verifyUserAttemptsAndScore(self.loginUsername, self.userName, self.numberOfAttemptsAfterRetaking, self.scoreAfterRetaking, enums.playerQuizScoreType.HIGHEST, self.quizEntryName, True) == False:
                
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify quiz attempts and score after retaking quiz")  
                return                                                                               

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Remove last attempts when 'allow multiple attempts is available was done successfully")
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