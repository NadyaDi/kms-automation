from base import *
import clsTestService
import enums
from logger import writeToLog
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


class QuizAnalytics(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Analytics locators:
    #=============================================================================================================
    QUIZ_ANALYTICS_QUIZ_QUESTIONS_TAB                = ('xpath', '//a[@class="userreportsQuizQuestions-tab "]')
    QUIZ_ANALYTICS_QUIZ_USERS_TAB                    = ('xpath', '//a[@class="userreportsQuizUsers-tab"]')        
    QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_CLOSED        = ('xpath', '//a[@class="quizMainObject" and contains(text(),"QUESTION_TITLE")]')
    QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED        = ('xpath', '//a[@class="quizMainObject opened" and contains(text(),"QUESTION_TITLE")]')
    QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_COLLAPSED     = ('xpath', '//a[@class="quizMainObject collapsed" and contains(text(),"QUESTION_TITLE")]')
    QUIZ_ANALYTICS_ADD_FEEDBACK_LINK                 = ('xpath', '//button[contains(@class,"button--transparent btn-link feedback-add")]')
    QUIZ_ANALYTICS_ADD_FEEDBACK_BTN                  = ('xpath', '//button[@class="btn btn-primary feedback-submit"]') 
    QUIZ_ANALYTICS_CANCEL_FEEDBACK_BTN               = ('xpath', '//button[contains(@class,"button--transparent feedback-cancel")]')
    QUIZ_ANALYTICS_EDIT_FEEDBACK_BTN                 = ('xpath', '//button[contains(@class,"button--transparent btn-link feedback-edit")]')
    QUIZ_ANALYTICS_DELETE_FEEDBACK_BTN               = ('xpath', '//button[contains(@class,"button--transparent feedback-delete")]')
    QUIZ_ANALYTICS_UPDATE_FEEDBACK_BTN               = ('xpath', '//button[contains(@class,"button--transparent feedback-delete")]')
    QUIZ_ANALYTICS_ADD_FEEDBACK_TEXT_FIELD           = ('xpath', '//textarea[@class="noresize feedback-text-input"]')
    QUIZ_ANALYTICS_FEEDBACK_OWNER                    = ('xpath', '//span[@class="feedback-title__writer" and text()="FEEDBACK_OWNER"]')
    QUIZ_ANALYTICS_FEEDBACK_DATE                     = ('xpath', '//span[@class="feedback-title__date" and text()="FEEDBACK_DATE"]')
    QUIZ_ANALYTICS_FEEDBACK_TEXT                     = ('xpath', '//div[contains(@class,"feedback-text feedback-text")]')
    QUIZ_ANALYTICS_PAGE_TITLE                        = ('xpath', '//h1[text()="Analytics for media "]')
    #=============================================================================================================
    # @Author: Inbar Willman
    # Add feedback to open-Q
    # feedbackToAddDic = Dictionary of all the questions that we add feedback to. The dictionary calls list with 
    # The question Title and the feedback
    def addFeedbackToOpenQuestion(self, feedbackToAddDic, entryName='', forceNavigate=False):
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False  
        
        for i in range(0,len(feedbackToAddDic)):
            tmpQuestionFeedbackList = feedbackToAddDic[str(i+1)]
            tmpQuestionTitle = tmpQuestionFeedbackList[0]
            tmpQuestionFeedback = tmpQuestionFeedbackList[1]
            tmpFeedbackOwner = tmpQuestionFeedbackList[2]
            tmpFeedbackDate = tmpQuestionFeedbackList[3]
            
            if self.clickOnOpenQuestionTitle(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on open-Q title")
                return False              
        
            if self.click(self.QUIZ_ANALYTICS_ADD_FEEDBACK_LINK) == False:
                writeToLog("INFO","FAILED to click on add feedback button")
                return False 
        
            if self.clear_and_send_keys(self.QUIZ_ANALYTICS_ADD_FEEDBACK_TEXT_FIELD, tmpQuestionFeedback) == False:
                writeToLog("INFO","FAILED to insert feedback to " + tmpQuestionTitle + " question")
                return False  
        
            if self.click(self.QUIZ_ANALYTICS_ADD_FEEDBACK_BTN) == False:
                writeToLog("INFO","FAILED to click on add button")
                return False         
        
            self.clsCommon.general.waitForLoaderToDisappear()
        
            # Verify that feedback is added correctly
            tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
            if tmpQuestionFeedback not in tmpFeedback.text:
                writeToLog("INFO","FAILED to display feedback correctly")
                return False            
        
            # Verify that correct feedback owner is display for the feedback
            tmpOwner = (self.QUIZ_ANALYTICS_FEEDBACK_OWNER[0], self.QUIZ_ANALYTICS_FEEDBACK_OWNER[1].replace('FEEDBACK_OWNER', tmpFeedbackOwner))  
            if self.wait_element(tmpOwner) == False:
                writeToLog("INFO","FAILED to display feedback owner correctly")
                return False
        
            # Verify that correct feedback date is display for the feedback
#             tmpOwner = (self.ENTRY_PAGE_ANALYTICS_FEEDBACK_DATE[0], self.ENTRY_PAGE_ANALYTICS_FEEDBACK_DATE[1].replace('FEEDBACK_DATE', tmpFeedbackDate))  
#             if self.wait_element(tmpOwner) == False:
#                 writeToLog("INFO","FAILED to display feedback date correctly")
#                 return False  
    
            # Going to close open-Q section
            tmpQuestionTitleOpened = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[1].replace('QUESTION_TITLE', tmpQuestionTitle))
            if self.click(tmpQuestionTitleOpened) == False:
                writeToLog("INFO","FAILED to close open-Q section")
                return False            

        writeToLog("INFO","Success: feedback was added successfully")
        return True
                         
    
    # @Author: Inbar Willman
    # Edit open question feedback
    def editOpenQuestionFeedback(self, feedbackToEditDic, entryName='', forceNavigate=False):
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False 
            
        for i in range(0,len(feedbackToEditDic)):
            tmpQuestionFeedbackList = feedbackToEditDic[str(i+1)]
            tmpQuestionTitle = tmpQuestionFeedbackList[0]
            tmpQuestionCurrentFeedback = tmpQuestionFeedbackList[1]
            tmpQuestionNewFeedback = tmpQuestionFeedbackList[2]
            tmpFeedbackOwner = tmpQuestionFeedbackList[3]
            tmpFeedbackDate = tmpQuestionFeedbackList[4]             
        
            if self.clickOnOpenQuestionTitle(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on open-Q title")
                return False
        
            # Verify that the current feedback is displayed before editing it
            tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
            if tmpQuestionCurrentFeedback not in tmpFeedback.text:
                writeToLog("INFO","FAILED to display current feedback correctly")
                return False 
            
            if self.click(self.QUIZ_ANALYTICS_EDIT_FEEDBACK_BTN) == False:
                writeToLog("INFO","FAILED to click on edit feedback button")
                return False 
        
            if self.clear_and_send_keys(self.QUIZ_ANALYTICS_ADD_FEEDBACK_TEXT_FIELD, tmpQuestionNewFeedback) == False:
                writeToLog("INFO","FAILED to insert feedback to " + tmpQuestionTitle + " question")
                return False  
        
            if self.click(self.QUIZ_ANALYTICS_ADD_FEEDBACK_BTN) == False:
                writeToLog("INFO","FAILED to click on update button")
                return False         
        
            self.clsCommon.general.waitForLoaderToDisappear()
        
            # Verify that feedback is edited correctly
            tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
            if tmpQuestionNewFeedback not in tmpFeedback.text:
                writeToLog("INFO","FAILED to display edited feedback correctly")
                return False             
        
            # Verify that correct feedback owner is display for the feedback
            tmpOwner = (self.QUIZ_ANALYTICS_FEEDBACK_OWNER[0], self.QUIZ_ANALYTICS_FEEDBACK_OWNER[1].replace('FEEDBACK_OWNER', tmpFeedbackOwner))  
            if self.wait_element(tmpOwner) == False:
                writeToLog("INFO","FAILED to display feedback owner correctly")
                return False

            # Going to close open-Q section
            tmpQuestionTitleOpened = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[1].replace('QUESTION_TITLE', tmpQuestionTitle))
            if self.click(tmpQuestionTitleOpened) == False:
                writeToLog("INFO","FAILED to close open-Q section")
                return False  

        writeToLog("INFO","Success: feedback was edited successfully")
        return True     
    
                       
    # @Author: Inbar Willman
    # Delete open question feedback
    def deleteOpenQuestionFeedback(self, feedbackToDeleteDic='', entryName='', forceNavigate=False):
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False  
            
        for i in range(0,len(feedbackToDeleteDic)):
            tmpQuestionFeedbackList = feedbackToDeleteDic[str(i+1)]
            tmpQuestionTitle = tmpQuestionFeedbackList[0]
            tmpQuestionCurrentFeedback = tmpQuestionFeedbackList[1]                 
        
            if self.clickOnOpenQuestionTitle(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on open-Q title")
                return False
        
            if self.click(self.QUIZ_ANALYTICS_DELETE_FEEDBACK_BTN) == False:
                writeToLog("INFO","FAILED to click on delete feedback button")
                return False        
        
            self.clsCommon.general.waitForLoaderToDisappear()
        
            # Verify that feedback isn't displayed anymore
            tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
            if tmpFeedback != False:
                if tmpQuestionCurrentFeedback in tmpFeedback.text:
                    writeToLog("INFO","FAILED: deleted feedback is still displayed")
                    return False           
  
                # Verify that add feedback button is displayed
                if self.wait_element(self.QUIZ_ANALYTICS_ADD_FEEDBACK_LINK) == False:
                    writeToLog("INFO","FAILED to display add feedback button")
                    return False
        
                # Going to close open-Q section
                tmpQuestionTitleOpened = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[1].replace('QUESTION_TITLE', tmpQuestionTitle))
                if self.click(tmpQuestionTitleOpened) == False:
                    writeToLog("INFO","FAILED to close open-Q section")
                    return False          

        writeToLog("INFO","Success: feedback was deleted successfully")
        return True   
    
    
    # @Author: Inbar Willman
    # The function Click on open question in 3 states:
    # Closed - the question section wasn't opened yet
    # Opened - the quesrtion section is open
    # Collapsed - the question section opened already and then closed
    def clickOnOpenQuestionTitle(self, questionTitle): 
        # Question title before we clicked on it    
        tmpQuestionTitleClosed = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_CLOSED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_CLOSED[1].replace('QUESTION_TITLE', questionTitle))
        
        # Question title in opened state
        tmpQuestionTitleOpened = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[1].replace('QUESTION_TITLE', questionTitle))
        
        # Question title in collapsed state
        tmpQuestionTitleCollapsed = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_COLLAPSED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_COLLAPSED[1].replace('QUESTION_TITLE', questionTitle))

        # Check is question section open state, if so, click on question title:
        if self.wait_element(tmpQuestionTitleOpened, 5) == False:
            # If question is in closed state
            if self.wait_element(tmpQuestionTitleClosed, 5) != False:
                if self.click(tmpQuestionTitleClosed) == False:
                    writeToLog("INFO","FAILED to click on " + questionTitle + " question")
                    return False  
            # If we are in collapsed state    
            else:
                if self.click(tmpQuestionTitleCollapsed) == False:
                    writeToLog("INFO","FAILED to click on " + questionTitle + " question")
                    return False  
        
        sleep(5)
        writeToLog("INFO","Success: Open-Q title " + questionTitle + "was clicked")       
        return True      
    
    
    # @Author: Inbar Willman
    # Verify that user is able to see feedback that was edited by other user
    def verifyOpenQuestionFeedbackAfterEditOrDeletion(self, questionFeedbackList, entryName='', forceNavigate=False):
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False  
        
        for i in range(len(questionFeedbackList)):
            tmpFeedbackList = questionFeedbackList[str(i+1)]
            tmpQuestionTitle = tmpFeedbackList[0]   
            tmpOriginalFeedback = tmpFeedbackList[1]
            
            # If feedback list is bigger than 2 we verify edited feedback
            if len(tmpFeedbackList) > 2:
                tmpEditedFeedback = tmpFeedbackList[2]
                tmpFeedbackOwner = tmpFeedbackList[3]
            
            if self.clickOnOpenQuestionTitle(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on open-Q title")
                return False
        
            # Get feedback text section
            tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
        
            # If we want to verify deletion
            if len(tmpFeedbackList) == 2:
                if tmpFeedback != False:
                    if tmpOriginalFeedback in tmpFeedback.text:
                        writeToLog("INFO","FAILED: deleted feedback is still displayed")
                        return False
        
            # If we want to verify edited feedback
            else:
                # Verify that the edited feedback is displayed 
                if tmpEditedFeedback not in tmpFeedback.text:
                    writeToLog("INFO","FAILED to display edited feedback correctly")
                    return False
        
                # Verify that correct feedback owner is display for the feedback
                tmpOwner = (self.QUIZ_ANALYTICS_FEEDBACK_OWNER[0], self.QUIZ_ANALYTICS_FEEDBACK_OWNER[1].replace('FEEDBACK_OWNER', tmpFeedbackOwner))  
                if self.wait_element(tmpOwner) == False:
                    writeToLog("INFO","FAILED to display feedback owner correctly")
                    return False
            
            # Going to close open-Q section
            tmpQuestionTitleOpened = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[1].replace('QUESTION_TITLE', tmpQuestionTitle))
            if self.click(tmpQuestionTitleOpened) == False:
                writeToLog("INFO","FAILED to close open-Q section")
                return False              
        
        writeToLog("INFO","Success: Open-Q edited feedback is displayed correctly")       
        return True                                               