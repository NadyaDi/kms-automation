from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from base import *
import clsTestService
import enums


class Player(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=====================================================================================================================
    #                                                      Channel locators:                 
    #=====================================================================================================================
    PLAYER_IFRAME                                               = ('id', 'kplayer_ifp')
    PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER                       = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-play')]")
    PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER                      = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-pause')]")
    PLAYER_REPLAY_BUTTON_CONTROLS_CONTAINER                     = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-replay')]")
    PLAYER_GENERIC_PLAY_REPLAY_PASUSE_BUTTON_CONTROLS_CONTAINER = ('xpath', "//button[@data-plugin-name='playPauseBtn']")
    PLAYER_CURRENT_TIME_LABEL                                   = ('xpath', "//div[@data-plugin-name='currentTimeLabel']")
    PLAYER_SLIDE_SIDE_BAR_MENU                                  = ('xpath', "//div[@id='sideBarContainerReminderContainer' and @class='icon-chapterMenu']")
    PLAYER_SLIDE_IN_SIDE_MENU                                   = ('xpath', "//li[@class='mediaBox slideBox']")
    PLAYER_VIEW_PIP                                             = ('id','pip')
    PLAYER_VIEW_SIDEBYSIDE                                      = ('id','sideBySide')
    PLAYER_VIEW_SINGLEVIEW                                      = ('id','singleView')
    PLAYER_VIEW_SWITCHVIEW                                      = ('id','switchView')
    PLAYER_LAYOUT                                               = ('id','kplayer')
    PLAYER_SIDE_BAR_MENU_PARENT                                 = ('xpath',"//div[@class='nano-content']")   
    PLAYER_SLIDE_IN_SIDE_BAR_MENU                               = ('xpath',"//li[contains (@class,'mediaBox slideBox')]")
    PLAYER_SILDE_START_TIME                                     = ('xpath', "//span[contains(text(), 'SLIDE_TIME')]") # When using this locator, replace 'SLIDE_TIME' string with your real slide_time
    PLAYER_SLIDE_RESULT_NO_MATCH                                = ('xpath', "//li[contains(@class,'resultNoMatch')]")
    PLAYER_SCROLLER_SIDE_BAR_MENU                               = ('xpath', "//div[@class='nano-slider']")
    PLAYER_SLIDE_MENU_BAR_CANCEL_SEARCH_BUTTON                  = ('xpath', "//div[@id='searchBoxCancelIcon' and @class='searchIcon icon-clear tooltipBelow active']")
    PLAYER_SLIDE_DECK_CHAPTER_PARENT                            = ('xpath', "//span[@class='k-chapter-title' and @title='CHAPTER_NAME']/ancestor::div[@class='boxInfo']")# When using this locator, replace 'CHAPTER_NAME' string with your real chapter name
    PLAYER_SLIDE_DECK_CHAPTER                                   = ("xpath", "//span[@class='k-chapter-title' and @title='CHAPTER_NAME']")# When using this locator, replace 'CHAPTER_NAME' string with your real chapter name
    PLAYER_SLIDE_NUMBER                                         = ('xpath', "//div[@class='slideNumber' and @title='Slide number' and contains(text(),'SLIDE_NUMBER')]") # When using this locator, replace 'SLIDE_NUMBER' string with your real slide number
    PLAYER_OPEN_CHAPTER_ICON                                    = ('xpath', "//div[@class='slideBoxToggle icon-toggle' and @title='Expand/collapse chapter']")
    PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS                         = ('xpath', "//span[@class='toggleAll icon-toggleAll']")
    PLAYER_QUIZ_CONTINUE_BUTTON                                 = ('xpath', "//div[@class='confirm-box' and text()='Continue']")
    PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON                             = ('xpath', "//div[@class='ftr-right' and text()='SKIP FOR NOW']")
    PLAYER_SEARCH_TEXTBOX_IN_SLIDES_BAR_MENU                    = ('xpath', "//input[@id='searchBox' and @placeholder='Search']")
    #=====================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here switches to player Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any player method, please use switchToPlayerIframe method, before addressing to player elements
    # because you need to switch to player iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method to 
    # return to default iframe in the end of use of player methods or elements, meaning in the test or other classes.
    #======================================================================================================================
    def switchToPlayerIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
            return True
        else:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER
            self.wait_visible(self.PLAYER_IFRAME, 60)
            self.swith_to_iframe(self.PLAYER_IFRAME)
            return True
    
    
    # fromActionBar = True, to click play on the bar below the player
    # fromActionBar = Flase, to click play on middle of the screen player
    def clickPlay(self, fromActionBar=True):
        self.switchToPlayerIframe()
        if fromActionBar == True:
            if self.click(self.PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER) == False:
                writeToLog("INFO","FAILED to click Play; fromActionBar = " + str(fromActionBar))
                return False
            
        return True     
            
            
    # fromActionBar = True, to click pause on the bar below the player
    # fromActionBar = False, to click pause on middle of the screen player
    def clickPause(self, fromActionBar=True):
        self.switchToPlayerIframe()
        if fromActionBar == True:
            if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER) == False:
                writeToLog("INFO","FAILED to click Pause; fromActionBar = " + str(fromActionBar))
                return False
            
        return True      
    
    
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03'
    # additional = additional delay befor pause 
    def clickPlayAndPause(self, delay, timeout=30, additional=0):
        self.switchToPlayerIframe()
        if self.clickPlay() == False:
            return False
        
        # Wait for delay
        if self.wait_for_text(self.PLAYER_CURRENT_TIME_LABEL, delay, timeout) == False:
            writeToLog("INFO","FAILED to seek timer to: '" + delay + "'")
            return False
        sleep(additional)
        if self.clickPause() == False:
            return False
        
        return True
    
    # Author: Inbar Willman
    # Click play for quiz entry until specific given question
    def clickPlayUntilSpecificQuestion(self, questionNumber):
        self.switchToPlayerIframe()
        if self.clickPlay() == False:
            return False
        
        #Click continue button
        if self.click(self.PLAYER_QUIZ_CONTINUE_BUTTON) == False:
            writeToLog("INFO","FAILED to click quiz continue button")
            return False  
        
        for i in range(questionNumber):
            self.wait_visible(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON)
            if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON) == False:
                writeToLog("INFO","FAILED to click quiz skip for now button")
                return False 
            i = i + 1 
        
        return True    
    
    
    # The method will play, pause after the delay and verify the synchronization the image (qr code) with the current time label
    # tolerance - seconds: the deviation from the time and image.
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03')
    def clickPlayPauseAndVerify(self, delay, timeout=30, tolerance=1):
        if self.clickPlayAndPause(delay, timeout) == False:
            return False
        
        qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
        if qrCodeSc == False:
            return False
        
        result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
        if result == None:
            return False
        
        # Convert delay string to seconds
        qrCodeResultInSeconds = utilityTestFunc.convertTimeToSecondsMSS(delay)
        
        if (qrCodeResultInSeconds > int(result) + tolerance) or (qrCodeResultInSeconds < int(result) - tolerance) == True:
            writeToLog("INFO","FAILED to verify playing, the image and timer are not synchronized; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
            return False
        
        writeToLog("INFO","Playing verified; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
        return True
    
    
    # The method chack the qr code on the player thumbnail
    def verifyThumbnailInPlayer(self, expecterQrCode):        
        qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
        if qrCodeSc == False:
            writeToLog("INFO","FAILED to take qr screen shot")
            return False
        
        result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
        if result == None:
            writeToLog("INFO","FAILED to resolve qr code")
            return False
        
        if str(expecterQrCode) != result:
            writeToLog("INFO","FAILED to verify thumbnail, the image and in the tumbnail is '" + str(result) + "' but need to be '" + str(expecterQrCode) + "'")
            return False
        
        writeToLog("INFO","Thumbnail was verified")
        return True
    
    
    # The method will play, pause after the delay and verify the synchronization the image (qr code) with the current time label
    # tolerance - seconds: the deviation from the time and image.
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03')
    def navigateToEntryClickPlayPause(self, entryName, delay, toVerify=True, timeout=30, tolerance=1):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False
                 
                if toVerify == True:  
                    if self.clickPlayPauseAndVerify(delay, timeout, tolerance) == False:
                        writeToLog("INFO","FAILED to click Play Pause And Verify")
                        return False
                else:
                    if self.clickPlayAndPause(delay, timeout) == False:
                        writeToLog("INFO","FAILED to click Play Pause")
                        return False                   
            else:
                writeToLog("INFO","Entry name not supplied")
                return False
            
        except NoSuchElementException:
            return False
          
        return True
    
    
    # @Author: Inbar Willman
    # The method will navigate to quiz entry page and play quiz until given question
    def navigateToQuizEntryAndClickPlay(self, entryName, questionNumber):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False
                 
                if self.clickPlayUntilSpecificQuestion(questionNumber) == False:
                    writeToLog("INFO","FAILED to click Play Pause")
                    return False                   
            else:
                writeToLog("INFO","Entry name not supplied")
                return False
            
        except NoSuchElementException:
            return False
          
        return True
        
    
    # The method will play, pause after the delay and verify the synchronization the image (qr code) with the current time label
    # tolerance - seconds: the deviation from the time and image.
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03')
    def navigateToEntryClickPlayPauseAndVerify2(self, entryName, delay, timeout=30, tolerance=1):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False 
                  
                if self.clickPlayPauseAndVerify(delay, timeout, tolerance) == False:
                    writeToLog("INFO","FAILED to click Play Pause And Verify")
                    return False
            else:
                writeToLog("INFO","Entry name not supplied")
                return False
            
        except NoSuchElementException:
            return False
          
        return True    
    
    
    # creator: Michal zomper
    # The function verify the slides in the menu slide bar
    # checking that the total number of slides is correct + verify that the time for each slide is correct 
    # checkSize parameter is to know when to check the slides list len 
    def verifySlidesInPlayerSideBar(self, mySlidesList, checkSize=True):
        self.switchToPlayerIframe()
        sleep(2)
        self.get_element(self.PLAYER_SLIDE_SIDE_BAR_MENU).send_keys(Keys.PAGE_UP)
        sleep(3)
        if self.click(self.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
            writeToLog("INFO","FAILED to click on the sides bar menu")
            return False
        
        sleep(2) 
        # find the parent of all menu slides
        sideMenu = self.get_element(self.PLAYER_SIDE_BAR_MENU_PARENT)
        # check if the number of slides is correct
        if checkSize == True:
            if len(sideMenu.find_elements_by_xpath(self.PLAYER_SLIDE_IN_SIDE_BAR_MENU[1])) != len(mySlidesList):
                writeToLog("INFO","FAILED to verify number of slides in side bar menu")
                return False
        sleep(2)
        
        if self.checkSlidesTimeInSlideBarMenu(mySlidesList) == False:
            writeToLog("INFO","FAILED to verify one or more slides in slide bar menu")
            return False
            
        writeToLog("INFO","SUCCESS verify slides in side bar menu")
        self.clsCommon.base.switch_to_default_content()
        sleep(2)
        return True
    
    
    # creator: Michal zomper
    # The Function go over the slides in the slide menu bar and verify that the time is correct 
    def checkSlidesTimeInSlideBarMenu(self, mySlidesList, isVerifySlideNumber=False):
        sleep(2)
        # Verify that the slides time is correct
        count = 0
        for slide in mySlidesList:
            sleep(1)
            slide_time = (self.PLAYER_SILDE_START_TIME[0], self.PLAYER_SILDE_START_TIME[1].replace('SLIDE_TIME', mySlidesList[slide]))
            if self.wait_visible(slide_time) == False:
                writeToLog("INFO","FAILED to verify slide time ' " + mySlidesList[slide] + "' in the slide menu bar")
                return False
            
            if isVerifySlideNumber == True:
                slideNumber = (self.PLAYER_SLIDE_NUMBER[0], self.PLAYER_SLIDE_NUMBER[1].replace('SLIDE_NUMBER',slide))
                if self.wait_visible(slideNumber) == False:
                    writeToLog("INFO","FAILED to verify slide number '" + slide +"' in slides menu bar")
                    return False

            # After the 4 slide we need to move the side menu scroller down so we can see the rest of the slides
            if count > 1:
                self.scrollInSlidesMenuBar(1)
            count = count + 1
        
        writeToLog("INFO","SUCCESS slides are display in the correct time in the slides bar menu")
        return True
        
        
    # creator: Michal zomper
    # The function move the scroller in the slides menu bar according to the size that the function get
    # size - the number of slides that need to scroll to get to the right point (in order to scroll down size need to be positive / in order to scroll up size need to be negative )
    def scrollInSlidesMenuBar(self, size):
        self.switchToPlayerIframe()
        #slideHeight = self.get_element(self.PLAYER_SCROLLER_SIDE_BAR_MENU).size['height']
        scroller = self.get_element(self.PLAYER_SCROLLER_SIDE_BAR_MENU)
        action = ActionChains(self.driver)
        #action.move_to_element(scroller).move_to_element_with_offset(scroller, 2.5, 3).click_and_hold().move_by_offset(0, 35).release().perform()
        action.move_to_element(scroller).click_and_hold().move_by_offset(0, 35*size).release().perform()
        
        
    # creator: Michal zomper
    def changePlayerView(self, playerView = enums.PlayerView.PIP):
        self.switchToPlayerIframe()
        #self.hover_on_element(self.PLAYER_LAYOUT)
        ActionChains(self.driver).move_to_element(self.get_element(self.PLAYER_LAYOUT)).perform()
        if playerView == enums.PlayerView.PIP:
            if self.click(self.PLAYER_VIEW_PIP, 30) == False:
                writeToLog("INFO","FAILED to click on pip view on the player")
                return False

        if playerView == enums.PlayerView.SIDEBYSIDE:
            if self.click(self.PLAYER_VIEW_SIDEBYSIDE, 30) == False:
                writeToLog("INFO","FAILED to click on sidebyside view on the player")
                return False

        if playerView == enums.PlayerView.SINGLEVIEW:
            if self.click(self.PLAYER_VIEW_SINGLEVIEW, 30) == False:
                writeToLog("INFO","FAILED to click on singleView view on the player")
                return False
            
        if playerView == enums.PlayerView.SWITCHVIEW:
            if self.click(self.PLAYER_VIEW_SWITCHVIEW, 30) == False:
                writeToLog("INFO","FAILED to click on switchView view on the player")
                return False
            
        writeToLog("INFO","SUCCESS to change player view")
        self.clsCommon.base.switch_to_default_content()
        return True
        
        
    # creator: Michal zomper
    # The function check that the slides display at the correct time when the player is running
    # The function check the QR code in the video, ptt are much and that they both much to the player time
    def verifySlideDisplayAtTheCorrctTime(self, timeToStop, qrResult):
        self.switchToPlayerIframe()
        
        sleep(2)
        if self.clickPlayAndPause(timeToStop, timeout=30) == False:
            writeToLog("INFO","FAILED to click on the player")
            return False
        
        videoImage =  self.clsCommon.qrcode.getScreenshotAndResolvePlayerQrCode(enums.PlayerPart.TOP)
        slideImage =  self.clsCommon.qrcode.getScreenshotAndResolvePlayerQrCode(enums.PlayerPart.BOTTOM)
        
        slideImageResult = int(slideImage)-1 <= int(qrResult) <= int(slideImage)+1 
        videoImage1Result = int(videoImage)-1 <= int(qrResult) <= int(videoImage)+1 
            
        if (slideImageResult == False or videoImage1Result == False) or (slideImageResult == False and videoImage1Result == False):
        #if (str(playerTime) == str(videoImage) == str(slideImage) == str(qrResult)) == False:
            writeToLog("INFO","FAILED,  video /image time are NOT match to the result that we are expecting. videoImage: " + str(videoImage) + " slideImage: " + str(slideImage))
            return False
        
        # Get the time in the player time line
        playerTime = utilityTestFunc.convertTimeToSecondsMSS((self.get_element(self.PLAYER_CURRENT_TIME_LABEL)).text)
         
        if (int(playerTime)-1 <= int(playerTime) <= int(playerTime)+1) == False:
            writeToLog("INFO","FAILED,  player time is NOT match to the result that we are expecting. plyerTime: " +  str(playerTime))
            return False
        
        writeToLog("INFO","SUCCESS, slide appear in the correct time")
        return True


    # creator: Michal zomper
    def verifySlidesDisplayAtTheCorrctTime(self, mySlidesList):
        self.switchToPlayerIframe()
        
        for slide in mySlidesList:
            if self.verifySlideDisplayAtTheCorrctTime(slide, mySlidesList[slide][1:]) == False:
                writeToLog("INFO","FAILED to verify slide:" + slide + " at time: " + mySlidesList[slide][1:])
                return False
            
        writeToLog("INFO","SUCCESS, all slides are verified and appear at the correct time")
        return True
                
    
    # creator: Michal zomper
    # The function checking all the info in the slides menu bar  
    # The function check that the chapters are display in the correct time + all the slides that need to be in the chapters display correctly
    def vrifyChapterAndSlidesInSlidesMenuBarInEntrypage(self, chapterName, slidesListInChapter, chapterIsclose=False): 
        self.switchToPlayerIframe() 
        sleep(2)
        if self.click(self.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
            writeToLog("INFO","FAILED to click and open slides bar menu")
            return False
        sleep(2)
    
        chapterDetails = (self.PLAYER_SLIDE_DECK_CHAPTER_PARENT[0], self.PLAYER_SLIDE_DECK_CHAPTER_PARENT[1].replace('CHAPTER_NAME', chapterName))
        try:
            details = self.get_element(chapterDetails)
        except NoSuchElementException:
            writeToLog("INFO","FAILED find chapter '" + chapterName + "' details")
            return False

        chapterDetailsList = (details.text).split('\n')
        sleep(1)
        # check chapter details
        if chapterDetailsList[1] != chapterName:
            writeToLog("INFO","FAILED, chapter name is not correct")
            return False
        
        # Check chapter start time
        if chapterDetailsList[2] != slidesListInChapter[next(iter(slidesListInChapter))]:
            writeToLog("INFO","FAILED, chapter time is not correct")
            return False
        
        sleep(2)
        if self.MoveToChapter(chapterName) == False:
            writeToLog("INFO","FAILED to hover chapter in slides menu bar")
            return False
        self.scrollInSlidesMenuBar(2)
        sleep(2)
        
        if chapterIsclose == True:
            el = details.find_element_by_xpath("..")
            child = self.get_child_element(el,self.PLAYER_OPEN_CHAPTER_ICON)
            sleep(2)
            self.scrollInSlidesMenuBar(1)
            # open chapter in order to see all the slides
            if self.clickElement(child) == False:
                writeToLog("INFO","FAILED to open chapter in order to see all the slides")
                return False
         
        sleep(1)   
        # Verify that all the slides in the chapter are correct
        if self.checkSlidesTimeInSlideBarMenu(slidesListInChapter, isVerifySlideNumber=True) == False:
            writeToLog("INFO","FAILED, can NOT verify that all the needed slides are display under chapter: " + chapterName)
            return False
        sleep(1)
        
        if self.click(self.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
            writeToLog("INFO","FAILED to click and close slides bar menu")
            return False
        
        sleep(2)
        writeToLog("INFO","SUCCESS," + chapterName + ":all slides are verified and appear at the correct time")
        return True
    
    
    # creator: Michal zomper
    # The function move the scroller in the slides menu bar so that the needed chapter is now display
    def MoveToChapter(self, chapterName, timeOut=10):
        tmpLocator = (self.PLAYER_SLIDE_DECK_CHAPTER[0], self.PLAYER_SLIDE_DECK_CHAPTER[1].replace('CHAPTER_NAME', chapterName))
        sleep(1)
        if self.hover_on_element(tmpLocator) == False:
            if self.click(tmpLocator, timeOut) == False:
                writeToLog("INFO","FAILED to find chapter")
                return False
        self.scrollInSlidesMenuBar(1)
        return True
        
    # creator: Michal zomper
    # The function only! check slides that changed their location in time line   
    def verifyslidesThatChangedLocationInTimeLine(self, changeTimeOfSlidesList):
        for slide in changeTimeOfSlidesList:
            slidetime = changeTimeOfSlidesList[slide]
            expectedSlideQrCodeResult =  utilityTestFunc.convertTimeToSecondsMSS(slide)
            
            if self.clickPlayAndPause(slidetime[1:], timeout=30) == False:
                writeToLog("INFO","FAILED to click on the player")
                return False
            
            videoImage =  self.clsCommon.qrcode.getScreenshotAndResolvePlayerQrCode(enums.PlayerPart.TOP)
            slideImage =  self.clsCommon.qrcode.getScreenshotAndResolvePlayerQrCode(enums.PlayerPart.BOTTOM)
              
            slideImageResult = int(slideImage)-1 <= int(expectedSlideQrCodeResult) <= int(slideImage)+1 
            videoImage1Result = int(videoImage)-1 <= int(utilityTestFunc.convertTimeToSecondsMSS(changeTimeOfSlidesList[slide])) <= int(videoImage)+1 
                
            if (slideImageResult == False or videoImage1Result == False) or (slideImageResult == False and videoImage1Result == False):
                writeToLog("INFO","FAILED to verify slide that was in time: " + str(expectedSlideQrCodeResult) + " changed to time: " + str(slidetime))
                return False
            
        writeToLog("INFO","SUCCESS, verify all slides changes")
        return True
      
    # creator: Michal zomper   
    # totalNumberOfslides - the total number of slides that were uploaded to the entry    
    def searchSlideInSlidesBarMenu(self, slidesForSearchList, totalNumberOfslides):   
        self.switchToPlayerIframe() 
        if self.click(self.PLAYER_SLIDE_SIDE_BAR_MENU, 30) == False:
            writeToLog("INFO","FAILED to click and open slides bar menu")
            return False
        sleep(2)
          
        for slide in slidesForSearchList:
            self.click(self.PLAYER_SEARCH_TEXTBOX_IN_SLIDES_BAR_MENU)
            searchEl = self.get_element(self.PLAYER_SEARCH_TEXTBOX_IN_SLIDES_BAR_MENU)
            ActionChains(self.driver).click(searchEl).send_keys(slide + Keys.SPACE + Keys.ENTER).perform()
            #ActionChains(self.driver).click(searchEl).send_keys(Keys.SPACE + Keys.ENTER).perform()
            
            
            slide_time = (self.PLAYER_SILDE_START_TIME[0], self.PLAYER_SILDE_START_TIME[1].replace('SLIDE_TIME', slidesForSearchList[slide]))
            if self.wait_visible(slide_time) == False:
                writeToLog("INFO","FAILED to verify slide time ' " + str(slidesForSearchList[slide]) + "' in the slide menu bar")
                return False
            
            # check that only one slide display
            if totalNumberOfslides-1 != len(self.get_elements(self.PLAYER_SLIDE_RESULT_NO_MATCH)):
                writeToLog("INFO","FAILED to verify  that only the slide '" + str(slide) + "' display in the search result")
                return False
                
            if self.click(self.PLAYER_SLIDE_MENU_BAR_CANCEL_SEARCH_BUTTON , 20) == False:
                writeToLog("INFO","FAILED to click on the search 'X' button in order to clean search textbox")
                return False
            
            writeToLog("INFO","SUCCESS, slide '" + str(slide) +"' at time '" + str(slidesForSearchList[slide]) + "' was found in search")
        
        writeToLog("INFO","SUCCESS, All slides were found after search in the slides menu bar")
        return True   

            