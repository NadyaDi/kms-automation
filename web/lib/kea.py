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
    KEA_ADD_NEW_QUESTION_BUTTON                   = ('xpath', "//button[@class='question-type-button question-types-icon multiple-options-question-type active ng-star-inserted']")  
    KEA_SELECT_VIDEO_FOR_EDIT                     = ('xpath', '//a[@class="btn btn-small btn-primary btn-select-media"]')
    KEA_LAUNCH                                    = ('xpath', "//i[@class='icon-editor']")
    KEA_APP_DISPLAY                               = ('id', 'kea-anchor')
    KEA_IFRAME                                    = ('xpath', '//iframe[@class="span12 hostedEnabled kea-frame kea-iframe-js"]')
    KEA_QUIZ_PLAYER                               = ('id', 'quiz-player_ifp')
    KEA_LOADING_SPINNER                           = ('class_name', 'spinner')
    KEA_QUIZ_QUESTION_FIELD                       = ('id', 'questionTxt')
    KEA_QUIZ_ANSWER                               = ('id', 'ANSWER_NUMBER')
    KEA_QUIZ_ADD_ANSWER_BUTTON                    = ('xpath', '//div[@class="add-answer-btn"]') 
    KEA_QUIZ_BUTTON                               = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="BUTTON_NAME"]')
    EDITOR_TABLE                                  = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]')
    EDITOR_TABLE_SIZE                             = ('xpath', '//table[@class="table table-condensed table-hover mymediaTable mediaTable full"]/tbody/tr')
    EDITOR_NO_MORE_MEDIA_FOUND_MSG                = ('xpath', '//div[@id="quizMyMedia_scroller_alert" and text()="There are no more media items."]')
    EDITOR_TIMELINE                               = ('xpath', '//div[@class="kea-timeline-playhead" and @style="transform: translateX(PIXELpx);"]')
    EDITOR_TIME_PICKER                            = ('id', 'jump-to__input')
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
        if self.click(self.KEA_ADD_NEW_QUESTION_BUTTON) == False:
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
        
        if self.wait_while_not_visible(self.KEA_LOADING_SPINNER, 30) == False:
            writeToLog("INFO","FAILED to wait until spinner isn't visible")
            return False  
        
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
    def verifyFiltersInEditor(self, entriesDict):    
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
    
    
    # TODO NOT FINISHED 
    # @Author: Tzachi guetta    
    def trimEntry(self, entryName, startTime, endTime, navigateTo, navigateFrom):
        if self.launchKEA(entryName, navigateTo, navigateFrom) == False:
            writeToLog("INFO","Failed to launch KEA for: " + entryName)
            return False
        
        self.switchToKeaIframe()
        
        if self.clear_and_send_keys(self.EDITOR_TIME_PICKER, startTime + Keys.ENTER) == False:
            writeToLog("INFO","FAILED to insert start time into editor input field")
            return False
        
        
        writeToLog("INFO","Success, KEA has been launched for: " + entryName) 
        return True
    