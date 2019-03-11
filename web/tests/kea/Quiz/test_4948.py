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
    # Test Name : Quiz - Secure Embed OFF - Answer Quiz with Anonymous and then with KMS user
    # Test description:
    # Verify that the user is able to resume a submitted quiz entry after answering to the 'Multiple Choice', 'True and False' and watching the 'Reflection Point' question types
    # Verify that the secure embed off quiz entry has the same functionality and behavior like in KMS
    # We verify that the selected answer are resumed as being unanswered after refreshing the page
    # We verify that no Quiz Question remained answered
    # We verify that the 'Submitted Screen' is properly displayed with the expected score, 'Why' and included answer states
    # Verify that the Anonymous user is able to submit a quiz and that then a KMS user is able to start a new quiz from zero to the end
    #================================================================================================================================
    testNum = "4948"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description   = "Description" 
    tags          = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    typeTest      = 'Embeded Quiz Entry Submitted State with 100% score with Anonymous User and KMS User'
    
    # this variables are used in order to take the embed link, embed file, embed link
    instanceUrl = None
    embedLink = None
    embedLinkFilePath = localSettings.LOCAL_SETTINGS_LINUX_EMBED_SHARED_FOLDER
    embedUrl = localSettings.LOCAL_SETTINGS_APACHE_EMBED_PATH
            
    # Each list is used in order to create a different Quiz Question Type
    questionMultiple         = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalse     = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflection       = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']
    
    # Each list is used in order to verify that the quiz question types are unanswered
    questionAnswerOne        = ['Question Title for Multiple Choice', '', False]
    questionAnswerTwo        = ['Question Title for True and False', '', False]
    questionAnswerThree      = ['Question Title for Reflection Point', '', False]
    
    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizStateNew     = {'1':questionAnswerOne,'2':questionAnswerTwo, '3':questionAnswerThree} 
    

    # Each list is used in order to verify that all the Quiz Question types are answered
    questionAnswerOneSubmitted        = ['Question Title for Multiple Choice', 'question #1 option #1', True]
    questionAnswerTwoSubmitted        = ['Question Title for True and False', 'True text', True]
    questionAnswerThreeSubmitted      = ['Question Title for Reflection Point', '', True]
    
    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizStateSubmitted = {'1':questionAnswerOneSubmitted,'2':questionAnswerTwoSubmitted, '3':questionAnswerThreeSubmitted} 


    # This Dictionary is used in order to create all the Quiz Question types within a single call
    questionDict             = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection}
    
    # This values are used in order to find and answer to the quiz questions
    questionName1            = "Question Title for Multiple Choice"
    answerText1              = "question #1 option #1"
    
    questionName2            = "Question Title for True and False"
    answerText2              = "True text"
        
    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be present in the Question Name
    answersDict = {questionName1:answerText1,
                   questionName2:answerText2} 
    
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
            self.entryName       = clsTestService.addGuidToString("Quiz - Secure Embed OFF - Submitted with Anonymous and KMS User", self.testNum)
            self.newEntryName    = clsTestService.addGuidToString("Quiz - Secure Embed OFF - Submitted with Anonymous and KMS User - Quiz", self.testNum)
            self.embedLinkFilePath = self.embedLinkFilePath + clsTestService.addGuidToString('embed.html', self.testNum)
            self.embedUrl = self.embedUrl + clsTestService.addGuidToString('embed.html', self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            i = 1
            self.instanceUrl = self.common.base.driver.current_url
  
            writeToLog("INFO","Step " + str(i) + ": Going to turn off the secureEmbed in admin panel")
            if self.common.admin.enableSecureEmbed(False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to turn off the secureEmbed in admin panel")
                return                
              
            self.common.base.navigate(self.instanceUrl)
            writeToLog("INFO","Step " + str(i) + ": Going to create a new entry, " + self.entryName)  
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new entry, " + self.entryName)  
                return
            else:
                i = i + 1
                                                
            writeToLog("INFO","Step " + str(i) + ": Going to create a new Quiz for the " + self.entryName + " entry")  
            if self.common.kea.quizCreation(self.entryName, self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
            else:
                i = i + 1
                 
            self.embedLink = self.common.entryPage.getEmbedLink()  
            writeToLog("INFO","Step " + str(i) + ": Going to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")   
                return
            else:
                i = i + 1
  
            writeToLog("INFO","Step " + str(i) + ": Going to write the " + self.newEntryName  + " embed code in a file")
            if self.common.writeToFile(self.embedLinkFilePath, self.embedLink) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to write the " + self.newEntryName  + " embed code in a file")
                return
            else:
                i = i + 1                
               
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to embed entry page ( by link )")
                return
            else:
                i = i + 1 
                    
            writeToLog("INFO","Step " + str(i) + ": Going to answer to all the Quiz Questions from the " + self.newEntryName + " entry as Anonymous user")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='', embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer to all the Quiz Questions from the " + self.newEntryName + " entry as Anonymous user")  
                return  
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to verify that " + self.newEntryName + "'s entry submitted screen is properly displayed")  
            if self.common.player.verifySubmittedScreen(str(100), enums.Location.ENTRY_PAGE, self.questionDict, self.expectedQuizStateSubmitted, 5, embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that " + self.newEntryName + "'s entry submitted screen is properly displayed") 
                return  
            else:
                i = i + 1
                
            self.common.base.navigate(self.instanceUrl) 
            writeToLog("INFO","Step " + str(i) + ": Going to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")
            if self.common.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) == False:
                writeToLog("INFO", "Step " + str(i) + ":FAILED to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")
                return
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to embed entry page ( by link )")
                return
            else:
                i = i + 1 
                
            writeToLog("INFO","Step " + str(i) + ": Going to answer to all the Quiz Questions from the " + self.newEntryName + " entry as KMS user")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='', embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer to all the Quiz Questions from the " + self.newEntryName + " entry as KMS user")  
                return  
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to verify that " + self.newEntryName + "'s entry submitted screen is properly displayed")  
            if self.common.player.verifySubmittedScreen(str(100), enums.Location.ENTRY_PAGE, self.questionDict, self.expectedQuizStateSubmitted, 5, embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that " + self.newEntryName + "'s entry submitted screen is properly displayed") 
                return  
            else:
                i = i + 1                    
            ##################################################################
            writeToLog("INFO","TEST PASSED: Entry Page has been successfully verified for a " + self.typeTest)
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.base.navigate(self.instanceUrl) 
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.newEntryName])
            self.common.deleteFile(self.embedLinkFilePath)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')