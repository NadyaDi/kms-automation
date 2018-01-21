import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #================================================================================================================================
    #  @Author: Tzachi Guetta
    # Test description:
    # In case disclaimer module is turned on and set to "before upload" 
    # The following test will check that upload is prevented before disclaimer's check-box was checked.
    # The test's Flow: 
    # Login -> Checking that the user is not able to upload before accepting disclaimer -> Accepting disclaimer -> performing upload
    # then, Navigating to Entry page. 
    # test cleanup: deleting the uploaded file, turning off disclaimer module
    #================================================================================================================================
    testNum     = "1555"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Tzachi Entry description"
    entryTags = "entrytags1,entrytags2,"
    filePath = "C:\\Users\\tzachi.guetta\\Downloads\\1.JPG"
    
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
            self,captur,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString('entryName')
            ##################### TEST STEPS - MAIN FLOW #####################
            
            
            ########################### KMS ADMIN SETUP ###########################
            self.common.admin.navigateToAdminPage()
            self.common.admin.adminDisclaimer(True)
            ########################### KMS ADMIN SETUP ###########################
            
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
             
            writeToLog("INFO","Step 2: Going to upload entry while disclaimer turned ON")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags, disclaimer=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
               
            writeToLog("INFO","Step 3: Going to navigate to Entry Page")
            if self.common.entryPage.navigateToEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to Entry Page")
                return
            ##################################################################
            print("DONE")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            self.common.admin.adminDisclaimer(False)
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')