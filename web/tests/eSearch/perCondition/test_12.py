import time, pytest
import sys,os
import clsCommon
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
    #  @Author: Horia Cus
    # Test Name : Create an Entry that contains four caption
    # Test description:
    # Create an entry that contains four caption
    #================================================================================================================================
    testNum = "12"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = "Fields display - Captions"
    entryDescription = 'Fields display - description'
    entryTags = "captions,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\10SecQR100109.mp4'
    navigateFrom = enums.Location.UPLOAD_PAGE
    captionPath1 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\caption_1.srt'
    captionPath2 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\caption_2.srt'
    captionPath3 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\caption_3.srt'
    captionPath4 = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\caption_4.srt'
    captionLanguage1 = "English"
    captionLanguage2 = "Latin"
    captionLanguage3 = "German"
    captionLanguage4 = "Italian"
    captionLabel1 = "EN"
    captionLabel2 = "LT"
    captionLabel3 = "DE"
    captionLabel4 = "IT"
    captionTab = enums.EditEntryPageTabName.CAPTIONS
    
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
            writeToLog("INFO","Going to upload an entry that should contain four captions")           
                                          
            writeToLog("INFO","Step 1: Going to upload an entry to my media")            
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to upload an entry to my media")
                return
            
            writeToLog("INFO","Step 2: Going to enter in the entry page")
            if self.common.entryPage.navigateToEntry(self.entryName, self.navigateFrom) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 2: FAILED to enter in the entry page")
                return
            
            writeToLog("INFO", "STEP 3: Going to wait until the media is being processed")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 3: Failed to process the media file")
                return
                        
            writeToLog("INFO", "STEP 4: Going to navigate to the edit entry page")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO", "STEP 4: FAILED to enter in the edit entry page")
                return 
            
            writeToLog("INFO", "STEP 5: Going to insert caption  " + self.captionPath1 + " file")
            if self.common.editEntryPage.addCaptions(self.captionPath1, self.captionLanguage1, self.captionLabel1) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 5: FAILED to add captions to upload " + self.captionPath1 + " file")
                return

            writeToLog("INFO", "STEP 6: Going to insert caption  " + self.captionPath2 + " file")
            if self.common.editEntryPage.addCaptions(self.captionPath2, self.captionLanguage2, self.captionLabel2) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 6: FAILED to add captions to upload " + self.captionPath2 + " file")
                return
            
            writeToLog("INFO", "STEP 7: Going to insert caption  " + self.captionPath3 + " file")
            if self.common.editEntryPage.addCaptions(self.captionPath3, self.captionLanguage3, self.captionLabel3) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 7: FAILED to add captions to upload " + self.captionPath3 + " file")
                return

            writeToLog("INFO", "STEP 8: Going to insert caption  " + self.captionPath4 + " file")
            if self.common.editEntryPage.addCaptions(self.captionPath4, self.captionLanguage4, self.captionLabel4) == False:
                self.status = "Fail"
                writeToLog("INFO", "Step 8: FAILED to add captions to upload " + self.captionPath4 + " file")
                return
             
            writeToLog("INFO","TEST PASSED: Entry has been successfully uploaded with four captions") 
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