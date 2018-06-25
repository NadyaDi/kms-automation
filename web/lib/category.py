from base import *
import clsTestService
from general import General
from logger import writeToLog


class Category(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Category locators:
    #=============================================================================================================
    CATEGORY_NAME_NAV_BAR                                       = ('xpath', "//a[@role='button' and contains(text(), 'CATEGORY_NAME')]")# When using this locator, replace 'CATEGORY_NAME' string with your real category name
    CATEGORY_TITLE_IN_CATEGORY_PAGE                             = ('xpath', "//span[@id='gallery_title' and contains(text(), 'CATEGORY_NAME')]")# When using this locator, replace 'CATEGORY_NAME' string with your real category name
    CATEGORY_SEARCH_MAGNAFINE_GLASS                             = ('id', 'gallerySearch-tab')
    CATEGORY_SEARCH_RESULT                                      = ('class_name', 'entryTitle')
    CATEGORY_ENTRY_SEARCH_RESULT                                = ('xpath', "//div[@class='photo-group thumb_wrapper' and @title='ENTRY_NAME']")# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    CATEGORY_3_DOTS_ON_ENTRY_THUMBNAIL                          = ("//a[@href='javascript:;' and contains(text(),'...')]")
    CATEGORY_ADD_NEW_BUTTON                                     = ('xpath', "//a[@id='add-new-tab']")
    CATEGORY_ADD_NEW_MEDIA_UPLOAD_BUTTON                        = ('xpath', "//a[@class='MediaUpload-tab']")
    CATEGORY_PENDING_TAB                                        = ('xpath', "//a[@id='categorymoderation-tab']")
    CATEGORY_ENTRY_THUMBNAIL                                    = ('xpath', "//div[@class='photo-group thumb_wrapper' and @title='ENTRY NAME']")
    CATEGORY_NUMBER_OF_VIEWS_FOR_ENTRY                          = ('xpath', "//span[@class='screenreader-only' and contains(text(), 'NUMBER likes')]")
    CATEGORY_NUMBER_OF_LIKES_FOR_ENTRY                          = ('xpath', "//span[@class='screenreader-only' and contains(text(), 'NUMBER views')]")
    CATEGORY_NUMBER_OF_COMMENTS_FOR_ENTRY                       = ('xpath', "//a[contains(@aria-label, 'NUMBER comment(s)')]")
    CATEGORY_PLUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL                = ('xpath', "//i[@class='icon-plus-sign']")
    CATEGORY_MINUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL               = ('xpath', "//i[@class='icon-minus-sign']")
    CATEGORY_BROWSE_CHANNELS_BUTTON                             = ('xpath', "//a[@id='channelcategories-tab']")
    CATEGORY_ACTION_BUTTON                                      = ('xpath', "//button[@id='galleryActionsDropdownButton']")
    CATEGORY_EDIT_BUTTON                                        = ('xpath', "//i[@class='icon-wrench']")
    #=============================================================================================================
    def clickOnEntryAfterSearchInCategory(self, entryName):
        tmpEntrySearchName = (self.CATEGORY_ENTRY_SEARCH_RESULT[0], self.CATEGORY_ENTRY_SEARCH_RESULT[1].replace('ENTRY_NAME', entryName))
        try:
            self.get_elements(tmpEntrySearchName)[2].click()
            sleep(3)
            return True
        except:
            return False
        
    def navigateToCategory(self, categoryName):
        # Check if we are already in category page
        tmpCategoryName = (self.CATEGORY_TITLE_IN_CATEGORY_PAGE[0], self.CATEGORY_TITLE_IN_CATEGORY_PAGE[1].replace('CATEGORY_NAME', categoryName))
        if self.wait_visible(tmpCategoryName, 5) != False:
            writeToLog("INFO","Success Already in my category page")
            return True
        
        # Click on the category name in the nav bar
        tmpNavCategoryName = (self.CATEGORY_NAME_NAV_BAR[0], self.CATEGORY_NAME_NAV_BAR[1].replace('CATEGORY_NAME', categoryName))
        if self.click(tmpNavCategoryName, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on category name '" + categoryName + "' in the nav bar")
            return False
        
        # Verify category page open
        if self.wait_visible(tmpCategoryName, 30) == False:
            writeToLog("INFO","FAILED to verify category page is display")
            return False
        
        return True
    
    
    def searchEntryInCategory(self, entryName): 
        # Click on the magnafine glass
        if self.click(self.CATEGORY_SEARCH_MAGNAFINE_GLASS, 30) == False:
            writeToLog("INFO","FAILED to click on magnafine glass in category page")
            return False
        sleep(2)
        # Search Entry     
        self.clsCommon.myMedia.getSearchBarElement().click()
        self.clsCommon.myMedia.getSearchBarElement().send_keys(entryName)
        sleep(2)
        self.clsCommon.general.waitForLoaderToDisappear()

        # Verify that the entry was found  
        tmpEntrySearchName = (self.CATEGORY_ENTRY_SEARCH_RESULT[0], self.CATEGORY_ENTRY_SEARCH_RESULT[1].replace('ENTRY_NAME', entryName))
        if self.get_element(tmpEntrySearchName) == None:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' in search result")
            return False
        
        writeToLog("INFO","Success entry '" + entryName + "' was found")
        return True
        
    
    # Author: Michal Zomper 
    def navigateToEditEntryPageFromCategoryPage(self, entryName, categoryName):
        if self.clsCommon.entryPage.navigateToEntryPageFromCategoryPage(entryName, categoryName) == False:
            writeToLog("INFO","FAILED navigate to category")
            return False
        
        if self.clsCommon.editEntryPage.navigateToEditEntryPageFromEntryPage(entryName) == False:
            writeToLog("INFO","FAILED navigate to edit entry page")
            return False
        
        writeToLog("INFO","Success, edit  entry '" + entryName + "' is display")
        return True


    # Author: Tzachi Guetta
    def addNewContentToCategory(self, categoryName, uploadEntrieList):
        try:
            self.clsCommon.navigateTo(enums.Location.CATEGORY_PAGE, nameValue=categoryName)
            
            if self.click(self.clsCommon.channel.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
                writeToLog("INFO","FAILED to click add to channel button")
                return False     
            
            sleep(1)
            self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30)
            
            if self.click(self.CATEGORY_ADD_NEW_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Add New at category page")
                return False
            
            if self.click(self.CATEGORY_ADD_NEW_MEDIA_UPLOAD_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Add New -> Media upload, at category page")
                return False
            
            if self.clsCommon.upload.uploadMulitple(uploadEntrieList, uploadFrom=enums.Location.CATEGORY_PAGE) == False:
                writeToLog("INFO","FAILED to upload media from category page")
                return False
            
        except NoSuchElementException:
            return False
        
        return True
    
    # Author: Michal Zomper 
    def verifyEntryDetails(self, entryName, numberOfLiks, numberOfViews, numberOfComments):
        tmp_entryName = (self.CATEGORY_ENTRY_THUMBNAIL[0], self.CATEGORY_ENTRY_THUMBNAIL[1].replace('ENTRY NAME', entryName))
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.hover_on_element(tmp_entryName) == False:
                writeToLog("INFO","FAILED to hover entry in order to see the entry details")
                return False
        
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            try:
                parent_entry = self.get_element(tmp_entryName)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to get entry '" + entryName + "' element")
                return False
             
            if self.click_child(parent_entry, self.CATEGORY_PLUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL, timeout=20, multipleElements=False) == False:
                writeToLog("INFO","FAILED to click on the plus button in order to see entry details")
                return False
        
        tmp_views = (self.CATEGORY_NUMBER_OF_VIEWS_FOR_ENTRY[0], self.CATEGORY_NUMBER_OF_VIEWS_FOR_ENTRY[1].replace('NUMBER', numberOfViews))
        tmp_likes = (self.CATEGORY_NUMBER_OF_LIKES_FOR_ENTRY[0], self.CATEGORY_NUMBER_OF_LIKES_FOR_ENTRY[1].replace('NUMBER', numberOfLiks))
        tmp_comments = (self.CATEGORY_NUMBER_OF_COMMENTS_FOR_ENTRY[0], self.CATEGORY_NUMBER_OF_COMMENTS_FOR_ENTRY[1].replace('NUMBER', numberOfComments))
        
        if self.is_visible(tmp_views, multipleElements=True) == False:
            writeToLog("INFO","FAILED to verify that the entry have " + numberOfViews + " views")
            return False
            
        if self.is_visible(tmp_likes, multipleElements=True) == False:
            writeToLog("INFO","FAILED to verify that the entry have " + numberOfLiks + " likes")
            return False
        
        
        if self.is_visible(tmp_comments) == False:
            writeToLog("INFO","FAILED to verify that the entry have " + numberOfComments + " comments")
            return False
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if self.click_child(parent_entry, self.CATEGORY_MINUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL, timeout=20, multipleElements=False) == False:
                writeToLog("INFO","FAILED to click on the minus button in order to close entry details")
                return False
            
        writeToLog("INFO","Success, all entry details was verified successfully")
        return True
    
    
    # Author: Michal Zomper 
    def navigateToEditCategoryPage(self, categoryName):
        if self.navigateToCategory(categoryName) == False:
            writeToLog("INFO","FAILED navigate to category")
            return False
        
        if self.click(self.CATEGORY_ACTION_BUTTON) == False:
            writeToLog("INFO","FAILED to click on action button")
            return False 
        
        if self.click(self.CATEGORY_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on edit button")
            return False 
        
        writeToLog("INFO","Success, all entry details was verified successfully")
        return True