import time, pytest

from clsCommon import Common
import clsTestService
from localSettings import *
import localSettings
from utilityTestFunc import *
import enums
import collections


class Test:
    
    #================================================================================================================================
    #  @Author: Michal Zomper
    # Test description:
    # Slide Deck Upload add/remove chapters:
    # Enter entry edit page and go to time line tab
    # Upload a pdf file.
    # All file slides will spread evenly in the entry time line
    # In the player check that all the slides appear in the slides menu
    # From the Time line add several chapters 
    # In the player verify that the correct slides display under the correct chapter in the slides menu
    # Go again to time line tab - remove the added chapter
    # In the player verify that the chapter doen't display any more and that all the slides are still display in the slides menu
    #================================================================================================================================
    testNum     = "3275"
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
    filePath = localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\videos\30secQrMidLeftSmall.mp4'
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
            self.entryName = clsTestService.addGuidToString("SlideDeckUpload add-remove chapters", self.testNum)

            # The key is the qrcode result and the value is the time that the slide need to appear in
            # for example: {'2':'00:01'} - the key is 2 and the value is 00:01 mean that the qrcode of the slide in 00:01 second is 2
            self.slidesQrCodeAndTimeList = collections.OrderedDict()  
            self.slidesQrCodeAndTimeList = {'0': '00:00', '1': '00:01','2': '00:02', '3': '00:03','4': '00:04','5': '00:05', '6': '00:06', '7': '00:07', '8': '00:08', '9': '00:09',
                                            '10': '00:10', '11': '00:11','12': '00:12', '13': '00:13','14': '00:14','15': '00:15', '16': '00:16', '17': '00:17', '18': '00:18', '19': '00:19',
                                            '20': '00:20', '21': '00:21','22': '00:22', '23': '00:23','24': '00:24','25': '00:25', '26': '00:26', '27': '00:27', '28': '00:28', '29': '00:29'}
            self.chaptersList = collections.OrderedDict() 
            self.chaptersList = {'First Chapter':'00:05', 'Second Chapter':'00:14'}
            
            self.slidesWithoutChapter = collections.OrderedDict() 
            self.slidesWithoutChapter = {'0': '00:00', '1': '00:01','2': '00:02', '3': '00:03','4': '00:04'}
            
            self.firstChapterSlidesList = collections.OrderedDict() 
            self.firstChapterSlidesList = {'1.1': '00:05', '1.2': '00:06', '1.3': '00:07', '1.4': '00:08', '1.5': '00:09', '1.6': '00:10', '1.7': '00:11','1.8': '00:12', '1.9': '00:13'}
            
            self.secondChapterSlidesList = collections.OrderedDict() 
            self.secondChapterSlidesList = {'2.1': '00:14','2.2': '00:15', '2.3': '00:16', '2.4': '00:17', '2.5': '00:18', '2.6': '00:19','2.7': '00:20', '2.8': '00:21','2.9': '00:22',
                                            '2.10': '00:23', '2.11': '00:24','2.12': '00:25', '2.13': '00:26', '2.14': '00:27', '2.15': '00:28', '2.16': '00:29'}
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
             
            writeToLog("INFO","Step 6: Going to verify that all slides that aren't in chapters display in the slides side menu")
            if self.common.player.verifySlidesInPlayerSideBar(self.slidesWithoutChapter, checkSize=False) == False:
                writeToLog("INFO","Step 6: FAILED to verify that all slides that aren't in chapters display in the slides side menu")
                self.status = "Fail"
                return
             
            self.common.player.switchToPlayerIframe() 
            writeToLog("INFO","Step 7: Going to close slides menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 7: FAILED to click and open slides bar menu")
                return
             
            writeToLog("INFO","Step 8: Going to verify that chapter one is display correctly in the player (in entry page)")
            if self.common.player.vrifyChapterAndSlidesInSlidesMenuBarInEntrypage(next(iter(self.chaptersList)), self.firstChapterSlidesList, chapterIsclose=True) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 8: FAILED to verify chapter one and all of his slides")
                return            
               
            writeToLog("INFO","Step 9: Going to open slides menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 9: FAILED to click and open slides bar menu")
                self.status = "Fail"
                return
               
            # click on the EXPAND_COLLAPSE button in the slides menu bar in order to open all the chapters
            self.common.base.click(self.common.player.PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS)
            self.common.base.click(self.common.player.PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS)
               
            writeToLog("INFO","Step 10: Going to close slides menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 10: FAILED to click and open slides bar menu")
                return
               
            writeToLog("INFO","Step 11: Going to verify that chapter two is display correctly in the player (in entry page)")
            if self.common.player.vrifyChapterAndSlidesInSlidesMenuBarInEntrypage("Second Chapter", self.secondChapterSlidesList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 11: FAILED to verify chapter two and all of his slides")
                return  
              
            self.common.base.switch_to_default_content()
            writeToLog("INFO","Step 12: Going to delete chapters")
            if self.common.editEntryPage.deletechpaters(self.entryName, self.chaptersList) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 12: FAILED to delete chapters")
                return
            
            writeToLog("INFO","Step 13: Going to navigate to entry page")
            if self.common.entryPage.navigateToEntryPageFromMyMedia(self.entryName) == False:
                writeToLog("INFO","Step 13: FAILED to navigate to entry page")
                self.status = "Fail"
                return
            
            self.common.player.switchToPlayerIframe() 
            writeToLog("INFO","Step 14: Going to open slide menu bar")
            if self.common.base.click(self.common.player.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
                writeToLog("INFO","Step 14: FAILED to click and open slides bar menu")
                self.status = "Fail"
                return

            writeToLog("INFO","Step 15: Going to verify that all chapters were deleted")              
            # click on the EXPAND_COLLAPSE button in the slides menu bar in order to open all the chapters
            self.common.base.click(self.common.player.PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS)
            for chapter in self.chaptersList:
                if self.common.player.MoveToChapter(chapter, timeOut=5) == True:
                    writeToLog("INFO","Step 15:FAILED chapter '" + chapter + "' was found although he was deleted")
                    self.status = "Fail"
                    return
                writeToLog("INFO","Step 15: Previous Step Failed as Expected - The chapter '" +  chapter + "' should not be displayed")
                
                
            sleep(4)
            writeToLog("INFO","Step 16: Going to switch the player view so that the player will be in the big window and the slides in the small window")
            if self.common.player.changePlayerView(enums.PlayerView.SWITCHVIEW) == False:
                self.status = "Fail"
                writeToLog("INFO","Step 16: FAILED to switch the player view")
                return  
            
            sleep(3)
            index = 0
            writeToLog("INFO","Step 17: Going to check 4 slide (slide from the start / 2 in the middle / end of the video) and see that they appear at the correct time and did not deleted with the chapter")
            for i in range(4):
                sleep(2)
                index = index + i + 4 
                if self.common.player.verifySlideDisplayAtTheCorrctTime(self.slidesQrCodeAndTimeList[str(index)][1:], index) == False:
                    self.status = "Fail"
                    writeToLog("INFO","Step 17: FAILED to verify slide")
                    return  

            #########################################################################
            writeToLog("INFO","TEST PASSED: 'Slide Deck Upload - add/remove chapters' was done successfully")            
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
