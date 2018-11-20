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
    #  @Author: Inbar Willman
    # Test Name : eSearch - Sort by - Gallery - pending tab - when no search is made
    # Test description:
    # Upload entries with different sort by values
    # Go to channel page, pending and make the next sorts (with and without search):
    #    1. Creation Date - Descending -  The entries order should be from the last uploaded video to the first one.
    #    2. Creation Ascending - The entries order should be from the first uploaded video to the last one.
    #    3. Update Date - Descending -  The entries order should be from the last updated video to the first one.
    #    4. Creation Ascending - The entries order should be from the first updated video to the last one.
    #    5. Alphabetical A-Z - The entries order should be alphabetical A-Z
    #    6. Alphabetical Z-A - The entries order should be alphabetical Z-A
    #    7. Likes - The entries order should be from the most liked to the least liked
    #    8. Comments - The entries order should be from the ones with the most comments to the ones with least comments
    #    9. Scheduling Descending - The entries order should be from the first scheduling date to the latest scheduling date
    #    10. Scheduling Ascending - The entries order should be from the latest scheduling date to the first scheduling date
    #================================================================================================================================
    testNum = "4407"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    userName = "admin"
    userPass = "123456"
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
            
            self.searchInGalleryPending = "Sort by"
            self.gallery = "category for eSearch moderator"
            self.sortEntriesByCreationDateDescending = ("Sort by - Sort H", "Sort by - Sort G", "Sort by - Sort F", "Sort by - Sort E", "Sort by - Sort D", 
                                                        "Sort by - Sort C", "Sort by - Sort B", "Sort by - Sort A")
            self.sortEntriesByCreationDateAscending  = ("Sort by - Sort A", "Sort by - Sort B", "Sort by - Sort C", "Sort by - Sort D", "Sort by - Sort E",
                                                        "Sort by - Sort F", "Sort by - Sort G", "Sort by - Sort H")
            self.sortEntriesByUpdateDateDescending   = ("Sort by - Sort F", "Sort by - Sort G", "Sort by - Sort D", "Sort by - Sort E", "Sort by - Sort A",
                                                        "Sort by - Sort H", "Sort by - Sort C", "Sort by - Sort B")
            self.sortEntriesByUpdateDateAscending    = ("Sort by - Sort B", "Sort by - Sort C", "Sort by - Sort H", "Sort by - Sort A", "Sort by - Sort E",
                                                        "Sort by - Sort D", "Sort by - Sort G", "Sort by - Sort F")
            self.sortEntriesByAlphabeticalAToZ       = ("Sort by - Sort A", "Sort by - Sort B", "Sort by - Sort C", "Sort by - Sort D", "Sort by - Sort E",
                                                       "Sort by - Sort F", "Sort by - Sort G", "Sort by - Sort H")
            self.sortEntriesByAlphabeticalZToA       = ("Sort by - Sort H", "Sort by - Sort G", "Sort by - Sort F","Sort by - Sort E", "Sort by - Sort D", 
                                                        "Sort by - Sort C", "Sort by - Sort B", "Sort by - Sort A")
            self.sortEntriesByLikes                  = ("Sort by - Sort F", "Sort by - Sort D", "Sort by - Sort H", "Sort by - Sort G", "Sort by - Sort C", 
                                                        "Sort by - Sort E", "Sort by - Sort A", "Sort by - Sort B")
            self.SortEntriesByComments               = ("Sort by - Sort G", "Sort by - Sort F", "Sort by - Sort C", "Sort by - Sort E", "Sort by - Sort B", 
                                                        "Sort by - Sort A", "Sort by - Sort D", "Sort by - Sort H")
            self.sortEntriesBySchedulingAscending    = ("Sort by Scheduling - Past", "Sort by Scheduling - In scheduling", "Sort by Scheduling - Future")
            self.sortEntriesBySchedulingDescending   = ("Sort by Scheduling - Future", "Sort by Scheduling - In scheduling", "Sort by Scheduling - Past")
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to login to KMS")
            if self.common.login.loginToKMS(self.userName, self.userPass) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login to KMS")
                return 
                        
            writeToLog("INFO","Step 2: Going to navigate to gallery page - pending tab")
            if self.common.channel.navigateToPendingaTab(self.gallery, location=enums.Location.CATEGORY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to go to navigate gallery page")
                return      
                                      
            writeToLog("INFO","Step 3: Going to verify default sort before making a search")
            if self.common.channel.verifyChannelsDefaultSort(enums.SortBy.CREATION_DATE_DESC) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to displayed correct default sort before making a search")
                return   
             
            writeToLog("INFO","Step 4: Going verify sort entries by 'Creation date - ascending' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.CREATION_DATE_ASC, entriesList=self.sortEntriesByCreationDateAscending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to sort entries by 'Creation date - ascending' - when no search is made")
                return 
               
            writeToLog("INFO","Step 5: Going verify sort entries by 'Creation date - descending' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.CREATION_DATE_DESC, entriesList=self.sortEntriesByCreationDateDescending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to sort entries by 'Creation date - descending' - when no search is made")
                return  
               
            writeToLog("INFO","Step 6: Going verify sort entries by 'Alphabetical A-Z' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.ALPHABETICAL, entriesList=self.sortEntriesByAlphabeticalAToZ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to sort entries by 'Alphabetical A-Z' - when no search is made")
                return   
               
            writeToLog("INFO","Step 7: Going verify sort entries by 'Alphabetical Z-A' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.ALPHABETICAL_Z_A, entriesList=self.sortEntriesByAlphabeticalZToA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to sort entries by 'Alphabetical Z-A' - when no search is made")
                return                                      
   
            writeToLog("INFO","Step 8: Going verify sort entries by 'Likes' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.LIKES, entriesList=self.sortEntriesByLikes) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to sort entries by 'Likes' - when no search is made")
                return   
               
            writeToLog("INFO","Step 9: Going verify sort entries by 'Comments' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.COMMENTS, entriesList=self.SortEntriesByComments) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to sort entries by 'Comments' - when no search is made")
                return    
              
            writeToLog("INFO","Step 10: Going verify sort entries by 'Scheduling Ascending' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.SCHEDULING_ASC, entriesList=self.sortEntriesBySchedulingAscending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to sort entries by 'Scheduling Ascending' - when no search is made")
                return  
              
            writeToLog("INFO","Step 11: Going verify sort entries by 'Scheduling Descending' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(sortBy=enums.SortBy.SCHEDULING_DESC, entriesList=self.sortEntriesBySchedulingDescending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to sort entries by 'Scheduling Descending' - when no search is made")
                return          
            
            writeToLog("INFO","Step 12: Going verify sort entries by 'Update - Descending' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(enums.SortBy.UPDATE_DESC, entriesList=self.sortEntriesByUpdateDateDescending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to sort entries by 'Update - Descending' - when no search is made")
                return  
              
            writeToLog("INFO","Step 13: Going verify sort entries by 'Update - Ascending' - when no search is made")
            if self.common.channel.verifySortAndFiltersInPendingTab(enums.SortBy.UPDATE_ASC, entriesList=self.sortEntriesByUpdateDateAscending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to sort entries by 'Update - Ascending' - when no search is made")
                return                                                 
            ##################################################################
            writeToLog("INFO","TEST PASSED: Sort by in 'channel' - media tab - when no search is made was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 

            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')