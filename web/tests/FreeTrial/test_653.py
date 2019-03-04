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
    # Test Name : Free trial
    # Test description:
    # create new free trial instance
    # In the new instance upload and publish media
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
    instanceNumber = None
    InstanceSuffix = ".qakmstest.dev.kaltura.com"
    AdminSecret = "a884f9a36523cc14e05f265ed9920999"
    InstanceId = "MediaSpace" 
    CompanyName = "Kaltura"
    Application = "MediaSpace"
    UserID = "qaapplicationautomation@mailinator.com"
    Password = "Kaltura1!"
    categoryList = [("About Kaltura")]
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_Code_10sec.mp4'
    if clsTestService.isAutomationEnv() == True:
        instanceNumberFilePath = '/home/local/kaltura.gen/q/QA-App/Automation/FreeTrial/FreeTrial.txt'
        
    else:
        instanceNumberFilePath = r'Q:\FreeTrial\FreeTrial.txt'

    
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

            writeToLog("INFO","Step 1: navigate to free trial url form")    
            self.instanceNumber = self.common.freeTrail.setInstanceNumber(self.instanceNumberFilePath)
            if self.instanceNumber == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to set instance number")
                return
            
            writeToLog("INFO","Step 2: navigate to free trial url form")
            if self.common.base.navigate("http://qakmstest.dev.kaltura.com/free-trial-test/") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to free trail url form: http://qakmstest.dev.kaltura.com/free-trial-test/")
                return
                          
            writeToLog("INFO","Step 3: create free trial instance")
            if self.common.freeTrail.createFreeTrialInctance(self.PartnerID, self.AdminSecret, self.InstanceId, self.CompanyName, self.instanceNumber + self.InstanceSuffix, self.Application) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to create free trial instance")
                return
            sleep(2)
             
            localSettings.LOCAL_SETTINGS_TEST_BASE_URL = "http://"+self.instanceNumber + self.InstanceSuffix
            localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/user/login'
            localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/my-media'                
            writeToLog("INFO","Step 4: navigate to new instance url")
            if self.common.base.navigate(localSettings.LOCAL_SETTINGS_TEST_BASE_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to instance url: " + localSettings.LOCAL_SETTINGS_TEST_BASE_URL)
                return
            
            writeToLog("INFO","Step 5: login to instance")
            if self.common.login.loginToKMS(self.UserID, self.Password, localSettings.LOCAL_SETTINGS_KMS_LOGIN_URL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to login to new instance")
                return
            sleep(2)
            
            writeToLog("INFO","Step 6: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED failed to upload entry: " + self.entryName)
                return
             
            sleep(2)       
            writeToLog("INFO","Step 7: Going navigate to my media")            
            if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED navigate to my media")
                return   
                           
            writeToLog("INFO","Step 8: Going to navigate to entry page")            
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to entry page: '" + self.entryName + "'")
                return     
            
            sleep(2)     
            writeToLog("INFO","Step 9: Going to publish the entry ")            
            if self.common.myMedia.publishSingleEntry(self.entryName, self.categoryList, "", publishFrom = enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to publish entry '" + self.entryName + "'")
                return             
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Free Trial' was done successfully")
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