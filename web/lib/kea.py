import subprocess
from selenium.common.exceptions import StaleElementReferenceException,\
    MoveTargetOutOfBoundsException
import string
try:
    import win32com.client
except:
    pass
import enums
from base import *
import clsTestService
from general import General
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import random


class Kea(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Upload locators:
    #=============================================================================================================
    KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON                                    = ('xpath', "//button[contains(@class,'multiple-options-question-type')]")
    KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON_ACTIVE                             = ('xpath', "//button[contains(@class,'multiple-options-question-type ng-star-inserted active')]")
    KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON_DEFAULT                            = ('xpath', "//button[contains(@class,'multiple-options-question-type active ng-star-inserted')]")
    KEA_ADD_NEW_REFLECTION_POINT_BUTTON                                     = ('xpath', "//button[contains(@class,'reflection-point-question-type')]")
    KEA_ADD_NEW_REFLECTION_POINT_BUTTON_ACTIVE                              = ('xpath', "//button[contains(@class,'reflection-point-question-type ng-star-inserted active')]")
    KEA_ADD_NEW_TRUE_FALSE_QUESTION_BUTTON                                  = ('xpath', "//button[contains(@class,'true-false-question-type')]")
    KEA_ADD_NEW_TRUE_FALSE_QUESTION_BUTTON_ACTIVE                           = ('xpath', "//button[contains(@class,'true-false-question-type ng-star-inserted active')]")
    KEA_ADD_NEW_ADD_QUESTION_TRUE_ANSWER_FIELD                              = ('xpath', "//textarea[@placeholder='Add the CORRECT Answer Here']")
    KEA_ADD_NEW_QUESTION_FALSE_ANSWER_FIELD                                 = ('xpath', "//textarea[@placeholder='Add Additional Answer Here']")
    KEA_ADD_NEW_QUESTION_HINT_AND_WHY_TOGGLE_MENU_BUTTON                    = ('xpath', "//button[@class='menu-button unbutton']")
    KEA_ADD_NEW_QUESTION_HINT_BUTTON                                        = ('xpath', "//button[@class='unbutton menu-item' and contains(text(),'Hint')]")
    KEA_ADD_NEW_QUESTION_WHY_BUTTON                                         = ('xpath', "//button[@class='unbutton menu-item' and contains(text(),'Why')]")
    KEA_ADD_NEW_QUESTION_NUMBER                                             = ('xpath', "//span[@class='question-number']")
    KEA_SELECT_VIDEO_FOR_EDIT                                               = ('xpath', '//a[@class="btn btn-small btn-primary btn-select-media"]')
    KEA_VIDEO_EDITOR_TAB                                                    = ('xpath', "//a[@class='nav-button' and @aria-label='Video Editor']") 
    KEA_VIDEO_EDITOR_TAB_ACTIVE                                             = ('xpath', "//a[@class='nav-button active' and @aria-label='Video Editor']")
    KEA_LAUNCH                                                              = ('xpath', "//i[@class='icon-editor']")
    KEA_COLLAPSE_PANEL_BUTTON                                               = ('xpath', "//button[contains(@class,'show-hide-button show-hide-button--hide') and @aria-label='Collapse Panel']")
    KEA_EXPAND_PANEL_BUTTON                                                 = ('xpath', "//button[contains(@class,'show') and @aria-label='Expand Panel']")
    KEA_COLLAPSED_PLAYER_CONTAINER                                          = ('xpath', "//div[@class='player-components__container']")
    KEA_EXPANDED_PLAYER_CONTAINER                                           = ('xpath', "//div[contains(@class,'player-components-container__expanded')]")
    KEA_EXIT_BUTTON                                                         = ('xpath', "//button[@class='nav-button' and @aria-label='Exit']")
    KEA_MAIN_CONTAINER                                                      = ('xpath', "//div[@class='kea-main-container']")
    KEA_MAIN_CONFIRMATION_POP_UP                                            = ('xpath', "//div[contains(@class,'ui-widget-content ui-corner-all ui-shadow')]")
    KEA_MAIN_CONFIRMATION_POP_UP_SURE_BUTTON                                = ('xpath', "//span[@class='ui-button-text ui-clickable' and contains(text(),'m sure')]")
    KEA_MAIN_CONFIRMATION_POP_UP_CANCEL_BUTTON                              = ('xpath', "//button[contains(@class,'link--cancel') and contains(text(),'Cancel')]")
    KEA_APP_DISPLAY                                                         = ('id', 'kea-anchor')
    KEA_TAB_TITLE                                                           = ('xpath', "//h1[contains(@class,'title') and contains(text(),'TAB_NAME')]")
    KEA_IFRAME                                                              = ('xpath', '//iframe[@class="span12 hostedEnabled kea-frame kea-iframe-js"]')
    KEA_QUIZ_PLAYER                                                         = ('id', 'quiz-player_ifp')
    KEA_LOADING_SPINNER                                                     = ('class_name', 'spinner')
    KEA_LOADING_CONTAINER                                                   = ('xpath', "//div[contains(@class,'loading__container')]") 
    KEA_MEDIA_IS_BEING_PROCESSED                                            = ('xpath', "//div[@class='kErrorMessageText' and text()='Please wait while media is processing']") 
    KEA_QUIZ_QUESTION_FIELD                                                 = ('id', 'questionTxt')
    KEA_QUIZ_ANSWER                                                         = ('id', 'ANSWER_NUMBER')
    KEA_QUIZ_ANSWER_GENERAL                                                 = ('xpath', "//textarea[contains(@id,'answer-text')]") 
    KEA_EDITOR_TAB                                                          = ('xpath', "//a[@aria-label='Video Editor']") 
    KEA_QUIZ_TAB                                                            = ('xpath', "//a[@class='nav-button' and @aria-label='Quiz']") 
    KEA_QUIZ_TAB_ACTIVE                                                     = ('xpath', "//a[@class='nav-button active' and @aria-label='Quiz']") 
    KEA_QUIZ_ADD_ANSWER_BUTTON                                              = ('xpath', '//div[@class="add-answer-btn"]') 
    KEA_QUIZ_BUTTON                                                         = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="BUTTON_NAME"]')
    KEA_QUIZ_SHUFFLE_BUTTON                                                 = ('xpath', '//div[@class="shuffle-answers"]')
    KEA_QUIZ_LOADING_CONTAINER                                              = ('xpath', '//div[@class="loading-backdrop show ng-star-inserted"]')
    EDITOR_TABLE                                                            = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]')
    EDITOR_TABLE_SIZE                                                       = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]/tbody/tr')
    EDITOR_NO_MORE_MEDIA_FOUND_MSG                                          = ('xpath', '//div[@id="quizMyMedia_scroller_alert" and text()="There are no more media items."]')
    EDITOR_TIMELINE                                                         = ('xpath', '//div[@class="kea-timeline-playhead" and @style="transform: translateX(PIXELpx);"]')
    EDITOR_TIME_PICKER                                                      = ('xpath', "//input[@class='ui-inputtext ui-corner-all ui-state-default ui-widget ui-state-filled']")
    EDITOR_TIME_PICKER_HIGHLIGHTED_CONTAINER                                = ('xpath', "//p-inputmask[@id='jump-to__input' and contains(@class,'focus')]")
    EDITOR_REALTIME_MARKER                                                  = ('xpath', "//span[@class='realtime-marker__head-box-time']")
    EDITOR_REALTIME_MARKER_CONTAINER                                        = ('xpath', "//div[contains(@class,'realtime-marker realtime-marker--sticky realtime-marker--no-box')]")
    EDITOR_TIMELINE_OPTION_RESET                                            = ('xpath', "//button[@aria-label='Reset']")
    EDITOR_TIMELINE_OPTION_UNDO                                             = ('xpath', "//button[@aria-label='Undo']")
    EDITOR_TIMELINE_OPTION_REDO                                             = ('xpath', "//button[@aria-label='Redo']")
    EDITOR_TIMELINE_SET_IN                                                  = ('xpath', "//i[contains(@class,'kicon-pin_left')]")
    EDITOR_TIMELINE_SET_OUT                                                 = ('xpath', "//i[contains(@class,'kicon-pin_right')]")
    EDITOR_TIMELINE_SPLIT_ICON                                              = ('xpath', "//button[@aria-label='Split']")
    EDITOR_TIMELINE_DELETE_BUTTON                                           = ('xpath', "//button[@aria-label='Delete']")
    EDITOR_SAVE_BUTTON                                                      = ('xpath', "//button[@class='button--save ui-button-secondary default-button button--editor ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
    EDITOR_SAVE_A_COPY_BUTTON                                               = ('xpath', "//button[@class='save-as-button branded-button button--editor ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only ng-star-inserted']")
    EDITOR_SAVE_BUTTON_CONF                                                 = ('xpath', "//button[@class='button modal-footer-buttons__save branded-button ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
    EDITOR_SAVED_MSG                                                        = ('xpath', "//strong[contains(.,'Media was successfully saved.')]")
    EDITOR_SAVED_OK_MSG                                                     = ('xpath', "//button[contains(.,'OK')]")
    EDITOR_CREATE_BUTTON                                                    = ('xpath', "//button[contains(.,'Create')]")
    EDITOR_SUCCESS_MSG                                                      = ('xpath', "//p-header[contains(.,'Success')]")
    EDITOR_TOTAL_TIME                                                       = ('xpath', "//span[@class='total-time']")
    EDITOR_TOTAL_TIME_TOOLBAR                                               = ('xpath', "//span[contains(@class,'toolbar__total-time')]")
    EDITOR_GO_TO_MEDIA_PAGE_BUTTON                                          = ('xpath', "//a[contains(.,'Media Page')]")
    EDITOR_SEARCH_X_BUTTON                                                  = ('xpath', "//i[@class='v2ui-close-icon']")
    KEA_EDITOR_MEDIA_DETAILS_SECTION                                        = ('xpath', "//div[@class='media-details-pane']")
    KEA_EDITOR_MEDIA_DETAILS_CONTAINER                                      = ('xpath', "//div[contains(@class,'media-details-container')]")
    KEA_ENTRY_NAME                                                          = ('xpath', "//span[@class='entry-name']")
    KEA_TOGGLE_MENU_OPTION                                                  = ('xpath', "//span[contains(text(),'OPTION_NAME')]")
    KEA_OPTION_NORMAL                                                       = ('xpath', "//label[contains(@class,'ng-star-inserted') and text()='OPTION_NAME']")  
    KEA_OPTION_ACTIVE                                                       = ('xpath', "//label[contains(@class,'ui-label-active') and text()='OPTION_NAME']")
    KEA_OPTION_GRAYED_OUT                                                   = ('xpath', "//label[contains(@class,'ui-label-disabled') and text()='OPTION_NAME']")
    KEA_OPTION_INPUT_FIELD                                                  = ('xpath', "//input[@id='FIELD_NAME']")
    KEA_OPTION_TEXTAREA_FIELD                                               = ('xpath', "//textarea[@id='FIELD_NAME']")  
    KEA_PREVIEW_ICON                                                        = ('xpath', "//i[@class='kicon-preview']") 
    KEA_LOADING_SPINNER_CONTAINER                                           = ('xpath', "//div[@class='spinner-container']")
    KEA_LOADING_SPINNER_QUIZ_PLAYER                                         = ('xpath', "//div[@id='loadingSpinner_quiz-player']") 
    KEA_PREVIEW_PLAY_BUTTON                                                 = ('xpath', "//a[@class='icon-play  comp largePlayBtn  largePlayBtnBorder']")
    KEA_PREVIEW_CLOSE_BUTTON                                                = ('xpath', '//i[contains(@class,"kCloseBtn")]')   
    KEA_IFRAME_PREVIEW_PLAYER                                               = ('xpath', "//iframe[@class='ng-star-inserted' and contains(@src,'iframeembed=true&playerId=kaltura_player')]")
    KEA_IFRAME_BLANK                                                        = ('xpath', "//iframe[@title='Kaltura Editor Application']")  
    KEA_QUIZ_OPTIONS_REVERT_TO_DEFAULT_BUTTON                               = ('xpath', "//button[@class='link-button pull-right ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
    KEA_TIMELINE_SECTION_CONTAINER                                          = ('xpath', "//div[@class='markers-container']")
    KEA_TIMELINE_SECTION_QUESTION_BUBBLE_CONTAINER                          = ('xpath', "//div[@class='kea-timeline-stacked-item kea-timeline-cuepoint']")
    KEA_TIMELINE_SECTION_QUESTION_BUBBLE                                    = ('xpath', "//i[@class='kicon-quiz-cuepoint-inner']")
    KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE                              = ('xpath', "//p[@class='question-tooltip__content']")
    KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_NUMBER                    = ('xpath', "//span[@class='question-tooltip__header__content']")
    KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_TIMESTAMP                 = ('xpath', "//span[@class='question-tooltip__header__duration']")
    KEA_TIMELINE_SECTION_TOTAL_QUESTION_NUMBER                              = ('xpath', "//span[@class='ng-tns-c14-1 ng-star-inserted' and contains(text(),'Total Q: QUESTION_NUMBER')]")
    KEA_TIMELINE_PRESENTED_SECTIONS                                         = ('xpath', "//div[contains(@class,'kea-timeline-stacked-item') and contains(@style,'background-image')]")
    KEA_TIMELINE_SECTION_DRAG_HAND                                          = ('xpath', "//div[@class='answer-drag-handle']")
    KEA_PLAYER_CONTROLS_PLAY_BUTTON                                         = ('xpath', "//button[@class='player-control player-control__play-pause' and @aria-label='Play']")       
    KEA_PLAYER_CONTROLS_PAUSE_BUTTON                                        = ('xpath', "//button[@class='player-control player-control__play-pause' and @aria-label='Pause']")
    KEA_PLAYER_CONTROLS_NEXT_ARROW_BUTTON                                   = ('xpath', "//span[@class='arrows arrow-next']") 
    KEA_PLAYER_CONTROLS_PREVIOUS_ARROW_BUTTON                               = ('xpath', "//span[@class='arrows arrow-back']")
    KEA_TIMELINE_CONTROLS_ZOOM_LEVEL_POINTER                                = ('xpath', "//span[@class='ui-slider-handle ui-state-default ui-corner-all ui-clickable ng-star-inserted']")
    KEA_TIMELINE_CONTROLS_ZOOM_LEVEL_POINTER_VALUE                          = ('xpath', "//span[@class='ui-slider-handle ui-state-default ui-corner-all ui-clickable ng-star-inserted' and @style='left: VALUE%;']")
    KEA_TIMELINE_CONTROLS_ZOOM_OUT_BUTTON                                   = ('xpath', "//button[contains(@class,'zoom_button') and @aria-label='Zoom out']")
    KEA_TIMELINE_CONTROLS_ZOOM_IN_BUTTON                                    = ('xpath', "//button[contains(@class,'zoom_button') and @aria-label='Zoom in']")
    KEA_TIMELINE_CONTROLS_ZOOM_IN_TOOLTIP                                   = ('xpath', "//div[@class='ui-tooltip-text ui-shadow ui-corner-all' and text()='Zoom in']")
    KEA_TIMELINE_CONTROLS_PLAY_BUTTON                                       = ('xpath', "//div[contains(@class,'ui-tooltip-text ui-shadow ui-corner-all')]")
    KEA_CONFIRMATION_POP_UP_CONTINUE                                        = ('xpath', "//button[contains(@class,'button') and text()='Continue']")
    KEA_CONFIRMATION_POP_UP_TITLE                                           = ('xpath', "//div[@class='kErrorMessageTitle']")
    KEA_CONFIRMATION_POP_UP_CONTAINER                                       = ('xpath', "//div[@class='kErrorMessage']")
    KEA_CONFIRMATION_POP_UP_CANCEL_BUTTON                                   = ('xpath', "//button[contains(@class,'button--cancel') and text()='Cancel']")
    KEA_CONFIRMATION_POP_UP_OK_BUTTON                                       = ('xpath', "//button[contains(@class,'button--ok') and text()='OK']")
    KEA_HOTSPOTS_URL_INPUT_ERROR                                            = ('xpath', '//div[contains(@class,"url-input")]')
    KEA_HOTSPOTS_TAB                                                        = ('xpath', "//a[@class='nav-button' and @aria-label='Hotspots']") 
    KEA_HOTSPOTS_TAB_ACTIVE                                                 = ('xpath', "//a[@class='nav-button active' and @aria-label='Hotspots']") 
    KEA_HOTSPOTS_ADD_NEW_BUTTON                                             = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="Add Hotspot"]')
    KEA_HOTSPOTS_DONE_BUTTON_ADVANCED_SETTINGS                              = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="Done"]')
    KEA_HOTSPOTS_DONE_BUTTON_NORMAL                                         = ('xpath', '//button[contains(@class,"btn btn-save pull-right")]')
    KEA_HOTSPOTS_SAVE_BUTTON                                                = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="Save"]')
    KEA_HOTSPOTS_SAVE_BUTTON_PARENT                                         = ('xpath', '//button[contains(@class,"ui-button-text-only")]')
    KEA_HOTSPOTS_CANCEL_BUTTON                                              = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="Cancel"]')
    KEA_HOTSPOTS_ADVANCED_SETTINGS                                          = ('xpath', '//button[@class="form-button" and text()="Advanced Settings"]')
    KEA_HOTSPOTS_TOOL_TIP_CREATION_CANCEL_BUTTON                            = ('xpath', '//button[contains(@class,"form-button") and text()="Cancel"]')
    KEA_HOTSPOTS_TOOL_TIP_CREATION_CONTAINER                                = ('xpath', '//div[@class="form-horizontal"]')
    KEA_HOTSPOTS_FORM_TEXT_INPUT_FIELD                                      = ('xpath', '//input[@id="inputText"]')
    KEA_HOTSPOTS_FORM_LINK_INPUT_FIELD                                      = ('xpath', '//input[@id="inputUrl"]')
    KEA_HOTSPOTS_FORM_LINK_INPUT_FIELD_TIME                                 = ('xpath', '//input[@id="jumpTo"]')
    KEA_HOTSPOTS_FORM_LINK_TYPE_URL                                         = ('xpath', "//label[contains(@class,'click-type__label') and text()='URL']")
    KEA_HOTSPOTS_FORM_LINK_TYPE_TIME                                        = ('xpath', "//label[contains(@class,'click-type__label') and text()='Time in this video']")
    KEA_HOTSPOTS_FORM_TEXT_STYLE                                            = ('xpath', '//label[contains(@class,"ui-dropdown-label ui-inputtext")]')
    KEA_HOTSPOTS_FORM_TEXT_STYLE_VALUE                                      = ('xpath', '//span[contains(@class,"ng-star-inserted") and text()="TEXT_STYLE"]')
    KEA_HOTSPOTS_FORM_COLOR                                                 = ('xpath', '//div[@class="sp-preview-inner"]')
    KEA_HOTSPOTS_FORM_COLOR_VALUE                                           = ('xpath', '//input[@class="sp-input"]')
    KEA_HOTSPOTS_FORM_TEXT_SIZE                                             = ('xpath', '//input[@id="textSize"]')
    KEA_HOTSPOTS_FORM_ROUNDNESS                                             = ('xpath', '//input[@id="roundness"]')
    KEA_HOTSPOTS_FORM_LOCATION_X                                            = ('xpath', '//input[@id="position-x"]')
    KEA_HOTSPOTS_FORM_LOCATION_Y                                            = ('xpath', '//input[@id="position-y"]')
    KEA_HOTSPOTS_FORM_SIZE_WIDTH                                            = ('xpath', '//input[@id="size-width"]')
    KEA_HOTSPOTS_FORM_SIZE_HEIGHT                                           = ('xpath', '//input[@id="size-height"]')
    KEA_HOTSPOTS_LIST_HEADER                                                = ('xpath', "//div[@class='panel__header']")
    KEA_HOTSPOTS_LIST_CONTENT                                               = ('xpath', "//div[@class='panel__content']")
    KEA_HOTSPOTS_LIST_PANEL_HOTSPOT                                         = ('xpath', "//kea-hotspots-list-item[contains(@class,'ng-star-inserted')]")
    KEA_HOTSPOTS_PLAYER_BUTTON                                              = ('xpath', "//div[@class='hotspot__button']")
    KEA_HOTSPOTS_PLAYER_HOTSPOT_CONTAINER                                   = ('xpath', "//div[contains(@class,'hotspot__container ui-draggable ui-draggable-handle')]")
    KEA_HOTSPOTS_PLAYER_HOTSPOT_CONTAINER_SELECTED                          = ('xpath', "//div[contains(@class,'selected ui-resizable')]")
    KEA_HOTSPOTS_PLAYER_ADD_HOTSPOT_TOOLTIP                                 = ('xpath', "//span[@class='message__text']")
    KEA_HOTSPOTS_PANEL_ITEM_TITLE                                           = ('xpath', "//div[contains(@class,'panel-item__title')]")
    KEA_HOTSPOTS_PANEL_ITEM_LINK                                            = ('xpath', "//div[contains(@class,'panel-item__link')]")
    KEA_HOTSPOTS_PANEL_MORE_HAMBURGER_MENU                                  = ('xpath', "//i[@class='kicon-more']")
    KEA_HOTSPOTS_PANEL_ACTION_MENU_CONTAINER                                = ('xpath', "//div[contains(@class,'hotspot-action ui-menu ui-widget')]")
    KEA_HOTSPOTS_PANEL_ACTION_MENU_DUPLICATE                                = ('xpath', "//span[@class='ui-menuitem-text' and text()='Duplicate']")
    KEA_HOTSPOTS_PANEL_ACTION_MENU_EDIT                                     = ('xpath', "//span[@class='ui-menuitem-text' and text()='Edit']")
    KEA_HOTSPOTS_PANEL_ACTION_MENU_DELETE                                   = ('xpath', "//span[@class='ui-menuitem-text' and text()='Delete']")
    KEA_HOTSPOTS_DELETE_POP_UP_CONFIRMATION_BUTTON                          = ('xpath', "//button[contains(@class,'ng-star-inserted') and text()='Delete Hotspot']")
    KEA_TIMELINE_SECTION_HOTSPOT_CONTAINER                                  = ('xpath', '//div[contains(@class,"kea-timeline-stacked-item kea-timeline-stacked-item--audio-disabled")]')
    KEA_TIMELINE_SECTION_HOTSPOT_DRAG_CONTAINER_RIGHT                       = ('xpath', '//div[contains(@class,"handle--right content-item__handle--selected")]')
    KEA_TIMELINE_SECTION_HOTSPOT_DRAG_CONTAINER_LEFT                        = ('xpath', '//div[contains(@class,"handle--left content-item__handle--selected")]')
    KEA_TIMELINE_SECTION_HOTSPOT_TRIM_EDGE_BUTTONS                          = ('xpath', '//i[contains(@class,"kicon-trim_handle content-item__handle-icon")]')
    KEA_PLAYER_CONTAINER                                                    = ('xpath', '//div[@class="player-container"]')
    KEA_ADD_NEW_OPEN_QUESTION_BUTTON                                        = ('xpath', "//button[contains(@class,'open-question-question-type')]")
    KEA_ADD_NEW_OPEN_QUESTION_BUTTON_ACTIVE                                 = ('xpath', "//button[contains(@class,'open-question-question-type ng-star-inserted active')]")
    KEA_ALLOW_MULTIPLE_ATTEMPTS_OPTION_GRAYED_OUT                           = ('xpath', '//label[@class="ui-chkbox-label ng-star-inserted" and text()="Allow Multiple Attempts"]')
    KEA_NUMBER_OF_ALLOW_ATTEMPTS                                            = ('xpath', '//input[@name="attemptsAllowed"]')
    KEA_SCORE_TYPE_DROP_DOWN                                                = ('xpath', '//label[contains(@class,"ui-dropdown-label ui-inputtext ui-corner-all ng-star-inserted")]')
    KEA_SCORE_TYPE_OPTION                                                   = ('xpath', '//span[contains(@class, "ng-star-inserted") and text()="SCORE_TYPE"]')
    #============================================================================================================
    # @Author: Inbar Willman       
    def navigateToEditorMediaSelection(self, forceNavigate = False):
        # Check if we are already in my media selection page
        if forceNavigate == False:
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MEDIA_SELECTION_URL, False, 1) == True:
                writeToLog("INFO","Success Already in media selection page")
                return True
        
        # Click on add new drop down
        if self.clsCommon.upload.addNewVideoQuiz() == False:
            writeToLog("INFO","Failed to navigate to media selection page")
            return False           
        
        return True
    
    
    # @Author: Inbar Willman    
    # This method search for entry in media selection page and then opening KEA for the selected entry
    def searchAndSelectEntryInMediaSelection(self, entryName, forceNavigate=True):
        # Navigate to media selection page
        if self.navigateToEditorMediaSelection(forceNavigate) == False:
            return False
        
        # Click on search bar and search for entry
        self.clsCommon.myMedia.getSearchBarElement().click()
        self.clsCommon.myMedia.getSearchBarElement().send_keys('"' + entryName + '"')
        self.clsCommon.general.waitForLoaderToDisappear()
        
        sleep(6)
        
        if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_NO_ENTRIES_FOUND, 1, True) != False:
            writeToLog("INFO", "FAILED to find the " + entryName + " within the first try...")
            sleep(10)
            if self.click(self.EDITOR_SEARCH_X_BUTTON, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the X button in order to clear the search")
                return False
            
            self.clsCommon.general.waitForLoaderToDisappear()
            self.clsCommon.myMedia.getSearchBarElement().click()
            self.clsCommon.myMedia.getSearchBarElement().send_keys('"' + entryName + '"')
            self.clsCommon.general.waitForLoaderToDisappear()
            
        if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_NO_ENTRIES_FOUND, 1, True) != False:
            writeToLog("INFO", "FAILED, the " + entryName + " couldn't be found inside the Editor after two tries")
            return False
        
        # Click on select button in order to open KEA
        if self.click(self.KEA_SELECT_VIDEO_FOR_EDIT) == False:
            writeToLog("INFO","FAILED to select entry and open KEA")
            return False 
        
        sleep(4)   
        
        # Verify that we are in KEA page and app is displayed
        if self.wait_visible(self.KEA_APP_DISPLAY, 40) == False:
            writeToLog("INFO","FAILED to display KEA page")
            return False
        
        if self.wait_while_not_visible(self.KEA_LOADING_CONTAINER, 60) == False:
            writeToLog("INFO", "FAILED to wait until the KEA Loading container disappeared")
            return False            
        
        return True
    
    
    # @Author: Inbar Willman    
    def startQuiz(self):
        self.switchToKeaIframe()
        # Click start button to start quiz
        if self.keaQuizClickButton(enums.KeaQuizButtons.START) == False:
            writeToLog("INFO","FAILED to click start quiz")
            return False  
        
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 50) == False:
            writeToLog("INFO","FAILED to wait until spinner isn't visible")
            return False   
         
        return True
    
    
    # @Author: Inbar Willman   
    def addQuizQuestion(self, questionText, answerText, additionalAnswerList): 
#         if self.startQuiz() == False:
#             writeToLog("INFO","FAILED to click start quiz")
#             return False 
        
        sleep(60)
                     
        self.switchToKeaIframe()    
           
        # Enter in 'Multiple Choice' KEA Quiz Question screen
        if self.selectQuestionType(enums.QuizQuestionType.Multiple) == False:
            writeToLog("INFO", "FAILED to enter in " + enums.QuizQuestionType.Multiple.value + " Quiz Question screen")
            return False             
 
        # Add question fields
        if self.fillQuizFields(questionText, answerText, additionalAnswerList) == False:
            writeToLog("INFO","FAILED to fill question fields")
            return False 
         
        # Save Question
        if self.saveQuizChanges() == False:
            writeToLog("INFO", "FAILED to save the changes")
            return False
         
        return True
    
    
    # @Author: Inbar Willman
    def switchToKeaIframe(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.KEA:
            return True
        else:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KEA
            self.swith_to_iframe(self.KEA_IFRAME)
            return True
    
            
    # @Author: Inbar Willman
    def switchToKeaQuizPlayer(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.KEA_QUIZ_PLAYER:
            return True
        else:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KEA_QUIZ_PLAYER
            self.swith_to_iframe(self.KEA_QUIZ_PLAYER)
            return True
            
    
    # @Author: Inbar Willman  
    def keaQuizClickButton(self, buttonName): 
        tmpButton = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', buttonName.value))
        if self.wait_visible(tmpButton, 60, True) == False:
            writeToLog("INFO", "FAILED to display " + buttonName.value + " button")
            return False
        
        if self.click(tmpButton) == False:
            writeToLog("INFO","FAILED to click on " + buttonName.value + " button")
            return False
        
        return True
    
    
    # @Author: Inbar Willman
    def fillQuizFields(self, questionText, answerText, additionalAnswerList=''):   
        # Fill question text 
        if self.click(self.KEA_QUIZ_QUESTION_FIELD) == False:
            writeToLog("INFO","FAILED to click on question text field")
            return False
         
        if self.send_keys(self.KEA_QUIZ_QUESTION_FIELD, questionText) == False:
            writeToLog("INFO","FAILED to fill question field")
            return False
         
        # Fill First answer
        tmpFirstAnswer = (self.KEA_QUIZ_ANSWER[0], self.KEA_QUIZ_ANSWER[1].replace('ANSWER_NUMBER', 'answer-text0'))
        if self.click(tmpFirstAnswer) == False:
            writeToLog("INFO","FAILED to click on first answer text field")
            return False
        if self.send_keys(tmpFirstAnswer, answerText) == False:
            writeToLog("INFO","FAILED to fill first answer text field")
            return False
        
        # We verify if we want to user additional answers
        if additionalAnswerList != '':
            # Fill second answer if there are just two answers
            if len(additionalAnswerList) == 1:
                tmpSecondAnswer = (self.KEA_QUIZ_ANSWER[0], self.KEA_QUIZ_ANSWER[1].replace('ANSWER_NUMBER', 'answer-text1'))
                if self.click(tmpSecondAnswer) == False:
                    writeToLog("INFO","FAILED to click on second answer text field")
                    return False
                if self.send_keys(tmpSecondAnswer, additionalAnswerList[0]) == False:
                    writeToLog("INFO","FAILED to fill second answer text field")
                    return False                
             
            else:
                i = 1
                for answer in additionalAnswerList:
                    tmpAnswer = (self.KEA_QUIZ_ANSWER[0], self.KEA_QUIZ_ANSWER[1].replace('ANSWER_NUMBER', 'answer-text' + str(i)))
                    if self.click(tmpAnswer) == False:
                        writeToLog("INFO","FAILED to click on " + i +"th answer text field")
                        return False                    
                    if self.send_keys(tmpAnswer, answer) == False:
                        writeToLog("INFO","FAILED to fill " + i +"th answer text field")
                        return False    
                    # Check if in the last answer, if not click add quiz button
                    if len(additionalAnswerList) != i:
                        if self.click(self.KEA_QUIZ_ADD_ANSWER_BUTTON) == False:
                            writeToLog("INFO","FAILED click add answer button")
                            return False                           
                    i = i + 1
                               
        return True
    
    
    # @Author: Inbar Willman
    # After creating quiz, click done.
    # After that there are two options - Click 'Go to media page' or 'Edit Quiz'.
    # Default value is 'Go To Media page'
    def clickDone(self, doneOption=enums.KeaQuizButtons.GO_TO_MEDIA_PAGE):    
        if self.keaQuizClickButton(enums.KeaQuizButtons.DONE) == False:
            writeToLog("INFO","FAILED to click Done button")
            return False 
        
#         if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 30) == False:
#             writeToLog("INFO","FAILED to wait until spinner isn't visible")
#             return False  
# Until we catch the locator of the overlay we are going to use sleep

        sleep(5)

        if doneOption == enums.KeaQuizButtons.GO_TO_MEDIA_PAGE:
            if self.keaQuizClickButton(enums.KeaQuizButtons.GO_TO_MEDIA_PAGE) == False:
                writeToLog("INFO","FAILED to click go to media page button")
                return False
            self.switch_to_default_content()
        elif doneOption == enums.KeaQuizButtons.EDIT_QUIZ:
            if self.keaQuizClickButton(enums.KeaQuizButtons.EDIT_QUIZ) == False:
                writeToLog("INFO","FAILED to click edit quiz button")
                return False
            sleep(3)
        else:
            writeToLog("INFO","FAILED, unknown doneoption: '" + doneOption + "'")
            return False 
         
        sleep (8)   
        return True
    
    # @Author: Inbar Willman
    # The function check and verify that the entries sort in my media are in the correct order 
    def verifySortInEditor(self, sortBy, entriesList): 
        if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.SORT_BY,sortBy) == False:
            writeToLog("INFO","FAILED to sort entries")
            return False
                
        if self.clsCommon.myMedia.showAllEntries(searchIn=enums.Location.EDITOR_PAGE) == False:
            writeToLog("INFO","FAILED to show all entries in editor page")
            return False
        sleep(10)
        
        try:
            entriesInMyMedia = self.wait_visible(self.EDITOR_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False
        entriesInMyMedia = entriesInMyMedia.split("\n")
        
        # run over the list and delete tab before the entry name
        for idx, entry in enumerate(entriesInMyMedia):
            entriesInMyMedia[idx] = entry.lstrip()
                
        if self.clsCommon.myMedia.verifySortOrder(entriesList, entriesInMyMedia) == False:
            writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct")
            return False
        
        writeToLog("INFO","Success, My media sort by '" + sortBy.value + "' was successful")
        return True


    # @Author: Inbar Willman
    # The function check and verify that the entries sort in my media are in the correct order 
    def verifyFiltersInEditor(self, entriesDict, noEntriesExpected=False): 
        if noEntriesExpected == True:
            if self.wait_element(self.clsCommon.myMedia.ENTRY_NO_MEDIA_FOUND_MESSAGE, 1, multipleElements=True) != False:
                writeToLog("INFO", "PASSED, no entries are displayed")
                return True
            else:
                writeToLog("INFO", "Some entries are present, we will verify the dictionaries")
                   
        if self.clsCommon.myMedia.showAllEntries(searchIn=enums.Location.EDITOR_PAGE) == False:
            writeToLog("INFO","FAILED to show all entries in editor page")
            return False
        sleep(10)
        
        try:
            entriesInEditor = self.wait_visible(self.EDITOR_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False
        
        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInAddToChannel == False:
                if (entry.lower() in entriesInEditor) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in editor page although he need to be found")
                    return False
                 
            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInAddToChannel == True:
                if (entry.lower() in entriesInEditor) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in editor page although he doesn't need to be found")
                    return False
                 
        writeToLog("INFO","Success, Only the correct media display in channel - pending tab")
        return True    
    
    
    # @Author: Tzachi guetta
    def launchKEA(self, entryName, navigateTo, navigateFrom, isCreateClippingPermissionIsOn=False):
        if isCreateClippingPermissionIsOn == False:
            if self.clsCommon.navigateTo(navigateTo, navigateFrom, entryName) == False:
                return False 
        
        if navigateTo == enums.Location.EDIT_ENTRY_PAGE:
            if self.click(self.KEA_LAUNCH) == False:
                writeToLog("INFO","FAILED to click on KEA launch button")
                return False
            
        elif navigateTo == enums.Location.ENTRY_PAGE:
            if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
                writeToLog("INFO", "FAILED to wait until the " + entryName + " has been processed")
                return False
            
            self.click(self.clsCommon.entryPage.ENTRY_PAGE_DETAILS_BUTTON)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            sleep(4)
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
                writeToLog("INFO","FAILED to click on Actions button (at entry page)")
                return False
            
            sleep(3.5)
            
            if isCreateClippingPermissionIsOn == True:
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_CREATE_CLIP_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on Actions -> 'Create clip' button (at entry page)")
            else:
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_KEA_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on Actions -> Launch KEA button (at entry page)")
                    return False
            
        # Verify that we are in KEA page and app is displayed
        if self.wait_visible(self.KEA_APP_DISPLAY, 40) == False:
            writeToLog("INFO","FAILED to display KEA page")
            return False 
        
        #sleeping two seconds in order to make sure that the loading screen is no longer present
        sleep(2)   
        if isCreateClippingPermissionIsOn == True:
            if self.verifyEditorForClippingPermission() == False:
                writeToLog("INFO","FAILED to display just relevant editor buttons")
                return False
        sleep(3)
        # We wait until the KEA page is successfully loaded
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 45) == False:
            writeToLog("INFO","FAILED to wait until spinner isn't visible")
            return False
        
        sleep(5)                      
        
        if self.wait_while_not_visible(self.KEA_MEDIA_IS_BEING_PROCESSED, 120) == False:
            writeToLog("INFO", "FAILED to wait until the " + entryName + " has been processed during the launch kea")
            return False
        
        writeToLog("INFO","Success, KEA has been launched for: " + entryName) 
        return True
    

    # @Author: Tzachi guetta
    # interface to KEA's timeline functionalities: split, (Fade IN\out - TBD)
    def editorTimelineActions(self, startTime, endTime='', openEditorTab=False, timelineAction=None):
        self.switchToKeaIframe()            
        if openEditorTab == True:
            if self.click(self.KEA_EDITOR_TAB, 45) == False:
                writeToLog("INFO","FAILED to click on Editor Tab")
                return False
            
        if self.setEditorStartTime(startTime) == False:
            writeToLog("INFO", "FAILED to select the split start point")
            return False                
        sleep(1)
            
        if timelineAction == enums.KeaEditorTimelineOptions.DELETE:
            if self.click(self.EDITOR_TIMELINE_SPLIT_ICON) == False:
                    writeToLog("INFO","FAILED to click Split icon (time-line)")
                    return False
            sleep(1)
            
            if self.setEditorStartTime(endTime) == False:
                return False   
            
            sleep(1)
            if self.click(self.EDITOR_TIMELINE_SPLIT_ICON) == False:
                writeToLog("INFO","FAILED to click Split icon (time-line)")
                return False
            
            sleep(1)
            if self.click(self.EDITOR_TIMELINE_DELETE_BUTTON) == False:
                writeToLog("INFO","FAILED to click delete icon (time-line)")
                return False
        
        elif timelineAction == enums.KeaEditorTimelineOptions.SPLIT:
            if self.click(self.EDITOR_TIMELINE_SPLIT_ICON) == False:
                writeToLog("INFO","FAILED to click Split icon (time-line)")
                return False
            sleep(1)
            
        elif timelineAction == enums.KeaEditorTimelineOptions.SET_IN:
            if self.click(self.EDITOR_TIMELINE_SET_IN, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Set In option")
                return False
            
        elif timelineAction == enums.KeaEditorTimelineOptions.SET_OUT:
            if self.click(self.EDITOR_TIMELINE_SET_OUT, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Set Out option")
                return False
            
        else:
            writeToLog("INFO", "FAILED, please make sure that you used a supported timeline action")
            return False

        writeToLog("INFO", "Timeline section has been successfully " + timelineAction.value + " edited")
        return True
    
    
    # @Author: Oleg Sigalov  
    # Helper method to set the start time in KEA editor, under the left bottom player corner     
    # splitStartTime: String to set the time, example: "00:10" represents 10 seconds
    def setEditorStartTime(self, splitStartTime):
        if self.click(self.EDITOR_TIME_PICKER) == False:
            writeToLog("INFO","FAILED to click on input field")
            return False 
        
        # send_keys doesn't work, use instead:
        self.driver.execute_script("arguments[0].value='" + splitStartTime + "'", self.wait_element(self.EDITOR_TIME_PICKER))
        
        if self.send_keys(self.EDITOR_TIME_PICKER, Keys.ENTER) == False:
            writeToLog("INFO","FAILED to send Enter to input field")
            return False
        
        # Verify marker moved correctly
        markerElement = self.wait_element(self.EDITOR_REALTIME_MARKER)
        if markerElement == False:
            writeToLog("INFO","FAILED to get the marker element")
            return False
            
        if markerElement.text != splitStartTime + ".00":
            writeToLog("INFO","FAILED to set marker to:" + splitStartTime)
            return False  

        return True
    
    
    # @Author: Tzachi guetta  
    # Currently support split only     
    # expectedEntryDuration = the duration of the new entry  
    def trimEntry(self, entryName, startTime, endTime, expectedEntryDuration, navigateTo, navigateFrom, openEditorTab=False, isCreateClippingPermissionIsOn=False, timelineAction=enums.KeaEditorTimelineOptions.DELETE):
        if self.launchKEA(entryName, navigateTo, navigateFrom, isCreateClippingPermissionIsOn) == False:
            writeToLog("INFO","Failed to launch KEA for: " + entryName)
            return False
        sleep(2)
        
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
            self.click(self.clsCommon.kafGeneric.KAF_REFRSH_BUTTON) 
        else:
            self.refresh()
            
        sleep(3)   
        self.switchToKeaIframe()
        sleep(6)

        if self.editorTimelineActions(startTime, endTime, openEditorTab, timelineAction) == False:
            writeToLog("INFO","FAILED to split the entry: " + str(entryName))
            return False            
        
        sleep(1)
        if self.saveEditorChanges(saveCopy=False)== False:
            writeToLog("INFO","FAILED to save the entry changes from KEA Editor Timeline")
            return False
                
        entryDuration = self.get_element_text(self.EDITOR_TOTAL_TIME, 10)
        self.switch_to_default_content()
        
        if expectedEntryDuration in entryDuration:
            writeToLog("INFO","Success,  Entry: " + entryName +", was trimmed, the new entry Duration is: " + expectedEntryDuration) 
            return True
        
        writeToLog("INFO","FAILED,  Entry: " + entryName +", was trimmed, but the new entry Duration is not as expected : " + entryDuration + " instead of :" + expectedEntryDuration) 
        return False
    
    
    # @Author: Horia Cus
    # Show all entries in quiz page   
    def showAllEntriesInAddQuizPage(self, timeOut=60):
        # Get all entries in results
        try:
            tmpResultsList = self.get_elements(self.clsCommon.globalSearch.GLOBAL_SEARCH_ENTRY_RESUTLT_ROW)
            
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries in results")
            return False
        
        if len(tmpResultsList) < 4:
            writeToLog("INFO","Success, All media in global page are displayed")
            return True 
        
        else:      
            self.clsCommon.sendKeysToBodyElement(Keys.END)
            wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)  
            while wait_until > datetime.datetime.now():                       
                if self.is_present(self.clsCommon.globalSearch.GLOBAL_SEARCH_NO_RESULTS_ALERT_QUIZ, 2) == True:
                    writeToLog("INFO","Success, All media in global page are displayed")
                    sleep(1)
                    # go back to the top of the page
                    self.clsCommon.sendKeysToBodyElement(Keys.HOME)
                    return True 
             
                self.clsCommon.sendKeysToBodyElement(Keys.END)
             
        writeToLog("INFO","FAILED to show all media")
        return False
    
    
    # @Author: Horia Cus
    # The function check the the entries in my media are filter correctly
    def verifyFiltersInAddQuizPage(self, entriesDict, noEntriesExpected=False):
        if noEntriesExpected == True:
            if self.wait_element(self.clsCommon.myMedia.ENTRY_NO_MEDIA_FOUND_MESSAGE, 1, multipleElements=True) != False:
                writeToLog("INFO", "PASSED, no entries are displayed")
                return True
            else:
                writeToLog("INFO", "Some entries are present, we will verify the dictionaries")
                
        if self.showAllEntriesInAddQuizPage() == False:
            writeToLog("INFO","FAILED to show all entries in global page")
            return False
             
        try:
            # Get list of all entries element in results
            entriesInGlobalPage = self.get_elements(self.clsCommon.globalSearch.GLOBAL_SEARCH_ENTRY_RESUTLT_NAME)
            listOfEntriesInResults = []
            
            # Get text of each entry element and add to a new list
            for entry in entriesInGlobalPage:
                entry.text.lower()
                listOfEntriesInResults.append(entry.text.lower())
                
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list")
            return False
         
        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInMyMedia == False:
                if (entry.lower() in listOfEntriesInResults) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in global page results although he need to be found")
                    return False
                 
            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInMyMedia == True:
                if (entry.lower() in listOfEntriesInResults) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in global page results although he doesn't need to be found")
                    return False
                 
        writeToLog("INFO","Success, Only the correct media display in global page")
        return True    

      
    # @Author: Tzachi guetta  
    # Currently support split only     
    # expectedEntryDuration = the duration of the new entry  
    def clipEntry(self, entryName, startTime, endTime, expectedEntryDuration, navigateTo, navigateFrom, openEditorTab=False, isCreateClippingPermissionIsOn=False, timelineAction=enums.KeaEditorTimelineOptions.DELETE):
        if self.launchKEA(entryName, navigateTo, navigateFrom, isCreateClippingPermissionIsOn) == False:
            writeToLog("INFO","Failed to launch KEA for: " + entryName)
            return False
        sleep(2)
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
            self.click(self.clsCommon.kafGeneric.KAF_REFRSH_BUTTON) 
        else:
            self.refresh()
            
        sleep(3)   
        self.switchToKeaIframe()
        sleep(6)
        
        if self.editorTimelineActions(startTime, endTime, openEditorTab, timelineAction) == False:
            return False
        
        sleep(1)
        
        if self.saveEditorChanges(saveCopy=True) == False:
            writeToLog("INFO","FAILED to save a copy based on the changes that were performed to the KEA Editor timeline")
            return False
        
        sleep(1)
        if self.click(self.EDITOR_GO_TO_MEDIA_PAGE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'Go to Media Page' button")
            return False
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
            # Set iframe is player, to make sure switchToKAFIframeGeneric() will switch to default and then to KAF iframe
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.PLAYER
            self.clsCommon.kafGeneric.switchToKAFIframeGeneric()
        else:
            self.switch_to_default_content()
        
        if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
            writeToLog("INFO","FAILED to wait Till Media Is Being Processed")
            return False
        
        #If the entry is Quiz, So openEditorTab = True, Then - wait 10sec refresh and wait again
        if openEditorTab == True:
            sleep(10)
            self.refresh()
            sleep(5)
            
        self.clsCommon.player.switchToPlayerIframe()
        entryDuration = self.get_element(self.clsCommon.player.PLAYER_TOTAL_VIDEO_LENGTH).text
        self.switch_to_default_content()
        
        if expectedEntryDuration in entryDuration:
            writeToLog("INFO","Success,  Entry: " + entryName +", was clipped, the new entry Duration is: " + expectedEntryDuration) 
            return True
        
        writeToLog("INFO","FAILED,  Entry: " + entryName +", was clipped, but the new entry Duration is not as expected : " + entryDuration + " instead of :" + expectedEntryDuration) 
        return False


#     def quizCreation(self, entryName, dictQuestions, dictDetails='', dictScores='', dictExperience='', timeout=15):
#         sleep(25)
#         if self.searchAndSelectEntryInMediaSelection(entryName) == False:
#             writeToLog("INFO", "FAILED to navigate to " + entryName)
#             return False
#         sleep(timeout)
#         
#         # We create the locator for the KEA Quiz Question title field area (used only in the "Reflection Point" and "True and False" Quiz Questions)
#         questionField = (self.KEA_OPTION_TEXTAREA_FIELD[0], self.KEA_OPTION_TEXTAREA_FIELD[1].replace('FIELD_NAME', 'questionTxt')) 
#                    
#         for questionNumber in dictQuestions:
#             questionDetails = dictQuestions[questionNumber]
#             
#             self.switchToKeaIframe() 
#             if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 30) == False:
#                 writeToLog("INFO","FAILED to wait until spinner isn't visible")
#                 return False 
#             
#             # Specifying the time stamp, where the Quiz Question should be placed within the entry
#             # click on the editor in order to higlight the timeline field and select all the text
#             if self.click(self.EDITOR_TIME_PICKER, 1, True) == False:
#                 writeToLog("INFO", "FAILED to click on the kea timeline field")
#                 return False
#             
#             timestamp = questionDetails[0]
#             
#             # replace the text present in the timestamp field with the new one
#             if self.send_keys(self.EDITOR_TIME_PICKER, timestamp + Keys.ENTER) == False:
#                 writeToLog("INFO", "FAILED to select the timeline field text")
#                 return False
#         
#             # Creating the variable for the Quiz Question Type
#             qestionType = questionDetails[1]
#             if qestionType == enums.QuizQuestionType.Multiple:   
#                 # We enter in the KEA Quiz Question Type screen
#                 if self.selectQuestionType(qestionType) == False:
#                     writeToLog("INFO", "FAILED to enter in the " + qestionType.value + " Question screen")
#                     return False      
#          
#                 # Add question fields
#                 # We verify if we have only one question
#                 if questionDetails[4] != '':
#                     QuizQuestion1AdditionalAnswers = [questionDetails[4]]
#                 
#                 if questionDetails[5] != '':
#                     QuizQuestion1AdditionalAnswers.append(questionDetails[5])
#                     
#                 if questionDetails[6] != '':
#                     QuizQuestion1AdditionalAnswers.append(questionDetails[6])
#                     
#                 if len(QuizQuestion1AdditionalAnswers) >= 1:
#                     if self.fillQuizFields(questionDetails[2], questionDetails[3], QuizQuestion1AdditionalAnswers) == False:
#                         writeToLog("INFO","FAILED to fill question fields")
#                         return False
#                 else:
#                     writeToLog("INFO", "Please make sure that you supply at least two question answers")
#                     return False
#                 
#                 # we verify if the value for the 'Hint' is present in the list
#                 if len(questionDetails) >= 8:  
#                     # we verify if we want to create a Hint for the current Quiz Question
#                     if questionDetails[7] != '':
#                         if self.createHintAndWhy(questionDetails[7], whyText='') == False:
#                             writeToLog("INFO", "FAILED to create a Hint for the " + questionDetails[2] + " Quiz Question")
#                             return False
#                     else:
#                         writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
# 
#                     # we verify if the value for the 'Why' is present in the list
#                     if len(questionDetails) >= 9:
#                         # we verify if we want to create a Why for the current Quiz Question
#                         if questionDetails[8] != '':
#                             sleep(2)
#                             if self.createHintAndWhy(hintText='', whyText=questionDetails[8]) == False:
#                                 writeToLog("INFO", "FAILED to create a Why for the " + questionDetails[2] + " Quiz Question")
#                                 return False
#                         else:
#                             writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
#                 else:
#                     writeToLog("INFO", "No 'Hint' or 'Why' will be created for the " + questionDetails[2] + " Quiz Question")
#                     
#             elif qestionType == enums.QuizQuestionType.REFLECTION:
#                 # We enter in the KEA Quiz Question Type screen
#                 if self.selectQuestionType(qestionType) == False:
#                     writeToLog("INFO", "FAILED to enter in the " + qestionType.value + " Question screen")
#                     return False    
#                 
#                 # We select the KEA Quiz Question title field
#                 if self.click(questionField, 2, True) == False:
#                     writeToLog("INFO", "FAILED to select the reflection point text area")
#                     return False
#                 
#                 # We insert the title for the KEA Quiz Question type
#                 if self.send_keys(questionField, questionDetails[2], True) == False:
#                     writeToLog("INFO", "FAILED to insert the " + questionDetails[2] + " reflection point")
#                     return False
#                 
#                 # We make sure that no 'Hint' or 'Why' are trying to be created for 'Reflection Point' Quiz Question
#                 if len(questionDetails) >= 4:
#                     writeToLog("INFO", "Hint and Why are not supported for the Reflection Point Quiz Question")
#                     return False
#                 
#             elif qestionType == enums.QuizQuestionType.TRUE_FALSE:
#                 # We enter in the KEA Quiz Question Type screen
#                 if self.selectQuestionType(qestionType) == False:
#                     writeToLog("INFO", "FAILED to enter in the " + qestionType.value + " Question screen")
#                     return False    
#                 
#                 # We select the KEA Quiz Question title field
#                 if self.click(questionField, 2, True) == False:
#                     writeToLog("INFO", "FAILED to select the reflection point text area")
#                     return False
#                 
#                 #we insert the Question title inside the Question text area
#                 if self.send_keys(questionField, questionDetails[2], True) == False:
#                     writeToLog("INFO", "FAILED to insert the " + questionDetails[2] + " reflection point")
#                     return False
#                 
#                 # We insert the title for the KEA Quiz Question type
#                 if questionDetails[3] and questionDetails[4] != '':
#                     if self.click(self.KEA_ADD_NEW_ADD_QUESTION_TRUE_ANSWER_FIELD, 3, True) == False:
#                         writeToLog("INFO", "FAILED to select the 'True' text area field")
#                         return False
# 
#                     if self.clear_and_send_keys(self.KEA_ADD_NEW_ADD_QUESTION_TRUE_ANSWER_FIELD, questionDetails[3], True)== False:
#                         writeToLog("INFO", "FAILED to insert the " + questionDetails[3] + " text within the 'True' field")
#                         return False
#                     
#                     if self.click(self.KEA_ADD_NEW_QUESTION_FALSE_ANSWER_FIELD, 3, True) == False:
#                         writeToLog("INFO", "FAILED to select the 'False' text area field")
#                         return False
# 
#                     if self.clear_and_send_keys(self.KEA_ADD_NEW_QUESTION_FALSE_ANSWER_FIELD, questionDetails[4], True)== False:
#                         writeToLog("INFO", "FAILED to insert the " + questionDetails[4] + " text within the 'False' field")
#                         return False
#                 
#                 # we verify if the value for the 'Hint' is present in the list
#                 if len(questionDetails) >= 6:  
#                     # we verify if we want to create a Hint for the current Quiz Question
#                     if questionDetails[5] != '':
#                         if self.createHintAndWhy(questionDetails[5], whyText='') == False:
#                             writeToLog("INFO", "FAILED to create a Hint for the " + questionDetails[2] + " Quiz Question")
#                             return False
#                     else:
#                         writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
#                         
#                     # we verify if the value for the 'Why' is present in the list
#                     if len(questionDetails) == 7:
#                         # we verify if we want to create a Why for the current Quiz Question
#                         if questionDetails[6] != '':
#                             sleep(2)
#                             if self.createHintAndWhy(hintText='', whyText=questionDetails[6]) == False:
#                                 writeToLog("INFO", "FAILED to create a Why for the " + questionDetails[2] + " Quiz Question")
#                                 return False
#                         else:
#                             writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
#                 else:
#                     writeToLog("INFO", "No 'Hint' or 'Why' will be created for the " + questionDetails[2] + " Quiz Question")
#             
#             # We verify that the KEA Quiz Question type is supported
#             else:
#                 writeToLog("INFO", "FAILED, please make sure that you're using a support KEA Quiz Question type, using enums(e.g enums.QuizQuestionType.type)")
#                 return False
#                                             
#             # Save Question
#             if self.saveQuizChanges() == False:
#                 writeToLog("INFO", "FAILED to save the changes")
#                 return False
#             
#         # Edit the KEA Quiz Section if necessary by enabling or disabling any KEA option from the KEA Details, Scores and Experience sections
#         if dictDetails != '' or dictScores != '' or dictExperience != '':
#             # We verify if we modify more than one option for the same KEA Section
#             if type(dictDetails) is list:
#                 for option in dictDetails:
#                     if self.editQuizOptions(enums.KEAQuizSection.DETAILS, option, saveChanges=False, resumeEditing=False) == False:
#                         writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.DETAILS.value + " KEA Section options")
#                         return False
#                         
#             else:
#                 # We modify only one option for this specific KEA section
#                 if dictDetails != '':
#                     if self.editQuizOptions(enums.KEAQuizSection.DETAILS, option, saveChanges=False, resumeEditing=False) == False:
#                         writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.DETAILS.value + " KEA Section options")
#                         return False
#                     
#             # We verify if we modify more than one option for the same KEA Section
#             if type(dictScores) is list:
#                 for option in dictScores:
#                     if self.editQuizOptions(enums.KEAQuizSection.SCORES, option, saveChanges=False, resumeEditing=False) == False:
#                         writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.SCORES.value + " KEA Section options")
#                         return False
#                     
#             else:
#                 # We modify only one option for this specific KEA section
#                 if dictScores != '':
#                     if self.editQuizOptions(enums.KEAQuizSection.SCORES, option, saveChanges=False, resumeEditing=False) == False:
#                         writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.SCORES.value + " KEA Section options")
#                         return False
#                     
#             # We verify if we modify more than one option for the same KEA Section   
#             if type(dictExperience) is list:
#                 for option in dictExperience:
#                     if self.editQuizOptions(enums.KEAQuizSection.EXPERIENCE, option, saveChanges=False, resumeEditing=False) == False:
#                         writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.EXPERIENCE.value + " KEA Section options")
#                         return False
#                 
#             else:
#                 # We modify only one option for this specific KEA section
#                 if dictExperience != '':
#                     if self.editQuizOptions(enums.KEAQuizSection.EXPERIENCE, option, saveChanges=False, resumeEditing=False) == False:
#                         writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.EXPERIENCE.value + " KEA Section options")
#                         return False
#             
#             # We save all the changes performed from each KEA Section
#             if self.saveKeaChanges(resumeEditing=True) == False:
#                 writeToLog("INFO", "FAILED to save the changes performed in the KEA Section")
#                 return False
#         else:
#             writeToLog("INFO", "No changes for the KEA Sections was performed")
#         
#         # Save the KEA Quiz entry and navigate to the entry page
#         self.switchToKeaIframe() 
#         self.clickDone()
#         return True


    # @Author: Tzachi guetta  & Horia Cus
    # the following function will create a Quiz (within the given dictQuestions)
    # Please follow the individual list structure for each Quiz Question type
    # questionMultiple     = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text', 'Why Text']
    # questionTrueAndFalse = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text', 'Why Text']
    # questionReflection   = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point', 'Hint Text', 'Why Text']
    # dictQuestions        = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection}
    # questionOpen         = ['0:25', enums.QuizQuestionType.OPEN_QUESTION, 'Question title for Open-Q'] 
    # If you want to change the answer order you can use this function: changeAnswerOrder
    def quizCreation(self, entryName, dictQuestions, dictDetails='', dictScores='', dictExperience='', timeout=20):
        sleep(25)
   
        # Need this step in order to workaround an issue that may fail a test case after uploading an entry
        if self.wait_element(self.clsCommon.upload.UPLOAD_PAGE_TITLE, 0.5, True) != False:
            sleep(2) 
            if self.clsCommon.navigateTo(enums.Location.HOME) == False:
                writeToLog("INFO", "FAILED to navigate to home page")
                return False
           
        if self.searchAndSelectEntryInMediaSelection(entryName) == False:
            writeToLog("INFO", "FAILED to navigate to " + entryName)
            return False
        sleep(timeout)
          
        if self.wait_while_not_visible(self.KEA_MEDIA_IS_BEING_PROCESSED, 120) == False:
            writeToLog("INFO", "FAILED to process the " + entryName + " during the launch")
            return False
        self.switchToKeaIframe()
        if self.wait_while_not_visible(self.KEA_QUIZ_LOADING_CONTAINER, 120) == False:
            writeToLog("INFO", "FAILED to load the quiz screen")
            return False
         
        # We create the locator for the KEA Quiz Question title field area (used only in the "Reflection Point" and "True and False" and "Open-Q" Quiz Questions)
        questionField = (self.KEA_OPTION_TEXTAREA_FIELD[0], self.KEA_OPTION_TEXTAREA_FIELD[1].replace('FIELD_NAME', 'questionTxt')) 
                    
        for questionNumber in dictQuestions:
            questionDetails = dictQuestions[questionNumber]
            
            self.switchToKeaIframe() 
            if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 45) == False:
                writeToLog("INFO","FAILED to wait until spinner isn't visible")
                return False 
            
            # Because D2L application doesn't properly display the entire Quiz screen we need to scroll down in order to select the time stamp field
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
                sleep(2)
                
            # Set the time position of the current quiz inside the timeline section
            if self.setRealTimeMarkerToTime(questionDetails[0]) == False:
                writeToLog("INFO", "FAILED to set the question " + questionDetails[2] + " at time location: " + questionDetails[0] )  
                return False
            
            # Scroll back up if using D2L application
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                self.clsCommon.sendKeysToBodyElement(Keys.ARROW_UP, 4)
                sleep(2)        
            
            # Creating the variable for the Quiz Question Type
            qestionType = questionDetails[1]
            if qestionType == enums.QuizQuestionType.Multiple:   
                # We enter in the KEA Quiz Question Type screen
                if self.selectQuestionType(qestionType) == False:
                    writeToLog("INFO", "FAILED to enter in the " + qestionType.value + " Question screen")
                    return False      
         
                # Add question fields
                # We verify if we have only one question
                if questionDetails[4] != '':
                    QuizQuestion1AdditionalAnswers = [questionDetails[4]]
                
                if questionDetails[5] != '':
                    QuizQuestion1AdditionalAnswers.append(questionDetails[5])
                    
                if questionDetails[6] != '':
                    QuizQuestion1AdditionalAnswers.append(questionDetails[6])
                    
                if len(QuizQuestion1AdditionalAnswers) >= 1:
                    if self.fillQuizFields(questionDetails[2], questionDetails[3], QuizQuestion1AdditionalAnswers) == False:
                        writeToLog("INFO","FAILED to fill question fields")
                        return False
                else:
                    writeToLog("INFO", "Please make sure that you supply at least two question answers")
                    return False
                
                # we verify if the value for the 'Hint' is present in the list
                if len(questionDetails) >= 8:  
                    # we verify if we want to create a Hint for the current Quiz Question
                    if questionDetails[7] != '':
                        if self.createHintAndWhy(questionDetails[7], whyText='') == False:
                            writeToLog("INFO", "FAILED to create a Hint for the " + questionDetails[2] + " Quiz Question")
                            return False
                    else:
                        writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")

                    # we verify if the value for the 'Why' is present in the list
                    if len(questionDetails) >= 9:
                        # we verify if we want to create a Why for the current Quiz Question
                        if questionDetails[8] != '':
                            sleep(2)
                            if self.createHintAndWhy(hintText='', whyText=questionDetails[8]) == False:
                                writeToLog("INFO", "FAILED to create a Why for the " + questionDetails[2] + " Quiz Question")
                                return False
                        else:
                            writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
                else:
                    writeToLog("INFO", "No 'Hint' or 'Why' will be created for the " + questionDetails[2] + " Quiz Question")
                    
            elif qestionType == enums.QuizQuestionType.REFLECTION:
                # We enter in the KEA Quiz Question Type screen
                if self.selectQuestionType(qestionType) == False:
                    writeToLog("INFO", "FAILED to enter in the " + qestionType.value + " Question screen")
                    return False    
                
                # We select the KEA Quiz Question title field
                if self.click(questionField, 2, True) == False:
                    writeToLog("INFO", "FAILED to select the reflection point text area")
                    return False
                
                # We insert the title for the KEA Quiz Question type
                if self.send_keys(questionField, questionDetails[2], True) == False:
                    writeToLog("INFO", "FAILED to insert the " + questionDetails[2] + " reflection point")
                    return False
                
                # We make sure that no 'Hint' or 'Why' are trying to be created for 'Reflection Point' Quiz Question
                if len(questionDetails) >= 4:
                    writeToLog("INFO", "Hint and Why are not supported for the Reflection Point Quiz Question")
                    return False
                
            elif qestionType == enums.QuizQuestionType.TRUE_FALSE:
                # We enter in the KEA Quiz Question Type screen
                if self.selectQuestionType(qestionType) == False:
                    writeToLog("INFO", "FAILED to enter in the " + qestionType.value + " Question screen")
                    return False    
                
                # We select the KEA Quiz Question title field
                if self.click(questionField, 2, True) == False:
                    writeToLog("INFO", "FAILED to select the reflection point text area")
                    return False
                
                #we insert the Question title inside the Question text area
                if self.send_keys(questionField, questionDetails[2], True) == False:
                    writeToLog("INFO", "FAILED to insert the " + questionDetails[2] + " reflection point")
                    return False
                
                # We insert the title for the KEA Quiz Question type
                if questionDetails[3] and questionDetails[4] != '':
                    if self.click(self.KEA_ADD_NEW_ADD_QUESTION_TRUE_ANSWER_FIELD, 3, True) == False:
                        writeToLog("INFO", "FAILED to select the 'True' text area field")
                        return False

                    if self.clear_and_send_keys(self.KEA_ADD_NEW_ADD_QUESTION_TRUE_ANSWER_FIELD, questionDetails[3], True)== False:
                        writeToLog("INFO", "FAILED to insert the " + questionDetails[3] + " text within the 'True' field")
                        return False
                    
                    if self.click(self.KEA_ADD_NEW_QUESTION_FALSE_ANSWER_FIELD, 3, True) == False:
                        writeToLog("INFO", "FAILED to select the 'False' text area field")
                        return False

                    if self.clear_and_send_keys(self.KEA_ADD_NEW_QUESTION_FALSE_ANSWER_FIELD, questionDetails[4], True)== False:
                        writeToLog("INFO", "FAILED to insert the " + questionDetails[4] + " text within the 'False' field")
                        return False
                
                # we verify if the value for the 'Hint' is present in the list
                if len(questionDetails) >= 6:  
                    # we verify if we want to create a Hint for the current Quiz Question
                    if questionDetails[5] != '':
                        if self.createHintAndWhy(questionDetails[5], whyText='') == False:
                            writeToLog("INFO", "FAILED to create a Hint for the " + questionDetails[2] + " Quiz Question")
                            return False
                    else:
                        writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
                        
                    # we verify if the value for the 'Why' is present in the list
                    if len(questionDetails) == 7:
                        # we verify if we want to create a Why for the current Quiz Question
                        if questionDetails[6] != '':
                            sleep(2)
                            if self.createHintAndWhy(hintText='', whyText=questionDetails[6]) == False:
                                writeToLog("INFO", "FAILED to create a Why for the " + questionDetails[2] + " Quiz Question")
                                return False
                        else:
                            writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
                else:
                    writeToLog("INFO", "No 'Hint' or 'Why' will be created for the " + questionDetails[2] + " Quiz Question")
                    
            elif qestionType == enums.QuizQuestionType.OPEN_QUESTION:
                # We enter in the KEA Quiz Question Type screen
                if self.selectQuestionType(qestionType) == False:
                    writeToLog("INFO", "FAILED to enter in the " + qestionType.value + " Question screen")
                    return False    
                
                # We select the KEA Quiz Question title field
                if self.click(questionField, 2, True) == False:
                    writeToLog("INFO", "FAILED to select the reflection point text area")
                    return False
                
                # We insert the title for the KEA Quiz Question type
                if self.send_keys(questionField, questionDetails[2], True) == False:
                    writeToLog("INFO", "FAILED to insert the " + questionDetails[2] + " open-Q")
                    return False
                
                # we verify if the value for the 'Hint' is present in the list
                if len(questionDetails) >= 4:  
                    # we verify if we want to create a Hint for the current Quiz Question
                    if questionDetails[3] != '':
                        if self.createHintAndWhy(questionDetails[3], whyText='') == False:
                            writeToLog("INFO", "FAILED to create a Hint for the " + questionDetails[2] + " Quiz Question")
                            return False
                    else:
                        writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
                        
                    # we verify if the value for the 'Why' is present in the list
                    if len(questionDetails) == 5:
                        # we verify if we want to create a Why for the current Quiz Question
                        if questionDetails[4] != '':
                            sleep(2)
                            if self.createHintAndWhy(hintText='', whyText=questionDetails[4]) == False:
                                writeToLog("INFO", "FAILED to create a Why for the " + questionDetails[2] + " Quiz Question")
                                return False
                        else:
                            writeToLog("INFO", "No hint was given for the " + questionDetails[2] + " Quiz Question")
                else:
                    writeToLog("INFO", "No 'Hint' or 'Why' will be created for the " + questionDetails[2] + " Quiz Question")          
            
            # We verify that the KEA Quiz Question type is supported
            else:
                writeToLog("INFO", "FAILED, please make sure that you're using a support KEA Quiz Question type, using enums(e.g enums.QuizQuestionType.type)")
                return False
                                            
            # Save Question
            if self.saveQuizChanges() == False:
                writeToLog("INFO", "FAILED to save the changes")
                return False
            
        # Edit the KEA Quiz Section if necessary by enabling or disabling any KEA option from the KEA Details, Scores and Experience sections
        if dictDetails != '' or dictScores != '' or dictExperience != '':
            # We verify if we modify more than one option for the same KEA Section
            if type(dictDetails) is list:
                for option in dictDetails:
                    if self.editQuizOptions(enums.KEAQuizSection.DETAILS, option, saveChanges=False, resumeEditing=False) == False:
                        writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.DETAILS.value + " KEA Section options")
                        return False
                        
            else:
                # We modify only one option for this specific KEA section
                if dictDetails != '':
                    if self.editQuizOptions(enums.KEAQuizSection.DETAILS, option, saveChanges=False, resumeEditing=False) == False:
                        writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.DETAILS.value + " KEA Section options")
                        return False
                    
            # We verify if we modify more than one option for the same KEA Section
            if type(dictScores) is list:
                for option in dictScores:
                    if self.editQuizOptions(enums.KEAQuizSection.SCORES, option, saveChanges=False, resumeEditing=False) == False:
                        writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.SCORES.value + " KEA Section options")
                        return False
                    
            else:
                # We modify only one option for this specific KEA section
                if dictScores != '':
                    if self.editQuizOptions(enums.KEAQuizSection.SCORES, option, saveChanges=False, resumeEditing=False) == False:
                        writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.SCORES.value + " KEA Section options")
                        return False
                    
            # We verify if we modify more than one option for the same KEA Section   
            if type(dictExperience) is list:
                for option in dictExperience:
                    if self.editQuizOptions(enums.KEAQuizSection.EXPERIENCE, option, saveChanges=False, resumeEditing=False) == False:
                        writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.EXPERIENCE.value + " KEA Section options")
                        return False
                
            else:
                # We modify only one option for this specific KEA section
                if dictExperience != '':
                    if self.editQuizOptions(enums.KEAQuizSection.EXPERIENCE, option, saveChanges=False, resumeEditing=False) == False:
                        writeToLog("INFO", "FAILED to change the " + enums.KEAQuizSection.EXPERIENCE.value + " KEA Section options")
                        return False
            
            # We save all the changes performed from each KEA Section
            if self.saveKeaChanges(resumeEditing=True) == False:
                writeToLog("INFO", "FAILED to save the changes performed in the KEA Section")
                return False
        else:
            writeToLog("INFO", "No changes for the KEA Sections was performed")
        
        # Save the KEA Quiz entry and navigate to the entry page
        self.switchToKeaIframe() 
        self.clickDone()
        return True
    
    

    # @Author: Horia Cus
    # This function will move the real time marker to the desired time location
    # The real time marker location will be moved by clicking directly on the time line section
    # If the real time marker couldn't be set properly by clicking on the time line section, the Editor Time option will be used
    # timeLocation must be string using mm:ss format ( e.g str(10:00) )
    def setRealTimeMarkerToTime(self, timeLocation):
        self.switchToKeaIframe()
        
        # Take the details from the kea time line section
        keaTimelineSection  = self.wait_element(self.KEA_TIMELINE_PRESENTED_SECTIONS, 10, True)

        # Verify that the time line section is available       
        if keaTimelineSection == False:
            writeToLog("INFO", "FAILED to take the KEA timeline section element")
            return False
        
        # Take the length needed in order to set by the correct pixels the time location, based on the length of the timeline section, entry time and time location
        entryTotalTime               = self.wait_element(self.EDITOR_TOTAL_TIME, 1, True).text.replace(' ', '')[1:]
        m, s                         = entryTotalTime.split(':')
        entryTotalTimeSeconds        = int(m) * 60 + int(s)
        m, s                         = timeLocation.split(':')
        quizTimeLocationInSeconds    = float(m) * 60 + float(s)
        keaTimelineSectionWidth      = keaTimelineSection.size['width']
        widthSizeForOneSecond        = keaTimelineSectionWidth/entryTotalTimeSeconds
        widthSizeInOrderToReachDesiredStartTime = widthSizeForOneSecond * quizTimeLocationInSeconds

        actionSetQuizLocation = ActionChains(self.driver)
        # Set the time line location using action chain
        # Time marker is moved based on the clicked spot from the timeline section element
        try:
            actionSetQuizLocation.move_to_element_with_offset(keaTimelineSection, widthSizeInOrderToReachDesiredStartTime+2.5, -10).pause(1).click().perform()
        except Exception:
            writeToLog("INFO", "FAILED to click on the timeline section during the first time in order to set the desired time marker location")
            timeLineSectionMarker = self.wait_element(self.EDITOR_REALTIME_MARKER, 3, True)
            try:
                ActionChains(self.driver).move_to_element(timeLineSectionMarker).send_keys(Keys.PAGE_DOWN).pause(5).perform()
                ActionChains(self.driver).move_to_element_with_offset(keaTimelineSection, widthSizeInOrderToReachDesiredStartTime+2.5, -10).pause(1).click().perform()
            except Exception:
                # Verify if the real time marker already matches with our time location
                if self.wait_element(self.EDITOR_REALTIME_MARKER, 3, True).text[:5] != timeLocation:
                    writeToLog("INFO", "FAILED to set the start time to during the second try " + str(timeLocation) + " using action chain")
                    # we continue to try to change the real marker time using input field ( not action chains )
                else:
                    writeToLog("INFO", "PASSED, the real time marker has been successfully set to the " + timeLocation + " time location, using Action Chain")
                    return True
        
        timeLineSectionMarker = self.wait_element(self.EDITOR_REALTIME_MARKER, 3, True).text[:5]
        
        # Verify that the Time Marker matches with our desired time location
        if timeLineSectionMarker != timeLocation:
            timeLineSectionMarkerUpdated = self.wait_element(self.EDITOR_REALTIME_MARKER, 3, True).text[4:]
            
            # Verify if there's a gap of one second between the action
            if int(timeLineSectionMarkerUpdated[0]) + 1 == int(timeLocation[-1]):
                if self.driver.capabilities['browserName'] == 'firefox':
                    # If the ml seconds are higher than 49 we need a less difference in px
                    if int(timeLineSectionMarkerUpdated[2:]) >= 49:
                        differencePx = 7
                    # If the ml seconds are less than 49 we need a higher difference in px
                    else:
                        differencePx = 22
                else:
                    # If the ml seconds are higher than 49 we need a less difference in px
                    if int(timeLineSectionMarkerUpdated[2:]) >= 49:
                        differencePx = 10
                    # If the ml seconds are less than 49 we need a higher difference in px
                    else:
                        differencePx = 30       
                    
                actionSetQuizLocationSecond = ActionChains(self.driver)
                
                try:
                    actionSetQuizLocationSecond.move_to_element_with_offset(keaTimelineSection, widthSizeInOrderToReachDesiredStartTime+2.5+differencePx, -10).pause(1).click().perform()
                except Exception:
                    writeToLog("INFO", "FAILED to set the start time to during the second try " + str(timeLocation))
                    return False
                
            else:
                writeToLog("INFO", "Couldn't set the " + timeLocation + " using action chains, but " + timeLineSectionMarker + " time location has been set")
                
        timeLineSectionMarkerUpdated = self.wait_element(self.EDITOR_REALTIME_MARKER, 3, True).text[:5]
                    
        # Verify that the Time Marker matches with our desired time location after the second try of using Action Chain
        if timeLineSectionMarkerUpdated != timeLocation:
            # As a redundancy, if we are unable to set the desired time location by Action Chain, we are going to use Editor Time Picker           
            # Select the time stamp input field
            if self.click(self.EDITOR_TIME_PICKER, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the kea timeline field")
                return False
            sleep(1)

            timePickerHighlighted = self.wait_element(self.EDITOR_TIME_PICKER_HIGHLIGHTED_CONTAINER, 3, True)

            # Verify that the input time field is highlighted
            if timePickerHighlighted == False:
                writeToLog("INFO", "Time picker input field couldn't be highlighted during the first try")

                if self.click(self.EDITOR_TIME_PICKER, 1, True) == False:
                    writeToLog("INFO", "FAILED to click on the kea timeline field")
                    return False
                sleep(1)

                timePickerHighlighted = self.wait_element(self.EDITOR_TIME_PICKER_HIGHLIGHTED_CONTAINER, 3, True)
                if timePickerHighlighted == False:
                    writeToLog("INFO", "FAILED to highlight the time picker input field during the second time")
                    return False

            # Clear first the current Editor Time Location
            if self.clear_and_send_keys(self.EDITOR_TIME_PICKER, timeLocation) == False:
                writeToLog("INFO", "FAILED to select the timeline field text")
                return False
            sleep(2)
            # Put the desired time location inside the Editor Time input field
            if self.clear_and_send_keys(self.EDITOR_TIME_PICKER, timeLocation) == False:
                writeToLog("INFO", "FAILED to select the timeline field text")
                return False

            # Move the real time maker to the desired time stamp
            sleep(2)
            self.clsCommon.sendKeysToBodyElement(Keys.ENTER)
            sleep(2)
            
            timeLineSectionMarkerUpdated = self.wait_element(self.EDITOR_REALTIME_MARKER, 1, True).text[:5]
            
            # Verify that the Time Marker matches with our desired time location
            if timeLineSectionMarkerUpdated != timeLocation:
                writeToLog("INFO", "FAILED to set the real time marker to the " + timeLocation + " time location using Editor Time Picker")
                return False
            else:
                writeToLog("INFO", "PASSED, the real time marker has been successfully set to the " + timeLocation + " time location using, Editor Time Picker")
                return True
            
        writeToLog("INFO", "PASSED, the real time marker has been successfully set to the " + timeLocation + " time location, using Action Chain")
        return True
    
    
    # @Author: Horia Cus
    # This function can navigate to a specific entry and initiate the KEA Quiz option
    # This function work for both entries that have Quiz created or not
    # entryName must be inserted in order to verify that the KEA page has been successfully opened and loaded
    def initiateQuizFlow(self, entryName, navigateToEntry=False, timeOut=40):
        self.switch_to_default_content()
        if navigateToEntry == True:
            sleep(timeOut)
            if self.launchKEA(entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Failed to launch KEA for: " + entryName)
                return False

        self.switchToKeaIframe()
        
        if self.verifyKeaEntryName(entryName, 60) == False:
            writeToLog("INFO", "FAILED to load the page until the " + entryName + " was present")
            return False
        
        if self.wait_element(self.KEA_QUIZ_TAB_ACTIVE, 5, True) == False:
            if self.click(self.KEA_QUIZ_TAB, 5, True) == False:
                writeToLog("INFO","FAILED to click on the KEA Quiz tab menu")
                return False  
            
        start_button = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', enums.KeaQuizButtons.START.value))
        
        if self.wait_element(start_button, 2, True) != False:
            if self.click(start_button, 1, True) == False:
                writeToLog("INFO","FAILED to click on the Quiz Start button")
                return False
        
        sleep(3)       
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_CONTAINER, 60) == False:
            writeToLog("INFO","FAILED, the loading spinner remained in infinite loading")
            return False
        
        sleep(1)
                
        if self.wait_element(self.KEA_QUIZ_TAB_ACTIVE, 5, True) == False:
            writeToLog("INFO", "FAILED, KEA Quiz tab is not active")
            return False
                      
        return True
    

    # @Author: Horia Cus
    # This function verifies that the KEA entry name is present and that it matches with the desired one
    def verifyKeaEntryName(self, entryName, timeout=60):
        self.switchToKeaIframe()
        
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                el = self.wait_element(self.KEA_ENTRY_NAME, 60, multipleElements=True)
                if el.text == entryName:
                    self.setImplicitlyWaitToDefault()
                    writeToLog("INFO", "The " + entryName + " has been found in KEA page")
                    break
                else:
                    writeToLog("INFO", "The KEA entry-name doesn't matches with " + entryName + " entry")
                    return False
            except:
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    writeToLog("INFO", "FAILED to find the " + entryName + " within the " + str(timeout) + " seconds")
                    return False
                pass
        
        if self.wait_while_not_visible(self.KEA_LOADING_CONTAINER, 60) == False:
            writeToLog("INFO", "FAILED to wait until the KEA page has been successfully loaded")
            return False

        writeToLog("INFO", "KEA Page is active for the " + entryName + " entry")
        return True
                        

    # @Author: Horia Cus
    # This function triggers a specific KEA Section and it can enable / disable or add an input for any available KEA option
    # keaCategory = must be enum
    # keaOption must be enum and have a map
    # If saveChanges = True, all the KEA changes will be saved by clicking on the done button and waiting for the spinner to disappear
    def editQuizOptions(self, keaSection, keaOptionDict, saveChanges=False, resumeEditing=False):
        if keaSection != '':
            tmpKEASection = (self.KEA_TOGGLE_MENU_OPTION[0], self.KEA_TOGGLE_MENU_OPTION[1].replace('OPTION_NAME', keaSection.value))
    
        else:
            writeToLog("INFO", "Please specify in which KEA section we should enable or disable the options")
            return False
        
        self.switchToKeaIframe()
        sleep(1)
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to click on the " + keaSection.value + " KEA section drop down menu")
            return False
                
        for options in keaOptionDict:                
            if keaOptionDict[options] == True:   
                if options == enums.KEAQuizOptions.NO_SEEKING_FORWARD:
                    options = enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to enable the " + options.value + " in order to enable the: " + enums.KEAQuizOptions.NO_SEEKING_FORWARD.value)
                        return False
                    
                    sleep(1)
                    options = enums.KEAQuizOptions.NO_SEEKING_FORWARD
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to enable the " + options.value)
                        return False                
             
                elif self.changeKEAOptionState(options, True) == False:
                    return False 
                
                elif options == enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to enable the " + options.value)
                        return False          
                              
            elif keaOptionDict[options] == False:
                if options == enums.KEAQuizOptions.DO_NOT_SHOW_SCORES:
                    options = enums.KEAQuizOptions.SHOW_SCORES
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to disable the " + options.value + " by enabling the dependency option: " + enums.KEAQuizOptions.SHOW_SCORES.value)
                        return False

                elif options == enums.KEAQuizOptions.NO_SEEKING_FORWARD:
                    options = enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to enable the " + options.value + " in order to enable the: " + enums.KEAQuizOptions.NO_SEEKING_FORWARD.value)
                        return False
                    
                    sleep(1)
                    options = enums.KEAQuizOptions.NO_SEEKING_FORWARD
                    if self.changeKEAOptionState(options, False) == False:
                        writeToLog("INFO", "FAILED to enable the " + options.value)
                        return False  
                    
                elif options == enums.KEAQuizOptions.SHOW_SCORES:
                    options = enums.KEAQuizOptions.DO_NOT_SHOW_SCORES
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to disable the " + options.value + " by enabling the dependency option: " + enums.KEAQuizOptions.DO_NOT_SHOW_SCORES.value)
                        return False
                    
                elif options == enums.KEAQuizOptions.ALLOW_SKIP:
                    options = enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to disable the " + options.value + " by enabling the dependency option: " + enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP.value)
                        return False
                
                elif options == enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP:
                    options = enums.KEAQuizOptions.ALLOW_SKIP
                    if self.changeKEAOptionState(options, True) == False:
                        writeToLog("INFO", "FAILED to disable the " + options.value + " by enabling the dependency option: " + enums.KEAQuizOptions.ALLOW_SKIP.value)
                        return False
                                       
                else:
                    if self.changeKEAOptionState(options, False) == False:
                        return False
                
            elif keaOptionDict[options] != '':
                if options == enums.KEAQuizOptions.SET_NUMBER_OF_ATTEMPTS:
                    if self.clear_and_send_keys(self.KEA_NUMBER_OF_ALLOW_ATTEMPTS, keaOptionDict[options]) == False:
                        writeToLog("INFO", "FAILED to insert number of allow attempts")
                        return False 
                        
                elif options == enums.KEAQuizOptions.QUIZ_SCORE_TYPE: 
                    if self.click(self.KEA_SCORE_TYPE_DROP_DOWN) == False:
                        writeToLog("INFO", "FAILED to click on score type dropdown")
                        return False  
                    
                    tmpScoreType = (self.KEA_SCORE_TYPE_OPTION[0], self.KEA_SCORE_TYPE_OPTION[1].replace('SCORE_TYPE', keaOptionDict[options]))    
                    if self.click(tmpScoreType) == False:
                        writeToLog("INFO", "FAILED to click on " + options.value + " score type")
                        return False
                                              
                else:
                    if options == enums.KEAQuizOptions.QUIZ_NAME:
                        tmpKEAInputField = (self.KEA_OPTION_INPUT_FIELD[0], self.KEA_OPTION_INPUT_FIELD[1].replace('FIELD_NAME', 'quizName'))
                    
                    elif options == enums.KEAQuizOptions.SHOW_WELCOME_PAGE:
                        tmpKEAInputField = (self.KEA_OPTION_TEXTAREA_FIELD[0], self.KEA_OPTION_TEXTAREA_FIELD[1].replace('FIELD_NAME', 'welcomeMessage'))
                
                    if self.click(tmpKEAInputField, 5, True) == False:
                        writeToLog("INFO", "FAILED to select the " + options.value + " option")
                        return False
                
                    if self.clear_and_send_keys(tmpKEAInputField, keaOptionDict[options], True) == False:
                        writeToLog("INFO", "FAILED to clear and add " + keaOptionDict[options] + " text to the " + keaOptionDict.value)
                        return False
                
                    sleep(3) 
                                                          
        sleep(1)  
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to collapse the " + keaSection.value)
            return False
        
        if saveChanges == True:
            if self.saveKeaChanges(resumeEditing) == False:
                writeToLog("INFO", "FAILED to save the KEA changes")
                return False
                                    
        return True
    

    # @Author: Horia Cus
    # This function changes the status of any KEA Option to enable or disable
    # If stateEnabled=True, it will verify if the specific KEA Option is enabled, if not, it will enable it
    # If stateEnabled=False, it will verify if the specific KEA Option is disabled, if not, it will disable it
    # keaOption must be enum and have a map
    # stateEnabled must be Boolean
    def changeKEAOptionState(self, keaOption, stateEnabled):
        self.switchToKeaIframe()
        
        if stateEnabled == True:                        
            tmpKEAOption = (self.KEA_OPTION_ACTIVE[0], self.KEA_OPTION_ACTIVE[1].replace('OPTION_NAME', keaOption.value))
            if self.wait_element(tmpKEAOption, 1, True) != False:
                writeToLog("INFO", "The " + keaOption.value + " is already enabled")
                return True
            
            else:
                if keaOption.value == enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:
                    if self.click(self.KEA_ALLOW_MULTIPLE_ATTEMPTS_OPTION_GRAYED_OUT) == False:
                        writeToLog("INFO", "FAILED to enable " + keaOption.value + " option")
                        return False                        
                else:        
                    tmpKEAOption = (self.KEA_OPTION_NORMAL[0], self.KEA_OPTION_NORMAL[1].replace('OPTION_NAME', keaOption.value))
                    if self.click(tmpKEAOption, 5, True) == False:
                        writeToLog("INFO", "FAILED to enable " + keaOption.value + " option")
                        return False

        elif stateEnabled == False:
            if keaOption == enums.KEAQuizOptions.ALLOW_DOWNLOAD or keaOption == enums.KEAQuizOptions.INSTRUCTIONS:
                if self.verifyKEAOptionState(enums.KEAQuizOptions.SHOW_WELCOME_PAGE, False) == True:
                    writeToLog("INFO", "The " + keaOption.value + " is already disabled due to the dependent option, " + enums.KEAQuizOptions.SHOW_WELCOME_PAGE.value)  
                    return True
                                  
            tmpKEAOptionActive = (self.KEA_OPTION_ACTIVE[0], self.KEA_OPTION_ACTIVE[1].replace('OPTION_NAME', keaOption.value))
            if keaOption.value == enums.KEAQuizOptions.ALLOW_MULTUPLE_ATTEMPTS:
                tmpKEAOptionNormal = self.KEA_ALLOW_MULTIPLE_ATTEMPTS_OPTION_GRAYED_OUT
            else:
                tmpKEAOptionNormal = (self.KEA_OPTION_NORMAL[0], self.KEA_OPTION_NORMAL[1].replace('OPTION_NAME', keaOption.value))
            if self.wait_element(tmpKEAOptionActive, 1, True) == False and self.wait_element(tmpKEAOptionNormal, 1, True) != False:
                writeToLog("INFO", "The " + keaOption.value + " is already disabled")
                return True
            
            else:
                if self.click(tmpKEAOptionNormal, 5, True) == False:
                    writeToLog("INFO", "FAILED to enable " + keaOption.value + " option")
                    return False
        else:
            writeToLog("INFO", "Make sure that you use boolean")
            return False
    
        return True
    

    # @Author: Horia Cus
    # This function verifies if the status of any KEA Option is enabled or disabled
    # If expectedState=True, it will verify if the specific KEA Option is enabled
    # If expectedState=False, it will verify if the specific KEA Option is disabled
    # keaOption must be enum and have a map with boolean
    def verifyKEAOptionState(self, keaOption, expectedState):
        self.switchToKeaIframe()
        
        if expectedState == True:
            tmpKEAOptionActive = (self.KEA_OPTION_ACTIVE[0], self.KEA_OPTION_ACTIVE[1].replace('OPTION_NAME', keaOption.value))
            if self.wait_element(tmpKEAOptionActive, 1, True) == False:
                writeToLog("INFO", "The " + keaOption.value + " is not enabled")
                return False

        elif expectedState == False:
            tmpKEAOptionActive = (self.KEA_OPTION_ACTIVE[0], self.KEA_OPTION_ACTIVE[1].replace('OPTION_NAME', keaOption.value))
            tmpKEAOptionNormal = (self.KEA_OPTION_NORMAL[0], self.KEA_OPTION_NORMAL[1].replace('OPTION_NAME', keaOption.value))
            if self.wait_element(tmpKEAOptionActive, 1, True) == False and self.wait_element(tmpKEAOptionNormal, 1, True) != False:
                writeToLog("INFO", "The " + keaOption.value + " is disabled")
                return True
            else:
                writeToLog("INFO", "The " + keaOption.value + " is not disabled")
                return False

        else:
            writeToLog("INFO", "Make sure that you use boolean")
            return False 
        
        return True
    

    # @Author: Horia Cus
    # This function verifies if the status of any KEA Option is enabled or disabled or that a specific element is present or not
    # keaSection must be enum
    # keaOption must be enum and have a map
    def verifyQuizOptionsInKEA(self, keaSection, keaOption):
        self.switchToKeaIframe()
        
        if keaSection != '':
            tmpKEASection = (self.KEA_TOGGLE_MENU_OPTION[0], self.KEA_TOGGLE_MENU_OPTION[1].replace('OPTION_NAME', keaSection.value))
        else:
            writeToLog("INFO", "Please specify in which KEA section we should verify the state of the options")
            return False
        
        sleep(1)
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to click on the " + keaSection.value)
            return False
        
        for options in keaOption:
            if options == enums.KEAQuizOptions.QUIZ_NAME:
                if self.verifyKeaEntryName(keaOption[options], 5) == False:
                    writeToLog("INFO", "The KEA entry name doesn't match with " + keaOption[options] + " name")
                    return False
                            
            else:
                if keaOption[options] == True:
                    if self.verifyKEAOptionState(options, True) == False:
                        return False  
                                  
                elif keaOption[options] == False:
                    if self.verifyKEAOptionState(options, False) == False:
                        return False

                elif keaOption[options] != '':
                    writeToLog("INFO", "Work in progress")
#                     if self.clsCommon.player.verifyQuizElementsInPlayer() == False: WIP
            
        sleep(1)         
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to collapse the " + keaSection.value)
            return False     
        
        return True
    
    
    # @Author: Horia Cus
    # This function switches to the KEA Preview Player Iframe
    def switchToKEAPreviewPlayer(self):
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.KEA_QUIZ_PLAYER:
            return True
        else:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KEA_QUIZ_PLAYER
            if self.swith_to_iframe(self.KEA_IFRAME_PREVIEW_PLAYER) == False:
                writeToLog("INFO", "FAILED to switch to KEA preview player")
                return False
            else:
                return True
            

    # @Author: Horia Cus
    # This function switches to the KEA BLANK Iframe
    def switchToKEABlank(self):
        self.switch_to_default_content()
        
        if localSettings.TEST_CURRENT_IFRAME_ENUM == enums.IframeName.KEA_QUIZ_BLANK:
            return True
        else:
            localSettings.TEST_CURRENT_IFRAME_ENUM = enums.IframeName.KEA_QUIZ_BLANK
            if self.swith_to_iframe(self.KEA_IFRAME_BLANK) == False:
                writeToLog("INFO", "FAILED to switch to KEA preview player")
                return False
            else:
                return True
    

    # @Author: Horia Cus
    # This function opens the KEA preview screen
    def openKEAPreviewScreen(self):
        self.switchToKeaIframe()

        if self.click(self.KEA_PREVIEW_ICON, 5, True) == False:
            writeToLog("INFO", "FAILED to click on the preview icon")
            return False
        
        self.switchToKEAPreviewPlayer()
                
        if self.wait_visible(self.KEA_PREVIEW_PLAY_BUTTON, 30, True) == False:
            writeToLog("INFO", "FAILED to load the preview screen")
            return False
        
        return True
    
    
    # @Author: Horia Cus
    # This function closes the KEA Preview screen
    def closeKEAPreviewScreen(self):       
        self.switchToKEABlank()

        if self.click(self.KEA_PREVIEW_CLOSE_BUTTON, 5, True) == False:
            writeToLog("INFO", "FAILED to close the KEA preview screen")
            return False

        self.switch_to_default_content()
        self.switchToKeaIframe()
        return True


    # @Author: Horia Cus
    # This function verifies that the default options are displayed after using the revert option
    # keaSection = must use enums.KEAQuizSection
    def revertToDefaultInKEA(self, keaSection):
        self.switchToKeaIframe()
        
        tmpKEASection = (self.KEA_TOGGLE_MENU_OPTION[0], self.KEA_TOGGLE_MENU_OPTION[1].replace('OPTION_NAME', keaSection.value))
        tmpKEAOptionSeeking = (self.KEA_OPTION_NORMAL[0], self.KEA_OPTION_NORMAL[1].replace('OPTION_NAME', enums.KEAQuizOptions.NO_SEEKING_FORWARD.value))
        
        sleep(1)
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to click on the " + keaSection.value)
            return False
        sleep(1)
        if self.click(self.KEA_QUIZ_OPTIONS_REVERT_TO_DEFAULT_BUTTON, 5, True) == False:
            writeToLog("INFO", "FAILED to click on the revert to default button")
            return False
        
        if keaSection == enums.KEAQuizSection.DETAILS:            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.SHOW_WELCOME_PAGE, True) == False:
                return False
            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.ALLOW_DOWNLOAD, True) == False:
                return False
            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.INSTRUCTIONS, True) == False:
                return False
            
        elif keaSection == enums.KEAQuizSection.SCORES:            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.DO_NOT_SHOW_SCORES, False) == False:
                return False
            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.SHOW_SCORES, True) == False:
                return False
            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.INCLUDE_ANSWERS, True) == False:
                return False
            
        elif keaSection == enums.KEAQuizSection.EXPERIENCE:            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.ALLOW_ANSWER_CHANGE, True) == False:
                return False
            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.ALLOW_SKIP, True) == False:
                return False
            
            if self.verifyKEAOptionState(enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP, False) == False:
                return False
            
            if self.wait_element(tmpKEAOptionSeeking, 1, False) != False:   
                if self.verifyKEAOptionState(enums.KEAQuizOptions.NO_SEEKING_FORWARD, False) == False:
                    return False
            else:
                writeToLog("INFO", "AS EXPECTED, no seeking forward option was found as disabled")
        
        sleep(1)
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to collapse the " + keaSection.value)
            return False
            
        return True
    
    
    # @Author: Horia Cus
    # This function can navigate to the Entry page while being in the KEA Page
    # entryName = entry that you want to navigate to
    def navigateToEntryPageFromKEA(self, entryName):
        self.switch_to_default_content()
        
        if self.clsCommon.entryPage.verifyEntryNamePresent(entryName, 3) == True:
            writeToLog("INFO","You are already in the " + entryName + " entry page")
            return True 
        
        if self.saveKeaChanges() == False:
            writeToLog("INFO", "FAILED to save the KEA changes")
            return False
                
        tmp_button = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', enums.KeaQuizButtons.GO_TO_MEDIA_PAGE.value))
        sleep(1)
        if self.wait_element(tmp_button, 60, True) == False:
            writeToLog("INFO", "FAILED to find the go to media button")
            return False
        
        sleep(1)
        if self.click(tmp_button, 5, True) == False:
            writeToLog("INFO", "FAILED to click on the Go To Media button")
            return False
        
        self.switch_to_default_content()
        
        sleep(3)
        
        if self.clsCommon.entryPage.verifyEntryNamePresent(entryName, 60)== False:
            writeToLog("INFO","FAILED to load the entry page for " + entryName + " entry")
            return False
        
        sleep(2)    
        return True
    
    
    # @Author: Horia Cus
    # This function saves any change performed within the KEA page by clicking on the done button and waiting for the changes to be performed
    # if resumeEditing=True, we will click on the "Edit" button and wait for the kea options to be displayed
    def saveKeaChanges(self, resumeEditing=False):
        self.switchToKeaIframe()
        
        tmp_button_done = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', enums.KeaQuizButtons.DONE.value))

        if self.wait_element(tmp_button_done, 3, True) != False:
            if self.click(tmp_button_done, 5, True) == False:
                writeToLog("INFO", "FAILED to click on the done button")
                return False
            
            sleep(0.5)
            
            if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 75) == False:
                writeToLog("INFO","FAILED to save the changes")
                return False  
            
            sleep(2)
            
        else:
            writeToLog("INFO", "FAILED to find the 'done' button in order to save the changes")
            return False
        
        if resumeEditing == True:
            sleep(3)
            tmp_button_edit = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', enums.KeaQuizButtons.EDIT_QUIZ.value))
            if self.wait_element(tmp_button_edit, 30, True) == False:
                writeToLog("INFO", "FAILED to find the edit quiz button")
                return False
            
            if self.click(tmp_button_edit, 3, True) == False:
                writeToLog("INFO", "FAILED to click on the edit quiz button")
                return False
            
            if self.wait_element(tmp_button_done, 30, True) == False:
                writeToLog("INFO", "FAILED to load the edit quiz page")
                return False
            sleep(1)
                        
        return True
    
    
    # @Author: Horia Cus
    # This function creates a hint and why while being in the 'Multiple Choices' or 'True and False' KEA Quiz Question type screen
    # hintText = is the text that you want to be displayed in the hint screen ( use only str)
    # whyText  = is the text that you want to be displayed in the why screen ( use only str)
    # You can  create a hint without specifying a why, leaving the whyText as = ''
    def createHintAndWhy(self, hintText='', whyText=''):
        self.switchToKeaIframe()
        
        # we verify that we are in a KEA Quiz Question screen
        saveButton = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', enums.KeaQuizButtons.SAVE.value))
        if self.wait_element(saveButton, 3, True) == False:
            writeToLog("INFO", "FAILED, please make sure that you're in 'Multiple Choices' or 'True and False' KEA Quiz Question type screen")
            return False
        
        # we used this locator in order to save the hint any why changes
        applyButton = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', enums.KeaQuizButtons.APPLY.value))

        if hintText != '':
            if self.click(self.KEA_ADD_NEW_QUESTION_HINT_AND_WHY_TOGGLE_MENU_BUTTON, 3, True) == False:
                writeToLog("INFO", "FAILED to trigger the Hint and Why toggle menu")
                return False
            sleep(1)
            
            # access the Hint option
            if self.click(self.KEA_ADD_NEW_QUESTION_HINT_BUTTON, 3, True) == False:
                writeToLog("INFO", "FAILED to select the 'Hint' option from the Hint and Why toggle menu")
                return False
            # leave time for input field to be properly displayed
            sleep(1)
            # We use action chains in order to insert text within the fields, input text area being already active
            action = ActionChains(self.driver)
            try:
                action.send_keys(hintText).perform()
            except Exception:
                writeToLog("INFO", "FAILED to insert " + hintText + " in the hint text field")
                return False
            # We wait one second in order to make sure that all the text was properly inserted
            sleep(1)
            # We save the changes
            if self.click(applyButton, 3, True) == False:
                writeToLog("INFO", "FAILED to click on the 'Apply button' in order to save the Hint changes")
                return False
            
        if whyText != '':
            if self.click(self.KEA_ADD_NEW_QUESTION_HINT_AND_WHY_TOGGLE_MENU_BUTTON, 3, True) == False:
                writeToLog("INFO", "FAILED to trigger the Hint and Why toggle menu")
                return False
            sleep(1)
            # access the Why option
            if self.click(self.KEA_ADD_NEW_QUESTION_WHY_BUTTON, 3, True) == False:
                writeToLog("INFO", "FAILED to select the 'Why' option from the Hint and Why toggle menu")
                return False
            # leave time for the input field to be properly displayed
            sleep(1)
            # We use action chains in order to insert text within the fields, because the fields are already clicked
            action = ActionChains(self.driver)
            try:
                action.send_keys(whyText).perform()
            except Exception:
                writeToLog("INFO", "FAILED to insert " + whyText + " in the 'why' text field")
                return False
            # We wait one second in order to make sure that all the text was properly inserted
            sleep(1)
            # We save the changes
            if self.click(applyButton, 3, True) == False:
                writeToLog("INFO", "FAILED to click on the 'Apply button' in order to save the Why changes")
                return False

        return True
    

    # @Author: Horia Cus
    # This function enters in any Quiz Question Type screen
    # questionType must be enum ( e.g enums.QuizQuestionType.Multiple )
    # we support 'Multiple Choice', 'True and False' and 'Reflection Point'
    def selectQuestionType(self, qestionType):
        self.switchToKeaIframe()
        
        if qestionType == enums.QuizQuestionType.Multiple:
            # Verify if the KEA Quiz Question type is already highlighted
            if self.wait_element(self.KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON_ACTIVE, 2, True) != False or self.wait_element(self.KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON_DEFAULT, 2, True) != False:
                if self.click(self.KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON) == False:
                    writeToLog("INFO","FAILED to activate the 'ADD NEW MULTIPLE' quiz type")
                    return False
                
            # We highlight the KEA Quiz Question type and then access it
            else:
                if self.click(self.KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON) == False:
                    writeToLog("INFO","FAILED to highlight the 'ADD NEW MULTIPLE' quiz type")
                    return False
                sleep(1)

                if self.click(self.KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON_ACTIVE) == False:
                    writeToLog("INFO","FAILED to activate the 'ADD NEW MULTIPLE' quiz type")
                    return False

        elif qestionType == enums.QuizQuestionType.REFLECTION:
            # Verify if the KEA Quiz Question type is already highlighted
            if self.wait_element(self.KEA_ADD_NEW_REFLECTION_POINT_BUTTON_ACTIVE, 2, True) != False:
                if self.click(self.KEA_ADD_NEW_REFLECTION_POINT_BUTTON_ACTIVE) == False:
                    writeToLog("INFO","FAILED to activate the 'ADD NEW MULTIPLE' quiz type")
                    return False
                
            # We highlight the KEA Quiz Question type and then access it
            else:
                if self.click(self.KEA_ADD_NEW_REFLECTION_POINT_BUTTON) == False:
                    writeToLog("INFO","FAILED to highlight the 'Reflection Point' quiz type")
                    return False
                sleep(1)

                if self.click(self.KEA_ADD_NEW_REFLECTION_POINT_BUTTON_ACTIVE) == False:
                    writeToLog("INFO","FAILED to activate the 'Reflection Point' quiz type")
                    return False
                    
        elif qestionType == enums.QuizQuestionType.TRUE_FALSE:
            # Verify if the KEA Quiz Question type is already highlighted
            if self.wait_element(self.KEA_ADD_NEW_TRUE_FALSE_QUESTION_BUTTON_ACTIVE, 2, True) != False:
                if self.click(self.KEA_ADD_NEW_TRUE_FALSE_QUESTION_BUTTON_ACTIVE) == False:
                    writeToLog("INFO","FAILED to activate the 'True and False' quiz type")
                    return False
                
            # We highlight the KEA Quiz Question type and then access it
            else:
                if self.click(self.KEA_ADD_NEW_TRUE_FALSE_QUESTION_BUTTON) == False:
                    writeToLog("INFO","FAILED to highlight the 'True and False' quiz type")
                    return False
                sleep(1)

                if self.click(self.KEA_ADD_NEW_TRUE_FALSE_QUESTION_BUTTON_ACTIVE) == False:
                    writeToLog("INFO","FAILED to activate the 'True and False' quiz type")
                    return False
                
        elif qestionType == enums.QuizQuestionType.OPEN_QUESTION:
            # Verify if the KEA Quiz Question type is already highlighted
            if self.wait_element(self.KEA_ADD_NEW_OPEN_QUESTION_BUTTON_ACTIVE, 2, True) != False:
                if self.click(self.KEA_ADD_NEW_OPEN_QUESTION_BUTTON_ACTIVE) == False:
                    writeToLog("INFO","FAILED to activate the 'open-Q' quiz type")
                    return False
                
            # We highlight the KEA Quiz Question type and then access it
            else:
                if self.click(self.KEA_ADD_NEW_OPEN_QUESTION_BUTTON) == False:
                    writeToLog("INFO","FAILED to highlight the 'open-Q' quiz type")
                    return False
                sleep(1)

                if self.click(self.KEA_ADD_NEW_OPEN_QUESTION_BUTTON_ACTIVE) == False:
                    writeToLog("INFO","FAILED to activate the 'open-Q' quiz type")
                    return False            
                
        # We verify that a supported KEA Quiz Question type has been used      
        else:
            writeToLog("INFO", "FAILED, please make sure that you used a supported KEA Quiz Question type and that the value used was enum")
            return False
                
        return True


    # @Author: Inbar Willman
    # Check editor when user is able just to create clip in editor
    def verifyEditorForClippingPermission(self):
        # Verify that quiz tab isn't displayed
        if self.wait_element(self.KEA_QUIZ_TAB, timeout=3) != False:
            writeToLog("INFO","FAILED: Quiz tab is displayed in editor")
            return False    
        
        # Verify that 'Save' button for trim isn't displayed       
        if self.wait_element(self.EDITOR_SAVE_BUTTON, timeout=3) != False:
            writeToLog("INFO","FAILED: 'Save' button is displayed in editor")
            return False      
        
        writeToLog("INFO","Success: 'Save' button and Quiz tab aren't displayed in editor")   
        return True       

      
    # @Author: Horia Cus
    # This function will verify the quiz question number, timestamp and title in the KEA Timeline section
    # questionDict must have the following structure {'NUMBER OF QUESTION':questionDetailsList}
    # questionDetailsList must contain ['timestamp', enums.QuizQuestionType.Type, 'Question title']
    def keaTimelineVerification(self, questionDict):
        self.switchToKeaIframe()
        if self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 5, True) == False:
            writeToLog("INFO", "FAILED to find any quiz question pointer in the time line section")
            return False
        
        # We take all the available quiz question pointers from the timeline KEA section
        presentedQuestionsInTimeline = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
        
        # We verify that the number of the available quiz questions from the timeline, matches with the number of quiz questions given in the questionDict
        if len(presentedQuestionsInTimeline) != len(questionDict):
            writeToLog("INFO", "FAILED, in timeline section were found " + str(len(presentedQuestionsInTimeline)) + " questions, and in the dictionary were given " + str(len(questionDict)) + " questions")
            return False
        
        totalQuestionNumber = (self.KEA_TIMELINE_SECTION_TOTAL_QUESTION_NUMBER[0], self.KEA_TIMELINE_SECTION_TOTAL_QUESTION_NUMBER[1].replace('QUESTION_NUMBER', str(len(presentedQuestionsInTimeline))))
        
        if self.wait_element(totalQuestionNumber, 1, True) == False:
            writeToLog("INFO", "FAILED, the total number of question text doesn't match with the total number of questions from the KEA timeline section")
            return False
        
        actions = {}
        
        # We verify all the available quiz question pointers, by verifying the quiz number,time stamp and quiz title
        for x in range(0, len(presentedQuestionsInTimeline)):
            # We take the locator element for the current quiz number
            currentQuestion = presentedQuestionsInTimeline[x]
            
            actions["action{0}".format(x)]= ActionChains(self.driver)
            
            # We hover over the current quiz number, in order to verify the elements
            try:
                actions["action{0}".format(x)].move_to_element(currentQuestion).pause(2).perform()
            except Exception:
                writeToLog("INFO", "FAILED to hover over the quiz number " + str(x+1) + " during the first try")
                # Add redundancy step if unable to select the element during the first try
                if self.clickElement(currentQuestion, True) == False:
                    writeToLog("INFO", "FAILED to click on the quiz number "  + str(x+1) + " in order to hover on it during the second try")
                    return False
                
                if self.setRealTimeMarkerToTime('00:00') == False:
                    writeToLog("INFO", "FAILED to resume the real time marker to second zero in order to hover on the quiz cue point during the second try")
                    return False
                
                try:
                    ActionChains(self.driver).move_to_element(currentQuestion).pause(2).perform()
                except Exception:
                    writeToLog("INFO", "FAILED to hover over the quiz number " + str(x+1) + " after two tries")
                    return False
            
            # We take the quiz title and time stamp for the current quiz number
            currentQuestionDetails = questionDict[str(x+1)]
            
            # We take the presented quiz number, title and time stamp
            try:
                questionNumberPresented     = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_NUMBER, 2, True).text
                questionTitlePresented      = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE, 2, True).text
                questionTimestampPresented  = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_TIMESTAMP, 2, True).text
            except Exception:
                writeToLog("INFO", "FAILED to find the question details while hovering over the question: " + currentQuestionDetails[2] + " during the first time")
                try:
                    # Take the entry name in order to switch between the KEA Tabs
                    try:
                        entryName = self.wait_element(self.KEA_ENTRY_NAME, 60, multipleElements=True).text
                    except Exception:
                        writeToLog("INFO", "FAILED to take the Entry Name while trying to verify the timeline section")
                        return False
                    
                    # Switch between the kea tabs in order to refresh the elements
                    if self.launchKEATab(entryName, enums.keaTab.VIDEO_EDITOR, False, 1) == False:
                        writeToLog("INFO", "FAILED to navigate to the Video Editor in order to try to perform a switch between the tabs and take the Cue Point details")
                        return False
                    sleep(3)
                    
                    if self.launchKEATab(entryName, enums.keaTab.QUIZ, False, 1) == False:
                        writeToLog("INFO", "FAILED to navigate to the Video Editor in order to try to perform a switch between the tabs and take the Cue Point details")
                        return False
                    sleep(7)
                    # Take the questions from the timeline after switching between KEA Tabs
                    presentedQuestionsInTimelineSecondTry = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
                    currentQuestionSecondTry              = presentedQuestionsInTimelineSecondTry[x]
                    
                    ActionChains(self.driver).move_to_element(currentQuestionSecondTry).pause(2).perform()
                    questionNumberPresented     = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_NUMBER, 2, True).text
                    questionTitlePresented      = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE, 2, True).text
                    questionTimestampPresented  = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_TIMESTAMP, 2, True).text
                except Exception:
                    writeToLog("INFO", "FAILED to find the question details while hovering over the question: " + currentQuestionDetails[2] + " after two tries")
                    return False
                
            
            # We verify that the quiz number, matches with the desired order from the questionDict
            # First we verify the question number and then we verify the 'Question' text that its presented
            if questionNumberPresented.count(str(x+1)) != 1 and questionNumberPresented.count('Question') != 1:
                writeToLog("INFO", "FAILED, the question " + currentQuestionDetails[2] + " was not found at the number " + str(x+1))
                return False
            
            # We verify that the presented title, matches with the desired one from the questionDict
            if questionTitlePresented != currentQuestionDetails[2]:
                writeToLog("INFO", "FAILED, the following question title was presented: " + questionTitlePresented + " instead of " + currentQuestionDetails[2] + " title that has been given in the dictionary")
                return False
            
            # We verify that the presented time stamp, matches with the desired one from the questionDict
            if questionTimestampPresented != currentQuestionDetails[0]:
                writeToLog("INFO", "FAILED, the question " + currentQuestionDetails[2] + " has been found at timestamp : "  + questionTimestampPresented + " instead of " + currentQuestionDetails[0])
                return False
            
        return True
    
    
    # @Author: Horia Cus
    # This function can change the answer order by drag and drop or shuffle
    # changeAnswerOrderDict must contain a list for each question that needs to be modified
    # changeAnswerOrderDict = {'1':answerOrderOne} 
    # This list is used in order to change the answer order using drag and drop
    # index 0 = question title that must be found while hovering over the quiz question bubble
    # index 1 = question answer that we want to move to a different location
    # index 2 = question location where we want to move index 1
    # answerOrderOne        = ['question #1 Title', 4, 1] ( answer from place four will be moved to the 1st place ) 
    # This list is used in order to verify that the answer options are displayed in the desired order
    # answerListOrderOne    = ['question #1 option #4', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3']
    # This dictionary is used in order to verify the answer list order : verifyAnswerOrderDict = {'1':answerListOrderOne}
    # If shuffle == True, there's no need to have an expectedAnswerListDict
    def changeAnswerOrder(self, changeAnswerOrderDict, expectedAnswerListDict, shuffle=False, tries=3):
        self.switchToKeaIframe()
        # Verify that we are in the KEA editor
        if self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 15, True) == False:
            writeToLog("INFO", "FAILED to find any quiz question pointer in the time line section")
            return False
        
        # Take all the available quiz question pointers from the timeline KEA section
        quizCuePoint = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
        
        # Iterate each available question
        for questionNumber in changeAnswerOrderDict:
            
            # Take the details for the current question
            questionDetails = changeAnswerOrderDict[questionNumber]
            
            # Create the locator for the current question
            questionCuePoint = quizCuePoint[int(questionNumber) - 1]
            
            action = ActionChains(self.driver)
            # Hover over the current question
            try:
                action.move_to_element(questionCuePoint).pause(1).perform()
            except Exception:
                writeToLog("INFO", "FAILED to hover over the quiz " + questionDetails[0])
                return False
            
            # Take the presented title from the hovered question
            questionTitlePresented = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE, 5, True)
            
            # Verify that the question title was presented
            if questionTitlePresented == False:
                writeToLog("INFO", "FAILED to take the question title")
                return False
            else:
                questionTitlePresented = questionTitlePresented.text
            
            
            # Verify that the presented title is present also in our question details list
            if questionTitlePresented in questionDetails:
                # Enter in the quiz question editing screen
                if self.clickElement(questionCuePoint) == False:
                    writeToLog("INFO", "FAILED to select the question cue point for " + questionDetails[0])
                    return False
                
                numberOfAnswers     = str(len(self.wait_elements(self.KEA_TIMELINE_SECTION_DRAG_HAND, 3)))
                availableAnswers    = self.wait_elements(self.KEA_TIMELINE_SECTION_DRAG_HAND, 3)
                
                if shuffle == True:
                    count = 0
                    while True or count <= tries:
                        # Take the current answer list presented, in order to verify that after we use the shuffle option, the list will change
                        answerListPresentedFirst = self.extractAnswersListPresented()
                        
                        # Trigger the shuffle option
                        if self.click(self.KEA_QUIZ_SHUFFLE_BUTTON, 1, True) == False:
                            writeToLog("INFO", "FAILED to click on the shuffle button")
                        
                        # Verify that the answer order is changed
                        if self.verifyAnswersOrder(answerListPresentedFirst, shuffle=True) == False:
                            count += 1
                            writeToLog("INFO", "During the " + str(count) + " try, the same answer order has been displayed, going to retry")  
                            if count > tries:
                                writeToLog("INFO", "FAILED, the shuffle option has no functionality")
                                return False
                        else:
                            break                   
                    
                elif shuffle == False:               
                    # Verify that the answer number is available in the presented answer list
                    if questionDetails[2] > int(numberOfAnswers):
                        writeToLog("INFO", "FAILED, only " + numberOfAnswers + " number of answers are available, instead of " + str(questionDetails[2]))
                        return False
                    
                    # Create the element for the answer that we want to move
                    answerToBeMoved   = availableAnswers[questionDetails[1] - 1]
                    # Create the element for the place where we want to move our answer
                    # If we want to move the answer lower, we must specify only the answer that it should replace
                    if questionDetails[1] < questionDetails[2]:
                        placeToBeMoved     = availableAnswers[questionDetails[2] - 1]
                    
                    # If we want to move the answer higher, we must specify two location upper than the one where it would be placed
                    elif questionDetails[1] > questionDetails[2]:
                        # If the answer should be moved to the first position, we will use quiz question title as pointer
                        if questionDetails[2] == 1:
                            placeToBeMoved = self.wait_element(self.KEA_QUIZ_QUESTION_FIELD, 1, True)
                        else:
                            placeToBeMoved     = availableAnswers[questionDetails[2] - 2]
                    
                    # Move the answer to the desired new location
                    try:
                        action.move_to_element(answerToBeMoved).pause(1).drag_and_drop(answerToBeMoved, placeToBeMoved).perform()
                        action.reset_actions()
                    except Exception:
                        writeToLog("INFO", "FAILED to hover over the quiz " + questionDetails[1])
                        return False
                    
                    # Create the list attribute in order to verify that the answer order has been changed successfully
                    answerList = expectedAnswerListDict[questionNumber]
                    
                    # Verify that the answer order has been changed successfully
                    if self.verifyAnswersOrder(answerList) == False:
                        return False                   
                    
                # Save the changes
                if self.saveQuizChanges() == False:
                    writeToLog("INFO", "FAILED to save the Quiz changes for " + questionDetails[1] + " question")
                    return False

            else:
                writeToLog("INFO", "FAILED to find the " + questionDetails[0] + " because the " + questionTitlePresented + " was presented")
                return False

        writeToLog("INFO", "Quiz answer's order has been changed successfully")
        return True
    

    # @Author: Horia Cus
    # This function will click on the save button and wait until the changes are saved
    def saveQuizChanges(self):
        # We save the KEA Quiz Question
        if self.keaQuizClickButton(enums.KeaQuizButtons.SAVE) == False:
            writeToLog("INFO","FAILED to click on the save button")
            return False  
        
        # We wait until the changes were successfully saved
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 35) == False:
            writeToLog("INFO","FAILED to wait until spinner isn't visible")
            return False 
        
        sleep(1)
        
        return True
    

    # @Author: Horia Cus
    # This function will verify that the answer that are presented matches with the answerList
    # answerList = contains a list with all the available answers and the correct order
    def verifyAnswersOrder(self, answerList, shuffle=False):
        # Take the answer list presented
        answerListPresented = self.extractAnswersListPresented()
        
        # Verify that the answer list that was first presented, no longer matches with the answer list that is now presented
        if shuffle == True:
            if answerListPresented == answerList:
                writeToLog("INFO", "The shuffle option kept the same structure")
                return False
        
        # Verify that the answer list presented, matches with our desired answer list
        else:
            if answerListPresented != answerList:
                writeToLog("INFO", "FAILED, the answer order doesn't match with the answer dictionary")
                return False                     

        writeToLog("INFO", "Answer order is properly displayed")
        return True
    

    # @Author: Horia Cus
    # This function will iterate through each answer field and return a list with all the available answers in the order that they were found
    def extractAnswersListPresented(self):
        answerFields = self.wait_elements(self.KEA_QUIZ_ANSWER_GENERAL, 1)
        answerListPresented = []
        
        if answerFields == False:
            writeToLog("INFO", "FAILED to take the elements for the answers")
            return False
        
        # We iterate throguh each available answer field
        for x in range(0, len(answerFields)):
            # Select the answer input field
            if self.clickElement(answerFields[x]) == False:
                writeToLog("INFO", "FAILED to click on the answer field")
                return False
            
            # Copy the answer text in clipboard
            self.send_keys_to_element(answerFields[x], Keys.CONTROL + 'a')
            self.send_keys_to_element(answerFields[x], Keys.CONTROL + 'c')
            
            # Take the answer text from clipboard
            answerText = self.clsCommon.base.paste_from_clipboard()
            
            # Add the answer text to answer list
            answerListPresented.append(answerText)
        
        return answerListPresented
    
    

    # @Author: Horia Cus
    # This function can change the question order from the KEA timeline section by moving in forward and / or backwards
    # changeTimelineOrderDict = is a dictionary that contains as key the Quiz Number and as value the amount of seconds that we want to move the question forward and / or backwards
    # e.g changeTimelineOrderDict = {'1':3, '2':2, '3':1}, question one will be moved by three seconds
    # This function will not change the timeline properly if the zoom in / zoom out has been used
    def changeQuestionOrderInTimeline(self, changeTimelineOrderDict):
        self.switchToKeaIframe()
        # Verify that we are in the KEA editor
        if self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 15, True) == False:
            writeToLog("INFO", "FAILED to find any quiz question pointer in the time line section")
            return False
        
        sleep(5)        
        # Iterate each available question
        for questionNumber in changeTimelineOrderDict:
            # Take all the available quiz question pointers from the timeline KEA section
            quizCuePoint = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 15)
            
            # Take the details for the current question ( number of seconds that the quiz should be moved by )
            questionDetails = changeTimelineOrderDict[questionNumber]
            
            # Create the locator for the current question
            questionCuePoint = quizCuePoint[int(questionNumber) - 1]
            
            # Move the quiz number to a new timeline location
            try:
                ActionChains(self.driver).move_to_element(questionCuePoint).click().pause(2).drag_and_drop_by_offset(None,35.7*questionDetails, 0).perform()
            except Exception:
                writeToLog("INFO", "FAILED to move question number " + str(questionNumber)  + " by " + str(questionDetails) + " seconds")
                return False
            
            # Save the new timeline location
            if self.saveQuizChanges() == False:
                writeToLog("INFO", "FAILED to save the new timeline location for  " + str(questionNumber)  + " question number")
                return False
            
            if self.clickDone(enums.KeaQuizButtons.EDIT_QUIZ) == False:
                writeToLog("INFO", "FAILED to save the new timeline location for  " + str(questionNumber)  + " question number")
                return False
                        
        return True
    

    # @Author: Horia Cus
    # This function will verify that the entry can be played in KEA Editor and KEA Quiz page
    # Verify that the entire entry can be watched from the beginning till the end
    # Increment tries by one for each 15 seconds of the entry ( e.g Entry = 30 seconds, tries=2 )
    def verifyPlayingProcess(self, tries=2):
        self.switchToKeaIframe()
        # Verify that we are in the KEA editor
        if self.wait_element(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 15, True) == False:
            writeToLog("INFO", "FAILED to find the KEA player play button")
            return False
        
        # Take the entry time
        entryTotalTime = self.wait_element(self.EDITOR_TOTAL_TIME, 1, True).text.replace(" ", "")[1:]
        
        # Because the video resumes back to zero before the last second to be displayed, we have to issue this variable
        if entryTotalTime[3:] == '00':
            # with changes to the mm
            entryTotalTimeVerify = str(int(entryTotalTime[:2])-1) + ':59'
        else:
            # with changes to ss
            entryTotalTimeVerify = entryTotalTime[:3] + str(int(entryTotalTime[3:])-1)
        
        # Time presented inside the timeline cursor
        realTimeMarker = self.wait_element(self.EDITOR_REALTIME_MARKER, 1, True).text[:5]
        
        # Verify if we are at the beginning of the entry
        if self.resumeFromBeginningKEA(forceResume=False) == False:
            writeToLog("INFO", "FAILED to start the entry from the beginning")
            return False
        
        # Trigger the playing process
        if self.click(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 2, True) == False:
            writeToLog("INFO", "FAILED to click on the KEA play button")
            return False
        sleep(1)
        
        # Wait until the loading spinner is no longer present
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_QUIZ_PLAYER, 30) == False:
            writeToLog("INFO", "FAILED to load the KEA entry video playing process")
            return False
        
        # Set the real time to second one
        x = 1
        realtTimeMakerElement = self.wait_element(self.EDITOR_REALTIME_MARKER, 1, True)
        
        # Wait until the timeline cursor reached the first second
        startTimeLine = '00:00'
        while startTimeLine == realTimeMarker:
            startTimeLine = realtTimeMakerElement.text[:5]
        
        # Because the speed for the playing process is higher than the loop run, we increment the number of tries by one for each 15 seconds
        attempt = 0
        
        # We let the playing process to run until we reach the end of the entry
        while realTimeMarker != entryTotalTimeVerify:
            # We take the presented time from timeline cursor     
            realTimeMarkerUpdated = realtTimeMakerElement.text[:5]
            
            # We take the real time based on 1 second of sleep and number of iteration from X
            realTime = str(datetime.timedelta(seconds=x))[2:]
            
            writeToLog("INFO", "AS Expected, Current time present in the marker " + str(realTimeMarkerUpdated) + " real time expected" + realTime)
            # Verify that the presented time from the timeline cursor, matches with the expected time
            if realTimeMarkerUpdated != realTime:
                attempt += 1
                writeToLog("INFO", "AS Expected, Presented time " + realTimeMarkerUpdated + " expected" + realTime + " during the " + str(attempt) + " attempt")

                # For each 15 seconds, 1 try should be passed, if the number of attempts is higher than tries, will return false
                if attempt > tries:
                    writeToLog("INFO", "Timeline time was: " + realTimeMarkerUpdated + " and " + realTime + " was expected")
                    return False 
                # Take the presented time from the timeline cursor in order to compare it with entry total time
                realTimeMarker = realtTimeMakerElement.text[:5]
            else:
                # Take the presented time from the timeline cursor in order to compare it with entry total time
                realTimeMarker = realtTimeMakerElement.text[:5]
                sleep(1)
            
            # Increment the real time by one for each run
            x += 1
            
        writeToLog("INFO", "The entire entry has been successfully watched")
        return True

        
    # @Author: Horia Cus
    # This function will refresh the page if the playing process is already started or if the user is at a different time within the timeline than zero
    def resumeFromBeginningKEA(self, forceResume=False):     
        self.switchToKeaIframe()

        # Verify if any of the elements that indicates if the user is at the beginning of entry is present or not
        if self.wait_element(self.EDITOR_REALTIME_MARKER, 1, True).text != '00:00.00' or self.wait_element(self.KEA_PLAYER_CONTROLS_PAUSE_BUTTON, 1) != False or forceResume == True:
            # Refresh the page  
            self.driver.refresh()
            
            # Change the iframe to default in order to be able to resume to KEA iframe
            self.clsCommon.base.switch_to_default_content()
            self.switchToKeaIframe()
            
            # Verify that the KEA page has been loaded successful
            if self.wait_element(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 15, True) == False:
                writeToLog("INFO", "FAILED to find the KEA player play button")
                return False
        
        return True
    

    # @Author: Horia Cus
    # This function verifies that the user is able to navigate forward and backwards to each quiz question using navigation buttons
    # Verify that the proper question number and time stamp are displayed
    def verifyKEANavigation(self):
        self.switchToKeaIframe()
        # Verify that we are in the KEA Page
        if self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 30, True) == False:
            writeToLog("INFO", "FAILED to find any quiz question pointer in the time line section")
            return False
        
        # Verify if we are at the beginning of the entry
        if self.resumeFromBeginningKEA(forceResume=False) == False:
            writeToLog("INFO", "FAILED to start the entry from the beginning")
            return False
        
        # We take all the available quiz question pointers from the timeline KEA section
        presentedQuestionsInTimeline = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
        
        presentedQuestionDict = {}
        
        # Navigate to each Quiz Question using next option
        for x in range(0, len(presentedQuestionsInTimeline)):
            # Navigate to the next available question
            if self.click(self.KEA_PLAYER_CONTROLS_NEXT_ARROW_BUTTON, 15, True) == False:
                writeToLog("INFO", "FAILED to navigate to the " + str(x+1) + " question field")
                return False
            
            # Take the details for the current question
            try:
                presentedQuestionNumber = self.wait_element(self.KEA_ADD_NEW_QUESTION_NUMBER, 5, True).text
                presentedQuestionTime = self.wait_element(self.EDITOR_REALTIME_MARKER, 5, True).text
            except Exception:
                writeToLog("INFO", "FAILED to take the details after returning back to the first question")
                return False
            
            # Verify that the expected question number is displayed 
            if presentedQuestionNumber.count(str(x+1)) == 0:
                writeToLog("INFO", "FAILED, question number " + str(x+1) + " was expected, instead " + presentedQuestionNumber + " is presented")
                return False
            
            # Add the Question details inside the dictionary
            presentedQuestionDict.update({presentedQuestionNumber:presentedQuestionTime})
        
        # Navigate back to the first question, using next arrow at the end of the last available question
        if self.click(self.KEA_PLAYER_CONTROLS_NEXT_ARROW_BUTTON, 15, True) == False:
            writeToLog("INFO", "FAILED to navigate to the " + str(x+1) + " question field")
            return False
        
        # Take the details back from the first question
        try:
            presentedQuestionNumber = self.wait_element(self.KEA_ADD_NEW_QUESTION_NUMBER, 5, True).text
            presentedQuestionTime   = self.wait_element(self.EDITOR_REALTIME_MARKER, 5, True).text
        except Exception:
            writeToLog("INFO", "FAILED to take the details after returning back to the first question")
            return False
        
        # Verify that the user was resumed back to the first question   
        if presentedQuestionNumber.count('1') != 1:
            writeToLog("INFO", "FAILED, to resume to the first question after iterating all of the available Quiz Questions")
            return False
        
        # Verify that the first time stamp that was presented matches with the current one
        if presentedQuestionDict[presentedQuestionNumber] != presentedQuestionTime:
            writeToLog("INFO", "FAILED, at first the " + presentedQuestionDict[presentedQuestionNumber] + " was present and now " + presentedQuestionTime + " time is presented")
            return False
        
        presentedQuestionDictPrevious = {}
        i = len(presentedQuestionDict)
        for x in range(0, len(presentedQuestionDict)):
            # Navigate to the previous question
            if self.click(self.KEA_PLAYER_CONTROLS_PREVIOUS_ARROW_BUTTON, 5, True) == False:
                writeToLog("INFO", "FAILED to navigate using previous arrow")
                return False
            
            # Take the details for the current question
            try:
                presentedQuestionNumber = self.wait_element(self.KEA_ADD_NEW_QUESTION_NUMBER, 5, True).text
                presentedQuestionTime   = self.wait_element(self.EDITOR_REALTIME_MARKER, 5, True).text
            except Exception:
                writeToLog("INFO", "FAILED to take the details after returning back to the first question")
                return False
            
            # Verify that the expected question number is displayed 
            if presentedQuestionNumber.count(str(i)) == 0:
                writeToLog("INFO", "FAILED, question number " + str(x+1) + " was expected, instead " + presentedQuestionNumber + " is presented")
                return False
            
            # Add the Question details inside the dictionary
            presentedQuestionDictPrevious.update({presentedQuestionNumber:presentedQuestionTime})
            
            i -= 1
        
        # Verify that all the available Quiz Question were navigated forward and backward
        if len(presentedQuestionDict) != len(presentedQuestionsInTimeline) or len(presentedQuestionDictPrevious) != len(presentedQuestionsInTimeline):
            writeToLog("INFO", "FAILED " + str(len(presentedQuestionDict)) + " questions were found while navigating forward, " + str(len(presentedQuestionDictPrevious)) + " were found while navigating backwards, and " + len(presentedQuestionsInTimeline) + " were presented"  )
            return False

        writeToLog("INFO", "PASSED, all the quiz questions were properly navigated forward and backward")
        return True
    
    
    # @Author: Horia Cus
    # This function will verify the KEA Timeline section and Navigation while using the zoom option
    # Zoom option will be used by using the Zoom Level pointer forward and backwards
    # Question Cue Point distance is verified after each zoom in call
    # KEA Timline Container size is verified after each zoom in call
    # KEA Zoom Level Pointer is verified after each zoom in call
    def verifyZoomLevelInTimeline(self):
        self.switchToKeaIframe()
        # Verify that we are in the KEA Page
        if self.wait_element(self.KEA_TIMELINE_SECTION_CONTAINER, 30, True) == False:
            writeToLog("INFO", "FAILED to find the KEA Timeline section")
            return False
        
        # Taking the default size of the timeline container
        containerDefaultSize = self.wait_element(self.KEA_TIMELINE_SECTION_CONTAINER, 30, True).size['width']
        
        # Taking the zoom level elements
        zoomLevelDefault        = (self.KEA_TIMELINE_CONTROLS_ZOOM_LEVEL_POINTER_VALUE[0], self.KEA_TIMELINE_CONTROLS_ZOOM_LEVEL_POINTER_VALUE[1].replace('VALUE', str(0)))
#         zoomInButtonElement     = self.wait_element(self.KEA_TIMELINE_CONTROLS_ZOOM_IN_BUTTON, 5, True)
        zoomOutButtonElement    = self.wait_element(self.KEA_TIMELINE_CONTROLS_ZOOM_OUT_BUTTON , 5, True)
        zoomLevelPointer        = self.wait_element(self.KEA_TIMELINE_CONTROLS_ZOOM_LEVEL_POINTER, 5, True)
        
        # Verify that we are at the beginning of the timeline section
        if self.wait_element(zoomLevelDefault, 5, True) == False:
            writeToLog("INFO", "FAILED to find the KEA Timeline Zoom Level Pointer at the initial location ( beginning )")
            return False
        
        action = ActionChains(self.driver)
        
        # Create a list that will be used in order to compare the initial size of a Question with the updated one after using the zoom option
        questionListPresented = []
        
        # Use the zoom option until reaching the maximum length available
        for x in range(0,15):
            # Incrementing the zoom in option
            zoomInPosition = x*5
            # Taking the Zoom Pointer location before using the zoom option
            pointerInitial  =  self.wait_element(self.KEA_TIMELINE_CONTROLS_ZOOM_LEVEL_POINTER, 1, True).location['x']
            
            # Taking the Timeline Container size before using the zoom option
            containerInitialSize = int(self.wait_element(self.KEA_TIMELINE_SECTION_CONTAINER, 30, True).size['width'])
            
            # Verify if Questions are created within the timeline section
            if self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_CONTAINER, 1) != False:
                # Take all the available questions
                presentedQuestions = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_CONTAINER, 1)
                # Add question's position inside a list
                for i in range (0, len(presentedQuestions)):  
                    # Take the location attribute from the active question
                    presentedQuestion = presentedQuestions[i].get_attribute('style').split()[1]
                    # Convert the location attribute in integer
                    presentedQuestionPosition = int(re.search(r'\d+', presentedQuestion).group())
                    # Add the question location inside the question List
                    questionListPresented.append(presentedQuestionPosition)
                
                # Verify that at least one time the Zoom option has been used
                if len(questionListPresented) > len(presentedQuestions):
                    # Comparing the last two sets of Questions ( before zoom option / after zoom option) and verify that the second set has a higher location
                    # Take the last before / after zoom in list elements
                    compareList = questionListPresented[-len(presentedQuestions)*2:]
                    for k in range(0,len(presentedQuestions)-1):
                        # Verify that the list that was created after zoom option has a higher location than the list that was created before that
                        if compareList[k] > compareList[k+len(presentedQuestions)]:
                            writeToLog("INFO", "FAILED, question number " + str(k+1) + " has been found at " + str(questionListPresented[k]) + " before zoom in, and at " + str(questionListPresented[k+len(presentedQuestions)]) + " after zoom in")
                            return False
                                                                                                                                                                                             
            # Use the zoom in option, by drag and drop of Zoom Level Pointer element
            try:
                action.move_to_element(zoomLevelPointer).click_and_hold(zoomLevelPointer).move_to_element_with_offset(zoomOutButtonElement, 45+zoomInPosition, 0).release().pause(1).perform()
#                 action.reset_actions()
                sleep(2)
            except Exception:
                writeToLog("INFO", "FAILED to use zoom in option properly at the " + str(x+1) + " try")
                return False
            
            # Take the Location for Zoom option Pointer after using the zoom in option
            pointerUpdated          =  self.wait_element(self.KEA_TIMELINE_CONTROLS_ZOOM_LEVEL_POINTER, 1, True).location['x']
            # Take the Timeline Container size after using the zoom in option
            containerUpdatedSize    =  int(self.wait_element(self.KEA_TIMELINE_SECTION_CONTAINER, 30, True).size['width'])
            
            # Verify that the Timeline pointer location has been changed after using the zoom in option
            if pointerInitial >= pointerUpdated:
                writeToLog("INFO", "FAILED, Zoom Level pointer was set at " + str(pointerInitial) + " and we expected " + str(pointerUpdated))
                return False
            
            # Verify that the Timeline container size is bigger after using the zoom in option
            if containerInitialSize >= containerUpdatedSize:
                writeToLog("INFO", "FAILED, Zoom Level pointer was set at " + str(pointerInitial) + " and we expected " + str(pointerUpdated))
                return False
                       
        # Use the zoom out option, by drag and drop of Zoom Level Pointer element, in order to reach zero state
        try:
            action.move_to_element(zoomLevelPointer).click_and_hold(zoomLevelPointer).move_to_element(zoomOutButtonElement).release(zoomLevelPointer).perform()
        except Exception:
            writeToLog("INFO", "FAILED to use zoom out option till the end")
            return False
        sleep(2)
        
        containerZoomedOutSize    =  int(self.wait_element(self.KEA_TIMELINE_SECTION_CONTAINER, 30, True).size['width'])  
        
        # Verify that the Initial Timeline Container size is the same after using the zoom in and zoom out option
        if containerDefaultSize != containerZoomedOutSize:
            writeToLog("INFO", "FAILED, the default Timeline size container was " + str(containerDefaultSize) + " and after we moved back to the initial position using zoom out option, it was " + str(containerZoomedOutSize))
            return False
        
        # Verify that the Zoom Level pointer is displayed back at the beginning of the bar
        if self.wait_element(zoomLevelDefault, 5, True) == False:
            writeToLog("INFO", "FAILED, the Zoom Level Pointer was not set back to the original position")
            return False  
        
        writeToLog("INFO", "Zoom Level has been successfully verified inside the KEA timeline section")
        return True
    
    
    # @Author: Horia Cus
    # This function can delete any available Question displayed in the KEA Timeline section
    # questionDeleteList must contain only the string of the Question Title
    # E.g questionDeleteList = ['Quesion Title 1', 'Question Title 5']
    def deleteQuestions(self, questionDeleteList):
        self.switchToKeaIframe()
        # Verify that we are in the KEA Page
        if self.wait_element(self.KEA_TIMELINE_SECTION_CONTAINER, 30, True) == False:
            writeToLog("INFO", "FAILED to find the KEA Timeline section")
            return False
        
        
        # Take all the available quiz question cue points from the KEA Timline section
        presentedInitialCuePointsInTimeline = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
        presentedUpdatedCuePointsInTimeline = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
        
        i = 0
        # Iterate through each Question that needs to be deleted
        for questionToBeDeleted in questionDeleteList:
            # Used in order to verify the number of Questions in Timeline section after we delete them
            i += 1
            
            # Iterate through each Question Cue Point until finding the desired Question and delete it
            for x in range(0, len(presentedUpdatedCuePointsInTimeline)):
                
                # Create the element for the current Question Cue Point
                questionCuePoint = presentedUpdatedCuePointsInTimeline[x]
                
                # Hover over the current Question Cue Point
                try:
                    ActionChains(self.driver).move_to_element(questionCuePoint).pause(2).perform()
                except Exception:
                    writeToLog("INFO", "FAILED to hover over the quiz " + str(x+1) + " question number Cue Point during the first try")
                    return False
                
                # Take the presented title from the hovered Cue Point
                questionTitlePresented = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE, 5, True)
                
                # Verify that the Question Title is presented while hovering over the Cue Point
                if questionTitlePresented == False:
                    for x in range(0,5):
                        # Add a redundancy step for action chain
                        try:
                            ActionChains(self.driver).move_to_element(questionCuePoint).pause(2).perform()
                        except Exception:
                            writeToLog("INFO", "FAILED to hover over the quiz " + str(x+1) + " question number Cue Point during the second try")
                            return False
                        
                        questionTitlePresented = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE, 5, True)
                        if questionTitlePresented == False:
                            writeToLog("INFO", "FAILED to take the question title from the question cue point number " + str(x+1))
                            return False
                        else:
                            break
                else:
                    try:
                        # Take the Question Title presented on the hovered Cue Point
                        questionTitlePresented = questionTitlePresented.text
                    except Exception:
                        writeToLog("INFO", "FAILED to take the Question Title from the cue point number " + str(x+1) + " while using the element")
                        return False
                    
                # Verify if the Question Title Presented matches with Question Title from given List
                if questionTitlePresented == questionToBeDeleted:
                    # Access the Question Editing page
                    if self.clickElement(questionCuePoint) == False:
                        writeToLog("INFO", "FAILED to select the question cue point number " + str(x+1))
                        return False
                    
                    # Delete the Question
                    deleteButton = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', 'Delete'))
                    if self.click(deleteButton, 5, True) == False:
                        writeToLog("INFO", "FAILED to click on the Question delete button")
                        return False
                    
                    # Wait for two seconds in order to give time for the Cue Point to disappear from KEA Timeline section and break from the loop
                    sleep(2)
                    break
                    
                else:
                    # Verify if the Question that needs to be deleted was found within the maximum amount of tries
                    if x+1 == len(presentedUpdatedCuePointsInTimeline):
                        writeToLog("INFO", "FAILED to find the question: " + questionToBeDeleted + " inside the KEA Timeline section")
                        return False
                    
            # Take the current number of Question Cue Points
            presentedUpdatedCuePointsInTimeline = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
            
            # Verify that the KEA Timeline section has been updated properly with the correct number of Question Cue Points
            if len(presentedUpdatedCuePointsInTimeline)+i != len(presentedInitialCuePointsInTimeline):
                writeToLog("INFO", "FAILED, after we deleted question " + questionToBeDeleted + " we expected " + len(presentedUpdatedCuePointsInTimeline) + " question numbers in timeline, but " + len(presentedInitialCuePointsInTimeline) + " are displayed")
                return False

        questionsDeleted = ", ".join(questionDeleteList)
        writeToLog("INFO","The following Questions were deleted: " + questionsDeleted)
        return True
    
    
    # @Author: Horia Cus
    # This function can use any action option available for the KEA Editor ( Undo, Redo and Reset)
    # It will verify that the KEA Section is presented with the proper time length, size and number of sections based on the action selected
    # actionToBePerformed must contain enums ( e.g enums.KeaEditorTimelineOptions.REDO )
    def timeLineUndoRedoReset(self, actionToBePerformed):
        self.switchToKeaIframe()
        
        # Verify that we are in the KEA Page
        if self.wait_element(self.KEA_TIMELINE_SECTION_CONTAINER, 30, True) == False:
            writeToLog("INFO", "FAILED to find the KEA Timeline section")
            return False
        
        # Take the KEA Timeline section details before performing any action
        presentedSectionsInitial       = self.wait_elements(self.KEA_TIMELINE_PRESENTED_SECTIONS, 5)
        sectionListSizesInitial        = []
        sectionListTotalTimeInitial    = []
        presentedTotalTimeInitial      = self.wait_element(self.EDITOR_TOTAL_TIME_TOOLBAR, 2).text.replace('Total:', '')[1:6]
        
        # Take the size of section's container and the time length displayed within each presented section
        for x in range(0, len(presentedSectionsInitial)):
            sectionListSizesInitial.append(int(presentedSectionsInitial[x].size['width']))
            sectionListTotalTimeInitial.append(presentedSectionsInitial[x].text)
        
        # Verify the action that needs to be performed
        if actionToBePerformed == enums.KeaEditorTimelineOptions.RESET:
            
            # Verify that there are elements that can be reset
            if len(presentedSectionsInitial) > 1 or sectionListSizesInitial[x] < 1065:
                
                # Click on the 'Reset' action button
                if self.click(self.EDITOR_TIMELINE_OPTION_RESET, 3, True) == False:
                    writeToLog("INFO", "FAILED to click on the Reset button")
                    return False
                
                # Verify if the confirmation pop up is displayed
                if self.wait_element(self.KEA_CONFIRMATION_POP_UP_TITLE, 3, True) != False:
                    # Confirm the Reset action
                    if self.click(self.KEA_CONFIRMATION_POP_UP_CONTINUE, 1, True) == False:
                        writeToLog("INFO", "FAILED to confirm the Reset option changes")
                        return False
                else:
                    writeToLog("INFO", "No confirmation pop up was presented for the reset action")
                
                # Take the elements for the presented sections
                presentedSectionsUpdated            = self.wait_elements(self.KEA_TIMELINE_PRESENTED_SECTIONS, 5)
                presentedTotalTimeUpdatedForSection = presentedSectionsUpdated[0].text[:5]
                presentedTotalTimeUpdated           = self.wait_element(self.EDITOR_TOTAL_TIME_TOOLBAR, 2).text.replace('Total:', '')[1:6]
                
                # Verify that only one section is presented
                if len(presentedSectionsUpdated) != 1:
                    writeToLog("INFO", "FAILED, " + len(presentedSectionsUpdated) + " sections are displayed, instead of only one, after using the reset option")
                    return False
                
                # Verify that the present section's time matches with the total time of the entry
                if presentedTotalTimeUpdated != presentedTotalTimeUpdatedForSection:
                    writeToLog("INFO", "FAILED, in the timeline section, ")
                    return False
            
            # Return false if no 'Reset' action can be performed 
            else:
                writeToLog("INFO", "FAIFAILED, there's nothing to reset because no changes were performed within the timeline section")
                return False                

        # Verify the action that needs to be performed  
        elif actionToBePerformed == enums.KeaEditorTimelineOptions.REDO:
            
            # Click on the 'Redo' action button
            if self.click(self.EDITOR_TIMELINE_OPTION_REDO, 3, True) == False:
                writeToLog("INFO", "FAILED to click on the Redo button")
                return False
            
            # Wait one second to make sure that the UI is updated
            sleep(1)
            
            # Take the KEA timeline section details after using the 'Redo' option
            presentedSectionsUpdated        = self.wait_elements(self.KEA_TIMELINE_PRESENTED_SECTIONS, 5)
            presentedTotalTimeUpdated       = self.wait_element(self.EDITOR_TOTAL_TIME_TOOLBAR, 2).text.replace('Total:', '')[1:6]
            sectionListSizesUpdated         = []
            sectionListTotalTimeUpdated     = []

            
            # Take the size of section's container and the time length displayed from each presented section
            for x in range(0, len(presentedSectionsUpdated)):
                sectionListSizesUpdated.append(int(presentedSectionsUpdated[x].size['width']))
                sectionListTotalTimeUpdated.append(presentedSectionsUpdated[x].text)
            
            # Verify the 'Redo' action after a Delete
            # Verify that a section has been deleted after using the 'Redo' action
            if len(presentedSectionsUpdated) == len(presentedSectionsInitial) - 1:
                # Verify that the updated total time for the entry is lower after a section has been deleted
                if presentedTotalTimeUpdated > presentedTotalTimeInitial:
                    writeToLog("INFO", "FAILED, the presented total time after using the Redo option for a Delete action, is not lower than the initial total time" )
                    return False
            
            # Verify the 'Redo' action after a Set In / Set Out
            elif len(presentedSectionsUpdated) == len(presentedSectionsInitial):
                # Verify that a section has been set out / set in by checking its size ( set out / set in section remains at 2px width only after a split )
                for x in range(0, len(sectionListSizesUpdated)):
                    if sectionListSizesUpdated[x] < sectionListSizesInitial[x]:
                        break
                    
                    if x + 1 == len(sectionListSizesInitial):
                        writeToLog("INFO", "FAILED, no section has been set out / set in after using the 'Redo' action")
                        return False
                
                # Verify that the time length of the entry has been decreased after resuming a set out / set in section
                if presentedTotalTimeUpdated >= presentedTotalTimeInitial:
                    writeToLog("INFO", "FAILED, the presented total time after using the Redo option for a Set Out / Set In action, is not higher than the initial total time" )
                    return False
            
            # Verify the 'Redo' action after a Split
            # Verify that the number of sections has been increased by one after using the 'Redo' action
            elif len(presentedSectionsUpdated) == len(presentedSectionsInitial) + 1:
                tries = 1
                # Verify that the size for at least two section has been decreased after using the 'Redo' action in order to re-split the sections
                for updatedSize in sectionListSizesUpdated:
                    # Verify that the updatedSize for the section that has been re-split has been changed
                    if updatedSize in sectionListSizesInitial:
                        if len(sectionListSizesUpdated) == tries:
                            writeToLog("INFO", "FAILED, section size has not been properly changed after a split performed by 'Redo'")
                            return False
                        tries += 1
                        
                tries = 1
                # Verify that the time length for at least two section has been decreased after using the 'Redo' action in order to re-split the sections
                for updatedTime in sectionListTotalTimeUpdated:
                    # Verify that the updatedTime for the section that has been re-split has been changed
                    if updatedTime in sectionListTotalTimeInitial:
                        if len(sectionListTotalTimeUpdated) == tries:
                            writeToLog("INFO", "FAILED, section time length has not been properly changed after a split performed by 'Redo'")
                            return False
                        tries += 1            

        # Verify the action that needs to be performed
        elif actionToBePerformed == enums.KeaEditorTimelineOptions.UNDO:
                        
            # Verify that at least one undo input can be performed for the current state
            if len(presentedSectionsInitial) > 1 or sectionListSizesInitial[x] < 1065:
                
                # Click on the 'Undo' action button
                if self.click(self.EDITOR_TIMELINE_OPTION_UNDO, 3, True) == False:
                    writeToLog("INFO", "FAILED to click on the Undo button")
                    return False
                
                # Wait one second to make sure that the UI is updated
                sleep(1)
                
                # Take the KEA timeline section details after using the undo option
                presentedSectionsUpdated = self.wait_elements(self.KEA_TIMELINE_PRESENTED_SECTIONS, 5)
                
                sectionListSizesUpdated     = []
                sectionListTotalTimeUpdated = []
                
                # Take the size of section's container and the time length displayed from each presented section
                for x in range(0, len(presentedSectionsUpdated)):
                    sectionListSizesUpdated.append(int(presentedSectionsUpdated[x].size['width']))
                    sectionListTotalTimeUpdated.append(presentedSectionsUpdated[x].text)
                
                # Verify the 'Undo' action after a SPLIT
                # Verify that a section has been combined after using the 'Undo' action
                if len(presentedSectionsUpdated) == len(presentedSectionsInitial) - 1:
                    
                    # Verify that the section's container size has been increased after using the 'Undo' action
                    for x in range(0, len(presentedSectionsUpdated)):
                        # Compare the initial size with the updated size and verify that the updated size for at least one section's container has been increased
                        if sectionListSizesUpdated[x] > sectionListSizesInitial[x]:
                            writeToLog("INFO", "Size has been increased for a section, after using the undo option, after a split")
                            break
                        
                        # Verify that we were able to find an increase in size within the number of presented sections
                        if x + 1 == len(presentedSectionsUpdated):
                            writeToLog("INFO", "FAILED, after using the split option and then undo, the same number of sections were displayed")
                            return False
                                                                    
                    # Verify that the section's time length has been increased after using the 'Undo' action
                    for x in range(0, len(presentedSectionsUpdated)):
                        # Compare the initial time length with the updated time length and verify that the time length for the updated section has been increased 
                        if sectionListTotalTimeUpdated[x] > sectionListTotalTimeInitial[x]:
                            writeToLog("INFO", "Time length has been increased for a section, after using the undo option, after a split")
                            break
                        
                        # Verify that we were able to find an increase in time length within the number of presented sections
                        else:
                            if x + 1 == len(presentedSectionsUpdated):
                                writeToLog("INFO", "FAILED, after splitting a section and then using the undo option, section time length didn't increased")
                                return False
                        
                # Verify the 'Undo' option after a Set In and / or Set Out
                # Verify that the same number of the presented section remained after using the 'Undo' action
                elif len(presentedSectionsUpdated) == len(presentedSectionsInitial):
                    
                    # Verify that the size of at least one presented section has been increased after combining a set out / set in section
                    for x in range(0, len(presentedSectionsUpdated)):
                        if sectionListTotalTimeUpdated[x] > sectionListTotalTimeInitial[x]:
                            writeToLog("INFO", "Time length has been increased for a section, after using the undo option")
                            break
                        
                        # Verify that we were able to find an increase in size for at least one presented section within the number of presented sections
                        else:
                            if x + 1 == len(presentedSectionsUpdated):
                                writeToLog("INFO", "FAILED, section time has not been increased for any available section, after using the undo option")
                                return False
                
                # Verify the 'Undo' option after a Delete
                # Verify that the number of sections has been increased by one than the initial presented section
                elif len(presentedSectionsUpdated) == len(presentedSectionsInitial) + 1:
                    
                    # Verify that the time length information has been presented for each presented section
                    if len(sectionListTotalTimeUpdated) != len(sectionListTotalTimeInitial) + 1:
                        writeToLog("INFO", "FAILED, after the user deleted a section and used the Undo option, the previously section was not resumed")
                        return False    
                
                # Return False if no criteria was match for the 'Undo' action
                else:
                    writeToLog("INFO", "FAILED, no undo changes were performed")
                    return False
            
            # Return False if no elements can be undo            
            else:
                writeToLog("INFO", "FAILED, no undo option is available for the current state")
                return False
            
        writeToLog("INFO", "KEA Timeline option has been successfully changed using the " + actionToBePerformed.value + " option")
        return True
    
    
    # @Author: Horia Cus
    # This function will save the current entry with the latest changes performed within the KEA Editor Timeline
    # if saveCopy = False, it will save the current entry with the latest changes performed
    # if saveCopy = True, it will save the changes from the entry in a new entry
    def saveEditorChanges(self, saveCopy=False):
        self.switchToKeaIframe()
        
        # Save the current entry with all the changes that were performed within the KEA Timeline section  
        if saveCopy == False:
            if self.click(self.EDITOR_SAVE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on the save Button from KEA Editor")
                return False
            
            if self.click(self.EDITOR_SAVE_BUTTON_CONF, 1, True) == False:
                writeToLog("INFO","FAILED to confirm the save pop up from KEA Editor")
                return False
            
            if self.wait_element(self.EDITOR_SAVED_MSG, 360) == False:
                writeToLog("INFO","FAILED, ""Media was successfully saved."" - was not presented within the 360 seconds")
                return False
            
            if self.click(self.EDITOR_SAVED_OK_MSG, multipleElements=True) == False:
                writeToLog("INFO","FAILED to dismiss the confirmation pop up by clicking on the OK button")
                return False
            
        # Save the changes that were performed within the KEA Timeline section as a new entry
        elif saveCopy == True:
            if self.click(self.EDITOR_SAVE_A_COPY_BUTTON) == False:
                writeToLog("INFO","FAILED to click on the Save a Copy button from KEA Editor")
                return False
            
            if self.click(self.EDITOR_CREATE_BUTTON, 1, True) == False:
                writeToLog("INFO","FAILED to confirm the save pop up from KEA Editor")
                return False
            
            if self.wait_element(self.EDITOR_SUCCESS_MSG, 360) == False:
                writeToLog("INFO","FAILED, ""Media was successfully saved."" - was not presented within the 360 seconds")
                return False
            
        writeToLog("INFO", "Changes from KEA Editor timeline were saved properly")
        return True
    
    
    # @Author: Horia Cus
    # This function will compare the entry length from Entry Page and KEA Page
    def compareEntryDurationInKeaAndEntryPage(self, entryName, expectedDuration):
        self.switch_to_default_content()
        
        # Navigate to the entry page
        if self.clsCommon.navigateTo(navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA, nameValue=entryName) == False:
            writeToLog("INFO", "FAILED to navigate to the Entry Page for " + entryName + " entry")
            return False
        
        # Wait if the media is still being processed
        if self.clsCommon.entryPage.waitTillMediaIsBeingProcessed() == False:
            writeToLog("INFO", "FAILED to wait until the " + entryName + " has been processed")
            return False
        
        self.clsCommon.player.switchToPlayerIframe()
        
        # Take the entry time length from the player
        try:
            entryDurationInEntryPage = self.wait_element(self.clsCommon.player.PLAYER_TOTAL_VIDEO_LENGTH, 75).text.replace('/','').strip()
        except Exception:
            writeToLog("INFO", "FAILED to take the entry duration from Entry Page for " + entryName + " entry")
            return False
        
        # Going to add one more 0 at the beginning of the entry length if the video has less than 9 minutes in order to match the structure from KEA Page
        if len(entryDurationInEntryPage) == 4 and entryDurationInEntryPage[0] == '0':
            entryDurationInEntryPage = '0'+ entryDurationInEntryPage
            
        self.switch_to_default_content()
        
        # Navigate to the KEA Editor
        if self.launchKEA(entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
            writeToLog("INFO", "FAILED to navigate to the KEA page for " + entryName + " entry")
            return False
        
        self.switchToKeaIframe()
        
        # Take the entry time length from the KEA section
        try:
            entryDurationInKea = self.wait_element(self.EDITOR_TOTAL_TIME, 60).text.replace('/','').strip()
        except Exception:
            writeToLog("INFO", "FAILED to take the entry duration from Entry Page for " + entryName + " entry")
            return False
        
        self.switch_to_default_content()
        
        # Verify that the entry time length it's the same in both KEA Editor and Entry Page
        if entryDurationInEntryPage != entryDurationInKea:
            writeToLog("INFO","FAILED, " + entryDurationInEntryPage + " time has been presented in Entry Page and " + entryDurationInKea + " in KEA page" ) 
            return False
        
        if entryDurationInEntryPage != expectedDuration:
            writeToLog("INFO","FAILED, " + entryDurationInEntryPage + " time has been presented in Entry Page and KEA but " + expectedDuration + " was expected" ) 
            return False
        
        writeToLog("INFO", "Entry duration matches in both Entry Page and KEA Page")
        return True
    
    
    # @Author: Horia Cus
    # hotspotList must contain the following structure ['Hotspot Title', enums.keaLocation.Location, startTime, endTime, 'link.address', enums.textStyle.Style, 'font color code', 'background color code', text size, roundness size, container size]
    # A hotspot list may contain only the hotspot title
    # For the link.address we can have a web page ( e.g https://6269.qakmstest.dev.kaltura.com/ ) and also a time location ( e.g 90, which will translate into 01:30 )
    # If you want to specify only the Title, Location, and Text Size you can put '' string at the options that you don't want to be changed
    # hotspotOne      = ['Hotspot Title One', enums.keaLocation.TOP_RIGHT, 0, 10, 'https://autoone.kaltura.com/', enums.textStyle.BOLD, '#fafafa', '#fefefe', '', '', enums.keaHotspotContainerSize.SMALL]
    # hotspotTwo      = ['Hotspot Title Two', enums.keaLocation.TOP_LEFT, 5, 15, '', enums.textStyle.NORMAL, '', '', 12, 12]
    # hotspotThree    = ['Hotspot Title Three', enums.keaLocation.CENTER, 15, 20, 'https://autothree.kaltura.com/', enums.textStyle.THIN, '', '', 12, 12]
    # hotspotFour     = ['Hotspot Title Four', enums.keaLocation.BOTTOM_RIGHT, 20, 25, '', enums.textStyle.THIN, '', '', 12, 16]
    # hotspotFive     = ['Hotspot Title Five', enums.keaLocation.BOTTOM_LEFT, 25, 30, '', enums.textStyle.BOLD, '', '', 18, 16]
    # hotspotsDict    = {'1':hotspotOne,'2':hotspotTwo, '3':hotspotThree, '4':hotspotFour, '5':hotspotFive}
    # hotspotsDict must contain the following structure  = {'1':hotspotOne,'2':hotspotTwo}
    # creationType = the type of the method that will be used in order to select the start time / end time of the hotspot ( end time is supported only for Cue Point method)
    def hotspotCreation(self, hotspotsDict, openHotspotsTab=False, creationType=enums.keaHotspotCreationType.VIDEO_PAUSED):
        self.switchToKeaIframe()  
        # Navigate to the Hotspot tab if needed
        if openHotspotsTab == True:
            if self.launchKEATab('', enums.keaTab.HOTSPOTS) == False:
                writeToLog("INFO", "FAILED to navigate to the KEA Hotsptos tab")
                return False
        
        # Create all the desired Hotspots
        for hotspotNumber in hotspotsDict:
            
            # Take the details for the current hotspot
            hotspotDetails = hotspotsDict[hotspotNumber]
            
            if creationType == enums.keaHotspotCreationType.VIDEO_PLAYING:
                if self.playEntryAndReturnAtTime(hotspotDetails[2]) == False:
                    return False
            
            # Verify if the font color should be changed
            if len(hotspotDetails) > 1 and hotspotDetails[1] != '':
                if self.hotspotLocation(hotspotDetails[1]) == False:
                    writeToLog("INFO", "FAILED to change the location for " + hotspotDetails[0] + " to " + hotspotDetails[1])
                    return False
                    
            else:
                # Create a new hotspot
                if self.click(self.KEA_HOTSPOTS_ADD_NEW_BUTTON, 1, True) == False:
                    writeToLog("INFO", "FAILED to click on the Add new Button")
                    return False
                
                # Verify that the video playing process stopped after clicking on the Add New Hotspot
                if creationType == enums.keaHotspotCreationType.VIDEO_PLAYING:
                    if self.wait_element(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 1, True) == False:
                        writeToLog("INFO", "FAILED, the Video Playing process didn't stopped after clicking on ADD New Hotspot")
                        return False
            
            if self.click(self.KEA_HOTSPOTS_ADVANCED_SETTINGS, 1, True) == False:
                writeToLog("INFO", "FAILED to activate the Advanced Settings for Hotspots")
                return False
            
            # Insert the text for the current hotspot
            if self.click_and_send_keys(self.KEA_HOTSPOTS_FORM_TEXT_INPUT_FIELD, hotspotDetails[0], True)== False:
                writeToLog("INFO", "FAILED to insert " + hotspotDetails[0] + " text inside the Text Field")
                return False
            
            # Verify if a link should be inserted
            if len(hotspotDetails) > 4:
                if hotspotDetails[4] != '':
                    # Verify if the link is to a web page
                    if type(hotspotDetails[4]) is str:
                        sleep(0.2)
                        if self.click(self.KEA_HOTSPOTS_FORM_LINK_TYPE_URL, 1, True) == False:
                            writeToLog("INFO", "FAILED to click on the URL label")
                            return False
                        
                        if self.click_and_send_keys(self.KEA_HOTSPOTS_FORM_LINK_INPUT_FIELD, hotspotDetails[4], True) == False:
                            writeToLog("INFO", "FAILED to insert " + hotspotDetails[4] + " link inside the Link Field")
                            return False
                        
                    # Verify if the link needs to be set to a time location of the entry
                    elif type(hotspotDetails[4]) is int:
                        if self.click(self.KEA_HOTSPOTS_FORM_LINK_TYPE_TIME, 1, True) == False:
                            writeToLog("INFO", "FAILED to click on the Time label")
                            return False
                        
                        # time string has format mm:ss
                        timeString = str(datetime.timedelta(seconds=hotspotDetails[4]))[2:]
                        
                        if self.clear_and_send_keys(self.KEA_HOTSPOTS_FORM_LINK_INPUT_FIELD_TIME, timeString, True) == False:
                            writeToLog("INFO", "FAILED to insert the " + timeString + " time inside the Link Input time field of the hotspot")
                            return False
                        sleep(0.3)
                        
                    else:
                        writeToLog("INFO", "FAILED, invalid format used while trying to specify a LINK for the hotspot")
                        return False
            
            # Verify if the font style should be changed
            if len(hotspotDetails) > 5:
                if hotspotDetails[5] != '':
                    textStyle = (self.KEA_HOTSPOTS_FORM_TEXT_STYLE_VALUE[0], self.KEA_HOTSPOTS_FORM_TEXT_STYLE_VALUE[1].replace("TEXT_STYLE",  hotspotDetails[5].value))
                    if self.click(self.KEA_HOTSPOTS_FORM_TEXT_STYLE, 1, True) == False:
                        writeToLog("INFO", "FAILED to activate the Text Color drop down menu")
                        return False
                    
                    if self.click(textStyle, 1, True)== False:
                        writeToLog("INFO", "FAILED to select the font style for  " + hotspotDetails[0] + " as " + hotspotDetails[5].value)
                        return False
            
            # Verify if the font color should be changed
            if len(hotspotDetails) > 6:
                # Because Font Color and Background Color field have the same locators we use indexing [0] = Font color [1] = Background Color
                colorPicker = self.wait_elements(self.KEA_HOTSPOTS_FORM_COLOR, 1)
                if colorPicker == False:
                    writeToLog("INFO", "FAILED to find the color picker option")
                    return False
                
                if hotspotDetails[6] != '':
                    if self.clickElement(colorPicker[0]) == False:
                        writeToLog("INFO", "FAILED to click on the Hotspot Font Color button")
                        return False
                    
                    if self.clear_and_send_keys(self.KEA_HOTSPOTS_FORM_COLOR_VALUE, hotspotDetails[6], True) == False:
                        writeToLog("INFO", "FAILED to select the font color for  " + hotspotDetails[0] + " as " + hotspotDetails[6].value)
                        return False
                    
                    if self.clsCommon.sendKeysToBodyElement(Keys.ENTER) != True:
                        writeToLog("INFO", "FAILED to save the color by clicking on the enter button")
                        return False
                    
                    if self.clickElement(colorPicker[0]) == False:
                        writeToLog("INFO", "FAILED to collapse the Hotspot Font Color tool tip menu")
                        return False
                    
            # Verify if the background color should be changed
            if len(hotspotDetails) > 7:
                if hotspotDetails[7] != '':
                    if self.clickElement(colorPicker[1]) == False:
                        writeToLog("INFO", "FAILED to click on the Background Color button")
                        return False
                    
                    if self.clear_and_send_keys(self.KEA_HOTSPOTS_FORM_COLOR_VALUE, hotspotDetails[7], True) == False:
                        writeToLog("INFO", "FAILED to select the background color for  " + hotspotDetails[0] + " as " + hotspotDetails[7].value)
                        return False
                    
                    if self.clsCommon.sendKeysToBodyElement(Keys.ENTER) != True:
                        writeToLog("INFO", "FAILED to save the color by clicking on the enter button")
                        return False
                    
                    if self.clickElement(colorPicker[1]) == False:
                        writeToLog("INFO", "FAILED to collapse the Background Color tool tip menu")
                        return False
                    
            # Verify if the Font Size should be changed
            if len(hotspotDetails) > 8:
                if hotspotDetails[8] != '':
                    # Selecting the Text Input Field
                    if self.click(self.KEA_HOTSPOTS_FORM_TEXT_SIZE, 1, True) == False:
                        writeToLog("INFO", "FAILED to click on the form text size input field for " + hotspotDetails[0] + " hotspot")
                        return False
                    
                    # Changing the value of the Text Size
                    if self.clear_and_send_keys(self.KEA_HOTSPOTS_FORM_TEXT_SIZE, str(hotspotDetails[8]), True) == False:
                        writeToLog("INFO", "FAILED to change the font size to " + str(hotspotDetails[8]) + " for " + hotspotDetails[0] + " hotspot")
                        return False
                    
            # Verify if the Roundness of the Hotspot Container should be changed
            if len(hotspotDetails) > 9:
                if hotspotDetails[9] != '':
                    # Selecting the Roundness Input Field
                    if self.click(self.KEA_HOTSPOTS_FORM_ROUNDNESS, 1, True) == False:
                        writeToLog("INFO", "FAILED to click on the roundness input field for " + hotspotDetails[0] + " hotspot")
                        return False
                    
                    # Changing the value of the Roundness Size
                    if self.clear_and_send_keys(self.KEA_HOTSPOTS_FORM_ROUNDNESS, str(hotspotDetails[9]), True) == False:
                        writeToLog("INFO", "FAILED to change the font size to " + str(hotspotDetails[9]) + " for " + hotspotDetails[0] + " hotspot")
                        return False
                    
            # Verify if the Hotspot Container size should be changed
            if len(hotspotDetails) > 10:
                if hotspotDetails[10] != '':
                    # Create the container size specific for each class
                    if hotspotDetails[10] == enums.keaHotspotContainerSize.DEFAULT:
                        width   = 128
                        height  = 32
                        
                    elif hotspotDetails[10] == enums.keaHotspotContainerSize.SMALL:
                        width   = 64
                        height  = 32
                    
                    elif hotspotDetails[10] == enums.keaHotspotContainerSize.MEDIUM:
                        width   = 256
                        height  = 64
                        
                    elif hotspotDetails[10] == enums.keaHotspotContainerSize.LARGE:
                        width   = 364
                        height  = 128
                    
                    else:
                        writeToLog("INFO", "FAILED, the desired container size doesn't exists " + hotspotDetails[10])
                        return False
                    
                    # Highlight the width input field
                    if self.click(self.KEA_HOTSPOTS_FORM_SIZE_WIDTH, 1, True) == False:
                        writeToLog("INFO", "FAILED to click on the width input field from the Advanced Settings")
                        return False
                    
                    # Select the current width text from the input field
                    if self.clsCommon.sendKeysToBodyElement(Keys.CONTROL + 'a') != True:
                        writeToLog("INFO", "FAILED to select the current width from the Advanced Settings Input Field")
                        return False
                    
                    # Replace the current width with the desired one
                    if self.send_keys(self.KEA_HOTSPOTS_FORM_SIZE_WIDTH, str(width), True) == False:
                        writeToLog("INFO", "FAILED to insert the desired width size")
                        return False
                    
                    # Highlight the input field
                    if self.click(self.KEA_HOTSPOTS_FORM_SIZE_HEIGHT, 1, False) == False:
                        writeToLog("INFO", "FAILED to click on the height input field from the Advanced Settings")
                        return False
                    
                    # Select the current height text from the input field
                    if self.clsCommon.sendKeysToBodyElement(Keys.CONTROL + 'a') != True:
                        writeToLog("INFO", "FAILED to select the current width from the Advanced Settings Input Field")
                        return False
                    
                    # Replace the current height with the desired one
                    if self.send_keys(self.KEA_HOTSPOTS_FORM_SIZE_HEIGHT, str(height), True) == False:
                        writeToLog("INFO", "FAILED to insert the desired height size")
                        return False
                    
            # Save the current hotspot
            if self.saveHotspotChanges(settingsChanges=True) == False:
                writeToLog("INFO", "FAILED to save the KEA hotspots for " + hotspotDetails[0])
                return False
            
            # Set the start time and end time for the hotspot
            if len(hotspotDetails) >= 3:
                if hotspotDetails[2] != None or hotspotDetails[3] != None:
                    if creationType == enums.keaHotspotCreationType.VIDEO_PAUSED:
                        if self.hotspotCuePoint(hotspotDetails[0], hotspotDetails[2], hotspotDetails[3]) == False:
                            writeToLog("INFO", "FAILED to set for the " + hotspotDetails[0] + " hotspot, start time to " + hotspotDetails[2] + " and end time to " + hotspotDetails[3])
                            return False
                        
                        # Move back the real time marker to the initial position
                        if self.setRealTimeMarkerToTime('00:00') == False:
                            writeToLog("INFO", "FAILED to set the real time marker back to the initial position after creating " + hotspotDetails[0] + " hotspot")
                            return False
        
        hotspotNameList = []
        for hotspotNumber in hotspotsDict:
            hotspotNameList.append(hotspotsDict[hotspotNumber][0])
        
        if len(hotspotNameList) > 1:   
            hotspots = ", ".join(hotspotNameList)
        else:
            hotspots = hotspotNameList[0]
        
        sleep(2)
        writeToLog("INFO","The following hotspots were verified: " + hotspots + "")
        return True
    
    
    # @Author: Horia Cus
    # This function will place the desired hotspot to the desired location
    # startTime and endTime must be integer
    # startTime represents the place from where the hotspot will be placed
    # endTime represents the place from where the hotspots will end
    def hotspotCuePoint(self, hotspotName, startTime=None, endTime=None):
        self.switchToKeaIframe()  
        
        # Verify that the Hotspot section is present
        if self.wait_element(self.EDITOR_REALTIME_MARKER, 15, True) == False:
            writeToLog("INFO", "FAILED To verify that we are in the Hotspots Section")
            return False
        
        # Take entrie's total time length and presented hotspots
        presentedHotspots = self.wait_elements(self.KEA_TIMELINE_SECTION_HOTSPOT_CONTAINER, 15)
        entryTotalTime    = self.wait_element(self.EDITOR_TOTAL_TIME, 1, True).text.replace(' ', '')[1:]
        m, s = entryTotalTime.split(':')
        entryTotalTimeSeconds   = int(m) * 60 + int(s)
        
        # Verify that at least one hotspot is presented
        if presentedHotspots == False:
            writeToLog("INFO", "FAILED to take the presetend hotspots")
            return False
        
        # Change the start time and end time for the desired hotspotName from the presented hotspots
        for x in range(0, len(presentedHotspots)):
            presentedHotspot         = presentedHotspots[x]
            presentedHotspotTitle    = presentedHotspot.text
            presentedHotspotWidth    = presentedHotspot.size['width']
            widthSizeForOneSecond    = presentedHotspotWidth/entryTotalTimeSeconds
            
            # Verify that the hostpotName is a match with the presented Hotspots
            if presentedHotspotTitle == hotspotName:
                # Highlight the correct hotspot in order to activate the editing options              
                writeToLog("INFO", "Going to set for " + hotspotName + " start time to " + str(startTime) + " and end time to " + str(endTime))
                if self.clickElement(presentedHotspot) == False:
                    writeToLog("INFO", "FAILED to highlight the " + presentedHotspot.text + " hotspot")
                    return False
                
                # Take the element that will be used in order to set the start time
                hotspotContainerRight      = self.wait_element(self.KEA_TIMELINE_SECTION_HOTSPOT_DRAG_CONTAINER_RIGHT, 5, True)
                
                # Take the element that will be used in order to set the end time
                hotspotContainerLeft       = self.wait_element(self.KEA_TIMELINE_SECTION_HOTSPOT_DRAG_CONTAINER_LEFT, 5, True)
                
                # Verify that the hotspot options are available
                if hotspotContainerRight == False or hotspotContainerLeft == False:
                    writeToLog("INFO", "FAILED to select the " + presentedHotspot + " hotspot")
                    return False

                # The overlay element it's the real time marker that was dragged by action chain instead of the desired hotspot
                try:
                    overlayElement = self.wait_element(self.EDITOR_REALTIME_MARKER_CONTAINER, 5)
                    self.driver.execute_script("arguments[0].setAttribute('style','display:none;')", overlayElement)
                    sleep(1)
                except Exception:
                    writeToLog("INFO", "FAILED to dismiss the real time maker while editing the cue points")
                    return False
                
                # Set the action chain for start time
                actionStartTime = ActionChains(self.driver)
                # Set the desired start time of the hotspot
                if startTime != None:
                    widthSizeInOrderToReachDesiredStartTime = widthSizeForOneSecond * startTime
                    
                    try:
                        actionStartTime.drag_and_drop_by_offset(hotspotContainerLeft, widthSizeInOrderToReachDesiredStartTime, 0).pause(1).perform()
                    except Exception:
                        writeToLog("INFO", "FAILED to set the start time for " + hotspotName + " to " + str(startTime) + " second")
                        return False
                    
                
                # Set the action chain for end time
                actionEndTime = ActionChains(self.driver)
                # Set the desired end time of the hotspot 
                if endTime != None:
                    
                    # Verify that the end time its within boundaries
                    secondsToDecrease = 0
                    if endTime > entryTotalTimeSeconds:
                        writeToLog("INFO", "The end time of " + str(endTime) + " seconds, for " + hotspotName + " exceeds the entry total time of " + str(entryTotalTimeSeconds) + " seconds")
                        return False
                    
                    # Take the number of seconds that we need to decrease in order to reach the desired end time
                    while entryTotalTimeSeconds != endTime:
                        entryTotalTimeSeconds -= 1
                        secondsToDecrease += 1
                    
                    # Take the number of pixels that we need to decrease in order to reach the desired end time
                    widthSizeInOrderToReachDesiredEndTime = widthSizeForOneSecond * secondsToDecrease
                    
                    # Verify that the end time cue point is not already placed in the end time location
                    if widthSizeInOrderToReachDesiredEndTime != float(0.0):
                        try:
                            actionEndTime.drag_and_drop_by_offset(hotspotContainerRight, -widthSizeInOrderToReachDesiredEndTime, 0).pause(1).perform()
                        except MoveTargetOutOfBoundsException:
                            # Because the MoveTargetOutOfBoundsException error may be trigger due to the fact that the Cue Point is not visible, we navigate to view the element itself
                            self.driver.execute_script("arguments[0].scrollIntoView();", hotspotContainerRight)
                            sleep(1)
                            try:
                                ActionChains(self.driver).drag_and_drop_by_offset(hotspotContainerRight, -widthSizeInOrderToReachDesiredEndTime, 0).pause(1).perform()
                            except Exception:       
                                writeToLog("INFO", "FAILED to set the end time for " + hotspotName + " to " + str(endTime) + " second")
                                return False
                
                # Re-display the real time marker after changing the hotspot size
                try:
                    self.driver.execute_script("arguments[0].setAttribute('style','display;')", overlayElement)
                    sleep(1)
                except Exception:
                    writeToLog("INFO", "FAILED to re display the real time maker after editing the hotspots cue points")
                    return False
                
                # Save the new cue point changes
                if self.click(self.KEA_HOTSPOTS_SAVE_BUTTON, 1, True) == False:
                    writeToLog("INFO", "FAILED to save the hotspot changes")
                    return False
                
                if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_CONTAINER, 30) == False:
                    writeToLog("INFO", "FAILED to wait until the hotspot changes were saved")
                    return False
                
                break
            
            
            # Verify that the hostpoName was a match with at least one presented hotspot 
            if x + 1 == len(presentedHotspots):
                writeToLog("INFO", "FAILED to find the expected hostpot within the presented hotspots")
                return False
                   
        writeToLog("INFO", "Hotspot: " + hotspotName + " has been successfully set to " + str(startTime) + " start time and " + str(endTime) + " end time")
        return True
   
    
    # @Author: Horia Cus
    # This function will click on the desired location from the player screen
    # location must contain enum ( e.g enums.keaLocation.CENTER ) 
    # For now we support Five types of locations, top right / left, buttom right / left and center
    def hotspotLocation(self, location):
        self.switchToKeaIframe()
        
        # Take the Hotspot Player Screen element details
        hotspotScreen = self.wait_element(self.KEA_PLAYER_CONTAINER, 30, True)
        
        # Verify that we are able to take the X, Y coordinates for the desired location
        if type(self.hotspotLocationCoordinates(location)) is not list:
            writeToLog("INFO", "FAILED to take the coordinates for location " + location.value)
            return False
        
        # Take the X, Y coordinates for the desired location
        x, y = self.hotspotLocationCoordinates(location)
        
        # Verify if a hotspot is already selected, if so, the hotpost will be unselected
        if self.wait_element(self.KEA_HOTSPOTS_PLAYER_HOTSPOT_CONTAINER_SELECTED, 1, True) != False:
            if self.clickElement(hotspotScreen) == False:
                writeToLog("INFO", "FAILED to click on the hotspot player screen in order to un select the hotspot container")
                return False
        
        action = ActionChains(self.driver)
        # Move the quiz number to a new timeline location
        try:
            # Start the location from the Top Left corner and move it to the desired place
            if location != enums.keaLocation.CENTER:
                action.move_to_element_with_offset(hotspotScreen, 0, 0).pause(2).move_by_offset(x, y).pause(2).click().perform()
            
            # Start from the center of the element and move the element by negative x value in order to proper place the hotspot to the center
            elif location == enums.keaLocation.CENTER:
                action.move_to_element(hotspotScreen).pause(2).move_by_offset(-x, y).pause(2).click().perform()
        except Exception:
            writeToLog("INFO", "FAILED to set the KEA Location at " + location.value)
            return False
        
        writeToLog("INFO", "KEA Location has been successfully set at " + location.value)
        return True
    
    
    # @Author: Horia Cus
    # This function will save the changes performed within the Hotspot section
    # If settingsChanges = True, means that changes were performed within the List and it will click on the done button first
    def saveHotspotChanges(self, settingsChanges=True):
        self.switchToKeaIframe()
        
        if settingsChanges == True:
            # Save the settings hotspot changes
            if self.click(self.KEA_HOTSPOTS_DONE_BUTTON_ADVANCED_SETTINGS, 1, True) == False:
                if self.click(self.KEA_HOTSPOTS_DONE_BUTTON_NORMAL, 1, True) == False:
                    writeToLog("INFO", "FAILED to save the KEA hotspots setting changes")
                    return False
        
        # Save the presented hotspots inside the entry
        if self.click(self.KEA_HOTSPOTS_SAVE_BUTTON, 1, True) == False:
            writeToLog("INFO", "FAILED to save the hotspot changes")
            return False
        
        # Verify that the changes were saved
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_CONTAINER, 30) == False:
            writeToLog("INFO", "FAILED to wait until the hotspot changes were saved")
            return False
        
        return True
    

    # @Author: Horia Cus
    # This function can edit / delete and duplicate any presented  hotspotName
    # hotspotName = contains the string of the hotspot title
    # hotspotAction must  be enum ( e.g enums.keaHotspotActions.DUPLICATE )
    def hotspotActions(self, hotspotName, hotspotAction, editHotspotDict=''):
        self.switchToKeaIframe()
        
        hotspotIndexLocation = self.returnHotspotIndexFromList(hotspotName)
        
        if type(hotspotIndexLocation) is not int:
            writeToLog("INFO", "FAILED to take the hospot: " + hotspotName + " index location")
            return False
        
        # Create the elements for hamburger menu
        hotspotsActionMenu = self.wait_elements(self.KEA_HOTSPOTS_PANEL_MORE_HAMBURGER_MENU, 1)
        
        # Verify that we were able to find the hamburger menu buttons
        if hotspotsActionMenu == False:
            writeToLog("INFO", "FAILED to find the action menu for the presented hotspots")
            return False
        
        # Create the elements for the Hotspot Title
        presentedHotspotsTitle  = self.wait_elements(self.KEA_HOTSPOTS_PANEL_ITEM_TITLE, 1)
        
        # Highlight the hotspotName field by clicking on its container
        if self.clickElement(presentedHotspotsTitle[hotspotIndexLocation]) == False:
            writeToLog("INFO", "FAILED to highligth the " + hotspotName + " hotspot")
            return False
        
        # Trigger the Action Drop Down Menu
        if self.clickElement(hotspotsActionMenu[hotspotIndexLocation]) == False:
            writeToLog("INFO", "FAILED to trigger the action menu for hotspot: " + hotspotName + " at the second try")
            return False
            
        if hotspotAction == enums.keaHotspotActions.DUPLICATE:
            # Duplicate the hotspotName
            if self.click(self.KEA_HOTSPOTS_PANEL_ACTION_MENU_DUPLICATE, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Duplicate button for the hotspot: " + hotspotName)
                return False
            
            # Add a special suffix for the duplicated hotspot in order to verify it in other function
            action = ActionChains(self.driver)
            
            try:
                action.send_keys(' Duplicated').perform()
            except Exception:
                writeToLog("INFO", "FAILED to add Duplicated suffix for the " + hotspotName + " hotspot")
                return False
            
            # Save the duplicated hotspot
            if self.saveHotspotChanges(settingsChanges=True) == False:
                writeToLog("INFO", "FAILED to save the changes for " + hotspotName + " Duplicated hotspot")
                return False
            
        elif hotspotAction == enums.keaHotspotActions.EDIT:
            # Edit the hotspotName
            if self.click(self.KEA_HOTSPOTS_PANEL_ACTION_MENU_EDIT, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Edit button for the hotspot: " + hotspotName)
                return False
            
            # Add a suffix to the edited hotspotName in order to verify it in other function
            action = ActionChains(self.driver)
            
            try:
                action.send_keys(' Edited').perform()
            except Exception:
                writeToLog("INFO", "FAILED to add Edited suffix for the " + hotspotName + " hotspot")
                return False
            
            # Save the edited hotspot
            if self.saveHotspotChanges(settingsChanges=True) == False:
                writeToLog("INFO", "FAILED to save the changes for " + hotspotName + " Edited hotspot")
                return False
            
        elif hotspotAction == enums.keaHotspotActions.DELETE:
            # Trigger the delete process for the hotspotName
            if self.click(self.KEA_HOTSPOTS_PANEL_ACTION_MENU_DELETE, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Delete Action Button for the hotspot: " + hotspotName)
                return False
            
            # Verify that the Delete Confirmation Pop up is triggered
            if self.wait_element(self.KEA_CONFIRMATION_POP_UP_CONTAINER, 3, True) == False:
                writeToLog("INFO", "FAILED to trigger the Delete Confirmation Pop up")
                return False
            
            # Confirm the delete process
            if self.click(self.KEA_HOTSPOTS_DELETE_POP_UP_CONFIRMATION_BUTTON, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Delete Hotspot button")
                return False
            
            # Verify that the confirmation pop up is no longer present
            if self.wait_while_not_visible(self.KEA_CONFIRMATION_POP_UP_CONTAINER, 10) == False:
                writeToLog("INFO", "FAILED, the confirmation pop up is still present")
                return False
            
            # Save the changes
            if self.saveHotspotChanges(settingsChanges=False) == False:
                writeToLog("INFO", "FAILED to save the changes after deleting the " + hotspotName + " hotspot")
                return False
            
            try:
                # Verify that the element is no longer present
                presentedHotspotsTitle[hotspotIndexLocation].text
                writeToLog("INFO", "FAILED, the hotspot " + hotspotName + " element is still present, although it should have been deleted")
                return False
            # If an exception its thrown, means that the element is no longer present, which is what we want, since the hotspot has been deleted
            except StaleElementReferenceException:
                writeToLog("INFO", "The hotspot " + hotspotName + " has been successfully deleted")
                return True
            
        elif hotspotAction == enums.keaHotspotActions.CANCEL_DELETE:
            # Trigger the delete process for the hotspotName
            if self.click(self.KEA_HOTSPOTS_PANEL_ACTION_MENU_DELETE, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Delete Action Button for the hotspot: " + hotspotName)
                return False
            
            # Verify that the Delete Confirmation Pop up is triggered
            if self.wait_element(self.KEA_CONFIRMATION_POP_UP_CONTAINER, 3, True) == False:
                writeToLog("INFO", "FAILED to trigger the Delete Confirmation Pop up")
                return False
            
            # Click on the Cancel button
            if self.click(self.KEA_CONFIRMATION_POP_UP_CANCEL_BUTTON, 1, True) == False:
                writeToLog("INFO", "FAILED to cancel the Hotspot Deletion process by clicking on the Cancel Button")
                return False
            sleep(1)

            try:
                # Verify that the element is still present
                presentedHotspotsTitle[hotspotIndexLocation].text
            # If an exception its thrown, means that the element is no longer present, which is what we want, since the hotspot has been deleted
            except StaleElementReferenceException:
                writeToLog("INFO", "The hotspot " + hotspotName + " has been deleted, although it shouldn't")
                return False
        
        # Verify that a valid action has been used during the function call
        else:
            writeToLog("INFO", "FAILED, please make sure that you've used a supported hotspot action")
            return False

        writeToLog("INFO", "The hotspot " + hotspotName + " has been successfully " + hotspotAction.value + "ed")
        return True
    
    
    # @Author: Horia Cus
    # This function can launch the KEA Editor for the desired entry name
    # This function will open the specified keaTab while being in the KEA Editor
    # entryName must be inserted ( if navigateToEntry = True) in order to verify that the KEA page has been successfully opened and loaded
    # keaTab must contain enum ( e.g enums.keaTab.QUIZ)
    # expectedConfirmation = True, it will pass the confirmation pop up during the transition, if no confirmation pop up is presented, it will return False
        # If you have changes that were not saved, you should expect a confirmation pop up during the transition to another KEA Tab 
    def launchKEATab(self, entryName, keaTab, navigateToEntry=False, timeOut=1, expectedConfirmation=False):
        self.switch_to_default_content()
        if navigateToEntry == True:
            sleep(timeOut)
            if self.launchKEA(entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Failed to launch KEA for: " + entryName)
                return False
        
            if self.verifyKeaEntryName(entryName, 60) == False:
                writeToLog("INFO", "FAILED to load the page until the " + entryName + " was present")
                return False
            
        self.switchToKeaIframe()
        if keaTab == enums.keaTab.QUIZ:
            if self.wait_element(self.KEA_QUIZ_TAB_ACTIVE, 1, True) != False:
                writeToLog("INFO", "KEA Quiz tab is already active")
            else:
                if self.wait_element(self.KEA_QUIZ_TAB, 45, True) == False:
                    writeToLog("INFO", "FAILED to find the KEA Quiz tab")
                    return False
                
                if self.click(self.KEA_QUIZ_TAB, 1, True) == False:
                    writeToLog("INFO", "FAILED to click on the KEA Quiz tab")
                    return False
                
                if expectedConfirmation == True:
                    if self.wait_element(self.KEA_CONFIRMATION_POP_UP_CONTAINER, 3, True) == False:
                        writeToLog("INFO", "FAILED, no confirmation pop up has been displayed")
                        return False
                    
                    if self.click(self.KEA_CONFIRMATION_POP_UP_OK_BUTTON, 1, True) == False:
                        writeToLog("INFO", "FAILED to click on the OK confirmation pop up")
                        return False                    
                
                sleep(0.5)
                if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_CONTAINER, 60) == False:
                    writeToLog("INFO", "FAILED to wait until the KEA Quiz tab has been successfully loaded")
                    return False
                
                if self.wait_element(self.KEA_QUIZ_TAB_ACTIVE, 5, True) == False:
                    writeToLog("INFO", "FAILED, the KEA Quiz tab is not displayed as being enabled")
                    return False
        
        elif keaTab == enums.keaTab.VIDEO_EDITOR:
            if self.wait_element(self.KEA_VIDEO_EDITOR_TAB_ACTIVE, 1, True) != False:
                writeToLog("INFO", "KEA Video Editor tab is already active")
            else:
                if self.wait_element(self.KEA_VIDEO_EDITOR_TAB, 45, True) == False:
                    writeToLog("INFO", "FAILED to find the KEA Video Editor tab")
                    return False
                
                if self.click(self.KEA_VIDEO_EDITOR_TAB, 1, True) == False:
                    writeToLog("INFO", "FAILED to click on the KEA Video Editor tab")
                    return False
                
                if expectedConfirmation == True:
                    if self.wait_element(self.KEA_CONFIRMATION_POP_UP_CONTAINER, 3, True) == False:
                        writeToLog("INFO", "FAILED, no confirmation pop up has been displayed")
                        return False
                    
                    if self.click(self.KEA_CONFIRMATION_POP_UP_OK_BUTTON, 1, True) == False:
                        writeToLog("INFO", "FAILED to click on the OK confirmation pop up")
                        return False   
                
                sleep(0.5)
                if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_CONTAINER, 60) == False:
                    writeToLog("INFO", "FAILED to wait until the KEA Video Editor tab has been successfully loaded")
                    return False
                
                if self.wait_element(self.KEA_VIDEO_EDITOR_TAB_ACTIVE, 5, True) == False:
                    writeToLog("INFO", "FAILED, the KEA Video Editor tab is not displayed as being enabled")
                    return False
                
        elif keaTab == enums.keaTab.HOTSPOTS:
            if self.wait_element(self.KEA_HOTSPOTS_TAB_ACTIVE, 1, True) != False:
                writeToLog("INFO", "KEA Hotspots tab is already active")
            else:
                if self.wait_element(self.KEA_HOTSPOTS_TAB, 45, True) == False:
                    writeToLog("INFO", "FAILED to find the KEA Hotspots tab")
                    return False
                
                if self.click(self.KEA_HOTSPOTS_TAB, 1, True) == False:
                    writeToLog("INFO", "FAILED to click on the KEA Hotspots tab")
                    return False
                
                if expectedConfirmation == True:
                    if self.wait_element(self.KEA_CONFIRMATION_POP_UP_CONTAINER, 3, True) == False:
                        writeToLog("INFO", "FAILED, no confirmation pop up has been displayed")
                        return False
                    
                    if self.click(self.KEA_CONFIRMATION_POP_UP_OK_BUTTON, 1, True) == False:
                        writeToLog("INFO", "FAILED to click on the OK confirmation pop up")
                        return False   
                                    
                sleep(0.5)
                if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_CONTAINER, 60) == False:
                    writeToLog("INFO", "FAILED to wait until the KEA Hotspots tab has been successfully loaded")
                    return False
                
                if self.wait_element(self.KEA_HOTSPOTS_TAB_ACTIVE, 5, True) == False:
                    writeToLog("INFO", "FAILED, the KEA Hotspots tab is not displayed as being enabled")
                    return False
                
        else:
            writeToLog("INFO", "FAILED, please make sure that you've used a supported KEA section")
            return False
        
        sleep(3.5)
        writeToLog("INFO", "The " + keaTab.value + " has been successfully opened")
        return True
    

    # @Author: Horia Cus
    # This function will verify that the expected hotspots are properly presented in the timeline section by
    # Verifying the hotspot container size based on the duration
    # Verifying the X location based on the start time
    # Verifying the Y location based on the start and end time
    # Verify the place order based on creation
    # For hotspotDict structure please check hotspotCreation function
    # expectedHotspotNumber = 5, will also verify that exactly five hotspots are presented
    def hotspotTimelineVerification(self, hotspotsDict, expectedHotspotNumber=None):
        self.switchToKeaIframe()
        # Verify that we are in the Hotspot Section
        if self.wait_element(self.EDITOR_REALTIME_MARKER, 15, True) == False:
            writeToLog("INFO", "FAILED To verify that we are in the Hotspots Section")
            return False        
        
        # Create a Blank Hotspot in order to take the properties that we need
        if self.click(self.KEA_HOTSPOTS_ADD_NEW_BUTTON, 15, True) == False:
            writeToLog("INFO", "FAILED to add a new hotspot in order to take its width")
            return False
        
        if self.saveHotspotChanges(settingsChanges=True) == False:
            writeToLog("INFO", "FAILED to save the blank hotspot")
            return False
        
        presentedHotspots       = self.wait_elements(self.KEA_TIMELINE_SECTION_HOTSPOT_CONTAINER, 15)
        zeroSecondXValue        = None
        
        # Take the properties from the Blank Hotspot
        for x in range(0, len(presentedHotspots)):
            if presentedHotspots[x].text == '':
                maximumHotspotSize        = presentedHotspots[x].size['width']
                zeroSecondXValue          = presentedHotspots[x].location['x']
                break
            
            if x + 1 == len(presentedHotspots):
                writeToLog("INFO", "FAIELD to find the blank hotspot")
                return False
        
        # Delete the Blank Hotspot
        if self.hotspotActions('<Blank>', enums.keaHotspotActions.DELETE) == False:
            writeToLog("INFO", "FAILED to delete the blank hotspot")
            return False
        
        # Take the list with all the presented hotspots from the Timeline section
        presentedHotspots           = self.wait_elements(self.KEA_TIMELINE_SECTION_HOTSPOT_CONTAINER, 15)
        # Take the list with all the presented hotspots from the HS List
        presetendHotspotsList       = self.wait_elements(self.KEA_HOTSPOTS_LIST_PANEL_HOTSPOT, 15)
        
        # Verify that the same number of hotspots are displayed in both Timeline section and HS list
        if len(presentedHotspots) != len(presetendHotspotsList):
            writeToLog("INFO", "FAILED, a number of " + len(presentedHotspots) + " hotspots were displayed in the timeline and "  + len(presetendHotspotsList) + " in the HS List")
            return False
        
        # Verify that the Hotspot order list is the same in both Timeline and HS list sections
        for x in range(0,len(presentedHotspots)):
            try:
                presentedHotspotsTitleTimeline   = presentedHotspots[x].text
                presentedHotspotsTitleList       = presetendHotspotsList[x].text
            except Exception:
                writeToLog("INFO", "FAILED to take the presented hotspot title from timeline and HS list sections")
                return False
            
            if presentedHotspotsTitleList.count(presentedHotspotsTitleTimeline) != 1:
                writeToLog("INFO", "FAILED to find the " + presentedHotspotsTitleTimeline + " title inside the HS list")
                return False

        # Take entrie's length time
        entryTotalTime              = self.wait_element(self.EDITOR_TOTAL_TIME, 1, True).text.replace(' ', '')[1:]
        m, s                        = entryTotalTime.split(':')
        entryTotalTimeSeconds       = int(m) * 60 + int(s)
        # Take the number of px needed for each second based on the entry time
        widthSizeForOneSecond       = maximumHotspotSize/entryTotalTimeSeconds

        # Verify that we have at least one hotspot presented
        if presentedHotspots == False:
            writeToLog("INFO", "FAILED to find any available hotspots within the timeline section")
            return False
        
        # Verify that the expectedHostNumber matches with the number of the presentedHotspots
        if expectedHotspotNumber != None:
            if expectedHotspotNumber != len(presentedHotspots):
                writeToLog("INFO", "FAILED, a number of " + str(expectedHotspotNumber) + " hotspots were expected but " + str(len(presentedHotspots)) + " hotspots were presented")
                return False  
            
        # Create a list with the successfully verified hotspots
        hotspotNameList = []       
        
        # Used in order to verify that the hotspot is displayed on the right Y location
        previousYValue = -1
        expectedHotspotVerified = 0
        i = 1
        # Iterate through each presented hotspot
        for x in range(0, len(presentedHotspots)):
            try:
                try:
                    presentedHotspot         = presentedHotspots[x]
                    presentedHotspotTitle    = presentedHotspot.text
                except Exception:
                    writeToLog("INFO", "FAILED to take the presented hotspot at the " + str(x) + " try")
                    return False
                    
                # Iterate through the presented hotspots until the expected one is found
                for k in range(0,len(presentedHotspots)):
                    expectedHotspot          = hotspotsDict[str(k+1)]
                    
                    if presentedHotspotTitle == expectedHotspot[0]:
                        writeToLog("INFO", "The hotspot " + presentedHotspotTitle + " was found at place " + str(x))
                        break
                    else:
                        if k + 1 == len(presentedHotspots):
                            writeToLog("INFO", "FAILED to find the expected hotspot: " + expectedHotspot[0])
                            return False 
                        
                # Take the presented hotspot details
                presentedHotspotWidth    = presentedHotspot.size['width']
                presentedHotspotXValue   = presentedHotspot.location['x']
                presentedHotspotYValue   = presentedHotspot.location['y']
                presentedHotspotTime     = int(presentedHotspotWidth/widthSizeForOneSecond)
                
                expectedHotspotTime      = expectedHotspot[3] - expectedHotspot[2]
                expectedHotspotXValue    = int(zeroSecondXValue + widthSizeForOneSecond * expectedHotspot[2])
            except Exception:
                writeToLog("INFO", "FAILED to take the Expected and Presented hotspot details")           
                
            # Verify that the width of the hotspot container matches with the expected duration
            if presentedHotspotTime != expectedHotspotTime:
                # Allow a two second inconsistency
                for x in range(0,2):
                    if presentedHotspotTime + x == expectedHotspotTime:
                        break
                    
                    if x == 2:
                        writeToLog("INFO", "FAILED, the length of " + presentedHotspotTitle + " was " + str(presentedHotspotTime) + " while we expected " + str(expectedHotspotTime))
                        return False
            
            # Verify that the presented hotspot is presented at the expected X location
            if presentedHotspotXValue != expectedHotspotXValue:
                # Allow a five px inconsistency
                for x in range(0,7):
                    if presentedHotspotXValue == expectedHotspotXValue + x:
                        break
                    
                    if x >= 5:
                        if presentedHotspotXValue + 1 != expectedHotspotXValue:
                            writeToLog("INFO", "FAILED, the x Location of " + presentedHotspotTitle + " was " + str(presentedHotspotXValue) + " while we expected " + str(expectedHotspotXValue))
                            return False
                        else:
                            break
            
            # Verify that the current iterated hotspot is displayed on a higher Y value than the previous hotspot
            if presentedHotspotYValue <= previousYValue:
                writeToLog("INFO", "FAILED, the Y Location of " + presentedHotspotTitle + " was " + str(presentedHotspotYValue) + " while from the previous hotspot was " + str(previousYValue))
                return False
            else:
                previousYValue = presentedHotspotYValue
            
            i += 1
            expectedHotspotVerified += 1
            hotspotNameList.append(expectedHotspot[0])
            writeToLog("INFO", "The following hotspot has been successfully presented in the timeline section " + expectedHotspot[0])
                
        if len(hotspotNameList) > 1:   
            hotspots = "\n".join(hotspotNameList)
        else:
            hotspots = expectedHotspot[0]
        
        # Verify that the expected hotspots were presented in the timeline section
        if expectedHotspotVerified != len(hotspotsDict):
            writeToLog("INFO", "FAILED, a number of " + str(expectedHotspotVerified) + " hotspots were found based on the hotspotDict, while we expected to verify: " + str(len(hotspotsDict)) + " number of hotspots from hotspotDict")
            return False
        else:
            writeToLog("INFO", "ALL the " + str(len(hotspotsDict)) + " expected hotspots from the hotspotDict were properly found inside the timeline section")

        writeToLog("INFO","The following hotspots were properly verified in the timeline section:\n" + hotspots)
        return True
    

    # @Author: Horia Cus
    # This function will return the X, Y value for the desired location
    # location must contain enum ( e.g enums.keaLocation.CENTER ) 
    def hotspotLocationCoordinates(self, location):
        self.switchToKeaIframe()
        
        # Take the Hotspot Player Screen element details
        hotspotScreen = self.wait_element(self.KEA_PLAYER_CONTAINER, 30, True)
        
        # Verify that the Hotspot Player Screen is presented
        if hotspotScreen == False:
            writeToLog("INFO", "FAILED to find the Hotspot screen")
            return False
        
        # Take the width of hotspot container in order to proper align it to the center location
        if location == enums.keaLocation.CENTER:
            # In order to proper align the hotspot to the center we need to take container's width, if no container is presented we will divide by the default value 
            containerSize = self.wait_element(self.KEA_HOTSPOTS_PLAYER_HOTSPOT_CONTAINER, 1, True)
            
            if containerSize != False:
                containerSize = containerSize.size['width']
                
            elif type(containerSize) is not int:
                writeToLog("INFO", "No hotspots information that contains container size were given")
                # Use the default value
                containerSize = 128
                
            else:
                writeToLog("INFO", "FAILED to take the width size for the " + location.value + " location")
                return False
        
        # Set the off sets for the desired KEA Location
        if location == enums.keaLocation.TOP_LEFT:
            x = hotspotScreen.size['width']/500
            y = hotspotScreen.size['height']/500
            
        elif location == enums.keaLocation.TOP_RIGHT:
            x = hotspotScreen.size['width']/1.20
            y = hotspotScreen.size['height']/500

        elif location == enums.keaLocation.BOTTOM_LEFT:
            x = hotspotScreen.size['width']/500
            y = hotspotScreen.size['height'] - hotspotScreen.size['height']/6.5
              
        elif location == enums.keaLocation.BOTTOM_RIGHT:
            x = hotspotScreen.size['width']/1.20
            y = hotspotScreen.size['height'] - hotspotScreen.size['height']/6.5
            
        elif location == enums.keaLocation.CENTER:            
            # width size of the hotspot button, divided by two in order to align it to the center properly
            x = containerSize/2
            y = 0
            
        elif location == enums.keaLocation.PROTECTED_ZONE_CENTER:               
            # width size of the hotspot button, divided by two in order to align it to the center properly
            x = hotspotScreen.size['width']/2
            y = hotspotScreen.size['height']/1.08
            
        elif location == enums.keaLocation.PROTECTED_ZONE_LEFT:
            x = hotspotScreen.size['width']/500
            y = hotspotScreen.size['height']/1.08
            
        elif location == enums.keaLocation.PROTECTED_ZONE_RIGHT:
            x = hotspotScreen.size['width']/1.08
            y = hotspotScreen.size['height']/1.08
        
        else:
            writeToLog("INFO", "FAILED, please make sure that you've used a supported KEA Location")
            return False
        
        locationCoordinatesList = [x,y]
        
        writeToLog("INFO", "The following coordinates were provided for " + location.value + " location, X: " + str(locationCoordinatesList[0]) + " and Y " + str(locationCoordinatesList[1]))
        return locationCoordinatesList
    
    
    # @Author: Horia Cus
    # This function verifies that:
    # 1. a proper tool tip is displayed while being in any player location, including protected zone
    # 2. the tool tip disappears after exiting the player screen
    # 3. the tool tip is properly displayed, based on the desired location
    # 4. If expectedHotspot = True, we will verify that the Add Hotspot tool tip is not available
    def hotspotToolTipVerification(self, location, expectedHotspot=False):
        self.switchToKeaIframe()
        
        # Take the Hotspot Player Screen element details
        hotspotScreen = self.wait_element(self.KEA_PLAYER_CONTAINER, 30, True)
        
        action = ActionChains(self.driver)
        
        if expectedHotspot == True:
            presentedHotspots = self.wait_elements(self.KEA_HOTSPOTS_PLAYER_HOTSPOT_CONTAINER, 10)
            
            if len(presentedHotspots) < 1:
                writeToLog("INFO", "FAILED, no hotspots were available within the player")
                return False
            
            # Verify that the Add New Hotspot tool tip is not presented for any presented hotspot
            for x in range(0, len(presentedHotspots)):
                try:
                    presentedHotspots[x]
                    action.move_to_element(presentedHotspots[x]).pause(2).perform()
                    
                    # Verify if the Add New Hotspot tool tip is found
                    addHotspotToolTip = self.wait_element(self.KEA_HOTSPOTS_PLAYER_ADD_HOTSPOT_TOOLTIP, 1, True)
                    
                    if addHotspotToolTip != False:
                        writeToLog("INFO", "FAILED, the Add New Hotspot tool tip was displayed while hovering over the " + presentedHotspots[x].text + " hotspot")
                        return False
                
                except Exception:
                    writeToLog("INFO", "FAILED, to hover over the " + presentedHotspots[x].text + " hotspot")
                    return False
                
            writeToLog("INFO", "AS EXPECTED, no Add New Hotspot tool tip has been presented while hovering over existing hotspots")
            return True
        
        else:
            # Verify that we are able to take the X, Y coordinates for the desired location
            if type(self.hotspotLocationCoordinates(location)) is not list:
                writeToLog("INFO", "FAILED to take the coordinates for location " + location.value)
                return False
            
            # Take the X, Y coordinates for the desired location
            x, y = self.hotspotLocationCoordinates(location)
            
            # Move the quiz number to a new timeline location
            try:
                
                # Start the location from the Top Left corner and move it to the desired place
                if location != enums.keaLocation.CENTER:
                    action.move_to_element_with_offset(hotspotScreen, 0, 0).pause(2).move_by_offset(x, y).pause(2).perform()
                    
                    if self.wait_element(self.KEA_HOTSPOTS_PLAYER_ADD_HOTSPOT_TOOLTIP, 1, True) == False:
                        writeToLog("INFO", "FAILED to display the hotspot tool tip while being at the location: "  + location.value)
                        return False
                
                # Start from the center of the element and move the element by negative x value in order to proper place the hotspot to the center
                elif location == enums.keaLocation.CENTER:
                    action.move_to_element(hotspotScreen).pause(2).move_by_offset(-x, 0).pause(2).perform()
                    
                # Take the Add Hotspot details
                addHotspotToolTip = self.wait_element(self.KEA_HOTSPOTS_PLAYER_ADD_HOTSPOT_TOOLTIP, 1, True)
                
                # Verify that the Add Hotspot tool tip was presented
                if addHotspotToolTip == False:
                    writeToLog("INFO", "FAILED to display the hotspot tool tip while being at the location: "  + location.value)
                    return False
                
                if location.value.count('Protected') == 0:
                    # Verify the Add Hotspot tool tip text
                    if addHotspotToolTip.text.strip() != 'Add hotspot here':
                        writeToLog("INFO", "FAILED, an invalid tool tip text was presented: " + addHotspotToolTip.text.strip() + " while being in the hotspot zone")
                        return False
                else:
                    if addHotspotToolTip.text.strip() != "Can't add hotspot on the protected zone":
                        writeToLog("INFO", "FAILED, an invalid tool tip text was presented: " + addHotspotToolTip.text.strip() + " while being in protected zone")
                        return False                
                         
                if location == enums.keaLocation.TOP_LEFT:
                    hotspotToolTipLocation = {'x': 503, 'y': 75}
                    
                elif location == enums.keaLocation.TOP_RIGHT:
                    hotspotToolTipLocation = {'x': 916, 'y': 75}
                    
                elif location == enums.keaLocation.CENTER:
                    hotspotToolTipLocation = {'x': 782, 'y': 268}
                    
                elif location == enums.keaLocation.BOTTOM_LEFT:
                    hotspotToolTipLocation = {'x': 503, 'y': 402}
                    
                elif location == enums.keaLocation.BOTTOM_RIGHT:
                    hotspotToolTipLocation = {'x': 916, 'y': 402}
                    
                elif location == enums.keaLocation.PROTECTED_ZONE_CENTER:
                    hotspotToolTipLocation = {'x': 846, 'y': 433}
                    
                elif location == enums.keaLocation.PROTECTED_ZONE_LEFT:
                    hotspotToolTipLocation = {'x': 503, 'y': 433}
                    
                elif location == enums.keaLocation.PROTECTED_ZONE_RIGHT:
                    hotspotToolTipLocation = {'x': 849, 'y': 433}
    
                # Verify the Add Hotspot tool tip location
                if addHotspotToolTip.location != hotspotToolTipLocation:
                    writeToLog("INFO", "FAILED, the tool tip for " + location.value + " was displayed at X:" + str(addHotspotToolTip.location['x']) + " and Y:" + addHotspotToolTip.location['y'] + " coordinates" )
                    return False
                
                playButton = self.wait_element(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 1, True)
                
                if playButton == False:
                    writeToLog("INFO", "FAILED to take the play button in order to move from player section")
                    return False
                
                ActionChains(self.driver).move_to_element(playButton).pause(2).perform()
                
                addHotspotToolTipUpdated = self.wait_element(self.KEA_HOTSPOTS_PLAYER_ADD_HOTSPOT_TOOLTIP, 1, True)
                
                if addHotspotToolTipUpdated != False:
                    writeToLog("INFO", "FAILED, the tool tip is still displayed after exiting the player area")
                    return False            
                
            except Exception:
                writeToLog("INFO", "FAILED to hover over the KEA location:" + location.value)
                return False
        
        writeToLog("INFO", "KEA Location has been successfully verified at " + location.value)
        return True
    

    # @Author: Horia Cus
    # This function will move the desired hotspot using drag and drop to the new hotspot location
    # hotspotName = contains the string of the Hotspot Title
    # hotspotNewLocation = contains the enum of the desired new location for the hotspot ( e.g enums.keaLocation.CENTER ) 
    # If the desired new hotspotLocation is already took by other hotspot, the function will return False
    def changeHotspotLocationPlayer(self, hotspotName, hotspotNewLocation):
        self.switchToKeaIframe()
        
        # Take the list of the presented hotspots
        presentedHotspots = self.wait_elements(self.KEA_HOTSPOTS_PLAYER_HOTSPOT_CONTAINER, 10)
        
        # Verify that at least one hotspots has been found in the player screen
        if presentedHotspots == False:
            writeToLog("INFO", "FAILED, no hotspots were found within the player screen")
            return False
        
        # Take the hotspot index for our hotspotName
        for x in range(0, len(presentedHotspots)):
            if presentedHotspots[x].text == hotspotName:
                hotspotIndex = x
                break
            
            if x + 1 == len(presentedHotspots):
                writeToLog("INFO", "FAILED to find the " + hotspotName + " inside the presented hotspots")
                return False
        
        # Create a list and dictionary that will be used in order to create a new hotspot with our desired location
        hotspotLocationDetailsList = [hotspotNewLocation.value, hotspotNewLocation]
        
        hotspotDict = {'1': hotspotLocationDetailsList}
        
        # Create a new hotspot that is created at the desired new location
        if self.hotspotCreation(hotspotDict) == False:
            writeToLog("INFO", "FAILED to create a new hotspot in order to take the coordinates for the desired location" + hotspotNewLocation.value)
            return False

        # Take the list with the updated presented hotspots
        hotspotLocationElement = self.wait_elements(self.KEA_HOTSPOTS_PLAYER_HOTSPOT_CONTAINER, 10)
        
        action = ActionChains(self.driver)
        
        # Move the hotspotName to the desired new location
        try:
            action.drag_and_drop(hotspotLocationElement[hotspotIndex], hotspotLocationElement[-1]).pause(2).perform()
        except Exception:
            writeToLog("INFO", "FAILED to move the " + hotspotName + " to the " + hotspotNewLocation.value + " location")
            return False
        
        # Delete the hotspot that was created in order to move the hotspotName to the new location
        if self.hotspotActions(hotspotNewLocation.value, enums.keaHotspotActions.DELETE) == False:
            writeToLog("INFO", "FAILED to delete the new hotspot that was created in order to take the coordinates" + hotspotNewLocation.value)
            return False
        
        sleep(5)
        writeToLog("INFO", "The hotspot: " + hotspotName + " has been successfully moved to the new location: " + hotspotNewLocation.value)
        return True
    

    # @Author: Horia Cus
    # This function will move the desired hotspot to the new hotspot location
    # hotspotName = contains the string of the Hotspot Title
    # hotspotNewLocation = contains the enum of the desired new location for the hotspot ( e.g enums.keaLocation.CENTER ) 
    # If the desired new hotspotLocation is already took by other hotspot, the function will return False
    def changeHotspotLocationSettings(self, hotspotName, hotspotNewLocation):
        self.switchToKeaIframe()
        
        if self.openHotspotAdvancedSettings(hotspotName) == False:
            writeToLog("INFO", "FAILED to enter in Hotspot Advanced Screen for: " + hotspotName + " hotspot")
            return False
        
        # Take the X,Y coordinates specific for the hotspotNewLocation
        hotspotNewLocationCoordinates = self.hotspotLocationCoordinates(hotspotNewLocation)
        
        # Verify that the X,Y coordinates were properly provided
        if type(hotspotNewLocationCoordinates) is not list:
            writeToLog("INFO", "FAILED to take the coordinates for the hotspot location: " + hotspotNewLocation.value)
            return False
        
        # Create the variables for the x,y locations
        x,y = hotspotNewLocationCoordinates
        
        # Add the X location to the Location X input field
        if self.click(self.KEA_HOTSPOTS_FORM_LOCATION_X, 1, True) == False:
            writeToLog("INFO", "FAILED to highlight the X input field location")
            return False
        
        # Select the text present inside the X input field
        if self.clsCommon.sendKeysToBodyElement(Keys.CONTROL + 'a') != True:
            writeToLog("INFO", "FAILED to select the text from the X input field location")
            return False
        
        # Add the new X value to the X input field
        try:
            ActionChains(self.driver).send_keys(str(int(x))).perform()
        except Exception:
            writeToLog("INFO", "FAILED to add X coordinate: " + str(int(x)) + " inside the Form list of the hotspot: " + hotspotName)
            return False
        
        # Add the Y location to the Location X input field
        if self.click(self.KEA_HOTSPOTS_FORM_LOCATION_Y, 1, True) == False:
            writeToLog("INFO", "FAILED to highlight the X input field location")
            return False
        
        # Select the text present inside the Y input field
        if self.clsCommon.sendKeysToBodyElement(Keys.CONTROL + 'a') != True:
            writeToLog("INFO", "FAILED to select the text from the X input field location")
            return False
        
        # Add the new X value to the X input field
        try:
            ActionChains(self.driver).send_keys(str(int(y))).perform()
        except Exception:
            writeToLog("INFO", "FAILED to add Y coordinate: " + str(int(y)) + " inside the Form list of the hotspot: " + hotspotName)
            return False
        
        # Save the coordinates changes
        if self.saveHotspotChanges(settingsChanges=True) == False:
            writeToLog("INFO", "FAILED to save the changes for " + hotspotName + " Edited hotspot")
            return False
        
        writeToLog("INFO", "Coordinates for the " + hotspotName + " hotspot were set to X: " + str(int(x)) + " and Y:" + str(int(y)) + " specific for the location " + hotspotNewLocation.value)
        return True 
    
    
    # @Author: Horia Cus
    # This function verifies the Hotspot present on the Panel from the left side of the player while being in the Hotspots tab
    # Verifies that the expected hotspots are displayed with the desired configurations
    def hotspotListVerification(self, hotspotDict, expectedHotspotNumber=None):
        self.switchToKeaIframe()
        
        # Take the expectedHostpotNumber based on the length of the hotspotDict if no force number was given
        if expectedHotspotNumber == None:
            expectedHotspotNumber = str(len(hotspotDict))
        else:
            expectedHotspotNumber = str(expectedHotspotNumber)

        # Take the details from the HS List Header
        hotspotListHeader   = self.wait_element(self.KEA_HOTSPOTS_LIST_HEADER, 10, True)
        
        # Take the details of the HS List counter
        hotspotListCounter  =  self.get_child_element_by_type(hotspotListHeader, 'tag_name', 'span').text.split()
        
        if hotspotListHeader == False:
            writeToLog("INFO", "FAILED to take the HS List header details")
            return False
        
        # Take the details of the available HS from the list
        hotspotListContent = self.wait_element(self.KEA_HOTSPOTS_LIST_CONTENT, 1, True)
        
        if hotspotListContent == False:
            writeToLog("INFO", "FAILED to take the HS List content details")
            return False
        
        if len(hotspotListCounter) != 2:
            writeToLog("INFO", "FAILED, more than the expected information for HS counter were given")
            return False
        
        # Verify that the presented hotspots from the HS Panel list matches with the expected number
        else:
            if hotspotListCounter[0] != expectedHotspotNumber:
                writeToLog("INFO", "FAILED,a total of " + hotspotListCounter + " HS were displayed in the HS list but " + expectedHotspotNumber + " were expected")
                return False
            
            if hotspotListCounter[1] != 'Hotspots':
                writeToLog("INFO", "FAILED, the 'Hotspots' text placeholder was not displayed, instead " + hotspotListCounter[1] + " text was present")
                return False
        
        # Verify that a proper placeholder text is presented if no hotspots are available
        if expectedHotspotNumber == str(0):
            if hotspotListContent.text != 'No hotspots for this video':
                writeToLog("INFO", "FAILED, we expected Zero Hotspots but the HS list is populated")
                return False
        else:
            hotspotListPanels = self.wait_elements(self.KEA_HOTSPOTS_LIST_PANEL_HOTSPOT, 1)
            
            # Verify that the number of expected hotspots matches with the number of HS List Panel presented
            if type(hotspotListPanels) != list:
                writeToLog("INFO", "FAILED, Hotspot List Panels elements couldn't be provided")
                return False
            else:
                if str(len(hotspotListPanels)) != expectedHotspotNumber:
                    writeToLog("INFO", "FAILED, a number of " + expectedHotspotNumber + " were expected but, " + str(len(hotspotListPanels)) + " HS were presented")
                    return False
                
                else:
                    # Verify the hotspot expected details while being in the Advanced Settings
                    if hotspotDict != '':
                        for x in range(0, len(hotspotDict)):
                            expectedHotspotDetails     = hotspotDict[str(x+1)]
                            expectedHotspotDetailTitle = expectedHotspotDetails[0]
                            
                            presentedHotspotsTitle  = self.wait_elements(self.KEA_HOTSPOTS_PANEL_ITEM_TITLE, 1)
                            presentedHotspotsLink   = self.wait_elements(self.KEA_HOTSPOTS_PANEL_ITEM_LINK, 1)
                            hotspotNameIndex = 0
                            
                            # Verify and take the expected hotspot index number
                            for x in range(0, len(presentedHotspotsTitle)):
                                if presentedHotspotsTitle[x].text == expectedHotspotDetailTitle:
                                    hotspotNameIndex = x
                                    break
                                
                                if x + 1 == len(presentedHotspotsTitle):
                                    writeToLog("INFO", "FAILED to find the " + expectedHotspotDetailTitle + " hotspot inside the HS list panel")
                                    return False
                            
                            if expectedHotspotDetails[4] != '':
                                if type(expectedHotspotDetails[4]) is str:
                                    if presentedHotspotsLink[hotspotNameIndex].text != expectedHotspotDetails[4]:
                                        writeToLog("INFO", "FAILED, we expected that " + expectedHotspotDetails[4] + " link to be displayed, instead " + presentedHotspotsLink[hotspotNameIndex].text + " was presented")
                                        return False
                                elif type(expectedHotspotDetails[4]) is int:
                                    # time string has format mm:ss
                                    expectedTimeString = str(datetime.timedelta(seconds=expectedHotspotDetails[4]))[2:]
                                    
                                    if presentedHotspotsLink[hotspotNameIndex].text != 'Jump to time: ' + expectedTimeString:
                                        writeToLog("INFO", "FAILED, " + presentedHotspotsLink[hotspotNameIndex].text  + " time was set in the HS list, however, we expected " + expectedTimeString)
                                        return False
                                else:
                                    writeToLog("INFO", "FAILED, invalid format for the hotspot link verification in HS list")
                                    return False
                            else:
                                try:
                                    presentedHotspotsLink[hotspotNameIndex]
                                    if presentedHotspotsLink[hotspotNameIndex].text != '':
                                        writeToLog("INFO", "FAILED, we expected to have no Link, however, " + presentedHotspotsLink[hotspotNameIndex].text + " link was displayed")
                                        return False
                                except TypeError:
                                    writeToLog("INFO", "As expected, no hotspot link has been provided for " + presentedHotspotsTitle[hotspotNameIndex].text ) 
                                
                            # Highlight the presented Hostpot from the HS Panel List
                            if self.clickElement(presentedHotspotsTitle[hotspotNameIndex]) == False:
                                writeToLog("INFO", "FAILED to highligth the " + expectedHotspotDetailTitle + " hotspot")
                                return False
                            
                            if self.click(self.KEA_HOTSPOTS_ADVANCED_SETTINGS, 1, True) == False:
                                writeToLog("INFO", "FAILED to click on the Advanced Settings for " + expectedHotspotDetailTitle + " Hotspot")
                                return False
                            
                            sleep(1)
                            # TO BE DEVELOPED
                            # title verification
                            # link verification
                            # style verification
                            # need pyperclip issue solved in order to proceed with the implementation
                            
                            if self.click(self.KEA_HOTSPOTS_CANCEL_BUTTON, 1, True) == False:
                                writeToLog("INFO", "FAILED to dismiss the Advanced Settings Option of the " + expectedHotspotDetailTitle + " Hotspot")
                                return False
                            
                            if self.wait_element(self.KEA_HOTSPOTS_LIST_CONTENT, 10, True) == False:
                                writeToLog("INFO", "FAILED to display back the Hotspot List after clicking on the Cancel button from the Advanced Settings")
                                return False
                
        writeToLog("INFO", "Proper information has been presented inside the HS list")
        return True
    

    # @Author: Horia Cus
    # This function will stop the playing process from KEA player and resume it from beginning, and start the playing process again from second zero
    def startFromBeginningPlayingProcess(self,):
        self.switchToKeaIframe()
        
        # Verify that the video playing process is stopped
        if self.wait_element(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 0.3, True) == False:
            if self.wait_element(self.KEA_PLAYER_CONTROLS_PAUSE_BUTTON, 1, True) == False:
                writeToLog("INFO", "FAILED to find both play and pause buttons")
                return False
            else:
                if self.click(self.KEA_PLAYER_CONTROLS_PAUSE_BUTTON, 1, True) == False:
                    writeToLog("INFO", "FAILED to pause the video")
                    return False
                else:
                    if self.wait_element(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 1, True) == False:
                        writeToLog("INFO", "FAILED to find the play button after pausing the video")
                        return False
        
        # Take the time were the video is paused at
        realTimeMarkerCurrentTime = self.wait_element(self.EDITOR_REALTIME_MARKER, 1, True).text
        realTimeMarkerTimeUpdated = None
        
        if realTimeMarkerCurrentTime != '00:00.00':
            while realTimeMarkerTimeUpdated != '00:00.00':
                self.clsCommon.sendKeysToBodyElement(Keys.ARROW_LEFT)
                realTimeMarkerTimeUpdated = self.wait_element(self.EDITOR_REALTIME_MARKER, 1, True).text
        
        sleep(3)
        # Trigger the playing process
        if self.click(self.KEA_PLAYER_CONTROLS_PLAY_BUTTON, 1, True) == False:
            writeToLog("INFO", "FAILED to trigger the playing process from second zero of the entry")
            return False
        sleep(0.1)
        
        # Wait until the loading spinner is no longer present
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_QUIZ_PLAYER, 30) == False:
            writeToLog("INFO", "FAILED to load the KEA entry video playing process")
            return False
        
        return True
    

    # @Author: Horia Cus
    # This function will play the entry and return once reaching the timeToReturn
    # timeToReturn must contain the following format 'mm:ss' ( e.g '01:59')
    def playEntryAndReturnAtTime(self, timeToReturn):
        self.switchToKeaIframe()
        
        # Trigger the playing process from second one
        if self.startFromBeginningPlayingProcess() == False:
            writeToLog("INFO", "FAILED to initiate the playing process from second zero")
            return False
        
        currentPlayTime = None
        
        # Return when the time reaches the timeToReturn value
        while timeToReturn != currentPlayTime:
            currentPlayTime = self.wait_element(self.EDITOR_REALTIME_MARKER, 1, True).text[:5]
        
        writeToLog("INFO", "The video was returned at time " + timeToReturn)
        return True
    
    
    # @Author: Horia Cus
    # This function can perform four type of hotspot creation interrupts:
    # By clicking on the Cancel Button when the Hotspot Creation Tool Tip is active
    # By clicking on the Player Screen when the Hotspot Creation Tool Tip is active
    # By performing a switch between the tabs after placing a blank hotspot in the Hotspot Panel
    # By exiting the KEA Editor when the Hotspot Creation Tool Tip is active
    # hotspotInterruptType must be enum ( e.g  enums.keaHotspotCreationInterrupt.CANCEL_BUTTON)
    # hotspotLocation must contain enum ( e.g enums.keaLocation.CENTER ) 
    def hotspotCreationInterrupts(self, hotspotInterruptType, hotspotLocation, entryName):
        self.switchToKeaIframe()
        
        # Place a new Add Hotspot on the player
        if self.hotspotLocation(hotspotLocation) == False:
            writeToLog("INFO", "FAILED to set the Hotspot Location at " + hotspotLocation)
            return False
        
        # Verify the Hotspot Creation Interrupts while using the Cancel Button
        if hotspotInterruptType == enums.keaHotspotCreationInterrupt.CANCEL_BUTTON:
            if self.click(self.KEA_HOTSPOTS_TOOL_TIP_CREATION_CANCEL_BUTTON, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the Cancel Button from the Creation Tool Tip")
                return False

        # Verify the Hotspot Creation Interrupts while clicking on the player
        elif hotspotInterruptType == enums.keaHotspotCreationInterrupt.CANCEL_OUTSIDE:
            if self.click(self.KEA_PLAYER_CONTAINER, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the player container in order to dismiss the Creation Tool Tip")
                return False

        # Verify the Hotspot Creation Interrupts while switching between KEA Tabs
        elif hotspotInterruptType == enums.keaHotspotCreationInterrupt.TAB_SWITCHING:
            # Place the Blank Hotspot inside the panel, without saving it
            if self.click(self.KEA_HOTSPOTS_DONE_BUTTON_NORMAL, 1, True) == False:
                    writeToLog("INFO", "FAILED to save the KEA hotspots setting changes")
                    return False
            
            # Verify that the confirmation pop up during the transition is present when the hotspots are not saved
            if self.launchKEATab(entryName, enums.keaTab.VIDEO_EDITOR, False, 0, True) == False:
                writeToLog("INFO", "FAILED to switch to a second tab while having Hotspot Creation Tool Tip active")
                return False
            
            # Resume back to the Hotspots Tab
            if self.launchKEATab(entryName, enums.keaTab.HOTSPOTS, False, 0, False) == False:
                writeToLog("INFO", "FAILED to switch back to the Hotspot Tab")
                return False
            
            # Verify that there's no Blank Hotspot to be deleted
            if self.hotspotActions('<Blank>', enums.keaHotspotActions.DELETE) != False:
                writeToLog("INFO", "FAILED the Blank hotspot could be deleted from the Hotspot Panel, when it shouldn't have been presented in the first place")
                return False            

        # Verify the Hotspot Creation Interrupts while Exiting the KEA Editor
        elif hotspotInterruptType == enums.keaHotspotCreationInterrupt.EXIT_KEA:
            if self.exitKeaEditor() == False:
                writeToLog("INFO", "FAILED to exit the KEA Editor for " + entryName + " entry")
                return False
            
            if self.launchKEATab(entryName, enums.keaTab.HOTSPOTS, True, 0, False) == False:
                writeToLog("INFO", "FAILED to re-launch the KEA Hotspots tab for " + entryName + " entry")
                return False  
                               
        else:
            writeToLog("INFO", "FAILED, please make sure that you've selected a supported hotspot creation interrupt option")
            return False
        
        # Verify that the Add New Hotspot Creation Tool Tip is no longer present
        if self.wait_element(self.KEA_HOTSPOTS_TOOL_TIP_CREATION_CONTAINER, 1, True) != False:
            writeToLog("INFO", "FAILED, the Hotspot Tool Tip Creation is still displayed after perform the: " + hotspotInterruptType.value + " interrupt")
        
        writeToLog("INFO", "The hotspot interrupt: " + hotspotInterruptType.value + " has been performed successfully on " + entryName + " entry")
        return True 
    
    
    # @Author: Horia Cus
    # This function verifies the negative and positive flow while exiting the KEA Editor page
    def exitKeaEditor(self,):
        self.switchToKeaIframe()
        
        # Verify that the KEA Editor container is present
        if self.wait_element(self.KEA_MAIN_CONTAINER, 20, True) == False:
            writeToLog("INFO", "FAILED to find the KEA Editor page")
            return False
        
        # Trigger the Exit Confirmation Pop Up
        if self.click(self.KEA_EXIT_BUTTON, 1, True) == False:
            writeToLog("INFO", "FAILED to click on the Exit Button from the navigation bar")
            return False
        
        # Verify that the Exit Confirmation Pop Up is presented
        if self.wait_element(self.KEA_MAIN_CONFIRMATION_POP_UP, 5, True) == False:
            writeToLog("INFO", "FAILED to display the Confirmation Dialog for exiting the KEA Editor")
            return False
        
        # Verify the negative flow
        if self.click(self.KEA_MAIN_CONFIRMATION_POP_UP_CANCEL_BUTTON, 1, True) == False:
            writeToLog("INFO", "FAILED to cancel the Exit Kea Editor process")
            return False
        
        # Verify that the KEA Exit pop up is no longer present
        if self.wait_while_not_visible(self.KEA_MAIN_CONFIRMATION_POP_UP, 15) == False:
            writeToLog("INFO", "FAILED to dismiss the KEA Exit confirmation pop up after clicking on the Cancel Button")
            return False
        
        # Trigger the Exit Confirmation Pop Up
        if self.click(self.KEA_EXIT_BUTTON, 1, True) == False:
            writeToLog("INFO", "FAILED to click on the Exit Button from the navigation bar")
            return False
        
        # Confirm the Exit Confirmation Pop uo
        if self.click(self.KEA_MAIN_CONFIRMATION_POP_UP_SURE_BUTTON, 3, True) == False:
            writeToLog("INFO", "FAILED to click on the Exit Confirmation Button")
            return False
        
        # Verify that the KEA Editor container is no longer present
        if self.wait_while_not_visible(self.KEA_MAIN_CONTAINER, 45) == False:
            writeToLog("INFO", "FAILED, the KEA Page is still displayed")
            return False  
        
        # Switch to default content, due to the fact that we are no longer in the KEA Editor page
        self.switch_to_default_content()
        writeToLog("INFO", "KEA Editor has been successfully exited")
        return True
    
    
    # @Author: Horia Cus
    # This function navigates to the desired tab that needs to be verified
    # Verifies that the following elements for all the KEA Tabs are displayed
        # KEA Player, timeline section, entry name, zoom level, tab name, timeline marker time set to zero,
    # Verifies the specific elements for each individual KEA Tab
    def keaTabVerification(self, entryName, keaTab, expectedSaveButtonState=False, hotspotsPresented=False, verifyZoomLevelOption=False):
        self.switchToKeaIframe()
        
        # Navigate to the desired kea tab
        if self.launchKEATab(entryName, keaTab) == False:
            writeToLog("INFO", "FAILED to access the " + keaTab.value + " KEA Tab")
            return False
                
        # Verify that the KEA Player is presented
        if self.wait_element(self.KEA_PLAYER_CONTAINER, 15, True) == False:
            writeToLog("INFO", "FAILED to display the v2 Player inside the tab")
            return False
          
        # Verify that the expected entry name is presented in the tab
        if self.verifyKeaEntryName(entryName, 5) == False:
            writeToLog("INFO", "FAILED to display the entry name: " + entryName + " inside the " + keaTab.value)
            return False
        
        # Verify that the timeline section is presented
        if self.wait_element(self.KEA_TIMELINE_PRESENTED_SECTIONS, 30, True) == False:
            writeToLog("INFO", "FAILED, the timeline section for " + keaTab.value + " is not presented")
            return False
        
        if verifyZoomLevelOption == True:
            # Verify the zoom options
            if self.verifyZoomLevelInTimeline() == False:
                writeToLog("INFO", "FAILED, the Zoom Leave wasn't be properly presented inside the " + keaTab.value)
                return False
        
        # Verify that a proper tab name is presented in the title
        tabNameLocator = (self.KEA_TAB_TITLE[0], self.KEA_TAB_TITLE[1].replace('TAB_NAME', keaTab.value))
        if self.wait_element(tabNameLocator, 1, True) == False:
            writeToLog("INFO", "FAILED to display the " + keaTab.value + " Tab Title")
            return False
        
        # Verify that the marker timeline starts from second zero
        try:
            markerTimeInTimeline = self.wait_element(self.EDITOR_REALTIME_MARKER, 3, True).text
        except Exception:
            writeToLog("INFO", "FAILED to take the time from the real time timeline section")
            return False
        
        if markerTimeInTimeline != '00:00.00':
            writeToLog("INFO", "FAILED, we expected to have the Timeline Marker at second zero but it was displayed at: " + markerTimeInTimeline)
            return False
        
        # Verify if the save option is enabled or disabled
        if keaTab == enums.keaTab.HOTSPOTS or keaTab == enums.keaTab.VIDEO_EDITOR:
            if self.verifySaveButtonState(expectedSaveButtonState) == False:
                return False
        
        # Verify the specific options from the Video Editor and Quiz KEA Tab
        if keaTab == enums.keaTab.VIDEO_EDITOR or keaTab == enums.keaTab.QUIZ:
            # Take the Media Details from the element
            try:
                mediaDetailsEntry = self.wait_element(self.KEA_EDITOR_MEDIA_DETAILS_CONTAINER, 1, True).text.splitlines()
            except Exception:
                writeToLog("INFO", "FAILED to display the details for the selected media entry inside the KEA " + keaTab.value + " Tab")
                return False
            
            # Verify that the presented entry name from media details matches with our entry name
            if mediaDetailsEntry[1] != entryName:
                writeToLog("INFO", "FAILED to display the " + entryName + " inside the Media Details list, instead " + mediaDetailsEntry[1] + " entry name has been presented")
                return False
            
            # Verify that the elements properly collapse
            if self.verifySidePanelState() == False:
                writeToLog("INFO", "FAILED to proper collapse and expand the side panel for the " + keaTab.value + " KEA Tab")
                return False
          
        # Verify the specific elements from Hotspots Tab
        if keaTab == enums.keaTab.HOTSPOTS:
            if self.keaHotspotsTabVerification(hotspotsPresented) == False:
                return False
        
        writeToLog("INFO", "The KEA Tab " + keaTab.value + " has been properly displayed in the KEA Page")    
        return True
    
    
    # @Author: Horia Cus
    # This function verifies the specific Hotspots elements while being in KEA Page
    # if hotspotsPresented=True, we will verify that the hotspot list is populated and that the specific Hotspots Action are presented
    # if hotspotsPresented=False, we will verify that a proper placeholder text is displayed
    def keaHotspotsTabVerification(self, hotspotsPresented):
        self.switchToKeaIframe()
        
        # Verify that the Hotspot Counter and Add Hotspot options are displayed
        if self.wait_element(self.KEA_HOTSPOTS_LIST_HEADER, 1, True) == False:
            writeToLog("INFO", "FAILED to display the Hotspots counter and Add Hotspot button")
            return False
                              
        if hotspotsPresented == True:
            # Take a list with all the available hotspots from the sidebar
            if self.wait_element(self.KEA_HOTSPOTS_PANEL_ITEM_TITLE, 5, True) == False:
                writeToLog("INFO", "FAILED to find any hotspots presented in the hotspots list from the side bar menu")
                return False
            
            # Verify that the action button is displayed
            if self.wait_element(self.KEA_HOTSPOTS_PANEL_MORE_HAMBURGER_MENU, 1, True) == False:
                writeToLog("INFO", "FAILED to find the trigger for the action menu inside the Hotspots List")
                return False
            
            # Verify that we are able to trigger the Hotspots Action drop down menu
            if self.click(self.KEA_HOTSPOTS_PANEL_MORE_HAMBURGER_MENU, 1, True) == False:
                writeToLog("INFO", "FAILED to trigger the Hotspots Action menu")
                return False
            
            # Verify that the Duplicate Hotspot Action is displayed
            if self.wait_element(self.KEA_HOTSPOTS_PANEL_ACTION_MENU_DUPLICATE, 1, True) == False:
                writeToLog("INFO", "FAILED to display the Duplicate Action inside the Hotspots Action Menu")
                return False

            # Verify that the Delete Hotspot Action is displayed
            if self.wait_element(self.KEA_HOTSPOTS_PANEL_ACTION_MENU_DELETE, 1, True) == False:
                writeToLog("INFO", "FAILED to display the Delete Action inside the Hotspots Action Menu")
                return False
            
            # Verify that the Edit Hotspot Action is displayed
            if self.wait_element(self.KEA_HOTSPOTS_PANEL_ACTION_MENU_EDIT, 1, True) == False:
                writeToLog("INFO", "FAILED to display the Edit Action inside the Hotspots Action Menu")
                return False
            
            if self.click(self.KEA_HOTSPOTS_PANEL_MORE_HAMBURGER_MENU, 1, True) == False:
                writeToLog("INFO", "FAILED to collapse the Hotspots Action menu")
                return False
        else:
            hotspotListContent = self.wait_element(self.KEA_HOTSPOTS_LIST_CONTENT, 1, True)
            
            # Verify that a proper placeholder is displayed while having no Hotspots for the entry
            if hotspotListContent.text != 'No hotspots for this video':
                writeToLog("INFO", "FAILED, we expected Zero Hotspots but the HS list is populated")
                return False
                
        return True
    
    
    # @Author: Horia Cus
    # This function verifies that the Side Panel can be collapsed and expanded
        # Verifies that when the Side Panel is collapsed, the player container is expanded
        # Verifies that when the Side Panel is expanded, the player container is collapsed
    def verifySidePanelState(self):
        self.switchToKeaIframe()
                        
        # Collapse the side panel
        self.click(self.KEA_COLLAPSE_PANEL_BUTTON, 1, True)
        
        expandedPlayerContainer = self.wait_element(self.KEA_EXPANDED_PLAYER_CONTAINER, 3, True) 
        
        # Verify that the player container is now expanded
        if expandedPlayerContainer == False:
            writeToLog("INFO", "FAILED to expand the player container after collapsing the Side Panel")
            return False
        
        expandedPlayerContainerXLocation = expandedPlayerContainer.location['x']
        
        # Expand the side panel
        self.click(self.KEA_EXPAND_PANEL_BUTTON, 1, True)
        
        collapsedPlayerContainer         = self.wait_element(self.KEA_COLLAPSED_PLAYER_CONTAINER, 3, True)
        
        # Verify that the player container is now collapsed
        if collapsedPlayerContainer == False:
            writeToLog("INFO", "FAILED to resume the player container to the initial size after re opening the Side Panel")
            return False
        
        collapsedPlayerContainerXLocation = collapsedPlayerContainer.location['x']
        
        # Verify that the Player Container is properly displayed based on the Side Panel status
        if collapsedPlayerContainerXLocation <= expandedPlayerContainerXLocation:
            writeToLog("INFO", "FAILED to center the Player Container after collapsing the side panel")
            return False
        
        return True
    
    
    # @Author: Horia Cus
    # This function verifies if the save button is enabled or disabled
    def verifySaveButtonState(self, isEnabled=True):
        self.switchToKeaIframe()
        
        # Take the save button element
        saveButton = self.wait_element(self.KEA_HOTSPOTS_SAVE_BUTTON, 5, True)
        
        if saveButton != False:
            # Take the parent of the save button element
            saveButtonParrent         = self.wait_element(self.KEA_HOTSPOTS_SAVE_BUTTON_PARENT, 1, True)
            # Take the arguments from the parent
            saveButtonArgumentsDict   = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', saveButtonParrent)
            
            # Convert the arguments into a string
            saveButtonArgumentsString = ', '.join("{!s}={!r}".format(key,val) for (key,val) in saveButtonArgumentsDict.items())
            
            # Verify if disabled is presented as argument
            isEnabledNumber = saveButtonArgumentsString.count('disabled')
            
            if isEnabled == True:
                if isEnabledNumber == 1:
                    writeToLog("INFO", "FAILED, the Save button it's displayed as being disabled, although we expected to be enabled")
            else:
                if isEnabledNumber == 0:
                    writeToLog("INFO", "FAILED, the Save button it's displayed as being enabled, although we expected to be disabled")
        else:
            writeToLog("INFO", "FAILED, the save button is not presented at all in the KEA Page")
            return False
        
        return True
    
    
    # @Author: Horia Cus
    # This function creates a Dictionary that contains a full list of details with different configurations for each Hotspot
    # desiredNumberOfHotspots = represents the number of hotspots lists that you want to have in the dictionary
    # entryDuration needs to be integer and cover the time of the entry, in order to proper create a start and end time of cue points
    # Make sure that you used an entry that has at least 10 seconds of length
    def keaGenerateHotspotsDictionary(self, desiredNumberOfHotspots, entryDuration):
        # Create empty variables that will be populated within the for loop     
        hotspotDetailsList                   = None
        hotspotGenereatedDict                = {}
        
        # Create and update the hotspot Dict with new Hotspots Details
        for x in range(0, desiredNumberOfHotspots):
            # Create a random Hotspot Title that can have at least four characters and maximum of 15            
            hotspotTitle                     = ''.join(random.choice(string.ascii_letters) for x in range(random.randint(4,15)))
            # Create a list with the available pre-defined locations
            hotspotLocationList              = [enums.keaLocation.BOTTOM_LEFT, enums.keaLocation.BOTTOM_RIGHT, enums.keaLocation.CENTER, enums.keaLocation.TOP_LEFT, enums.keaLocation.TOP_RIGHT]
            # Create an integer interval for the start time of the hotspots based on the entry duration
            hotspotCuePointStartTime         = random.randint(0,entryDuration-4)
            # Create an integer interval for the end time of the hotspots based on the entry duration
            hotspotCuePointEndTime           = random.randint(hotspotCuePointStartTime+3,entryDuration)
            # Create a string that contains a valid link format
            hotspotLink                      = 'https://' + ''.join(random.choice(string.ascii_letters) for x in range(random.randint(4,15))).lower() + '.' +''.join(random.choice(string.ascii_letters) for x in range(random.randint(2,4))).lower()
            # Create a list that contains the valid link string and empty
            hotspotLinkListWithEmptyLink     = [hotspotLink, '']
            # Pick randomly if the hotspot to have or not a link
            hotspotLinkRandom                = random.choice(hotspotLinkListWithEmptyLink)            
            # Create a list with the available pre-defined text styles
            hotspotTextStyleList             = [enums.textStyle.BOLD, enums.textStyle.NORMAL]
            # Pick randomly a text style from the available list
            hotspotTextStyle                 = random.choice(hotspotTextStyleList)
            # Font and Background color returns Fails due to KMS = TBA
            hotspotFontColor                 = ''
            hotspotBackgroundColor           = ''
            # Create an integer interval based on the maximum and minimum values from the Text Size option
            hotspotTextSize                  = random.randint(12,18)
            # Create an integer interval based on the maximum and minimum values from the Roundness Size option
            hotspotRoundnessSize             = random.randint(2,16)
            
            # Verify if the hotspot location has been used already for an Hotspot from our Dictionary
            if len(hotspotGenereatedDict) >= 1:
                try:
                    for i in range(0, len(hotspotGenereatedDict)):
                        if len(hotspotGenereatedDict) == 1:
                            availableHotspotLocationList           = [x for x in hotspotLocationList if x != hotspotGenereatedDict[str(i)][1]]
                        
                        # Verify if a hotspot location is free or not
                        if type(availableHotspotLocationList) is list and len(availableHotspotLocationList) == 0:
                            break
                        
                        # Create a list with the unused hotspot locations
                        if len(hotspotGenereatedDict) > 1:
                            availableHotspotLocationList           = [x for x in availableHotspotLocationList if x != hotspotGenereatedDict[str(i)][1]]
                except Exception:
                    pass

            else:
                availableHotspotLocationList = hotspotLocationList
            
            # If a hotspot location is available, we will use first the pre-defined locations
            if len(availableHotspotLocationList) >= 1:
                hotspotLocation              = availableHotspotLocationList[0]
            # If no pre-defined hotspot locations are available, we will use the Add New button option and place the hotspot randomly
            else:
                hotspotLocation              = ''
                
            hotspotDetailsList               = [hotspotTitle, hotspotLocation, hotspotCuePointStartTime, hotspotCuePointEndTime, hotspotLinkRandom, hotspotTextStyle, hotspotFontColor, hotspotBackgroundColor, hotspotTextSize, hotspotRoundnessSize]
            
            
            hotspotGenereatedDict.update({str(x):hotspotDetailsList})
        
        # Verify that the expected number of hotsptos were inserted inside the dictionary
        if len(hotspotGenereatedDict) != desiredNumberOfHotspots:
            writeToLog("INFO", "FAILED, we expected to have a dictionary that contains " + str(desiredNumberOfHotspots) + " number of hotspots but only " + str(len(hotspotGenereatedDict)))
            return False
        
        return hotspotGenereatedDict
    
    
    # @Author: Horia Cus
    # Verify that the user is unable to create a new hotspot while having an invalid URL
    # Verification process is supported in both Advanced Settings and Add Hotspot Tool Tip
    # hotspotCreationScreen must contain enum ( e.g  enums.keaHotspotCreationScreen.ADVANCED_SETTINGS )
    # invalidURLString must contain any string without . ( e.g invalidurlstring)
    def verifyHotspotsCreationWithInvalidURL(self, hotspotCreationScreen, invalidURLString):
        self.switchToKeaIframe()
        
        # Trigger the Add New Hotspot tool tip in order to verify the invalid URL functionality inside the Add Hotspot Tool Tip
        if self.click(self.KEA_HOTSPOTS_ADD_NEW_BUTTON, 5, True) == False:
            writeToLog("INFO", "FAILED to click on the Add new Button")
            return False
        
        # Reach the Advanced Settings creen and take the specific locators
        if hotspotCreationScreen == enums.keaHotspotCreationScreen.ADVANCED_SETTINGS:
            if self.click(self.KEA_HOTSPOTS_ADVANCED_SETTINGS, 1, True) == False:
                writeToLog("INFO", "FAILED to activate the Advanced Settings for Hotspots")
                return False
            
            doneButtonLocator   = self.KEA_HOTSPOTS_DONE_BUTTON_ADVANCED_SETTINGS
            cancelButtonLocator = self.KEA_HOTSPOTS_CANCEL_BUTTON
        # Take the locators from the Add Hotspot tool tip
        else:
            doneButtonLocator   = self.KEA_HOTSPOTS_DONE_BUTTON_NORMAL
            cancelButtonLocator = self.KEA_HOTSPOTS_TOOL_TIP_CREATION_CANCEL_BUTTON
        
        # Insert the invalid url string inside the link field
        if self.clear_and_send_keys(self.KEA_HOTSPOTS_FORM_LINK_INPUT_FIELD, invalidURLString, True) == False:
            writeToLog("INFO", "FAILED to insert the invalid URL:" + invalidURLString + " inside Link Address from the Add Hotspots tool tip")
            return False
        
        # Try to save the hotspot by clicking on the done button
        if self.click(doneButtonLocator, 1, True) == False:
            writeToLog("INFO", "FAILED to click on the Done button from the Add Hotspots tool tip")
            return False
        
        # Take the element that needs to be triggered while having an invalid URL
        urlInputErrorElement = self.wait_element(self.KEA_HOTSPOTS_URL_INPUT_ERROR, 5, True)
        
        # Verify that the element for invalid URL is presented
        if urlInputErrorElement == False:
            writeToLog("INFO", "FAILED to display the Invalid URL Format error")
            return False
        else:
            # Verify that the expected error message is displayed
            if urlInputErrorElement.text != 'Invalid URL Format':
                writeToLog("INFO", "FAILED, we expected to see 'Invalid URL Format' error but " + urlInputErrorElement.text + " error was presented")
                return False
        
        # Verify that the Hotspot creation screen remained present and it can be dismissed
        if self.click(cancelButtonLocator, 1, True) == False:
            writeToLog("INFO", "FAILED to dismiss the " + hotspotCreationScreen.value + " Screen by clicking on the Cancel button")
            return False        
        
        writeToLog("INFO", "The invalid url has been successfully verified while being in " + hotspotCreationScreen.value + " Screen")
        return True
    

    # @Author: Horia Cus
    # This function will return the index number for the desired hotspotName from the HS List ( Side Bar )
    def returnHotspotIndexFromList(self, hotspotName):
        self.switchToKeaIframe()
        
        # Take a list with all the available hotspots from the HS List ( Side Bar )
        hotspotsPanelTitle = self.wait_elements(self.KEA_HOTSPOTS_PANEL_ITEM_TITLE, 5)
        
        # Verify that we were able to find hotspots inside the HS List
        if hotspotsPanelTitle == False:
            writeToLog("INFO", "FAILED to find any available hotspots in the side bar panel")
            return False
        
        # Take the hotspot index specific for the HS List ( Side Bar )
        hotspotIndexLocation = None
        for x in range(0, len(hotspotsPanelTitle)):
            # Verify if the current iterrated hotspot matches with our desired one
            if hotspotsPanelTitle[x].text == hotspotName:
                hotspotIndexLocation = x
                break
            
            # Verify that we were able to find our hotspot within the available number of tries
            if x + 1 == len(hotspotsPanelTitle):
                writeToLog("INFO", "FAILED to find the " + hotspotName + " inside the sidebar panel")
                return False
        
        writeToLog("INFO", "Hotspot Index Location for " + hotspotName + " hotspot is at: " + str(hotspotIndexLocation))  
        return hotspotIndexLocation
    

    # @Author: Horia Cus
    # This function will open the Advanced Settings Screen for the desired hotspotName
    def openHotspotAdvancedSettings(self, hotspotName):
        self.switchToKeaIframe()
        
        hotspotIndexLocation = self.returnHotspotIndexFromList(hotspotName)
        
        if type(hotspotIndexLocation) is not int:
            writeToLog("INFO", "FAILED to take the hospot: " + hotspotName + " index location")
            return False

        # Create the elements for the Hotspot Title
        presentedHotspotsTitle  = self.wait_elements(self.KEA_HOTSPOTS_PANEL_ITEM_TITLE, 1)
        
        # Highlight the hotspotName field by clicking on its container
        if self.clickElement(presentedHotspotsTitle[hotspotIndexLocation]) == False:
            writeToLog("INFO", "FAILED to highligth the " + hotspotName + " hotspot from the Hotspot List Screen")
            return False
        
        # Trigger the Advanced Settings Screen
        if self.click(self.KEA_HOTSPOTS_ADVANCED_SETTINGS, 1, True) == False:
            writeToLog("INFO", "FAILED to click on the Advanced Settings button for " + hotspotName + " hotspot")
            return False
        
        writeToLog("INFO", "Hotspot Advanced Setting Screen has been successfully opened for: " + hotspotName)
        return True