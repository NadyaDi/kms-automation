import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','..','lib')))
import time, pytest
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
    # Login to KMS, and upload a media
    # Navigate Edit Entry Page
    # under thumbnail tab change thumnbnail in 3 different ways : Upload, Capture, Auto-Generate
    #================================================================================================================================
    testNum     = "653"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    SearchByInSaaSAdmin = "Hostname"
    PartnerID = "2178791"
    instanceNumber = "2178791-6"
    InstanceSuffix = ".qakmstest.dev.kaltura.com"
    AdminSecret = "a884f9a36523cc14e05f265ed9920999"
    InstanceId = "MediaSpace" 
    CompanyName = "Kaltura"
    Application = "MediaSpace"
    UserID = "qaapplicationautomation@mailinator.com"
    Password = "Kaltura1!!"

    
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Free trial", self.testNum)
            ##################### TEST STEPS - MAIN FLOW ##################### 
            
            
            writeToLog("INFO","Step 1: create free trial instance")
            if self.common.freeTrail.createFreeTrialInctance(self.PartnerID, self.AdminSecret, self.InstanceId, self.CompanyName, self.instanceNumber + self.InstanceSuffix, self.Application) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to create free trial instance")
                return

                                 
                                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Free Trial' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
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