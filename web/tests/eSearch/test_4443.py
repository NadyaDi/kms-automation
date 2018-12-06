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
    # Test Name : Filter by Captions - Dependency with other filters - My Media
    # Test description:
    # Verify that channel entries are properly displayed while using no search term and filter them by captions
    #================================================================================================================================
    testNum = "4443"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    userName = "admin"
    userPass = "123456"
    channelName = "Channel for eSearch"
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
            if self.common.channel.navigateToChannel(self.channelName, forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to the channel")
                return
            
            writeToLog("INFO","Step 2: Going to filter channel entries by: " + enums.Captions.ALL.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.ALL) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 2: FAILED to filter channel entries  by '" + enums.Captions.ALL.value + "'")
                    return
                
            writeToLog("INFO","Step 3: Going to verify channel entries filter by: " + enums.Captions.ALL.value)  
            if self.common.channel.verifyEntriesDisplay(self.filterByAll) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to verify channel entries  by '" + enums.Captions.ALL.value + "'")
                return
            
            writeToLog("INFO","Step 4: Going to close down the filters drop down menu") 
            if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to close the filters drop down menu")
                return False       
                 
            writeToLog("INFO","Step 5: Going to filter channel entries by: " + enums.Captions.AVAILABLE.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.AVAILABLE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 5: FAILED to filter channel entries  by '" + enums.Captions.AVAILABLE.value + "'")
                    return
                 
            writeToLog("INFO","Step 6: Going to verify channel entries filter by: " + enums.Captions.AVAILABLE.value)  
            if self.common.channel.verifyEntriesDisplay(self.filterByAvailable) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify channel entries  by '" + enums.Captions.AVAILABLE.value + "'")
                return
             
            writeToLog("INFO","Step 7: Going to clear all the search filters") 
            if self.common.base.click(self.common.myMedia.FILTERS_CLEAR_ALL_BUTTON, 20) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to clear all the search filters")
                return False 
             
            writeToLog("INFO", "Step 8: Going to wait for the filter changes")
            if self.common.general.waitForLoaderToDisappear() == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 8: FAILED to clear the filter changes")
                return
              
            writeToLog("INFO","Step 9: Going to close down the filters drop down menu") 
            if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to close the filters drop down menu")
                return
 
            writeToLog("INFO","Step 10: Going to filter channel entries by: " + enums.Captions.NOT_AVAILABLE.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.CAPTIONS, enums.Captions.NOT_AVAILABLE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 10: FAILED to filter channel entries  by '" + enums.Captions.NOT_AVAILABLE.value + "'")
                    return
                 
            writeToLog("INFO","Step 11: Going to verify channel entries filter by: " + enums.Captions.NOT_AVAILABLE.value)  
            if self.common.channel.verifyEntriesDisplay(self.filterByNotAvailable) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to verify channel entries  by '" + enums.Captions.NOT_AVAILABLE.value + "'")
                return               
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed in channel while using caption filters with no search term")
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