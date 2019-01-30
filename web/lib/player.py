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
    PLAYER_ALERT_MESSAGE                                        = ('xpath', "//div[@class='alert-message alert-text' and text()='ALERT_MESSAGE']")
    PLAYER_CONTROLER_BAR                                        = ('xpath', "//div[@class='controlsContainer']")
    PLAYER_QUIZ_WELCOME_SCREEN_WELCOME_MESSAGE                  = ('xpath', "//div[@class='welcomeMessage']")
    PLAYER_QUIZ_WELCOME_SCREEN_INSTRUCTIONS                     = ('xpath', "//div[@class='InvideoTipMessage']")
    PLAYER_QUIZ_WELCOME_SCREEN_DOWNLOAD_TEXT                    = ('xpath', "//div[@class='pdf-download-txt']")
    PLAYER_QUIZ_WELCOME_SCREEN_PDF_DOWNLOAD_BUTTON              = ('xpath', "//div[@class='pdf-download-img' and @role='button' and @aria-label='Pre-Test - Download PDF']")
    PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT                     = ('xpath', "//p[contains(@id,'answer') and text()='ANSWER_TEXT']")
    PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_TEXT                   = ('xpath', "//div[contains(@class,'display-question') and text()='QUESTION_NAME']")
    PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT                = ('xpath', "//div[contains(@class,'display-question')]")
    PLAYER_QUIZ_QUESTION_SCREEN_NEXT_ARROW                      = ('xpath', "//a[contains(@class,'cp-navigation-btn next-cp')]") 
    PLAYER_QUIZ_QUESTION_SCREEN_NEXT_ARROW_DISABLED             = ('xpath', "//a[contains(@class,'cp-navigation-btn next-cp disabled')]")   
    PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW                  = ('xpath', "//a[contains(@class,'cp-navigation-btn prev')]")   
    PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW_DISABLED         = ('xpath', "//a[contains(@class,'cp-navigation-btn prev-cp disabled')]")   
    PLAYER_QUIZ_QUESTION_SCREEN_SELECT_BUTTON                   = ('xpath', "//div[@class='single-answer-box-apply qContinue' and @role='button' and text()='Select']")
    PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON                 = ('xpath', "//div[@aria-disabled='true' and @role='button' and text()='Selected']")
    PLAYER_QUIZ_QUESTION_SCREEN_CONTINUE_BUTTON                 = ('xpath', "//div[@class='ftr-right' and text()='CONTINUE']")  
    PLAYER_QUIZ_SCRUBBER_SLIDER                                 = ('xpath', "//div[@role='slider' and @data-plugin-name='scrubber']")
    PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE                        = ('xpath', "//div[contains(@class,'bubble-window')]")
    PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER                 = ('xpath', "//div[@id='NUMBER' and contains(@class,'bubble-window')]")
    PLAYER_QUIZ_SCRUBBER_DONE_BUBBLE                            = ('xpath', "//div[@id='quiz-done-continue-button']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_SUB_TEXT                       = ('xpath', "//div[@class='sub-text']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT                     = ('xpath', "//div[contains(@class,'title-text') and text()='TITLE_NAME']") 
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE       = ('xpath', "//li[@class='q-box' and @title='click to view the question and your answer']")     
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE_ID    = ('xpath', "//li[@class='q-box' and @id='NUMBER']")
    PLAYER_QUIZ_COMPLETED_SCREEN_SUBMIT_BUTTON                  = ('xpath', "//div[@title='Submit your answers']")
    PLAYER_QUIZ_COMPLETED_SCREEN_REVIEW_BUTTON                  = ('xpath', "//div[@title='review your answers']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_TITLE_DEFAULT             = ('xpath', "//div[@class='theQuestion']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_TITLE_NAME                = ('xpath', "//div[@class='theQuestion' and text()='ANSWER_TITLE']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_CORRECT_ANSWER            = ('xpath', "//div[@class='correctAnswer' and text()='ANSWER_NAME']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_USER_ANSWER               = ('xpath', "//div[@class='yourAnswer' and text()='ANSWER_NAME']")  
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_QUESTION_NUMBER           = ('xpath', "//div[@class='reviewAnswerNr' and text()='NUMBER']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_HIGLIGHTED_ANSWER         = ('xpath', "//div[@class='single-answer-box-bk wide single-answer-box-bk-apply disable' and @role='button']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_GO_BACK_BUTTON            = ('xpath', "//div[@class='gotItBox' and text()='Got It !']")
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
            
            if self.clickPlay(embed, fromActionBar, 60) == False:
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
            
            if self.clickPlay(False, True, 60) == False:
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
            if self.clickPlay(sleepBeforePlay=60) == False:
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
            
            if self.clickPlay(embed, fromActionBar, 60) == False:
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
                img2 = img.crop((img.width / 2.04, img.height / 1.77, img.width / 1.71, img.height / 1.34))
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
    
    
    # @Author: Horia Cus
    # This function verifies if a specific KEA element from any KEA option is present or not in the player screen
    # Supports only KEA Details section for now
    # location must be enum  (e.g enums.Location.ENTRY_PAGE)
    # if isPresent = True, the kea element must contain the text for the specific option
    # if isPresent = true, the keaElement must be empty = ''
    def verifyQuizElementsInPlayer(self, keaSection, keaOption, keaElement, location, timeOut=45, isPresent=True):
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        if self.verifyAndClickOnPlay(location, timeOut) != True:
            return False
                
        if keaSection == enums.KEAQuizSection.DETAILS:
            if keaOption == enums.KEAQuizOptions.SHOW_WELCOME_PAGE:
                tmpLocator = self.PLAYER_QUIZ_WELCOME_SCREEN_WELCOME_MESSAGE
                
            elif keaOption == enums.KEAQuizOptions.INSTRUCTIONS:
                tmpLocator = self.PLAYER_QUIZ_WELCOME_SCREEN_INSTRUCTIONS
    
            elif keaOption == enums.KEAQuizOptions.ALLOW_DOWNLOAD:
                tmpLocator = self.PLAYER_QUIZ_WELCOME_SCREEN_DOWNLOAD_TEXT
            else:
                writeToLog("INFO", "Make sure that you have used a supported KEA Option")
                return False
            
        elif keaSection == enums.KEAQuizSection.SCORES:            
            if keaOption == enums.KEAQuizOptions.DO_NOT_SHOW_SCORES or enums.KEAQuizOptions.SHOW_SCORES:
                tmpLocator = self.PLAYER_QUIZ_SUBMITTED_SCREEN_SUB_TEXT
            
        else:
            writeToLog("INFO", "Make sure that you use a supported KEA Section")
            return False
                
        if isPresent == True:
            wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)
            self.setImplicitlyWait(0)
            while True:
                try:
                    el = self.get_element(tmpLocator)
                    if el.text == keaElement:
                        self.setImplicitlyWaitToDefault()
                        writeToLog("INFO", "The " + keaElement + " has been found in KEA page")
                        self.switch_to_default_content()
                        return True
                    else:
                        writeToLog("INFO", "The KEA element doesn't match with " + keaElement + " entry")
                        return False
                except:
                    if wait_until < datetime.datetime.now():
                        self.setImplicitlyWaitToDefault()
                        writeToLog("INFO", "FAILED to find the " + keaElement + " within the " + str(timeOut) + " seconds")
                        return False
                    pass  
                
        elif isPresent == False:
            if self.wait_element(tmpLocator, 30, True) == False:
                self.switch_to_default_content()
                writeToLog("INFO", "The " + keaOption.value + " has not been found")
                return True
            
            else:    
                el = self.wait_element(tmpLocator, 10, True)  
                if el.text == '':
                    writeToLog("INFO", "The " + keaOption.value + " is disabled")
                    self.switch_to_default_content()
                    return True
                else:
                    writeToLog("INFO", "The " + keaOption.value + " is present")
                    return False
                
        self.switch_to_default_content()       
        return True 

    
    # @Author: Horia Cus
    # This function selects a specific KEA Iframe, triggers the playing process and selects an answer for each desired Quiz
    # if submitQuiz=True, all the Quiz questions must be answered, otherwise it will return False
    # questionDict must contain the following format: {questionName1:answerText1}
    # questionDict must have questionName:answerText
    # skipWelcomeScreen = True it will wait and click on the continue button
    # This function works only when the "ALLOW SKIP" option is enabled
    def selectQuizAnswer(self, questionDict, location=enums.Location.ENTRY_PAGE, timeOut=2, submitQuiz=True, skipWelcomeScreen=True):     
        if self.initiateQuizPlayback(location, timeOut, skipWelcomeScreen) == False:
            return False
        
        # taking the available question numbers                
        questionNumber     = self.get_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE)
        availableQuestions = len(questionNumber)
        givenQuestions     = len(questionDict)
        questionsFound     = 0
        
        if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 10, True) == False:
            writeToLog("INFO", "FAILED to pause the video")
            return False
        sleep(1)
        
        #availableQuestions will determine for how many times we will use the for loop
        for x in range(0,availableQuestions):
            #we use tmpQuizPage in order to navigate to the next Quiz Question page, by incrementing with +1 (using x value) from each run
            tmpQuizPage = (self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[0], self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[1].replace('NUMBER', str(x))) 
            if self.click(tmpQuizPage, 30, True) == False:
                writeToLog("INFO", "FAILED to move to the " + str(x+1) + " quiz page")
                return False        
            
            sleep(4)
            #we collect the active question in order to verify if it matches with one from our dictionary  
            activeQuestion = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 120, True).text
                        
            if activeQuestion in questionDict:
                #after the active question matches with one from our dictionary, we take the answer assigned for that question
                activeAnswer = questionDict[activeQuestion]
                tmpAnswerName = (self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[0], self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[1].replace('ANSWER_TEXT', activeAnswer))
                
                if self.wait_element(tmpAnswerName, 5, True) == False:
                    writeToLog("INFO", "The " + activeAnswer + " has not been found in the " + activeQuestion + " question page")
                    return False
                     
                if self.click(tmpAnswerName, 10, True) == False:
                    writeToLog("INFO", "FAILED to select the " + activeAnswer + " answer")
                    return False
                 
                if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECT_BUTTON, 5, True) == False and self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 1, True) == False:
                    writeToLog("INFO", "FAILED to confirm the " + activeAnswer + " answer" )
                    return False
                 
                if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 1, True) == False:
                    writeToLog("INFO", "The " + activeAnswer + " is not displayed as being selected")
                    return  False   
                
                #after each Quiz Question answered, we increment it by one, so at the end we will know if all the Quiz Question from our dictionary were answered or not        
                questionsFound += 1
                self.wait_while_not_visible(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 10)
                
            else:
                #if the active Quiz Question answer is not present in our dictionary, we will skip it
                if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 30, True) == False:
                    writeToLog("INFO", "FAILED to skip the " + activeQuestion + " which was not found in the dictionary")
                    return False

                self.wait_while_not_visible(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 10)
            sleep(1)
        
        # verify that all the Quiz Question from our dictionary were found  
        if questionsFound != givenQuestions:
            writeToLog("INFO", "FAILED to find all the questions from the dictionary")
            return False
        
        sleep(1)
        if submitQuiz == True:
            if availableQuestions != questionsFound:
                writeToLog("INFO", "Some answers were not selected " + str(questionsFound) + " out of " + str(availableQuestions) + " questions")
                return False
            
            if self.submitTheAnswers(location) != True:
                return False
             
        return True
    
    
    # @Author: Horia Cus
    # This function switches the KEA Player iframe based on the location
    # location must be enum ( e.g location=enums.Location.ENTRY_PAGE)
    def selectPlayerIframe(self, location):     
        if location == enums.Location.ENTRY_PAGE:
            self.switchToPlayerIframe()
         
        elif location == enums.Location.KEA_PAGE:
            self.clsCommon.kea.switchToKEAPreviewPlayer()
            
        return True
    
    
    # @Author: Horia Cus
    # This function navigates to the end screen and then submits the answers
    # In order to submit the answers, all the Quiz questions must be answered, you can use selectQuizAnswer function for that
    # location must be enum ( e.g location=enums.Location.ENTRY_PAGE)
    def submitTheAnswers(self, location):
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch to the " + location.value + " iframe")
            return False
        
        #we verify that the user is in the "Submitted Screen"
        completedTitle = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[1].replace('TITLE_NAME', 'Completed'))
        if self.wait_element(completedTitle, 2, True) == False:
            if self.wait_element(self.PLAYER_QUIZ_SCRUBBER_DONE_BUBBLE, 5, True) == False:
                writeToLog("INFO", "FAILED to find the scrubber end screen button")
                return False

            if self.click(self.PLAYER_QUIZ_SCRUBBER_DONE_BUBBLE, 5, True) == False:
                writeToLog("INFO", "FAILED to click on the scrubber end screen button")
                return False
            
        if self.wait_element(completedTitle, 10, True) == True:
            writeToLog("INFO", "FAILED to load the completed screen")
            return False
            
        if self.click(self.PLAYER_QUIZ_COMPLETED_SCREEN_SUBMIT_BUTTON, 30, True) == False:
            writeToLog("INFO", "FAILED to submit the answers")
            return False
        
        if self.wait_while_not_visible(self.PLAYER_QUIZ_COMPLETED_SCREEN_REVIEW_BUTTON, 30) == False:
            writeToLog("INFO", "FAILED to progress to the next screen")
        
        #we verify that the user progressed to the "Submitted Screen"   
        submittedTitle = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[1].replace('TITLE_NAME', 'Submitted'))
        if self.wait_element(submittedTitle, 10, True) == False:
            writeToLog("INFO", "FAILED to find the submitted screen")
            return False
        sleep(1)
            
        return True
    
    
    # @Author: Horia Cus
    # This function verifies if the play button is present and then trigger the playing process
    # location must be enum ( e.g location=enums.Location.ENTRY_PAGE)
    def verifyAndClickOnPlay(self, location=enums.Location.ENTRY_PAGE, timeOut=3):
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch to the " + location.value + " iframe")
            return False
        
        # we verify if the play button is present, if so, we will click on it and trigger the playing process
        if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, timeOut, True) != False:
            if self.click(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 2, True) == False:
                writeToLog("INFO", "FAILED to activate the preview screen")
                return False
            
        return True
    

    # @Author: Horia Cus
    # This function verifies that the included answers matches with the ones from the answersDict
    # answerDict must use the following format: questionName1:{'correct':answerText1, 'given':userAnswer1}
    # location must be enum ( e.g location=enums.Location.ENTRY_PAGE)
    def verifyIncludedAnswers(self, answersDict, location=enums.Location.ENTRY_PAGE):
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch to the " + location.value + " iframe")
            return False
        
        submittedTitle = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[1].replace('TITLE_NAME', 'Submitted'))
        if self.wait_element(submittedTitle, 10, True) == False:
            writeToLog("INFO", "FAILED, you're not in the Submitted page")
            return False
        
        # taking the numbers of included answers
        includedAnswers    = self.get_elements(self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE)
        availableAnswers   = len(includedAnswers)
        givenAnswers       = len(answersDict)
        answersFound       = 0
        reviewAnswerNumber = 1
        
        #availableAnswers will determine for how many times we will use the for loop
        for x in range(0,availableAnswers):
            #we use tmpAnswerPage in order to navigate to each "Submitted Screen Include Answer", and incrementing it with +1 (using the 'x' value) from each run
            tmpAnswerPage = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE_ID[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE_ID[1].replace('NUMBER', str(x)))
            if self.click(tmpAnswerPage, 10, True) == False:
                writeToLog("INFO", "FAILED to click on the answer page number " + str(x+1))
                return False  
            
            sleep(2)  
            
            #we verify that after we clicked on the answer page, the right page number has been displayed
            tmpActiveAnswer = (self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_QUESTION_NUMBER[0], self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_QUESTION_NUMBER[1].replace('NUMBER', str(reviewAnswerNumber)))    
            if self.wait_element(tmpActiveAnswer, 10, True) == False:
                writeToLog("INFO", "The answer page number " + str(reviewAnswerNumber) + " has an invalid number")
                return False
            
            #we verify if the Active Question is present in our dictionary
            activeQuestion = self.wait_element(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_TITLE_DEFAULT, 60, True).text
            if activeQuestion in answersDict:
                #we take the Correct and Given answer from the active question from our dictionary
                correctAnswer = answersDict[activeQuestion]['correct']
                userAnswer    = answersDict[activeQuestion]['given']
                tmpCorrectAnswerName = (self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_CORRECT_ANSWER[0], self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_CORRECT_ANSWER[1].replace('ANSWER_NAME', correctAnswer))
                tmpUserAnswerName    = (self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_USER_ANSWER[0], self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_USER_ANSWER[1].replace('ANSWER_NAME', userAnswer))
                
                if self.wait_element(tmpCorrectAnswerName, 10, True) == False:
                    writeToLog("INFO", "FAILED to find the Valid " + correctAnswer + " answer in " + activeQuestion + " question")
                    return False
                
                if self.wait_element(tmpUserAnswerName, 10, True) == False:
                    writeToLog("INFO", "FAILED to find the User " + userAnswer + " answer in " + activeQuestion + " question")
                    return False
                
                if self.click(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_GO_BACK_BUTTON, 5, True) == False:
                    writeToLog("INFO", "FAILED to click on the go back button")
                    return False
                
                if self.wait_element(submittedTitle, 30, True) == False:
                    writeToLog("INFO", "FAILED to properly return to the submitted page")
                    return False
                
                #after each Include Answer page opened, we increment it by one, so at the end we will know if all the 'Included Answers' from our dictionary were found or not       
                answersFound += 1
            
            reviewAnswerNumber += 1
        
        #we verify that all the elements from our answerDict were found within the number of tries
        if answersFound != givenAnswers:
            writeToLog("INFO", "Some questions were not found: " + str(answersFound) + " out of " + str(givenAnswers) + " questions")
            return False                        

        return True  
    
    
    # @Author: Horia Cus
    # This function downloads the PDF file from  Allow Download of Questions List option
    # filePath must contain the following format: os.path.join(localSettings.LOCAL_SETTINGS_TEMP_DOWNLOADS, name + ".extension")
    def downloadQuizPDF(self, filePath):        
        self.switchToPlayerIframe()
        
        sleep(3) 
        #we verify if the playing button is present, if so, we will click on it so we can trigger the Quiz Welcome screen
        if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 30, True) != False:
            if self.click(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 2, True) == False:
                writeToLog("INFO", "FAILED to activate the welcome screen")
                return False
        
        #we click on the "PDF Download" button in order to trigger the download process
        if self.click(self.clsCommon.player.PLAYER_QUIZ_WELCOME_SCREEN_PDF_DOWNLOAD_BUTTON, 10, True) == False:
            writeToLog("INFO", "Failed to click on the download button")
            return False
        
        #we wait for three seconds, in order to make sure that our file has been downloaded successfully
        sleep(3)
        self.switch_to_default_content()
        
        #we verify that the downloaded file is present in the filePath location
        if self.clsCommon.verifyFilePathLocationIsValid(filePath) == False:
            return False
        
        #we verify that the downloaded file is not empty
        if self.clsCommon.verifyMinimumSizeOfAFile(filePath) == False:
            return False
        
        return True
    

    # @Author: Horia Cus
    # This function navigates to the first quiz page while being in player or in an active quiz page
    # It returns the available question numbers
    # This function will work only if the "ALLOW SKIP" option is enabled
    def navigateToFirstQuestion(self, location=enums.Location.ENTRY_PAGE):     
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        # if the user is in the player, it will navigate directly to the first question screen by clicking on the question bubble
        if self.wait_element(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE, 3, True) != False:
            firstQuestion = (self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[0], self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[1].replace('NUMBER', str(0))) 
            if self.click(firstQuestion) == False:
                writeToLog("INFO", "FAILED to select the first Quiz Screen page while using player screen")
                return False
            questions     = self.get_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE)
            questionsNumber = len(questions)
            
        #in case that the user is in "Question Screen" (meaning- the question bubbles are not presented): we will navigate to the first question using the previous arrow
        else:
            #we verify if only one single Quiz Question is present
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW_DISABLED, 2, True) != False and self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_NEXT_ARROW_DISABLED, 2, True) != False:
                writeToLog("INFO", "You're already in the only single Quiz Page available")
                questionsNumber = 1
                return questionsNumber
            
            #we use the previous arrow button until we reach the first Quiz Question page                                    
            while self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW_DISABLED, 3, True) == False:
                if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW, 10, True) == False:
                    writeToLog("INFO", "FAILED to navigate to a previous Quiz Page while using navigation buttons")
                    return False
                questions       = self.get_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE)
                questionsNumber = len(questions)
                sleep(1)
                if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW, 15, True) == False:
                    writeToLog("INFO", "FAILED to load to a previous Quiz Page while using navigation buttons")
                    return False
        
        #we return the questionsNumber, in order to know how many questions are available and use it in other functions
        return questionsNumber 
                

    # @Author: Horia Cus
    # This function navigates to the first quiz page while being in player or in an active quiz page
    def clickAndSeekOnSlider(self, precentage=5, location=enums.Location.ENTRY_PAGE, noSeekingForwardEnabled=False):     
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        #we verify that the scurbber slider is present, so we can proceed further
        if self.wait_element(self.PLAYER_QUIZ_SCRUBBER_SLIDER, 10, True) == False:
            writeToLog("INFO", "FAILED to find the slider element")
            return False
            
        action = ActionChains(self.driver)
        try:
            slider = self.wait_element(self.PLAYER_QUIZ_SCRUBBER_SLIDER)
            #we move the slider forward or backwards, using a precentage
            action.move_to_element(slider).move_by_offset(slider.size['width']/precentage, 0).pause(1).click().perform()
        except Exception:
            writeToLog("INFO", "FAILED to click and seek on slider")
            return False
        
        sleep(1)
        alertScreen = (self.PLAYER_ALERT_MESSAGE[0], self.PLAYER_ALERT_MESSAGE[1].replace('ALERT_MESSAGE', 'You are not allowed to seek forward'))
        
        #we verify if the noSeekingForward option is enabled or not
        if noSeekingForwardEnabled == True:
            if self.wait_element(alertScreen, 3, True) != False:
                writeToLog("INFO", "'No seeking forward' option is enabled")
                return True
            else:
                writeToLog("INFO", "FAILED, the 'No seeking forward' option is disabled")
                return False

        elif noSeekingForwardEnabled == False:
            if self.wait_element(alertScreen, 3, True) == False:
                writeToLog("INFO", "'No seeking forward' option is disabled")
                return True
            else:
                writeToLog("INFO", "FAILED, the 'No seeking forward' option is enabled")
                return False
        
        return True
        

    # @Author: Horia Cus
    # This function selects a specific KEA Iframe, navigates to the first quiz page and then replaces the already answered questions with new ones
    # if submitQuiz=True, all the Quiz questions must be answered, otherwise it will return False
    # questionDict must contain the following format: {questionName1:answerText1}
    # questionDict must have questionName:answerText
    # skipWelcomeScreen = True it will wait and click on the continue button
    # This function works only when the "ALLOW SKIP" option is enabled
    # In order to select the first row of answers, please use: selectQuizAnswer function
    # If questionNumbers = 0, it will navigate to the first quiz page and return the quiz numbers
    # If you don't want to navigate to the first question screen, please make sure that the questionNumbers = with the entry questions presented
    # This function supports for now only multiple options question
    def changeQuizAnswer(self, questionDict, location=enums.Location.ENTRY_PAGE, questionNumbers=0, submitQuiz=False):   
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        if questionNumbers == 0:
            questionNumbers = self.navigateToFirstQuestion(location)
            if questionNumbers == False:
                writeToLog("INFO", "FAILED to take the number of all the available questions")
                return  False
                    
        # taking the available questions numbers and answers               
        availableQuestions = questionNumbers
        givenAnswers       = len(questionDict)
        answersReplaced    = 0         
    
        #questionNumbers will determine for how many times we will use the for loop
        for x in range(0, questionNumbers): 
            sleep(2)
            activeQuestion        = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 10, True).text
            activeSelectedAnswer  = self.wait_element(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_HIGLIGHTED_ANSWER, 10, True).text
            
            #we verify if the Active Question is present in our dictionary       
            if activeQuestion in questionDict:
                newAnswer = questionDict[activeQuestion]
                tmpAnswerName = (self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[0], self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[1].replace('ANSWER_TEXT', newAnswer))
                
                #we verify if the already selected answer matches with the one that should have been used, in order to replace it
                if activeSelectedAnswer.count(newAnswer) == 1:
                    writeToLog("INFO", "The " + newAnswer + " is already selected")
                    if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_CONTINUE_BUTTON) == False:
                        writeToLog("INFO", "FAILED to click on the CONTINUE button, while an answer has been already selected")
                        return False
                
                # if the active selected answer doesn't matches with the new one, we will replace it, with the new one                  
                else:
                    if self.wait_element(tmpAnswerName, 5, True) == False:
                        writeToLog("INFO", "The " + newAnswer + " has not been found in the " + activeQuestion + " question page")
                        return False
                         
                    if self.click(tmpAnswerName, 10, True) == False:
                        writeToLog("INFO", "FAILED to click on the " + newAnswer + " answer")
                        return False
                     
                    if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECT_BUTTON, 5, True) == False and self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 1, True) == False:
                        writeToLog("INFO", "FAILED to confirm the " + newAnswer + " answer" )
                        return False
    
                    if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 2, True) == False:
                        writeToLog("INFO", "The " + newAnswer + " is not displayed as being selected")
                        return  False  
               
                #after each Answer Replaced, we increment it by one, so at the end we will know if all the 'New Answers' from our dictionary were found and replaced or not                               
                answersReplaced += 1
                self.wait_while_not_visible(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 10)
                
                
            else:
                if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_NEXT_ARROW, 30, True) == False:
                    writeToLog("INFO", "FAILED to navigate from the " + activeQuestion + " to the next one")
                    return False

                self.wait_while_not_visible(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 10)
            sleep(1)
            #after we replaced the answer or skipped the Quiz Question, we will navigate to the next one
            if x != questionNumbers - 1:
                tmpQuizPage = (self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[0], self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[1].replace('NUMBER', str(x+1))) 
                
                if self.click(tmpQuizPage, 30, True) == False:
                    writeToLog("INFO", "FAILED to move to the " + str(x+1) + " quiz page")
                    return False  
                        
        #we verify that all the "New Answers" from our dictionary were found within the number of tries
        if answersReplaced != givenAnswers:
            writeToLog("INFO", "FAILED to replace all the questions with the new answers")
            return False
        
        sleep(1)
        if submitQuiz == True:
            if availableQuestions != answersReplaced:
                writeToLog("INFO", "Some answers were not replaced: " + str(answersReplaced) + " out of " + str(availableQuestions) + " questions")
                return False
            
            if self.submitTheAnswers(location) != True:
                return False
            
        return True
    

    # @Author: Horia Cus
    # This function verifies if the user is within the playing screen or quiz welcome screen, if not it will automatically refresh the page
    # If forceResume=True, the function will automatically refresh the page, despite of the content displayed
    def resumeFromBeginningQuiz(self,location=enums.Location.ENTRY_PAGE, timeOut=2, forceResume=False):     
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        sleep(timeOut)
        #we verify if any of the elements that indicates if the user is at the beginning of entry is present or not
        if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 90, True) == False and self.wait_element(self.PLAYER_QUIZ_CONTINUE_BUTTON, 90, True) == False or forceResume == True:  
            self.driver.refresh()
            
            if self.selectPlayerIframe(location) != True:
                writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
                return False
                
            sleep(5)
            if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 10, True) == False:
                writeToLog("INFO", "FAILED to load the page after refreshing it")
                return False 
        
        return True
    

    # @Author: Horia Cus
    # This function verifies if the Welcome Screen is enabled and then clicks on the "CONTINUE" button
    def continueFromQuizWelcomeScreen(self):
        #we verify if the "Continue" button specific for the Quiz "Welcome Screen" is present or not     
        if self.wait_element(self.PLAYER_QUIZ_CONTINUE_BUTTON, 10, True) != False:
            writeToLog("INFO", "Continue button has been found in welcome screen")
        else:
            writeToLog("INFO", "FAILED to find the continue button from the welcome screen")
            return False
        
        #we click on the "continue" button and then wait one second in order to give time for the playing process to start
        if self.click(self.PLAYER_QUIZ_CONTINUE_BUTTON, 10, True) == False:
            writeToLog("INFO", "FAILED to continue further from the welcome screen")
            return False
        sleep(1)
        
        return True
   

    # @Author: Horia Cus
    # This function selects a specific player iframe, triggers the playing process and skips all the Quiz Questions
    # skipWelcomeScreen = True it will wait and click on the continue button
    # This function works only when the "ALLOW SKIP" option is enabled
    # if allowSkip is Enabled, the following method will check 2 things:
        #the user is able to skip all the questions by clicking on the "skip for now" per each of the questions
        #the user is able to navigate between the questions by clicking on the questions's bubble
    def skipQuizAnswers(self, location=enums.Location.ENTRY_PAGE, timeOut=2, skipWelcomeScreen=True):     
        if self.initiateQuizPlayback(location, timeOut, skipWelcomeScreen) == False:
            return False
        
        # taking the available questions number 
        availableQuestions = len(self.get_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE))
        if availableQuestions <= 0:
            writeToLog("INFO", "FAILED to find any Question bubbles")
            return False      
        
        #we create a list, so at the end of the function we will now each Quiz Question that was skipped
        quizQuestions = []
        
        #we click on the pause option so we make sure that we won't skip any Question Bubble
        #if the pause button is clicked and then the user clicks on the Quiz Question bubble, if the "ALLOW SKIP" option is not enabled, the user will remain in a pause state
        if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 10, True) == False:
            writeToLog("INFO", "FAILED to pause the video")
            return False
        sleep(1)
        
        #we run the for loop based on the availableQuestion        
        for x in range(0,availableQuestions):
            #we navigate to the "Quiz Question" screen using question bubbles, and incrementing it by 'x' after each run
            tmpQuizPage = (self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[0], self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[1].replace('NUMBER', str(x))) 
            if self.click(tmpQuizPage, 30, True) == False:
                writeToLog("INFO", "FAILED to move to the " + str(x+1) + " quiz page")
                return False    

            #we verify that the question screen is properly displayed, with an active question
            sleep(2)
            try:  
                activeQuestion = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 30, True).text
            except Exception:
                writeToLog("INFO","FAILED to find the Quiz Question element")
                return False
            
            #we click on the 'skip for now button'
            if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 30, True) == False:
                writeToLog("INFO", "FAILED to skip the " + activeQuestion + " quiz question")
                return False
            
            #we insert the question found in the quizQuestion list
            quizQuestions.append(activeQuestion)
            #we wait for the "Quiz Question" screen to no longer be present, and proceed further
            self.wait_while_not_visible(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 10)
            
        quizes = ", ".join(quizQuestions)
        writeToLog("INFO","The following Quiz Questions were skipped: " + quizes + "")
        return True
    
    
    # @Author: Horia Cus
    # This function initiates the playing process from the beginning
    def initiateQuizPlayback(self, location=enums.Location.ENTRY_PAGE, timeOut=2, skipWelcomeScreen=True):     
        sleep(timeOut)
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        sleep(1)
        #we resume the entry from the beginning
        if self.resumeFromBeginningQuiz(location) == False:
            return False                  
        
        #we triggering the playing process
        if self.verifyAndClickOnPlay(location) != True:
            return False
        
        #we dismiss the "Quiz Welcome Screen" if its enabled 
        sleep(1)
        if skipWelcomeScreen == True:
            if self.continueFromQuizWelcomeScreen() == False:
                return False
            
        return True
    
    
    # @Author: Horia Cus
    # This function selects a specific player iframe, triggers the playing process and verify that the skip option is disabled
    # skipWelcomeScreen = True it will wait and click on the continue button
    # If you want to verify if the skip option is enabled, please use skipQuizAnswers function
    # This function works only when the "ALLOW SKIP" option is disabled, "DO NOT ALLOW SKIP" enabled
    # This function verifies two things:
        #that the user is unable to navigate to the "Quiz Question" screen using question bubbles
        #that the question screen is automatically triggered after the user reaches the question bubble, after resuming the playing process
    # the timeOut is the maximum amount of time given for the Question Screen to be displayed naturally
    def verifySkipOptionDisabled(self, location=enums.Location.ENTRY_PAGE, timeOut=15, skipWelcomeScreen=True):     
        if self.initiateQuizPlayback(location, 5, skipWelcomeScreen) == False:
            return False
        
        # taking the available questions number 
        availableQuestions = len(self.get_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE))
        if availableQuestions <= 0:
            writeToLog("INFO", "FAILED to find any Question within the entry")
            return False      
        
        # we click on the pause button in order to make sure that we won't skip any question and to verify that the user is unable to navigate to the question screen using question bubbles
        if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 10, True) == False:
            writeToLog("INFO", "FAILED to pause the video")
            return False
        
        #we try to navigate to the first question screen
        tmpQuizPage = (self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[0], self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[1].replace('NUMBER', str(0))) 
        if self.click(tmpQuizPage, 30, True) == False:
            writeToLog("INFO", "FAILED to find a Quiz Question bubble and click on it")
            return False
        
        #we verify that the question screen is not displayed after clicking on the question bubbles
        sleep(2)
        if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 3, True) != False:
            writeToLog("INFO", "FAILED, the navigate to the Quiz Question screen option is enabled")
            return False 
        
        #we resume the playing process 
        if self.click(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 2, True) == False:
            writeToLog("INFO", "FAILED to resume the playing process")
            return False
        
        #we wait for the question screen to be naturally opened within the timeOut period
        sleep(timeOut)
        if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 5, True) == False:
            writeToLog("INFO","FAILED to find the Quiz Question element")
            return False
        
        #we verify that the "skip for now" button is not present
        if self.wait_element(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 10, True) != False:
            writeToLog("INFO", "FAILED, the 'skip for now' button is displayed")
            return False
        
        return True 
    
    
    # @Author: Horia Cus
    # This function selects a specific KEA Iframe, navigates to the first quiz page and then verify that a new answer cannot be inserted
    # questionDict must contain the following format: {questionName1:answerText1}
    # questionDict must have questionName:answerText
    # This function works only when the "ALLOW SKIP" option is enabled
    # In order to select the first row of answers, please use: selectQuizAnswer function
    # If navigateToFirstQuestion = True, it will navigate to the first quiz page and return the quiz numbers
    # This function supports for now only multiple options question
    # If you want to verify if the "CHANGE QUIZ ANSWER" option is enabled, please use the changeQuizAnswer function
    # Now we support only "Multiple Question" quiz
    def verifyChangeQuizAnswerOptionDisabled(self, questionDict, location=enums.Location.ENTRY_PAGE, navigateToFirstQuestion=True):  
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        #we navigate to the first question, in order to have a question that has been answered already
        if navigateToFirstQuestion == True:
            if self.navigateToFirstQuestion(location) == False:
                writeToLog("INFO", "FAILED to navigate to the first quiz question")
                return  False
                
        #we verify that the question page that we are in, has an answer selected 
        sleep(2)    
        try:
            activeQuestion        = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 10, True).text
            activeSelectedAnswer  = self.wait_element(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_HIGLIGHTED_ANSWER, 10, True).text
        except Exception:
            writeToLog("INFO", "FAILED to find an active question and a selected answer")
            return False
        
        #we verify that the "active question' text from the active "Question Screen", matches with one from our dictionary
        if activeQuestion in questionDict:
            #we take the new answer, specific for the active question screen
            newAnswer = questionDict[activeQuestion]
            tmpAnswerName = (self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[0], self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[1].replace('ANSWER_TEXT', newAnswer))
            
            #we verify that the selected answer that we want to replace, it's not the same with the new one
            if activeSelectedAnswer.count(newAnswer) == 1:
                writeToLog("INFO", "The " + newAnswer + " is already selected, please make sure that you're using a new answer")
                return False  
            
            #we verify that the new answer is present in the question screen
            if self.wait_element(tmpAnswerName, 5, True) == False:
                writeToLog("INFO", "The " + newAnswer + " has not been found in the " + activeQuestion + " question page")
                return False
                 
            #we click on the new answer, in order to trigger the highlight state
            if self.click(tmpAnswerName, 10, True) == False:
                writeToLog("INFO", "FAILED to click on the " + newAnswer + " answer")
                return False
            
            #we verify that the new answer is not highlighted after clicking on it
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECT_BUTTON, 2, True) != False:
                writeToLog("INFO", "The select option is displayed for the " + newAnswer + " new answer")
                return False
        
        else:
            writeToLog("INFO", "FAILED to find a Quiz Question that matches with the questionDict")
            return False
        
        return True 