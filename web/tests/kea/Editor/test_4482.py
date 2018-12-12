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
    #  @Author: Tzachi Guetta
    # Test Name : Trimming a Quiz entry
    # Test description:
    # 
    #================================================================================================================================
    testNum = "4482"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    description = "Description" 
    tags = "Tags,"
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    questionNumber1 = ['00:05', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Question #1', 'Why Question #1'] 
    questionNumber2 = ['00:10', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4', 'Hint Question #2', 'Why Question #2'] 
    questionNumber3 = ['00:15', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4', 'Hint Question #3', 'Why Question #3'] 
    questionNumber4 = ['00:20', enums.QuizQuestionType.Multiple, 'question #4 Title', 'question #4 option #1', 'question #4 option #2', 'question #4 option #3', 'question #4 option #4', 'Hint Question #4', 'Why Question #4'] 
    questionNumber5 = ['00:25', enums.QuizQuestionType.Multiple, 'question #5 Title', 'question #5 option #1', 'question #5 option #2', 'question #5 option #3', 'question #5 option #4', 'Hint Question #5', 'Why Question #5']   
    
    dictQuestions = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3,'4':questionNumber4,'5':questionNumber5}            
#     dictQuestions = [('1',questionNumber1),('2',questionNumber2),('3',questionNumber3),('4',questionNumber4),('5',questionNumber5)]
    
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
            self.videoEntryName = clsTestService.addGuidToString("Upload media - Video", self.testNum)
            expectedEntryDuration = "00:20"
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to upload entry - to be trimmed")  
            if self.common.upload.uploadEntry(self.filePathVideo, self.videoEntryName, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to add Quiz")  
            if self.common.kea.quizCreation(self.videoEntryName, self.dictQuestions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to add Quiz")
                return  
                      
            writeToLog("INFO","Step 2: Going to trim the entry from 30sec to 20sec")  
            if self.common.kea.trimEntry(self.videoEntryName, "00:10", "00:20", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to trim the entry from 30sec to 20sec")
                return
 
            writeToLog("INFO","Step 3: Going to collect the new entry's QR codes")  
            self.QRlist = self.common.player.collectQrTimestampsFromPlayer(self.videoEntryName)
            if  self.QRlist == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to collect the new entry's QR codes")
                return
             
            self.isExist = ["5", "7", "22", "28"];
            self.isAbsent = ["12", "13", "15", "17"];
            writeToLog("INFO","Step 4: Going to verify the entry duration (using QR codes)")  
            if self.common.player.compareQRlists(self.QRlist, self.isExist, self.isAbsent) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify the entry duration (using QR codes)")
                return        
                 
            writeToLog("INFO","TEST PASSED")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia(self.videoEntryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')