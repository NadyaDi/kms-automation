import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Quiz - Change Answer order for all Quiz Question Types - KEA Editor 
    # Test description:
    # Verify that the user is able to change the Quiz Question type's answer order 
    # Verify that the user is able to change the order using swap and drag and drop options
    #================================================================================================================================
    testNum = "4829"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
        
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']
    
    # This list is used in order to change the answer order using drag and drop
    # index 0 = question title that must be found while hovering over the quiz question bubble
    # index 1 = question answer that we want to move to a different location
    # index 2 = question location where we want to move index 1
    answerOrderOne        = ['question #1 Title', 4, 1]   
    answerOrderTwo        = ['question #2 Title', 1, 2]   
    answerOrderThree      = ['question #3 Title', 1, 4]
    
    # This list is used in order to verify that the answer options are displayed in the desired order
    answerListOrderOne    = ['question #1 option #4', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3']
    answerListOrderTwo    = ['question #2 option #2', 'question #2 option #1', 'question #2 option #3', 'question #2 option #4']   
    answerListOrderThree  = ['question #3 option #2', 'question #3 option #3', 'question #3 option #4', 'question #3 option #1']   
    
    # This dictionary is used in order to create the quiz questions
    dictQuestions         = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3}
    
    # This dictionary is used in order to change the answer list order
    changeAnswerOrderDict = {'1':answerOrderOne, '2':answerOrderTwo, '3':answerOrderThree} 
    
    # This dictionary is used in order to verify the answer list order
    verifyAnswerOrderDict = {'1':answerListOrderOne, '2':answerListOrderTwo, '3':answerListOrderThree} 


    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):
        #write to log we started the test
        logStartTest(self,driverFix)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            ##################################################################
            self.entryName           = clsTestService.addGuidToString("Quiz - Answer Order - KEA Page", self.testNum)
            self.entryNameQuiz       = clsTestService.addGuidToString("Quiz - Answer Order - KEA Page - Quiz", self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to create a new entry, " + self.entryName)  
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create a new entry, " + self.entryName)  
                return
                     
            writeToLog("INFO","Step 2: Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return
               
            writeToLog("INFO","Step 3: Going to navigate to " + self.entryNameQuiz + " entry editor")  
            if self.common.kea.launchKEA(self.entryNameQuiz, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to " + self.entryNameQuiz + " entry editor") 
                return
              
            writeToLog("INFO","Step 4: Going to verify that the answer order for " + self.entryNameQuiz + " can be changed by drag and drop")  
            if self.common.kea.changeAnswerOrder(self.changeAnswerOrderDict, self.verifyAnswerOrderDict)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to verify that the answer order for " + self.entryNameQuiz + " can be changed by drag and drop")  
                return
            
            writeToLog("INFO","Step 5: Going to verify that the answer order for " + self.entryNameQuiz + " can be changed using shuffle option")  
            if self.common.kea.changeAnswerOrder(self.changeAnswerOrderDict, self.verifyAnswerOrderDict, True)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify that the answer order for " + self.entryNameQuiz + " can be changed using shuffle option")  
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: The answer order for all the available quiz question has been successfully changed and verified")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.entryNameQuiz])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')