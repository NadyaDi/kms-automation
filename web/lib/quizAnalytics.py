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
    QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE               = ('xpath', '//a[@class="quizMainObject" and contains(text(),"QUESTION_TITLE")]')
    QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED        = ('xpath', '//a[@class="quizMainObject opened" and contains(text(),"QUESTION_TITLE")]')
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
    def addFeedbackToOpenQuestion(self, questionTitle, feedbackText, entryName='', forceNavigate=False, feedbackOwner='', feedbackDate=''):
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False  
        
        # Check is question section is collapsed, if so, click on question title:
        if self.wait_element(self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED) == False:
            tmpQuestionTitle = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE[1].replace('QUESTION_TITLE', questionTitle))    
            if self.click(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on " + questionTitle + " question")
                return False  
        
        if self.click(self.QUIZ_ANALYTICS_ADD_FEEDBACK_LINK) == False:
            writeToLog("INFO","FAILED to click on add feedback button")
            return False 
        
        if self.clear_and_send_keys(self.QUIZ_ANALYTICS_ADD_FEEDBACK_TEXT_FIELD, feedbackText) == False:
            writeToLog("INFO","FAILED to insert feedback to " + questionTitle + " question")
            return False  
        
        if self.click(self.QUIZ_ANALYTICS_ADD_FEEDBACK_BTN) == False:
            writeToLog("INFO","FAILED to click on add button")
            return False         
        
        self.clsCommon.general.waitForLoaderToDisappear()
        
        # Verify that feedback is added correctly
        tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
        if feedbackText not in tmpFeedback.text:
            writeToLog("INFO","FAILED to display feedback correctly")
            return False            
        
        # Verify that correct feedback owner is display for the feedback
        tmpOwner = (self.QUIZ_ANALYTICS_FEEDBACK_OWNER[0], self.QUIZ_ANALYTICS_FEEDBACK_OWNER[1].replace('FEEDBACK_OWNER', feedbackOwner))  
        if self.wait_element(tmpOwner) == False:
            writeToLog("INFO","FAILED to display feedback owner correctly")
            return False
        
        # Verify that correct feedback date is display for the feedback
#         tmpOwner = (self.ENTRY_PAGE_ANALYTICS_FEEDBACK_DATE[0], self.ENTRY_PAGE_ANALYTICS_FEEDBACK_DATE[1].replace('FEEDBACK_DATE', feedbackDate))  
#         if self.wait_element(tmpOwner) == False:
#             writeToLog("INFO","FAILED to display feedback date correctly")
#             return False  

        writeToLog("INFO","Success: feedback was added successfully")
        return True
                         
    
    # @Author: Inbar Willman
    # Edit open question feedback
    def editOpenQuestionFeedback(self, questionTitle, feedbackText, entryName='', forceNavigate=False, feedbackOwner='', feedbackDate=''):
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False  
        
        # Check is question section is collapsed, if so, click on question title:
        if self.wait_element(self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED) == False:
            tmpQuestionTitle = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE[1].replace('QUESTION_TITLE', questionTitle))    
            if self.click(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on " + questionTitle + " question")
                return False  
        
        if self.click(self.QUIZ_ANALYTICS_EDIT_FEEDBACK_BTN) == False:
            writeToLog("INFO","FAILED to click on edit feedback button")
            return False 
        
        if self.clear_and_send_keys(self.QUIZ_ANALYTICS_ADD_FEEDBACK_TEXT_FIELD, feedbackText) == False:
            writeToLog("INFO","FAILED to insert feedback to " + questionTitle + " question")
            return False  
        
        if self.click(self.QUIZ_ANALYTICS_ADD_FEEDBACK_BTN) == False:
            writeToLog("INFO","FAILED to click on update button")
            return False         
        
        self.clsCommon.general.waitForLoaderToDisappear()
        
        # Verify that feedback is edited correctly
        tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
        if feedbackText not in tmpFeedback.text:
            writeToLog("INFO","FAILED to display edited feedback correctly")
            return False             
        
        # Verify that correct feedback owner is display for the feedback
        tmpOwner = (self.QUIZ_ANALYTICS_FEEDBACK_OWNER[0], self.QUIZ_ANALYTICS_FEEDBACK_OWNER[1].replace('FEEDBACK_OWNER', feedbackOwner))  
        if self.wait_element(tmpOwner) == False:
            writeToLog("INFO","FAILED to display feedback owner correctly")
            return False

        writeToLog("INFO","Success: feedback was edited successfully")
        return True     
    
                       
    # @Author: Inbar Willman
    # Delete open question feedback
    def deleteOpenQuestionFeedback(self, questionTitle, feedbackText, entryName='', forceNavigate=False, feedbackOwner='', feedbackDate=''):
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False  
        
        # Check is question section is collapsed, if so, click on question title:
        if self.wait_element(self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED) == False:
            tmpQuestionTitle = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE[1].replace('QUESTION_TITLE', questionTitle))    
            if self.click(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on " + questionTitle + " question")
                return False  
        
        if self.click(self.QUIZ_ANALYTICS_DELETE_FEEDBACK_BTN) == False:
            writeToLog("INFO","FAILED to click on delete feedback button")
            return False        
        
        self.clsCommon.general.waitForLoaderToDisappear()
        
        # Verify that feedback isn't displayed anymore
        tmpFeedback = self.wait_element(self.QUIZ_ANALYTICS_FEEDBACK_TEXT)
        if feedbackText not in tmpFeedback.text:
            writeToLog("INFO","FAILED to display edited feedback correctly")
            return False           
        
        # Verify that add feedback button is displayed
        if self.wait_element(self.QUIZ_ANALYTICS_ADD_FEEDBACK_LINK) == False:
            writeToLog("INFO","FAILED to display add feedback button")
            return False

        writeToLog("INFO","Success: feedback was deleted successfully")
        return True                                               