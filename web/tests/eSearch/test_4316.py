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
    # Test Name : eSearch - Sort by - Add to channel - SR tab
    # Test description:
    # Upload entries with different sort by values
    # Go to Add to channel page, SR tab and make the next sorts (with and without search):
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
    testNum = "4316"
    
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
            self,self.driver = clsTestService.initialize(self, driverFix)
            self.common = Common(self.driver) 
            
            self.searchInAddToChannel = "Sort by"
            self.sRChannel = "SR-Channel for eSearch"
            self.channel = "Channel for eSearch"
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
            writeToLog("INFO","Step 1: Going to enable category scheduling module")
            if self.common.admin.enableCategoryScheduling(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to enable category scheduling module")
                return 
            
            writeToLog("INFO","Step 2: Going to login to KMS")
            if self.common.loginAsUser() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to login to KMS")
                return  
                        
            writeToLog("INFO","Step 3: Going to channel page")
            if self.common.channel.navigateToChannel(self.channel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to go to channel page")
                return 
            
            writeToLog("INFO","Step 4: Going to click on 'Add to channel' button")
            if self.common.base.click(self.common.channel.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to to click on 'Add to channel' button")
                return             
            
            writeToLog("INFO","Step 5: Going to navigate to SR tab")
            if self.common.channel.navigateToSrTabInAddToChannel(self.sRChannel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to to navigate to SR tab")
                return    
            
            writeToLog("INFO","Step 6: Going to verify default sort before making a search in SR tab")
            if self.common.channel.verifyChannelsDefaultSort(enums.SortBy.CREATION_DATE_DESC) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to displayed correct default sort before making a search in SR tab")
                return   
              
            writeToLog("INFO","Step 7: Going to make a search in 'Add to channel' - 'SR' tab")
            if self.common.channel.searchInAddToChannel(self.searchInAddToChannel, tabToSearcFrom=enums.AddToChannelTabs.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to make a search in 'Add to channel' - 'SR' tab")
                return 
               
            writeToLog("INFO","Step 8: Going to verify default sort after making a search")
            if self.common.channel.verifyChannelsDefaultSort(enums.SortBy.RELEVANCE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to displayed correct default sort after making a search")
                return                                                                                                           
                    
            writeToLog("INFO","Step 9: Going verify sort entries by 'Creation date - ascending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_ASC, self.sortEntriesByCreationDateAscending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to sort entries by 'Creation date - ascending' - when search is made")
                return 
                 
            writeToLog("INFO","Step 10: Going verify sort entries by 'Creation date - descending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_DESC, self.sortEntriesByCreationDateDescending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to sort entries by 'Creation date - descending' - when search is made")
                return  
                 
            writeToLog("INFO","Step 11: Going verify sort entries by 'Alphabetical A-Z' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL, self.sortEntriesByAlphabeticalAToZ, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to sort entries by 'Alphabetical A-Z' - when search is made")
                return   
                 
            writeToLog("INFO","Step 12: Going verify sort entries by 'Alphabetical Z-A' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL_Z_A, self.sortEntriesByAlphabeticalZToA, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to sort entries by 'Alphabetical Z-A' - when search is made")
                return                                      
     
            writeToLog("INFO","Step 13: Going verify sort entries by 'Likes' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.LIKES, self.sortEntriesByLikes, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to sort entries by 'Likes' - when search is made")
                return   
                 
            writeToLog("INFO","Step 14: Going verify sort entries by 'Comments' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.COMMENTS, self.SortEntriesByComments, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to sort entries by 'Comments' - when search is made")
                return
               
            writeToLog("INFO","Step 15: Going verify sort entries by 'Scheduling Ascending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_ASC, self.sortEntriesBySchedulingAscending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to sort entries by 'Scheduling Ascending' - when search is made")
                return  
                  
            writeToLog("INFO","Step 16: Going verify sort entries by 'Scheduling Descending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_DESC, self.sortEntriesBySchedulingDescending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to sort entries by 'Scheduling Descending' - when search is made")
                return  
             
            writeToLog("INFO","Step 17: Going verify sort entries by 'Update - Descending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.UPDATE_DESC, self.sortEntriesByUpdateDateDescending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to sort entries by 'Update - Descending' - when search is made")
                return  
             
            writeToLog("INFO","Step 18: Going verify sort entries by 'Update - Ascending' - when search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.UPDATE_ASC, self.sortEntriesByUpdateDateAscending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to sort entries by 'Update - Ascending' - when search is made")
                return 
  
            writeToLog("INFO","Step 19: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel(tab=enums.AddToChannelTabs.SHARED_REPOSITORY) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to clear search")
                return 
              
            writeToLog("INFO","Step 20: Going verify sort entries by 'Creation date - ascending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_ASC, self.sortEntriesByCreationDateAscending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to sort entries by 'Creation date - ascending' - when no search is made")
                return 
               
            writeToLog("INFO","Step 21: Going verify sort entries by 'Creation date - descending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.CREATION_DATE_DESC, self.sortEntriesByCreationDateDescending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to sort entries by 'Creation date - descending' - when no search is made")
                return  
               
            writeToLog("INFO","Step 22: Going verify sort entries by 'Alphabetical A-Z' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL, self.sortEntriesByAlphabeticalAToZ, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to sort entries by 'Alphabetical A-Z' - when no search is made")
                return   
               
            writeToLog("INFO","Step 23: Going verify sort entries by 'Alphabetical Z-A' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.ALPHABETICAL_Z_A, self.sortEntriesByAlphabeticalZToA, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to sort entries by 'Alphabetical Z-A' - when no search is made")
                return                                      
   
            writeToLog("INFO","Step 24: Going verify sort entries by 'Likes' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.LIKES, self.sortEntriesByLikes, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to sort entries by 'Likes' - when no search is made")
                return   
               
            writeToLog("INFO","Step 25: Going verify sort entries by 'Comments' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.COMMENTS, self.SortEntriesByComments, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED to sort entries by 'Comments' - when no search is made")
                return    
              
            writeToLog("INFO","Step 26: Going verify sort entries by 'Scheduling Ascending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_ASC, self.sortEntriesBySchedulingAscending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED to sort entries by 'Scheduling Ascending' - when no search is made")
                return  
              
            writeToLog("INFO","Step 27: Going verify sort entries by 'Scheduling Descending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.SCHEDULING_DESC, self.sortEntriesBySchedulingDescending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED to sort entries by 'Scheduling Descending' - when no search is made")
                return         
             
            writeToLog("INFO","Step 28: Going verify sort entries by 'Update - Descending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.UPDATE_DESC, self.sortEntriesByUpdateDateDescending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED to sort entries by 'Update - Descending' - when search is made")
                return  
            
            writeToLog("INFO","Step 29: Going verify sort entries by 'Update - Ascending' - when no search is made")
            if self.common.channel.verifySortInAddToChannel(enums.SortBy.UPDATE_ASC, self.sortEntriesByUpdateDateAscending, searchIn=enums.Location.ADD_TO_CHANNEL_SR) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED to sort entries by 'Update - Ascending' - when no search is made")
                return                                                                  
            ##################################################################
            writeToLog("INFO","TEST PASSED: Sort by in 'Add to channel - SR tab' was done successfully")
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