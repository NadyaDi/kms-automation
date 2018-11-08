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
    testNum = "11"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryDescription1 = 'Description'
    entryDescription2 = "Fields display - entry description"
    entryDescription3 = ""
    entryDescription4 = ""
    entryTag1 = 'tag,'
    entryTag2 = 'tag,'
    entryTag3 = 'Fields display - single tag,'
    entryTag4 = "tag,"
    entryTagMultiple = ['Fields display - multiple tags 1,','Fields display - multiple tags 2,', 'Fields display - multiple tags 3,', 'Fields display - multiple tags 4,',
                        'Fields display - multiple tags 5,', 'Fields display - multiple tags 6,']
    
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    
    singleCaptionsFile = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\Fields display - single caption.srt'
    multipleCaptionsFile = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\Fields display - multiple captions.srt'
    
    singleSlidesFile = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\FieldsDisplaySingleSlide.pptx'
    multipleSlidesFile = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\FieldsDisplayMultipleSlides.pptx'
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

            self.entryForFieldsDisplay1 = "Fields display - Name"
            self.entryForFieldsDisplay2 = "Fields display - Description"
            self.entryForFieldsDisplay3 = "Fields display - All Fields - single" # Will be quiz
            self.entryForFieldsDisplay4 = "Fields display - All Fields - multiple" # Will be quiz
            self.entryForFieldsDisplay5 = "Fields display - All Fields - single - Quiz" # Created from self.entryForFieldsDisplay3
            self.entryForFieldsDisplay6 = "Fields display - All Fields - multiple - Quiz" # Created from self.entryForFieldsDisplay4
            self.entryForFieldsDisplay7 = "Fields display - Polls" # Created manually
            
            self.slidesQrCodeAndTimeList = [('0', '00:00'), ('1', '00:04'), ('2', '00:08'), ('3', '00:12'), ('4', '00:16'), ('5', '00:19'),
                                            ('6', '00:23'), ('7', '00:27')]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)
            
            self.singleSlideQrCodeAndTimeList = [('0', '00:00')]
            self.singleSlideQrCodeAndTimeList = collections.OrderedDict(self.singleSlideQrCodeAndTimeList)
            
            self.chaptersList = [('Fields display - multiple chapters 1','00:01'), ('Fields display - multiple chapters 2','00:03'), ('Fields display - multiple chapters 3','00:06'),
                                 ('Fields display - multiple chapters 4','00:09'), ('Fields display - multiple chapters 5','00:12'), ('Fields display - multiple chapters 6','00:15')]
            self.chaptersList = collections.OrderedDict(self.chaptersList)
            
            self.singleChapter = [('Fields display - single chapter','00:01')]
            self.singleChapter = collections.OrderedDict(self.singleChapter)
            
            # Category tests in gallery/add to gallery tabs 
            self.categoryForEsearch = 'eSearch category'
            self.categoryForModerator = 'category for eSearch moderator' 
            
            # Channel for tests in channel/ add to channel tabs
            self.channelForEsearch  = "Channel for eSearch"
            self.channelForModerator = 'channel moderator for eSearch'
            self.SrChannelForEsearch = "SR-Channel for eSearch"
            
            self.customdatatPtofileId = "10885192"
            
            # Custom data fields
            self.singleTextCustomdataField1 = "SIngleText"
            self.singleTextCustomdataFieldInput1 = "Fields display - single customdata text"
            self.unlimitedTextCustomdataField1 = "UnlimitedText0"
            self.unlimitedTextCustomdataFieldInput1 = ["Fields display - unlimited customdata text 1", "Fields display - unlimited customdata text 2"]
            self.unlimitedTextCustomdataAddField = "UnlimitedText"
            self.ListCustomdataField1 = "SingleTextSelectedList"
            self.ListCustomdataFieldOption1 = "Search in - One"
            
            #Quiz questions
            self.QuizQuestion1 = 'Fields Display - single quiz'
            self.QuizQuestion1Answer1 = 'Fields Display - single quiz answer 1'
            self.QuizQuestion1AdditionalAnswers = ['Fields Display - single quiz answer 1', 'Fields Display - single quiz answer 1', 'Fields Display - single quiz answer 1']
            
            self.QuizMultipleQuestion1 = 'Fields Display - multiple quiz 1'
            self.QuizMultipleQuestion1Answer1 = 'Fields Display - multiple quiz answer 1'
            self.QuizMultipleQuestion1AdditionalAnswers1 = ['Fields Display - multiple quiz answer 1', 'Fields Display - multiple answer 1', 'Fields Display - multiple quiz answer 1']
            
            self.QuizMultipleQuestion2 = 'Fields Display - multiple quiz 2'
            self.QuizMultipleQuestion1Answer2 = 'Fields Display - multiple quiz answer 2'
            self.QuizMultipleQuestion1AdditionalAnswers2 = ['Fields Display - multiple quiz answer 2', 'Fields Display - single multiple answer 2', 'Fields Display - multiple quiz answer 2']
            
            self.QuizMultipleQuestion3 = 'Fields Display - multiple quiz 3'
            self.QuizMultipleQuestion1Answer3 = 'Fields Display - multiple quiz answer 3'
            self.QuizMultipleQuestion1AdditionalAnswers3 = ['Fields Display - multiple quiz answer 3', 'Fields Display - single multiple answer 3', 'Fields Display - multiple quiz answer 3']  
            
            self.QuizMultipleQuestion4 = 'Fields Display - multiple quiz 4'
            self.QuizMultipleQuestion1Answer4 = 'Fields Display - multiple quiz answer 4'
            self.QuizMultipleQuestion1AdditionalAnswers4 = ['Fields Display - multiple quiz answer 4', 'Fields Display - single multiple answer 4', 'Fields Display - multiple quiz answer 4']      
            
            
            # Comments will be added manually
            ##################### TEST STEPS - MAIN FLOW #############################################################
            writeToLog("INFO","Going to add cue points and metadata for entries for fields display in results tests")           
            
            writeToLog("INFO","Step 1: Going navigate to admin page and enable customdata module") 
            if self.common.admin.enableCustomMetadata(True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED navigate to admin page and enable customdata module")
                return
               
            writeToLog("INFO","Step 2: Going to select customdata profile id") 
            if self.common.admin.selectCustomdataProfileId(self.customdatatPtofileId) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to select customdata profile id")
                return
              
            writeToLog("INFO","Step 3: Going navigate to home page")            
            if self.common.home.navigateToHomePage(forceNavigate=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED navigate to home page")
                return
                
            step = 4
                 
            writeToLog("INFO","Going to upload entries") 
            for i in range(1,5):
                writeToLog("INFO","Step " + str(step) + ": Going to upload new entry '" + eval('self.entryForFieldsDisplay'+str(i)))            
                if self.common.upload.uploadEntry(self.filePath, eval('self.entryForFieldsDisplay'+str(i)), eval('self.entryDescription'+str(i)), eval('self.entryTag'+str(i))) == None:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry: " + eval('self.entryForFieldsDisplay'+str(i)))
                    return    
                      
                step = step + 1
                       
                writeToLog("INFO","Step " + str(step) + ": Going to publish entry '" + eval('self.entryForFieldsDisplay'+str(i)) + " to eSearch categories and channels")            
                if self.common.myMedia.publishSingleEntry(eval('self.entryForFieldsDisplay'+str(i)), [self.categoryForEsearch, self.categoryForModerator], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.UPLOAD_PAGE) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step " + str(step) + ": FAILED to upload new entry " + eval('self.entryForFieldsDisplay'+str(i)))
                    return                
                      
                step = step + 1
                  
            writeToLog("INFO","Step 13: Going to navigate to add new video quiz")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 13: FAILED to click video quiz")
                return  
                   
            writeToLog("INFO","Step 14: Going to search for: " + self.entryForFieldsDisplay3 + " and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryForFieldsDisplay3, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 14: FAILED to find entry and open KEA")
                return  
                   
            writeToLog("INFO","Step 15: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 15: FAILED to start quiz and add questions")
                return   
                   
            writeToLog("INFO","Step 16: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to save quiz and navigate to media page")
                return                 
                   
            writeToLog("INFO","Step 17: Going to navigate to edit entry page for the next entry: " + self.entryForFieldsDisplay5)    
            if self.common.editEntryPage.navigateToEditEntry(self.entryForFieldsDisplay5) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 17: FAILED to navigate to edit entry page of the next entry: " + self.entryForFieldsDisplay5)
                return 
                
            writeToLog("INFO","Step 18: Going to add new text single customdata fields for: " + self.entryForFieldsDisplay5)    
            if self.common.editEntryPage.setCustomDataField(self.singleTextCustomdataField1, self.singleTextCustomdataFieldInput1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 18: FAILED to add new text single customdata fields for: " + self.entryForFieldsDisplay5)
                return 
   
            writeToLog("INFO","Step 19: Going to add captions for " + self.entryForFieldsDisplay5)    
            if self.common.editEntryPage.addCaptions(self.singleCaptionsFile, "Afar", "captions") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 19: FAILED to add captions to: " + self.entryForFieldsDisplay5)
                return             
                
            writeToLog("INFO","Step 20: Going to add slides to " + self.entryForFieldsDisplay5)    
            if self.common.editEntryPage.uploadSlidesDeck(self.singleSlidesFile, self.singleSlideQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 20: FAILED to add slides to: " +  self.entryForFieldsDisplay5)
                return                         
                   
            writeToLog("INFO","Step 21: Going to add chapters to " + self.entryForFieldsDisplay5)    
            if self.common.editEntryPage.addChapters(self.entryForFieldsDisplay3, self.singleChapter) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 21: FAILED to add chapters to: " +  self.entryForFieldsDisplay5)
                return               
            
            writeToLog("INFO","Step 22: Going to navigate to entry page ")    
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryForFieldsDisplay5, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 22: FAILED to navigate to entry: " + self.entryForFieldsDisplay5)
                return        
             
            writeToLog("INFO","Step 23: Going to publish entry " + self.entryForFieldsDisplay5)    
            if self.common.myMedia.publishSingleEntry(self.entryForFieldsDisplay5, [self.categoryForEsearch, self.categoryForModerator], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 23: FAILED to publish entry: " +  self.entryForFieldsDisplay5)
                return     
             
            writeToLog("INFO","Step 24: Going to navigate to add new video quiz")
            if self.common.upload.addNewVideoQuiz() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 24: FAILED to click video quiz")
                return  
                    
            writeToLog("INFO","Step 25: Going to search for: " + self.entryForFieldsDisplay4 + " and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryForFieldsDisplay4, False) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 25: FAILED to find entry and open KEA")
                return   
             
            writeToLog("INFO","Step 26: Going to add  question to quiz")
            if self.common.kea.addQuizQuestion(self.QuizMultipleQuestion1, self.QuizMultipleQuestion1Answer1, self.QuizMultipleQuestion1AdditionalAnswers1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 26: FAILED to add question to quiz")
                return   
             
            writeToLog("INFO","Step 27: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                self.status = "Fail"
                writeToLog("INFO","Step 27: FAILED to save quiz and navigate to media page")
                return                                    
                
            writeToLog("INFO","Step 28: Going to navigate to edit entry page for the next entry: " + self.entryForFieldsDisplay6)    
            if self.common.editEntryPage.navigateToEditEntry(self.entryForFieldsDisplay6) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 28: FAILED to navigate to edit entry page of the next entry: " + self.entryForFieldsDisplay6)
                return 
              
            writeToLog("INFO","Step 29: Going to add new text single customdata fields for: " + self.entryForFieldsDisplay6)    
            if self.common.editEntryPage.setCustomDataField(self.singleTextCustomdataField1, self.singleTextCustomdataFieldInput1) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 29: FAILED to add new text single customdata fields for: " + self.entryForFieldsDisplay6)
                return   
               
            writeToLog("INFO","Step 30: Going to add new text unlimited customdata fields for: " + self.entryForFieldsDisplay6)    
            if self.common.editEntryPage.setCustomDataField(self.unlimitedTextCustomdataField1, self.unlimitedTextCustomdataFieldInput1, self.unlimitedTextCustomdataAddField, enums.CustomdataType.TEXT_UNLIMITED) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 30: FAILED to add new text unlimited customdata fields for: " + self.entryForFieldsDisplay6)
                return  
               
            writeToLog("INFO","Step 31: Going to add new tags for: " + self.entryForFieldsDisplay6)    
            if self.common.editEntryPage.changeEntryMetadata(self.entryForFieldsDisplay6, self.entryForFieldsDisplay6, self.entryDescription4, self.entryTagMultiple) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 31: FAILED to add tags for: " + self.entryForFieldsDisplay6)
                return                                    
               
            writeToLog("INFO","Step 32: Going to add captions for " + self.entryForFieldsDisplay6)    
            if self.common.editEntryPage.addCaptions(self.multipleCaptionsFile, "Afar", "captions") == False:
                self.status = "Fail"
                writeToLog("INFO","Step 32: FAILED to add captions to: " + self.entryForFieldsDisplay6)
                return             
                
            writeToLog("INFO","Step 33: Going to add slides to " + self.entryForFieldsDisplay6)    
            if self.common.editEntryPage.uploadSlidesDeck(self.multipleSlidesFile, self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 33: FAILED to add slides to: " +  self.entryForFieldsDisplay6)
                return                         
                 
            writeToLog("INFO","Step 34: Going to add chapters to " + self.entryForFieldsDisplay6)    
            if self.common.editEntryPage.addChapters(self.entryForFieldsDisplay4, self.chaptersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 34: FAILED to add chapters to: " +  self.entryForFieldsDisplay6)
                return               
             
            writeToLog("INFO","Step 35: Going to navigate to entry page ")    
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryForFieldsDisplay6, True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 35: FAILED to navigate to entry: " + self.entryForFieldsDisplay6)
                return    
            
            writeToLog("INFO","Step 36: Going to publish entry " + self.entryForFieldsDisplay6)    
            if self.common.myMedia.publishSingleEntry(self.entryForFieldsDisplay6, [self.categoryForEsearch, self.categoryForModerator], [self.channelForEsearch, self.SrChannelForEsearch, self.channelForModerator], publishFrom = enums.Location.ENTRY_PAGE) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 36: FAILED to publish entry: " +  self.entryForFieldsDisplay6)
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