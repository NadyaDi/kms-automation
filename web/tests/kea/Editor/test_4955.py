import time, pytest
import sys,os
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','..','lib')))
from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections


class Test:

    #================================================================================================================================
    #  @Author: Horia Cus
    # Test Name : Editor: Trim Quiz entry (with Slides and Captions)
    # Test description:
    # 1. Verify that the captions and slides are properly displayed after and before trimming the quiz entry
    # 2. Verify that the questions are properly displayed after and before trimming the quiz  entry
    #================================================================================================================================
    testNum = "4955"

    supported_platforms = clsTestService.updatePlatforms(testNum)

    status = "Fail"
    driver = None
    common = None
    # Test variables

    testType                = "Quiz entry that was Trimmed while having Slides and Captions"
    description             = "Description"
    tags                    = "Tags,"
    entryName               = None
    quizEntryName           = None
    quizEntryNameClipped    = None
    entryDescription        = "description"
    entryTags               = "tag1,"

    captionLanguage = 'Afar'
    captionLabel = 'abc'
    captionText = '- Caption search 2'

    # Variables used in order to create a video entry with Slides and Captions
    filePathCaption = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\captions\Trim-Caption.srt'
    filePathVideo = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    slideDeckFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\10SlidestimelineQRCode.pptx'
    slidesQrCodeAndTimeList = None
    deleteSlidesList = None

    # List and dictionary used in order to create and verify a Quiz
    questionNumber1 = ['00:05', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4']
    questionNumber2 = ['00:10', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4']
    questionNumber3 = ['00:17', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']
    questionNumber4 = ['00:20', enums.QuizQuestionType.Multiple, 'question #4 Title', 'question #4 option #1', 'question #4 option #2', 'question #4 option #3', 'question #4 option #4']
    questionNumber5 = ['00:25', enums.QuizQuestionType.Multiple, 'question #5 Title', 'question #5 option #1', 'question #5 option #2', 'question #5 option #3', 'question #5 option #4']
    dictQuestions = {'1':questionNumber1,'2':questionNumber2,'3':questionNumber3,'4':questionNumber4,'5':questionNumber5}

    questionClip1 = ['00:05', enums.QuizQuestionType.Multiple, 'question #1 Title', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4']
    questionClip2 = ['00:10', enums.QuizQuestionType.Multiple, 'question #2 Title', 'question #2 option #1', 'question #2 option #2', 'question #2 option #3', 'question #2 option #4']
    questionClip5 = ['00:15', enums.QuizQuestionType.Multiple, 'question #5 Title', 'question #5 option #1', 'question #5 option #2', 'question #5 option #3', 'question #5 option #4']
    dictQuestionsClippedExist = {'1':questionClip1,'2':questionClip2,'3':questionClip5}

    questionClip3 = ['00:17', enums.QuizQuestionType.Multiple, 'question #3 Title', 'question #3 option #1', 'question #3 option #2', 'question #3 option #3', 'question #3 option #4']
    questionClip4 = ['00:20', enums.QuizQuestionType.Multiple, 'question #4 Title', 'question #4 option #1', 'question #4 option #2', 'question #4 option #3', 'question #4 option #4']
    dictQuestionsClippedAbsent = {'4':questionClip3,'5':questionClip4}

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


            # Variables used in order to proper create the Entry and the Slides inside it
            self.entryName             = clsTestService.addGuidToString("Quiz Trimmed with Slides and Captions", self.testNum)
            self.quizEntryName         = clsTestService.addGuidToString("Quiz Trimmed with Slides and Captions - Quiz", self.testNum)

            expectedEntryDuration = "0:20"

            self.slidesQrCodeAndTimeList = [('0','00:00'), ('1','00:01'),('2','00:02'), ('3','00:03'), ('4','00:04'), ('5','00:05'), ('6','00:06'), ('7','00:07'), ('8','00:08'), ('9','00:09'),
                                            ('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'),
                                            ('20','00:20'), ('21','00:21'), ('22','00:22'), ('23','00:23'), ('24','00:24'), ('25','00:25'), ('26','00:26'), ('27','00:27'), ('28','00:28'), ('29','00:29')]
            self.slidesQrCodeAndTimeList = collections.OrderedDict(self.slidesQrCodeAndTimeList)


            self.deleteSlidesList = [('10','00:10'), ('11','00:11'), ('12','00:12'), ('13','00:13'), ('14','00:14'), ('15','00:15'), ('16','00:16'), ('17','00:17'), ('18','00:18'), ('19','00:19'), ('20','00:20'), ('21','00:21')]
            self.deleteSlidesList = collections.OrderedDict(self.deleteSlidesList)
            ##################### TEST STEPS - MAIN FLOW #####################
            writeToLog("INFO","Step 1: Going to upload " + self.entryName + " entry")
            if self.common.upload.uploadEntry(self.filePathVideo, self.entryName, self.entryDescription, self.entryTags, disclaimer=False) == None:
                writeToLog("INFO","Step 1: FAILED to upload " + self.entryName + " entry")
                return
  
            writeToLog("INFO","Step 2: Going to create a Quiz for " + self.entryName + " entry")
            if self.common.kea.quizCreation(self.entryName, self.dictQuestions, timeout=30) == False:
                writeToLog("INFO","Step 2: FAILED to create a Quiz for " + self.entryName + " entry")
                return
  
            self.common.base.refresh()
            sleep(8)
  
            writeToLog("INFO","Step 3: Going to navigate to edit entry page for " + self.quizEntryName + " entry")
            if self.common.editEntryPage.navigateToEditEntryPageFromEntryPage(self.quizEntryName) == False:
                writeToLog("INFO","Step 3: FAILED to navigate to edit entry page for " + self.quizEntryName + " entry")
                return
  
            writeToLog("INFO","Step 4: Going to upload a slide deck for the " + self.quizEntryName + " entry")
            if self.common.editEntryPage.uploadSlidesDeck(self.slideDeckFilePath, self.slidesQrCodeAndTimeList, False, False) == False:
                writeToLog("INFO","Step 4: FAILED to upload a slide deck for the " + self.quizEntryName + " entry")
                return
            sleep(60)
            writeToLog("INFO","Step 5: Going to navigate to the Captions Edit Tab")
            if self.common.editEntryPage.clickOnEditTab(enums.EditEntryPageTabName.CAPTIONS) == False:
                writeToLog("INFO","Step 5: FAILED to navigate to the Captions Edit Tab")
                return
  
            writeToLog("INFO","Step 6: Going to add caption for the " + self.quizEntryName + " entry")
            if self.common.editEntryPage.addCaptions(self.filePathCaption, self.captionLanguage, self.captionLabel) == False:
                writeToLog("INFO","Step 6: FAILED to add caption for the " + self.quizEntryName + " entry")
                return
 
            writeToLog("INFO","Step 7: Going to collect all the available Questions from the " + self.quizEntryName + " entry, before trim")
            self.quizQuestionsBeforeTrimming = self.common.player.collectQuizQuestionsFromPlayer(self.quizEntryName, 5)
            if self.quizQuestionsBeforeTrimming == False:
                writeToLog("INFO","Step 7: FAILED to collect all the available Questions from the " + self.quizEntryName + " entry, before trim")
                return
             
            writeToLog("INFO","Step 8: Going to compare the presented Quiz Questions with the Expected Quiz Questions, before trim")
            if self.common.player.compareQuizQuestionDict(self.dictQuestions, self.quizQuestionsBeforeTrimming) == False:
                writeToLog("INFO","Step 8: FAILED to compare the presented Quiz Questions with the Expected Quiz Questions, before trimming") 
                return
 
            self.common.base.refresh()
            sleep(8)
 
            writeToLog("INFO","Step 9: Going to collect " + self.quizEntryName + " entrie's QR codes from Slider, before trim")
            self.QRlist = self.common.player.collectQrOfSlidesFromPlayer(self.quizEntryName, quizEntry=True, resumeFromBeginning=True)
            if  self.QRlist == False:
                writeToLog("INFO","Step 9: FAILED to collect " + self.quizEntryName + " entrie's QR codes from Slider, before trim")
                return
 
            self.isExistQR       = ["2", "4", "7"];
            self.isExistQRSecond = ["3", "6", "9"];
            self.isAbsentQR      = ["33", "55", "100", "99"];
            writeToLog("INFO","Step 10: Going to verify that the presented Slides matches with the Expected slides, before trim")
            if self.common.player.compareLists(self.QRlist, self.isExistQR, self.isAbsentQR, enums.PlayerObjects.QR) == False:
                # Because we may have a QR code that couldn't be catch we add a redundancy
                writeToLog("INFO","Step 10.1: FAILED to verify that the presented Slides matches with the Expected slides, while using the first list of QR Codes, before trim")
                if self.common.player.compareLists(self.QRlist, self.isExistQRSecond, self.isAbsentQR, enums.PlayerObjects.QR) == False:           
                    writeToLog("INFO","Step 10.2: FAILED to verify that the presented Slides matches with the Expected slides, while using the second list of QR Codes, before trim")
                    return
 
            self.common.base.refresh()
            sleep(8)
 
            writeToLog("INFO","Step 11: Going to collect all the presented captions from the " + self.quizEntryName + " entrie's player, before trim")
            self.captionList = self.common.player.collectCaptionsFromPlayer(self.quizEntryName, quizEntry=True)
            if  self.captionList == False:
                writeToLog("INFO","Step 11: FAILED to collect all the presented captions from the " + self.quizEntryName + " entrie's player, before trim")
                return
 
            self.isExist = ["Caption2search", "Caption7search", "Caption14search"];
            self.isAbsent = ["Caption100search", "Caption32search"];
            writeToLog("INFO","Step 11: Going to verify that the presented captions for " + self.quizEntryName + " entry displays the expected ones, before trim")
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.CAPTIONS) == False:
                writeToLog("INFO","Step 11: FAILED to verify that the presented captions for " + self.quizEntryName + " entry displays the expected ones, before trim")
                return
  
            writeToLog("INFO","Step 12: Going to clip the " + self.quizEntryName + " entry from second 12 to second 22, leaving a length of the entry of 20 seconds")
            if self.common.kea.trimEntry(self.quizEntryName, "00:12", "00:22", expectedEntryDuration, enums.Location.EDIT_ENTRY_PAGE, enums.Location.MY_MEDIA, openEditorTab=True) == False:
                writeToLog("INFO","Step 12: FAILED to clip the " + self.quizEntryName + " entry from second 12 to second 22, leaving a length of the entry of 20 seconds")
                return
  
            writeToLog("INFO","Step 13: Going to collect all the available Questions from the " + self.quizEntryName + " entry, after trim")
            self.qestionCollectedAfterTrim = self.common.player.collectQuizQuestionsFromPlayer(self.quizEntryName, 3)
            if self.qestionCollectedAfterTrim == False:
                writeToLog("INFO","Step 13: FAILED to collect all the available Questions from the " + self.quizEntryName + " entry, after trim")
                return
  
            writeToLog("INFO","Step 14: Going to compare the presented Quiz Questions with the Expected Quiz Questions, after trim")
            if self.common.player.compareQuizQuestionDict(self.qestionCollectedAfterTrim, self.dictQuestionsClippedExist, self.dictQuestionsClippedAbsent) == False:
                writeToLog("INFO","Step 14: FAILED to compare the presented Quiz Questions with the Expected Quiz Questions, after trim")
                return
  
            self.common.base.refresh()
            sleep(8)
 
            writeToLog("INFO","Step 15: Going to collect " + self.quizEntryName + " entrie's QR codes from Slider, after trim")
            self.QRlist = self.common.player.collectQrOfSlidesFromPlayer(self.quizEntryName, quizEntry=True, resumeFromBeginning=True)
            if  self.QRlist == False:
                writeToLog("INFO","Step 15: FAILED to collect " + self.quizEntryName + " entrie's QR codes from Slider, after trim")
                return
 
            self.isExistQR = ["1", "2", "9"];
            self.isAbsentQR = ["6", "7", "16", "12"];
            writeToLog("INFO","Step 16: Going to verify that the presented Slides matches with the Expected slides, after trim")
            if self.common.player.compareLists(self.QRlist, self.isExistQR, self.isAbsentQR, enums.PlayerObjects.QR) == False:
                writeToLog("INFO","Step 16: FAILED to verify that the presented Slides matches with the Expected slides, after trim")
                return
 
            self.common.base.refresh()
            sleep(8)

            writeToLog("INFO","Step 17: Going to collect all the presented captions from the " + self.quizEntryName + " entrie's player, after trim")
            self.captionList = self.common.player.collectCaptionsFromPlayer(self.quizEntryName, quizEntry=True)
            if  self.captionList == False:
                writeToLog("INFO","Step 17: FAILED to collect all the presented captions from the " + self.quizEntryName + " entrie's player, after trim")
                return

            self.isExist = ["Caption1search", "Caption7search", "Caption23search"];
            self.isAbsent = ["Caption18search", "Caption14search", "Caption15search", "Caption17search"];
            writeToLog("INFO","Step 18: Going to verify that the presented captions for " + self.quizEntryName + " entry displays the expected ones, after trim")
            if self.common.player.compareLists(self.captionList, self.isExist, self.isAbsent, enums.PlayerObjects.CAPTIONS) == False:
                writeToLog("INFO","Step 18: FAILED to verify that the presented captions for " + self.quizEntryName + " entry displays the expected ones, after trim")
                return
            ######################################################################################################
            self.status = "Pass"
            writeToLog("INFO","TEST PASSED, all the elements were properly verified for a " + self.testType)
        # if an exception happened we need to handle it and fail the test
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)

    ########################### TEST TEARDOWN ###########################
    def teardown_method(self,method):
        try:
            self.common.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************")
            self.common.myMedia.deleteEntriesFromMyMedia([self.entryName, self.quizEntryName])
            writeToLog("INFO","**************** Ended: teardown_method *******************")
        except:
            pass
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")

    pytest.main('test_' + testNum  + '.py --tb=line')