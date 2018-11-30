import time, pytest
import sys,os
from _ast import Num
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums 



class Test:
    
    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Search in entry page - Polls - webcast
    # Test description:
    # Enter an entry and verify that the proper elements are displayed in the search result while being in show less and show more screen
    # Enter a specific entry - Media tab , make a search that matches multiple values in field, and check for field display in results
    #    1. Description
    #    2. Polls
    #================================================================================================================================
    testNum = "4438"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    userName = "admin"
    userPass = "123456"
    entryID = "1_nm3oq699"
    description = "Fields display - description"
    entryName = "Fields display - multiple polls"
    pollName = "Polls"
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
            
            # Searches in page
            self.searchInMultipleCaptions = "multiple captions"
            self.searchInMultipleTags = "multiple tags"
            self.searchInMultipleSlides = "multiple slides"
            self.searchInMultipleChapters = "multiple chapters" 
            self.searchInMultipleQuiz = "multiple quiz"      
            self.searchInMultipleComments = "multiple comments" 
            self.searchInMultiplePolls = "multiple polls"    
            self.searchInMultipleDetails = "multiple customdata"                           
                                   
            # Fields number of display
            self.captionsNumOfDisplay = 7
            self.tagsNumOfDisplay = 6
            self.quizNumOfDisplay = 6
            self.slidesNumOfDisplay = 8
            self.chapersNumOfDisplay = 6
            self.commentsNumOfDisplay = 6
            self.pollsNumOfDisplay = 6
            self.detailsNumOfDisplay = 11
            
            # Entry details
            self.entryOwner = "Inbar will"
            self.categoriesList = ["eSearch category", "Channel for eSearch", "SR-Channel for eSearch"]
            
            # Entries
            self.entryForFieldsDisplay1 = "Fields display - Name"
            self.entryForFieldsDisplay2 = "Fields display - Description"
            self.entryForFieldsDisplay3 = "Fields display - All Fields - single - Quiz" # Created from self.entryForFieldsDisplay3
            self.entryForFieldsDisplay4 = "Fields display - All Fields - multiple - Quiz" # Created from self.entryForFieldsDisplay4
            self.entryForFieldsDisplay5 = "Fields display - multiple polls" # Created manually  
            
            ##################### TEST STEPS - MAIN FLOW #####################   
            writeToLog("INFO","Step 1: Going to navigate to " + self.entryName + " entry page")
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to " + self.entryName + " entry page")
                return 
            
            writeToLog("INFO", "Step 2: Going to verify that the " + self.description + " are not displayed in the search results")
            if self.common.entryPage.verifyEntryNameAndDescriptionInSearch(self.description) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 2: " + self.description + "are displayed in the search results")
                return
                        
            writeToLog("INFO", "Step 3: Verify that the search results for " + self.pollName + "are properly displayed while using show less/all/more option")
            if self.common.entryPage.verifyFieldDisplayInEntryPageAfterMakingASearch(self.pollName, enums.EntryFields.POLLS, 6) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 3: Failed, the search results for" + self.pollName + "are not properly displayed while using show less/all/more option")
                return                                                           
            ##################################################################
            writeToLog("INFO","TEST PASSED: Verify that multiple elements are properly displayed in the search results from an entry page")
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