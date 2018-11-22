import time, pytest,sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
from upload import UploadEntry


class Test:
    
    #==============================================================================================================
    # Test Description 
    # author: Tzachi guetta
    # Category page - Category Moderated
    #==============================================================================================================
    testNum     = "713"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = "Entry description"
    entryTags = "entrytags1,entrytags2,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg' 
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\audios\audio.mp3' 
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4' 
    
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
            self.entryName1 = clsTestService.addGuidToString('entryName1')
            self.entryName2 = clsTestService.addGuidToString('entryName2')
            self.entryName3 = clsTestService.addGuidToString('entryName3')
            self.entryName4 = clsTestService.addGuidToString('entryName4')
            self.entryName5 = clsTestService.addGuidToString('entryName5')
            self.imageEntry1 = UploadEntry(self.filePathImage, self.entryName2, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.imageEntry2 = UploadEntry(self.filePathImage, self.entryName3, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.imageEntry3 = UploadEntry(self.filePathImage, self.entryName1, self.entryDescription, self.entryTags, timeout=60, retries=3)            
            uploadEntrieList = [self.imageEntry1, self.imageEntry2, self.imageEntry3]
            self.newUserId = "pythonautomation1@mailinator.com"
            self.newUserPass = "Kaltura1!"
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to perform login to KMS site as End-user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login as End-user")
                return
               
            self.entriesToUpload = { 
                self.entryName4: self.filePath,
                self.entryName5: self.filePath }            
               
            writeToLog("INFO","Step 2: Going to upload 5 entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload 5 entries")
                return
                 
            writeToLog("INFO","Step 3: Going to set entry #4 as Unlisted")
            if self.common.myMedia.publishSingleEntryPrivacyToUnlistedInMyMedia(self.entryName4) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to set entry #4 as Unlisted")
                return     
                  
            writeToLog("INFO","Step 4: Going to publish entries 1-3 to Moderated category")
            if self.common.category.addNewContentToCategory("KMS-Automation_Moderate_Category", uploadEntrieList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to publish entries 1-3 to Moderated category")
                return
                  
            writeToLog("INFO","Step 5: Going to logout from End-user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED failed to logout from End-user")
                return  
                                      
            writeToLog("INFO","Step 6: Going to login to KMS with channel's owner")
            if self.common.login.loginToKMS(self.newUserId, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to login with channel's owner")
                return
             
            expectedEntriesList = [self.entryName1, self.entryName2]
               
            writeToLog("INFO","Step 7: Going to sort entries by Alphabetical & Image type")
            if self.common.channel.sortAndFilterInPendingTab(enums.SortBy.ALPHABETICAL, enums.MediaType.IMAGE, "KMS-Automation_Moderate_Category", True, enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to sort entries by Alphabetical & Image type")
                return
               
            writeToLog("INFO","Step 8: Going to verify entries order - by Alphabetical & Image type")
            if self.common.myMedia.verifyEntriesOrder(expectedEntriesList, enums.Location.PENDING_TAB) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify entries order - by Alphabetical & Image type")
                return
                    
            writeToLog("INFO","Step 9: Going to handle entries in Pending tab: rejecting entry #1, Approving entry #2")
            if self.common.category.handlePendingEntriesInCategory("KMS-Automation_Moderate_Category", self.entryName1, self.entryName2, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to handle entries in Pending tab")
                return
             
            writeToLog("INFO","Step 10: Going to logout ")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED failed to logout")
                return  
             
            writeToLog("INFO","Step 11: Going to perform login to KMS site End-user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to login as End-user")
                return
             
            self.entries = {self.entryName1: enums.EntryPrivacyType.REJECTED, 
                            self.entryName2: enums.EntryPrivacyType.PUBLISHED,
                            self.entryName3: enums.EntryPrivacyType.PENDING, 
                            self.entryName4: enums.EntryPrivacyType.UNLISTED,
                            self.entryName5: enums.EntryPrivacyType.PRIVATE }
             
            writeToLog("INFO","Step 12: Going to verify the entries' privacy on my-media")
            try:
                for entry in self.entries:
                    if self.common.myMedia.verifyEntryPrivacyInMyMedia(entry, self.entries.get(entry)) == False:
                        writeToLog("INFO","Step 12: FAILED verify privacy for entry: " + str(entry))  
                        self.status = "Fail"
                        return                        
            except:
                writeToLog("INFO","Step 12: FAILED verify privacy for entry: " + str(entry))  
                self.status = "Fail"
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Category Moderated' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            if self.status == "Fail" : 
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