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
    #  @Author: Michal Zomper
    # Test description:

    #================================================================================================================================
    testNum = "665"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entryName5 = None
    entryDescription1 = "different description"
    entryDescription = "Description"
    entryTags = "Tags,"
    entryTags1 = "different Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    numberOfEntriesToUpload = 4
    entriesList = []
    
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
            self.entryName1 = clsTestService.addGuidToString("Different Search in my media ", self.testNum)
            self.entryName = clsTestService.addGuidToString("search in my media ", self.testNum)
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, self.entryDescription1, self.entryTags1) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
            self.entriesList.append(self.entryName1)
            
            writeToLog("INFO","Step 2: Going to upload " + str(self.numberOfEntriesToUpload) + " entries")  
            number = "1"
            for i in range(self.numberOfEntriesToUpload):
                if self.common.upload.uploadEntry(self.filePath, self.entryName+number, self.entryDescription, self.entryTags) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step 2: FAILED to upload entry' " + self.entryName+number + "'")
                    return 
                self.entriesList.append(self.entryName+number)
                number = str(int(number) + 1)
                                
            writeToLog("INFO","Step 3: Going navigate to my media")            
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to my media")
                return   
                
            writeToLog("INFO","Step 4: Going navigate to entry page via entry thumbnail")  
            if self.common.myMedia.navigateToEntryPageFromMyMediaViaThubnail(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to entry '" + self.entryName + "' via entry thumbnail")
                return
             
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Search in my media' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")                     
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')