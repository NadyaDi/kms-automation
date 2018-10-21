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
    # Test Name : eSearch - Sort by - Add to gallery - My media tab
    # Test description:
    # Upload entries with different sort by values
    # Go to Add to gallery page, my media tab and make the next sorts (with and without search):
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
    testNum = "4318"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
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
            
            self.searchInAddToChannel = "C160E832-1-Sort by"
            self.gallery = "Apps Automation Category"
            self.sortEntriesByCreationDateDescending = ("C160E832-1-Sort by - Sort H", "C160E832-1-Sort by - Sort G", "C160E832-1-Sort by - Sort F", "C160E832-1-Sort by - Sort E", "C160E832-1-Sort by - Sort D", 
                                                        "C160E832-1-Sort by - Sort C", "C160E832-1-Sort by - Sort B", "C160E832-1-Sort by - Sort A")
            self.sortEntriesByCreationDateAscending  = ("C160E832-1-Sort by - Sort A", "C160E832-1-Sort by - Sort B", "C160E832-1-Sort by - Sort C", "C160E832-1-Sort by - Sort D", "C160E832-1-Sort by - Sort E",
                                                        "C160E832-1-Sort by - Sort F", "C160E832-1-Sort by - Sort G", "C160E832-1-Sort by - Sort H")
            self.sortEntriesByUpdateDateDescending   = ()
            self.sortEntriesByUpdateDateAscending    = ()
            self.sortEntriesByAlphabeticalAToZ       = ("C160E832-1-Sort by - Sort A", "C160E832-1-Sort by - Sort B", "C160E832-1-Sort by - Sort C", "C160E832-1-Sort by - Sort D", "C160E832-1-Sort by - Sort E",
                                                       "C160E832-1-Sort by - Sort F", "C160E832-1-Sort by - Sort G", "C160E832-1-Sort by - Sort H")
            self.sortEntriesByAlphabeticalZToA       = ("C160E832-1-Sort by - Sort H", "C160E832-1-Sort by - Sort G", "C160E832-1-Sort by - Sort F","C160E832-1-Sort by - Sort E", "C160E832-1-Sort by - Sort D", 
                                                        "C160E832-1-Sort by - Sort C", "C160E832-1-Sort by - Sort B", "C160E832-1-Sort by - Sort A")
            self.sortEntriesByLikes                   = ("C160E832-1-Sort by - Sort F", "C160E832-1-Sort by - Sort D", "C160E832-1-Sort by - Sort H", "C160E832-1-Sort by - Sort G", "C160E832-1-Sort by - Sort C", 
                                                        "C160E832-1-Sort by - Sort E", "C160E832-1-Sort by - Sort A", "C160E832-1-Sort by - Sort B")
            self.SortEntriesByComments               = ("C160E832-1-Sort by - Sort G", "C160E832-1-Sort by - Sort F", "C160E832-1-Sort by - Sort C", "C160E832-1-Sort by - Sort E", "C160E832-1-Sort by - Sort B", 
                                                        "C160E832-1-Sort by - Sort A", "C160E832-1-Sort by - Sort D", "C160E832-1-Sort by - Sort H")
            self.sortEntriesBySchedulingAscending    = ("C160E832-1-Sort by Scheduling - Past", "C160E832-1-Sort by Scheduling - In scheduling", "C160E832-1-Sort by Scheduling - Future")
            self.sortEntriesBySchedulingDescending   = ("C160E832-1-Sort by Scheduling - Future", "C160E832-1-Sort by Scheduling - In scheduling", "C160E832-1-Sort by Scheduling - Past")
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to gallery page")
            if self.common.category.navigateToCategory(self.gallery) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to go to gallery page")
                return 
            
            writeToLog("INFO","Step 2: Going to click on 'Add to Gallery' button")
            if self.common.base.click(self.common.channel.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to to click on 'Add to Gallery' button")
                return             
             
            writeToLog("INFO","Step 3: Going to verify default sort before making a search")
            if self.common.channel.verifyChannelsDefaultSort(enums.SortBy.CREATION_DATE_DESC) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to displayed correct default sort before making a search")
                return   
               
            writeToLog("INFO","Step 4: Going to make a search in 'Add to Gallery' - 'My Media' tab")
            if self.common.channel.searchInAddToChannel(self.searchInAddToChannel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to make a search in 'Add to Gallery' - 'My Media' tab")
                return 
               
            writeToLog("INFO","Step 5: Going to verify default sort after making a search")
            if self.common.channel.verifyChannelsDefaultSort(enums.SortBy.RELEVANCE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to displayed correct default sort after making a search")
                return                                                                                                           
                   
            writeToLog("INFO","Step 6: Going verify sort entries by 'Creation date - ascending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_ASC, self.sortEntriesByCreationDateAscending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to sort entries by 'Creation date - ascending' - when search is made")
                return 
                
            writeToLog("INFO","Step 7: Going verify sort entries by 'Creation date - descending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_DESC, self.sortEntriesByCreationDateDescending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to sort entries by 'Creation date - descending' - when search is made")
                return  
                
            writeToLog("INFO","Step 8: Going verify sort entries by 'Alphabetical A-Z' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL, self.sortEntriesByAlphabeticalAToZ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to sort entries by 'Alphabetical A-Z' - when search is made")
                return   
                
            writeToLog("INFO","Step 9: Going verify sort entries by 'Alphabetical Z-A' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL_Z_A, self.sortEntriesByAlphabeticalZToA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to sort entries by 'Alphabetical Z-A' - when search is made")
                return                                      
    
            writeToLog("INFO","Step 10: Going verify sort entries by 'Likes' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.LIKES, self.sortEntriesByLikes) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to sort entries by 'Likes' - when search is made")
                return   
                
            writeToLog("INFO","Step 11: Going verify sort entries by 'Comments' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.COMMENTS, self.SortEntriesByComments) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to sort entries by 'Comments' - when search is made")
                return
               
            writeToLog("INFO","Step 12: Going verify sort entries by 'Scheduling Ascending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_ASC, self.sortEntriesBySchedulingAscending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to sort entries by 'Scheduling Ascending' - when search is made")
                return  
                
            writeToLog("INFO","Step 13: Going verify sort entries by 'Scheduling Descending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_DESC, self.sortEntriesBySchedulingDescending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to sort entries by 'Scheduling Descending' - when search is made")
                return  
  
            writeToLog("INFO","Step 14: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to clear search")
                return 
             
            writeToLog("INFO","Step 15: Going verify sort entries by 'Creation date - ascending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_ASC, self.sortEntriesByCreationDateAscending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to sort entries by 'Creation date - ascending' - when no search is made")
                return 
              
            writeToLog("INFO","Step 16: Going verify sort entries by 'Creation date - descending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_DESC, self.sortEntriesByCreationDateDescending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to sort entries by 'Creation date - descending' - when no search is made")
                return  
              
            writeToLog("INFO","Step 17: Going verify sort entries by 'Alphabetical A-Z' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL, self.sortEntriesByAlphabeticalAToZ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to sort entries by 'Alphabetical A-Z' - when no search is made")
                return   
              
            writeToLog("INFO","Step 18: Going verify sort entries by 'Alphabetical Z-A' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL_Z_A, self.sortEntriesByAlphabeticalZToA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to sort entries by 'Alphabetical Z-A' - when no search is made")
                return                                      
  
            writeToLog("INFO","Step 19: Going verify sort entries by 'Likes' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.LIKES, self.sortEntriesByLikes) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to sort entries by 'Likes' - when no search is made")
                return   
              
            writeToLog("INFO","Step 20: Going verify sort entries by 'Comments' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.COMMENTS, self.SortEntriesByComments) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to sort entries by 'Comments' - when no search is made")
                return    
             
            writeToLog("INFO","Step 21: Going verify sort entries by 'Scheduling Ascending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_ASC, self.sortEntriesBySchedulingAscending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to sort entries by 'Scheduling Ascending' - when no search is made")
                return  
             
            writeToLog("INFO","Step 22: Going verify sort entries by 'Scheduling Descending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_DESC, self.sortEntriesBySchedulingDescending) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to sort entries by 'Scheduling Descending' - when no search is made")
                return                                            
            ##################################################################
            writeToLog("INFO","TEST PASSED: Sort by in 'Add to gallery - My Media tab' was done successfully")
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
#             sleep(2)
#             self.common.login.logOutOfKMS()
#             self.common.login.loginToKMS(self.userName1, self.userPass1)                   
#             for i in range(1,5):
#                 self.common.channel.deleteChannel(eval('self.channelName'+str(i)))
#      
#             self.common.myMedia.deleteEntriesFromMyMedia([self.entryName1, self.entryName2, self.entryName3])   
            writeToLog("INFO","**************** Ended: teardown_method *******************")            
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')