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



class Kea(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Upload locators:
    #=============================================================================================================
    KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON          = ('xpath', "//button[contains(@class,'question-type-button question-types-icon multiple-options-question-type')]")
    KEA_SELECT_VIDEO_FOR_EDIT                     = ('xpath', '//a[@class="btn btn-small btn-primary btn-select-media"]')
    KEA_LAUNCH                                    = ('xpath', "//i[@class='icon-editor']")
    KEA_APP_DISPLAY                               = ('id', 'kea-anchor')
    KEA_IFRAME                                    = ('xpath', '//iframe[@class="span12 hostedEnabled kea-frame kea-iframe-js"]')
    KEA_QUIZ_PLAYER                               = ('id', 'quiz-player_ifp')
    KEA_LOADING_SPINNER                           = ('class_name', 'spinner')
    KEA_QUIZ_QUESTION_FIELD                       = ('id', 'questionTxt')
    KEA_QUIZ_ANSWER                               = ('id', 'ANSWER_NUMBER')
    KEA_EDITOR_TAB                                = ('xpath', "//a[@aria-label='Video Editor']") 
    KEA_QUIZ_TAB                                  = ('xpath', "//a[@class='nav-button' and @aria-label='Quiz']") 
    KEA_QUIZ_TAB_ACTIVE                           = ('xpath', "//a[@class='nav-button active' and @aria-label='Quiz']") 
    KEA_QUIZ_ADD_ANSWER_BUTTON                    = ('xpath', '//div[@class="add-answer-btn"]') 
    KEA_QUIZ_BUTTON                               = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="BUTTON_NAME"]')
    EDITOR_TABLE                                  = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]')
    EDITOR_TABLE_SIZE                             = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]/tbody/tr')
    EDITOR_NO_MORE_MEDIA_FOUND_MSG                = ('xpath', '//div[@id="quizMyMedia_scroller_alert" and text()="There are no more media items."]')
    EDITOR_TIMELINE                               = ('xpath', '//div[@class="kea-timeline-playhead" and @style="transform: translateX(PIXELpx);"]')
    EDITOR_TIME_PICKER                            = ('xpath', "//input[@class='ui-inputtext ui-corner-all ui-state-default ui-widget ui-state-filled']")
    EDITORT_TIMELINE_SPLIT_ICON                   = ('xpath', "//button[@aria-label='Split']")
    EDITOR_TIMELINE_DELETE_BUTTON                 = ('xpath', "//button[@aria-label='Delete']")
    EDITOR_SAVE_BUTTON                            = ('xpath', "//button[@class='button--save ui-button-secondary default-button button--editor ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
    EDITOR_SAVE_A_COPY_BUTTON                     = ('xpath', "//button[@class='save-as-button branded-button button--editor ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only ng-star-inserted']")
    EDITOR_SAVE_BUTTON_CONF                       = ('xpath', "//button[@class='button modal-footer-buttons__save branded-button ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")
    EDITOR_SAVED_MSG                              = ('xpath', "//strong[contains(.,'Media was successfully saved.')]")
    EDITOR_SAVED_OK_MSG                           = ('xpath', "//button[contains(.,'OK')]")
    EDITOR_CREATE_BUTTON                          = ('xpath', "//button[contains(.,'Create')]")
    EDITOR_SUCCESS_MSG                            = ('xpath', "//p-header[contains(.,'Success')]")
    EDITOR_TOTAL_TIME                             = ('xpath', "//span[@class='total-time']")
    EDITOR_GO_TO_MEDIA_PAGE_BUTTON                = ('xpath', "//a[contains(.,'Media Page')]")
    KEA_ENTRY_NAME                                = ('xpath', "//span[@class='entry-name']")
    KEA_TOGGLE_MENU_OPTION                        = ('xpath', "//span[text()='OPTION_NAME']")  
    KEA_OPTION_NORMAL                             = ('xpath', "//label[contains(@class,'ui-chkbox-label') and text()='OPTION_NAME']")  
    KEA_OPTION_ACTIVE                             = ('xpath', "//label[contains(@class,'ui-label-active') and text()='OPTION_NAME']")
    KEA_OPTION_INPUT_FIELD                        = ('xpath', "//input[@id='FIELD_NAME']")
    KEA_OPTION_TEXTAREA_FIELD                     = ('xpath', "//textarea[@id='FIELD_NAME']")  
    KEA_PREVIEW_ICON                              = ('xpath', "//i[@class='kicon-preview']") 
    KEA_LOADING_SPINNER_CONTAINER                 = ('xpath', "//div[@class='spinner-container']") 
    KEA_PREVIEW_PLAY_BUTTON                       = ('xpath', "//a[@class='icon-play  comp largePlayBtn  largePlayBtnBorder']")
    KEA_PREVIEW_CLOSE_BUTTON                      = ('xpath', '//i[contains(@class,"kCloseBtn")]')   
    KEA_IFRAME_PREVIEW_PLAYER                     = ('xpath', "//iframe[@class='ng-star-inserted' and contains(@src,'iframeembed=true&playerId=kaltura_player')]")
    KEA_PREVIEW_WELCOME_MESSAGE                   = ('xpath', "//div[@class='welcomeMessage']")
    KEA_PREVIEW_INSTRUCTIONS                      = ('xpath', "//div[@class='InvideoTipMessage']")
    KEA_PREVIEW_DOWNLOAD                          = ('xpath', "//div[@class='pdf-download-txt']")
    KEA_IFRAME_BLANK                              = ('xpath', "//iframe[@title='Kaltura Editor Application']")  
    KEA_QUIZ_OPTIONS_REVERT_TO_DEFAULT_BUTTON     = ('xpath', "//button[@class='link-button pull-right ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")    
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
           
        # Click add new question button
        if self.click(self.KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON) == False:
            writeToLog("INFO","FAILED to click add question button")
            return False 
 
        # Add question fields
        if self.fillQuizFields(questionText, answerText, additionalAnswerList) == False:
            writeToLog("INFO","FAILED to fill question fields")
            return False 
         
        # Save Question
        if self.keaQuizClickButton(enums.KeaQuizButtons.SAVE) == False:
            writeToLog("INFO","FAILED to Save question")
            return False  
         
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 30) == False:
            writeToLog("INFO","FAILED to wait until spinner isn't visible")
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
    def fillQuizFields(self, questionText, answerText, additionalAnswerList):   
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
    def launchKEA(self, entryName, navigateTo, navigateFrom):
        if self.clsCommon.navigateTo(navigateTo, navigateFrom, entryName) == False:
            return False
        
        if navigateTo == enums.Location.EDIT_ENTRY_PAGE:
            if self.click(self.KEA_LAUNCH) == False:
                writeToLog("INFO","FAILED to click on KEA launch button")
                return False
            
        elif navigateTo == enums.Location.ENTRY_PAGE:
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
                writeToLog("INFO","FAILED to click on Actions button (at entry page)")
                return False
            
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_KEA_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Actions -> Launch KEA button (at entry page)")
                return False
            
        # Verify that we are in KEA page and app is displayed
        if self.wait_visible(self.KEA_APP_DISPLAY, 40) == False:
            writeToLog("INFO","FAILED to display KEA page")
            return False              
        
        writeToLog("INFO","Success, KEA has been launched for: " + entryName) 
        return True
    

    # @Author: Tzachi guetta
    # interface to KEA's timeline functionalities: split, (set IN\out, delete, Fade IN\out - TBD)
    def keaTimelinefunc(self,entryName, splitStartTime, splitEndTime, navigateTo, navigateFrom, openEditorTab):
        if self.launchKEA(entryName, navigateTo, navigateFrom) == False:
            writeToLog("INFO","Failed to launch KEA for: " + entryName)
            return False
        
        sleep(2)
        self.refresh()
        sleep(3)
        self.switchToKeaIframe()
        sleep(3)
        
        if openEditorTab == True:
            if self.click(self.KEA_EDITOR_TAB) == False:
                writeToLog("INFO","FAILED to click on Editor Tab")
                return False
            
        self.click(self.EDITOR_TIME_PICKER)           
        if self.send_keys(self.EDITOR_TIME_PICKER, splitStartTime + Keys.ENTER) == False:
            writeToLog("INFO","FAILED to insert start time into editor input field")
            return False
        
        sleep(1)
        if self.click(self.EDITORT_TIMELINE_SPLIT_ICON) == False:
                writeToLog("INFO","FAILED to click Split icon (time-line)")
                return False
        sleep(1)
        
        self.click(self.EDITOR_TIME_PICKER) 
        if self.send_keys(self.EDITOR_TIME_PICKER, splitEndTime + Keys.ENTER) == False:
            writeToLog("INFO","FAILED to insert start time into editor input field")
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
    
        
    # @Author: Tzachi guetta  
    # Currently support split only     
    # expectedEntryDuration = the duration of the new entry  
    def trimEntry(self, entryName, splitStartTime, splitEndTime, expectedEntryDuration, navigateTo, navigateFrom, openEditorTab=False):
        self.keaTimelinefunc(entryName, splitStartTime, splitEndTime, navigateTo, navigateFrom, openEditorTab)
        
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
    def clipEntry(self, entryName, splitStartTime, splitEndTime, expectedEntryDuration, navigateTo, navigateFrom, openEditorTab=False):
        self.keaTimelinefunc(entryName, splitStartTime, splitEndTime, navigateTo, navigateFrom, openEditorTab)
        
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
    # Currently support question type=Multiple ONLY     
    def quizCreation(self, entryName, dictQuestions, timeout=15): #TBD: dictDetails, dictScores, dictExperience
        sleep(25)
        self.searchAndSelectEntryInMediaSelection(entryName)
        sleep(timeout) 
                   
        for questionNumber in dictQuestions:
            questionDetails = dictQuestions[questionNumber]
            
            self.switchToKeaIframe() 
                    
            timestamp = questionDetails[0]
            if self.clear_and_send_keys(self.EDITOR_TIME_PICKER, timestamp + Keys.ENTER) == False:
                writeToLog("INFO","FAILED to insert the time-stamp of question # " + questionNumber)
                return False
            
            qestionType = questionDetails[1]
            if qestionType == enums.QuizQuestionType.Multiple:
                
                # Click on add new multiple option question type button
                if self.click(self.KEA_ADD_NEW_MULTIPLE_QUESTION_BUTTON) == False:
                        writeToLog("INFO","FAILED to click on add new multiple option question type button")
                        return False                 
         
                # Add question fields
                QuizQuestion1AdditionalAnswers = [questionDetails[4], questionDetails[5], questionDetails[6]]
                if self.fillQuizFields(questionDetails[2], questionDetails[3], QuizQuestion1AdditionalAnswers) == False:
                    writeToLog("INFO","FAILED to fill question fields")
                    return False 
                 
                # Save Question
                if self.keaQuizClickButton(enums.KeaQuizButtons.SAVE) == False:
                    writeToLog("INFO","FAILED to Save question")
                    return False  
                 
                if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 30) == False:
                    writeToLog("INFO","FAILED to wait until spinner isn't visible")
                    return False 
                sleep(2)
                
            elif qestionType == enums.QuizQuestionType.REFLECTION:
                return False
            else:
                return False
                
        self.switchToKeaIframe() 
        self.clickDone()
        return True
    
    
    # @Author: Horia Cus
    # This function can navigate to a specific entry and open the KEA - Quiz Tab
    # entryName must be inserted in order to verify that the KEA page has been successfully opened and loaded
    def initiateQuizTab(self, entryName, navigateToEntry=False, timeout=90):
        if navigateToEntry == True:
            if self.launchKEA(entryName, navigateTo=enums.Location.ENTRY_PAGE, navigateFrom=enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","Failed to launch KEA for: " + entryName)
                return False
        
        self.switchToKeaIframe()
        
        if self.verifyKeaEntryName(entryName, timeout) == False:
            writeToLog("INFO", "FAILED to load the page until the " + entryName + " was present")
            return False
        
        if self.click(self.KEA_QUIZ_TAB, 5, True) == False:
            writeToLog("INFO","FAILED to click on the KEA Quiz tab menu")
            return False  
    
        if self.keaQuizClickButton(enums.KeaQuizButtons.START) == False:
            writeToLog("INFO","FAILED to click on the start button")
            return False
                
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER_CONTAINER, 60) == False:
            writeToLog("INFO","FAILED, the loading spinner remained in infinite loading")
            return False
        
        sleep(3)
                
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
    # This function verifies if a specific KEA element from any KEA option is present or not in the preview screen
    # Supports only KEA Details section now
    def verifyQuizWelcomeScreenElements(self, keaOption, keaElement, timeout=60):
        if keaOption == enums.KEAQuizOptions.SHOW_WELCOME_PAGE:
            tmpLocator = self.KEA_PREVIEW_WELCOME_MESSAGE
            
        elif keaOption == enums.KEAQuizOptions.INSTRUCTIONS:
            tmpLocator = self.KEA_PREVIEW_INSTRUCTIONS

        elif keaOption == enums.KEAQuizOptions.ALLOW_DOWNLOAD:
            tmpLocator = self.KEA_PREVIEW_DOWNLOAD
            
        else:
            writeToLog("INFO", "Make sure that you have used a supported KEA Option")
            return False
        
        self.switchToKEAPreviewPlayer()

        if self.wait_element(self.KEA_PREVIEW_PLAY_BUTTON, 5, True) != False:
            if self.click(self.KEA_PREVIEW_PLAY_BUTTON, 5, True) == False:
                writeToLog("INFO", "FAILED to activate the preview screen")
                return False
        
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                el = self.wait_element(tmpLocator, 60, multipleElements=True)
                if el.text == keaElement:
                    self.setImplicitlyWaitToDefault()
                    writeToLog("INFO", "The " + keaElement + " has been found in KEA page")
                    return True
                else:
                    writeToLog("INFO", "The KEA element doesn't match with " + keaElement + " entry")
                    return False
            except:
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    writeToLog("INFO", "FAILED to find the " + keaElement + " within the " + str(timeout) + " seconds")
                    return False
                pass
            

    # @Author: Horia Cus
    # This function triggers a specific KEA Section and it can enable / disable or add an input for any available KEA option
    # keaCategory = must be enum
    # keaOption must be enum and have a map
    def editQuizOptions(self, keaSection, keaOptionDict):
        if keaSection != '':
            tmpKEASection = (self.KEA_TOGGLE_MENU_OPTION[0], self.KEA_TOGGLE_MENU_OPTION[1].replace('OPTION_NAME', keaSection.value))
        else:
            writeToLog("INFO", "Please specify in which KEA section we should enable or disable the options")
            return False
        
        self.switchToKeaIframe()
        sleep(1)
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to click on the " + keaSection.value)
            return False
        sleep(3)
                
        for options in keaOptionDict:
            if keaOptionDict[options] == True:
                if self.changeKEAOptionState(options, True) == False:
                    return False
                
            elif keaOptionDict[options] == False:
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
    # If stateEnabled=True, it will verify if the specific KEA Option is enabled
    # If stateEnabled=False, it will verify if the specific KEA Option is disabled
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
            if self.wait_element(tmpKEAOptionActive, 1, True) != False and self.wait_element(tmpKEAOptionNormal, 1, True) == False:
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
            writeToLog("INFO", "Please specify in which KEA section we should enable or disable the options")
            return False
        
        sleep(1)
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to click on the " + keaSection.value)
            return False
        sleep(2)
        
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
                    if self.openKEAPreviewScreen() == False:
                        return False
                    
                    if self.verifyQuizWelcomeScreenElements(options, keaOption[options], timeout=90) == False:
                        return False
                    
                    if self.closeKEAPreviewScreen() == False:
                        return False
            
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
        
        sleep(1)
        if self.click(tmpKEASection, 5, True) == False:
            writeToLog("INFO", "Failed to collapse the " + keaSection.value)
            return False
            
        return True