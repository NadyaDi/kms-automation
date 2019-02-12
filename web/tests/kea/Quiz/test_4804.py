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
    # Test Name : Quiz - Submitted Quiz in Channel with Normal User
    # Test description:
    # Verify that a normal KMS user can answer to all 'Multiple Choice', 'True and False' and watching the 'Reflection Point' question types from Channel
    # We verify that the selected answer remained selected after refreshing the page
    # We verify that no Quiz Question remained unanswered
    # We verify that the 'Submitted Screen' is properly displayed with the expected score, 'Why' and included answer states
    #================================================================================================================================
    testNum = "4804"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description   = "Description" 
    tags          = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    typeTest      = 'New Quiz Entry State with KMS User in Channel'
    channelPublish = 'KMS AUTOMATION - KEA'
    
    mediaOwner     = 'python_automation'
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
            self.entryName       = clsTestService.addGuidToString("Quiz - Question New KMS User in Channel", self.testNum)
            self.newEntryName    = clsTestService.addGuidToString("Quiz - Question New KMS User in Channel - Quiz", self.testNum)
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
            if self.common.kea.quizCreation(self.entryName, self.questionDict, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
            else:
                i = i + 1
                 
            writeToLog("INFO","Step " + str(i) + ": Going to publish the " + self.newEntryName + " entry in a channel")
            if self.common.myMedia.publishSingleEntry(self.newEntryName, '', self.channelPublish, publishFrom = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Step " + str(i) + ": FAILED to publish the " + self.newEntryName + "  entry in a channel")
                return
            else:
                i = i + 1
                
            writeToLog("INFO","Step " + str(i) + ": Going to log out from the " + self.mediaOwner + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from the " + self.mediaOwner + " account")   
                return
            else:
                i = i + 1
            
            writeToLog("INFO","Step " + str(i) + ": Going to authenticate using " + self.newUserName + " account")  
            if self.common.login.loginToKMS(self.newUserName, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from the " + self.newUserName + " account")   
                return
            else:
                i = i + 1

            writeToLog("INFO","Step " + str(i) + ": Going to navigate to the " + self.channelPublish + " channel, and access the " + self.newEntryName + " entry")          
            if self.common.channel.navigateToEntryFromChannel(self.channelPublish, self.newEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to the " + self.channelPublish + " channel, access to the " + self.newEntryName + " entry")
                return
            else:
                i = i + 1 
                    
            writeToLog("INFO","Step " + str(i) + ": Going to answer to all the Quiz Questions from the " + self.newEntryName + " entry")  
            if self.common.player.answerQuiz(self.answersDict, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='') == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to answer to all the Quiz Questions from the " + self.newEntryName + " entry")  
                return  
            else:
                i = i + 1            
                 
            writeToLog("INFO","Step " + str(i) + ": Going to resume from the beginning the " + self.newEntryName + " entry")  
            if self.common.player.resumeFromBeginningQuiz(enums.Location.ENTRY_PAGE, timeOut=1, forceResume=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to resume from the beginning the " + self.newEntryName + " entry")
                return  
            else:
                i = i + 1
            
            writeToLog("INFO","Step " + str(i) + ": Going to verify that all the available quiz questions from the " + self.newEntryName + " entry remained answered")  
            if self.common.player.quizVerification(self.questionDict, self.expectedQuizStateNew, submittedQuiz=True, resumeQuiz=False, newQuiz=False, expectedQuizScore=str(100), location=enums.Location.ENTRY_PAGE, timeOut=60) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to verify that all the available quiz questions from the " + self.newEntryName + " entry remained answered")
                return  
            else:
                i = i + 1

            self.common.base.switch_to_default_content()               
            writeToLog("INFO","Step " + str(i) + ": Going to log out from the " + self.newUserName + " account")  
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from the " + self.newUserName + " account")   
                return
            else:
                i = i + 1
            
            writeToLog("INFO","Step " + str(i) + ": Going to authenticate using " + self.mediaOwner + " account, in order to teardown")  
            if self.common.login.loginToKMS(self.mediaOwner, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to log out from the " + self.mediaOwner + " account, in order to teardown")   
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
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.newEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')