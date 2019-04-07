import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from enum import *
import time, pytest
from clsCommon import Common
import clsTestService
import enums
from localSettings import *
import localSettings
from utilityTestFunc import *
import ctypes
import collections
from upload import UploadEntry

class Test:
    #================================================================================================================================
    # @Author: Oded Berihon
    # Test Name : Canvas: My Media - Filter Media View Different Statuses
    # Test description:
    # upload 4 entries
    # some of the entries live as private /publish  /Pending / Rejected
    # In the Status filter:
    #    1. Filter by 'Private' -  Only Private entries should be displayed 
    #    2. Filter by 'Published' - Only Published entries should be displayed
    #    3. Filter by 'Pending' - Only Pending entries should be displayed
    #    4. Filter by 'Rejected' - Only Rejected entries should be displayed
    #    5. Filter by 'All Media' - All the user's entries should be displayed - in any status..
    # *A compatible label should be displayed on top of the entry's thumbnail.
    #================================================================================================================================
    testNum     = "2292"
    application = enums.Application.CANVAS
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
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    galleryName = "New1"
    userName1 = "autocanvas@mailinator.com"
    userPass1 = "Kaltura1!"
    filterByPrivate = None
    filterByPublished = None
    filterByRejected = None
    filterByPending = None
    filterByAllMedia = None
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self, driverFix, self.application)
            ########################### TEST SETUP ###########################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            self.entryName1 = clsTestService.addGuidToString("My Media - Filter by status - Private", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Media - Filter by status - Published", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("My Media - Filter by status - Rejected", self.testNum)
            self.entryName4 = clsTestService.addGuidToString("My Media - Filter by status - Pending", self.testNum)
            
            self.filterByPrivate = {self.entryName1: True, self.entryName2: False, self.entryName3: False, self.entryName4: False}
            self.filterByPublished = {self.entryName1: False, self.entryName2: True, self.entryName3: False, self.entryName4: False}
            self.filterByRejected = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False}
            self.filterByPending = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryName4: True}
            self.filterByAllMedia = {self.entryName1: enums.EntryPrivacyType.PRIVATE, self.entryName2: enums.EntryPrivacyType.PUBLISHED, self.entryName3: enums.EntryPrivacyType.REJECTED, self.entryName4: enums.EntryPrivacyType.PENDING}
            
            self.entriesToUpload = {
            self.entryName1: self.filePath,
            self.entryName2: self.filePath }
            
            self.rejectedEntrey = UploadEntry(self.filePath, self.entryName3, self.description, self.tags, timeout=60, retries=3)
            self.PendingEntry = UploadEntry(self.filePath, self.entryName4, self.description, self.tags, timeout=60, retries=3)
            uploadEntrieList = [self.rejectedEntrey, self.PendingEntry] 
            
            ##################### TEST STEPS - MAIN FLOW ##################### 
                   
            writeToLog("INFO","Step 1: Going to upload 2 entries")   
            if self.common.upload.uploadEntries(self.entriesToUpload, self.description, self.tags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to upload 2 entries")
                return  
                  
            writeToLog("INFO","Step 2: Going to set one entry as published")  
            if self.common.myMedia.publishEntriesFromMyMedia(self.entryName2, "", "", [self.galleryName]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to publish entry '" + self.entryName2 + "'")
                return 
                 
            writeToLog("INFO","Step 3: Going to publish entries to moderated gallery")  
            if self.common.kafGeneric.addNewContentToGallery(self.galleryName, uploadEntrieList, isGalleryModerate=True)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to publish entries to moderated gallery")
                return 
             
            sleep(3)    
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 4: Going to logout from main user")
            if self.common.canvas.logOutOfCanvas() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to logout from user: " + self.userName1)
                return  
                                    
            writeToLog("INFO","Step 5:Going to login with : " + self.userName1)
            if  self.common.canvas.loginToCanvas(self.userName1, self.userPass1)  == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to login with " + self.userName1)
                return
                 
            writeToLog("INFO","Step 6: Going to handle entries in gallery pending tab")  
            if self.common.kafGeneric.handlePendingEntriesIngallery(self.galleryName, self.entryName3, self.entryName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to handle entries in gallery pending tab")
                return 
             
            sleep(3) 
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 7: Going to logout from user: " + self.userName1)
            if self.common.canvas.logOutOfCanvas() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to logout from main user")
                return  
             
            sleep(2)                       
            writeToLog("INFO","Step 8: Going to login with main user")
            if self.common.canvas.loginToCanvas(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to login with main user")
                return
                
            writeToLog("INFO","Step 9: Going navigate to my media")  
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED navigate to my media")
                return  
                
            sleep(1)
            # New UI only !! this parameter will be click after every sort so each sort will only have only the chosen type 
            tmpStatus = (self.common.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.common.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace("DROPDOWNLIST_ITEM", enums.EntryPrivacyType.ALL_STATUSSES.value))
            writeToLog("INFO","Step 10: Going to verify that only entries with " + enums.EntryPrivacyType.PRIVATE.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PRIVATE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 10: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PRIVATE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 10: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                    return
                  
            writeToLog("INFO","Step 11: Going to verify my media entries by: " + enums.EntryPrivacyType.PRIVATE.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByPrivate) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                return 
              
            writeToLog("INFO","Step 12: Going to verify entry privacy label: " + enums.EntryPrivacyType.PRIVATE.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName1, enums.EntryPrivacyType.PRIVATE, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to verify that entry '" + self.entryName1 + "' label is '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                return 
              
            # close the filters
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpStatus, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Status' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                  
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False
              
            sleep(1)
            writeToLog("INFO","Step 13: Going to verify that only entries with " + enums.EntryPrivacyType.PUBLISHED.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PUBLISHED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 13: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PUBLISHED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 13: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                    return
              
            writeToLog("INFO","Step 14: Going to verify my media entries by: " + enums.EntryPrivacyType.PUBLISHED.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByPublished) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                return 
             
            writeToLog("INFO","Step 15: Going to verify entry privacy label: " + enums.EntryPrivacyType.PUBLISHED.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName2, enums.EntryPrivacyType.PUBLISHED, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to verify that entry '" + self.entryName2 + "' label is '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                return
             
            # remove privacy type from filter
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpStatus, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Status' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                 
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False
                 
            sleep(1)
            writeToLog("INFO","Step 16: Going to verify that only entries with " + enums.EntryPrivacyType.REJECTED.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.REJECTED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 16: FAILED to filter my media entries by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.REJECTED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 16: FAILED to filter my media entries by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                    return
              
            writeToLog("INFO","Step 17: Going to verify my media entries by: " + enums.EntryPrivacyType.REJECTED.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByRejected) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                return 
             
            writeToLog("INFO","Step 18: Going to verify entry privacy label: " + enums.EntryPrivacyType.REJECTED.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName3, enums.EntryPrivacyType.REJECTED, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to verify that entry '" + self.entryName3 + "' label is '" + enums.EntryPrivacyType.REJECTED.value + "'")
                return
             
            # remove privacy type from filter
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpStatus, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Status' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False
      
            sleep(1)
            writeToLog("INFO","Step 19: Going to verify that only entries with " + enums.EntryPrivacyType.PENDING.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PENDING) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 19: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PENDING.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PENDING) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 19: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PENDING.value + "'")
                    return
              
            writeToLog("INFO","Step 20: Going to verify my media entries by: " + enums.EntryPrivacyType.PENDING.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByPending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.PENDING.value + "'")
                return 
             
            writeToLog("INFO","Step 21: Going to verify entry privacy label: " + enums.EntryPrivacyType.PENDING.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName4, enums.EntryPrivacyType.PENDING, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to verify that entry '" + self.entryName4 + "' label is '" + enums.EntryPrivacyType.PENDING.value + "'")
                return
             
            # remove privacy type from filter
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpStatus, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Status' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False
                 
             
            sleep(1)
            writeToLog("INFO","Step 22: Going to verify that only entries with " + enums.EntryPrivacyType.ALL_STATUSSES.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.ALL_STATUSSES) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 22: FAILED to filter my media entries by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.ALL_STATUSSES) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 22: FAILED to filter my media entries by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                    return
             
            writeToLog("INFO","Step 23: Going to verify my media entries by: " + enums.EntryPrivacyType.ALL_STATUSSES.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByAllMedia) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                return
             
            writeToLog("INFO","Step 24: Going to verify all entries privacy when filter set to: " + enums.EntryPrivacyType.ALL_STATUSSES.value)  
            if self.common.myMedia.verifyEntriesPrivacyInMyMedia(self.filterByAllMedia) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to verify all entries privacy when filter set to : " + enums.EntryPrivacyType.ALL_STATUSSES.value)
                return
            
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'Canvas: My Media - Filter Media View Different Statuses' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.base.switch_to_default_content()
            if (localSettings.LOCAL_SETTINGS_LOGIN_USERNAME.lower().split('@')[0] in self.common.canvas.getCanvasLoginUserName().split(' ')[0]) == False:
                sleep()
                self.common.canvas.logOutOfCanvas()
                self.common.canvas.loginToCanvas(localSettings.LOCAL_SETTINGS_LOGIN_USERNAME, localSettings.LOCAL_SETTINGS_LOGIN_PASSWORD)
            self.common.canvas.switchToCanvasIframe()
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4])
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')