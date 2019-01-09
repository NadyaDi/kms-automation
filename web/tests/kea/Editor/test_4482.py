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
    #  @Author: Tzachi Guetta
    # Test Name : Trimming a Quiz entry
    # Test description:
    # 
    #================================================================================================================================
    testNum = "4482"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    questionNumber1 = ['00:05', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:10', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:15', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4'] 
    questionNumber4 = ['00:20', enums.QuizQuestionType.Multiple, 'question #4 Title', 'question #4 option #1', 'question #4 option #2', 'question #4 option #3', 'question #4 option #4'] 
    questionNumber5 = ['00:25', enums.QuizQuestionType.Multiple, 'question #5 Title', 'question #5 option #1', 'question #5 option #2', 'question #5 option #3', 'question #5 option #4']   
    dictQuestions = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3,'4':questionNumber4,'5':questionNumber5} 
    
    questionTrim1 = ['00:05', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionTrim2 = ['00:10', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionTrim5 = ['00:15', enums.QuizQuestionType.Multiple, 'question #5 Title', 'question #5 option #1', 'question #5 option #2', 'question #5 option #3', 'question #5 option #4']   
    dictQuestionsTrimmedExist = {'1':questionTrim1,'2':questionTrim2,'3':questionTrim5}
    
    questionTrim3 = ['00:15', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4'] 
    questionTrim4 = ['00:20', enums.QuizQuestionType.Multiple, 'question #4 Title', 'question #4 option #1', 'question #4 option #2', 'question #4 option #3', 'question #4 option #4'] 
    dictQuestionsTrimmedAbsent = {'4':questionTrim3,'5':questionTrim4}         
    
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
            self.videoEntryName = clsTestService.addGuidToString("Upload media - Video", self.testNum)
            expectedEntryDuration = "00:20"
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload entry")  
            if self.common.upload.uploadEntry(self.filePathVideo, self.videoEntryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to add Quiz")  
            if self.common.kea.quizCreation(self.videoEntryName, self.dictQuestions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to add Quiz")
                return  
            
            self.common.base.refresh()
            
            writeToLog("INFO","Step 3: Going to collect the new Quiz's question information from the player")  
            self.quizQuestionsBeforeTrimming = self.common.player.collectQuizQuestionsFromPlayer(self.videoEntryName + " - Quiz", 5)
            if  self.quizQuestionsBeforeTrimming == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to collect the new Quiz's question information from the player")
                return

            writeToLog("INFO","Step 4: Going to Compare the quiz questions info - that were presented on player")  
            if self.common.player.compareQuizQuestionDict(self.dictQuestions, self.quizQuestionsBeforeTrimming) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to Compare the quiz questions info - that were presented on player")
                return 
                        
            writeToLog("INFO","Step 5: Going to trim the entry from 12sec to 22sec - (2 quiz questions will be removed)")  
            if self.common.kea.trimEntry(self.videoEntryName + " - Quiz", "0012", "0022", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to trim the entry from 12sec to 22sec - (2 quiz questions will be removed)")
                return
 
            writeToLog("INFO","Step 6: Going to collect the new Quiz's question information from the player (after the Quiz was trimmed)")
            self.qestionCollectedafterTrim = self.common.player.collectQuizQuestionsFromPlayer(self.videoEntryName + " - Quiz", 3)
            if  self.qestionCollectedafterTrim == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to collect the new Quiz's question information from the player")
                return  
            
            writeToLog("INFO","Step 7: Going to Compare the quiz questions info - after the quiz was trimmed") 
            if self.common.player.compareQuizQuestionDict(self.qestionCollectedafterTrim, self.dictQuestionsTrimmedExist, self.dictQuestionsTrimmedAbsent) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to Compare the quiz questions info - after the quiz was trimmed") 
                return 
                 
            writeToLog("INFO","TEST PASSED")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.videoEntryName, self.videoEntryName + " - Quiz"])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')