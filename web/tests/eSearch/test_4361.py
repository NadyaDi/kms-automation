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
    #  @Author: Inbar Willman
    # Test Name : eSearch - Fields display in results - My Media
    # Test description:
    # Upload entries with different cue points fields
    # Go to My Media, make a search, and check for fields display in results
    #    1. Name
    #    2. Description
    #    3. Tag
    #    4. Details 
    #    5. Chapters
    #    6. Slides
    #    7. Captions
    #    8. Quiz
    #    9. Comments
    #    10. Polls
    #================================================================================================================================
    testNum = "4361"
    
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
            
            # Searches in page
            self.searchInEntryName = "Fields display - Name"
            self.searchInEntryDescription = "Fields display - entry description"
            self.searchInSingleCaption = "single captions"
            self.searchInMultipleCaptions = "multiple captions"
            self.searchInSingleTag = "single tag"
            self.searchInMultipleTags = "multiple tags"
            self.searchInSingleSlide = "single slide"
            self.searchInMultipleSlides = "multiple slides"
            self.searchInSingleChapter = "single chapter"
            self.searchInMultipleChapters = "multiple chapters" 
            self.searchInSingleQuiz = "single quiz"
            self.searchInMultipleQuiz = "multiple quiz"      
            self.searchInSingleComment = "single comment"
            self.searchInMultipleComments = "multiple comments" 
            self.searchInSinglePoll = "single poll"
            self.searchInMultiplePolls = "multiple polls"                             
                                   
            
            # Fields number of display
            self.captionsNumOfDisplay = 7
            self.tagsNumOfDisplay = 6
            self.quizNumOfDisplay = 6
            self.slidesNumOfDisplay = 8
            self.chapersNumOfDisplay = 6
            self.commentsNumOfDisplay = 6
            self.pollsNumOfDisplay = 6
            
            # Entries
            self.entryForFieldsDisplay1 = "Fields display - Name"
            self.entryForFieldsDisplay2 = "Fields display - Description"
            self.entryForFieldsDisplay3 = "Fields display - All Fields - single - Quiz" # Created from self.entryForFieldsDisplay3
            self.entryForFieldsDisplay4 = "Fields display - All Fields - multiple - Quiz" # Created from self.entryForFieldsDisplay4
            self.entryForFieldsDisplay5 = "Fields display - multiple polls" # Created manually  
            
            # Fields display
            self.fieldsForSearchInEntryName = {'Captions':False, 'Tags':False, 'Quiz':False, 'Slides':False, 'Details':False, 'Chapters':False, 'Comments':False, 'Poll':False}                
            ##################### TEST STEPS - MAIN FLOW ##################### 
#             writeToLog("INFO","Step 1: Going navigate to 'My Media' page")
#             if self.common.myMedia.navigateToMyMedia(forceNavigate=True) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 1: FAILED navigate to 'My Media' page")
#                 return 
#              
            writeToLog("INFO","Step 2: Going to make a search in My Media that matches entry name")
            if self.common.myMedia.searchEntryMyMedia(self.searchInEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to make a search in My Media that matches entry name")
                return 
             
            writeToLog("INFO","Step 3: Going to verify fields display in results for search in entry name")
            if self.common.myMedia.checkEntriesFieldsInResults(self.fieldsForSearchInEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to displayed correct fields for search in entry name")
                return  
             
            writeToLog("INFO","Step 4: Going to make a search in My Media that matches entry description")
            if self.common.myMedia.searchEntryMyMedia(self.searchInEntryDescription) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to make a search in My Media that matches entry description")
                return  
             
            writeToLog("INFO","Step 5: Going to verify fields display in results for search in entry description")
            if self.common.myMedia.checkEntriesFieldsInResults(self.fieldsForSearchInEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to displayed correct fields for search in entry description")
                return  
             
            writeToLog("INFO","Step 6: Going to make a search in My Media that matches single caption")
            if self.common.myMedia.searchEntryMyMedia(self.searchInSingleCaption) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to make a search in My Media that matches single caption")
                return   
             
            writeToLog("INFO","Step 7: Going to verify single captions field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, 'Caption') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify single captions field display after clicking on field name")
                return  
             
            writeToLog("INFO","Step 8: Going to verify single captions field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, 'Caption') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify single captions field display after clicking on show more button")
                return  
             
            writeToLog("INFO","Step 9: Going to verify single captions field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, 'Caption') == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify single captions field display after clicking on show all button")
                return 
            
            writeToLog("INFO","Step 10: Going to make a search in My Media that matches multiple captions")
            if self.common.myMedia.searchEntryMyMedia(self.searchInMultipleCaptions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to make a search in My Media that matches multiple captions")
                return   
            
            writeToLog("INFO","Step 11: Going to verify multiple captions field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, 'Captions', numOfDisplay=self.captionsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to verify multiple captions field display after clicking on field name")
                return  
             
            writeToLog("INFO","Step 12: Going to verify multiple captions field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, 'Captions', numOfDisplay=self.captionsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to verify multiple captions field display after clicking on show more button")
                return  
            
            writeToLog("INFO","Step 13: Going to verify multiple captions field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, 'Captions', numOfDisplay=self.captionsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to verify multiple captions field display after clicking on show all button")
                return                                                                                                     
     
            ##################################################################
            writeToLog("INFO","TEST PASSED: Search in 'My Media' done successfully")
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