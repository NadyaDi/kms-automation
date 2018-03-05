import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums


class Test:
    
    #==============================================================================================================
    # Test Description 
    # Test Description Test Description Test Description Test Description Test Description Test Description
    # Test Description Test Description Test Description Test Description Test Description Test Description
    #==============================================================================================================
    testNum     = "354"
    enableProxy = False
    
    supported_platforms = clsTestService.updatePlatforms(testNum)
    
    status = "Pass"
    timeout_accured = "False"
    driver = None
    common = None
    # Test variables
    entryName = None
    entryDescription = "Description"
    entryTags = "Tags,"
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\QR_30_sec_new.mp4'
    slideDeckFilePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\ppt\PDFtimelineQRCode.pdf'
    slidesQrCodeAndTimeList = None
    chaptersList = None
    slidesWithoutChapter = None
    firstChapterSlidesList = None
    secondChapterSlidesList = None
    
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
            self,capture,self.driver = clsTestService.initializeAndLoginAsUser(self, driverFix)
            self.common = Common(self.driver)
            self.entryName = clsTestService.addGuidToString("Slide Deck Upload - delete slides", self.testNum)

            # The key is the qrcode result and the value is the time that the slide need to appear in
            # for example: {'2':'00:01'} - the key is 2 and the value is 00:01 mean that the qrcode of the slide in 00:01 second is 2 
            self.slidesQrCodeAndTimeList = {'0': '00:00', '1': '00:01','2': '00:02', '3': '00:03','4': '00:04','5': '00:05', '6': '00:06', '7': '00:07', '8': '00:08', '9': '00:09',
                                            '10': '00:10', '11': '00:11','12': '00:12', '13': '00:13','14': '00:14','15': '00:15', '16': '00:16', '17': '00:17', '18': '00:18', '19': '00:19',
                                            '20': '00:20', '21': '00:21','22': '00:22', '23': '00:23','24': '00:24','25': '00:25', '26': '00:26', '27': '00:27', '28': '00:28', '29': '00:29'}
            
            self.newSlidesQrCodeAndTimeList = {'0': '00:00', '1': '00:01','2': '00:02', '3': '00:03','4': '00:04','5': '00:05', '6': '00:06', '7': '00:07', '8': '00:08', '9': '00:09',
                                            '10': '00:10', '11': '00:11','12': '00:12', '13': '00:13','14': '00:14','15': '00:15', '16': '00:16', '17': '00:17', '18': '00:18', '19': '00:19',
                                            '20': '00:20', '21': '00:21','22': '00:22', '23': '00:23','24': '00:24','25': '00:25', '26': '00:26', '27': '00:27', '28': '00:28', '29': '00:29'}
            ##################### TEST STEPS - MAIN FLOW ##################### 
       
            writeToLog("INFO","Step 1: Going to upload entry")
            if self.common.upload.uploadEntry(self.filePath, self.entryName, self.entryDescription, self.entryTags) == None:
                self.status = "Fail"
                writeToLog("INFO","Step 1: FAILED failed to upload entry")
                return
                          
            writeToLog("INFO","Step 2: Going to navigate to edit Entry Page")
            if self.common.editEntryPage.navigateToEditEntryPageFromMyMedia(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 2: FAILED to navigate to edit entry page")
                return
                 
            writeToLog("INFO","Step 3: Going add upload slide deck")
            if self.common.editEntryPage.uploadSlidesDeck(self.slideDeckFilePath, self.slidesQrCodeAndTimeList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 3: FAILED to add slides to entry time line")
                return
            
            
            
            
                             
            writeToLog("INFO","Step 4: Going add chapters")
            if self.common.editEntryPage.addChapters(self.entryName, self.chaptersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 4: FAILED to remove slides from time line")
                return
                
            writeToLog("INFO","Step 5: Going to navigate to entry page")
            if self.common.editEntryPage.navigateToEntryPageFromEditEntryPage(self.entryName) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 5: FAILED to navigate to entry page: " + self.entryName)
                return  
                
            writeToLog("INFO","Step 6: Going to verify that chapter one is display correctly in the player (in entry page)")
            if self.common.player.vrifyChapterAndSlidesInSlidesMenuBarInEntrypage(next(iter(self.chaptersList)), self.firstChapterSlidesList, chapterIsclose=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 6: FAILED to verify chapter one and all of his slides")
                return            
              
            writeToLog("INFO","Step 7: Going to open slides menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 7: FAILED to click and open slides bar menu")
                self.status = "Fail"
                return
              
            # click on the EXPAND_COLLAPSE button in the slides menu bar in order to open all the chapters
            self.common.base.click(self.common.player.PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS)
            self.common.base.click(self.common.player.PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS)
              
            writeToLog("INFO","Step 8: Going to close slides menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 8: FAILED to click and open slides bar menu")
                return
              
            writeToLog("INFO","Step 9: Going to verify that chapter two is display correctly in the player (in entry page)")
            if self.common.player.vrifyChapterAndSlidesInSlidesMenuBarInEntrypage("Second Chapter", self.secondChapterSlidesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 9: FAILED to verify chapter two and all of his slides")
                return  
              
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 10: Going to delete chapters")
            if self.common.editEntryPage.deletechpaters(self.entryName, self.chaptersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 10: FAILED to delete chapters")
                return
            
            writeToLog("INFO","Step 11: Going to navigate to entry page")
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 11: FAILED to navigate to entry page")
                self.status = "Fail"
                return
            
            self.common.player.switchToPlayerIframe() 
            writeToLog("INFO","Step 12: Going to open slide menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 121: FAILED to click and open slides bar menu")
                self.status = "Fail"
                return

            writeToLog("INFO","Step 13: Going to verify that all chapters was deleted")              
            # click on the EXPAND_COLLAPSE button in the slides menu bar in order to open all the chapters
            self.common.base.click(self.common.player.PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS)
            for chapter in self.chaptersList:
                if self.common.player.MoveToChapter(chapter, timeOut=5) == True:
                    writeToLog("INFO","Step 13:FAILED chapter '" + chapter + "' was found although he was deleted")
                    self.status = "Fail"
                    return
                writeToLog("INFO","Step 13: Previous Step Failed as Expected - The chapter '" +  chapter + "' should not be displayed")

            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Slide Deck Upload - delete slides' was done successfully")            
        # if an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = clsTestService.handleException(self,inst,self.startTime)
            
    ########################### TEST TEARDOWN ###########################    
    def teardown_method(self,method):
        try:
            self.common.base.handleTestFail(self.status)
            writeToLog("INFO","**************** Starting: teardown_method ****************") 
            self.common.base.switch_to_default_content()
            self.common.myMedia.deleteSingleEntryFromMyMedia(self.entryName)
            writeToLog("INFO","**************** Ended: teardown_method *******************")  
        except:
            pass       
        clsTestService.basicTearDown(self)
        #write to log we finished the test
        logFinishedTest(self,self.startTime)
        assert (self.status == "Pass")    

    pytest.main('test_' + testNum  + '.py --tb=line')