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
    # Test Name : My Media - Filter by status
    # Test description:
    # upload 5 entries from all types: image / audio / video
    # some of the entries live as private /publish /Unlisted /Pending / Rejected
    # In the Status filter:
    #    1. Filter by 'Private' -  Only Private entries should be displayed 
    #    2. Filter by 'Published' - Only Published entries should be displayed
    #    3. Filter by 'Pending' - Only Pending entries should be displayed
    #    4. Filter by 'Rejected' - Only Rejected entries should be displayed
    #    5. Filter by 'Unlisted' - Only Unlisted entries should be displayed
    #    6. Filter by 'All Media' - All the user's entries should be displayed - in any status..
    # *A compatible label should be displayed on top of the entry's thumbnail.
    #================================================================================================================================
    testNum = "666"
    
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
    description = "Description" 
    tags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\qrcode_middle_4.png'
    categoryName = [("Apps Automation Category")]
    channelName =  "Moderated Channel"
    userName1 = "Automation_User_1"
    userPass1 = "Kaltura1!"
    filterByPrivate = None
    filterByUnlisted = None
    filterByPublished = None
    filterByRejected = None
    filterByPending = None
    filterByAllMedia = None
    
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
            self.entryName1 = clsTestService.addGuidToString("My Media - Filter by status - Private", self.testNum)
            self.entryName2 = clsTestService.addGuidToString("My Media - Filter by status - Unlisted", self.testNum)
            self.entryName3 = clsTestService.addGuidToString("My Media - Filter by status - Published", self.testNum)
            self.entryName4 = clsTestService.addGuidToString("My Media - Filter by status - Rejected", self.testNum)
            self.entryName5 = clsTestService.addGuidToString("My Media - Filter by status - Pending", self.testNum)
            self.channelName = clsTestService.addGuidToString(self.channelName, self.testNum)
            
            # each dictionary get a list of entries and bool parameter that indicate if the entry need to be display in the list filter or not
#             self.filterByPrivate = {(self.entryName1, True), (self.entryName2, False), (self.entryName3, False), (self.entryName4, False), (self.entryName5, False)}
#             self.filterByUnlisted = [(self.entryName1, False), (self.entryName2, True), (self.entryName3, False), (self.entryName4, False), (self.entryName5, False)]
#             self.filterByPublished = [(self.entryName1, False), (self.entryName2, False), (self.entryName3, True), (self.entryName4, False), (self.entryName5, False)]
#             self.filterByRejected = [(self.entryName1, False), (self.entryName2, False), (self.entryName3, False), (self.entryName4, True), (self.entryName5, False)]
#             self.filterByPending = [(self.entryName1, False), (self.entryName2, False), (self.entryName3, False), (self.entryName4, False), (self.entryName5, True)]
#             self.filterByAllMedia = [(self.entryName1, enums.EntryPrivacyType.PRIVATE), (self.entryName2, enums.EntryPrivacyType.UNLISTED), (self.entryName3, enums.EntryPrivacyType.PUBLISHED), (self.entryName4, enums.EntryPrivacyType.REJECTED), (self.entryName5, enums.EntryPrivacyType.PENDING)]

            self.filterByPrivate = {self.entryName1: True, self.entryName2: False, self.entryName3: False, self.entryName4: False, self.entryName5: False}
            self.filterByUnlisted = {self.entryName1: False, self.entryName2: True, self.entryName3: False, self.entryName4: False, self.entryName5: False}
            self.filterByPublished = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryName4: False, self.entryName5: False}
            self.filterByRejected = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryName4: True, self.entryName5: False}
            self.filterByPending = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryName4: False, self.entryName5: True}
            self.filterByAllMedia = {self.entryName1: enums.EntryPrivacyType.PRIVATE, self.entryName2: enums.EntryPrivacyType.UNLISTED, self.entryName3: enums.EntryPrivacyType.PUBLISHED, self.entryName4: enums.EntryPrivacyType.REJECTED, self.entryName5: enums.EntryPrivacyType.PENDING}

            ##################### TEST STEPS - MAIN FLOW ##################### 
            for i in range(1,6):
                writeToLog("INFO","Step " + str(i) + ": Going to upload new images entries")            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryName'+str(i)), self.description, self.tags) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i) + ": FAILED to upload new entry " + eval('self.entryName'+str(i)))
                    return
                
            writeToLog("INFO","Step 6: Going navigate to my media")  
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate to my media")
                return  
    
            writeToLog("INFO","Step 7: Going to set one entry as unlisted")  
            if self.common.myMedia.publishSingleEntryPrivacyToUnlistedInMyMedia(self.entryName2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to set entry '" + self.entryName2 + "' as unlisted")
                return 
                
            writeToLog("INFO","Step 8: Going navigate to my media")  
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to my media")
                return  
               
            writeToLog("INFO","Step 9: Going to set one entry as published")  
            if self.common.myMedia.publishEntriesFromMyMedia(self.entryName3, self.categoryName, "") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to publish entry '" + self.entryName3 + "'")
                return 
               
#             sleep(3)
            writeToLog("INFO","Step 10: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to logout from main user")
                return  
                                  
            writeToLog("INFO","Step 11: Going to login with : " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to login with " + self.userName1)
                return
               
            writeToLog("INFO","Step 12: Going to create Channel")
            if self.common.channel.createChannel(self.channelName, self.description, self.tags, enums.ChannelPrivacyType.OPEN, True, True, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to create Channel")
                return
               
            sleep(3)
            writeToLog("INFO","Step 13: Going to logout from " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to logout from " + self.userName1)
                return  
                                  
            writeToLog("INFO","Step 14: Going to login with main user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to login with main user")
                return
               
            writeToLog("INFO","Step 15: Going to publish entries to moderated channel")  
            if self.common.channel.addExistingContentToChannel(self.channelName, [self.entryName4, self.entryName5], isChannelModerate=True, publishFrom = enums.Location.CHANNELS_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to publish entries to moderated channel")
                return 
               
            sleep(3)
            writeToLog("INFO","Step 16: Going to logout from main user")
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to logout from main user")
                return  
                                  
            writeToLog("INFO","Step 17: Going to login with : " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to login with " + self.userName1)
                return
               
            writeToLog("INFO","Step 18: Going to reject entry form channel")  
            if self.common.channel.handlePendingEntriesInChannel(self.channelName, self.entryName4, "" , navigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to reject entry '" + self.entryName4 + "' from channel '" + self.channelName + "'")
                return 
               
            sleep(3)
            writeToLog("INFO","Step 19: Going to logout from " + self.userName1)
            if self.common.login.logOutOfKMS() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to logout from " + self.userName1)
                return  
                                  
            writeToLog("INFO","Step 20: Going to login with main user")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to login with main user")
                return
              
            writeToLog("INFO","Step 21: Going navigate to my media")  
            if self.common.myMedia.navigateToMyMedia() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED navigate to my media")
                return  
              
            sleep(1)
            # New UI only !! this parameter will be click after every sort so each sort will only have only the chosen type 
            tmpStatus = (self.common.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.common.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace("DROPDOWNLIST_ITEM", enums.EntryPrivacyType.ALL_STATUSSES.value))
            writeToLog("INFO","Step 22: Going to verify that only entries with " + enums.EntryPrivacyType.PRIVATE.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PRIVATE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 22: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PRIVATE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 22: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                    return
                
            writeToLog("INFO","Step 23: Going to verify my media entries by: " + enums.EntryPrivacyType.PRIVATE.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByPrivate) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.PRIVATE.value + "'")
                return 
            
            writeToLog("INFO","Step 24: Going to verify entry privacy label: " + enums.EntryPrivacyType.PRIVATE.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName1, enums.EntryPrivacyType.PRIVATE, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to verify that entry '" + self.entryName1 + "' label is '" + enums.EntryPrivacyType.PRIVATE.value + "'")
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
            writeToLog("INFO","Step 25: Going to verify that only entries with " + enums.EntryPrivacyType.UNLISTED.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.UNLISTED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 25: FAILED to filter my media entries by '" + enums.EntryPrivacyType.UNLISTED.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.UNLISTED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 25: FAILED to filter my media entries by '" + enums.EntryPrivacyType.UNLISTED.value + "'")
                    return
              
            writeToLog("INFO","Step 26: Going to verify my media entries by: " + enums.EntryPrivacyType.UNLISTED.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByUnlisted) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.UNLISTED.value + "'")
                return 
            
            writeToLog("INFO","Step 27: Going to verify entry privacy label: " + enums.EntryPrivacyType.UNLISTED.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName2, enums.EntryPrivacyType.UNLISTED, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED to verify that entry '" + self.entryName2 + "' label is '" + enums.EntryPrivacyType.UNLISTED.value + "'")
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
            writeToLog("INFO","Step 28: Going to verify that only entries with " + enums.EntryPrivacyType.PUBLISHED.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PUBLISHED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 28: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PUBLISHED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 28: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                    return
             
            writeToLog("INFO","Step 29: Going to verify my media entries by: " + enums.EntryPrivacyType.PUBLISHED.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByPublished) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
                return 
            
            writeToLog("INFO","Step 30: Going to verify entry privacy label: " + enums.EntryPrivacyType.PUBLISHED.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName3, enums.EntryPrivacyType.PUBLISHED, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 30: FAILED to verify that entry '" + self.entryName3 + "' label is '" + enums.EntryPrivacyType.PUBLISHED.value + "'")
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
            writeToLog("INFO","Step 31: Going to verify that only entries with " + enums.EntryPrivacyType.REJECTED.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.REJECTED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 31: FAILED to filter my media entries by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.REJECTED) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 31: FAILED to filter my media entries by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                    return
             
            writeToLog("INFO","Step 32: Going to verify my media entries by: " + enums.EntryPrivacyType.REJECTED.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByRejected) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 32: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.REJECTED.value + "'")
                return 
            
            writeToLog("INFO","Step 33: Going to verify entry privacy label: " + enums.EntryPrivacyType.REJECTED.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName4, enums.EntryPrivacyType.REJECTED, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 33: FAILED to verify that entry '" + self.entryName4 + "' label is '" + enums.EntryPrivacyType.REJECTED.value + "'")
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
            writeToLog("INFO","Step 34: Going to verify that only entries with " + enums.EntryPrivacyType.PENDING.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PENDING) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 34: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PENDING.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.PENDING) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 34: FAILED to filter my media entries by '" + enums.EntryPrivacyType.PENDING.value + "'")
                    return
             
            writeToLog("INFO","Step 35: Going to verify my media entries by: " + enums.EntryPrivacyType.PENDING.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByPending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 35: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.PENDING.value + "'")
                return 
            
            writeToLog("INFO","Step 36: Going to verify entry privacy label: " + enums.EntryPrivacyType.PENDING.value)  
            if self.common.myMedia.verifyEntryPrivacyInMyMedia(self.entryName5, enums.EntryPrivacyType.PENDING, forceNavigate=False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 36: FAILED to verify that entry '" + self.entryName5 + "' label is '" + enums.EntryPrivacyType.PENDING.value + "'")
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
            writeToLog("INFO","Step 37: Going to verify that only entries with " + enums.EntryPrivacyType.ALL_STATUSSES.value + " icon display")
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.ALL_STATUSSES) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 37: FAILED to filter my media entries by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                    return
            else:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.PRIVACY ,enums.EntryPrivacyType.ALL_STATUSSES) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 37: FAILED to filter my media entries by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                    return
            
            writeToLog("INFO","Step 38: Going to verify my media entries by: " + enums.EntryPrivacyType.ALL_STATUSSES.value)  
            if self.common.myMedia.verifyFiltersInMyMedia(self.filterByAllMedia) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 38: FAILED to verify my media entries  by '" + enums.EntryPrivacyType.ALL_STATUSSES.value + "'")
                return
            
            writeToLog("INFO","Step 39: Going to verify all entries privacy when filter set to: " + enums.EntryPrivacyType.ALL_STATUSSES.value)  
            if self.common.myMedia.verifyEntriesPrivacyInMyMedia(self.filterByAllMedia) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 39: FAILED to verify all entries privacy when filter set to : " + enums.EntryPrivacyType.ALL_STATUSSES.value)
                return
           
            ##################################################################
            writeToLog("INFO","TEST PASSED: 'My Media - Filter by status' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")     
            if localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN != "QA APPLICATION" or localSettings.LOCAL_SETTINGS_USERNAME_AFTER_LOGIN != "QA Application":
                self.common.login.logOutOfKMS()
                self.common.loginAsUser() 
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3, self.entryName4, self.entryName5])
            sleep(2)
            self.common.login.logOutOfKMS() 
            self.common.login.loginToKMS(self.userName1, self.userPass1)
            self.common.channel.deleteChannel(self.channelName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')