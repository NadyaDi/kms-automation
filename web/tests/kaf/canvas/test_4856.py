import sys,os
from enums import Location
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from enum import *
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *
import ctypes
from upload import UploadEntry

class Test:
    #================================================================================================================================
    # @Author: Inbar Willman
    # Test Name : Canvas: Gradebook
    # Test description:
    # Upload entry
    # Go course -> Go to 'Announcements' tab -> Add new announcement -> In announcement, click on wysiwyg and choose media to embed from upload page
    # Verify that the embed was created successfully 
    # Verify that the embed was deleted successfully
    #================================================================================================================================
    testNum     = "4856"
    application = enums.Application.CANVAS
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
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
    
    questionName1 = "question #1 Title"
    answerText1   = "question #1 option #2"
    
    questionName2 = "question #2 Title"
    answerText2   = "question #2 option #1"
    
    questionName3 = "question #3 Title"
    answerText3   = "question #3 option #1"
    
    entryUrl = ''
    
    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be present in the Question Name
    questionDict = {questionName1:answerText1, 
                    questionName2:answerText2, 
                    questionName3:answerText3}
    
    #this dictionary is used in order to verify that proper elements are present in the include answer screen
    includeAnswersDict = {questionName1:{'correct':answerText1, 'given':answerText1}, 
                          questionName2:{'correct':answerText2, 'given':answerText2}, 
                          questionName3:{'correct':answerText3, 'given':answerText3}}
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix, self.application)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Quiz_Gradebook", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("Quiz_Gradebook - Quiz", self.testNum)
            self.newEntryName = clsTestService.addGuidToString("Quiz_Gradebook-Quiz", self.testNum)
            self.entryToUpload = UploadEntry(self.filePath, self.entryName, self.description, self.tags, timeout=60, retries=3)
            self.uploadEntrieList = [self.entryToUpload] 
            self.ponitesPossible = '100'
            self.expectedGrade = '66.67'
            self.kalturaVideoQuizName = clsTestService.addGuidToString("gradebook", self.testNum) 
            
            self.galleryName = "New1"
            
            self.studentUsername = 'studentautomation@mailinator.com'
            self.studentPassword = 'Kaltura1!'
            
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entry")    
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
                               
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
                             
            writeToLog("INFO","Step 4: Going to to navigate to My Media page")    
            if self.common.kafGeneric.navigateToMyMediaKAF() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to navigate to My Media page")
                return            
                               
            writeToLog("INFO","Step 5 : Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5 : FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return 
               
            writeToLog("INFO","Step 6 : Going to navigate to quiz entry page")  
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.quizEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6 : FAILED to navigate to quiz entry page")  
                return
                
            writeToLog("INFO","Step 7 : Going to edit quiz name")  
            if self.common.editEntryPage.changeEntryMetadata(self.quizEntryName, self.newEntryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7 : FAILED to edit quiz name")  
                return 
                
            writeToLog("INFO","Step 8 : Going to create embed assignment")  
            if self.common.canvas.createEmbedAssignment(self.kalturaVideoQuizName, self.newEntryName, self.ponitesPossible) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8 : FAILED to create embed assignment")  
                return  
             
            writeToLog("INFO","Step 9 : Going to logout as main user")  
            if self.common.canvas.logOutOfCanvas() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9 : FAILED to logout as main user")  
                return
             
            writeToLog("INFO","Step 10 : Going to login as student")  
            if self.common.canvas.loginToCanvas(self.studentUsername, self.studentPassword) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10 : FAILED to login as student")  
                return  
             
            writeToLog("INFO","Step 11: Going to navigate to assignment page")  
            if self.common.canvas.navigateToAssignmentPage(self.kalturaVideoQuizName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to navigate to assignment page")
                return             
              
            writeToLog("INFO","Step 12: Going to answer quiz as student")  
            if self.common.player.answerQuiz(self.questionDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to answer quiz as student")
                return  
              
            self.common.base.switch_to_default_content()
 
            writeToLog("INFO","Step 13 : Going to verify grade as student")  
            if self.common.canvas.verifyGradeAsStudentCanvas(self.expectedGrade, self.kalturaVideoQuizName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13 : FAILED to verify grade as student")  
                return  
                                                                  
            writeToLog("INFO","Step 14: Going to logout from Canvas as student")  
            if self.common.canvas.logOutOfCanvas() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to logout from Canvas as student")
                return    
                  
            writeToLog("INFO","Step 15: Going to login to Canvas as main user")  
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to login to Canvas as main user")
                return 
               
            writeToLog("INFO","Step 16: Going to verify gradebook grade as main user")  
            if self.common.canvas.verifyGradeAsAdminCanvas(self.expectedGrade, self.kalturaVideoQuizName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to verify gradebook grade as main user")
                return 
             
            writeToLog("INFO","Step 17: Going to delete assignment")  
            if self.common.canvas.deleteAssignment(self.kalturaVideoQuizName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to delete assignment")
                return                 
            
            #########################################################################
            writeToLog("INFO","TEST PASSED: Gradebook test was done successfully")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)  
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.base.switch_to_default_content()
            if (localSettings.LOCAL_SETTINGS_LOGIN_USERNAME.lower() in self.common.canvas.getCanvasLoginUserName()) == False:
                self.common.canvas.logOutOfCanvas()
                self.common.loginAsUser()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.newEntryName])
            self.common.canvas.deleteAssignment(self.kalturaVideoQuizName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')