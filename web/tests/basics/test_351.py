import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #==============================================================================================================
    # Test Description 
    # Test Description Test Description Test Description Test Description Test Description Test Description
    # Test Description Test Description Test Description Test Description Test Description Test Description
    #==============================================================================================================
    testNum     = "351"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = None
    entryTags = None 
    slideDeckFilePath = None
    
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Slide Deck Upload")
            self.entryDescription = "Description"
            self.entryTags = "Tags,"
            self.filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
            self.whereToPublishFrom = "Entry Page"

            
            ##################### TEST STEPS - MAIN FLOW ##################### 
                
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
                    
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                return False
            
            writeToLog("INFO","Step 3: Going add upload slide deck")
            if self.common.editEntryPage.uploadSlidesDeck(self.slideDeckFilePath) == False:
                writeToLog("INFO","Step 2: FAILED to add  slides to entry")
                return False
                          
         

            
            ##################################################################
            print("Test 'Slide Deck Upload' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.login.logOutOfKMS()
            self.common.loginAsUser()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')