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
    # Test Name : eSearch - Fields display in results - Multiple - Add to channel - My media tab
    # Test description:
    # Upload entries with different cue points fields
    # Go to add to channel - My Media, make a search that matches multiple values in field, and check for field display in results
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
    testNum = "4410"
    
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
            
            self.channel = "Channel for eSearch"
            
            # Entries
            self.entryForFieldsDisplay1 = "Fields display - Name"
            self.entryForFieldsDisplay2 = "Fields display - Description"
            self.entryForFieldsDisplay3 = "Fields display - All Fields - single - Quiz" # Created from self.entryForFieldsDisplay3
            self.entryForFieldsDisplay4 = "Fields display - All Fields - multiple - Quiz" # Created from self.entryForFieldsDisplay4
            self.entryForFieldsDisplay5 = "Fields display - multiple polls" # Created manually  
            
            ##################### TEST STEPS - MAIN FLOW #####################   
            writeToLog("INFO","Step 1: Going to navigate to add to channel - media tab")
            if self.common.channel.navigateToAddToChannel(self.channel) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to navigate to add to channel - media tab")
                return               
        
            writeToLog("INFO","Step 2: Going to make a search in 'Add to channel - My media' tab that matches multiple caption values")
            if self.common.channel.searchInAddToChannel(self.searchInMultipleCaptions) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to make a search in 'Add to channel - My media' tab that matches multiple caption values")
                return   
                   
            writeToLog("INFO","Step 3: Going to verify multiple captions field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.CAPTIONS, numOfDisplay=self.captionsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to verify multiple captions field display after clicking on field name")
                return  
                     
            writeToLog("INFO","Step 4: Going to verify multiple captions field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.CAPTIONS, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.captionsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to verify multiple captions field display after clicking on show more button")
                return  
                   
            writeToLog("INFO","Step 5: Going to verify multiple captions field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.CAPTIONS, numOfDisplay=self.captionsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to verify multiple captions field display after clicking on show all button")
                return    
             
            writeToLog("INFO","Step 6: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to clear search")
                return              
  
            writeToLog("INFO","Step 7: Going to make a search in 'Add to channel - My media' tab that matches multiple tags values")
            if self.common.channel.searchInAddToChannel(self.searchInMultipleTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to make a search in 'Add to channel - My media' tab that matches multiple tags values")
                return
                  
            writeToLog("INFO","Step 8: Going to verify multiple tags field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.TAGS, numOfDisplay=self.tagsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify multiple tags field display after clicking on field name")
                return  
                     
            writeToLog("INFO","Step 9: Going to verify multiple tags field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.TAGS, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.tagsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify multiple tags field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 10: Going to verify multiple tags field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.TAGS, numOfDisplay=self.tagsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to verify multiple tags field display after clicking on show all button")
                return   
  
            writeToLog("INFO","Step 11: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to clear search")
                return              
  
            writeToLog("INFO","Step 12: Going to make a search in 'Add to channel - My media' tab that matches multiple quiz values")
            if self.common.channel.searchInAddToChannel(self.searchInMultipleQuiz) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to make a search in 'Add to channel - My media' tab that matches multiple quiz values")
                return 
                  
            writeToLog("INFO","Step 13: Going to verify multiple quiz field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.QUIZ, numOfDisplay=self.quizNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to verify multiple quiz field display after clicking on field name")
                return  
                     
            writeToLog("INFO","Step 14: Going to verify multiple quiz field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.QUIZ, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.tagsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to verify multiple quiz field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 15: Going to verify multiple quiz field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.QUIZ, numOfDisplay=self.quizNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to verify multiple quiz field display after clicking on show all button")
                return   
             
            writeToLog("INFO","Step 16: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to clear search")
                return              
  
            writeToLog("INFO","Step 17: Going to make a search in 'Add to channel - My media' tab that matches multiple slide values")
            if self.common.channel.searchInAddToChannel(self.searchInMultipleSlides) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to make a search in 'Add to channel - My media' tab that matches multiple slide values")
                return             
                  
            writeToLog("INFO","Step 18: Going to verify multiple slides field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.SLIDES, numOfDisplay=self.slidesNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to verify multiple slides field display after clicking on field name")
                return  
                     
            writeToLog("INFO","Step 19: Going to verify multiple slides field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.SLIDES, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.slidesNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to verify multiple slides field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 20: Going to verify multiple slides field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.SLIDES, numOfDisplay=self.slidesNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to verify multiple slides field display after clicking on show all button")
                return                                                       
     
            writeToLog("INFO","Step 21: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to clear search")
                return              
 
            writeToLog("INFO","Step 22: Going to make a search in 'Add to channel - My media' tab that matches multiple chapter values")
            if self.common.channel.searchInAddToChannel(self.searchInMultipleChapters) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to make a search in 'Add to channel - My media' tab that matches multiple chapter values")
                return
                  
            writeToLog("INFO","Step 23: Going to verify multiple chapters field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.CHAPTERS, numOfDisplay=self.chapersNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to verify multiple chapters field display after clicking on field name")
                return  
                     
            writeToLog("INFO","Step 24: Going to verify multiple chapters field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.CHAPTERS, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.chapersNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to verify multiple chapters field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 25: Going to verify multiple chapters field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.CHAPTERS, numOfDisplay=self.chapersNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED to verify multiple chapters field display after clicking on show all button")
                return   
    
            writeToLog("INFO","Step 26: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED to clear search")
                return              
 
            writeToLog("INFO","Step 27: Going to make a search in 'Add to channel - My media' tab that matches multiple comments values")
            if self.common.channel.searchInAddToChannel(self.searchInMultipleComments) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED to make a search in 'Add to channel - My media' tab that matches multiple comments values")
                return
                  
            writeToLog("INFO","Step 28: Going to verify multiple comments field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.COMMENTS, numOfDisplay=self.commentsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED to verify multiple comments field display after clicking on field name")
                return  
                     
            writeToLog("INFO","Step 29: Going to verify multiple comments field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.COMMENTS, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.commentsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED to verify multiple comments field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 30: Going to verify multiple comment field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.COMMENTS, numOfDisplay=self.commentsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 30: FAILED to verify multiple comment field display after clicking on show all button")
                return
   
            writeToLog("INFO","Step 31: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 31: FAILED to clear search")
                return              
 
            writeToLog("INFO","Step 32: Going to make a search in 'Add to channel - My media' tab that matches multiple polls values")
            if self.common.channel.searchInAddToChannel(self.searchInMultiplePolls) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 32: FAILED to make a search in 'Add to channel - My media' tab that matches multiple polls values")
                return   
                 
            writeToLog("INFO","Step 33: Going to verify multiple polls field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.POLLS, numOfDisplay=self.pollsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 33: FAILED to verify multiple polls field display after clicking on field name")
                return  
                    
            writeToLog("INFO","Step 34: Going to verify multiple polls field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.POLLS, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.pollsNumOfDisplay, isWebcast=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 34: FAILED to verify multiple polls field display after clicking on show more button")
                return  
                 
            writeToLog("INFO","Step 35: Going to verify multiple polls field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.POLLS, numOfDisplay=self.pollsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 35: FAILED to verify multiple polls field display after clicking on show all button")
                return  
   
            writeToLog("INFO","Step 36: Going to clear search")
            if self.common.channel.clearSearchInAddToChannel() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 36: FAILED to clear search")
                return              
 
            writeToLog("INFO","Step 37: Going to make a search in 'Add to channel - My media' tab that matches multiple details values")
            if self.common.channel.searchInAddToChannel(self.searchInMultipleDetails) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 37: FAILED to make a search in 'Add to channel - My media' tab that matches multiple details values")
                return  
                 
            writeToLog("INFO","Step 38: Going to verify multiple details field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(False, enums.EntryFields.DETAILS, numOfDisplay=self.detailsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 38: FAILED to verify multiple details field display after clicking on field name")
                return  
                    
            writeToLog("INFO","Step 39: Going to verify multiple details field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(False, enums.EntryFields.DETAILS, entryOwner=self.entryOwner, categoriesList=self.categoriesList, numOfDisplay=self.detailsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 39: FAILED to verify multiple details field display after clicking on show more button")
                return  
                 
            writeToLog("INFO","Step 40: Going to verify multiple details field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(False, enums.EntryFields.DETAILS, numOfDisplay=self.detailsNumOfDisplay) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 40: FAILED to verify multiple details field display after clicking on show all button")
                return                                                                                                                         
            ##################################################################
            writeToLog("INFO","TEST PASSED: verify multiple field values display in 'Add to channel - My media tab' done successfully")
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