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
    # Test Name : Search in entry page - Captions
    # Test description:
    # Enters a caption entry that has four caption labels and verifies that the right elements are displayed for each label
    #================================================================================================================================
    testNum = "4439"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    userName = "admin"
    userPass = "123456"
    entryID = "1_nm3oq699"
    description = "Fields display - description"
    entryName = "Fields display - Captions"
    captionName = "Caption"
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
            labelNumber1 = (self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[0], self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[1].replace('LABEL', 'EN'))
            labelNumber2 = (self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[0], self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[1].replace('LABEL', 'LT'))
            labelNumber3 = (self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[0], self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[1].replace('LABEL', 'DE'))
            labelNumber4 = (self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[0], self.common.entryPage.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[1].replace('LABEL', 'IT'))
            labelList= ["EN", "LT", "DE", "IT"]
            searchElement1= "search 1"
            searchElement2= "search 2"
            searchElement3 = "search 3"
            searchElement4 = "search 4"
            allElements = "search"
            labelEntriesMap = {labelNumber1:searchElement1, labelNumber2:searchElement2, labelNumber3:searchElement3, labelNumber4:searchElement4}
            
            writeToLog("INFO","Step 1: Going to navigate to " + self.entryName + " entry page")
            if self.common.entryPage.navigateToEntry(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to " + self.entryName + " entry page")
                return 
                        
            writeToLog("INFO", "Step 2: Verify that the search results for " + self.captionName + "are properly displayed while using show less/all/more option")
            if self.common.entryPage.verifyFieldDisplayInEntryPageAfterMakingASearch(self.captionName, enums.EntryFields.CAPTIONS, 16) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 2: Failed, the search results for" + self.captionName + "are not properly displayed while using show less/all/more option")
                return 

            writeToLog("INFO", "Step 3: Verify that each caption label is displayed in the drop down menu")
            if self.common.entryPage.verifySearchDropDownLabels(self.captionName, labelList) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 3: FAILED to display each caption label in the drop down menu")
                return
            
            i = 4
            for entry in labelEntriesMap:
                i = i
                writeToLog("INFO", "Step " + str(i) + ": Verify that each caption label for " + str(entry) + " is displayed in the drop down menu") 
                if self.common.entryPage.searchLabelElements(self.captionName, entry, 4, labelEntriesMap[entry], allElements) == False:
                    self.status = "Fail"
                    writeToLog("INFO", "Step" + str(i) + ": Failed to display all the label caption for " + str(entry) + " in the container results")
                else:
                    i = i + 1
                    continue
                return                                                                     
            ##################################################################
            writeToLog("INFO","TEST PASSED: Verify that the specific label captions elements are displayed in the search results")
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