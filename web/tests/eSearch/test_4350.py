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
    # Test Name : eSearch - Search In - channel - media tab
    # Test description:
    # Upload entries with different cue points fields
    # Go channel page, media tab, make a search, and filter entries by 'Search in' drop down:
    #    1. Search in: All Fields 
    #    2. Search in: Details 
    #    3. Search in: Chapters/Slides
    #    4. Search in: Captions
    #    5. Search in: Quiz
    #    6. Search in: Comments
    #    7. Search in: Polls
    #================================================================================================================================
    testNum = "4350"
    
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
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver) 
            
            self.searchInchannel = "searchIn"
            self.channel = "Channel for eSearch"
            
            self.entryForSearchIn1 = "Search in - Captions"
            self.entryForSearchIn2 = "Search in - All field"
            self.entryForSearchIn3 = "Search in - Details"
            self.entryForSearchIn4 = "Search in - Chapters/Slides"
            self.entryForSearchIn5 = "Search in" # Will be quiz
            self.entryForSearchIn6 = "Search in - Webcast" # Created manually
            self.entryForSearchIn7 = "Search in - Quiz" # name of searchIn5 after creating quiz
            
            self.searchInAllFields = {self.entryForSearchIn1:True, self.entryForSearchIn2:True, self.entryForSearchIn3:True, self.entryForSearchIn4:True, self.entryForSearchIn6:True, self.entryForSearchIn7:True}
            self.searchInDeatails = {self.entryForSearchIn1:False, self.entryForSearchIn2:True, self.entryForSearchIn3:True, self.entryForSearchIn4:False, self.entryForSearchIn6:False, self.entryForSearchIn7:True}
            self.searchInChaptersAndSlides = {self.entryForSearchIn1:False, self.entryForSearchIn2:True, self.entryForSearchIn3:False, self.entryForSearchIn4:True, self.entryForSearchIn6:False, self.entryForSearchIn7:True}
            self.SearchIncaptions = {self.entryForSearchIn1:True, self.entryForSearchIn2:True,self.entryForSearchIn3:False, self.entryForSearchIn4:False, self.entryForSearchIn6:False, self.entryForSearchIn7:True}
            self.searchInPolls = {self.entryForSearchIn1:False, self.entryForSearchIn2:False, self.entryForSearchIn3:False, self.entryForSearchIn4:False, self.entryForSearchIn6:True, self.entryForSearchIn7:False}
            self.searchInQuiz = {self.entryForSearchIn1:False, self.entryForSearchIn2:False, self.entryForSearchIn3:False, self.entryForSearchIn4:False, self.entryForSearchIn6:False, self.entryForSearchIn7:True}
            self.searchInComments = {self.entryForSearchIn1:False, self.entryForSearchIn2:True, self.entryForSearchIn3:False, self.entryForSearchIn4:False, self.entryForSearchIn6:False, self.entryForSearchIn7:True}
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to channel page")
            if self.common.channel.navigateToChannel(self.channel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to go to channel page")
                return 
            
            writeToLog("INFO","Step 2: Going to verify that 'search in' dropdown is disabled before search")
            if self.common.myMedia.verifySearchInDropDownState(False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to verify that 'search in' dropdown is disabled before search")
                return  
             
            writeToLog("INFO","Step 3: Going to make a search in channel- Media tab")
            if self.common.channel.searchInChannelWithoutVerifyResults(self.searchInchannel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to make a search in channel- Media tab")
                return          
            
            writeToLog("INFO","Step 4: Going to verify that 'search in' dropdown is enable after making a search")
            if self.common.myMedia.verifySearchInDropDownState(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify that 'search in' dropdown is enable after making a search")
                return  
            
            writeToLog("INFO","Step 5: Going to select 'search in' option: " + enums.SearchInDropDown.QUIZ.value)
            if self.common.myMedia.selectSearchInDropDownOption(option=enums.SearchInDropDown.QUIZ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to select 'search in' option: " + enums.SearchInDropDown.QUIZ.value)
                return              
            
            writeToLog("INFO","Step 6: Going to verify the correct entries are displayed in results")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.searchInQuiz) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to displayed correct entries in results")
                return  
            
            writeToLog("INFO","Step 7: Going to select 'search in' option: " + enums.SearchInDropDown.ALL_FIELDS.value)
            if self.common.myMedia.selectSearchInDropDownOption(option=enums.SearchInDropDown.ALL_FIELDS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to select 'search in' option: " + enums.SearchInDropDown.ALL_FIELDS.value)
                return              
            
            writeToLog("INFO","Step 8: Going to verify the correct entries are displayed in results")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.searchInAllFields) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to displayed correct entries in results")
                return    
            
            writeToLog("INFO","Step 9: Going to select 'search in' option: " + enums.SearchInDropDown.DETAILS.value)
            if self.common.myMedia.selectSearchInDropDownOption(option=enums.SearchInDropDown.DETAILS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to select 'search in' option: " + enums.SearchInDropDown.DETAILS.value)
                return              
            
            writeToLog("INFO","Step 10: Going to verify the correct entries are displayed in results")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.searchInDeatails) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to displayed correct entries in results")
                return               
            
            writeToLog("INFO","Step 11: Going to select 'search in' option: " + enums.SearchInDropDown.CHAPTERS_AND_SLIDES.value)
            if self.common.myMedia.selectSearchInDropDownOption(option=enums.SearchInDropDown.CHAPTERS_AND_SLIDES) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to select 'search in' option: " + enums.SearchInDropDown.CHAPTERS_AND_SLIDES.value)
                return              
            
            writeToLog("INFO","Step 12: Going to verify the correct entries are displayed in results")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.searchInChaptersAndSlides) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to displayed correct entries in results")
                return               
                        
            writeToLog("INFO","Step 13: Going to select 'search in' option: " + enums.SearchInDropDown.CAPTIONS.value)
            if self.common.myMedia.selectSearchInDropDownOption(option=enums.SearchInDropDown.CAPTIONS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to select 'search in' option: " + enums.SearchInDropDown.CAPTIONS.value)
                return              
            
            writeToLog("INFO","Step 14: Going to verify the correct entries are displayed in results")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.SearchIncaptions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to displayed correct entries in results")
                return      

            writeToLog("INFO","Step 15: Going to select 'search in' option: " + enums.SearchInDropDown.POLLS.value)
            if self.common.myMedia.selectSearchInDropDownOption(option=enums.SearchInDropDown.POLLS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to select 'search in' option: " + enums.SearchInDropDown.POLLS.value)
                return              
            
            writeToLog("INFO","Step 16: Going to verify the correct entries are displayed in results")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.searchInPolls) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to displayed correct entries in results")
                return            
            
            writeToLog("INFO","Step 17: Going to select 'search in' option: " + enums.SearchInDropDown.COMMENTS.value)
            if self.common.myMedia.selectSearchInDropDownOption(option=enums.SearchInDropDown.COMMENTS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to select 'search in' option: " + enums.SearchInDropDown.COMMENTS.value)
                return              
            
            writeToLog("INFO","Step 18: Going to verify the correct entries are displayed in results")
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.searchInComments) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to displayed correct entries in results")
                return   
            
            writeToLog("INFO","Step 19: Going to clear search")
            if self.common.myMedia.clearSearch() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to clear search")
                return  
            
            writeToLog("INFO","Step 20: Going to verify 'search in' dropdown is disabled after clearing search")
            if self.common.myMedia.verifySearchInDropDownState(False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to dosabled 'search in' dropdown is disabled after clearing search")
                return                          
            ##################################################################
            writeToLog("INFO","TEST PASSED: Search in channel - media tab done successfully")
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