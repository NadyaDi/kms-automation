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
    # Test Name : Quiz - Analytics - Open-Q feedback - Co-editor
    # Test description:
    # Go to editor page and create quiz with open-Q only 
    # Go to quiz page and and user as co-editor -> answer open-Q -> Go to Quiz Analytics -> Go to Quiz Question tab -> Add feedback to open-Q -> 
    # Login as co-editor -> Go to Quiz Analytics -> Go to Quiz Question tab -> Edit feedback to open-Q -> Delete Feedback -> Add feedback
    #================================================================================================================================
    testNum = "5113"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    questionOpen1 = ['00:25', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q 1']
    questionOpen2 = ['00:15', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q 2']
    
    # This Dictionary is used in order to create all the Quiz Question types within a single call
    questionDict = {'1':questionOpen1, '2':questionOpen2} 
    
    questionName1 = 'Question Title for Open-Q 1'
    answerText1   = 'Answer for Open-Q 1'
    
    questionName2 = 'Question Title for Open-Q 2'
    answerText2   = 'Answer for Open-Q 2'    

    quizQuestionDict = {questionName1:answerText1, questionName2:answerText2}
    
    questionAnswerOneSubmitted1 = ['Question Title for Open-Q 1', 'Answer for Open-Q 1', True]
    questionAnswerOneSubmitted2 = ['Question Title for Open-Q 1', 'Answer for Open-Q 2', True]

    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizStateSubmitted = {'1':questionAnswerOneSubmitted1, '2':questionAnswerOneSubmitted2} 
    
    adminFeedbackQuesion1 = 'Feedback for first open-Q' 
    adminFeedbackQuesion2 = 'Feedback for second open-Q'    
    coEditorFeedbackQuesion1 = 'Not good enough'  
    feedbackDate = ''
    
    # List of the open questions new added feedback
    openQuestionFeedbackToAdd1 = [questionName1, adminFeedbackQuesion1, 'QA Automation', feedbackDate] 
    openQuestionFeedbackToAdd2 = [questionName2, adminFeedbackQuesion2, 'QA Automation', feedbackDate]
    
    # This dictionary contains all the questions that need to be added
    addedFeedbackList = {'1':openQuestionFeedbackToAdd1, '2':openQuestionFeedbackToAdd2}

    # List of open questions new edited feedback
    openQuestionFeedbackToEdit1 = [questionName1, adminFeedbackQuesion1, coEditorFeedbackQuesion1, 'QA Member', feedbackDate]
    
    # This dictionary contains all the questions that need to be edited
    editedFeedbackList = {'1':openQuestionFeedbackToEdit1}
    
    # List of questions to delete
    openQuestionFeedbackToDelete = [questionName2, adminFeedbackQuesion2]

    # This dictionary contains all the questions that need to be deleted
    deletedFeedbackList = {'1':openQuestionFeedbackToDelete}
    
    # This dictionary contains the questions that deleted or edited and need to be verified by second user
    deletedOrEditedFeedbackList = {'1':openQuestionFeedbackToEdit1, '2':openQuestionFeedbackToDelete}
    
    coEditorUsername = 'python_member'
    coEditorPassword = 'Kaltura1!'
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
            self.entryName = clsTestService.addGuidToString("IVQ - Open-Q - Feedback - Co-editor", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("IVQ - Open-Q - Feedback - Co-editor - Quiz", self.testNum)   
            self.entryPageURL= ''  
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
  
            writeToLog("INFO","Step 6: Going to get entry page URL")
            self.entryPageURL = self.common.base.driver.current_url
              
            self.common.base.switch_to_default_content()            
              
            writeToLog("INFO","Step 7 : Going to navigate to edit entry page for " + self.quizEntryName)  
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.quizEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7 : FAILED to navigate to edit entry page for " + self.quizEntryName)  
                return               
              
            writeToLog("INFO","Step 8 : Going to add co-editor to " + self.quizEntryName)  
            if self.common.editEntryPage.addCollaborator(self.quizEntryName, self.coEditorUsername, True, False, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8 : FAILED to add co-editor to " + self.quizEntryName)  
                return  
             
            writeToLog("INFO","Step 9: Going to publish entry to unlisted")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate(self.quizEntryName, enums.ChannelPrivacyType.UNLISTED, publishFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 9: FAILED failed to publish entry to unlisted")
                return                        
              
            writeToLog("INFO","Step 10 : Going to add feedback to quiz open questions as quiz admin")  
            if self.common.quizAnalytics.addFeedbackToOpenQuestion(self.addedFeedbackList, entryName=self.quizEntryName, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10 : FAILED to add feedback to quiz open questions as quiz admin")  
                return            
              
            writeToLog("INFO","Step 11 : Going to logout as quiz admin")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11 : FAILED to logout as quiz admin")  
                return
             
            writeToLog("INFO","Step 12 : Going to login as quiz co-editor")  
            if self.common.login.loginToKMS(self.coEditorUsername, self.coEditorPassword) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12 : FAILED to login as quiz co-editor")  
                return    
             
            writeToLog("INFO","Step 13: Going to navigate to entry page (by link)")
            if self.common.base.navigate(self.entryPageURL) == False:
                writeToLog("INFO","Step 13: FAILED to navigate to entry page link")
                return             
             
            writeToLog("INFO","Step 14 : Going to edit feedback to the quiz first open-Q as co-editor")  
            if self.common.quizAnalytics.editOpenQuestionFeedback(self.editedFeedbackList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14 : FAILED to edit feedback to the quiz first open-Q as co-editor")  
                return 
             
            writeToLog("INFO","Step 15 : Going to delete quiz seconds open-Q as co-editor")  
            if self.common.quizAnalytics.deleteOpenQuestionFeedback(self.deletedFeedbackList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15 : FAILED to delete quiz seconds open-Q as co-editor")  
                return             
             
            writeToLog("INFO","Step 16 : Going to logout as quiz co-editor")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16 : FAILED to logout as quiz co-editor")  
                return
             
            writeToLog("INFO","Step 17 : Going to login as quiz admin")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17 : FAILED to login as quiz admin")  
                return
            
            writeToLog("INFO","Step 18 : Going to verify the edited and deleted feedback as admin")  
            if self.common.quizAnalytics.verifyOpenQuestionFeedbackAfterEditOrDeletion(self.deletedOrEditedFeedbackList, entryName=self.quizEntryName, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18 : FAILED to verify the edited and deleted feedback as admin")  
                return      
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Open-Q feedback is added successfully by co-editor")
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