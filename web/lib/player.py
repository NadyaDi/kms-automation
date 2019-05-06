from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from base import *
import clsTestService
import enums
from PIL import Image
from selenium.common.exceptions import StaleElementReferenceException,\
    MoveTargetOutOfBoundsException



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
    PLAYER_SCREEN_LOADING_SPINNER                               = ('xpath', "//div[@id='loadingSpinner_kplayer']")
    PLAYER_CONTROLS_CONTAINER_REAL_TIME                         = ('xpath', "//div[contains(@class,'currentTimeLabel display-high')]") 
    PLAYER_QUIZ_ANSWER_NO_3                                     = ('xpath', "//p[@id='answer-2-text']")
    PLAYER_TIMMER_BUTTON_CONTROLS_CONTAINER                     = ('xpath', "//span[contains(@class,'playHead PIE btn')]")
    PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER                       = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-play')]")
    PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER                      = ('xpath', "//button[@class='btn comp playPauseBtn display-high icon-pause']")
    #PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER              = ('xpath', "//a[@class='icon-play  comp largePlayBtn  largePlayBtnBorder' and @aria-label='Play clip']")
    PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER              = ('xpath', "//a[contains(@class,'icon-play')]")
    PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER                      = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-pause')]")
    PLAYER_REPLAY_BUTTON_CONTROLS_CONTAINER                     = ('xpath', "//button[@data-plugin-name='playPauseBtn' and contains(@class,'icon-replay')]")
    PLAYER_GENERIC_PLAY_REPLAY_PASUSE_BUTTON_CONTROLS_CONTAINER = ('xpath', "//button[@data-plugin-name='playPauseBtn']")
    PLAYER_CURRENT_TIME_LABEL                                   = ('xpath', "//div[@data-plugin-name='currentTimeLabel']")
    PLAYER_SLIDE_SIDE_BAR_MENU                                  = ('xpath', "//div[@id='sideBarContainerReminderContainer' and @class='icon-chapterMenu']")
    PLAYER_SLIDE_IN_SIDE_MENU                                   = ('xpath', "//li[@class='mediaBox slideBox']")
    PLAYER_SLIDE_PRESENTED_IMAGE                                = ('xpath', "//img[@id='SynchImg']")
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
    PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON                             = ('xpath', "//div[@class='ftr-right' and text()='SKIP FOR NOW' or text()='CONTINUE']")
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
    PLAYER_QUIZ_ANSWER_CUSTOM                                   = ('xpath', "//p[@id='answer-'NUMBER'-text']")
    PLAYER_ALERT_MESSAGE                                        = ('xpath', "//div[@class='alert-message alert-text' and text()='ALERT_MESSAGE']")
    PLAYER_CONTROLER_BAR                                        = ('xpath', "//div[@class='controlsContainer']")
    PLAYER_QUIZ_WELCOME_SCREEN_WELCOME_MESSAGE                  = ('xpath', "//div[@class='welcomeMessage']")
    PLAYER_QUIZ_WELCOME_SCREEN_INSTRUCTIONS                     = ('xpath', "//div[@class='InvideoTipMessage']")
    PLAYER_QUIZ_WELCOME_SCREEN_DOWNLOAD_TEXT                    = ('xpath', "//div[@class='pdf-download-txt']")
    PLAYER_QUIZ_WELCOME_SCREEN_PDF_DOWNLOAD_BUTTON              = ('xpath', "//div[@class='pdf-download-img' and @role='button' and @aria-label='Pre-Test - Download PDF']")
    PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT                     = ('xpath', "//p[contains(@id,'answer') and text()='ANSWER_TEXT']")
    PLAYER_QUIZ_QUESTION_SCREEN_ANSWER                          = ('xpath', "//div[contains(@class,'single-answer-box-bk')]")
    PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_TEXT                   = ('xpath', "//div[contains(@class,'display-question') and text()='QUESTION_NAME']")
    PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT                = ('xpath', "//div[contains(@class,'display-question')]")
    PLAYER_QUIZ_QUESTION_SCREEN_NEXT_ARROW                      = ('xpath', "//a[contains(@class,'cp-navigation-btn next-cp')]") 
    PLAYER_QUIZ_QUESTION_SCREEN_NEXT_ARROW_DISABLED             = ('xpath', "//a[contains(@class,'cp-navigation-btn next-cp disabled')]")   
    PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW                  = ('xpath', "//a[contains(@class,'cp-navigation-btn prev')]")   
    PLAYER_QUIZ_QUESTION_SCREEN_PREVIOUS_ARROW_DISABLED         = ('xpath', "//a[contains(@class,'cp-navigation-btn prev-cp disabled')]")   
    PLAYER_QUIZ_QUESTION_SCREEN_SELECT_BUTTON                   = ('xpath', "//div[@class='single-answer-box-apply qContinue' and @role='button' and text()='Select']")
    PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON                 = ('xpath', "//div[@aria-disabled='true' and @role='button' and text()='Selected']")
    PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_ANSWER_CONTAINER       = ('xpath', "//div[@class='single-answer-box-bk wide single-answer-box-bk-apply disable']")
    PLAYER_QUIZ_QUESTION_SCREEN_CONTINUE_BUTTON                 = ('xpath', "//div[@class='ftr-right' and text()='CONTINUE']")
    PLAYER_QUIZ_QUESTION_SCREEN_MULTIPLE_CHOICE_CONTAINER       = ('xpath', "//div[@class='ivqContainer multiple-choice-answer-question']")
    PLAYER_QUIZ_QUESTION_SCREEN_REFLECTION_POINT_CONTAINER      = ('xpath', "//div[@class='ivqContainer reflection-point-question']")
    PLAYER_QUIZ_QUESTION_SCREEN_TRUE_FALSE_CONTAINER            = ('xpath', "//div[@class='ivqContainer true-false-question']")
    PLAYER_QUIZ_QUESTION_SCREEN_HINT_BUTTON                     = ('xpath', "//div[@class='hint-why-box' and text()='HINT']")
    PLAYER_QUIZ_QUESTION_SCREEN_HINT_CONTAINER                  = ('xpath', "//div[@class='hint-container']")
    PLAYER_QUIZ_QUESTION_SCREEN_HINT_TEXT                       = ('xpath', "//div[@class='hint-container' and text()='HINT_TEXT']")
    PLAYER_QUIZ_QUESTION_SCREEN_HINT_CLOSE_BUTTON               = ('xpath', "//div[@class='header-container close-button' and @role='button']")
    PLAYER_QUIZ_SCRUBBER_CURRENT_TIME_LABEL_SPECIFIC            = ('xpath', "//div[@data-plugin-name='currentTimeLabel' and text()='TIME']")
    PLAYER_QUIZ_SCRUBBER_SLIDER                                 = ('xpath', "//div[@role='slider' and @data-plugin-name='scrubber']")
    PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE                        = ('xpath', "//div[contains(@class,'bubble-window')]")
    PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_ANSWERED               = ('xpath', "//div[@class='bubble bubble-ans bubble-window']")
    PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_UN_ANSWERED            = ('xpath', "//div[@class='bubble bubble-un-ans bubble-window' or @class='bubble bubble-un-ans bubble-window-quizEndFlow']")
    PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER                 = ('xpath', "//div[@id='NUMBER' and contains(@class,'bubble-window')]")
    PLAYER_QUIZ_SCRUBBER_DONE_BUBBLE                            = ('xpath', "//div[@id='quiz-done-continue-button']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_SUB_TEXT                       = ('xpath', "//div[contains(@class,'sub-text')]")
    PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT                     = ('xpath', "//div[contains(@class,'title-text') and text()='TITLE_NAME']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_SCORE                          = ('xpath', "//span[@class='scoreBig']")  
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE       = ('xpath', "//li[@class='q-box' and @title='click to view the question and your answer']")     
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE_ID    = ('xpath', "//li[contains(@class,'q-box') and @id='NUMBER']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_FALSE_ID        = ('xpath', "//li[@class='q-box q-box-false' and @id='NUMBER']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_TRUE_ID         = ('xpath', "//li[@class='q-box' and @id='NUMBER']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_REFLECTION_ID          = ('xpath', "//li[@class='q-box reflection-point-question' and @id='NUMBER']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_DONE_BUTTON                    = ('xpath', "//div[@class='confirm-box' and text()='Done !']")
    PLAYER_QUIZ_SUBMITTED_SCREEN_NEXT_ARROW                     = ('xpath', "//div[contains(@class,'hex-column  right-arrow')]")
    PLAYER_QUIZ_SUBMITTED_SCREEN_PREVIOUS_ARROW                 = ('xpath', "//div[contains(@class,'hex-column  left-arrow')]")
    PLAYER_QUIZ_ALMOST_DONE_SCREEN_OK_GOTIT_BUTTON              = ('xpath', "//div[@class='confirm-box' and contains(text(),'Ok')]")
    PLAYER_QUIZ_COMPLETED_SCREEN_SUBMIT_BUTTON                  = ('xpath', "//div[@title='Submit your answers']")
    PLAYER_QUIZ_COMPLETED_SCREEN_REVIEW_BUTTON                  = ('xpath', "//div[@title='review your answers']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_TITLE_DEFAULT             = ('xpath', "//div[@class='theQuestion']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_TITLE_NAME                = ('xpath', "//div[@class='theQuestion' and text()='ANSWER_TITLE']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_CORRECT_ANSWER            = ('xpath', "//div[@class='correctAnswer' and text()='ANSWER_NAME']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_USER_ANSWER               = ('xpath', "//div[@class='yourAnswer' and text()='ANSWER_NAME']")  
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_QUESTION_NUMBER           = ('xpath', "//div[@class='reviewAnswerNr' and text()='NUMBER']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_HIGLIGHTED_ANSWER         = ('xpath', "//div[@class='single-answer-box-bk wide single-answer-box-bk-apply disable' and @role='button']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_GO_BACK_BUTTON            = ('xpath', "//div[@class='gotItBox' and text()='Got It !']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_WHY_BUTTON                = ('xpath', "//div[@class='hint-why-box' and text()='WHY']")
    PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_CLOSE_BUTTON              = ('xpath', "//div[@class='header-container close-button']")
    PLAYER_TOUCH_OVERLAY                                        = ('xpath', "//div[@id='touchOverlay']")
    PLAYER_HOTSPOT_PRESENTED                                    = ('xpath', "//div[contains(@style,'text-rendering: geometricprecision')]")
    PLAYER_QUIZ_QUESTION_SCREEN_OPEN_Q_POINT_CONTAINER          = ('xpath', "//div[@class='ivqContainer open-question']")
    PLAYER_QUIZ_QUESTION_SCREEN_OPEN_QUESTION_TEXT              = ('xpath', '//textarea[@class="open-question-textarea"]')
    PLAYER_QUIZ_QUESTION_OPEN_QUESTION_SAVE_BTN                 = ('xpath', '//button[@id="open-question-save"]')  
    PLAYER_QUIZ_WELCOME_SCREEN_TOTAL_ATTEMPTS                   = ('xpath', '//div[@class="retake-box" and text()="Total attempts available for this quiz: NUMBER_OF_ATTEMPTS"]')
    PLAYER_SUBMITTED_SCREEN_CURRENT_ATTEMPT_NUMBER              = ('xpath', '//span[@class="retake-summary-text" and text()="This is attempt CURRENT_ATTEMPTS of TOTAL_ATTEMPTS"]')
    PLAYER_SUBMITTED_SCREEN_TOTAL_SCORE                         = ('xpath', '//span[@class="retake-summary-score-text" and text()=", your score is TOTAL_SCORE based on SCORE_TYPE"]')
    PLAYER_SUBMITTES_SCREEN_TAKE_THE_QUIZ_AGAIN_BTN             = ('xpath', '//div[@title="Take the Quiz again"]')
    PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_OPEN_Q_ID              = ('xpath', "//li[@class='q-box open-question' and @id='NUMBER']")
    PLAYER_QUIZ_QUESTION_SCREEN_OPEN_Q_CONTAINER                = ('xpath', "//div[@class='ivqContainer open-question answered']")
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
                if self.wait_element(self.PLAYER_EMBED_IFRAME_1, 5) != False:
                    self.swith_to_iframe(self.PLAYER_EMBED_IFRAME_1, 1)

                #Switch to second iframe
                self.wait_element(self.PLAYER_EMBED_IFRAME_2, 5)
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
            try:
                playButtonControlsEl = self.wait_element(self.PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER)
                playBtnWidth = playButtonControlsEl.size['width'] / 3
                playBtnHeight = playButtonControlsEl.size['height'] / 1.1
            except Exception:
                writeToLog("INFO", "FAILED to take the elements in order to click play using the action bar")
                return False
                
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
    def collectCaptionsFromPlayer(self, entryName, embed=False, fromActionBar=True, quizEntry=False):
        try:
            if len(entryName) != 0:
                if self.clsCommon.entryPage.navigateToEntryPageFromMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to navigate to edit entry page")
                    return False 
                
                if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                    writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
                    return False
            
            if self.clickPlay(embed, fromActionBar, 10) == False:
                if self.clickPlay(embed, False, 5) == False:
                    writeToLog("INFO", "FAILED to click on the play button")
                    return False
                
            if quizEntry == True:
                self.switchToPlayerIframe()
                if self.continueFromQuizWelcomeScreen() == False:
                    writeToLog("INFO", "FAILED to continue from Quiz Welcome Screen")
                    return False       
            
            playback = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            captionsList = [];
            
            while playback != False:
                try:
                    captionText = self.wait_element(self.PLAYER_CAPTIONS_TEXT).text
                    
                    if quizEntry == True:
                        # Verify if the Question Screen is displayed
                        if self.wait_element(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 0.67, True) != False:
                            sleep(3)
                            # Resume the playing process by skipping the Question Screen
                            if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 1, True) == False:
                                writeToLog("INFO", "FAILED to click on the Skip for now button")
                                return False
                            
                            # Make sure that we capture only the Slide Images
                            if self.wait_visible(self.PLAYER_CAPTIONS_TEXT, 1.5, True) == False:
                                writeToLog("INFO", "FAILED to displayed the Captions after dismissing the Question Screen")
                                return False                
    
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
            
            #Move forward from the Quiz Welcome Screen
            if self.continueFromQuizWelcomeScreen() == False:
                writeToLog("INFO", "FAILED to continue from Quiz Welcome Screen")
                return False  

            replay = self.wait_element(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            questionList = {}
            key = 1
            
            while replay != False:      
                
                question = self.wait_element(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, timeout=30)
                if question != False:
                    sleep(1)
                    
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
            
        if application == enums.Application.SHARE_POINT:
            self.clsCommon.sendKeysToBodyElement(Keys.PAGE_UP)
            self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN, 2)
            
        self.switchToPlayerIframe()     
        qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
        if qrCodeSc == False:
            writeToLog("INFO","FAILED to take qr screen shot")
            return False
        
        result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
        if result == None:
            writeToLog("INFO","FAILED to resolve qr code")
            return False
        
        if ((int(result)+1 == expecterQrCode) or (expecterQrCode == int(result))) == False:
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
                        
                    if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
                        self.switch_to_default_content()
                        self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
                        self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN,5)
                        sleep(1)
                        self.clsCommon.player.switchToPlayerIframe()
                        
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
    # If quizEntry = True, it will Skip all the Quiz Related screens, NOTICE that the QR Code for the second where the Question was presented, may not be captured     
    def collectQrOfSlidesFromPlayer(self, entryName, embed=False, fromActionBar=True, quizEntry=False, resumeFromBeginning=False):
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
                if self.clickPlay(embed, False, 1) == False:
                    writeToLog("INFO", "FAILED to click on the play button")
                    return False  
                
            if quizEntry == True:
                self.switchToPlayerIframe()
                if self.continueFromQuizWelcomeScreen() == False:
                    writeToLog("INFO", "FAILED to continue from Quiz Welcome Screen")
                    return False
            
            # Due to the fact that the user may be moved by force to a Quiz Question screen, we can use resumeFromBeginning to make sure that we won't miss any captions
            if resumeFromBeginning == True:
                if quizEntry == True:
                    if self.wait_element(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 15, True) != False:
                        if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 1, True) == False:
                            writeToLog("INFO", "FAILED to click on the skip for now button in order to resume the entry from the beginning")
                            return False
                        
                    # We verify that the Almost Completed screen is presented
                    almostDoneScreen = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[1].replace('TITLE_NAME', 'Almost Done'))
                    if self.wait_element(almostDoneScreen, 5) != False:
                        if self.click(self.PLAYER_QUIZ_ALMOST_DONE_SCREEN_OK_GOTIT_BUTTON, 1, True) == False:
                            writeToLog("INFO", "FAILED to close the Almost Done screen")
                            return False
                        sleep(2.5)
                
                if self.setPlayerAtSecondZero(True) == False:
                    writeToLog("INFO", "FAILED to resume the entry at the second zero")
                    return False
            
            qrPath = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER)
            QRPathList = []
            
            while qrPath != False:
                qrPath = self.clsCommon.qrcode.takeQrCodeScreenshot(False)
                
                if quizEntry == True:
                    # Verify if the Question Screen is displayed
                    if self.wait_element(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 0.68, True) != False:
                        sleep(3)
                        # Resume the playing process by skipping the Question Screen
                        if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 1, True) == False:
                            writeToLog("INFO", "FAILED to click on the Skip for now button")
                            return False
                        
                        # Make sure that we capture only the Slide Images
                        if self.wait_visible(self.PLAYER_SLIDE_PRESENTED_IMAGE, 1.5, True) == False:
                            writeToLog("INFO", "FAILED to displayed the Slide Images after dismissing the Question Screen")
                            return False
                        
                if qrPath == False:
                    break
                    
                QRPathList.append(qrPath)
                qrPath = self.wait_visible(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 3)
            
            
            for qrPath in QRPathList:
                # Changed value after using player version 2.75
                # Crop the image
#                 img = Image.open(qrPath)
#                 img2 = img.crop((img.width / 2.04, img.height / 1.77, img.width / 1.71, img.height / 1.34))
#                 img2.save(qrPath)           

                img = Image.open(qrPath)
                img2 = img.crop((img.width / 2.04, img.height / 1.67, img.width / 1.71, img.height / 1.24))
                img2.save(qrPath)           
            
            QRcodeList = []
            for qrPath in QRPathList:
                qrResolve = self.clsCommon.qrcode.resolveQrCode(qrPath)
                if qrResolve == False:
                    writeToLog("INFO","FAILED to resolve QR code")
                QRcodeList.append(qrResolve)
                
            
            if quizEntry == True:
                # Remove invalid elements ( None )  from the QR Code List
                QRcodeList = [x for x in QRcodeList if x != None]
                                
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
            sleep(2)
            ActionChains(self.driver).click(searchEl).send_keys(Keys.SPACE).perform()
            sleep(5)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            sleep(3)
            
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
    # Reflection Point questions, should not be present in the list
    # This function works only when the "ALLOW SKIP" option is enabled
    # expectedNumberOfAttemptsWelcomeSreen = int: How many attempts user has, displayed in welcome screen
    # currentNumberOfAttemptsSubmittedScreen = int: The number of the current attempt, displayed in submitted screen
    # totalGivenAttempts = int: The total given number of attempts
    # expectedGeneralQuizScore = String: Represent the score of all attempts based on the score type
    # scoreType = enum.playerQuizScoreType: Represent the score type (Latest, Highest, Average, Lowest, First)
    def answerQuiz(self, questionDict, skipWelcomeScreen, submitQuiz, location, timeOut, expectedQuizScore='', embed=False, verifySubmittedScreenDict='', expectedQuestionsStateDict='',expectedNumberOfAttemptsWelcomeSreen='', currentNumberOfAttemptsSubmittedScreen='', totalGivenAttempts='', expectedGeneralQuizScore='', scoreType='', showScore=True):     
        if self.initiateQuizPlayback(location, timeOut, skipWelcomeScreen, embed, expectedNumberOfAttemptsWelcomeSreen) == False:
            return False
         
        # taking the available question numbers                
        questionNumber     = self.get_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE)
        availableQuestions = len(questionNumber)
        
        # the number of questions that needs to be found and answered within the quiz entry
        givenQuestions     = len(questionDict)
        # the number of questions that were found within the entry that matches with the given questions
        questionsFound     = 0
         
        # We pause the video, in order to make sure that we won't miss any elements from the scrubber
        if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 10, True) != False:
            writeToLog("INFO", "AS EXPECTED, video was paused within the first second")
        else:
            # Remove overlay before click pause (insert to 'touchOverlay' element 'style="display:none;"')
            self.removeTouchOverlay()
             
            if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 10, True) == False:
                writeToLog("INFO", "FAILED to pause the video")
                return False
             
        sleep(1)
         
        #availableQuestions will determine for how many times we will use the for loop
        for x in range(0,availableQuestions):
            # In order to make sure that the user passed the Question Screen transition properly
            if self.wait_element(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE, 15, True) == False:
                writeToLog("INFO", "FAILED to find any quiz scrubber questions bubbles")
                return False
            sleep(0.1)            
            if self.wait_element(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 0.1, True) != False:
                if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 1, True) == False:
                    writeToLog("INFO", "FAILED to dismiss the Question Screen during the second try")
                    return False
            
            #we use tmpQuizPage in order to navigate to the next Quiz Question page, by incrementing with +1 (using x value) from each run
            tmpQuizPage = (self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[0], self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_NUMBER[1].replace('NUMBER', str(x))) 
            if self.click(tmpQuizPage, 5, True) == False:
                sleep(0.25)
                if self.click(tmpQuizPage, 2, True) == False:
                    writeToLog("INFO", "FAILED to move to the " + str(x+1) + " quiz page after two tries")
                    return False        
             
            # We collect the active question in order to verify if it matches with one from our dictionary, if the question has not been founded within the 75 seconds, the test case will fail  
            activeQuestion = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 75, True).text
            
            # Because Reflection Point can be only watch we verify it first
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_REFLECTION_POINT_CONTAINER, 1, True) != False:
                writeToLog("INFO", "AS EXPECTED, Reflection Screen has been found and skipped")
                # Due to the fact that Reflection Points cannot be answered, we increment the number of question found and given questions by one ( without being present in our questionDict)
                questionsFound += 1
                givenQuestions += 1
            
                sleep(1)
                # If the Question is a Reflection Point, we will click on the continue button
                if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 1, True) == False:
                    writeToLog("INFO", "FAILED to use the continue button for the " + activeQuestion + " question")
                    return False
                         
            elif activeQuestion in questionDict:
                #after the active question matches with one from our dictionary, we take the answer assigned for that question
                activeAnswer = questionDict[activeQuestion]
                
                # If it's an open-Q we want to skip this part, because the answer isn't displayed yet
                if "Open-Q" not in activeAnswer:
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
                
                elif self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_OPEN_Q_POINT_CONTAINER, 1, True) != False:
                    writeToLog("INFO", "AS EXPECTED, open-Q Screen has been found")
                
                    sleep(1)
                    # Insert answer to the open-Q                              
                    if self.send_keys(self.PLAYER_QUIZ_QUESTION_SCREEN_OPEN_QUESTION_TEXT, activeAnswer) == False:
                        writeToLog("INFO", "FAILED to add answer to open-Q")
                        return False
                                     
                    if self.click(self.PLAYER_QUIZ_QUESTION_OPEN_QUESTION_SAVE_BTN) == False:
                        writeToLog("INFO", "FAILED to save answer to open-Q")
                        return False
                    questionsFound += 1
                
                    sleep(4)
                                
            else:
                #if the active Quiz Question answer is not present in our dictionary, we will skip it
                if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 1, True) == False:
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
            # We verify that all the available questions were answered
            if availableQuestions != questionsFound:
                writeToLog("INFO", "Some answers were not selected " + str(questionsFound) + " out of " + str(availableQuestions) + " questions")
                return False
            
            # We submit the quiz
            if self.submitTheAnswers(location, embed) != True:
                return False
            
            # We verify the expected quiz score
            if expectedQuizScore != '':
                if self.verifySubmittedScreen(expectedQuizScore, location, verifySubmittedScreenDict, expectedQuestionsStateDict, 30, embed, currentNumberOfAttemptsSubmittedScreen, totalGivenAttempts, expectedGeneralQuizScore, scoreType, showScore) == False:
                    return False
             
            return True
    
    
    # @Author: Oleg Sigalov
    # Remove overlay from the player if exists (instert to 'touchOverlay' element 'style="display:none;"')
    # This method doesn't return anything, because it removes only if exists
    def removeTouchOverlay(self):
        try:
            overlayElement = self.wait_element(self.PLAYER_TOUCH_OVERLAY, 2, multipleElements=True)
            self.driver.execute_script("arguments[0].setAttribute('style','display:none;')", overlayElement)
        except:
            pass
    
    # @Author: Horia Cus
    # This function switches the KEA Player iframe based on the location
    # location must be enum ( e.g location=enums.Location.ENTRY_PAGE)
    def selectPlayerIframe(self, location, embed=False):     
        if location == enums.Location.ENTRY_PAGE:
            self.switchToPlayerIframe(embed)
         
        elif location == enums.Location.KEA_PAGE:
            self.clsCommon.kea.switchToKEAPreviewPlayer()
            
        return True
    
    
    # @Author: Horia Cus
    # This function navigates to the end screen and then submits the answers
    # In order to submit the answers, all the Quiz questions must be answered, you can use answerQuiz function for that
    # location must be enum ( e.g location=enums.Location.ENTRY_PAGE)
    def submitTheAnswers(self, location, embed=False):
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch to the " + location.value + " iframe")
            return False
        
        # Verify if the Done bubble is available, if so, we will navigate to it
        if self.wait_element(self.PLAYER_QUIZ_SCRUBBER_DONE_BUBBLE, 3, True) != False:        
            if self.click(self.PLAYER_QUIZ_SCRUBBER_DONE_BUBBLE, 1, True) == False:
                self.removeTouchOverlay()
                if self.click(self.PLAYER_QUIZ_SCRUBBER_DONE_BUBBLE, 1, True) == False:
                    writeToLog("INFO", "FAILED to click on the scrubber done bubble")
                    return False
        
        #we verify that the user is in the "Submitted Screen"
        completedTitle = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[1].replace('TITLE_NAME', 'Completed'))
        if self.wait_element(completedTitle, 60, True) == False:
            writeToLog("INFO", "FAILED to found the Completed Screen")
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
    def verifyAndClickOnPlay(self, location=enums.Location.ENTRY_PAGE, timeOut=30, embed=False):
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch to the " + location.value + " iframe")
            return False
        
        # we verify if the play button is present, if so, we will click on it and trigger the playing process
        if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, timeOut, True) != False:
            if self.click(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 2, True) == False:
                writeToLog("INFO", "FAILED to activate the preview screen")
                return False
            
        sleep(0.5)
        if self.wait_while_not_visible(self.PLAYER_SCREEN_LOADING_SPINNER, 15) == False:
            writeToLog("INFO", "FAILED to wait until the loading spinner disappeared")
            return False
        sleep(0.1)
            
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
            writeToLog("INFO", "FAILED, you're not in the Submitted Screen")
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
    def downloadQuizPDF(self, filePath, embed=False):        
        self.switchToPlayerIframe(embed)
        
        #we verify if the playing button is present, if so, we will click on it so we can trigger the Quiz Welcome screen
        if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 30, True) != False:
            if self.click(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 2, True) == False:
                writeToLog("INFO", "FAILED to activate the welcome screen")
                return False
        
        sleep(2)
        #we click on the "PDF Download" button in order to trigger the download process
        if self.click(self.clsCommon.player.PLAYER_QUIZ_WELCOME_SCREEN_PDF_DOWNLOAD_BUTTON, 10, True) == False:
            writeToLog("INFO", "Failed to click on the download button")
            return False
        
        #we wait for three seconds, in order to make sure that our file has been downloaded successfully
        sleep(7)
        
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
    # In order to select the first row of answers, please use: answerQuiz function
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
    def resumeFromBeginningQuiz(self,location=enums.Location.ENTRY_PAGE, timeOut=2, forceResume=False, embed=False):     
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        sleep(timeOut)
        #we verify if any of the elements that indicates if the user is at the beginning of entry is present or not
        if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 1, True) == False and self.wait_element(self.PLAYER_QUIZ_CONTINUE_BUTTON, 1, True) == False or forceResume == True:  
            self.driver.refresh()
            self.clsCommon.base.switch_to_default_content()
            
            if self.selectPlayerIframe(location, embed) != True:
                writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
                return False
                
            if self.wait_element(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 15, True) == False:
                writeToLog("INFO", "FAILED to load the page after refreshing it")
                return False 
        
        return True
    

    # @Author: Horia Cus
    # expectedNumberOfAttempts = int, How many attempts user has. Empty when user isn't able to retake the quiz again
    def continueFromQuizWelcomeScreen(self, expectedNumberOfAttempts='', location, embed):
        #we verify if the "Continue" button specific for the Quiz "Welcome Screen" is present or not     
        if self.wait_element(self.PLAYER_QUIZ_CONTINUE_BUTTON, 15, True) != False:
            writeToLog("INFO", "Continue button has been found in welcome screen")
        else:
            # Add a redundancy step for the play button
            if self.verifyAndClickOnPlay(location, embed=embed) != True:
                return False
            else:
                if self.wait_element(self.PLAYER_QUIZ_CONTINUE_BUTTON, 15, True) != False:
                    writeToLog("INFO", "Continue button has been found in welcome screen")
                else:  
                    writeToLog("INFO", "FAILED to find the continue button from the welcome screen")
                    return False
        
        # If expected number of attempts != '', we expect to see total attempt message with the number of the available attempts
        if expectedNumberOfAttempts != '':
            # If we have no more attempts we shouldn't get allow attempt message
            if expectedNumberOfAttempts == 0:
                tmpAvailableAttemptMsg = (self.PLAYER_QUIZ_WELCOME_SCREEN_TOTAL_ATTEMPTS[0], self.PLAYER_QUIZ_WELCOME_SCREEN_TOTAL_ATTEMPTS[1].replace('NUMBER_OF_ATTEMPTS', str(expectedNumberOfAttempts)))
                if self.wait_element(tmpAvailableAttemptMsg) == True:
                    writeToLog("INFO", "FAILED: allow attempts message is displayed, although all attempts were used")
                    return False
            else:
                tmpAvailableAttemptMsg = (self.PLAYER_QUIZ_WELCOME_SCREEN_TOTAL_ATTEMPTS[0], self.PLAYER_QUIZ_WELCOME_SCREEN_TOTAL_ATTEMPTS[1].replace('NUMBER_OF_ATTEMPTS', str(expectedNumberOfAttempts)))
                if self.wait_element(tmpAvailableAttemptMsg) == False:
                    writeToLog("INFO", "FAILED to display correct total attempts message")
                    return False                

        #we click on the "continue" button and then wait one second in order to give time for the playing process to start
        if self.click(self.PLAYER_QUIZ_CONTINUE_BUTTON, 10, True) == False:
            writeToLog("INFO", "FAILED to continue further from the welcome screen")
            return False
        sleep(1)
        
        if self.wait_while_not_visible(self.PLAYER_SCREEN_LOADING_SPINNER, 30) == False:
            writeToLog("INFO", "FAILED to load the video after continuing from the Quiz Welcome Screen")
            return False
        
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
        
        # Remove overlay before click pause (instert to 'touchOverlay' element 'style="display:none;"')
        self.removeTouchOverlay()
        
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
            sleep(1)
            
        quizes = ", ".join(quizQuestions)
        writeToLog("INFO","The following Quiz Questions were skipped: " + quizes + "")
        return True
    
    
    # @Author: Horia Cus
    # This function initiates the playing process from the beginning
    # expectedNumberOfAttemptsWelcomeSreen = int: How many attempts user has. Empty when user isn't able to retake the quiz again
    def initiateQuizPlayback(self, location=enums.Location.ENTRY_PAGE, timeOut=2, skipWelcomeScreen=True, embed=False, expectedNumberOfAttempts=''):     
        sleep(timeOut)
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        sleep(1)
        #we resume the entry from the beginning
        if self.resumeFromBeginningQuiz(location, embed=embed) == False:
            return False                  
        
        #we triggering the playing process
        if self.verifyAndClickOnPlay(location, embed=embed) != True:
            return False
        
        #we dismiss the "Quiz Welcome Screen" if its enabled 
        sleep(1)
        if skipWelcomeScreen == True:
            if self.continueFromQuizWelcomeScreen(expectedNumberOfAttempts, location, embed) == False:
                return False
            
        if self.wait_while_not_visible(self.PLAYER_SCREEN_LOADING_SPINNER, 30) == False:
            writeToLog("INFO", "FAILED to load the video")
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
        
        # Remove overlay before click pause (instert to 'touchOverlay' element 'style="display:none;"')
        self.removeTouchOverlay()
        
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
    # In order to select the first row of answers, please use: answerQuiz function
    # If navigateToFirstQuestion = True, it will navigate to the first quiz page and return the quiz numbers
    # This function supports for now only multiple options question
    # If you want to verify if the "CHANGE QUIZ ANSWER" option is enabled, please use the changeQuizAnswer function
    # Now we support only "Multiple Question" quiz
    def verifyChangeQuizAnswerOptionDisabled(self, questionDict, location=enums.Location.ENTRY_PAGE, navigateToFirstQuestion=True):  
        if self.selectPlayerIframe(location) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        # We navigate to the first question, in order to have a question that has been answered already
        if navigateToFirstQuestion == True:
            if self.navigateToFirstQuestion(location) == False:
                writeToLog("INFO", "FAILED to navigate to the first quiz question")
                return  False
                
        # We verify that the question page that we are in, has an answer selected 
        sleep(2)    
        try:
            activeQuestion        = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 10, True).text
            activeSelectedAnswer  = self.wait_element(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_HIGLIGHTED_ANSWER, 10, True).text
        except Exception:
            writeToLog("INFO", "FAILED to find an active question and a selected answer")
            return False
        
        # We verify that the "active question' text from the active "Question Screen", matches with one from our dictionary
        if activeQuestion in questionDict:
            # We take the new answer, specific for the active question screen
            newAnswer = questionDict[activeQuestion]
            tmpAnswerName = (self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[0], self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[1].replace('ANSWER_TEXT', newAnswer))
            
            # We verify that the selected answer that we want to replace, it's not the same with the new one
            if activeSelectedAnswer.count(newAnswer) == 1:
                writeToLog("INFO", "The " + newAnswer + " is already selected, please make sure that you're using a new answer")
                return False  
            
            # We verify that the new answer is present in the question screen
            if self.wait_element(tmpAnswerName, 5, True) == False:
                writeToLog("INFO", "The " + newAnswer + " has not been found in the " + activeQuestion + " question page")
                return False
                 
            # We click on the new answer, in order to trigger the highlight state
            if self.click(tmpAnswerName, 10, True) == False:
                writeToLog("INFO", "FAILED to click on the " + newAnswer + " answer")
                return False
            
            # We verify that the new answer is not highlighted after clicking on it
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECT_BUTTON, 2, True) != False:
                writeToLog("INFO", "The select option is displayed for the " + newAnswer + " new answer")
                return False
        
        else:
            writeToLog("INFO", "FAILED to find a Quiz Question that matches with the questionDict")
            return False
        
        return True
    
    
    # @Author: Horia Cus
    # This function will verify that all the quiz elements are properly displayed based on the state, question type, expected quiz score and question details
    # questionDict must follow the following structure       = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection} 
        # questionMultipleWithHintAndWhy     = ['mm:ss', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
        # questionMultipleWithOnlyHint       = ['mm:ss', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice']
        # questionMultipleWithoutHintAndWhy  = ['mm:ss', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4']
        # questionTrueAndFalse = ['mm:ss', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
        # questionReflection   = ['mm:ss', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']
    # expectedQuizStateNew must have the following structure = {'1':questionAnswered,'2':questionUnANswered, '3':questionReflection} 
        # questionAnswered        = ['Question Title', 'Answer One', True]
        # questionUnANswered      = ['Question Title', '', False]
        # questionReflection      = ['Question Title', '', False]
    # If the quiz state is submitted, the submittedQuiz must = True, and the resumeQuiz, newQuiz to = False
    # If the quiz state is resumed, the resumeQuiz must = True, and the submittedQuiz, newQuiz to = False
    # If the quiz state is new, the newQuiz must = True, and the submittedQuiz, resumeQuiz to = False
    # expectedQuizScore must contain the percentage of the expected quiz score ( use string e.g str(50) )
    # Questions can be verified with or without hint and why, you can verify the Hint and Why using this structure for both True and False and Multiple Choice:
        # Hint and Why = last two indexes from the list must contain ['Hint text' and 'Why Text']
        # Only Hint = last index must contain ['Hint text']
        # Without Hint and Why = last indexes must contain the answer text
    def quizVerification(self, questionDict, expectedQuestionsState, submittedQuiz, resumeQuiz, newQuiz, expectedQuizScore, location, timeOut=60, embed=False, skipWelcomeScreen=True):  
        if self.initiateQuizPlayback(location, 2, skipWelcomeScreen, embed) == False:
            return False
        
        # We verify from the beginning the submitted quiz option, because we don't have the scrubber ( only Quiz Welcome screen and the Submitted Screen)
        if submittedQuiz == True:
            if self.verifySubmittedScreen(expectedQuizScore, location, questionDict, expectedQuestionsState, 5, embed) == False:
                return False
            # We dismiss the submitted screen, in order to verify the Question Screens and the scrubber
            if self.click(self.PLAYER_QUIZ_SUBMITTED_SCREEN_DONE_BUTTON, 2, True) == False:
                writeToLog("INFO", "FAILED to click on the 'Done' button from the Submitted Screen in order to trigger the playing process")
                return False
            
            # We wait until the player screen is loaded
            if self.wait_while_not_visible(self.PLAYER_SCREEN_LOADING_SPINNER, 30) == False:
                writeToLog("INFO", "FAILED to load the video")
                return False
        
        # We pause the video, in order to make sure that we won't miss any elements from the scrubber
        if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 10, True) != False:
            writeToLog("INFO", "AS EXPECTED, video was paused within the first second")
        else:
            # Remove overlay before click pause (insert to 'touchOverlay' element 'style="display:none;"')
            self.removeTouchOverlay()
            
            if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 10, True) == False:
                writeToLog("INFO", "FAILED to pause the video")
                return False
                         
        sleep(1)        
        # We verify that the number of questions from our dictionary is the same with the number of the questions found in the scrubber, and the state of them
        if self.verifyQuestionBubbleState(expectedQuestionsState, submittedQuiz, resumeQuiz, newQuiz, location, embed) == False:
            return False        
         
        # We resume the playing process
        if self.click(self.PLAYER_PLAY_BUTTON_IN_THE_MIDDLE_OF_THE_PLAYER, 30, True) == False:
            writeToLog("INFO", "FAILED to pause the video")
            return False       
         
        # We verify each question from our dictionary 
        for x in range(0, len(questionDict)):
            tries = 0
            # We verify if the active question it's present in the current dictionary
            for questionNumber in questionDict:
                # We take the question details from the current list
                questionDetails = questionDict[questionNumber]
                # We take the question type, in order to know what we should verify
                questionType = questionDetails[1]
                
                # We wait for the active question to be displayed within the timeOut period and compare it with the current question details
                presentedQuestion = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, timeOut).text
                
                if presentedQuestion in questionDetails:
                    # We verify that all the quiz elements are properly displayed based on the state, question type, expected quiz score and question details                                             
                    if self.quizVerificationMethodHelper(questionType, questionDetails, expectedQuestionsState, questionNumber, location, embed) == False:
                        return False
                    
                    # We navigate to the next question or to the submitted / almost done screen
                    if self.click(self.PLAYER_QUIZ_SKIP_FOR_NOW_BUTTON, 5, True) == False:
                        writeToLog("INFO", "FAILED to move to the next Quiz Question")
                        return False
                    
                    # We break after we checked that the active question is valid, and continue with the next question from the range
                    break
                else:
                    tries += 1
                
                if len(questionDict)+1 == tries:
                    writeToLog("INFO", "FAILED to find the Quiz Question screen that would match the question dictionary")
                    return False
        
        # We verify that the 'Almost Done' screen is displayed for the quiz with new and/or resume status
        if newQuiz == True or resumeQuiz == True:
            if self.verifyAlmostDoneScreen(location, 60, embed) == False:
                writeToLog("INFO", "FAILED to display the Almost Done screen")
                return False
        
        writeToLog("INFO", "All the questions were properly verified")
        return True
    
    
    # @Author: Horia Cus
    # This function verify that the configured hint text during the KEA editing is displayed in the 'Hint Screen'
    # In order to use this function, you must be in the Quiz Question Screen
    # hintString = contains the text present in the 'Hint Screen'
    # After the hint screen was checked, the 'Question Screen' is resumed
    def hintVerification(self, hintString, location=enums.Location.ENTRY_PAGE, embed=False):  
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        # We verify that the user is present in an active 'Question Screen'
        if self.wait_element(self.PLAYER_QUIZ_QUESTION_TITLE, 5, True) == False:
            writeToLog("INFO", "FAILED, you're not in the Quiz Question screen")
            return False
        
        # We take the question title in order to make sure that we can resume the 'Question Screen' after being in the 'Hint Screen'
        questionTitleText = self.get_element(self.PLAYER_QUIZ_QUESTION_TITLE).text
        questionTitle = (self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_TEXT[0], self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_TEXT[1].replace('QUESTION_NAME', questionTitleText))
        
        # We verify that the 'Hint' string is valid
        if hintString != '':
            # We navigate to the Hint Screen
            if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_HINT_BUTTON, 3, True) == False:
                writeToLog("INFO", "FAILED to activate the Hint screen")
                return False
            
            # We verify that the hint from the Hint Screen, matches with the Hint inserted in the KEA Editor
            hintText = (self.PLAYER_QUIZ_QUESTION_SCREEN_HINT_TEXT[0], self.PLAYER_QUIZ_QUESTION_SCREEN_HINT_TEXT[1].replace('HINT_TEXT', hintString))
            if self.wait_element(hintText, 5, True) == False:
                writeToLog("INFO", "FAILED to find the " + hintString + " in the Hint screen")
                return False
            
            # We navigate back to the Quiz Question Screen
            if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_HINT_CLOSE_BUTTON, 3, True) == False:
                writeToLog("INFO", "FAILED to click on the Hint close button")
                return False
            
            # We verify that the 'Question Screen' is properly resumed
            if self.wait_element(questionTitle, 10, True) == False:
                writeToLog("INFO", "FAILED to resume the Quiz Question screen during the transition from the Hint page")
                return False
        
        writeToLog("INFO", "The " + hintString + " has been found in the 'Hint Screen'")
        return True
    

    # @Author: Horia Cus
    # This function verify the state of the bubbles in three different scenarios:
    # if submittedQuiz = True, it will verify that all the available quiz question bubbles are answered
    # if resumeQuiz = True, it will verify that from all the available quiz question bubbles at least one is unanswered ( based on the expectedQuestionsState )
    # if newQuiz = True, it will verify that all the available quiz question bubbles are unanswered
    # expectedQuizStateNew must have the following structure  = {'1':questionAnswered,'2':questionTwoNew, '3':questionThreeNew} 
    # questionAnswered        = ['Question answered', True]
    # questionUnanswered      = ['Question unanswered', False]
    # If True is present in the list, it means that the question bubble should be displayed as answered
    # If False is present in the list, it means that the question bubble should be displayed as unanswered
    def verifyQuestionBubbleState(self, expectedQuestionsState, submittedQuiz, resumeQuiz, newQuiz, location, embed=False):  
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        try:
            # We take the number of all the available question bubbles
            scrubberAllAvailableQuestions            = self.wait_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE, 1)
            # We take the number of answered question bubbles
            scrubberAnsweredQuestions                = self.wait_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_ANSWERED, 1)
            # We take the number of unanswered question bubbles
            scrubberUnAnsweredQuestions              = self.wait_elements(self.PLAYER_QUIZ_SCRUBBER_QUESTION_BUBBLE_UN_ANSWERED, 1)
        except Exception:
            pass

        # We verify that the number of questions from our dictionary is the same with the number of the questions found in the scrubber
        if len(expectedQuestionsState) != len(scrubberAllAvailableQuestions):
            writeToLog("INFO", "FAILED, " + str(len(expectedQuestionsState)) + " questions were expected and " + str(len(scrubberAllAvailableQuestions)) + " were found" )
            return False
        
        if submittedQuiz == True:           
            # We compare the available quiz question bubbles with the answered quiz question bubbles
            if len(scrubberAllAvailableQuestions) != len(scrubberAnsweredQuestions):
                writeToLog("INFO", "FAILED" + str(len(scrubberAllAvailableQuestions)) + " questions were found and " + str(len(scrubberAnsweredQuestions)) + " were answered, while the Quiz should be submitted")
                return False
            
        elif resumeQuiz == True:
            numberOfAnsweredQuestions   = 0
            numberOfUnasweredQuestions  = 0
            for questionNumber in expectedQuestionsState:
                questionDetails = expectedQuestionsState[questionNumber]
                # We take the number of the expected answered questions
                numberOfAnsweredQuestions  += questionDetails.count(True)
                # We take the number of the expected unanswered questions
                numberOfUnasweredQuestions += questionDetails.count(False)
            
            # We verify that the number of the answered quiz question bubbles match with the number of the expected quiz question state
            if len(scrubberAnsweredQuestions) != numberOfAnsweredQuestions:
                writeToLog("INFO", "FAILED" + str(len(scrubberAnsweredQuestions)) + " questions were found as answered and only " + str(numberOfAnsweredQuestions) + " should be answered, while resuming the quiz")
                return False         

            # We verify that the number of the unanswered quiz question bubbles match with the number of the expected quiz question state         
            if len(scrubberUnAnsweredQuestions) != numberOfUnasweredQuestions:
                writeToLog("INFO", "FAILED" + str(len(scrubberUnAnsweredQuestions)) + " questions were found as unanswered and only" + str(numberOfUnasweredQuestions) + " should be unanswered, while resuming the quiz")
                return False
            
        elif newQuiz == True:
            # We verify that all the available quiz question bubbles are unanswered
            if len(scrubberAllAvailableQuestions) != len(scrubberUnAnsweredQuestions):
                writeToLog("INFO", "FAILED" + str(len(scrubberAllAvailableQuestions)) + " questions were found and only" + str(scrubberUnAnsweredQuestions) + " where unanswered, while having a new quiz")
                return False
        
        writeToLog("INFO", "All the quiz question bubbles were properly displayed in the scrubber section")   
        return True
    

    # @Author: Horia Cus
    # This function verifies the state of the Question Screen by checking that:
    # the active question matches with the desired question from expectedQuestionsState
    # the active question is answered or not, based on the expectedQuestionsState
    # the active answer matches with the answer from the expectedQuestionsState
    # expectedQuizStateNew must have the following structure = {'1':questionAnswered,'2':questionUnANswered, '3':questionReflection} 
    # questionAnswered        = ['Question Title', 'Answer One', True]
    # questionUnANswered      = ['Question Title', '', False]
    # questionReflection      = ['Question Title', '', False]
    # questionAnswered        = ['Question Title', 'Answer One', False] will still verify that the selected answer is present, because the same dictionary is used in the verifySubmittedScreen, where we check the state of the included answers
    def verifyQuestionScreenState(self, expectedQuestionsState, location, embed=False):  
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        # We collect the active question in order to verify if it matches with one from our dictionary  
        presentedQuestion = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_QUESTION_DEFAULT, 120, True).text
        # We take the Quiz Question title from the expectedQuestionsState dictionary
        questionTitleString = expectedQuestionsState[0]
        
        # We verify that the active question is the same with the Question Title from our dictionary
        if presentedQuestion == questionTitleString:
            # The below condition will verify that no Answer is displayed as being selected / answered
            if expectedQuestionsState[1] == '' and expectedQuestionsState[2] == False:
                if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 1, True) != False:
                    writeToLog("INFO", "FAILED, a question has been answered inside the " + questionTitleString + " Quiz Question, when it shouldn't be")
                    return False
                
            # The below condition will verify that desired answer is displayed as being selected / answered 
            elif expectedQuestionsState[1] != '' or expectedQuestionsState[2] == True:
                if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_BUTTON, 1, True) == False:
                    writeToLog("INFO", "FAILED, no question is displayed as being selected inside the " + questionTitleString + " , when it should have")
                    return False
                
                # We take the string for the selected answer, using the answer container
                answerContainer = self.get_element(self.PLAYER_QUIZ_QUESTION_SCREEN_SELECTED_ANSWER_CONTAINER).text
                # We remove the \nSelected string from the answer container, leaving only the selected answer string
                answerText = answerContainer[:-9]
                
                # We verify that the active answer, matches with the answer inserted in our dictionary
                if answerText != expectedQuestionsState[1]:
                    writeToLog("INFO", "FAILED, " + answerText + " is displayed as being selected, when the " + expectedQuestionsState[1] + " should be selected")
                    return False                        
                
            else:
                writeToLog("INFO", "FAILED, please make sure that you used the correct structure for the expectedQuestionsState dictionary")
                return False
        else:
            writeToLog("INFO", "FAILED, the selected question " + expectedQuestionsState[0] +" doesn't match with the active one" + presentedQuestion)
            return False
        
        writeToLog("INFO", "All the available answers were properly checked for the " + expectedQuestionsState[0] + " question")                         
        return True
    

    # @Author: Horia Cus
    # This function verify that the Submitted Screen is present along with the correct expected quiz score
    # expectedQuizScore = must be string but use only numbers ( e.g expectedQuizScore=str(50))
    # timeOut = maximum amount of time until the 'Submitted Screen' screen should be triggered and displayed
    # expectedQuestionsState must be dictionary with the following structure {'QUESTION NUMBER':questionList}
        # questionListForCorrectAnswer     = ['question title', True]
        # questionListForInvalidAnswer     = ['question title', False]
        # questionListForReflectionPoint   = ['question title', False]
    # currentNumberOfAttemptsSubmittedScreen = Number: The number of the current attempt, displayed in submitted screen
    # totalGivenAttempts = Number: The total given number of attempts
    # expectedGeneralQuizScore = String: Represent the score of all attempts based on the score type
    # scoreType = enum.playerQuizScoreType: Represent the score type (Latest, Highest, Average, Lowest, First)
    def verifySubmittedScreen(self, expectedQuizScore, location, questionDict='', expectedQuestionsState='', timeOut=30, embed=False, currentNumberOfAttemptsSubmittedScreen='', totalGivenAttempts='', expectedGeneralQuizScore='', scoreType='', showScore=True):  
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        # We verify that the Submitted Screen is presented
        submittedScreen = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[1].replace('TITLE_NAME', 'Submitted'))
        if self.wait_element(submittedScreen, timeOut) == False:
            writeToLog("INFO", "FAILED, the Submitted Screen was not present")
            return False
         
        # We verify that the score is not present
        quizScore = self.wait_element(self.PLAYER_QUIZ_SUBMITTED_SCREEN_SCORE, 1)
        if showScore == True:
            if quizScore.text != expectedQuizScore:
                writeToLog("INFO", "FAILED, " + quizScore.text + " quiz score was displayed, instead of the expected: " + expectedQuizScore + " quiz score")
                return False
        else:
            if quizScore == True:
                writeToLog("INFO", "FAILED, score is displayed although it shouldn't be displayed")
                return False
        
        # If we have more than one attempt
        if totalGivenAttempts != '':
            # we verify that correct total score and score type are displayed
            tmpTotalScore = (self.PLAYER_SUBMITTED_SCREEN_TOTAL_SCORE[0], self.PLAYER_SUBMITTED_SCREEN_TOTAL_SCORE[1].replace('TOTAL_SCORE', expectedGeneralQuizScore).replace('SCORE_TYPE', scoreType.value))
            # If we are expecting to see score
            if showScore == True:
                if self.wait_element(tmpTotalScore) == False:
                    writeToLog("INFO", "FAILED, score and score type aren't presented correctly")
                    return False 
            else:
                if self.wait_element(tmpTotalScore) == True:
                    writeToLog("INFO", "FAILED, score is displayed although it should be displayed")
                    return False  
                          
            # we verify that correct attempts (total and current) are displayed
            tmpAttempts = (self.PLAYER_SUBMITTED_SCREEN_CURRENT_ATTEMPT_NUMBER[0], self.PLAYER_SUBMITTED_SCREEN_CURRENT_ATTEMPT_NUMBER[1].replace('CURRENT_ATTEMPTS', str(currentNumberOfAttemptsSubmittedScreen)).replace('TOTAL_ATTEMPTS', str(totalGivenAttempts)))    
            if self.wait_element(tmpAttempts) == False:
                writeToLog("INFO", "FAILED, attempts number isn't displayed correctly")
                return False                

        # If questionDict is empty, we will not verify the why
        if questionDict != '':            
            # We navigate to each specific question number
            for questionNumber in questionDict:
                # We take the question details from the current list
                questionDetails = questionDict[questionNumber]
                quizNumberID = int(questionNumber) - 1
                # We create the locator that it will be used in order to enter in the Include Answer screen
                quizQuestionNumber = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE_ID[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_RECTANGLE_ID[1].replace('NUMBER', str(quizNumberID)))
                
                # We verify that in the dictionary we have a why
                if enums.QuizQuestionType.Multiple in questionDetails and len(questionDetails) >= 9 or enums.QuizQuestionType.TRUE_FALSE in questionDetails and len(questionDetails) >= 6 or enums.QuizQuestionType.OPEN_QUESTION in questionDetails and len(questionDetails) >= 5:
                    # We verify if the Quiz Question number is on the second submitted screen page, and navigate to it
                    if quizNumberID >= 13:
                        if self.wait_visible(self.PLAYER_QUIZ_SUBMITTED_SCREEN_NEXT_ARROW, 1, True) != False:
                            if self.click(self.PLAYER_QUIZ_SUBMITTED_SCREEN_NEXT_ARROW, 1, True) == False:
                                writeToLog("INFO", "FAILED to navigate to the second submitted screen list")
                                return False
                    # We verify if the Quiz Question number is on the first submitted screen page, and navigate to it
                    elif quizNumberID <= 12:
                        if self.wait_visible(self.PLAYER_QUIZ_SUBMITTED_SCREEN_PREVIOUS_ARROW, 1, True) != False:
                            if self.click(self.PLAYER_QUIZ_SUBMITTED_SCREEN_PREVIOUS_ARROW, 1, True) == False:
                                writeToLog("INFO", "FAILED to navigate to the first submitted screen list")
                                return False                    
                    
                    if self.click(quizQuestionNumber, 1) == False:
                        writeToLog("INFO", "FAILED to navigate to the " + str(questionNumber) + " Include Answer screen")
                        return False
                    
                    presentedQuestion = self.wait_element(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_TITLE_DEFAULT, 5).text
                    
                    if presentedQuestion in questionDetails:
                        if self.click(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_WHY_BUTTON, 2) == False:
                            writeToLog("INFO", "FAILED to click on the why button")
                            return False
                        
                        sleep(1)
                        # we take the active why from the 'Why' screen
                        presentedWhy = self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_HINT_CONTAINER, 3).text
                        # we take the expected why from our list
                        expectedWhy = questionDetails[-1]
                        
                        if presentedWhy != expectedWhy:
                            writeToLog("INFO", "The active why: " + presentedWhy + " doesn't match with the expected why: " + expectedWhy)
                            return False
                        
                        if self.click(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_CLOSE_BUTTON, 1) == False:
                            writeToLog("INFO", "FAILED to exit from the 'Why' screen")
                            return False
                        
                        if self.click(self.PLAYER_QUIZ_INCLUDE_ANSWER_SCREEN_GO_BACK_BUTTON, 1) == False:
                            writeToLog("INFO", "FAILED to resume to the 'Included' Screen")
                            return False
                        
                    else:
                        writeToLog("INFO", "The active question: " + presentedQuestion + " doesn't match with the active list")
                        return False
                
                elif enums.QuizQuestionType.REFLECTION in questionDetails:
                    writeToLog("INFO", "AS EXPECTED: No 'WHY' is available for Reflection Quiz Questions")
                    
        # We verify the state of the include answer screen based on the boolean = True, included answer is correct, = False, included answer is wrong
        if expectedQuestionsState != '':
            for questionNumber in expectedQuestionsState:
                # We take the question details from the current list
                expectedDetails = expectedQuestionsState[questionNumber]
                quizNumberID = int(questionNumber) - 1
                
                # We verify if the Quiz Question number is on the second submitted screen page, and navigate to it
                if quizNumberID >= 13:
                    if self.wait_visible(self.PLAYER_QUIZ_SUBMITTED_SCREEN_NEXT_ARROW, 1, True) != False:
                        if self.click(self.PLAYER_QUIZ_SUBMITTED_SCREEN_NEXT_ARROW, 1, True) == False:
                            writeToLog("INFO", "FAILED to navigate to the second submitted screen list")
                            return False
                # We verify if the Quiz Question number is on the first submitted screen page, and navigate to it
                elif quizNumberID <= 12:
                    if self.wait_visible(self.PLAYER_QUIZ_SUBMITTED_SCREEN_PREVIOUS_ARROW, 1, True) != False:
                        if self.click(self.PLAYER_QUIZ_SUBMITTED_SCREEN_PREVIOUS_ARROW, 1, True) == False:
                            writeToLog("INFO", "FAILED to navigate to the first submitted screen list")
                            return False    
                
                # We verify that the answers that failed, are displayed properly in the include answer screen, along with Reflection Point
                if expectedDetails.count(False) == 1:
                    quizQuestionNumberFalse      = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_FALSE_ID[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_FALSE_ID[1].replace('NUMBER', str(quizNumberID)))
                    quizQuestionNumberReflection = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_REFLECTION_ID[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_REFLECTION_ID[1].replace('NUMBER', str(quizNumberID)))
                    if self.wait_element(quizQuestionNumberFalse, 1, True) == False and self.wait_element(quizQuestionNumberReflection, 1, True) == False:
                        writeToLog("INFO", "FAILED, the question " + questionDetails[0] + " is not displayed as false, when it should")
                        return False
                
                # We verify that the answers that passed, are displayed properly in the include answer screen, along with Reflection Point   
                elif expectedDetails.count(True) == 1:
                    quizQuestionNumberTrue = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_TRUE_ID[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_ANSWER_TRUE_ID[1].replace('NUMBER', str(quizNumberID)))
                    quizQuestionNumberReflection = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_REFLECTION_ID[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_REFLECTION_ID[1].replace('NUMBER', str(quizNumberID)))
                    quizQuestionNumberOpenQ = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_OPEN_Q_ID[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_INCLUDE_OPEN_Q_ID[1].replace('NUMBER', str(quizNumberID)))
                    if self.wait_element(quizQuestionNumberTrue, 1, True) == False  and self.wait_element(quizQuestionNumberReflection, 1, True) == False and self.wait_element(quizQuestionNumberOpenQ, 1, True) == False:
                        writeToLog("INFO", "FAILED, the question " + questionDetails[0] + " is not displayed as true, when it should")
                        return False
                    
        writeToLog("INFO", "ALL the details were properly displayed in the submitted screen")                    
        return True 
    

    # @Author: Horia Cus
    # This function verify that the 'Almost Done' screen is present by checking the title and description
    # timeOut = maximum amount of time until the 'Almost Done' screen should be triggered and displayed
    def verifyAlmostDoneScreen(self, location, timeOut=30, embed=False):  
        if self.selectPlayerIframe(location, embed) != True:
            writeToLog("INFO", "FAILED to switch the player iframe for the " + location.value + " location")
            return False
        
        # Verify if the user got stucked inside a Question Screen
        if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_CONTINUE_BUTTON, 2, True) != False:
            if self.click(self.PLAYER_QUIZ_QUESTION_SCREEN_CONTINUE_BUTTON, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Continue Button From Question Screen in order to proceed to the Almost Done Screen")
                return False
        
        # We verify that the Almost Completed screen is presented
        almostDoneScreen = (self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[0], self.PLAYER_QUIZ_SUBMITTED_SCREEN_TITLE_TEXT[1].replace('TITLE_NAME', 'Almost Done'))
        if self.wait_element(almostDoneScreen, timeOut) == False:
            writeToLog("INFO", "FAILED, the Almost Completed Screen was not displayed after resuming the Quiz")
            return False
        
        # We verify that the score is not present
        description = self.wait_element(self.PLAYER_QUIZ_SUBMITTED_SCREEN_SUB_TEXT, 10).text
        if description != 'It appears that some questions remained unanswered\nYou must answer all questions before you can submit':
            writeToLog("INFO", "FAILED, another description than the resume is displayed")
            return False
        
        return True
        
    
    # @Author: Horia Cus
    # This function will verify that all the quiz elements are properly displayed based on the state, question type, expected quiz score and question details
    # questionType must follow the following structure: enums.QuizQuestionType.Type
    # questionDetails must follow the following structure:     questionDict        = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection} 
        # questionMultiple     = ['mm:ss', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text for Multiple Choice', 'Why Text For Multiple Choice']
        # questionTrueAndFalse = ['mm:ss', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text for True and False', 'Why Text For True and False']
        # questionReflection   = ['mm:ss', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point']
    # expectedQuizStateNew must have the following structure = {'1':questionAnswered,'2':questionUnANswered, '3':questionReflection} 
        # questionAnswered        = ['Question Title', 'Answer One', True]
        # questionUnANswered      = ['Question Title', '', False]
        # questionReflection      = ['Question Title', '', False]
    # questionNumber must contain the number from the dictionary for the active quiz question
    # We verify that the proper container is displayed, based on the question Type
    # We verify that the correct time is displayed, based on the scrubber time and questionDetails time
    # We verify that all the answers are present in the Quiz Question screen, based on the questionDetails
    # We verify if the hint is available for the active Quiz Question, based on the len of the questionDetails, and verify if the proper 'Hint' is displayed
    def quizVerificationMethodHelper(self, questionType, questionDetails, expectedQuestionsState, questionNumber, location, embed=False):
        # We verify the active question based on the question type
        if questionType == enums.QuizQuestionType.Multiple:
            listInterval = questionDetails[3:7]
            hintTriggerNumber = 8
            try:
                hintText = questionDetails[7]
            except Exception:
                writeToLog("INFO", "AS Expected, no hint was provided for the " + questionDetails[2] + " Quiz Question")
                pass
            
            # We verify that the proper Quiz Question screen is displayed
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_MULTIPLE_CHOICE_CONTAINER, 5, True) == False:
                writeToLog("INFO", "FAILED to load the " + questionDetails[2] + " Quiz Question screen")
                return False

        # We verify the active question based on the question type          
        elif questionType == enums.QuizQuestionType.TRUE_FALSE:
            listInterval = questionDetails[3:5]
            hintTriggerNumber = 5
            try:
                hintText = questionDetails[5]
            except Exception:
                writeToLog("INFO", "AS Expected, no hint was provided for the " + questionDetails[2] + " Quiz Question")
                pass
            
            # We verify that the proper Quiz Question screen is displayed
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_TRUE_FALSE_CONTAINER, 5, True) == False:
                writeToLog("INFO", "FAILED to load the " + questionDetails[2] + " Quiz Question screen")
                return False
            
        # We verify the active question based on the question type  
        elif questionType == enums.QuizQuestionType.REFLECTION:
            # We verify that the proper Quiz Question screen is displayed
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_REFLECTION_POINT_CONTAINER, 5, True) == False:
                writeToLog("INFO", "FAILED to load the " + questionDetails[2] + " Quiz Question screen")
                return False  
            
        # We verify the active question based on the question type          
        elif questionType == enums.QuizQuestionType.OPEN_QUESTION:
            listInterval = questionDetails[3:4]
            hintTriggerNumber = 4
            try:
                hintText = questionDetails[4]
            except Exception:
                writeToLog("INFO", "AS Expected, no hint was provided for the " + questionDetails[2] + " Quiz Question")
                pass
            
            # We verify that the proper Quiz Question screen is displayed
            if self.wait_element(self.PLAYER_QUIZ_QUESTION_SCREEN_OPEN_Q_CONTAINER, 5, True) == False:
                writeToLog("INFO", "FAILED to load the " + questionDetails[2] + " Quiz Question screen")
                return False                 
            
        # We take the active time from the scrubber
        presentedTime = self.get_element(self.PLAYER_CURRENT_TIME_LABEL).text
        # We take the time that has been used during the KEA editing process
        if questionDetails[0][0] == str(0):
            questionTimeList = list(questionDetails[0][1:5])
            questionTime = ''.join(questionTimeList)
        else:
            questionTime = questionDetails[0]
         
        # We verify that the time from Entry Page matches with the time configured in KEA Editor
        if presentedTime != questionTime:
            writeToLog("INFO", "The  " + questionDetails[2] + " Question was not present at the expected time, expected time " + questionTime + "/ actual " + presentedTime )
            return False

        if questionType == enums.QuizQuestionType.Multiple or questionType == enums.QuizQuestionType.TRUE_FALSE:    
            # We take the answers that were given during the KEA editing process
            expectedQuestionAnswerList                  = listInterval
            expectedQuestionAnswersWithValidAnswers     = []
            
            # We add the answers that are valid (not empty) to the expectedQuestionAnswersWithValidAnswers
            for answer in expectedQuestionAnswerList:
                if answer != '':
                    expectedQuestionAnswersWithValidAnswers.append(answer)
            
            # We take the elements that are present in the Quiz Question screen
            questionAnswersPresent = self.wait_elements(self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER, 2)
            
            # We verify that the answer number from the Entry Page matches with the answer number configured in the KEA Editor
            if len(questionAnswersPresent) != len(expectedQuestionAnswersWithValidAnswers):
                writeToLog("INFO", "FAILED, the question number from the Entry Page doesn't match with the question number created in the KEA Editor")
                return False
            
            # We verify that the answer name from the entry page, matches with the one that was configured in the KEA Editor
            for answer in expectedQuestionAnswersWithValidAnswers:
                tmp_answer = (self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[0], self.PLAYER_QUIZ_QUESTION_SCREEN_ANSWER_TEXT[1].replace('ANSWER_TEXT', answer))
                if self.wait_element(tmp_answer, 3, True) == False:
                    writeToLog("INFO", "FAILED to find the " + answer + " in the " + questionDetails[2] + " question")
                    return False
            
            # We verify if a Hint should be present for the active quiz question
            if len(questionDetails) >= hintTriggerNumber:
                # We verify the Hint Screen
                if self.hintVerification(hintText, location, embed) == False:
                    return False
            else:
                writeToLog("INFO", "No HINT is available for the " + questionDetails[2] + " Quiz Question")
        
        # We verify the title, available answers and the state of the answers ( answered / unanswered )
        if questionType == enums.QuizQuestionType.Multiple or questionType == enums.QuizQuestionType.TRUE_FALSE:  
            if self.verifyQuestionScreenState(expectedQuestionsState[questionNumber], location, embed) == False:
                return False
        
        return True
    
    
    # @Author: Horia Cus
    # hotspotList must contain the following structure ['Hotspot Title', enums.keaLocation.Location, startTime, endTime, 'link.address', enums.textStyle.Style, 'font color code', 'background color code', text size, roundness size]
    # location=enums.Location.ENTRY_PAGE
    # For the link.address we can have a web page ( e.g https://6269.qakmstest.dev.kaltura.com/ ) and also a time location ( e.g 90, which will translate into 01:30 )
    # To be Developed: Cue Point Verification interval
    def hotspotVerification(self, hotspotsDict, location=enums.Location.ENTRY_PAGE, embed=False):        
        if self.verifyAndClickOnPlay(location, 30, embed) == False:
            return False
        
        # Create the list that will contain details for each available hotspot
        presentedHotspotsDetailsList = []
        presentedHotspotsNameList    = []
        
        # Run the player until we took all the available hotspots
        while self.wait_element(self.PLAYER_REPLAY_BUTTON_CONTROLS_CONTAINER, 0.1, True) == False:
            # Take the current hotspots elements
            presentedHotspots = self.wait_elements(self.PLAYER_HOTSPOT_PRESENTED, 30)
            
            # Verify that at least one hotspot has been found
            if presentedHotspots != False:
                # Iterate through each presented hotspot    
                for x in range(0, len(presentedHotspots)):
                    try:
                        # Verify that the hotspot found its new
                        if len(presentedHotspotsDetailsList) == 0 or any(presentedHotspots[x].text in sl for sl in presentedHotspotsDetailsList) == False:
                            # Take the presented hotspot details for the current iterated hotspot
                            hotspotStartTime            = self.returnEntryCurrentTimeInSeconds()
                            
                            hotspotTitle                = presentedHotspots[x].text             
                            hotspotStyleProperties      = presentedHotspots[x].get_attribute('style').split()
                            
                            hotspotStyleFontWeight      = hotspotStyleProperties[hotspotStyleProperties.index('font-weight:')+1].replace(';','')
                            
                            # Verify the hotspot font size
                            if hotspotStyleFontWeight == 'bold':
                                hotspotStyleFontWeight = enums.textStyle.BOLD
                                
                            elif hotspotStyleFontWeight == 'normal':
                                hotspotStyleFontWeight = enums.textStyle.NORMAL
                                
                            elif hotspotStyleFontWeight == 'lighter':
                                hotspotStyleFontWeight = enums.textStyle.THIN
                                
                            else:
                                writeToLog("INFO", "FAILED, unknown presented font weight " + hotspotStyleFontWeight)
                                return False
                            
                            # Verify the hotspot container size
                            hotspotWidth                = int(presentedHotspots[x].size['width'])
                            hotspotHeight               = int(presentedHotspots[x].size['height'])
                            if hotspotWidth >= 79 and hotspotWidth <= 95 and hotspotHeight >= 34 and hotspotHeight <= 50:
                                hotspotContainerSize    = enums.keaHotspotContainerSize.SMALL
                            elif hotspotWidth >= 336 and hotspotWidth <= 386 and hotspotHeight >= 79 and hotspotHeight <= 95:
                                hotspotContainerSize    = enums.keaHotspotContainerSize.MEDIUM
                            elif hotspotWidth >= 490 and hotspotWidth <= 526 and hotspotHeight >= 158 and hotspotHeight <= 198:
                                hotspotContainerSize    = enums.keaHotspotContainerSize.LARGE
                            else:
                                hotspotContainerSize    = enums.keaHotspotContainerSize.DEFAULT
                            
                            writeToLog("INFO", "The size of: " + hotspotTitle + " is: width: " + str(hotspotWidth) + " height: " + str(hotspotHeight) + " resulting in: " + hotspotContainerSize.value)
                            
                            hotspotStyleFontColor       = hotspotStyleProperties[hotspotStyleProperties.index('color:')+1].replace(';','')
                            hotspotStyleFontSize        = hotspotStyleProperties[hotspotStyleProperties.index('font-size:')+1].replace('px;','')
                            hotspotStyleBorderRadius    = hotspotStyleProperties[hotspotStyleProperties.index('border-radius:')+1].replace('px;','')
                            hotspotStyleBackgroundColor = ''.join(hotspotStyleProperties[hotspotStyleProperties.index('background:')+1:hotspotStyleProperties.index('none')])
                            
                            hotspotLocation             = presentedHotspots[x].location
                            # Verify the location for normal hotspots
                            if hotspotTitle.count('Duplicated') == 0:
                                if hotspotLocation == {'x': 787, 'y': 0} or hotspotLocation == {'x': 786, 'y': 1} or hotspotLocation == {'x': 785, 'y': 2}:
                                    hotspotLocation = enums.keaLocation.TOP_RIGHT
                                
                                elif hotspotLocation == {'x': 7, 'y': 0} or hotspotLocation == {'x': 6, 'y': 1}:
                                    hotspotLocation = enums.keaLocation.TOP_LEFT
                                    
                                elif hotspotLocation == {'x': 394, 'y': 270} or hotspotLocation == {'x': 395, 'y': 270} or hotspotLocation == {'x':439, 'y':270} or hotspotLocation == {'x':230, 'y':270}:
                                    hotspotLocation = enums.keaLocation.CENTER
                                    
                                elif hotspotLocation == {'x': 787, 'y': 419} or hotspotLocation == {'x': 786, 'y': 419} or hotspotLocation == {'x': 785, 'y': 419}:
                                    hotspotLocation = enums.keaLocation.BOTTOM_RIGHT
                                    
                                elif hotspotLocation == {'x': 6, 'y': 419} or hotspotLocation == {'x': 7, 'y': 419}:
                                    hotspotLocation = enums.keaLocation.BOTTOM_LEFT
                                else:
                                    writeToLog("INFO", "FAILED, couldn't find a match with the kea location for " + hotspotTitle + "  while using the following coordinates, X:" + str(hotspotLocation['x']) + " and Y:" + str(hotspotLocation['y']))
                                    return False
                            
                            # Verify the location for duplicated hotspots
                            elif hotspotTitle.count('Duplicated') == 1:
                                if hotspotLocation == {'x': 786, 'y': 24} or hotspotLocation == {'x': 785, 'y': 25}:
                                    hotspotLocation = enums.keaLocation.TOP_RIGHT
                                
                                elif hotspotLocation == {'x': 6, 'y': 24}:
                                    hotspotLocation = enums.keaLocation.TOP_LEFT
                                    
                                elif hotspotLocation == {'x': 394, 'y': 270} or hotspotLocation == {'x': 395, 'y': 270} or hotspotLocation == {'x':439, 'y':270} or hotspotLocation == {'x':230, 'y':270}:
                                    hotspotLocation = enums.keaLocation.CENTER
                                    
                                elif hotspotLocation == {'x': 786, 'y': 419} or hotspotLocation == {'x': 785, 'y': 419}:
                                    hotspotLocation = enums.keaLocation.BOTTOM_RIGHT
                                    
                                elif hotspotLocation == {'x': 6, 'y': 419}:
                                    hotspotLocation = enums.keaLocation.BOTTOM_LEFT
                                else:
                                    writeToLog("INFO", "FAILED, couldn't find a match with the kea location for " + hotspotTitle + "  while using the following coordinates, X:" + str(hotspotLocation['x']) + " and Y:" + str(hotspotLocation['y']))
                                    return False
                                
                                try:
                                    # Hide the main hotspot in order to be able to verify the link for the duplicated one
                                    mainHotspotIndex = 0
                                    hotspotTitleMain = hotspotTitle.replace(' Duplicated','')
                                    for x in range(0, len(presentedHotspots)):
                                        if presentedHotspots[x].text == hotspotTitleMain:
                                            mainHotspotIndex = x
 
                                    self.driver.execute_script("arguments[0].setAttribute('style','display:none;')", presentedHotspots[mainHotspotIndex])
                                    sleep(0.5)
                                except:
                                    pass
                                              
                            if self.clickElement(presentedHotspots[x]) == False:
                                writeToLog("INFO", "FAILED to click on the hotspot: " + hotspotTitle)
                                return False
                            else:
                                sleep(0.1)
                                if self.wait_while_not_visible(self.PLAYER_SCREEN_LOADING_SPINNER, 30) == False:
                                    writeToLog("INFO", "FAILED to load the player screen after clicking on the hotspot" + hotspotTitle)
                                    return False
                            
                            # Take the opened browser tabs
                            handles               = self.driver.window_handles
                            # Declare the hotspot link empty by default and it will be populated in the below code if necessary
                            hotspotLink           = ''
                            hotspotTimeAfterClick = None
                            # Verify if the presented hotspot has a link attached
                            if len(handles) != 1:
                                # Take the hotspot link
                                try:
                                    self.driver.switch_to.window(handles[1])
                                    sleep(5)
                                    hotspotLink = self.clsCommon.base.driver.current_url
                                    self.driver.close()
                                    self.driver.switch_to.window(handles[0])
                                    self.verifyAndClickOnPlay(location, 2, embed)
                                except Exception:
                                    writeToLog("INFO", "FAILED to take the presented link for " + hotspotTitle)
                                    return False
                            else:
                                # Take the entry current time after clicking on the hotspot, in order to verify if we have a time stamp link
                                hotspotTimeAfterClick        = self.returnEntryCurrentTimeInSeconds()
                                                    
                                # Verify if the hotspot link had a Time Stamp link
                                if hotspotStartTime != hotspotTimeAfterClick:
                                    timeLengthBetweenHotspotPresentedAndTimeLink = hotspotTimeAfterClick - hotspotStartTime
                                    # if there's only one second difference, no hotspot time link will be added
                                    if timeLengthBetweenHotspotPresentedAndTimeLink != 1:
                                        hotspotLink = hotspotTimeAfterClick
                                    
                                    
                                # Return an empty string if no Web Page or Time Stamp was provided
                                else:
                                    hotspotLink = ''
                            
                            if hotspotTitle.count('Duplicated') == 1:
                                try:
                                    self.driver.execute_script("arguments[0].setAttribute('style','display;')", presentedHotspots[mainHotspotIndex])
                                    sleep(0.5)
                                except:
                                    pass
                            
                            # Take the element index from the presentedHotspotList
                            presentedNumber = x
                            
                            # Verify for how much time the hotspot is presented
                            isStillPresented = True
                            while self.wait_element(self.PLAYER_REPLAY_BUTTON_CONTROLS_CONTAINER, 0.1, True) == False and isStillPresented == True:
                                # Verify if we had a hotspot that linked to a negative value of its time of display
                                if hotspotTimeAfterClick != None and hotspotTimeAfterClick < hotspotStartTime:
                                    startTimeResumed = 0
                                    # Wait until the hotspot that linked backwards is re displayed
                                    while startTimeResumed <= hotspotStartTime:
                                        startTimeResumed = self.returnEntryCurrentTimeInSeconds()
                                        
                                currentPresentedHotspots = self.wait_elements(self.PLAYER_HOTSPOT_PRESENTED, 0.1)
                                
                                # Verify if there are any hotspot available during the current time
                                if currentPresentedHotspots == False:
                                    isStillPresented = False
                                
                                try:
                                    # Verify for how much time the selected hotspot is displayed
                                    for x in range(0, len(currentPresentedHotspots)):
                                        # Verify that the hotspot that was found is still present on the screen
                                        if currentPresentedHotspots[x]._id == presentedHotspots[presentedNumber]._id:
                                            hotspotEndTime = self.returnEntryCurrentTimeInSeconds()
                                            break
                                        
                                        # Verify that the hotspot that was found is no longer present
                                        else:
                                            if x + 1 == len(currentPresentedHotspots):
                                                isStillPresented = False
                                                break
                                except TypeError:
                                    continue

                            # Create a list that contains all the details necessary for the hotspot verification
                            presentedHotspotDetails     = [hotspotTitle, hotspotLocation, hotspotStartTime, hotspotEndTime, hotspotLink, hotspotStyleFontWeight, hotspotStyleFontColor, hotspotStyleBackgroundColor, int(hotspotStyleFontSize), int(hotspotStyleBorderRadius), hotspotContainerSize]
                            presentedHotspotsDetailsList.append(presentedHotspotDetails)
                            presentedHotspotsNameList.append(hotspotTitle)
                            hotspots = "\n".join(presentedHotspotsNameList)
                            hotspotDetailsString = "".join(str(presentedHotspotDetails))
                            writeToLog("INFO", "The following hotspot: " + hotspotTitle + ", has been successfully added inside the presented hotspot list with the following details:\n" + hotspotDetailsString)
                            
                            # Check if we reached the end of the player
                            if self.wait_element(self.PLAYER_REPLAY_BUTTON_CONTROLS_CONTAINER, 0.1, True) != False:
                                writeToLog("INFO", "All of the following hotspots were found and added inside the list:\n" + hotspots)
                                break
                            
                            # Continue the playing process in order to take the details for the next available new hotspots
                            if self.setPlayerAtSecondZero() == False:
                                return False
                            
                            break
                    # This try catch help us when the element details are no longer available in DOM
                    except StaleElementReferenceException:
                        pass
                
        # Verify the expected hotspots properties with the presented hotspots properties
        for hotspotNumber in hotspotsDict:
            # Take the details for the iterated hotspot from the given dictionary
            currentExpectedList = hotspotsDict[hotspotNumber]
            
            if len(presentedHotspotsDetailsList) < len(hotspotsDict):
                writeToLog("INFO", "FAILED, a number of minimum " + str(len(hotspotsDict)) + " hotspots were expected and only " + str(len(presentedHotspotsDetailsList)) + " were found")
                return False
            
            # Verify the expected hotspots with presented hotspots
            for x in range(0, len(presentedHotspotsDetailsList)):
                currentPresentedList = presentedHotspotsDetailsList[x]
                
                # Verify that the presented hotspot title matches with the expected hotspot title
                if currentExpectedList[0] == currentPresentedList[0]:                    
                    # Set to the list the default value for Font Color if it wasn't set in hotspotDict
                    if currentExpectedList[6] == '':
                        currentExpectedList.insert(6, 'white')
                        currentExpectedList.pop(7)
                    
                    # Set to the list the default value for Background Color if it wasn't set in hotspotDict
                    if currentExpectedList[7] == '':
                        currentExpectedList.insert(7, 'rgba(0,0,0,0.6)')
                        currentExpectedList.pop(8)
                    
                    # Set to the list the default value for Font Size if it wasn't set in hotspotDict
                    if currentExpectedList[8] == '':
                        currentExpectedList.insert(8, 14)
                        currentExpectedList.pop(9)
                    
                    # Set to the list the default value for Border Radius if it wasn't set in hotspotDict
                    if currentExpectedList[9] == '':
                        currentExpectedList.insert(9, 3)
                        currentExpectedList.pop(10)
                        
                    try:
                        if currentExpectedList[10] == '':
                            currentExpectedList.insert(10, enums.keaHotspotContainerSize.DEFAULT)
                            currentExpectedList.pop(11)    
                    except IndexError:
                        currentExpectedList.insert(11, enums.keaHotspotContainerSize.DEFAULT)
                    
                    # Verify that the expected hotspot details, matches with the presented hotspot details
                    if currentExpectedList != currentPresentedList:
                        # Create a list with the inconsitencies between the expected and presented hotspots
                        inconsitencyList = []
                        
                        try:
                            for x in range(len(currentExpectedList)):
                                if currentExpectedList[x] != currentPresentedList[x]:
                                    inconsitencyList.append("FAILED, Expected " + str(currentExpectedList[x]) + " \n Presented " + str(currentPresentedList[x]) + " \n")
                            
                            if len(inconsitencyList) > 1:
                                inconsitencies = "\n".join(inconsitencyList)
                            else:
                                inconsitencies = inconsitencyList[0]
                            
                        except Exception:
                            writeToLog("INFO", "FAILED to take the inconsistency list")
                            
                        presentedHotspotDetailsString = "".join(str(currentPresentedList))
                        expectedHotspotDetailsString  = "".join(str(currentExpectedList))
                        writeToLog("INFO", "LIST for presented hotspot: " + presentedHotspotDetailsString + "\n LIST For expected hotspot: "  + expectedHotspotDetailsString)
                        writeToLog("INFO", "FAILED, the following inconsistencies were noticed for " + currentPresentedList[0] +" hotspot " + str(inconsitencies))
                        return  False
                    else:
                        writeToLog("INFO", "The hotspot:" + currentExpectedList[0] + " has been successfully presented")
                        break
                
                # Verify that the expected hotspot was found within the number of available presented hotspots
                if x + 1 == len(presentedHotspotsDetailsList):
                    writeToLog("INFO", "FAILED to find the " + currentExpectedList[0] + " inside the presented hotspot list: " + hotspots)
                    return False
        
        # Create a list with the successfully verified hotspots
        expectedHotspotNameList = []
        for hotspotNumber in hotspotsDict:
            expectedHotspotNameList.append(hotspotsDict[hotspotNumber][0])
        
        if len(expectedHotspotNameList) > 1:   
            hotspots = "\n".join(expectedHotspotNameList)
        else:
            hotspots = expectedHotspotNameList[0]
        
        writeToLog("INFO","The following hotspots were properly presented:\n" + hotspots)
        return True
    

    # @Author: Horia Cus
    # This function will resume a played entry back second zero and and start the playing process
    def setPlayerAtSecondZero(self, startPlayBack=True):
        # Stop the entry to the current location
        if self.wait_element(self.PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER, 0.2, True) == False:       
            if self.click(self.PLAYER_PAUSE_BUTTON_CONTROLS_CONTAINER, 1, True) == False:
                writeToLog("INFO", "FAILED to pause the video")
                return False
            
        timmerElement = self.wait_element(self.PLAYER_TIMMER_BUTTON_CONTROLS_CONTAINER, 1, True)
        # Take the number of pixels that needs to be moved backwards in order to reach second zero
        timmerElementPixelsToBeMoved = timmerElement.location['x']
        
        # Verify that we were able to find the timmer element
        if timmerElement == False:
            writeToLog("INFO", "FAILED to take the timmer elements")
            return False

        # Move the time control button to second zero
        try:
            ActionChains(self.driver).drag_and_drop_by_offset(timmerElement, -timmerElementPixelsToBeMoved, 0).release().pause(1).perform()
        except MoveTargetOutOfBoundsException:
            pass
        
        if startPlayBack == True:
            # Resume the playing process
            if self.click(self.PLAYER_PLAY_BUTTON_CONTROLS_CONTAINER, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the play button")
                return False
            
            if self.wait_while_not_visible(self.PLAYER_SCREEN_LOADING_SPINNER, 35) == False:
                writeToLog("INFO", "FAILED to load the video after it was resumed from the beginning")
                return False
        
        return True
    
    
    # @Author: Inbar Willman
    # This function verify the correct number of attempts is displayed before and after answering quiz when 'allow multiple attempts' is enabled
    # AllAttempsList - List of dictionaries - each dictionary represent the questions and answers for each attempt
    # expectedQuizScore = List of string: each string represent the current score (individual) of each attempt
    # totalGivenAttempts = int: The total given number of attempts
    # expectedAttemptGeneralScore = List of string: each string represent the total score after each attempts based on the score type
    # scoreType = enum.playerQuizScoreType: Represent the score type (Latest, Highest, Average, Lowest, First)
    def verifyQuizAttempts(self, AllAttempsList, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore='', embed=False, verifySubmittedScreenDict='', expectedQuestionsStateDict='', totalGivenAttempts='', expectedAttemptGeneralScore='', scoreType='', showScore=True):
        for i in range(0,len(AllAttempsList)):
            expectedNumberOfAttemptsWelcomeSreen = totalGivenAttempts - i
            currentNumberOfAttemptsSubmittedScreen = i + 1 
            # If we have expected quiz score and we ant to verify quiz score
            if len(expectedQuizScore) > 0:
                tmpExpectedQuizScore = expectedQuizScore[i]    
                tmpExpectedAttemptGeneralScore = expectedAttemptGeneralScore[i]        
            else:
                tmpExpectedQuizScore =  expectedQuizScore    
                tmpExpectedAttemptGeneralScore = expectedAttemptGeneralScore
                
            if self.answerQuiz(AllAttempsList[i], skipWelcomeScreen, submitQuiz, location, timeOut, tmpExpectedQuizScore, embed, verifySubmittedScreenDict, expectedQuestionsStateDict, expectedNumberOfAttemptsWelcomeSreen, currentNumberOfAttemptsSubmittedScreen, totalGivenAttempts, tmpExpectedAttemptGeneralScore, scoreType, showScore) == False:
                writeToLog("INFO", "FAILED to answer quiz")
                return False 
            
            # If we aren't in the last attempt click on 'take the quiz again'
            if i != len(AllAttempsList) - 1:
                if self.click(self.PLAYER_SUBMITTES_SCREEN_TAKE_THE_QUIZ_AGAIN_BTN) == False:
                    writeToLog("INFO", "FAILED to click on 'Take the quiz again' button")
                    return False  
            # If we are in the last attempt verify that 'take the quiz again isn't display
            else:
                if self.wait_element(self.PLAYER_SUBMITTES_SCREEN_TAKE_THE_QUIZ_AGAIN_BTN) == True:
                    writeToLog("INFO", "FAILED: 'Take the quiz again' button is display after the last attempt")
                    return False
                
                if self.initiateQuizPlayback(location, timeOut, skipWelcomeScreen, embed, 0) == False:
                    writeToLog("INFO", "FAILED to display correct welcome screen")
                    return False 
                                   
            i = i + 1

        return True
    

    # @Author: Horia Cus
    # This function will play the entry using the time cue point from the comment section
    # Verification works only for entries of maximum 55 seconds
    # timeSecondLocation = must contain an integer with the second from where you want to start the video (e.g 10 )
    def clickAndVerifyCommentTimeStamp(self, timeStampInSeconds):
        self.switch_to_default_content()
        
        # Take the comment elements
        presentedComments = self.wait_elements(self.clsCommon.entryPage.ENTRY_PAGE_COMMENT_TEXT_SECTION, 30)
        
        # Verify that at least one comment is presented
        if len(presentedComments) == 0:
            writeToLog("INFO", "FAILED to find any comments available for the entry")
            return False
        
        # Create the locator for our time location
        timeCommentCuePointLocator = (self.clsCommon.entryPage.ENTRY_PAGE_COMMENT_TIME_STAMP[0], self.clsCommon.entryPage.ENTRY_PAGE_COMMENT_TIME_STAMP[1].replace('TIME_INTEGER', str(timeStampInSeconds)))
        
        # Take the element for our time location
        commentTimeLocationElement = self.wait_element(timeCommentCuePointLocator, 1, True)
        
        # Verify that the element for our time location was found
        if commentTimeLocationElement == False:
            writeToLog("INFO", "FAILED to find any comment that has a time cue point at the second " + str(timeStampInSeconds))
            return False
        else:
            # Click on the comment time cue point
            if self.clickElement(commentTimeLocationElement) == False:
                writeToLog("INFO", "FAILED to click on the comment cue point from second " + str(timeStampInSeconds))
                return False
            sleep(0.2)
            
            # Wait until the video starts to plays
            if self.wait_while_not_visible(self.PLAYER_SCREEN_LOADING_SPINNER, 30) == False:
                writeToLog("INFO", "FAILED to load the video")
                return False
            self.switchToPlayerIframe()
            sleep(2)
            # Take the current time of the entry
            try:
                currentRealTime = self.wait_element(self.PLAYER_CONTROLS_CONTAINER_REAL_TIME, 1, True).text
            except Exception:
                writeToLog("INFO", "FAILED to take the entry current time")
                return False
            
            # Verify that the comment cue point launched the entry at the right time
            if int(currentRealTime[2:]) < timeStampInSeconds:
                writeToLog("INFO", "FAILED, the video was moved at " + currentRealTime + " time instead at expected second: " + str(timeStampInSeconds))
                return False
            
        self.switch_to_default_content()
        writeToLog("INFO", "The entry was played successfully at second " + str(timeStampInSeconds) + " while using comment cue point")
        return True
    
    
    # @Author: Horia Cus
    # This function will convert the mm:ss format and return it an integer that contains the entry time in seconds
    def returnEntryCurrentTimeInSeconds(self,):
        self.switchToPlayerIframe()
    
        # Take the entry total time details
        try:
            # Take the mm:ss string
            entryTotalTimeInMMSSFormat = self.wait_element(self.PLAYER_CONTROLS_CONTAINER_REAL_TIME, 0.1, True).text
            
            # Split the time in seconds and minutes
            entryInSeconds    = int(entryTotalTimeInMMSSFormat.split(':')[1])
            entryInMinutes    = int(entryTotalTimeInMMSSFormat.split(':')[0])
        except Exception:
            writeToLog("INFO", "FAILED to take the entry time")
            return False
        
        # Increase the value by one if necessary because there may be a gap of one second
        if entryInSeconds % 10 == 4:
            entryInSeconds += 1
            
        elif entryInSeconds == 59:
            entryInSeconds = 0
            entryInMinutes += 1
        
        elif entryInSeconds % 10 ==9:
            entryInSeconds += 1
        
        # Transform the MM:SS format into seconds
        entryTimeInSeconds = entryInMinutes * 60 + entryInSeconds
        
        return entryTimeInSeconds

      
    # @Author: Inbar Willman
    # This function verify the correct number of attempts is displayed after removing last attempt
    # AllAttempsList - List of dictionaries - each dictionary represent the questions and answers for each attempt
    # expectedQuizScore = List of string: each string represent the current score (individual) of each attempt
    # currentAttempt = int - Represent the number of the current attempt that we are in
    # totalGivenAttempts = int: The total given number of attempts
    # expectedAttemptGeneralScore = List of string: each string represent the total score after each attempts based on the score type
    # scoreType = enum.playerQuizScoreType: Represent the score type (Latest, Highest, Average, Lowest, First)
    def verifyQuizAttemptsAfterRemovingLastAttempt(self, AllAttempsList, skipWelcomeScreen=True, submitQuiz=True, location=enums.Location.ENTRY_PAGE, timeOut=3, expectedQuizScore=[], embed=False, verifySubmittedScreenDict='', expectedQuestionsStateDict='', currentAttempt='',totalGivenAttempts='', expectedAttemptGeneralScore=[], scoreType='', showScore=True):
        tmpCurrentAttempt = totalGivenAttempts - (currentAttempt - 1)
        if self.initiateQuizPlayback(location, timeOut, skipWelcomeScreen, embed, tmpCurrentAttempt) == False:
            writeToLog("INFO", "FAILED to verify welcome message")
            return False
        
        if self.click(self.PLAYER_SUBMITTES_SCREEN_TAKE_THE_QUIZ_AGAIN_BTN) == False:
            writeToLog("INFO", "FAILED to click on 'Take the quiz again' button")
            return False  
        
        for i in range(0,len(AllAttempsList)):
            currentAttempt = currentAttempt + i

            currentNumberOfAttemptsSubmittedScreen = currentAttempt
            
            if currentAttempt == 1:
                expectedNumberOfAttemptsWelcomeSreen = totalGivenAttempts   
                 
            elif currentAttempt == totalGivenAttempts:
                expectedNumberOfAttemptsWelcomeSreen = 1
            else:                
                expectedNumberOfAttemptsWelcomeSreen = totalGivenAttempts - (currentAttempt - 1)
                             
            if self.answerQuiz(AllAttempsList[i], skipWelcomeScreen, submitQuiz, location, timeOut, expectedQuizScore[i], embed, verifySubmittedScreenDict, expectedQuestionsStateDict, expectedNumberOfAttemptsWelcomeSreen, currentNumberOfAttemptsSubmittedScreen, totalGivenAttempts, expectedAttemptGeneralScore[i], scoreType, showScore) == False:
                writeToLog("INFO", "FAILED to answer quiz")
                return False 
            
            # If we aren't in the last attempt click on 'take the quiz again'
            if i != len(AllAttempsList) - 1:
                if self.click(self.PLAYER_SUBMITTES_SCREEN_TAKE_THE_QUIZ_AGAIN_BTN) == False:
                    writeToLog("INFO", "FAILED to click on 'Take the quiz again' button")
                    return False  
            else:
                if currentNumberOfAttemptsSubmittedScreen == totalGivenAttempts:
                    if self.wait_element(self.PLAYER_SUBMITTES_SCREEN_TAKE_THE_QUIZ_AGAIN_BTN) == True:
                        writeToLog("INFO", "FAILED: 'Take the quiz again' button is display after the last attempt")
                        return False
                
                    if self.initiateQuizPlayback(location, timeOut, skipWelcomeScreen, embed, 0) == False:
                        writeToLog("INFO", "FAILED to display correct welcome screen")
                        return False 
                else:
                    if self.initiateQuizPlayback(location, timeOut, skipWelcomeScreen, embed, expectedNumberOfAttemptsWelcomeSreen -1) == False:
                        writeToLog("INFO", "FAILED to display correct welcome screen")
                        return False                     
                                   
            i = i + 1

        return True