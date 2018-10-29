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
    # Create entries for search in tests
    #================================================================================================================================
    testNum = "7"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    userName1 = "inbar.willman@kaltura.com" # main user
    userPass1 = "Kaltura1!" 
    newDescription = 'Description'
    newTag = 'tag2,'
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
            self.entryForSearchIn1 = "Search in - Captions"
            self.entryForSearchIn2 = "Search in - All field"
            self.entryForSearchIn3 = "Search in - Details"
            self.entryForSearchIn4 = "Search in - Chapters/Slides"
            self.entryForSearchIn5 = "Search in - Quiz"
            self.entryForSearchIn6 = "Search in - Polls"
  
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
            self.sortEntriesByUpdatedDescending      = (self.entryForSortBy2, self.entryForSortBy3, self.entryForSortBy8, self.entryForSortBy1, self.entryForSortBy5,
                                                        self.entryForSortBy4, self.entryForSortBy7, self.entryForSortBy6)
            self.sortEntriesByUpdatedAscending       = (self.entryForSortBy6, self.entryForSortBy7, self.entryForSortBy4, self.entryForSortBy5, self.entryForSortBy1,
                                                        self.entryForSortBy8, self.entryForSortBy3, self.entryForSortBy2)
            ##################### TEST STEPS - MAIN FLOW #############################################################
            writeToLog("INFO","Going to add likes and comments to entries as: " + self.userName1 + " entries owner") 
            writeToLog("INFO","Step 1: Going to login with user " + self.userName1)
            if self.common.login.loginToKMS(self.userName1, self.userPass1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to login with " + self.userName1)
                return
                                  
            writeToLog("INFO","Step 2: Going navigate to entry '" + self.entryForSortBy2 + "'")    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy2, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED navigate to entry: " + self.entryForSortBy2)
                return 
                        
            writeToLog("INFO","Step 3: Going to update: " + self.entryForSortBy2)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy2, self.entryForSortBy2, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to update: " + self.entryForSortBy2)
                return   
           
            writeToLog("INFO","Step 4: Going navigate to entry: " + self.entryForSortBy3)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy3, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED navigate to entry: " + self.entryForSortBy3)
                return 
            
            writeToLog("INFO","Step 5: Going to update: " + self.entryForSortBy3)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy3, self.entryForSortBy3, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to update: " + self.entryForSortBy3)
                return    
            
            writeToLog("INFO","Step 6: Going navigate to entry: " + self.entryForSortBy8)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy8, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED navigate to entry: " + self.entryForSortBy8)
                return 
            
            writeToLog("INFO","Step 7: Going to update: " + self.entryForSortBy8)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy8, self.entryForSortBy8, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to update: " + self.entryForSortBy8)
                return               
                     
            writeToLog("INFO","Step 8: Going navigate to entry: " + self.entryForSortBy1)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy1, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED navigate to entry: " + self.entryForSortBy1)
                return 
            
            writeToLog("INFO","Step 9: Going to update: " + self.entryForSortBy1)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy1, self.entryForSortBy1, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to update: " + self.entryForSortBy1)
                return  
            
            writeToLog("INFO","Step 10: Going navigate to entry: " + self.entryForSortBy5)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy5, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED navigate to entry: " + self.entryForSortBy5)
                return 
            
            writeToLog("INFO","Step 11: Going to update: " + self.entryForSortBy5)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy5, self.entryForSortBy5, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to update: " + self.entryForSortBy5)
                return  
            
            writeToLog("INFO","Step 12: Going navigate to entry: " + self.entryForSortBy4)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy4, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED navigate to entry: " + self.entryForSortBy4)
                return 
            
            writeToLog("INFO","Step 13: Going to update: " + self.entryForSortBy4)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy4, self.entryForSortBy4, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to update: " + self.entryForSortBy4)
                return     
            
            writeToLog("INFO","Step 14: Going navigate to entry: " + self.entryForSortBy7)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy7, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED navigate to entry: " + self.entryForSortBy7)
                return 
            
            writeToLog("INFO","Step 15: Going to update: " + self.entryForSortBy7)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy7, self.entryForSortBy7, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to update: " + self.entryForSortBy7)
                return  
                                                                      
            writeToLog("INFO","Step 15: Going navigate to entry: " + self.entryForSortBy6)    
            if self.common.entryPage.navigateToEntry(self.entryForSortBy6, enums.Location.MY_MEDIA) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED navigate to entry: " + self.entryForSortBy6)
                return 
            
            writeToLog("INFO","Step 16: Going to update: " + self.entryForSortBy6)            
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSortBy6, self.entryForSortBy6, self.newDescription, self.newTag)== False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to update: " + self.entryForSortBy6)
                return                                                                        
 
            writeToLog("INFO","TEST PASSED: All entries were updated successfully") 
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