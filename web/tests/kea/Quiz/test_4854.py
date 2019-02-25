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
    # Test Name : Quiz - Video playing and Navigation process with Quiz Questions in KEA Page
    # Test description:
    # Verify that the entire length of the entry can be played
    # Verify that the next / previous arrow for Quiz Question has proper functionality
    #================================================================================================================================
    testNum = "4854"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description   = "Description" 
    tags          = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    typeTest      = 'Video playing process with Quiz Questions'   
            
    # Each list is used in order to create a different Quiz Question Type
    questionMultiple         = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalse     = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflection       = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']
    
    # This Dictionary is used in order to create all the Quiz Question types within a single call
    questionDict             = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection}
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
            self.entryName        = clsTestService.addGuidToString("Quiz - KEA Player navigation in KEA Page", self.testNum)
            self.entryNameQuiz    = clsTestService.addGuidToString("Quiz - KEA Player navigation in KEA Page - Quiz", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to create a new entry, " + self.entryName)  
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create a new entry, " + self.entryName)  
                return
                                                     
            writeToLog("INFO","Step 2: Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
                                      
            writeToLog("INFO","Step 3: Going to navigate to " + self.entryNameQuiz + " entry editor")  
            if self.common.kea.launchKEA(self.entryNameQuiz, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to navigate to " + self.entryNameQuiz + " entry editor") 
                return
              
            writeToLog("INFO","Step 4: Going to verify that the " + self.entryNameQuiz + " can be fully played inside the KEA Page")  
            if self.common.kea.verifyPlayingProcess(tries=2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify that the " + self.entryNameQuiz + " can be fully played inside the KEA Page")  
                return
            
            writeToLog("INFO","Step 5: Going to verify that the " + self.entryNameQuiz + "'s Quiz Questions can be navigated inside the KEA Page")  
            if self.common.kea.verifyKEANavigation() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify that the " + self.entryNameQuiz + "'s Quiz Questions can be navigated inside the KEA Page")  
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: Entry Page has been successfully verified for " + self.typeTest)
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