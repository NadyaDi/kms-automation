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
    # Test Name : Quiz Experience section in KEA Entry Page - Disabled
    # Test description:
    # Verify that all the KEA Quiz Experience options have proper functionality by:
    # Verifying that the "Allow answers change", "Allow skip", "Do not Allow Skip" and "No seeking forward" can be Disabled 
    # Verify that the option status is reflected in the Entry Page
    #================================================================================================================================
    testNum = "4772"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    
    #this list and dictionary is used in order to create a multiple quiz entry
    questionNumber1 = ['00:10', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4']
    questionNumber2 = ['00:15', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4']
    questionNumber3 = ['00:20', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']
    dictQuestions   = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3}
    
    #this variables are used in order to verify and answer/replace to quiz questions
    questionName1   = "question #1 Title"
    answerText1     = "question #1 option #1"
    replaceAnswer1  = "question #1 option #2"

    questionName2   = "question #2 Title"
    answerText2     = "question #2 option #1"
    replaceAnswer2  = "question #2 option #2"

    questionName3   = "question #3 Title"
    answerText3     = "question #3 option #1"
    replaceAnswer3  = "question #3 option #2"
    
    #this variable is used in order to navigate to the Quiz entry while using a guest account
    entryUrl = ''

    #this dictionaries is used in order to answer to the Quiz Questions
    #questionName is the question title
    #answerText is the answer that should be present in the Question Name
    questionDict = {questionName1:answerText1,
                    questionName2:answerText2,
                    questionName3:answerText3} 
    
    #this dictionary is used in order to select a new user
    replaceAnswersDict = {questionName1:replaceAnswer1,
                    questionName2:replaceAnswer2,
                    questionName3:replaceAnswer3} 
    
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
            self.entryName                          = clsTestService.addGuidToString("Quiz - Experience Disabled", self.testNum)
            self.newEntryName                       = clsTestService.addGuidToString("Quiz - Experience Disabled - Quiz", self.testNum)
            # this dictionary is used in order to edit the options           
            self.allowAnswerChangeDisabled          = {enums.KEAQuizOptions.ALLOW_ANSWER_CHANGE:False}
            self.allowSkipDisabled                  = {enums.KEAQuizOptions.ALLOW_SKIP:False}
            self.doNotAllowSkipDisabled             = {enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP:False}
            self.noSeekingForwardDisabled           = {enums.KEAQuizOptions.NO_SEEKING_FORWARD:False}
 
            # this dictionary is used in order to verify the options
            self.allowAnswerChangeDisabledList      = [enums.KEAQuizOptions.ALLOW_ANSWER_CHANGE, self.replaceAnswersDict, self.allowAnswerChangeDisabled]
            self.allowSkipDisabledList              = [enums.KEAQuizOptions.ALLOW_SKIP, '', self.allowSkipDisabled]
            self.doNotAllowSkipDisabledList         = [enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP, '', self.doNotAllowSkipDisabled]
            self.noSeekingForwardDisabledList       = [enums.KEAQuizOptions.NO_SEEKING_FORWARD, 5, self.noSeekingForwardDisabled]
            
            self.experienceOptionDisableList        = [self.allowAnswerChangeDisabledList, self.allowSkipDisabledList, self.doNotAllowSkipDisabledList, self.noSeekingForwardDisabledList]
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
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions, timeout=35) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new Quiz for the " + self.entryName + " entry")  
                return  
            else:
                i = i + 1
            
            #going to take the entry url in order to navigate to it while using a guest account
            self.entryUrl = self.common.base.driver.current_url
            writeToLog("INFO","Step " + str(i) + ": Going to publish the " + self.entryName +" entry as unlisted ")  
            if self.common.myMedia.publishSingleEntryToUnlistedOrPrivate(self.newEntryName, enums.ChannelPrivacyType.UNLISTED, alreadyPublished=False, publishFrom=enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step " + str(i) + ": FAILED to publish the " + self.entryName + " entry as unlisted")
                return
            else: 
                i = i + 1
 
            for option in self.experienceOptionDisableList:
                self.common.base.navigate(self.entryUrl)
                writeToLog("INFO","Step " + str(i) + ": Going to navigate to KEA Quiz tab for " + self.newEntryName)  
                if self.common.kea.initiateQuizFlow(self.newEntryName, navigateToEntry=True, timeOut=1) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to KEA Quiz tab for " + self.newEntryName)  
                    return 
                else:
                    i = i + 1
                    
                writeToLog("INFO","Step " + str(i) + ": Going to revert to default all the " + enums.KEAQuizSection.EXPERIENCE.value + " changes")  
                if self.common.kea.revertToDefaultInKEA(enums.KEAQuizSection.EXPERIENCE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to revert to default all the " + enums.KEAQuizSection.EXPERIENCE.value + " changes")  
                    return
                else:
                    i = i + 1
                    
                writeToLog("INFO","Step " + str(i) + ": Going to save the changes from the revert to default option and resume editing")  
                if self.common.kea.saveKeaChanges(resumeEditing=True) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to save the changes from the revert to default option and resume editing")    
                    return
                else:
                    i = i + 1
                
                writeToLog("INFO","Step " + str(i) + ": Going to change the " + enums.KEAQuizSection.EXPERIENCE.value + " option by disabling the " + option[0].value)  
                if self.common.kea.editQuizOptions(enums.KEAQuizSection.EXPERIENCE, option[2], saveChanges=True) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to change the " + enums.KEAQuizSection.EXPERIENCE.value + " option by disabling the " + option[0].value)   
                    return
                else:
                    i = i + 1
                   
                self.common.base.switch_to_default_content() 
                writeToLog("INFO","Step " + str(i) + ": Going to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")  
                if self.common.login.logOutOfKMS() == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to log out from the " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")   
                    return
                else:
                    i = i + 1
                  
                self.common.base.navigate(self.entryUrl)
                sleep(2)
                if option == self.allowAnswerChangeDisabledList: 
                    writeToLog("INFO","Step " + str(i) + ": Going to answer to all of the available Quiz while using a Guest account")  
                    if self.common.player.answerQuiz(self.questionDict, skipWelcomeScreen=True, submitQuiz=False, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='') == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to answer to all of the available Quiz while using a Guest account")
                        return                  
                    else:
                        i = i + 1
                
                elif option == self.noSeekingForwardDisabledList:
                    if self.common.player.initiateQuizPlayback() == False:
                        return
                     
                writeToLog("INFO","Step " + str(i) + ": Going to verify the KEA Section " + enums.KEAQuizSection.EXPERIENCE.value + " changes for " +next(iter(option)).value + " that are properly displayed in the " + self.newEntryName + " entry page") 
                if self.common.entryPage.verifyQuizOptionsInEntryPage(enums.KEAQuizSection.EXPERIENCE, option[0], option[1], keaOptionEnabled=False, navigateToEntryPageFromKEA=False, entryName=self.newEntryName) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to verify the KEA Section" + enums.KEAQuizSection.EXPERIENCE.value + " changes for " + next(iter(option)).value + " that are properly displayed in the " + self.newEntryName + " entry page") 
                    return
                else:
                    i = i + 1   
                          
                writeToLog("INFO","Step " + str(i) + ": Going to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")       
                if self.common.login.loginToKMS(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) == False:
                    writeToLog("INFO", "Step " + str(i) + ":FAILED to authenticate using " + localSettings.LOCAL_SETTINGS_LOGIN_USERNAME + " account")  
                    return False  
                else:
                    i = i + 1 
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the KEA Experience options were properly disabled and verified in KEA Entry Page")
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