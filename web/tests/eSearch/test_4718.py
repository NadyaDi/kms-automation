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
    #  @Author: oded berihon
    # Test Name : eSearch - Filter by media type in channel page  
    # Test description:
    # Upload all types of entries and sort them by their type
    # Go to my media page and sort the entries (with and without search):
    #    1. Sort by media type - only video type should be displayed in the results 
    #    2. Sort by audio type - only audio type should be displayed in the results .
    #    3. Sort by image type - only image type should be displayed in the results.
    #    4. Sort by quiz type - only quiz type should be displayed in the results.
    #    5. Sort by webcast type - only webcast type should be displayed in the results
    #
    #================================================================================================================================
    testNum = "4718"
    
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
            self.entryName1 = "Sort by media type - image"
            self.entryName2 = "Sort by media type - audio"
            self.entryName3 = "Sort by media type - video"
            self.entryNameQuiz = "Sort by media type - Quiz"
            
            self.channelForEsearch  = "Channel for eSearch"
            
            self.filterByImage = {self.entryName1: True, self.entryName2: False, self.entryName3: False, self.entryNameQuiz: False}
            self.filterByAudio = {self.entryName1: False, self.entryName2: True, self.entryName3: False, self.entryNameQuiz: False}
            self.filterByVideo = {self.entryName1: False, self.entryName2: False, self.entryName3: True, self.entryNameQuiz: False}
            self.filterByQuiz = {self.entryName1: False, self.entryName2: False, self.entryName3: False, self.entryNameQuiz: True}
            ##################### TEST STEPS - MAIN FLOW ##################### 

                        
            writeToLog("INFO","Step 2: Going to navigate to my media page")
            if self.common.channel.navigateToChannel(self.channelForEsearch) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to go to navigate my media page")
                return      
                                    
            sleep(1)
#             New UI only !! this parameter will be clicked after every filter search so each filter will only have only the chosen type 
            tmpType = (self.common.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.common.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace("DROPDOWNLIST_ITEM", enums.MediaType.ALL_MEDIA.value))
            writeToLog("INFO","Step 3: Going to filter channel entries by: " + enums.MediaType.IMAGE.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, enums.MediaType.IMAGE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 3: FAILED to filter channel entries  by '" + enums.MediaType.IMAGE.value + "'")
                    return
                
            writeToLog("INFO","Step 4: Going to verify channel entries filter by: " + enums.MediaType.IMAGE.value)  
            if self.common.channel.verifyEntriesDisplay(self.filterByImage, verifyIn=enums.Location.CHANNEL_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify channel entries  by '" + enums.MediaType.IMAGE.value + "'")
                return

            writeToLog("INFO","Step 5: Going to verify that only entries with " + enums.MediaType.IMAGE.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryName1], enums.MediaType.IMAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to filter and verify my media entries  by '" + enums.MediaType.IMAGE.value + "'")
                return  
            
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpType, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Media Type' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False
             
            sleep(1)
            writeToLog("INFO","Step 6: Going to filter my media entries by: " + enums.MediaType.AUDIO.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, enums.MediaType.AUDIO) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 6: FAILED to filter my media entries  by '" + enums.MediaType.AUDIO.value + "'")
                    return
                 
            writeToLog("INFO","Step 7: Going to verify my media entries filter by: " + enums.MediaType.AUDIO.value)  
            if self.common.channel.verifyEntriesDisplay(self.filterByAudio, verifyIn=enums.Location.CHANNEL_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify my media entries  by '" + enums.MediaType.AUDIO.value + "'")
                return
            
            writeToLog("INFO","Step 8: Going to verify that only entries with " + enums.MediaType.AUDIO.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryName2], enums.MediaType.AUDIO) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to filter and verify my media entries  by '" + enums.MediaType.AUDIO.value + "'")
                return        
              
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpType, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Media Type' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False
                 
            sleep(1)
            writeToLog("INFO","Step 9: Going to filter my media entries by: " + enums.MediaType.VIDEO.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, enums.MediaType.VIDEO) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 9: FAILED to filter my media entries  by '" + enums.MediaType.VIDEO.value + "'")
                    return
                 
            writeToLog("INFO","Step 10: Going to verify my media entries filter by: " + enums.MediaType.VIDEO.value)  
            if self.common.channel.verifyEntriesDisplay(self.filterByVideo, verifyIn=enums.Location.CHANNEL_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to verify my media entries  by '" + enums.MediaType.VIDEO.value + "'")
                return 
            
            writeToLog("INFO","Step 11: Going to verify that only entries with " + enums.MediaType.VIDEO.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryName3], enums.MediaType.VIDEO) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to filter and verify my media entries  by '" + enums.MediaType.VIDEO.value + "'")
                return                          
                  
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpType, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Media Type' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False            
               
            sleep(1)
            writeToLog("INFO","Step 12: Going to filter my media entries by: " + enums.MediaType.QUIZ.value) 
            if self.common.isElasticSearchOnPage() == True:
                if self.common.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, enums.MediaType.QUIZ) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 12: FAILED to filter my media entries  by '" + enums.MediaType.QUIZ.value + "'")
                    return
                 
            writeToLog("INFO","Step 13: Going to verify my media entries filter by: " + enums.MediaType.QUIZ.value)  
            if self.common.channel.verifyEntriesDisplay(self.filterByQuiz, verifyIn=enums.Location.CHANNEL_PAGE ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to verify my media entries  by '" + enums.MediaType.QUIZ.value + "'")
                return 
            
            writeToLog("INFO","Step 14: Going to verify that only entries with " + enums.MediaType.QUIZ.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryNameQuiz], enums.MediaType.QUIZ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to filter and verify my media entries  by '" + enums.MediaType.QUIZ.value + "'")
                return                      
                
            if self.common.isElasticSearchOnPage() == True:
                if self.common.base.click(tmpType, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on 'All Media Type' button in filters")
                    self.status = "Fail"
                    return False
                self.common.general.waitForLoaderToDisappear()
                # close the filters
                if self.common.base.click(self.common.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                    writeToLog("INFO","FAILED to click and close filters button in my media")
                    self.status = "Fail"
                    return False                         
                                    
            ##################################################################
            writeToLog("INFO","TEST PASSED: Sort by media type in 'my media' page done successfully")
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