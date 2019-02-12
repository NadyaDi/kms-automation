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
    # Test Name : Quiz - Entry with all the KEA Quiz Question types - KEA Page
    # Test description:
    # Verifying that all the KEA Quiz Question type can be created in KEA Editor, by:
    # Creating a KEA Quiz Question with 'Multiple Choice' with hint and why
    # Creating a KEA Quiz Question with 'True and False' with hint and why
    # Creating a KEA Quiz Question with 'Reflection Point'
    # Verify that the KEA Quiz questions were properly created within the KEA timeline section
    #================================================================================================================================
    testNum = "4776"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # Each list is used in order to create a different Quiz Question Type
    questionMultiple     = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalse = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True And False']
    questionReflection   = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']

    # This Dictionary is used in order to create all the Quiz Question types within a single call
    dictQuestions        = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection}
    
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
            self.entryName       = clsTestService.addGuidToString("Quiz - Question verification KEA", self.testNum)
            self.newEntryName    = clsTestService.addGuidToString("Quiz - Question verification KEA - Quiz", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            i = 1 
            writeToLog("INFO","Step " + str(i) + ": Going to create a new entry, " + self.entryName)  
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new entry, " + self.entryName)  
                return
            else:
                i = i + 1
                                         
            writeToLog("INFO","Step " + str(i) + ": Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions, timeout=25) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
            else:
                i = i + 1
                 
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to KEA Page for " + self.newEntryName)  
            if self.common.kea.launchKEA(self.newEntryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to KEA Page tab for " + self.newEntryName)  
                return 
            else:
                i = i + 1
              
            sleep(5)   
            writeToLog("INFO","Step " + str(i) + ": Going to verify the quiz questions present in the KEA Timeline for the " + self.newEntryName + " entry")  
            if self.common.kea.keaTimelineVerification(self.dictQuestions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify the quiz questions present in the KEA Timeline for the " + self.newEntryName + " entry")
                return  
            else:
                i = i + 1
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the KEA Quiz Question types were successfully created and verified within the KEA Page")
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.newEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')