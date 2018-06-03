import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from enum import *
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *


class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # Test description:
    # Check that quiz entry that was just played displayed in recently watched in home page
    # The test's Flow: 
    # Login to KMS-> Upload video entry-> Go to add new quiz -> Open KEA -> Create new quiz -> Go to My History -> Check that quiz entry isn't displayed ->
    # Play entry -> Go to My History page and make sure that entry exists in page Go to home page and make sure entry displayed in recently watched list-> 
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2757"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName= None
    entryNameQuiz = None
    questionNumber = 1
    entryDescription = "description"
    entryTags = "tag1,"
    playlist = 'Recently Watched '
    QuizQuestion1 = 'First question'
    QuizQuestion1Answer1 = 'First answer'
    QuizQuestion1AdditionalAnswers = ['Second answer', 'Third question', 'Fourth question']
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10sec_QR_mid_right.mp4'
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)      
            ########################################################################
            self.entryName = clsTestService.addGuidToString('MyHistoryRecentlyWatchedAudio', self.testNum)
            ########################## TEST STEPS - MAIN FLOW ####################### 
            self.entryName = clsTestService.addGuidToString('MyHistoryQuizEntry')
            self.entryNameQuiz = self.entryName + " - Quiz"
            self.entriesNames = [self.entryName, self.entryNameQuiz]
            ######################### TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload video entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload video entry")
                return
                  
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(navigateFrom = enums.Location.UPLOAD_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return           
                  
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return
                         
            writeToLog("INFO","Step 4: Going to navigate to add new video quiz")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to click video quiz")
                return  
              
            writeToLog("INFO","Step 5: Going to search the uploaded entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryName, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to find entry and open KEA")
                return  
              
            writeToLog("INFO","Step 6: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to start quiz and add questions")
                return   
              
            writeToLog("INFO","Step 7: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to save quiz and navigate to media page")
                return 
              
            writeToLog("INFO","Step 8: Going to Search quiz entry in My History page")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryNameQuiz) == True:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED - New entry is displayed in my history page")
                return       
            writeToLog("INFO","Step 8: Previous Step Failed as Expected - The entry should not be displayed") 
            
            writeToLog("INFO","Step 9: Going to play entry")
            if self.common.player.navigateToQuizEntryAndClickPlay(self.entryNameQuiz, self.questionNumber) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to navigate and play entry")
                return  
            
            writeToLog("INFO","Step 10: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to switch to default content")
                return  
            
            writeToLog("INFO","Step 11: Going to navigate to my history and check for entry")
            if self.common.myHistory.waitTillLocatorExistsInMyHistory(self.entryNameQuiz) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED find entry in my history")
                return   
            sleep(5)
            writeToLog("INFO","Step 12: Going to navigate to home page and check entry in recently watched list")
            if self.common.home.checkEntryInHomePlaylist(self.playlist, self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to find entry in recently watched list")
                return               
            #########################################################################
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')
