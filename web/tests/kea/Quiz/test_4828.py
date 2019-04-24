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
    # Test Name : Quiz - Secure Embed ON - Download functionality - KMS User
    # Test description:
    # Verify that the Allow Download of Questions List option has proper functionality by downloading the PDF file with Anonymous User
    # Verify that the download option has proper functionality in embed
    #================================================================================================================================
    testNum = "4828"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    # this variables are used in order to take the embed link, embed file, embed link
    instanceUrl = None
    embedLink = None
    embedLinkFilePath = localSettings.LOCAL_SETTINGS_LINUX_EMBED_SHARED_FOLDER
    embedUrl = localSettings.LOCAL_SETTINGS_APACHE_EMBED_PATH
    
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4'] 
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4'] 
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']   
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3} 

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
            self.entryName                  = clsTestService.addGuidToString("Quiz Download", self.testNum)
            self.entryNameQuiz              = clsTestService.addGuidToString("Quiz Download - Quiz", self.testNum)
            self.filePathDownloaded         = localSettings.LOCAL_SETTINGS_JENKINS_NODE_SHARED_DOWNLOAD + '/' + self.entryNameQuiz + ".pdf"
            self.embedLinkFilePath = self.embedLinkFilePath + clsTestService.addGuidToString('embed.html', self.testNum)
            self.embedUrl = self.embedUrl + clsTestService.addGuidToString('embed.html', self.testNum)
            ##################### TEST STEPS - MAIN FLOW #####################
            self.instanceUrl = self.common.base.driver.current_url
  
            writeToLog("INFO","Step 1: Going to turn ON the secureEmbed in admin panel")
            if self.common.admin.enableSecureEmbed(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to turn ON the secureEmbed in admin panel")
                return                
              
            self.common.base.navigate(self.instanceUrl)
            
            writeToLog("INFO","Step 2: Going to create a new entry, " + self.entryName)  
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to create a new entry, " + self.entryName)  
                return
                  
            writeToLog("INFO","Step 3: Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return

            self.embedLink = self.common.entryPage.getEmbedLink()
                  
            writeToLog("INFO","Step 4: Going to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")   
                return
  
            writeToLog("INFO","Step 5: Going to write the " + self.entryNameQuiz  + " embed code in a file")
            if self.common.writeToFile(self.embedLinkFilePath, self.embedLink) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to write the " + self.entryNameQuiz  + " embed code in a file")
                return

            writeToLog("INFO","Step 6: Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to navigate to embed entry page ( by link )")
                return
            
            writeToLog("INFO","Step 7: Going to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account, in order to verify secure embed ON")
            if self.common.login.loginToKMSEmbed(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) == False:
                writeToLog("INFO", "Step 7:FAILED to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account, in order to verify secure embed ON")
                return
            
            writeToLog("INFO","Step 8: Going to verify that the PDF can be downloaded while using an Anonymous User")
            if self.common.player.downloadQuizPDF(self.filePathDownloaded, embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to download the PDF file, while using an Anonymous User")
                return
            
            self.common.base.navigate(self.instanceUrl)           
            ##################################################################
            writeToLog("INFO","TEST PASSED: The download option for the Allow Download of Questions List option has proper functionality for KMS User with embedSecure on")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.entryNameQuiz])
            self.common.deleteFile(self.embedLinkFilePath)
            self.common.admin.enableSecureEmbed(False)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')