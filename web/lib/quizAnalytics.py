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
    QUIZ_ANALYTICS_QUIZ_USERS_TAB                    = ('xpath', '//a[@class="userreportsQuizUsers-tab "]')        
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
    QUIZ_ANALYTICS_NUM_OF_RIGHT_AND_WRONG_ANSWERS    = ('xpath', '//div[@class="drill-down-summary-text" and contains(text(),"Answered RIGHT_NUM right and WRONG_NUM wrong")]')
    QUIZ_ANALYTICS_USER_RIGHT_ANSWER                 = ('xpath', '//span[@class="quiz-answerer-user-id" and contains(text(),"USER_ID")]/ancestor::div[@class="drill-down-data-row right"]/descendant::span[@class="quiz-user-answer-text" and contains(text(),"USER_ANSWER")]')
    QUIZ_ANALYTICS_USER_WRONG_ANSWER                 = ('xpath', '//span[@class="quiz-answerer-user-id" and contains(text(),"USER_ID")]/ancestor::div[@class="drill-down-data-row wrong"]/descendant::span[@class="quiz-user-answer-text" and contains(text(),"USER_ANSWER")]')
    QUIZ_ANALYTICS_USER_VIEWED_ANSWER                = ('xpath', '//span[@class="quiz-answerer-user-id" and contains(text(),"USER_ID")]/ancestor::div[@class="drill-down-data-row right"]/descendant::span[@class="quiz-viewed " and contains(text(),"Viewed")]')
    QUIZ_ANALYTICS_REMOVE_ATTEMPTS_ICON              = ('xpath', '//a[@class="removeAttempts" and contains(@href,"user_entry_id=USER_ID")]') 
    QUIZ_ANALYTICS_REMOVE_ATTEMPT_BTN                = ('xpath', '//a[@class="btn btn-danger" and text()="REMOVE_OPTION"]')
    QUIZ_ANALYTICS_USER_ROW                          = ('xpath', '//tr[@id="quizUsersTable__row_USER_NAME"]')
    QUIZ_ANALYTICS_USER_ID                           = ('xpath', '//tr[@id="quizUsersTable__row_USER_NAME"]/descendant::a[contains(@class,"quizMainObject")]')
    QUIZ_ANALYTICS_SCORE_TYPE                        = ('xpath', '//td[@class="span2" and text()="Final Score (SCORE_TYPE)"]')
    QUIZ_ANALYTICS_ATTEMPT_WAS_REMOVED_MSG           = ('xpath', '//i[text()="Attempt was removed"]')
    QUIZ_ANALYTICS_FEEDBACk_DATE                     = ('xpath', '//span[@class="feedback-title__date" and text()="FEEDBACK_DATE"]')
    QUIZ_ANALYTICS_USERS_TAB_RIGHT_ANSWER            = ()
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
            tmpFeedback = (self.QUIZ_ANALYTICS_FEEDBACk_DATE[0], self.QUIZ_ANALYTICS_FEEDBACk_DATE[1].replace('FEEDBACK_DATE', tmpFeedbackDate))  
            if self.wait_element(tmpOwner) == False:
                writeToLog("INFO","FAILED to display feedback date correctly")
                return False  
    
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
        if self.wait_element(tmpQuestionTitleOpened, 3) == False:
            # If question is in closed state
            if self.wait_element(tmpQuestionTitleClosed, 3) != False:
                if self.click(tmpQuestionTitleClosed) == False:
                    writeToLog("INFO","FAILED to click on " + questionTitle + " question")
                    return False  
            # If we are in collapsed state    
            else:
                if self.click(tmpQuestionTitleCollapsed) == False:
                    writeToLog("INFO","FAILED to click on " + questionTitle + " question")
                    return False  
        
        sleep(5)
        writeToLog("INFO","Success: Open-Q title " + questionTitle + " was clicked")       
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
    
    
    # @Author: Inbar Willman
    # Verify that correct open-Q answer is displayed in quiz analytics -> Quiz questions tab
    # Verify that correct number of wrong and correct answers is displayed
    # answersDict - Dictionary that contains List with all answers data
    def verifyQuizAnswersInAnalytics(self, answersList, entryName='', forceNavigate=False): 
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False 
            
        for i in range(0,len(answersList)):
            # Get dictionary with all question users answers
            tmpAnswersDict     = answersList[i]
            
            # Get question title
            tmpAnswersList     = tmpAnswersDict['1']
            tmpQuestionTitle   = tmpAnswersList[0] 
            
            if self.clickOnOpenQuestionTitle(tmpQuestionTitle) == False:
                writeToLog("INFO","FAILED to click on open-Q title")
                return False
                
            # Run over all the users answers
            for i in range(0,len(tmpAnswersDict)):
                tmpAnswersList     = tmpAnswersDict[str(i+1)]
                tmpQuestionTitle   = tmpAnswersList[0]   
                tmpAnswer          = tmpAnswersList[1]  
                tmpUserID          = tmpAnswersList[2]   
                tmpRightAnswers    = tmpAnswersList[3]   
                tmpWrongAnswers    = tmpAnswersList[4] 
                tmpIsRightAnswer   = tmpAnswersList[5] 

                # Verify that correct answer is displayed
                # If answer is correct
                if tmpIsRightAnswer == True:
                    # If it's reflection question
                    if tmpAnswer == 'Viewed':
                        tmpReflectionAnswer = (self.QUIZ_ANALYTICS_USER_VIEWED_ANSWER[0], self.QUIZ_ANALYTICS_USER_VIEWED_ANSWER[1].replace('USER_ID', tmpUserID))
                        if self.wait_element(tmpReflectionAnswer) == False:
                            writeToLog("INFO","FAILED to displayed correct viewed text")
                            return False                        
                    else:    
                        tmpRightUserAnswer = (self.QUIZ_ANALYTICS_USER_RIGHT_ANSWER[0], self.QUIZ_ANALYTICS_USER_RIGHT_ANSWER[1].replace('USER_ID', tmpUserID).replace('USER_ANSWER', tmpAnswer))
                        if self.wait_element(tmpRightUserAnswer) == False:
                            writeToLog("INFO","FAILED to displayed correct right user's answer")
                            return False
                else:
                    tmpWrongUserAnswer = (self.QUIZ_ANALYTICS_USER_WRONG_ANSWER[0], self.QUIZ_ANALYTICS_USER_WRONG_ANSWER[1].replace('USER_ID', tmpUserID).replace('USER_ANSWER', tmpAnswer))
                    if self.wait_element(tmpWrongUserAnswer) == False:
                        writeToLog("INFO","FAILED to displayed correct wrong user's answer")
                        return False                
            
                # Verify that correct number of right and wrong answers is displayed
                tmpAnswersNum = (self.QUIZ_ANALYTICS_NUM_OF_RIGHT_AND_WRONG_ANSWERS[0], self.QUIZ_ANALYTICS_NUM_OF_RIGHT_AND_WRONG_ANSWERS[1].replace('RIGHT_NUM', tmpRightAnswers).replace('WRONG_NUM', tmpWrongAnswers))       
                if self.wait_element(tmpAnswersNum) == False:
                    writeToLog("INFO","FAILED to displayed correct number of wrong and right answers")
                    return False 
            
            # Close question section
            tmpQuestionTitleOpened = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[1].replace('QUESTION_TITLE', tmpQuestionTitle))
            if self.click(tmpQuestionTitleOpened) == False:
                writeToLog("INFO","FAILED to close open-Q section")
                return False   
                           
        writeToLog("INFO","SUCCESS: answered are verified")            
        return True      
    
    
    # @Author: Inbar Willman
    # Delete user attempt (last attempt/ all attempts) from quiz users tab in quiz analytics page
    # userLoginName = user username when making login
    # removeOption = enums.quizAnlyticsDeleteOption
    # entryName - Is given if forcing navigating to quiz analytics page
    def deleteUserAttempts(self, userLoginName, removeOption, entryName='',forceNavigate=False):
        # If we aren't in analytics page - quiz users tab
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate, enums.quizAnalytics.QUIZ_USERS) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz users page")
                return False 
            
        userId = self.getUserId(userLoginName) 
        if userId == False:
            writeToLog("INFO","FAILED to get userId")         
            return False 
        
        tmpDeleteIcon = (self.QUIZ_ANALYTICS_REMOVE_ATTEMPTS_ICON[0], self.QUIZ_ANALYTICS_REMOVE_ATTEMPTS_ICON[1].replace('USER_ID', userId))     
         
        if self.click(tmpDeleteIcon) == False:
            writeToLog("INFO","FAILED to click on delete icon for " + userLoginName)
            return False 
  
        tmpRemoveAttemptBtn = (self.QUIZ_ANALYTICS_REMOVE_ATTEMPT_BTN[0], self.QUIZ_ANALYTICS_REMOVE_ATTEMPT_BTN[1].replace('REMOVE_OPTION', removeOption.value))   
        if self.click(tmpRemoveAttemptBtn) == False:
            writeToLog("INFO","FAILED to click on delete " + removeOption.value + " option")
            return False 
        
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(5)
        writeToLog("INFO","Success: attempt/s was removed")
        return True                    
              
    
    # @Author: Inbar Willman
    # This function return the user row in users table
    # return false if can't find userId
    def getUserId(self, userLoginName): 
        userId = -1
        tmpUserId = (self.QUIZ_ANALYTICS_USER_ID[0], self.QUIZ_ANALYTICS_USER_ID[1].replace('USER_NAME', userLoginName))    
        tmpUserIdElement = self.wait_element(tmpUserId)
        
        if tmpUserIdElement == False:
            writeToLog("INFO","FAILED to find user name element")
            return False                        
        
        userId = tmpUserIdElement.get_attribute("id").split("_")[1]
        if userId == -1:
            writeToLog("INFO","FAILED to find user id")
            return False  
                     
        return userId
    
    
    # @Author: Inbar Willman
    # Verify that correct number of attempts, score and score type are displayed
    # userLoginName = user username when making login
    # numberOfAttempts = string from the next format 'x/y' (1/2, 1/1)
    # score = string from the next format 100%, 90%
    # scoreType= enums.playerQuizScoreType
    # entryName - Is given if forcing navigating to quiz analytics page
    def verifyUserAttemptsAndScore(self, userLoginName, userName, numberOfAttempts, score, scoreType, entryName='', forceNavigate=False):
        # If we aren't in analytics page - quiz users tab
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate, enums.quizAnalytics.QUIZ_USERS) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz users page")
                return False
    
        tmpUserRow = (self.QUIZ_ANALYTICS_USER_ROW[0], self.QUIZ_ANALYTICS_USER_ROW[1].replace('USER_NAME', userLoginName))
        tmpUserRowElement = self.wait_element(tmpUserRow)
        if tmpUserRowElement == False:
                writeToLog("INFO","FAILED to find user row element")
                return False
                        
        tmpUserRowText = tmpUserRowElement.text
        tmpGivenUserRowText = userName + "\n" + numberOfAttempts + " " + score
        
        if tmpGivenUserRowText != tmpUserRowText:
            writeToLog("INFO","FAILED to display correct user data")
            return False 
            
        tmpScoreType = (self.QUIZ_ANALYTICS_SCORE_TYPE[0], self.QUIZ_ANALYTICS_SCORE_TYPE[1].replace('SCORE_TYPE', scoreType.value))
        if self.wait_element(tmpScoreType) == False:
            writeToLog("INFO","FAILED to display correct score type")
            return False             
    
        writeToLog("INFO","Success: attempts and score are verified")
        return True
    
    
    # @Author: Inbar Willman
    # Verify message after removing all attempts or last attempts in case we have just one attempt
    def verifyRemovedAttemptMessage(self):
        if self.wait_element(self.QUIZ_ANALYTICS_ATTEMPT_WAS_REMOVED_MSG) == False:
            writeToLog("INFO","FAILED to displayed 'Attempt Was removed' message")
            return False  
        
        writeToLog("INFO","Success:'Attempt Was removed' message is displayed")
        return True 
    
    
    # @Author: Inbar Willman
    # Verify that correct number of attempts, score and score type are displayed for all users
    # allUsersDataDict = Dictionary that contains list with all user data (userId, username, number of attempts and score)
    # score = string from the next format 100%, 90%
    # scoreType= enums.playerQuizScoreType
    # entryName - Is given if forcing navigating to quiz analytics page
    def verifyAllUsersAttemptsAndScore(self, allUsersDataDict, scoreType, entryName='', forceNavigate=False):
        # If we aren't in analytics page - quiz users tab
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate, enums.quizAnalytics.QUIZ_USERS) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz users page")
                return False       
            
        for i in range(0, len(allUsersDataDict)):
            userDataList            = allUsersDataDict[str(i+1)]
            userLoginName           = userDataList[0]
            userName                = userDataList[1]
            userNumberOfAttempts    = userDataList[2]
            userScore               = userDataList[3]
    
            if self.verifyUserAttemptsAndScore(userLoginName, userName, userNumberOfAttempts, userScore, scoreType, '', False) == False:
                writeToLog("INFO","FAILED to verify attempts and score for all users")
                return False                    
    
        writeToLog("INFO","Success: attempts and score are verified for all users")
        return True   
    
    
    # @Author: Inbar Willman - To Do
    # Verify that correct user answer is displayed for each question in quiz users tab for user last attempt
    # Verify that correct number of wrong and correct answers is displayed for user last attempt
    # questionAndAnswerDict - Dictionary that call list with question title and question answer:
    # Dict format - {'1': firstQuestion}, firstQuestion = [firstQuestionTitle, firstQuestionAnswer, isCorrectAnswer=boolean]
    # numberOfRightAnswers / numberOfRightAnswers = string. The number of right/wrong users answers for last attempts
    def verifyQuizAnswersInQuizUsersAnalytics(self, quetionAndAnswerDict, userName, numberOfRightAnswers='', numberOfWrongAnswers='', entryName='', forceNavigate=False): 
        # If we aren't in analytics page
        if self.wait_element(self.QUIZ_ANALYTICS_PAGE_TITLE, 3) == False:
            if self.clsCommon.entryPage.navigateToQuizAnalyticsPage(entryName, forceNavigate, enums.quizAnalytics.QUIZ_USERS) == False:
                writeToLog("INFO","FAILED to navigate to quiz analytics - quiz question page")
                return False 
            
        for i in range(0,len(quetionAndAnswerDict)):
            # Get dictionary with all question users answers
            questionList     = quetionAndAnswerDict[str(i+1)]
            questionTitle    = questionList[0]
            questionAnswer   = questionList[1] 
            isRightAnswer    = questionList[2] 
            
            
            tmpUserNameBtn = (self.QUIZ_ANALYTICS_USER_ID[0], self.QUIZ_ANALYTICS_USER_ID[1].replace('USER_NAME', userName))
            if self.click(tmpUserNameBtn) == False:
                writeToLog("INFO","FAILED to click on userName button in order to open questions and answers section")
                return False 
            
            # If answer is right
            if isRightAnswer == True:
      
            
#             if self.clickOnOpenQuestionTitle(tmpQuestionTitle) == False:
#                 writeToLog("INFO","FAILED to click on open-Q title")
#                 return False
#                 
#             # Run over all the users answers
#             for i in range(0,len(tmpAnswersDict)):
#                 tmpAnswersList     = tmpAnswersDict[str(i+1)]
#                 tmpQuestionTitle   = tmpAnswersList[0]   
#                 tmpAnswer          = tmpAnswersList[1]  
#                 tmpUserID          = tmpAnswersList[2]   
#                 tmpRightAnswers    = tmpAnswersList[3]   
#                 tmpWrongAnswers    = tmpAnswersList[4] 
#                 tmpIsRightAnswer   = tmpAnswersList[5] 
# 
#                 # Verify that correct answer is displayed
#                 # If answer is correct
#                 if tmpIsRightAnswer == True:
#                     # If it's reflection question
#                     if tmpAnswer == 'Viewed':
#                         tmpReflectionAnswer = (self.QUIZ_ANALYTICS_USER_VIEWED_ANSWER[0], self.QUIZ_ANALYTICS_USER_VIEWED_ANSWER[1].replace('USER_ID', tmpUserID))
#                         if self.wait_element(tmpReflectionAnswer) == False:
#                             writeToLog("INFO","FAILED to displayed correct viewed text")
#                             return False                        
#                     else:    
#                         tmpRightUserAnswer = (self.QUIZ_ANALYTICS_USER_RIGHT_ANSWER[0], self.QUIZ_ANALYTICS_USER_RIGHT_ANSWER[1].replace('USER_ID', tmpUserID).replace('USER_ANSWER', tmpAnswer))
#                         if self.wait_element(tmpRightUserAnswer) == False:
#                             writeToLog("INFO","FAILED to displayed correct right user's answer")
#                             return False
#                 else:
#                     tmpWrongUserAnswer = (self.QUIZ_ANALYTICS_USER_WRONG_ANSWER[0], self.QUIZ_ANALYTICS_USER_WRONG_ANSWER[1].replace('USER_ID', tmpUserID).replace('USER_ANSWER', tmpAnswer))
#                     if self.wait_element(tmpWrongUserAnswer) == False:
#                         writeToLog("INFO","FAILED to displayed correct wrong user's answer")
#                         return False                
#             
                # Verify that correct number of right and wrong answers is displayed
                tmpAnswersNum = (self.QUIZ_ANALYTICS_NUM_OF_RIGHT_AND_WRONG_ANSWERS[0], self.QUIZ_ANALYTICS_NUM_OF_RIGHT_AND_WRONG_ANSWERS[1].replace('RIGHT_NUM', numberOfRightAnswers).replace('WRONG_NUM', numberOfWrongAnswers))       
                if self.wait_element(tmpAnswersNum) == False:
                    writeToLog("INFO","FAILED to displayed correct number of wrong and right answers")
                    return False 
#             
#             # Close question section
#             tmpQuestionTitleOpened = (self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[0], self.QUIZ_ANALYTICS_QUIZ_QUESTION_TITLE_OPENED[1].replace('QUESTION_TITLE', tmpQuestionTitle))
#             if self.click(tmpQuestionTitleOpened) == False:
#                 writeToLog("INFO","FAILED to close open-Q section")
#                 return False   
                           
        writeToLog("INFO","SUCCESS: answered are verified")            
        return True      