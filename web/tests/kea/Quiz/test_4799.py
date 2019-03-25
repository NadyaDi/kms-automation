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
    # Test Name : IVQ - Retake quiz Latest score
    # Test description:
    # Go to editor page and create quiz with option to retake quiz - 3 attempts
    # Go to quiz page and verify that user is able to retake quiz 3 times
    #================================================================================================================================
    testNum = "4799"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    questionOpen = ['00:25', enums.QuizQuestionType.OPEN_QUESTION, 'Question Title for Open-Q']
    
    # This Dictionary is used in order to create all the Quiz Question types within a single call
    questionDict = {'1':questionOpen} 
    
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
            self.entryName = clsTestService.addGuidToString("IVQ - Open-Q", self.testNum)
            self.quizEntryName = clsTestService.addGuidToString("IVQ - Open-Q - Quiz", self.testNum)  
            self.questionAnswer = "Answer for open question"    

            self.keaScoreType                    = {enums.KEAQuizOptions.QUIZ_SCORE_TYPE:enums.keaQuizScoreType.FIRST.value}
            self.keaNumberOfAllowedAttempts      = {enums.KEAQuizOptions.SET_NUMBER_OF_ATTEMPTS:4}
            self.keaAllowMultipleScore           = {enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:True}
            
            self.keaScoreOptions                 = [self.keaAllowMultipleScore, self.keaNumberOfAllowedAttempts, self.keaScoreType]
            
            self.keaAllScoreOptionsList          = [self.keaScoreOptions]     
            ######################### TEST STEPS - MAIN FLOW #######################
#             writeToLog("INFO","Step 1: Going to upload entry")    
#             if self.common.upload.uploadEntry(self.filePath, self.entryName, self.description, self.tags) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED to upload entry")
#                 return
#              
#             self.common.base.get_body_element().send_keys(Keys.PAGE_DOWN)
#                                 
#             writeToLog("INFO","Step 2: Going to to navigate to entry page")    
#             if self.common.upload.navigateToEntryPageFromUploadPage(self.entryName) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 2: FAILED to navigate entry page")
#                 return
#                                 
#             writeToLog("INFO","Step 3: Going to to wait until media end upload process")    
#             if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 3: FAILED to wait until media end upload process")
#                 return
#                                                                
            writeToLog("INFO","Step 4 : Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation('timeline.mp4', self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4 : FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return
             
            writeToLog("INFO","Step 5: Going to navigate to KEA Quiz tab for " + self.entryName)  
            if self.common.kea.initiateQuizFlow('timeline.mp4 - Quiz', navigateToEntry=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to KEA Quiz tab for " + self.entryName)  
                return 
             
            i = 6
             
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
            
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to " + self.quizEntryName + " page")  
            if self.common.entryPage.navigateToEntryPageFromMyHistory(self.quizEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to " + self.quizEntryName + " page")
                return   
            
            
            ##################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED: Open-Q is added sucssefully")
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