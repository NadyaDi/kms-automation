import subprocess
try:
    import win32com.client
except:
    pass
import enums
from base import *
import clsTestService
from general import General


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
    KEA_APP_DISPLAY                               = ('id', 'kea-anchor')
    KEA_IFRAME                                    = ('xpath', '//iframe[@class="span12 hostedEnabled kea-frame"]')
    KEA_QUIZ_PLAYER                               = ('id', 'quiz-player_ifp')
    KEA_LOADING_SPINNER                           = ('class_name', 'spinner')
    KEA_QUIZ_QUESTION_FIELD                       = ('id', 'questionTxt')
    KEA_QUIZ_ANSWER                               = ('id', 'ANSWER_NUMBER')
    KEA_QUIZ_ADD_ANSWER_BUTTON                    = ('xpath', '//div[@class="add-answer-btn"]') 
    KEA_QUIZ_BUTTON                               = ('xpath', '//span[@class="ui-button-text ui-clickable" and text()="BUTTON_NAME"]')
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
        self.clsCommon.myMedia.getSearchBarElement().send_keys(entryName)
        self.clsCommon.general.waitForLoaderToDisappear()
        
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
        if self.startQuiz() == False:
            writeToLog("INFO","FAILED to click start quiz")
            return False 
                    
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
        tmpButton = (self.KEA_QUIZ_BUTTON[0], self.KEA_QUIZ_BUTTON[1].replace('BUTTON_NAME', str(buttonName)))
        if self.click(tmpButton) == False:
            writeToLog("INFO","FAILED to click on " + buttonName + " button")
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