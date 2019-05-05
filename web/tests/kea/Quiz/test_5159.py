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
    # Test Name : Quiz - Analytics - Export quiz answers - Allow multiple attempts is disabled
    # Test description:
    # Go to editor page and create quiz with all type of questions with no option to retake -> Login with 3 different users and answer the quiz - > Login as admin
    # Go to analytics page -> quiz users tab -> click on export to csv -> Verify that correct users data is displayed
    #================================================================================================================================
    testNum = "5159"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathEntry = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    filePathQuizUsers = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\templates\quiz_users_5159.csv'
    filePathExoprtedQuizUsers = localSettings.LOCAL_SETTINGS_JENKINS_NODE_MEDIA_PATH + '/quiz_users.csv'
    
#    Next line is for local running 
#    filePathExoprtedQuizUsers = 'C:\\Users\\inbar.willman\\eclipse-workspace\\kms-automation\\web\\temp\\downloads\\quiz_users.csv'
    
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text']
    questionNumber3 = ['00:20', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q'] 
    questionNumber4 = ['00:25', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']  
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3,'4':questionNumber4} 
    
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
    quizQuestionNumber2 = "Question Title for True and False"
    quizQuestionNumber3 = "Question Title for Open-Q"
    quizQuestionNumber4 = "Question Title for Reflection Point"
    
    # User 1 answer
    user1answerQuestionNumber1 = "question #1 option #1"
    user1answerQuestionNumber2 = "True text"
    user1answerQuestionNumber3 = "Open-Q answer QA_Member_1 "
    
    # User 2 answer
    user2answerQuestionNumber1 = "question #1 option #1"
    user2answerQuestionNumber2 = "False text"
    user2answerQuestionNumber3 = "Open-Q answer QA_Member_2"
    
    # User 3 answer
    user3answerQuestionNumber1 = "question #1 option #2"
    user3answerQuestionNumber2 = "True text"
    user3answerQuestionNumber3 = "Open-Q answer QA_Member_3"
    
    user1AnswersDict ={quizQuestionNumber1:user1answerQuestionNumber1, quizQuestionNumber2:user1answerQuestionNumber2, quizQuestionNumber3:user1answerQuestionNumber3}
    user2AnswersDict ={quizQuestionNumber1:user2answerQuestionNumber1, quizQuestionNumber2:user2answerQuestionNumber2, quizQuestionNumber3:user2answerQuestionNumber3}
    user3AnswersDict ={quizQuestionNumber1:user3answerQuestionNumber1, quizQuestionNumber2:user3answerQuestionNumber2, quizQuestionNumber3:user3answerQuestionNumber3}

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
            self.entryName = clsTestService.addGuidToString("Quiz - Analytics - Export quiz questions", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz - Analytics - Export quiz questions - Quiz", self.testNum)      
            self.entryPageURL = None

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
                  
            writeToLog("INFO","Step 7 : Going to logout as quiz owner")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7 : FAILED to logout as quiz owner")  
                return 
                  
            writeToLog("INFO","Step 8 : Going to login as " + self.userNameUser1)  
            if self.common.login.loginToKMS(self.userId1, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8 : FAILED to login as " + self.userNameUser1)  
                return       
                  
            writeToLog("INFO","Step 9: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 9: FAILED to navigate to entry page link")
                return             
                   
            writeToLog("INFO","Step 10 : Going to answer quiz as " + self.userNameUser1)  
            if self.common.player.answerQuiz(self.user1AnswersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10 : FAILED to answer quiz as " + self.userNameUser1)  
                return    
                   
            self.common.base.switch_to_default_content()
                   
            writeToLog("INFO","Step 11 : Going to logout as " + self.userNameUser1)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11 : FAILED to logout as " + self.userNameUser1)  
                return  
              
            writeToLog("INFO","Step 12 : Going to login as " + self.userNameUser2)  
            if self.common.login.loginToKMS(self.userId2, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12 : FAILED to login as " + self.userNameUser2)  
                return       
                  
            writeToLog("INFO","Step 13: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 13: FAILED to navigate to entry page link")
                return             
                   
            writeToLog("INFO","Step 14 : Going to answer quiz as " + self.userNameUser2)  
            if self.common.player.answerQuiz(self.user2AnswersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14 : FAILED to answer quiz as " + self.userNameUser2)  
                return    
                   
            self.common.base.switch_to_default_content()
              
            writeToLog("INFO","Step 15 : Going to logout as " + self.userNameUser2)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15 : FAILED to logout as " + self.userNameUser2)  
                return              
              
            writeToLog("INFO","Step 16 : Going to login as " + self.userNameUser3)  
            if self.common.login.loginToKMS(self.userId3, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16 : FAILED to login as " + self.userNameUser3)  
                return       
                  
            writeToLog("INFO","Step 17: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 17: FAILED to navigate to entry page link")
                return             
                   
            writeToLog("INFO","Step 18 : Going to answer quiz as " + self.userNameUser3)  
            if self.common.player.answerQuiz(self.user3AnswersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, showScore=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18 : FAILED to answer quiz as " + self.userNameUser3)  
                return    
                   
            self.common.base.switch_to_default_content()
                   
            writeToLog("INFO","Step 19 : Going to logout as " + self.userNameUser3)  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19 : FAILED to logout as " + self.userNameUser3)  
                return  
                  
            writeToLog("INFO","Step 20 : Going to login as quiz owner")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20 : FAILED to login as quiz owner")  
                return   
             
            writeToLog("INFO","Step 21 : Going to export question csv file")  
            if self.common.quizAnalytics.exportCsvFileQuizAnalyticsPage(enums.quizAnalytics.QUIZ_USERS, self.quizEntryName, True)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21 : FAILED to export question csv file")  
                return
            
            sleep(10)
            
            writeToLog("INFO","Step 22 : Going to verify that quiz questions csv files is download correctly")  
            if self.common.compareBetweenTwoCsvFiles(self.filePathExoprtedQuizUsers, self.filePathQuizUsers)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22 : FAILED to verify that quiz questions csv files is download correctly")  
                return                                                         

            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Verify quiz answers csv file was done successfully")
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