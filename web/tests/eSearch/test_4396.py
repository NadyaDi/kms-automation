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
    # Test Name : eSearch - Fields display in results - Single - Global page
    # Test description:
    # Upload entries with different cue points fields
    # Go to global page, make a search that matches single value in field, and check for field display in results
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
    testNum = "4396"
    
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
            self.searchInSingleTag = "single tag"
            self.searchInSingleSlide = "single slide"
            self.searchInSingleChapter = "single chapter"
            self.searchInSingleQuiz = "single quiz"   
            self.searchInSingleComment = "single comment"
            self.searchInSinglePoll = "single poll" 
            self.searchInSingleDetail = "single customdata"                        
            
            # Entry details
            self.entryOwner = "Inbar will"
            self.categoriesList = ["eSearch category", "Channel for eSearch", "SR-Channel for eSearch"]
            
            # Entries
            self.entryForFieldsDisplay1 = "Fields display - Name"
            self.entryForFieldsDisplay2 = "Fields display - Description"
            self.entryForFieldsDisplay3 = "Fields display - All Fields - single - Quiz" # Created from self.entryForFieldsDisplay3
            self.entryForFieldsDisplay4 = "Fields display - All Fields - multiple - Quiz" # Created from self.entryForFieldsDisplay4
            self.entryForFieldsDisplay5 = "Fields display - multiple polls" # Created manually  
            
            # Fields display
            self.fieldsForSearchInEntryName = {'Captions':False, 'Tags':False, 'Quiz':False, 'Slides':False, 'Details':False, 'Chapters':False, 'Comments':False, 'Poll':False}                
            ##################### TEST STEPS - MAIN FLOW ##################### 
            writeToLog("INFO","Step 1: Going to make a search in global page that matches entry name")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED to make a global search that matches entry name")
                return 
                   
            writeToLog("INFO","Step 2: Going to verify fields display in results for search in entry name")
            if self.common.myMedia.checkEntriesFieldsInResults(self.fieldsForSearchInEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to displayed correct fields for search in entry name")
                return  
                    
            writeToLog("INFO","Step 3: Going to make a search in My Media that matches entry description")
            if self.common.myMedia.searchEntryMyMedia(self.searchInEntryDescription) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to make a search in My Media that matches entry description")
                return  
                    
            writeToLog("INFO","Step 4: Going to verify fields display in results for search in entry description")
            if self.common.myMedia.checkEntriesFieldsInResults(self.fieldsForSearchInEntryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to displayed correct fields for search in entry description")
                return  
                    
            writeToLog("INFO","Step 5: Going to make a search in global page that matches single caption")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSingleCaption) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to make a search in global page that matches single caption")
                return   
                    
            writeToLog("INFO","Step 6: Going to verify single captions field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.CAPTION) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify single captions field display after clicking on field name")
                return  
                    
            writeToLog("INFO","Step 7: Going to verify single captions field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.CAPTION, entryOwner=self.entryOwner, categoriesList=self.categoriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to verify single captions field display after clicking on show more button")
                return  
                    
            writeToLog("INFO","Step 8: Going to verify single captions field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.CAPTION) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify single captions field display after clicking on show all button")
                return 
                                
            writeToLog("INFO","Step 9: Going to make a search in global page that matches single tag")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSingleTag) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to make a search in global page that matches single tag")
                return   
                  
            writeToLog("INFO","Step 10: Going to verify single tag field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.TAG) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to verify single tag field display after clicking on field name")
                return  
                  
            writeToLog("INFO","Step 11: Going to verify single tag field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.TAGS, entryOwner=self.entryOwner, categoriesList=self.categoriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to verify single tag field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 12: Going to verify single captions field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.TAGS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to verify single captions field display after clicking on show all button")
                return 
  
            writeToLog("INFO","Step 13: Going to make a search in global page that matches single quiz")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSingleQuiz) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to make a search in global page that matches single quiz")
                return   
                  
            writeToLog("INFO","Step 14: Going to verify single quiz field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.QUIZ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to verify single quiz field display after clicking on field name")
                return  
                  
            writeToLog("INFO","Step 15: Going to verify single quiz field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.QUIZ, entryOwner=self.entryOwner, categoriesList=self.categoriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to verify single quiz field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 16: Going to verify single quiz field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.QUIZ) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to verify single quiz field display after clicking on show all button")
                return 
   
            writeToLog("INFO","Step 17: Going to make a search in global page that matches single slide")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSingleSlide) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to make a search in global page that matches single slide")
                return   
                  
            writeToLog("INFO","Step 18: Going to verify single slide field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.SLIDE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to verify single slide field display after clicking on field name")
                return  
                  
            writeToLog("INFO","Step 19: Going to verify single slide field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.SLIDE, entryOwner=self.entryOwner, categoriesList=self.categoriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to verify single slide field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 20: Going to verify single slide field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.SLIDE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to verify single slide field display after clicking on show all button")
                return 
   
            writeToLog("INFO","Step 21: Going to make a search in global page that matches single chapter")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSingleChapter) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to make a search in global page that matches single chapter")
                return   
                   
            writeToLog("INFO","Step 22: Going to verify single chapter field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.CHAPTER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to verify single chapter field display after clicking on field name")
                return  
                   
            writeToLog("INFO","Step 23: Going to verify single chapter field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.CHAPTER, entryOwner=self.entryOwner, categoriesList=self.categoriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to verify single chapter field display after clicking on show more button")
                return  
                   
            writeToLog("INFO","Step 24: Going to verify single chapter field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.CHAPTER) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to verify single chapter field display after clicking on show all button")
                return 
    
            writeToLog("INFO","Step 25: Going to make a search in global page that matches single comment")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSingleComment) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED to make a search in global page that matches single comment")
                return   
                   
            writeToLog("INFO","Step 26: Going to verify single comment field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.COMMENT) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED to verify single comment field display after clicking on field name")
                return  
                   
            writeToLog("INFO","Step 27: Going to verify single comment field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.COMMENT, entryOwner=self.entryOwner, categoriesList=self.categoriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED to verify single comment field display after clicking on show more button")
                return  
                   
            writeToLog("INFO","Step 28: Going to verify single comment field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.COMMENT) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED to verify single comment field display after clicking on show all button")
                return 
 
            writeToLog("INFO","Step 29: Going to make a search in global page that matches single poll")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSinglePoll) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED to make a search in global page that matches single poll")
                return   
                  
            writeToLog("INFO","Step 30: Going to verify single poll field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.POLL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 30: FAILED to verify single poll field display after clicking on field name")
                return  
                  
            writeToLog("INFO","Step 31: Going to verify single poll field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.POLL, entryOwner=self.entryOwner, categoriesList=self.categoriesList, isWebcast=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 31: FAILED to verify single poll field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 32: Going to verify single poll field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.POLL) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 32: FAILED to verify single poll field display after clicking on show all button")
                return 
  
            writeToLog("INFO","Step 33: Going to make a search in global page that matches single detail")
            if self.common.globalSearch.makeAGloablSearchForEsearch(self.searchInSingleDetail) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 33: FAILED to make a search in global page that matches single detail")
                return   
                  
            writeToLog("INFO","Step 34: Going to verify detail comment field display after clicking on field name")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnField(True, enums.EntryFields.DETAILS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 34: FAILED to verify detail comment field display after clicking on field name")
                return  
                  
            writeToLog("INFO","Step 35: Going to verify single detail field display after clicking on show more button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowMore(True, enums.EntryFields.DETAILS, entryOwner=self.entryOwner, categoriesList=self.categoriesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 35: FAILED to verify single detail field display after clicking on show more button")
                return  
                  
            writeToLog("INFO","Step 36: Going to verify single detail field display after clicking on show all button")
            if self.common.myMedia.verifyFieldDisplayInResultAfterClickingOnShowAll(True, enums.EntryFields.DETAILS) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 36: FAILED to verify single detail field display after clicking on show all button")
                return 
                                                                                     
            ##################################################################
            writeToLog("INFO","TEST PASSED: verify single field value display in 'My Media' done successfully")
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