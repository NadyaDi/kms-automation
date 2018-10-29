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
    # Test Name : Setup test for eSearch
    # Test description:
    # Adding comments and likes to sort by entries as inbar.willman@kaltura.com - entries owner
    #================================================================================================================================
    testNum = "4"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!"
    userName2 = "private"
    userPass2 = "123456"
    userName3 = "admin"
    userPass3 = "123456"
    userName4 = "unmod"
    userPass4 = "123456"
    userName5 = "adminForEsearch"
    userPass5 = "123456" 
    userName6 = "privateForEsearch"
    userPass6 = "123456"    
    userName7 = "unmodForEsearch"
    userPass7 = "123456"   

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
            
            # Entries for sort by in my media/global search/add to channel/channel/gallery/new video quiz
            self.entryForSortBy1 = "Sort by - Sort A"
            self.entryForSortBy2 = "Sort by - Sort B"
            self.entryForSortBy3 = "Sort by - Sort C"
            self.entryForSortBy4 = "Sort by - Sort D"
            self.entryForSortBy5 = "Sort by - Sort E"
            self.entryForSortBy6 = "Sort by - Sort F"
            self.entryForSortBy7 = "Sort by - Sort G"
            self.entryForSortBy8 = "Sort by - Sort H"
            self.entryForSortBy9 = "Sort by Scheduling - Future"
            self.entryForSortBy10 = "Sort by Scheduling - In scheduling"
            self.entryForSortBy11 = "Sort by Scheduling - Past"
  
            # List of expected results for entries sort by
            self.sortEntriesByCreationDateDescending = (self.entryForSortBy8, self.entryForSortBy7, self.entryForSortBy6,self.entryForSortBy5, self.entryForSortBy4, 
                                                        self.entryForSortBy3, self.entryForSortBy2, self.entryForSortBy1)
            self.sortEntriesByCreationDateAscending  = (self.entryForSortBy1, self.entryForSortBy2, self.entryForSortBy3, self.entryForSortBy4, self.entryForSortBy5,
                                                        self.entryForSortBy6, self.entryForSortBy7, self.entryForSortBy8)
            self.sortEntriesByUpdateDateDescending   = ()
            self.sortEntriesByUpdateDateAscending    = ()
            self.sortEntriesByAlphabeticalAToZ       = (self.entryForSortBy1, self.entryForSortBy2, self.entryForSortBy3, self.entryForSortBy4, self.entryForSortBy4,
                                                        self.entryForSortBy5, self.entryForSortBy6, self.entryForSortBy7, self.entryForSortBy8)
            self.sortEntriesByAlphabeticalZToA       = (self.entryForSortBy8, self.entryForSortBy7, self.entryForSortBy6,self.entryForSortBy5, self.entryForSortBy4, 
                                                        self.entryForSortBy3, self.entryForSortBy2, self.entryForSortBy1)
            self.sortEntriesByLikes                  = (self.entryForSortBy6, self.entryForSortBy4, self.entryForSortBy8, self.entryForSortBy7, self.entryForSortBy3,
                                                        self.entryForSortBy5, self.entryForSortBy1, self.entryForSortBy2)
            self.sortEntriesByComments               = (self.entryForSortBy7, self.entryForSortBy6, self.entryForSortBy3, self.entryForSortBy5, self.entryForSortBy2,
                                                         self.entryForSortBy1, self.entryForSortBy4, self.entryForSortBy8)
            self.sortEntriesBySchedulingAscending    = (self.entryForSortBy9, self.entryForSortBy10, self.entryForSortBy11)
            self.sortEntriesBySchedulingDescending   = (self.entryForSortBy11, self.entryForSortBy10, self.entryForSortBy9)
            ##################### TEST STEPS - MAIN FLOW #############################################################
            writeToLog("INFO","Going to add likes and comments to entries as: " + self.userName1 + " entries owner") 
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
                                  
            writeToLog("INFO","Step 2: Going navigate to entry '" + self.entryForSortBy1 + "'")    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy1, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to entry: " + self.entryForSortBy1)
                return 
                         
            writeToLog("INFO","Step 3: Going to like entry: " + self.entryForSortBy1)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to like entry: " + self.entryForSortBy1)
                return   
                       
            sleep(2) 
            writeToLog("INFO","Step 4: Going to add comments to entry: " + self.entryForSortBy1)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to add comments to entry: " + self.entryForSortBy1)
                return    
                      
            writeToLog("INFO","Step 5: Going navigate to entry: " + self.entryForSortBy2)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy2, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED navigate to entry: " + self.entryForSortBy2)
                return 
             
            sleep(2)         
            writeToLog("INFO","Step 6: Going to add comments to entry: " + self.entryForSortBy2)            
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to add comment to entry: " + self.entryForSortBy2)
                return   
                      
            writeToLog("INFO","Step 7: Going navigate to entry: " + self.entryForSortBy3)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy3, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED navigate to entry: " + self.entryForSortBy3)
                return 
             
            writeToLog("INFO","Step 8: Going to like entry: " + self.entryForSortBy3)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to like entry: " + self.entryForSortBy3)
                return               
                      
            sleep(2) 
            writeToLog("INFO","Step 9: Going to add comments to entry: " + self.entryForSortBy3)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3", "Comment 4", "Comment 5"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to add comments to entry: " + self.entryForSortBy3)
                return    
                      
            writeToLog("INFO","Step 10: Going navigate to entry: " + self.entryForSortBy4)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy4, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED navigate to entry: " + self.entryForSortBy4)
                return 
                      
            writeToLog("INFO","Step 11: Going to like entry: " + self.entryForSortBy4)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to like entry: " + self.entryForSortBy4)
                return 
                      
            sleep(2) 
            writeToLog("INFO","Step 12: Going to add comment to entry: " + self.entryForSortBy4)  
            if self.common.entryPage.addComment("Comment 1") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to add comment to entry: " + self.entryForSortBy4)
                return   
              
            writeToLog("INFO","Step 13: Going navigate to entry: " + self.entryForSortBy5)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy5, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED navigate to entry: " + self.entryForSortBy5)
                return     
              
            writeToLog("INFO","Step 14: Going to like entry: " + self.entryForSortBy5)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to like entry: " + self.entryForSortBy5)
                return 
                      
            sleep(2) 
            writeToLog("INFO","Step 15: Going to add comment to entry: " + self.entryForSortBy5)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3", "Comment 4"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to add comment to entry: " + self.entryForSortBy5)
                return
             
            writeToLog("INFO","Step 16: Going navigate to entry: " + self.entryForSortBy6)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy6, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED navigate to entry: " + self.entryForSortBy6)
                return     
              
            writeToLog("INFO","Step 17: Going to like entry: " + self.entryForSortBy6)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to like entry: " + self.entryForSortBy6)
                return 
                      
            sleep(2) 
            writeToLog("INFO","Step 18: Going to add comment to entry: " + self.entryForSortBy6)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3", "Comment 4", "Comment 5", "Comment 6"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to add comment to entry: " + self.entryForSortBy6)
                return            
              
            writeToLog("INFO","Step 19: Going navigate to entry: " + self.entryForSortBy7)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy7, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED navigate to entry: " + self.entryForSortBy7)
                return     
              
            writeToLog("INFO","Step 20: Going to like entry: " + self.entryForSortBy7)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to like entry: " + self.entryForSortBy7)
                return 
            
            sleep(2) 
            writeToLog("INFO","Step 21: Going to add comment to entry: " + self.entryForSortBy7)  
            if self.common.entryPage.addComments(["Comment 1", "Comment 2", "Comment 3", "Comment 4", "Comment 5", "Comment 6", "Comment 7"]) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to add comment to entry: " + self.entryForSortBy7)
                return                        
                     
            writeToLog("INFO","Step 22: Going navigate to entry " + self.entryForSortBy8)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy8, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED navigate to entry: " + self.entryForSortBy8)
                return 
                        
            writeToLog("INFO","Step 23: Going to like entry: " + self.entryForSortBy8)            
            if self.common.entryPage.LikeUnlikeEntry(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to like entry: " + self.entryForSortBy8)
                return   
                                         
            writeToLog("INFO","TEST PASSED: All comments and likes were added successfully by entries owenr") 
            #################################################################################

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