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
    # Verify that the caption filters are available when proper media type is selected
    #================================================================================================================================
    testNum = "4441"
    
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
            ##################### TEST STEPS - MAIN FLOW #####################
            entryName1 = enums.MediaType.QUIZ
            entryName2 = enums.MediaType.AUDIO
            entryName3 = enums.MediaType.VIDEO
            entryName4 = enums.MediaType.IMAGE
            entryName5 = enums.MediaType.WEBCAST_EVENTS
            entryName1Value = enums.MediaType.QUIZ.value
            entryName2Value = enums.MediaType.AUDIO.value
            entryName3Value = enums.MediaType.VIDEO.value
            entryName4Value = enums.MediaType.IMAGE.value
            entryName5Value = enums.MediaType.WEBCAST_EVENTS.value     
            entriesWithCaptions = {entryName1:entryName1Value, entryName2:entryName2Value, entryName3:entryName3Value, entryName5:entryName5Value}
            entrieWithoutCaptions = {entryName4:entryName4Value}
               
            writeToLog("INFO","Step 1: Going to navigate to my media page")
            if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to my media page")
                return
            i = 1
            for entry in entriesWithCaptions:
                i = i + 1
                writeToLog("INFO","Step " + str(i) + ": Going to filter my media entries by: " + entriesWithCaptions[entry]) 
                if self.common.isElasticSearchOnPage() == True:
                    if self.common.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, entry) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i) + ": FAILED to filter my media entries  by '" + entriesWithCaptions[entry] + "'")
                        return            
                      
                writeToLog("INFO","Step " + str(i + 1)  + ": Going to verify that the caption options are available") 
                tmpEntry = (self.common.myMedia.CAPTION_FILTER_INACTIVE[0], self.common.myMedia.CAPTION_FILTER_INACTIVE[1].replace('DROPDOWNLIST_ITEM', "Not Available undefined")) 
                if self.common.base.click(tmpEntry, timeout=3) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 1)  + ": FAILED to identify captions filters")
                    return
                  
                writeToLog("INFO","Step " + str(i + 2)  + ": Going to verify that the caption filter is clickable") 
                if self.common.base.wait_visible(tmpEntry, timeout=3) != False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 2)  + "FAILED, the caption filter option is not clickable")
                    return
                  
                writeToLog("INFO","Step " + str(i + 3)  + ": Going to clear all the search filters") 
                if self.common.base.click(self.common.myMedia.FILTERS_CLEAR_ALL_BUTTON, 20) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 3)  + ": FAILED to clear all the search filters")
                    return 
                   
                writeToLog("INFO","Step " + str(i + 4)  + ": Going to close down the filters drop down menu") 
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 4)  + ": FAILED to close the filters drop down menu")
                    return
                
                i = i + 4
                
            i = i - 1    
            for entry in entrieWithoutCaptions:
                i = i + 1 
                writeToLog("INFO","Step " + str(i + 1)  + ": Going to filter my media entries by: " + entrieWithoutCaptions[entry]) 
                if self.common.isElasticSearchOnPage() == True:
                    if self.common.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, entry) == False:
                        self.status = "Fail"
                        writeToLog("INFO","Step " + str(i + 1)  + ": FAILED to filter my media entries  by '" + entrieWithoutCaptions[entry] + "'")
                        return            
                    
                writeToLog("INFO","Step " + str(i + 2)  + ": Going to verify that the caption options are available") 
                tmpEntry = (self.common.myMedia.CAPTION_FILTER_INACTIVE[0], self.common.myMedia.CAPTION_FILTER_INACTIVE[1].replace('DROPDOWNLIST_ITEM', "Not Available undefined")) 
                if self.common.base.click(tmpEntry, timeout=3) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 2)  + ": FAILED to identify captions filters")
                    return
                
                writeToLog("INFO","Step " + str(i + 3)  + ": Going to verify that the caption filter has functionality") 
                if self.common.base.is_visible(tmpEntry) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 3)  + ": FAILED, the caption filter does not have functionality")
                    return
                
                writeToLog("INFO","Step " + str(i + 4)  + ": Going to clear all the search filters") 
                if self.common.base.click(self.common.myMedia.FILTERS_CLEAR_ALL_BUTTON, 20) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 4)  + ": FAILED to clear all the search filters")
                    return 
                 
                writeToLog("INFO","Step " + str(i + 5)  + ": Going to close down the filters drop down menu") 
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(i + 5)  + ": FAILED to close the filters drop down menu")
                    return
                i = i + 5
            ##################################################################
            writeToLog("INFO","TEST PASSED: All the entries are properly displayed while using caption filters without a search term")
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