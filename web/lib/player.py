from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from base import *
import clsTestService
import enums
from PIL import Image
from selenium.common.exceptions import StaleElementReferenceException

class Player(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=====================================================================================================================
    #                                                      Channel locators:                 
    #=====================================================================================================================
    PLAYER_IFRAME                                               = ('xpath', "//iframe[@id='kplayer_ifp']")
    PLAYER_EMBED_IFRAME_1                                       = ('xpath', '//iframe[contains(@id,"kmsembed")]')
    PLAYER_EMBED_IFRAME_2                                       = ('id', 'kaltura_player')
    PLAYER_SCREEN                                               = ('id', 'kplayer')
    PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER                       = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-play')]")
    PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER                      = ('xpath', "//button[@class='btn comp playPauseBtn display-high icon-pause']")
    #PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER              = ('xpath', "//a[@class='icon-play  comp largePlayBtn  largePlayBtnBorder' and @aria-label='Play clip']")
    PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER              = ('xpath', "//a[@class='icon-play  comp largePlayBtn  largePlayBtnBorder']")
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
    PLAYER_OPEN_CHAPTER_ICON                                    = ('xpath', "//button[@class='slideBoxToggle icon-toggle' and @tabindex='TABINDEXID']")
    PLAYER_EXPAND_COLLAPSE_ALL_CHAPTERS                         = ('xpath', "//span[@class='toggleAll icon-toggleAll']")
    PLAYER_QUIZ_CONTINUE_BUTTON                                 = ('xpath', "//div[@class='confirm-box' and text()='Continue']")
    PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON                             = ('xpath', "//div[@class='ftr-right' and text()='SKIP FOR NOW']")
    PLAYER_SEARCH_TEXTBOX_IN_SLIDES_BAR_MENU                    = ('xpath', "//input[@id='searchBox' and @placeholder='Search']")
    PLAYER_CAPTIONS_SECTION                                     = ('xpath', '//span[@style="position: relative;" and contains(text(),"CAPTION_TEXT")]')
    PLAYER_CAPTIONS_TEXT                                        = ('xpath', "//span[@style='position: relative;']")
    PLAYER_TOTAL_VIDEO_LENGTH                                   = ('xpath', "//div[@class='timers comp durationLabel display-medium']")
    PLAYER_CURRENT_PLAYBACK_TIME                                = ('xpath', "//div[@class='timers comp currentTimeLabel display-high disabled']")
    PLAYER_QUIZ_ALMOST_DONE_SCREEN                              = ('xpath', "//div[@class='title-text padding20']")
    PLAYER_QUIZ_QUESTION_TITLE                                  = ('xpath', "//div[@class='display-question padding7']")
    PLAYER_QUIZ_ANSWER_NO_1                                     = ('xpath', "//p[@id='answer-0-text']")
    PLAYER_QUIZ_ANSWER_NO_2                                     = ('xpath', "//p[@id='answer-1-text']")
    PLAYER_QUIZ_ANSWER_NO_3                                     = ('xpath', "//p[@id='answer-2-text']")
    PLAYER_QUIZ_ANSWER_NO_4                                     = ('xpath', "//p[@id='answer-3-text']")
    PLAYER_CONTROLER_BAR                                        = ('xpath', "//div[@class='controlsContainer']") 
    #=====================================================================================================================
    #                                                           Methods:
    #
    # The use of any method here switches to player Iframe but doesn't return it to default
    # !!! IMPORTENT !!! IMPORTENT !!!  IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!! IMPORTENT !!!
    # Before implement any player method, please use switchToPlayerIframe method, before addressing to player elements
    # because you need to switch to player iframe. And...!!! use 'self.switch_to_default_content' (Basic class) method to 
    # return to default iframe in the end of use of player methods or elements, meaning in the test or other classes.
    #======================================================================================================================
    def switchToPlayerIframe(self, embed=False):
        if embed == True:
            if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.EMBED_PLAYER:
                return True
            else:
                localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.EMBED_PLAYER
                #Switch to first iframe
                self.wait_visible(self.PLAYER_EMBED_IFRAME_1, 60)
                self.swith_to_iframe(self.PLAYER_EMBED_IFRAME_1)
                
                #Switch to second iframe
                self.wait_visible(self.PLAYER_EMBED_IFRAME_2, 60)
                self.swith_to_iframe(self.PLAYER_EMBED_IFRAME_2)
                return True

        else:
            if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.PLAYER:
                return True
            else:
                self.clsCommon.switch_to_default_iframe_generic()
                localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER
                self.wait_element(self.PLAYER_IFRAME, 60)
                self.swith_to_iframe(self.PLAYER_IFRAME)
                return True
    
    
    # fromActionBar = True, to click play on the bar below the player
    # fromActionBar = False, to click play on middle of the screen player
    def clickPlay(self,embed=False, fromActionBar=True, sleepBeforePlay=0):
        sleep(sleepBeforePlay)
        self.switchToPlayerIframe(embed)
        if fromActionBar == True:
            playButtonControlsEl = self.wait_element(self.PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER)
            playBtnWidth = playButtonControlsEl.size['width'] / 3
            playBtnHeight = playButtonControlsEl.size['height'] / 1.1
            
            if self.click(self.PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER, width=playBtnWidth, height=playBtnHeight) == False:
                writeToLog("INFO","FAILED to click Play; fromActionBar = " + str(fromActionBar))
                return False
        elif fromActionBar == False:
            if self.click(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 20, True) == False:
                writeToLog("INFO","FAILED to click Play in the middle of the player; fromActionBar = " + str(fromActionBar))
                return False   
        
        return True     
            
            
    # fromActionBar = True, to click pause on the bar below the player
    # fromActionBar = False, to click pause on middle of the screen player
    def clickPause(self,  embed=False, fromActionBar=True):
        self.switchToPlayerIframe(embed)
        if fromActionBar == True:
            playButtonControlsEl = self.wait_element(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            playBtnWidth = playButtonControlsEl.size['width'] / 3
            playBtnHeight = playButtonControlsEl.size['height'] / 1.1
            if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, width=playBtnWidth, height=playBtnHeight) == False:
                writeToLog("INFO","FAILED to click Pause; fromActionBar = " + str(fromActionBar))
                return False
            
        elif fromActionBar == False:
            if self.click(self.PLAYER_SCREEN) == False:
                writeToLog("INFO","FAILED to click Pause in the middle of the player; fromActionBar = " + str(fromActionBar))
                return False
             
        return True      
    
    
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03'
    # additional = additional delay befor pause 
    def clickPlayAndPause(self, delay, timeout=30, embed=False, clickPlayFromBarline=True, additional=0):
        self.switchToPlayerIframe(embed)
        if self.clickPlay(embed, fromActionBar=clickPlayFromBarline) == False:
            return False
 
        # Wait for delay
        if self.wait_for_text(self.PLAYER_CURRENT_TIME_LABEL, delay, timeout) == False:
            writeToLog("INFO","FAILED to seek timer to: '" + str(delay) + "'")
            return False
        sleep(additional)
        if self.clickPause(embed, fromActionBar=clickPlayFromBarline) == False:
            return False
        
        return True 
    
    
    # @ Author: Tzachi Guetta
    # This function will play the player from start to end - and collect all the Captions that were presented on the player - and return list of Captions codes (filters the duplicates)     
    def collectCaptionsFromPlayer(self, entryName, embed=False, fromActionBar=True):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False
            
            if self.clickPlay(embed, fromActionBar, 10) == False:
                return False       
            
            playback = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            captionsList = [];
            
            while playback != False:
                try:
                    captionText = self.wait_element(self.PLAYER_CAPTIONS_TEXT).text
                    if captionText == False:
                        writeToLog("INFO","FAILED to extract caption from player")
                        return self.removeDuplicate(captionsList, enums.PlayerObjects.CAPTIONS)
    
                    
                    captionsList.append(captionText)
                    playback = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 3)
                    sleep(0.3)
                except StaleElementReferenceException:
                    pass    
                         
            self.clsCommon.base.switch_to_default_content()
            return self.removeDuplicate(captionsList, enums.PlayerObjects.CAPTIONS)
   
        except Exception as exp:
            return False  
    
    # @ Author: Tzachi Guetta
    # This function will play the player from start to end - and collect all the QR codes that were presented on the player - and return list of QR codes (filters the duplicates)     
    def collectQrTimestampsFromPlayer(self, entryName):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False
            
            if self.clickPlay(False, True, 10) == False:
                return False       
            
            QRcode = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            QRcodeList = [];
            
            while QRcode != False:
                
                qrPath = self.clsCommon.qrcode.takeQrCodeScreenshot(showLog=False)
                if qrPath == False:
                    writeToLog("INFO","FAILED to take QR code screen shot")
                    return self.removeDuplicate(QRcodeList, enums.PlayerObjects.QR)              
                
                qrResolve = self.clsCommon.qrcode.resolveQrCode(qrPath)
                if qrResolve == False:
                    writeToLog("INFO","FAILED to resolve QR code")
                    return self.removeDuplicate(QRcodeList, enums.PlayerObjects.QR)  
                
                QRcodeList.append(qrResolve)
                QRcode = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 3)
                sleep(0.3)
            
            return self.removeDuplicate(QRcodeList, enums.PlayerObjects.QR)
            
        except Exception:
            return False
    
    
    # @ Author: Tzachi Guetta
    # This function will play the player from start to end - and collect all the Quiz Questions that were presented on the player - and return dictionary of Questions details
    # Currently support question type=Multiple ONLY     
    def collectQuizQuestionsFromPlayer(self, entryName, expectedQuestionCount=0):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False 
            
            self.switchToPlayerIframe()
            if self.clickPlay(sleepBeforePlay=10) == False:
                return False  
            
            #Click continue button
            if self.click(self.PLAYER_QUIZ_CONTINUE_BUTTON, 45) == False:
                writeToLog("INFO","FAILED to click on Welcome Screen's continue button (Quiz Entry)")
                return False  

            replay = self.wait_element(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            questionList = {}
            key = 1
            
            while replay != False:      
                
                question = self.wait_element(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, timeout=30)
                if question != False:
                    
                    questiondetails = self.extractQuizQuestionDetails()
                    questionList.update({str(key):questiondetails})
                    key = key + 1
                    
                    # Default is 0, will wait till player will stop play
                    if expectedQuestionCount != 0:
                        if key > expectedQuestionCount:
                            break
                    
                    if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON) == False:
                        writeToLog("INFO","FAILED to click quiz skip for now button")
                        return False
                    else:
                        continue
                
                else:
                    if self.wait_element(self.PLAYER_QUIZ_ALMOST_DONE_SCREEN, timeout=3) != False:
                        replay = False
                        
            writeToLog("INFO","Passed;")
            self.clsCommon.base.switch_to_default_content()
            return questionList
            
        except Exception:
            writeToLog("INFO","FAILED to extract the question's text")
            return False    
        
    
    # @ Author: Tzachi Guetta
    #  
    def extractQuizQuestionDetails(self): 
        try:
            questionDetails = []
            timestamp  =  self.wait_element(self.clsCommon.player.PLAYER_CURRENT_PLAYBACK_TIME).text
            if  timestamp == False:
                writeToLog("INFO","FAILED to extract player's current time")
                return False
            questionDetails.append("0" + timestamp)
            
            questionDetails.append(enums.QuizQuestionType.Multiple)           
            
            questionTitle= self.wait_element(self.clsCommon.player.PLAYER_QUIZ_QUESTION_TITLE).text
            if  questionTitle == False:
                writeToLog("INFO","FAILED to extract the Question's title")
                return False
            questionDetails.append(questionTitle)
                        
            questionAnswer1= self.wait_element(self.clsCommon.player.PLAYER_QUIZ_ANSWER_NO_1).text
            if  questionAnswer1 == False:
                writeToLog("INFO","FAILED to extract the Question's answer no1")
                return False
            questionDetails.append(questionAnswer1)  

            questionAnswer2= self.wait_element(self.clsCommon.player.PLAYER_QUIZ_ANSWER_NO_2).text
            if  questionAnswer2 == False:
                writeToLog("INFO","FAILED to extract the Question's answer no2")
                return False
            questionDetails.append(questionAnswer2)
                      
            questionAnswer3= self.wait_element(self.clsCommon.player.PLAYER_QUIZ_ANSWER_NO_3).text
            if  questionAnswer3 == False:
                writeToLog("INFO","extract was not performed to Question's answer no3")
                return questionDetails
            questionDetails.append(questionAnswer3)
                       
            questionAnswer4= self.wait_element(self.clsCommon.player.PLAYER_QUIZ_ANSWER_NO_4).text
            if  questionAnswer4 == False:
                writeToLog("INFO","extract was not performed to Question's answer no3")
                return questionDetails
            questionDetails.append(questionAnswer4)
            
            return questionDetails
        
        except Exception:
            return False        
    
    # @ Author: Tzachi Guetta    
    def removeDuplicate(self, duplicateList, playerObject): 
        try:
            final_list = [] 
            for num in duplicateList: 
                if num not in final_list: 
                    final_list.append(num)
                    
            writeToLog("INFO","The " + str(playerObject) +"'s that were found on player: " + str(final_list))
            return final_list
                
        except Exception:
            return False        
    
            
    # @ Author: Tzachi Guetta    
    # this method is checking 2 things:
    # checking if "isExistList" is exist on qrList - and return True in case all of the values were found
    # checking if "isAbsentList" is NOT exist on qrList - and return True in case all of the values were NOT found
    def compareLists(self, qrList, isExistList, isAbsentList, playerObject):
        try:     
            for qr1 in isExistList:
                if qr1 in qrList:
                    writeToLog("INFO","As Expected: The " + str(playerObject) + ": '" + qr1 +"' found on player")
                    
                else:
                    writeToLog("INFO","NOT Expected: The " + str(playerObject) + ": '" + qr1 +"' Not found on player")
                    return False
                
            for qr2 in isAbsentList:
                if qr2 not in qrList:
                    writeToLog("INFO","As Expected: The " + str(playerObject) + ": '" + qr2 +"' not found on player")
                    
                else:
                    writeToLog("INFO","NOT Expected: The " + str(playerObject) + ": '" + qr2 +"' found on player")
                    return False            
                
        except Exception:
            return False
      
        return True
    
    # @ Author: Tzachi Guetta    
    # the following method will perform the following action:
    # for isExistDict:  
        #     the method will verify first that the length of isExistDict is equal the length of questionDict,
        #     than the method will compared the content of questionDict to isExistDict
    # for isExistDict:
        # the function will verify that isAbsentDict's KEYS are not found inside questionDict
    def  compareQuizQuestionDict(self, questionDict, isExistDict='', isAbsentDict=''):
        try:     
            if isExistDict != '':
                if len(questionDict) == len(isExistDict):
                    for key in isExistDict:
                        if key in questionDict:
                            i=0
                            writeToLog("INFO","Verifying Question number " + str(key))
                            
                            for questionItem in isExistDict[key]:
                                if questionItem == questionDict[key][i]:
                                    i += 1
                                else:
                                    writeToLog("INFO","NOT Expected: the following question item wasn't found: " + str(questionItem))
                                    return False
                else:
                    writeToLog("INFO","NOT Expected: the length of the question list and the isExist dictionary is not equal")
                    return False
                
            if isAbsentDict != '':
                for key in isAbsentDict:
                    if key in questionDict:
                        writeToLog("INFO","NOT Expected: the following question number was found: " + key)
                        return False            
                
        except Exception as exp:
            return False
      
        return True
    
    # Author: Inbar Willman
    # This method will wait for delay and click pause, without clicking play
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03'
    # additional = additional delay before pause 
    def waitForPause(self, delay, timeout=30, embed=False, clickPlayFromBarline=True, additional=0):
        self.switchToPlayerIframe(embed)
        
        # Wait for delay
        if self.wait_for_text(self.PLAYER_CURRENT_TIME_LABEL, delay, timeout) == False:
            writeToLog("INFO","FAILED to seek timer to: '" + str(delay) + "'")
            return False
        sleep(additional)
        if self.clickPause(embed, fromActionBar=clickPlayFromBarline) == False:
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
    # compareToStr - if compareToStr not '' than compare the Player QR to the given string (compareToStr)
    def clickPlayPauseAndVerify(self, delay, timeout=30, tolerance=1, clickPlayFromBarline=True, compareToStr=''):
        if self.clickPlayAndPause(delay, timeout, False, clickPlayFromBarline) == False:
            return False
       
        qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
        if qrCodeSc == False:
            return False
       
        result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
        if result == None:
            return False
       
        if compareToStr == '':
            # Convert delay string to seconds
            qrCodeResultInSeconds = utilityTestFunc.convertTimeToSecondsMSS(delay)
            if (qrCodeResultInSeconds > int(result) + tolerance) or (qrCodeResultInSeconds < int(result) - tolerance) == True:
                writeToLog("INFO","FAILED to verify playing, the image and timer are not synchronized; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
                return False           
        else:
            if (int(result) > int(compareToStr) + tolerance) or (int(result) < int(compareToStr) - tolerance) == True:
                writeToLog("INFO","FAILED to verify playing; compareToStr = " + str(compareToStr) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
                return False
       
        writeToLog("INFO","Playing verified; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
        return True
    
    # Author: Inbar Willman
    # The method will pause after the delay and verify the synchronization the image (qr code) with the current time label
    # tolerance - seconds: the deviation from the time and image.
    # delay - (string) time to play in seconds in format: M:SS (for example, 3 seconds = '0:03')
    # compareToStr - if compareToStr not '' than compare the Player QR to the given string (compareToStr)
    def clickPauseAndVerify(self, delay, timeout=30, tolerance=1, clickPlayFromBarline=True, compareToStr=''):
        if self.waitForPause(delay, timeout, False, clickPlayFromBarline) == False:
            return False
       
        qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
        if qrCodeSc == False:
            return False
       
        result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
        if result == None:
            return False
       
        if compareToStr == '':
            # Convert delay string to seconds
            qrCodeResultInSeconds = utilityTestFunc.convertTimeToSecondsMSS(delay)
            if (qrCodeResultInSeconds > int(result) + tolerance) or (qrCodeResultInSeconds < int(result) - tolerance) == True:
                writeToLog("INFO","FAILED to verify playing, the image and timer are not synchronized; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
                return False           
        else:
            if (int(result) > int(compareToStr) + tolerance) or (int(result) < int(compareToStr) - tolerance) == True:
                writeToLog("INFO","FAILED to verify playing; compareToStr = " + str(compareToStr) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
                return False
       
        writeToLog("INFO","Playing verified; delay = " + str(delay) + "; tolerance = " + str(tolerance) + "; Player QrCode = " + str(result))
        return True    
    
    
    # The method chack the qr code on the player thumbnail
    def verifyThumbnailInPlayer(self, expecterQrCode):
        application = localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST
        if application == enums.Application.BLACK_BOARD:
            if self.clsCommon.blackBoard.switchToBlackboardIframe() == False:
                return False
        self.switchToPlayerIframe()     
        qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
        if qrCodeSc == False:
            writeToLog("INFO","FAILED to take qr screen shot")
            return False
        
        result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
        if result == None:
            writeToLog("INFO","FAILED to resolve qr code")
            return False
        
        if str(expecterQrCode) != result:
            writeToLog("INFO","FAILED to verify thumbnail, the image in the tumbnail is '" + str(result) + "' but need to be '" + str(expecterQrCode) + "'")
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
                 
                sleep(3)
                 
                if toVerify == True:  
                    if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                        self.click(self.clsCommon.d2l.D2L_HEANDL_ENTRY_WIDGET_IN_ENTRY_PAGE, timeout=3)
                        self.get_body_element().send_keys(Keys.PAGE_DOWN)
                        
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
    
    
    # Author: Michal zomper
    # The function verify the slides in the menu slide bar
    # checking that the total number of slides is correct + verify that the time for each slide is correct 
    # checkSize parameter is to know when to check the slides list len 
    def verifySlidesInPlayerSideBar(self, mySlidesList, checkSize=True):
        sleep(2)
        self.get_body_element().send_keys(Keys.PAGE_UP)
        sleep(2)
        self.switchToPlayerIframe()
        if self.click(self.PLAYER_SLIDE_SIDE_BAR_MENU, 30, multipleElements=True) == False:
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
    
    
    # Author: Michal zomper
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
        
        
    # Author: Michal zomper
    # The function move the scroller in the slides menu bar according to the size that the function get
    # size - the number of slides that need to scroll to get to the right point (in order to scroll down size need to be positive / in order to scroll up size need to be negative )
    def scrollInSlidesMenuBar(self, size):
        self.switchToPlayerIframe()
        #slideHeight = self.get_element(self.PLAYER_SCROLLER_SIDE_BAR_MENU).size['height']
        scroller = self.get_element(self.PLAYER_SCROLLER_SIDE_BAR_MENU)
        action = ActionChains(self.driver)
        #action.move_to_element(scroller).move_to_element_with_offset(scroller, 2.5, 3).click_and_hold().move_by_offset(0, 35).release().perform()
        action.move_to_element(scroller).click_and_hold().move_by_offset(0, 35*size).release().perform()
        
        
    # Author: Michal zomper
    def changePlayerView(self, playerView = enums.PlayerView.PIP):
        self.switchToPlayerIframe()
        #self.hover_on_element(self.PLAYER_LAYOUT)
        ActionChains(self.driver).move_to_element(self.get_element(self.PLAYER_LAYOUT)).perform()
        sleep(0.5)
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
    
        
    # @ Author: Tzachi Guetta
    # This function will play the player from start to end - and collect all the QR codes that were presented on the Slides on the player - and return list of QR codes (filters the duplicates)     
    def collectQrOfSlidesFromPlayer(self, entryName, embed=False, fromActionBar=True):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False
                
            # The QR codes of the slides needs to be presented on the bottom right of the player  - in order to capture them. then the following function will switch the player view to that position
            if self.changePlayerView(enums.PlayerView.SWITCHVIEW) == False:
                return False
            
            if self.clickPlay(embed, fromActionBar, 10) == False:
                return False       
            
            qrPath = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            QRPathList = []
            
            while qrPath != False:
                qrPath = self.clsCommon.qrcode.takeQrCodeScreenshot(False)
                if qrPath == False:
                    break
                    
                QRPathList.append(qrPath)
                qrPath = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 3)
            
            
            for qrPath in QRPathList:
                # Crop the image
                img = Image.open(qrPath)
                img2 = img.crop((img.width / 1.38, img.height / 1.56, img.width / 1.02, img.height / 1.08))
                img2.save(qrPath)           
            
            QRcodeList = []
            for qrPath in QRPathList:
                qrResolve = self.clsCommon.qrcode.resolveQrCode(qrPath)
                if qrResolve == False:
                    writeToLog("INFO","FAILED to resolve QR code")
                QRcodeList.append(qrResolve)
                
            self.clsCommon.base.switch_to_default_content()    
            return self.removeDuplicate(QRcodeList, enums.PlayerObjects.QR)
            
        except Exception as inst:
            return False
        
        
    # Author: Michal zomper
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


    # Author: Michal zomper
    def verifySlidesDisplayAtTheCorrctTime(self, mySlidesList):
        self.switchToPlayerIframe()
        
        for slide in mySlidesList:
            if self.verifySlideDisplayAtTheCorrctTime(slide, mySlidesList[slide][1:]) == False:
                writeToLog("INFO","FAILED to verify slide:" + slide + " at time: " + mySlidesList[slide][1:])
                return False
            
        writeToLog("INFO","SUCCESS, all slides are verified and appear at the correct time")
        return True
                
    
    # Author: Michal zomper & Oleg Sigalov
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
        
        try:
            tmp_chapter = (self.PLAYER_SLIDE_DECK_CHAPTER[0], self.PLAYER_SLIDE_DECK_CHAPTER[1].replace('CHAPTER_NAME', chapterName))
            self.get_element(tmp_chapter)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to find chapter '" + chapterName + "' in slides menu bar")
            return False
        
        self.scrollInSlidesMenuBar(2)
        sleep(2)
        
        if chapterIsclose == True:
            try: 
                el = details.find_element_by_xpath("..")
                # get tabindex from 'li' object, we will use it to locate the 'Expand/collapse chapter' button
                tabindexId = el.get_attribute("tabindex")
            except NoSuchElementException:
                writeToLog("INFO","FAILED to get child element of self.PLAYER_OPEN_CHAPTER_ICON")
                return False                
            tmpTabindexIdLocator = (self.PLAYER_OPEN_CHAPTER_ICON[0], self.PLAYER_OPEN_CHAPTER_ICON[1].replace('TABINDEXID', tabindexId))
            sleep(2)
            self.scrollInSlidesMenuBar(2)
            self.scrollInSlidesMenuBar(2)
            
            # open chapter in order to see all the slides
            if self.click(tmpTabindexIdLocator) == False:
                writeToLog("INFO","FAILED to open chapter in order to see all the slides in chapter")
                return False
     
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
    
    
    # Author: Michal zomper
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
        
    # Author: Michal zomper
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
      
    # Author: Michal zomper   
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
            ActionChains(self.driver).click(searchEl).send_keys(slide).perform()
            sleep(1)
            ActionChains(self.driver).click(searchEl).send_keys(Keys.SPACE).perform()
            sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            
            
            slide_time = (self.PLAYER_SILDE_START_TIME[0], self.PLAYER_SILDE_START_TIME[1].replace('SLIDE_TIME', slidesForSearchList[slide]))
            if self.wait_visible(slide_time) == False:
                writeToLog("INFO","FAILED to verify slide time ' " + str(slidesForSearchList[slide]) + "' in the slide menu bar")
                return False
            sleep(2)
            
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

    
    # @ Author: Inbar Willman
    def verifyCaptionText(self, captionText):
        tmp_caption = (self.PLAYER_CAPTIONS_SECTION[0], self.PLAYER_CAPTIONS_SECTION[1].replace('CAPTION_TEXT', captionText))
        if self.is_visible(tmp_caption) == False:
            writeToLog("INFO","FAILED to display correct text")
            return False  
        return True