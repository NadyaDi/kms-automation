import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections.abc

class Test:
    
    #================================================================================================================================
    #  @Author: Inbar Willman
    # Test Name : Setup test for eSearch
    # Test description:
    # Create entries for search in tests
    #================================================================================================================================
    testNum = "7"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription = 'Description'
    entryTags = 'tag2,'
    newTags = ['searchIn tag1,','searchIn tag2,', 'searchIn tag3,', 'searchIn tag4,', 'searchIn tag5,', 'searchIn tag6,']
    newDescription = "searchIn description"
    QuizQuestion1 = 'First question - SearchIn'
    QuizQuestion1Answer1 = 'First answer - SearchIn'
    QuizQuestion1AdditionalAnswers = ['Second answer - SearchIn', 'Third question - SearchIn', 'Fourth question - SearchIn']
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    captionsFile = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\caption-searchIn.srt'
    slidesFile = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\SearchIn.pptx'
    #run test as different instances on all the supported platforms
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
            
            # Entries for sort by in my media/global search/add to channel/channel/gallery/new video quiz
            self.entryForSearchIn1 = "Search in - Captions"
            self.entryForSearchIn2 = "Search in - All field"
            self.entryForSearchIn3 = "Search in - Details"
            self.entryForSearchIn4 = "Search in - Chapters/Slides"
            self.entryForSearchIn5 = "Search in" # Will be quiz
            self.entryForSearchIn6 = "Search in - Polls" # Created manually
            self.entryForSearchIn7 = "Search in - Quiz" # name of searchIn5 after creating quiz
            self.slidesQrCodeAndTimeList = [('0', '00:00'), ('1', '00:05'), ('2', '00:10'), ('3', '00:16'), ('4', '00:20'), ('5', ('00:25'))]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)
            self.chaptersList = [('searchIn Chapters 1','00:01'), ('searchIn Chapters 2','00:03'), ('searchIn Chapters 3','00:06'),
                                 ('searchIn Chapters 4','00:09'), ('searchIn Chapters 5','00:12'), ('searchIn Chapters 6','00:15')]
            
            # Category tests in gallery/add to gallery tabs 
            self.categoryForEsearch = 'eSearch category'
            self.categoryForModerator = 'category for eSearch moderator' 
            
            # Channel for tests in channel/ add to channel tabs
            self.channelForEsearch  = "Channel for eSearch"
            self.channelForModerator = 'channel moderator for eSearch'
            self.SrChannelForEsearch = "SR-Channel for eSearch"
            ##################### TEST STEPS - MAIN FLOW #############################################################
#             writeToLog("INFO","Going to add cue points and metadata for entries for 'search in' tests'") 
#             
#             step = 1
#             
#             writeToLog("INFO","Going to upload entries") 
#             for i in range(1,6):
#                 writeToLog("INFO","Step " + str(step) + ": Going to upload new entry '" + eval('self.entryForSearchIn'+str(step)))            
#                 if self.common.upload.uploadEntry(self.filePath, eval('self.entryForSearchIn'+str(i)), self.entryDescription, self.entryTags) == None:
#                     self.status = "Fail"
#                     writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry: " + eval('self.entryForSearchIn'+str(step)))
#                     return    
#                 
#                 step = step + 1
#                     
#                 writeToLog("INFO","Step " + str(step) + ": Going to publish entry '" + eval('self.entryForSearchIn'+str(step)) + " to eSearch categories and channels")            
#                 if self.common.myMedia.publishSingleEntry(eval('self.entryForSearchIn'+str(step)), [self.categoryForEsearch, self.categoryForModerator], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.UPLOAD_PAGE) == False:
#                     self.status = "Fail"
#                     writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry " + eval('self.entryForSearchIn'+str(step)))
#                     return                
#                 
#                 step = step + 1
      
#             writeToLog("INFO","Step 13: Going to navigate to edit entry page for the next entry: " + self.entryForSearchIn1)    
#             if self.common.editEntryPage.navigateToEditEntry(self.entryForSearchIn1) == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 13: FAILED to navigate to edit entry page of the next entry: " + self.entryForSearchIn1)
#                 return         
#            
#             writeToLog("INFO","Step 6: Going to add captions for " + self.entryForSearchIn1)    
#             if self.common.editEntryPage.addCaptions(self.captionsFile, "Afar", "captions") == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 6: FAILED to add captions to: " +  self.entryForSearchIn1)
#                 return 
            
            writeToLog("INFO","Step 7: Going to navigate to edit entry page for the next entry: " + self.entryForSearchIn2)    
            if self.common.editEntryPage.navigateToEditEntry(self.entryForSearchIn2) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 7: FAILED to navigate to edit entry page of the next entry: " + self.entryForSearchIn2)
                return  
            
#             writeToLog("INFO","Step 8: Going to add captions to " + self.entryForSearchIn2)    
#             if self.common.editEntryPage.addCaptions(self.captionsFile, "Afar", "captions") == False:
#                 self.status = "Fail"
#                 writeToLog("INFO","Step 8: FAILED to add captions to: " +  self.entryForSearchIn2)
#                 return  
            
            writeToLog("INFO","Step 9: Going to add slides to " + self.entryForSearchIn2)    
            if self.common.editEntryPage.uploadSlidesDeck(self.slidesFile, self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to add slides to: " +  self.entryForSearchIn2)
                return                         
              
            writeToLog("INFO","Step 10: Going to add chapters to " + self.entryForSearchIn2)    
            if self.common.editEntryPage.addChapters(self.entryForSearchIn2, self.chaptersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to add chapters to: " +  self.entryForSearchIn2)
                return  
            
            writeToLog("INFO","Step 11: Going to add tags and description for " + self.entryForSearchIn2)    
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSearchIn2, self.entryForSearchIn2, self.newDescription, self.newTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to add tags and description to: " +  self.entryForSearchIn2)
                return                       
 
            writeToLog("INFO","Step 12: Going to navigate to edit entry page for the next entry: " + self.entryForSearchIn3)    
            if self.common.editEntryPage.navigateToEditEntry(self.entryForSearchIn3) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to navigate to edit entry page of the next entry: " + self.entryForSearchIn3)
                return   
 
            writeToLog("INFO","Step 13: Going to add tags and description for " + self.entryForSearchIn3)    
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSearchIn3, self.entryForSearchIn3, self.newDescription, self.newTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to add tags and description to: " +  self.entryForSearchIn3)
                return    
 
            writeToLog("INFO","Step 14: Going to navigate to edit entry page for the next entry: " + self.entryForSearchIn4)    
            if self.common.editEntryPage.navigateToEditEntry(self.entryForSearchIn4) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to navigate to edit entry page of the next entry: " + self.entryForSearchIn4)
                return  
            
            writeToLog("INFO","Step 15: Going to add slides to " + self.entryForSearchIn4)    
            if self.common.editEntryPage.uploadSlidesDeck(self.slidesFile, self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to add slides to: " +  self.entryForSearchIn4)
                return                         
              
            writeToLog("INFO","Step 16: Going to add chapters to " + self.entryForSearchIn4)    
            if self.common.editEntryPage.addChapters(self.entryForSearchIn2, self.chaptersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to add chapters to: " +  self.entryForSearchIn4)
                return 
 
            writeToLog("INFO","Step 17: Going to navigate to add new video quiz")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to click video quiz")
                return  
              
            writeToLog("INFO","Step 18: Going to search for: " + self.entryForSearchIn5 + " and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryForSearchIn5, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to find entry and open KEA")
                return  
              
            writeToLog("INFO","Step 19: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to start quiz and add questions")
                return   
              
            writeToLog("INFO","Step 20: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to save quiz and navigate to media page")
                return 
            
            writeToLog("INFO","Step 21: Going to navigate to edit entry page for the next entry: " + self.entryForSearchIn7)    
            if self.common.editEntryPage.navigateToEditEntry(self.entryForSearchIn7) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to navigate to edit entry page of the next entry: " + self.entryForSearchIn7)
                return  
            
            writeToLog("INFO","Step 22: Going to add captions to " + self.entryForSearchIn7)    
            if self.common.editEntryPage.addCaptions(self.captionsFile, "Afar", "captions") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to add captions to: " +  self.entryForSearchIn7)
                return  
            
            writeToLog("INFO","Step 23: Going to add slides to " + self.entryForSearchIn7)    
            if self.common.editEntryPage.uploadSlidesDeck(self.slidesFile, self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to add slides to: " +  self.entryForSearchIn7)
                return                         
              
            writeToLog("INFO","Step 24: Going to add chapters to " + self.entryForSearchIn7)    
            if self.common.editEntryPage.addChapters(self.entryForSearchIn2, self.chaptersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to add chapters to: " +  self.entryForSearchIn7)
                return  
            
            writeToLog("INFO","Step 25: Going to add tags and description for " + self.entryForSearchIn7)    
            if self.common.editEntryPage.changeEntryMetadata(self.entryForSearchIn7, self.entryForSearchIn7, self.newDescription, self.newTags) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED to add tags and description to: " +  self.entryForSearchIn7)
                return             
            writeToLog("INFO","TEST PASSED: All entries were updated successfully") 
            #################################################################################

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