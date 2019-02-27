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
    # Test Name : Quiz - Secure Embed ON - Published Entry in Private Channel with KMS user
    # Test description:
    # Verify that the user is able to resume a submitted quiz entry after answering to the 'Multiple Choice', 'True and False' and watching the 'Reflection Point' question types
    # Verify that the entry can be accessed while being published in a Private Channel
    # Verify that the secure embed ON quiz entry has the same functionality and behavior like in KMS
    # We verify that the selected answer are resumed as being answered after refreshing the page
    # We verify that no Quiz Question remained unanswered
    # We verify that the 'Submitted Screen' is properly displayed with the expected score, 'Why' and included answer states
    #================================================================================================================================
    testNum = "4853"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description   = "Description" 
    tags          = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    typeTest      = 'Submitted Entry Quiz published in Private Channel with KMS user'
    
    # this variables are used in order to take the embed link, embed file, embed link
    instanceUrl = None
    embedLink = None
    embedLinkFilePath = localSettings.LOCAL_SETTINGS_LINUX_EMBED_SHARED_FOLDER
    embedUrl = localSettings.LOCAL_SETTINGS_APACHE_EMBED_PATH
    
    channelPublish = 'KMS AUTOMATION - PRIVATE'
    newUserName    = 'python_normal'
    newUserPass    = 'Kaltura1!'
            
    # Each list is used in order to create a different Quiz Question Type
    questionMultiple         = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
    questionTrueAndFalse     = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
    questionReflection       = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']
    
    # Each list is used in order to verify that all the Quiz Question types are answered
    questionAnswerOne        = ['Question Title for Multiple Choice', 'question #1 option #1', True]
    questionAnswerTwo        = ['Question Title for True and False', 'True text', True]
    questionAnswerThree      = ['Question Title for Reflection Point', '', True]
    
    # This Dictionary is used in order to verify the state of the answers ( answered / unanswered) from the active question screen
    expectedQuizStateNew     = {'1':questionAnswerOne,'2':questionAnswerTwo, '3':questionAnswerThree} 

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
            self.entryName       = clsTestService.addGuidToString("Quiz - Embeded Entry in Private Channel with KMS User", self.testNum)
            self.newEntryName    = clsTestService.addGuidToString("Quiz - Embeded Entry in Private Channel with KMS User - Quiz", self.testNum)
            self.embedLinkFilePath = self.embedLinkFilePath + clsTestService.addGuidToString('embed.html', self.testNum)
            self.embedUrl = self.embedUrl + clsTestService.addGuidToString('embed.html', self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            i = 1
            self.instanceUrl = self.common.base.driver.current_url
             
            writeToLog("INFO","Step 1: Going to turn ON the secureEmbed in admin panel")
            if self.common.admin.enableSecureEmbedPlaylist(True) == False:
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
            if self.common.kea.quizCreation(self.entryName, self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
            
            sleep(5)
            self.embedLink = self.common.entryPage.getEmbedLink()
                  
            writeToLog("INFO","Step 4: Going to publish the " + self.newEntryName + " entry in " + self.channelPublish + " channel")
            if self.common.myMedia.publishSingleEntry(self.newEntryName, '', self.channelPublish, publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step 4: FAILED to publish the " + self.newEntryName + " entry in " + self.channelPublish + " channel")
                return
                 
            writeToLog("INFO","Step 5: Going to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")   
                return
             
            writeToLog("INFO","Step 6: Going to write the " + self.newEntryName  + " entrie's embed code in a file")
            if self.common.writeToFile(self.embedLinkFilePath, self.embedLink) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to write the " + self.newEntryName  + " entrie's embed code in a file")
                return         
              
            writeToLog("INFO","Step 7: Going to navigate to embed entry page (by link)")
            if self.common.base.navigate(self.embedUrl) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to embed entry page ( by link )")
                return
                
            writeToLog("INFO","Step 8: Going to authenticate using " + self.newUserName + " account")
            if self.common.login.loginToKMSEmbed(self.newUserName, self.newUserPass) == False:
                writeToLog("INFO", "Step 8:FAILED to authenticate using " + self.newUserName + " account")
                return
                    
            writeToLog("INFO","Step 9: Going to answer to all the Quiz Questions from the " + self.newEntryName + " entry")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='', embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to answer to all the Quiz Questions from the " + self.newEntryName + " entry")  
                return            
                 
            writeToLog("INFO","Step 10: Going to resume from the beginning the " + self.newEntryName + " entry")  
            if self.common.player.resumeFromBeginningQuiz(enums.Location.ENTRY_PAGE, timeOut=1, forceResume=True, embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to resume from the beginning the " + self.newEntryName + " entry")
                return  
            
            writeToLog("INFO","Step 11: Going to verify that all the available quiz questions from the " + self.newEntryName + " entry remained answered")  
            if self.common.player.quizVerification(self.questionDict, self.expectedQuizStateNew, submittedQuiz=True, resumeQuiz=False, newQuiz=False, expectedQuizScore=str(100), location=enums.Location.ENTRY_PAGE, timeOut=60, embed=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to verify that all the available quiz questions from the " + self.newEntryName + " entry remained answered")
                return  

            self.common.base.navigate(self.instanceUrl)
            self.common.base.switch_to_default_content()               
            writeToLog("INFO","Step 12: Going to log out from the " + self.newUserName + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to log out from the " + self.newUserName + " account")   
                return

            writeToLog("INFO","Step 13: Going to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account, in order to teardown")  
            if self.common.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account, in order to teardown")   
                return
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
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.newEntryName])
            self.common.deleteFile(self.embedLinkFilePath)
            self.common.admin.enableSecureEmbedPlaylist(False)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')