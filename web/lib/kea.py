import subprocess
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
    KEA_LAUNCH                                                              = ('xpath', "//i[@class='icon-editor']")
    KEA_APP_DISPLAY                                                         = ('id', 'kea-anchor')
    KEA_IFRAME                                                              = ('xpath', '//iframe[@class="span12 hostedEnabled kea-frame kea-iframe-js"]')
    KEA_QUIZ_PLAYER                                                         = ('id', 'quiz-player_ifp')
    KEA_LOADING_SPINNER                                                     = ('class_name', 'spinner')
    KEA_QUIZ_QUESTION_FIELD                                                 = ('id', 'questionTxt')
    KEA_QUIZ_ANSWER                                                         = ('id', 'ANSWER_NUMBER')
    KEA_QUIZ_ANSWER_GENERAL                                                 = ('xpath', "//textarea[contains(@id,'answer-text')]") 
    KEA_EDITOR_TAB                                                          = ('xpath', "//a[@aria-label='Video Editor']") 
    KEA_QUIZ_TAB                                                            = ('xpath', "//a[@class='nav-button' and @aria-label='Quiz']") 
    KEA_QUIZ_TAB_ACTIVE                                                     = ('xpath', "//a[@class='nav-button active' and @aria-label='Quiz']") 
    KEA_QUIZ_ADD_ANSWER_BUTTON                                              = ('xpath', '//div[@class="add-answer-btn"]') 
    KEA_QUIZ_BUTTON                                                         = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="BUTTON_NAME"]')
    KEA_QUIZ_SHUFFLE_BUTTON                                                 = ('xpath', '//div[@class="shuffle-answers"]') 
    EDITOR_TABLE                                                            = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]')
    EDITOR_TABLE_SIZE                                                       = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]/tbody/tr')
    EDITOR_NO_MORE_MEDIA_FOUND_MSG                                          = ('xpath', '//div[@id="quizMyMedia_scroller_alert" and text()="There are no more media items."]')
    EDITOR_TIMELINE                                                         = ('xpath', '//div[@class="kea-timeline-playhead" and @style="transform: translateX(PIXELpx);"]')
    EDITOR_TIME_PICKER                                                      = ('xpath', "//input[@class='ui-inputtext ui-corner-all ui-state-default ui-widget ui-state-filled']")
    EDITOR_REALTIME_MARKER                                                  = ('xpath', "//span[@class='realtime-marker__head-box-time']")
    EDITORT_TIMELINE_SPLIT_ICON                                             = ('xpath', "//button[@aria-label='Split']")
    EDITOR_TIMELINE_DELETE_BUTTON                                           = ('xpath', "//button[@aria-label='Delete']")
    EDITOR_SAVE_BUTTON                                                      = ('xpath', "//button[@class='button--save ui-button-secondary default-button button--editor ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
    EDITOR_SAVE_A_COPY_BUTTON                                               = ('xpath', "//button[@class='save-as-button branded-button button--editor ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only ng-star-inserted']")
    EDITOR_SAVE_BUTTON_CONF                                                 = ('xpath', "//button[@class='button modal-footer-buttons__save branded-button ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
    EDITOR_SAVED_MSG                                                        = ('xpath', "//strong[contains(.,'Media was successfully saved.')]")
    EDITOR_SAVED_OK_MSG                                                     = ('xpath', "//button[contains(.,'OK')]")
    EDITOR_CREATE_BUTTON                                                    = ('xpath', "//button[contains(.,'Create')]")
    EDITOR_SUCCESS_MSG                                                      = ('xpath', "//p-header[contains(.,'Success')]")
    EDITOR_TOTAL_TIME                                                       = ('xpath', "//span[@class='total-time']")
    EDITOR_GO_TO_MEDIA_PAGE_BUTTON                                          = ('xpath', "//a[contains(.,'Media Page')]")
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
        
        # Click on select button in order to open KEA
        if self.click(self.KEA_SELECT_VIDEO_FOR_EDIT) == False:
            writeToLog("INFO","FAILED to select entry and open KEA")
            return False 
        
        sleep(4)   
        
        # Verify that we are in KEA page and app is displayed
        if self.wait_visible(self.KEA_APP_DISPLAY, 40) == False:
            writeToLog("INFO","FAILED to display KEA page")
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
        else:
            writeToLog("INFO","FAILED, unknown doneoption: '" + doneOption + "'")
            return False 
         
        sleep (3)   
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
            self.click(self.clsCommon.entryPage.ENTRY_PAGE_DETAILS_BUTTON)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
                writeToLog("INFO","FAILED to click on Actions button (at entry page)")
                return False
            
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
        
        writeToLog("INFO","Success, KEA has been launched for: " + entryName) 
        return True
    

    # @Author: Tzachi guetta
    # interface to KEA's timeline functionalities: split, (set IN\out, delete, Fade IN\out - TBD)
    def keaTimelinefunc(self,entryName, splitStartTime, splitEndTime, navigateTo, navigateFrom, openEditorTab, isCreateClippingPermissionIsOn=False):
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
        sleep(3)
        
        if openEditorTab == True:
            if self.click(self.KEA_EDITOR_TAB) == False:
                writeToLog("INFO","FAILED to click on Editor Tab")
                return False

        if self.setEditorStartTime(splitStartTime) == False:
            return False              
            
        sleep(1)
        if self.click(self.EDITORT_TIMELINE_SPLIT_ICON) == False:
                writeToLog("INFO","FAILED to click Split icon (time-line)")
                return False
        sleep(1)
        
        if self.setEditorStartTime(splitEndTime) == False:
            return False   
        
        sleep(1)
        if self.click(self.EDITORT_TIMELINE_SPLIT_ICON) == False:
            writeToLog("INFO","FAILED to click Split icon (time-line)")
            return False
        
        sleep(1)
        if self.click(self.EDITOR_TIMELINE_DELETE_BUTTON) == False:
            writeToLog("INFO","FAILED to click delete icon (time-line)")
            return False
        
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
    def trimEntry(self, entryName, splitStartTime, splitEndTime, expectedEntryDuration, navigateTo, navigateFrom, openEditorTab=False):
        if self.keaTimelinefunc(entryName, splitStartTime, splitEndTime, navigateTo, navigateFrom, openEditorTab) == False:
            writeToLog("INFO","FAILED to split the entry: " + str(entryName))
            return False            
        
        sleep(1)
        if self.click(self.EDITOR_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Save")
            return False
        
        sleep(1)
        if self.click(self.EDITOR_SAVE_BUTTON_CONF, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on Save confirmation button")
            return False
        
        if self.wait_element(self.EDITOR_SAVED_MSG, 360) == False:
            writeToLog("INFO","FAILED, ""Media was successfully saved."" - msg is missing")
            return False
        
        if self.click(self.EDITOR_SAVED_OK_MSG, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on 'OK' after trimmed msg")
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
    def clipEntry(self, entryName, splitStartTime, splitEndTime, expectedEntryDuration, navigateTo, navigateFrom, openEditorTab=False, isCreateClippingPermissionIsOn=False):
        self.keaTimelinefunc(entryName, splitStartTime, splitEndTime, navigateTo, navigateFrom, openEditorTab, isCreateClippingPermissionIsOn)
        
        sleep(1)
        if self.click(self.EDITOR_SAVE_A_COPY_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Save")
            return False
        
        sleep(1)
        if self.click(self.EDITOR_CREATE_BUTTON, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on Save confirmation button")
            return False
        
        if self.wait_element(self.EDITOR_SUCCESS_MSG, 360) == False:
            writeToLog("INFO","FAILED, ""Your media has been saved in My Media"" - message is missing")
            return False
        
        sleep(1)
        if self.click(self.EDITOR_GO_TO_MEDIA_PAGE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'Go to Media Page' button")
            return False
        
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


    # NOT FINISHED:
    # the following function will create a Quiz (within the given dictQuestions)
    # Please follow the individual list structure for each Quiz Question type
    # questionMultiple     = ['00:10', enums.QuizQuestionType.Multiple, 'Question Title for Multiple Choice', 'question #1 option #1', 'question #1 option #2', 'question #1 option #3', 'question #1 option #4', 'Hint Text', 'Why Text']
    # questionTrueAndFalse = ['00:15', enums.QuizQuestionType.TRUE_FALSE, 'Question Title for True and False', 'True text', 'False text', 'Hint Text', 'Why Text']
    # questionReflection   = ['00:20', enums.QuizQuestionType.REFLECTION, 'Question Title for Reflection Point', 'Hint Text', 'Why Text']
    # dictQuestions        = {'1':questionMultiple,'2':questionTrueAndFalse,'3':questionReflection}
    # If you want to change the answer order you can use this function: changeAnswerOrder
    def quizCreation(self, entryName, dictQuestions, dictDetails='', dictScores='', dictExperience='', timeout=15):
        sleep(25)
        if self.searchAndSelectEntryInMediaSelection(entryName) == False:
            writeToLog("INFO", "FAILED to navigate to " + entryName)
            return False
        sleep(timeout)
        
        # We create the locator for the KEA Quiz Question title field area (used only in the "Reflection Point" and "True and False" Quiz Questions)
        questionField = (self.KEA_OPTION_TEXTAREA_FIELD[0], self.KEA_OPTION_TEXTAREA_FIELD[1].replace('FIELD_NAME', 'questionTxt')) 
                   
        for questionNumber in dictQuestions:
            questionDetails = dictQuestions[questionNumber]
            
            self.switchToKeaIframe() 
            if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 30) == False:
                writeToLog("INFO","FAILED to wait until spinner isn't visible")
                return False 
            
            # Specifying the time stamp, where the Quiz Question should be placed within the entry
            # click on the editor in order to higlight the timeline field and select all the text
            if self.click(self.EDITOR_TIME_PICKER, 1, True) == False:
                writeToLog("INFO", "FAILED to click on the kea timeline field")
                return False
            
            timestamp = questionDetails[0]
            
            # replace the text present in the timestamp field with the new one
            if self.send_keys(self.EDITOR_TIME_PICKER, timestamp + Keys.ENTER) == False:
                writeToLog("INFO", "FAILED to select the timeline field text")
                return False
        
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
    # This function can navigate to a specific entry and initiate the KEA Quiz option
    # This function work for both entries that have Quiz created or not
    # entryName must be inserted in order to verify that the KEA page has been successfully opened and loaded
    def initiateQuizFlow(self, entryName, navigateToEntry=False, timeOut=25):
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
        
        if self.wait_element(start_button, 5, True) != False:
            if self.click(start_button, 5, True) == False:
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
                    return True
                else:
                    writeToLog("INFO", "The KEA entry-name doesn't matches with " + entryName + " entry")
                    return False
            except:
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    writeToLog("INFO", "FAILED to find the " + entryName + " within the " + str(timeout) + " seconds")
                    return False
                pass
                        

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
            
            if self.wait_element(tmpKEAOptionSeeking, 1, True) != False:   
                if self.verifyKEAOptionState(enums.KEAQuizOptions.NO_SEEKING_FORWARD, True) == False:
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

            if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 50) == False:
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
        
        # We verify all the available quiz question pointers, by verifying the quiz number,time stamp and quiz title
        for x in range(0, len(presentedQuestionsInTimeline)):
            # We take the locator element for the current quiz number
            currentQuestion = presentedQuestionsInTimeline[x]
            
            # We hover over the current quiz number, in order to verify the elements
            try:
                ActionChains(self.driver).move_to_element(currentQuestion).perform()
            except Exception:
                writeToLog("INFO", "FAILED to hover over the quiz number " + str(x+1))
                return False
            
            # We take the quiz title and time stamp for the current quiz number
            currentQuestionDetails = questionDict[str(x+1)]
            
            # We take the presented quiz number, title and time stamp
            try:
                questionNumberPresented     = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_NUMBER, 1, True).text
                questionTitlePresented      = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE, 1, True).text
                questionTimestampPresented  = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_QUESTION_TIMESTAMP, 1, True).text
            except Exception:
                writeToLog("INFO", "FAILED to find the question details while hovering over the question: " + currentQuestionDetails[2])
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
                action.move_to_element(questionCuePoint).perform()
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
        
        # Take all the available quiz question pointers from the timeline KEA section
        quizCuePoint = self.wait_elements(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE, 1)
        
        # Iterate each available question
        for questionNumber in changeTimelineOrderDict:
            
            # Take the details for the current question ( number of seconds that the quiz should be moved by )
            questionDetails = changeTimelineOrderDict[questionNumber]
            
            # Create the locator for the current question
            questionCuePoint = quizCuePoint[int(questionNumber) - 1]
            
            # Enter in the quiz question editing screen
            if self.clickElement(questionCuePoint) == False:
                writeToLog("INFO", "FAILED to select the question cue point for " + questionNumber + " question number")
                return False
                
            action = ActionChains(self.driver)
            # Move the quiz number to a new timeline location
            try:
                action.move_to_element(questionCuePoint).pause(1).click_and_hold().move_by_offset(35.7*questionDetails, 0).release().perform()
            except Exception:
                writeToLog("INFO", "FAILED to move question number " + str(questionNumber)  + " by " + str(questionDetails) + " seconds")
                return False
            
            # Save the new timeline location
            if self.saveQuizChanges() == False:
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
                
                action = ActionChains(self.driver)
                # Hover over the current Question Cue Point
                try:
                    action.move_to_element(questionCuePoint).perform()
                except Exception:
                    writeToLog("INFO", "FAILED to hover over the quiz " + str(x+1) + " question number Cue Point")
                    return False
                
                # Take the presented title from the hovered Cue Point
                questionTitlePresented = self.wait_element(self.KEA_TIMELINE_SECTION_QUESTION_BUBBLE_TITLE, 5, True)
                
                # Verify that the Question Title is presented while hovering over the Cue Point
                if questionTitlePresented == False:
                    writeToLog("INFO", "FAILED to take the question title from the question cue point number " + str(x+1))
                    return False
                else:
                    # Take the Question Title presented on the hovered Cue Point
                    questionTitlePresented = questionTitlePresented.text
                    
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