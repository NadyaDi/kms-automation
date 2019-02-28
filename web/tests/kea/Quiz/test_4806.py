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
    # Test Name :  Quiz - Details Section - Download functionality - Anonymous User in KMS
    # Test description:
    # Verify that the Allow Download of Questions List option has proper functionality by downloading the PDF file with Anonymous User
    #================================================================================================================================
    testNum = "4806"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    entryUrl = ''
    userName = 'python_automation'
    
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']   
    dictQuestions = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3} 

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
            self.entryName                  = clsTestService.addGuidToString("Quiz Details - Download functionality Anonymous KMS", self.testNum)
            self.entryNameQuiz              = clsTestService.addGuidToString("QuizDetails", self.testNum)
            self.filePathDownloaded         = localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD + '/' + self.entryNameQuiz + ".pdf"
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

            self.entryUrl = self.common.base.driver.current_url
            
            writeToLog("INFO","Step 3: Going to publish the " + self.entryNameQuiz +" entry as unlisted ")
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate(self.entryNameQuiz, enums.ChannelPrivacyType.UNLISTED, alreadyPublished=False, publishFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO", "Step 4: FAILED to publish the " + self.entryNameQuiz + " entry as unlisted")
                return
             
            writeToLog("INFO","Step 4: Going to log out from the " + self.userName + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to log out from the " + self.userName + " account")   
                return  
            
            self.common.base.navigate(self.entryUrl)
            sleep(2)
            
            writeToLog("INFO","Step 5: Going to verify that the PDF can be downloaded while using an Anonymous User")
            if self.common.player.downloadQuizPDF(self.filePathDownloaded) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to download the PDF file, while using an Anonymous User")
                return
                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: The download option for the Allow Download of Questions List option has proper functionality for Anonymous User")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.entryNameQuiz])
            self.common.deleteFolder(localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')