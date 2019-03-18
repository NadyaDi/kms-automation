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
    #  @Author: Inbar Willman
    # Test Name: Watch History - Filter by media type
    # The test's Flow: 
    # Login to KMS-> Upload entries from all types -> Go to entry page and play entry -> Go to
    # My History page and filter entries by media type - video
    # test cleanup: deleting the uploaded file
    #================================================================================================================================
    testNum     = "2697"
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Fail"
    driver = None
    common = None
    # Test variables
    entryDescription = "description"
    entryTags = "tag1,"
    QuizQuestion1 = 'First question'
    QuizQuestion1Answer1 = 'First answer'
    QuizQuestion1AdditionalAnswers = ['Second answer', 'Third question', 'Fourth question']
    questionNumber = 1
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePathQuiz = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR30SecMidRight.mp4'
    filePathAudio = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\Audios\audio.mp3'
    filePathImage = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\AutomatedBenefits.jpg'
    
    #run test as different instances on all the supported platforms
    @pytest.fixture(scope='module',params=supported_platforms)
    def driverFix(self,request):
        return request.param
    
    def test_01(self,driverFix,env):

        try:
            logStartTest(self,driverFix)
            ############################# TEST SETUP ###############################
            #capture test start time
            self.startTime = time.time()
            #initialize all the basic vars and start playing
            self,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            
            ########################################################################
            self.entryAudio = clsTestService.addGuidToString('audioType', self.testNum)
            self.entryVideo = clsTestService.addGuidToString('videoType', self.testNum)
            self.entryQuiz = clsTestService.addGuidToString('quizType', self.testNum)
            self.entryImage = clsTestService.addGuidToString('imageType', self.testNum)
            self.entriesToDelete = [self.entryAudio, self.entryVideo, self.entryQuiz + " - Quiz" , self.entryImage]
            self.entriesToUpload = {
                self.entryAudio: self.filePathAudio,
                self.entryVideo: self.filePathVideo,
                self.entryQuiz: self.filePathQuiz,
                self.entryImage: self.filePathImage
                }
            self.filterByImage = {self.entryAudio: False, self.entryVideo: False, self.entryQuiz + " - Quiz": False,self.entryImage: True}
            self.filterByAudio = {self.entryAudio: True, self.entryVideo: False, self.entryQuiz + " - Quiz": False, self.entryImage: False}
            self.filterByVideo = {self.entryAudio: False, self.entryVideo: True, self.entryQuiz + " - Quiz": False, self.entryImage: False}
            self.filterByQuiz = {self.entryAudio: False, self.entryVideo: False, self.entryQuiz + " - Quiz": True, self.entryImage: False}
            self.filterByAllMedia = {self.entryAudio: True, self.entryVideo: True, self.entryQuiz + " - Quiz": True, self.entryImage: True}
#             self.filterByImage = {'CCCAE781-2697-audioType': False, 'CCCAE781-2697-videoType': False, 'CCCAE781-2697-quizType - Quiz': False,'CCCAE781-2697-imageType': True}
#             self.filterByAudio = {'CCCAE781-2697-audioType': True, 'CCCAE781-2697-videoType': False, 'CCCAE781-2697-quizType - Quiz': False, 'CCCAE781-2697-imageType': False}
#             self.filterByVideo = {'CCCAE781-2697-audioType': False, 'CCCAE781-2697-videoType': True, 'CCCAE781-2697-quizType - Quiz': False, 'CCCAE781-2697-imageType': False}
#             self.filterByQuiz = {'CCCAE781-2697-audioType': False, 'CCCAE781-2697-videoType': False, 'CCCAE781-2697-quizType - Quiz': True, 'CCCAE781-2697-imageType': False}
#             self.filterByAllMedia = {'CCCAE781-2697-audioType': True, 'CCCAE781-2697-videoType': True, 'CCCAE781-2697-quizType - Quiz': True, 'CCCAE781-2697-imageType': True}
            ########################## TEST STEPS - MAIN FLOW #######################
            writeToLog("INFO","Step 1: Going to upload entries")
            if self.common.upload.uploadEntries(self.entriesToUpload, self.entryDescription, self.entryTags) == False:
                writeToLog("INFO","Step 1: FAILED to upload entry")
                return
              
            writeToLog("INFO","Step 2: Going to navigate to uploaded entry page")
            if self.common.entryPage.navigateToEntry(self.entryQuiz) == False:
                writeToLog("INFO","Step 2: FAILED to navigate to entry page")
                return  
              
            writeToLog("INFO","Step 3: Going to wait until media will finish processing")
            if self.common.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO","Step 3: FAILED - New entry is still processing")
                return
                           
            writeToLog("INFO","Step 4: Going to navigate to add new video quiz")
            if self.common.upload.addNewVideoQuiz() == False:
                writeToLog("INFO","Step 4: FAILED to click video quiz")
                return  
                
            writeToLog("INFO","Step 5: Going to search the uploaded entry and open KEA")
            if self.common.kea.searchAndSelectEntryInMediaSelection(self.entryQuiz, False) == False:
                writeToLog("INFO","Step 5: FAILED to find entry and open KEA")
                return  
                
            writeToLog("INFO","Step 6: Going to start quiz and add questions")
            if self.common.kea.addQuizQuestion(self.QuizQuestion1, self.QuizQuestion1Answer1, self.QuizQuestion1AdditionalAnswers) == False:
                writeToLog("INFO","Step 6: FAILED to start quiz and add questions")
                return   
                
            writeToLog("INFO","Step 7: Going to save quiz and navigate to media page")
            if self.common.kea.clickDone() == False:
                writeToLog("INFO","Step 7: FAILED to save quiz and navigate to media page")
                return 
  
            writeToLog("INFO","Step 8: Going to play quiz entry")
            if self.common.player.navigateToQuizEntryAndClickPlay(self.entryQuiz + " - Quiz", self.questionNumber) == False:
                writeToLog("INFO","Step 8: FAILED to navigate and play entry")
                return  
              
            writeToLog("INFO","Step 9: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                writeToLog("INFO","Step 9: FAILED to switch to default content")
                return
              
            writeToLog("INFO","Step 10: Going to play audio entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryAudio, '0:05', toVerify=False, timeout=50) == False:
                writeToLog("INFO","Step 10: FAILED to navigate and play audio entry")
                return 
             
            writeToLog("INFO","Step 9: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                writeToLog("INFO","Step 9: FAILED to switch to default content")
                return            
              
            writeToLog("INFO","Step 11: Going to play video entry")
            if self.common.player.navigateToEntryClickPlayPause(self.entryVideo, '0:05') == False:
                writeToLog("INFO","Step 11: FAILED to navigate and play video entry")
                return   
             
            writeToLog("INFO","Step 9: Going to switch to default content")
            if self.common.base.switch_to_default_content() == False:
                writeToLog("INFO","Step 9: FAILED to switch to default content")
                return            
              
            writeToLog("INFO","Step 12: Going to 'play' image entry")
            if self.common.entryPage.navigateToEntry(self.entryImage) == False:
                writeToLog("INFO","Step 12: FAILED to navigate and 'play' image entry")
                return 
            
            writeToLog("INFO","Step 13: Going to navigate to history page")
            if self.common.myHistory.navigateToMyHistory(True) == False:
                writeToLog("INFO","Step 12: FAILED to navigate to history page")
                return
            
            writeToLog("INFO","Step 14: Going to filter entries by media type audio")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.MEDIA_TYPE, dropDownListItem = enums.MediaType.AUDIO) == False:
                writeToLog("INFO","Step 14: FAILED to filter entries by media type audio")
                return   
            
            writeToLog("INFO","Step 15: Going to check that correct entries for audio filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByAudio) == False:
                writeToLog("INFO","Step 15: FAILED to displayed correct entries for audio type")
                return   
            
            writeToLog("INFO","Step 16: Going to verify that only entries with " + enums.MediaType.AUDIO.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryAudio], enums.MediaType.AUDIO) == False:
                writeToLog("INFO","Step 16: FAILED to filter and verify my media entries  by '" + enums.MediaType.AUDIO.value + "'")
                return
            
            writeToLog("INFO","Step 17: Going to filter entries by media video audio")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.MEDIA_TYPE, dropDownListItem = enums.MediaType.VIDEO) == False:
                writeToLog("INFO","Step 17: FAILED to filter entries by media type video")
                return              
            
            writeToLog("INFO","Step 18: Going to check that correct entries for video filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByVideo) == False:
                writeToLog("INFO","Step 18: FAILED to displayed correct entries for video type")
                return   
            
            writeToLog("INFO","Step 19: Going to verify that only entries with " + enums.MediaType.VIDEO.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryVideo], enums.MediaType.VIDEO) == False:
                writeToLog("INFO","Step 19: FAILED to filter and verify my media entries  by '" + enums.MediaType.VIDEO.value + "'")
                return 
            
            writeToLog("INFO","Step 20: Going to filter entries by media type quiz")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.MEDIA_TYPE, dropDownListItem = enums.MediaType.QUIZ) == False:
                writeToLog("INFO","Step 20: FAILED to filter entries by media type quiz")
                return              
            
            writeToLog("INFO","Step 21: Going to check that correct entries for quiz filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByQuiz) == False:
                writeToLog("INFO","Step 21: FAILED to displayed correct entries for quiz type")
                return   
            
            writeToLog("INFO","Step 22: Going to verify that only entries with " + enums.MediaType.QUIZ.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryQuiz + " - Quiz"], enums.MediaType.QUIZ) == False:
                writeToLog("INFO","Step 22: FAILED to filter and verify my media entries  by '" + enums.MediaType.QUIZ.value + "'")
                return  
            
            writeToLog("INFO","Step 23: Going to filter entries by media type audio")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.MEDIA_TYPE, dropDownListItem = enums.MediaType.IMAGE) == False:
                writeToLog("INFO","Step 23: FAILED to filter entries by media type audio")
                return                   
            
            writeToLog("INFO","Step 24: Going to check that correct entries for image filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByImage) == False:
                writeToLog("INFO","Step 24: FAILED to displayed correct entries for image type")
                return   
            
            writeToLog("INFO","Step 25: Going to verify that only entries with " + enums.MediaType.IMAGE.value + " icon display")  
            if self.common.myMedia.verifyEntryTypeIcon([self.entryImage], enums.MediaType.IMAGE) == False:
                writeToLog("INFO","Step 25: FAILED to filter and verify my media entries  by '" + enums.MediaType.IMAGE.value + "'")
                return 
            
            writeToLog("INFO","Step 26: Going to filter entries by media type audio")
            if self.common.myHistory.filterInMyHistory(dropDownListName = enums.MyHistoryFilters.MEDIA_TYPE, dropDownListItem = enums.MediaType.ALL_MEDIA) == False:
                writeToLog("INFO","Step 26: FAILED to filter entries by media type audio")
                return              
            
            writeToLog("INFO","Step 27: Going to check that correct entries for all media filter are displayed")
            if self.common.myHistory.verifyFiltersInMyHistory(self.filterByAllMedia) == False:
                writeToLog("INFO","Step 27: FAILED to displayed correct entries for all media type")
                return                                              
            #########################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED")
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)             
            writeToLog("INFO","**************** Starting: teardown_method **************** ")
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteEntriesFromMyMedia(self.entriesToDelete)
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass            
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')