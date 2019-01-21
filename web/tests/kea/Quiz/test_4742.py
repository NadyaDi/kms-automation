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
    # Test Name : KEA - Quiz Details section in KEA Editor
    # Test description:
    # Verify that all the KEA Quiz Details options have proper functionality by:
    # Verifying that the quiz name can be changed
    # Verifying that the welcome message, allow download and instructions can be enabled and disabled
    # Verify that the "Revert to default" option has functionality
    #================================================================================================================================
    testNum = "4742"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
        
    newWelcomeMessage  = "This is a complete new Welcome Message, enjoy!"
    welcomeMessageText = "In this video, you will be given a Quiz. Good Luck!"
    allowMessageText   = "Pre-test Available"
    instructionsText   = "All questions must be answered. The quiz will be submitted at the end."
    
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
            self.entryName          = clsTestService.addGuidToString("KEA Quiz - Details Options Quiz", self.testNum)
            self.newEntryName       = clsTestService.addGuidToString("KEA Quiz - Modified Options Quiz", self.testNum)
            
            self.changeEntryName                 = {enums.KEAQuizOptions.QUIZ_NAME:self.newEntryName}
            self.changeWelcomeMessage            = {enums.KEAQuizOptions.SHOW_WELCOME_PAGE:self.newWelcomeMessage}
            
            self.welcomeMessageEnabled           = {enums.KEAQuizOptions.SHOW_WELCOME_PAGE:True}
            self.allowDownloadEnabled            = {enums.KEAQuizOptions.ALLOW_DOWNLOAD:True}
            self.instructionsEnabled             = {enums.KEAQuizOptions.INSTRUCTIONS:True}
            
            self.welcomeMessageDisabled          = {enums.KEAQuizOptions.SHOW_WELCOME_PAGE:False}
            self.allowDownloadDisabled           = {enums.KEAQuizOptions.ALLOW_DOWNLOAD:False}
            self.instructionsDisabled            = {enums.KEAQuizOptions.INSTRUCTIONS:False}
            
            self.welcomeMessagePreview           = {enums.KEAQuizOptions.SHOW_WELCOME_PAGE:self.welcomeMessageText}
            self.allowDownloadPreview            = {enums.KEAQuizOptions.ALLOW_DOWNLOAD:self.allowMessageText}
            self.instructionsPreview             = {enums.KEAQuizOptions.INSTRUCTIONS:self.instructionsText}


            self.keaDetailsInputList             = [self.changeEntryName, self.changeWelcomeMessage]
            self.keaDetailsBooleanTrue           = [self.welcomeMessageEnabled, self.allowDownloadEnabled, self.instructionsEnabled]
            self.keaDetailsBooleanFalse          = [self.welcomeMessageDisabled, self.allowDownloadDisabled, self.instructionsDisabled]
            
            self.keaAllDetailsOptionsList        = [self.keaDetailsInputList, self.keaDetailsBooleanTrue, self.keaDetailsBooleanFalse]
            self.keaPreviewElementsList          = [self.welcomeMessagePreview, self.allowDownloadPreview, self.instructionsPreview]
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
            
            for option in self.keaAllDetailsOptionsList:
                optionNumber = 0
                while len(option) != optionNumber:
                    writeToLog("INFO","Step " + str(i) + ": Going to edit the " + enums.KEAQuizSection.DETAILS.value + " section by modifying the " + next(iter(option[optionNumber])).value)  
                    if self.common.kea.editQuizOptions(enums.KEAQuizSection.DETAILS, option[optionNumber]) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to edit the " + enums.KEAQuizSection.DETAILS.value + " section by modifying the " + next(iter(option[optionNumber])).value)
                        return
                    else:
                        i = i + 1
                     
                    writeToLog("INFO","Step " + str(i) + ": Going to verify the " + enums.KEAQuizSection.DETAILS.value + " section by " + next(iter(option[optionNumber])).value)  
                    if self.common.kea.verifyQuizOptionsInKEA(enums.KEAQuizSection.DETAILS, option[optionNumber]) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to verify the " + enums.KEAQuizSection.DETAILS.value + " section by " + next(iter(option[optionNumber])).value)
                        return 
                    else:
                        i = i + 1
                    
                    writeToLog("INFO","Step " + str(i) + ": Going to revert to default all the " + enums.KEAQuizSection.DETAILS.value + " changes")  
                    if self.common.kea.revertToDefaultInKEA(enums.KEAQuizSection.DETAILS) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to revert to default all the " + enums.KEAQuizSection.DETAILS.value + " changes")  
                        return
                    else:
                        i = i + 1
                        optionNumber = optionNumber + 1
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the KEA Details options were properly edited and verified in KEA PAGE")
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