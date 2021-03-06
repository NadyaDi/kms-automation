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
    # Test Name : Filter by Captions - with search - Category page - media tab
    # Test description:
    # Verify that category entries are properly displayed while using a search term and filter them by captions
    #================================================================================================================================
    testNum = "4444"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    userName = "admin"
    userPass = "123456"
    categoryName = "eSearch category"
    entryName = "Filter by caption"
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
            
            # Entries and dictionaries
            self.entryName1 = "Filter by caption - with caption audio"
            self.entryName2 = "Filter by caption - with caption video"
            self.entryName3 = "Filter by caption - with caption quiz - Quiz"
            self.entryName4 = "Filter by caption - without caption youtube"
            self.entryName5 = "Filter by caption - without caption image"
            self.entryName6 = "Filter by caption - without caption audio2"
            self.entryName7 = "Filter by caption - without caption video2"
            self.entryName8 = "Filter by caption - without caption quiz2 - Quiz"
            
            self.filterByAvailable = {self.entryName1: True, self.entryName2: True, self.entryName3: True, self.entryName4: False, self.entryName5: False, self.entryName6: False, self.entryName7: False, self.entryName8: False}
            self.filterByNotAvailable = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryName4: True, self.entryName5: True, self.entryName6: True, self.entryName7: True, self.entryName8: True}
            self.filterByAll = {self.entryName1: True, self.entryName2: True, self.entryName3: True, self.entryName4: True, self.entryName5: True, self.entryName6: True, self.entryName7: True, self.entryName8: True}

            ##################### TEST STEPS - MAIN FLOW #####################               
            writeToLog("INFO","Step 1: Going to navigate to the channel")
            if self.common.category.navigateToCategory(self.categoryName, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to the channel")
                return
            
            writeToLog("INFO","Step 2: Going to navigate to search by " + self.entryName + " in category")
            if self.common.category.searchInCategoryWithoutVerifyResults(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to search by " + self.entryName + " in category")
                return
            
            writeToLog("INFO","Step 3: Going to filter category entries by: " + enums.Captions.ALL.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.ALL) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 3: FAILED to filter category entries  by '" + enums.Captions.ALL.value + "'")
                    return
                
            writeToLog("INFO","Step 4: Going to verify category entries filter by: " + enums.Captions.ALL.value)  
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.filterByAll) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify category entries  by '" + enums.Captions.ALL.value + "'")
                return
            
            writeToLog("INFO", "STEP 5: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 5: Failed to clear the search menu")
                return      
                
            writeToLog("INFO","Step 6: Going to filter category entries by: " + enums.Captions.AVAILABLE.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.AVAILABLE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 6: FAILED to filter category entries  by '" + enums.Captions.AVAILABLE.value + "'")
                    return
                
            writeToLog("INFO","Step 7: Going to verify category entries filter by: " + enums.Captions.AVAILABLE.value)  
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.filterByAvailable) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify category entries  by '" + enums.Captions.AVAILABLE.value + "'")
                return
            
            writeToLog("INFO", "STEP 8: Going to clear the filter search menu")
            if self.common.myMedia.filterClearAllWhenOpened() == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 8: Failed to clear the search menu")
                return

            writeToLog("INFO","Step 9: Going to filter category entries by: " + enums.Captions.NOT_AVAILABLE.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.NOT_AVAILABLE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED to filter category entries  by '" + enums.Captions.NOT_AVAILABLE.value + "'")
                    return
                
            writeToLog("INFO","Step 10: Going to verify category entries filter by: " + enums.Captions.NOT_AVAILABLE.value)  
            if self.common.globalSearch.verifyFiltersInGlobalPage(self.filterByNotAvailable) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to verify category entries  by '" + enums.Captions.NOT_AVAILABLE.value + "'")
                return    
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in category while using caption filters with a search term")
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