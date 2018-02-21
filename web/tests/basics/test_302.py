import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

class Test:
    
    #==============================================================================================================
    # Test Description 
    # Test Description Test Description Test Description Test Description Test Description Test Description
    # Test Description Test Description Test Description Test Description Test Description Test Description
    #==============================================================================================================
    testNum     = "302"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName1 = None
    entryName2 = None
    entryName3 = None
    entryName4 = None
    entryName5 = None
    newUserId = None
    newUserPass = None
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    
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
            self.entryName1 = clsTestService.addGuidToString('entryName1')
            self.entryName2 = clsTestService.addGuidToString('entryName2')
            self.entryName3 = clsTestService.addGuidToString('entryName3')
            self.entryName4 = clsTestService.addGuidToString('entryName4')
            self.entryName5 = clsTestService.addGuidToString('entryName5')
            self.newUserId = "webcast@mailinator.com"
            self.newUserPass = "Automation1!"
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as user")
                return
             
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
             
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName2, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
             
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName3, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName4, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return
            
            writeToLog("INFO","Step 2: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName5, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry")
                return            
            
            writeToLog("INFO","Step 3: Going to publish two entries to Moderated channel")
            if self.common.channel.addContentToChannel("KMS-Automation_Moderate_Channel", [self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5], isChannelModerate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to publish two entries to Moderated channel")
                return
            
            writeToLog("INFO","Step 5: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED failed to logout from main user")
                return  
                                  
            writeToLog("INFO","Step 6: Going to login with channel's owner")
            if self.common.login.loginToKMS(self.newUserId, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to login with channel's owner")
                return
            
            writeToLog("INFO","Step 3: Going to handle entries in Pending tab")
            if self.common.channel.handlePendingEntriesInChannel("KMS-Automation_Moderate_Channel", [self.entryName1, self.entryName2], [self.entryName3, self.entryName4]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to handle entries in Pending tab")
                return    
            ##################################################################
            print("DONE")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            if self.status == "Fail":
                self.common.base.takeScreeshotGeneric('LAST_SCRENNSHOT')              
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.login.logOutOfKMS()
            self.common.loginAsUser()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')