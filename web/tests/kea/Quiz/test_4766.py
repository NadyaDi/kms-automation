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
    # Test Name : Quiz Experience section in KEA Editor
    # Test description:
    # Verify that all the KEA Quiz Experience options have proper functionality by:
    # Verifying that the "Allow answers change", "Allow skip", "Do not Allow Skip" and "No seeking forward" can be enabled and disabled
    # Verify that the "Revert to default" option has functionality
    #================================================================================================================================
    testNum = "4766"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
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
            self.entryName                       = clsTestService.addGuidToString("Quiz - Experience in KEA", self.testNum)
            self.newEntryName                    = clsTestService.addGuidToString("Quiz - Experience in KEA - Quiz", self.testNum)
                         
            self.allowAnswerChangeEnabled        = {enums.KEAQuizOptions.ALLOW_ANSWER_CHANGE:True}
            self.allowSkipEnabled                = {enums.KEAQuizOptions.ALLOW_SKIP:True}
            self.doNotAllowSkipEnabled           = {enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP:True}
            self.noSeekingForwardEnabled         = {enums.KEAQuizOptions.NO_SEEKING_FORWARD:True}
            
            self.allowAnswerChangeDisabled       = {enums.KEAQuizOptions.ALLOW_ANSWER_CHANGE:False}
            self.allowSkipDisabled               = {enums.KEAQuizOptions.ALLOW_SKIP:False}
            self.doNotAllowSkipDisabled          = {enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP:False}
            self.noSeekingForwardDisabled        = {enums.KEAQuizOptions.NO_SEEKING_FORWARD:False}
            
            self.keaExperienceBooleanTrue        = [self.allowAnswerChangeEnabled, self.allowSkipEnabled, self.doNotAllowSkipEnabled, self.noSeekingForwardEnabled]
            self.keaExperienceBooleanFalse       = [self.allowAnswerChangeDisabled, self.allowSkipDisabled, self.doNotAllowSkipDisabled, self.noSeekingForwardDisabled]
            
            self.keaAllExperienceOptionsList     = [self.keaExperienceBooleanTrue, self.keaExperienceBooleanFalse]
            ##################### TEST STEPS - MAIN FLOW ##################### 
            i = 1 
            writeToLog("INFO","Step " + str(i) + ": Going to create a new entry, " + self.entryName)  
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to create a new entry, " + self.entryName)  
                return
            else:
                i = i + 1
                             
            writeToLog("INFO","Step " + str(i) + ": Going to navigate to KEA Quiz tab for " + self.entryName)  
            if self.common.kea.initiateQuizFlow(self.entryName, navigateToEntry=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step " + str(i) + ": FAILED to navigate to KEA Quiz tab for " + self.entryName)  
                return 
            else:
                i = i + 1
            
            for option in self.keaAllExperienceOptionsList:
                optionNumber = 0
                while len(option) != optionNumber:
                    writeToLog("INFO","Step " + str(i) + ": Going to edit the " + enums.KEAQuizSection.EXPERIENCE.value + " section by modifying the " + next(iter(option[optionNumber])).value)  
                    if self.common.kea.editQuizOptions(enums.KEAQuizSection.EXPERIENCE, option[optionNumber]) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to edit the " + enums.KEAQuizSection.EXPERIENCE.value + " section by modifying the " + next(iter(option[optionNumber])).value)
                        return
                    else:
                        i = i + 1
                     
                    writeToLog("INFO","Step " + str(i) + ": Going to verify the " + enums.KEAQuizSection.EXPERIENCE.value + " section by " + next(iter(option[optionNumber])).value)  
                    if self.common.kea.verifyQuizOptionsInKEA(enums.KEAQuizSection.EXPERIENCE, option[optionNumber]) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to verify the " + enums.KEAQuizSection.EXPERIENCE.value + " section by " + next(iter(option[optionNumber])).value)
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
                        optionNumber = optionNumber + 1
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the KEA Experience options were properly enabled and disabled in KEA PAGE")
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