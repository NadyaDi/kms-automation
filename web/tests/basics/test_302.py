import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *


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
            self.newUserId = "pythonautomation1@mailinator.com"
            self.newUserPass = "Kaltura1!"
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as End-user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as End-user")
                return
             
            writeToLog("INFO","Step 2: Going to upload entry #1")
            if self.common.upload.uploadEntry(self.filePath, self.entryName1, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry #1")
                return
              
            writeToLog("INFO","Step 3: Going to upload entry #2")
            if self.common.upload.uploadEntry(self.filePath, self.entryName2, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED failed to upload entry #2")
                return
              
            writeToLog("INFO","Step 4: Going to upload entry #3")
            if self.common.upload.uploadEntry(self.filePath, self.entryName3, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED failed to upload entry #3")
                return
             
            writeToLog("INFO","Step 5: Going to upload entry #4")
            if self.common.upload.uploadEntry(self.filePath, self.entryName4, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry #4")
                return
             
            writeToLog("INFO","Step 5: Going to upload entry #5")
            if self.common.upload.uploadEntry(self.filePath, self.entryName5, "descritiondescrition", "tags1,tags2,") == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED failed to upload entry #5")
                return
             
            writeToLog("INFO","Step 6: Going to set entry #4 as Unlisted")
            if self.common.myMedia.publishSingleEntryPrivacyToUnlistedInMyMedia(self.entryName4) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to set entry #4 as Unlisted")
                return     
              
            writeToLog("INFO","Step 7: Going to publish entries 1-3 to Moderated channel")
            if self.common.channel.addContentToChannel("KMS-Automation_Moderate_Channel", [self.entryName1, self.entryName2, self.entryName3], isChannelModerate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to publish entries 1-3 to Moderated channel")
                return
              
            writeToLog("INFO","Step 8: Going to logout from End-user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED failed to logout from End-user")
                return  
                                    
            writeToLog("INFO","Step 9: Going to login to KMS with channel's owner")
            if self.common.login.loginToKMS(self.newUserId, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to login with channel's owner")
                return
              
            writeToLog("INFO","Step 10: Going to handle entries in Pending tab: rejecting entry #1, Approving entry #2")
            if self.common.channel.handlePendingEntriesInChannel("KMS-Automation_Moderate_Channel", self.entryName1, self.entryName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to handle entries in Pending tab")
                return
            
            writeToLog("INFO","Step 11: Going to logout ")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED failed to logout")
                return  
            
            writeToLog("INFO","Step 12: Going to perform login to KMS site End-user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to login as End-user")
                return
            
            self.entries = {self.entryName1: enums.EntryPrivacyType.REJECTED, self.entryName2: enums.EntryPrivacyType.PUBLISHED,
                            self.entryName3: enums.EntryPrivacyType.PENDING, self.entryName4: enums.EntryPrivacyType.UNLISTED,
                            self.entryName5: enums.EntryPrivacyType.PRIVATE }
            
            writeToLog("INFO","Step 13: Going to verify the entries' privacy on my-media")
            try:
                for entry in self.entries:
                    if self.common.myMedia.verifyEntryPrivacyInMyMedia(entry, self.entries.get(entry)) == False:
                        writeToLog("INFO","Step 13: FAILED verify privacy for entry: " + str(entry))  
                        self.status = "Fail"
                        return                        
            except:
                writeToLog("INFO","Step 13: FAILED verify privacy for entry: " + str(entry))  
                self.status = "Fail"
                return
            ##################################################################
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')