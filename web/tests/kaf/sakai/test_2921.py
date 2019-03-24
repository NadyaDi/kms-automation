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
    # author: Michal Zomper
    # Test Name:  Sakai - Gallery Moderation
    # Test description::
    # Login with non owner user of the gallery and upload entries > entries with added to pending tab
    # Login with owner user of the gallery and approve / reject the entries
    # Verify the the approve entry display in the gallery and that the reject entry don't dispaly in the gallery
    #==============================================================================================================
    testNum     = "2921"
    application = enums.Application.SAKAI
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
    newUserId = "sakaiauto"
    newUserPass = "Kaltura1!"
    galleryName = "New1"
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        #write to log we started the test
        logStartTest(self, driverFix, self.application)
        try:
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName1 = clsTestService.addGuidToString('1 rejected entry')
            self.entryName2 = clsTestService.addGuidToString('2 approved/published entry')
            self.entryName3 = clsTestService.addGuidToString('3 pending entry')
            self.entryName4 = clsTestService.addGuidToString('4 private entry')
            self.imageEntry1 = UploadEntry(self.filePathImage, self.entryName2, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.imageEntry2 = UploadEntry(self.filePathImage, self.entryName3, self.entryDescription, self.entryTags, timeout=60, retries=3)
            self.imageEntry3 = UploadEntry(self.filePathImage, self.entryName1, self.entryDescription, self.entryTags, timeout=60, retries=3)            
            self.uploadEntrieList = [self.imageEntry1, self.imageEntry2, self.imageEntry3]
            
            self.entriesToUpload = { 
                self.entryName4: self.filePath } 

            ##################### TEST STEPS - MAIN FLOW #####################
            
            writeToLog("INFO","Step 1: Going to upload  entry")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
                 
            writeToLog("INFO","Step 2: Going to publish entries 1-3 to Gallery")
            if self.common.kafGeneric.addNewContentToGallery(self.galleryName, self.uploadEntrieList, isGalleryModerate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to publish entries 1-3 gallery")
                return
            
            sleep(2)
            self.common.base.switch_to_default_content()     
            writeToLog("INFO","Step 3: Going to logout from main user")
            if self.common.sakai.logOutOfSakai() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to logout from main user")
                return  
                                      
            writeToLog("INFO","Step 4: Going to login with gallery's owner")
            if self.common.sakai.loginToSakai(self.newUserId, self.newUserPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to login with gallery's owner")
                return
             
            expectedEntriesList = [self.entryName1, self.entryName2, self.entryName3]
               
            writeToLog("INFO","Step 5: Going to sort entries by Alphabetical & Image type")
            if self.common.channel.sortAndFilterInPendingTab(enums.SortBy.ALPHABETICAL, enums.MediaType.IMAGE, self.galleryName, True, enums.Location.GALLERY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to sort entries by Alphabetical & Image type")
                return
               
            writeToLog("INFO","Step 6: Going to verify entries order - by Alphabetical & Image type")
            if self.common.myMedia.verifyEntriesOrder(expectedEntriesList, enums.Location.PENDING_TAB) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify entries order - by Alphabetical & Image type")
                return
                    
            writeToLog("INFO","Step 7: Going to handle entries in Pending tab: rejecting entry #1, Approving entry #2")
            if self.common.kafGeneric.handlePendingEntriesIngallery(self.galleryName, self.entryName1, self.entryName2, navigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to handle entries in Pending tab")
                return
            
            sleep(2)
            self.common.base.switch_to_default_content() 
            writeToLog("INFO","Step 8: Going to logout from gallery owner user")
            if self.common.sakai.logOutOfSakai() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to logout from gallery owner user")
                return  
             
            writeToLog("INFO","Step 9: Going to login with main user")
            if self.common.sakai.loginToSakai(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to login with main user")
                return
             
            self.entries = {self.entryName1: enums.EntryPrivacyType.REJECTED, 
                            self.entryName2: enums.EntryPrivacyType.PUBLISHED,
                            self.entryName3: enums.EntryPrivacyType.PENDING, 
                            self.entryName4: enums.EntryPrivacyType.PRIVATE }
             
            writeToLog("INFO","Step 10: Going navigate to my media")
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED navigate to my media")
                return
            
            writeToLog("INFO","Step 11: Going to verify the entries' privacy on my-media")
            try:
                for entry in self.entries:
                    if self.common.myMedia.verifyEntryPrivacyInMyMedia(entry, self.entries.get(entry), forceNavigate=False) == False:
                        writeToLog("INFO","Step 11: FAILED verify privacy for entry: " + str(entry))  
                        self.status = "Fail"
                        return                        
            except:
                writeToLog("INFO","Step 11: FAILED verify privacy for entry: " + str(entry))  
                self.status = "Fail"
                return
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Sakai - Gallery Moderated' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)              
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.common.base.switch_to_default_content()
            if (localSettings.LOCAL_SETTINGS_LOGIN_USERNAME in self.common.sakai.getSakaiLoginUserName().split(' ')[0]) == False:
                self.common.sakai.logOutOfSakai()
                self.common.sakai.loginToSakai(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
            self.common.kafGeneric.switchToKAFIframeGeneric()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')