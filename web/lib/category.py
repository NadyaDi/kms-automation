from base import *
import clsTestService
from general import General
from logger import writeToLog
from selenium.webdriver.common.keys import Keys


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
    SUB_CATEGORY_NAME_NAV_BAR                                   = ('xpath', "//a[@role='menuitem' and contains(text(), 'CATEGORY_NAME')]")# When using this locator, replace 'CATEGORY_NAME' string with your real category name
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
    CATEGORY_NO_RESULTS_MSG_NEW_UI                              = ('xpath', '//div[@class="no-results_body" and text()="No media results were found. Try to adjust your search terms."]')
    CATEGORY_NO_RESULTS_MSG_OLD_UI                              = ('xpath','//div[@class="alert alert-info" and text() = "No Search Results..."]') 
    CATEGORY_TABLE_SIZE                                         = ('xpath', '//table[@class="table table-hover mediaTable"]/tbody/tr')
    CATEGORY_TABLE_SIZE_NEW_UI                                  = ('xpath', '//li[contains(@class,"galleryItem")]')
    CATEGORY_TABLE_SIZE_AFTER_SEARCH                            = ('xpath', '//div[@class="results-entry__container"]')
    CATEGORY_TITLE                                              = ('xpath', '//span[@id="gallery_title"]')
    CATEGORY_NO_MORE_MEDIA_FOUND_MSG                            = ('xpath' , '//div[@id="entries_scroller_alert" and text()="No more Entries found."]')
    CATEGORY_NO_MORE_MEDIA_FOUND_NEW_UI_MSG                     = ('xpath' , '//div[@class="no-results alert alert-info" and text()="No more media found."]')
    CATEGORY_NO_MORE_MEDIA_ITEMS_MSG                            = ('xpath' , '//div[@id="channelGallery_scroller_alert" and text()="There are no more media items."]')
    CATEGORY_EDIT_ENTRY_BTN_OLD_UI                              = ('xpath', '//a[@aria-label="Edit ENTRY_NAME"]')          
    CATEGORY_EDIT_ENTRY_BTN_NEW_UI                              = ('xpath', '//a[@aria-label="Edit ENTRY_NAME"]')
    EDIT_CATEGORY_NAME_TEXTBOX                                  = ('xpath', '//input[@id="Category-name"]')
    EDIT_CATEGORY_DESCRIPTION_IFRAME                            = ('class_name', "wysihtml5-sandbox")
    EDIT_CATEGORY_DESCRIPTION_TEXT_BOX                          = ('xpath', "//div[@class='content']")
    EDIT_CATEGORY_DETAILS_DESCRIPTION                           = ('tag_name', 'body') #before using need to switch frame and click on the description box
    EDIT_CATEGORY_DETAILS_TAGS                                  = ('id', 's2id_tags')
    EDIT_CATEGORY_DETAILS_TAGS_INPUT                            = ('xpath', "//input[contains(@id,'s2id_autogen') and contains(@class, 'focused')]")
    EDIT_CATEGORY_TAGS_RESULT                                   = ('xpath', "//span[@class='select2-match' and contains(text(),'TAGS')]")
    EDIT_CATEGORY_CLEAR_TAGS_RESULT                             = ('xpath', "//a[@class='select2-search-choice-close']")
    EDIT_CATEGORY_SAVE_BUTTON                                   = ('xpath', "//button[@id='Category-submit']")
    EDIT_CATEGORY_SUCCESS_MESSAGE                               = ('xpath', "//div[contains(.,'The information was saved successfully')]")
    EDIT_CATEGORY_BACK_TO_CATEGORY_BUTTON                       = ('xpath', "//a[@class='btn btn-link' and contains(text(), 'Back to Category')]")
    CATEGORY_DESCRIPTION                                        = ('xpath', "//div[@class='js-description' and contains(text(), 'CATEGORY_DESCRIPTION')]")
    CATEGORY_TAGS                                               = ('xpath', "//a[@class='badge badge-info' and contains(text(), 'CATEGORY_TAGS')]")
    CATEGORY_GO_TO_CATEGORY_AFTER_UPLOAD                        = ('xpath', "//a[@id='next' and text()='Go To Category']")
    CATEGORIES_TABLE_SIZE                                       = ('xpath', '//li[@class="gallery-result row-fluid"]')
    CATEGORIES_NO_MORE_GALLERIES_ALERT                          = ('xpath', '//div[@class="message__text" and text()="No more galleries found."]')
    CATEGORIES_PAGE_ALL_GALLERIES_LIST                          = ('xpath', '//ul[@class="galleries-results-list row-fluid span12"]')                                       
    CATEGORY_MEMBERS_TAB                                        = ('xpath', '//a[@id="categorymembers-tab"]')
    CATEGORY_ADD_MEMBER_MODAL_USERNAME_FIELD                    = ('xpath', '//input[@id="AddCategoryMember-userId"]')   
    CATEGORY_ADD_MEMBER_MODAL_SET_PERMISSION                    = ('xpath', '//select[@id="AddCategoryMember-permission"]')
    CATEGORY_REFRESH_NOW_BUTTON                                 = ('xpath', "//a[text()='Refresh Now']")
    CATEGORY_EDIT_PAGE_TITLE                                    = ('xpath', "//h1[@id='category_title_edit']")
    CATEGORY_IMPORT_MEMBER_BUTTON                               = ('xpath', "//a[@id='importMembersBtn']")
    CATEGORY_MEMBERS_TAB_NEW_MEMBER_ROW                         = ('xpath', '//div[@class="row-fluid memberRow" and @data-id="MEMBER"]')
    CATEGORY_INHERIT_PERMISSIONS_BUTTON                         = ('xpath', "//input[@id='inherit']")
    CATEGORY_COMFIRM_INHERIT_PERMISSIONS                        = ('xpath', "//a[@class='btn btn-danger' and text()='Yes']")
    CATEGORY_GALLEY_ALL_MEDIA_TABLE                             = ('xpath', "//div[@id='galleryGrid']")
    CATEGORY_ADD_TO_CATEGORY_BUTTON                             = ('xpath', "//a[@id='tab-addcontent']")
    CATEGORY_MODERATION_TAB                                     = ('xpath', "//a[@id='categorymoderation-tab']")
    #=============================================================================================================
    def clickOnEntryAfterSearchInCategory(self, entryName):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            tmpEntrySearchName = (self.CATEGORY_ENTRY_SEARCH_RESULT[0], self.CATEGORY_ENTRY_SEARCH_RESULT[1].replace('ENTRY_NAME', entryName))
            if self.click(tmpEntrySearchName, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on Thumbnail of entry name '" + entryName + "' after search")
                return False
            sleep(3)    
        else:
            return self.clsCommon.myMedia.clickResultEntryAfterSearch(entryName)
            
            
    def navigateToCategory(self, categoryName, forceNavigate=False):
        # Check if we are already in category page
        tmpCategoryName = (self.CATEGORY_TITLE_IN_CATEGORY_PAGE[0], self.CATEGORY_TITLE_IN_CATEGORY_PAGE[1].replace('CATEGORY_NAME', categoryName))
        if forceNavigate == False:
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
    
    
    # @Author: Michal Zomper
    def navigateToSubCateogry(self, parentCategory, subCategory, forceNavigate=False):
        tmpSubCategoryName = (self.CATEGORY_TITLE_IN_CATEGORY_PAGE[0], self.CATEGORY_TITLE_IN_CATEGORY_PAGE[1].replace('CATEGORY_NAME', subCategory))
        if forceNavigate == False:
            # Check if we are already in category page
            if self.wait_visible(tmpSubCategoryName, 5) != False:
                writeToLog("INFO","Success Already in my category page")
                return True
    
        tmpParentCategoryName = (self.CATEGORY_NAME_NAV_BAR[0], self.CATEGORY_NAME_NAV_BAR[1].replace('CATEGORY_NAME', parentCategory))
        if self.hover_on_element(tmpParentCategoryName) == False:
            writeToLog("INFO","FAILED to hover on parent category page")
            return False
        sleep(2)
        tmpNavSubCategoryName = (self.SUB_CATEGORY_NAME_NAV_BAR[0], self.SUB_CATEGORY_NAME_NAV_BAR[1].replace('CATEGORY_NAME', subCategory))
        if self.click(tmpNavSubCategoryName, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on category name '" + subCategory + "' in the nav bar")
            return False
            
        # Verify category page open
        if self.wait_visible(tmpSubCategoryName, 30) == False:
            writeToLog("INFO","FAILED to verify category page is display")
            return False
        
        return True
    
    
    def searchEntryInCategory(self, entryName):
        if self.searchInCategoryWithoutVerifyResults(entryName) == False:
            writeToLog("INFO","FAILED to make a search")
            return False              
# TODO remove next block
#         if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:    
#             # Verify that the entry was found  
#             tmpEntrySearchName = (self.CATEGORY_ENTRY_SEARCH_RESULT[0], self.CATEGORY_ENTRY_SEARCH_RESULT[1].replace('ENTRY_NAME', entryName))
#             if self.get_element(tmpEntrySearchName) == None:
#                 writeToLog("INFO","FAILED to find entry '" + entryName + "' in search result")
#                 return False
#         else:
        if self.clsCommon.myMedia.getResultAfterSearch(entryName) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' in search result")
            return False                
        writeToLog("INFO","Success entry '" + entryName + "' was found")
        return True
    
    
    # @Author: Inbar Willman
    # Search in category without verify results
    # noQuotationMarks = True will force and wont add quotation marks at the beginning and the end of searchText(when Elastic search is enabled)
    def searchInCategoryWithoutVerifyResults(self, searchText, noQuotationMarks=False):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            # Click on the magnafine glass
            if self.click(self.CATEGORY_SEARCH_MAGNAFINE_GLASS, 30) == False:
                writeToLog("INFO","FAILED to click on magnafine glass in category page")
                return False
            sleep(2)
            # Search Entry     
            self.clsCommon.myMedia.getSearchBarElement().click()
        
        if noQuotationMarks == False:
            if self.clsCommon.isElasticSearchOnPage() == True:
                searchLine = '"' + searchText + '"'
            else:
                searchLine = searchText
        else:
            searchLine = searchText
            
        self.clsCommon.myMedia.getSearchBarElement().send_keys(searchLine)
        sleep(2)
        self.clsCommon.general.waitForLoaderToDisappear()
        
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


    # Author: Tzachi Guetta & Oleg Sigalov
    # The function perform upload to new media from category page
    # each item in uploadEntrieList need to have to value from type  "UploadEntry":  
    # UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
    # if we need only 1 upload we can set :self.entry1 = UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3) 
    # and pass only self.entry1
    # if we need to upload more then 1 entry we need to pass a list of UploadEntry : self.uploadEntrieList = [self.entry1, self.entry2,....]
    def addNewContentToCategory(self, categoryName, uploadEntrieList):
        try:
            if self.clsCommon.navigateTo(enums.Location.CATEGORY_PAGE, nameValue=categoryName) == False:
                writeToLog("INFO","FAILED navigate to category: " + self.categoryName)
                return False      
            
            if type(uploadEntrieList) is list:
                for entry in uploadEntrieList:
                    if self.addNewContentToCategoryWithoutNavigate(entry) == False:
                        writeToLog("INFO","FAILED to upload new media to category")
                        return False 
            else:
                if self.addNewContentToCategoryWithoutNavigate(uploadEntrieList) == False:
                    writeToLog("INFO","FAILED to upload new media to category")
                    return False  
                
        except:
            return False
        
        writeToLog("INFO","Success, media was added to category successfully")
        return True
    
    
    # Author: Michal Zomper
    #UploadEntry parameter need to have : UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
    def addNewContentToCategoryWithoutNavigate(self, uploadEntry):
        if self.click(self.clsCommon.category.CATEGORY_ADD_TO_CATEGORY_BUTTON) == False:
            writeToLog("INFO","FAILED to click add to Gallery button")
            return False     
            
        sleep(4)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30)
        
        if self.click(self.CATEGORY_ADD_NEW_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Add New at category page")
            return False
        sleep(2)
        
        if self.click(self.CATEGORY_ADD_NEW_MEDIA_UPLOAD_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Add New -> Media upload, at category page")
            return False
        sleep(3)
        
        if self.clsCommon.upload.uploadEntry(uploadEntry.filePath, uploadEntry.name, uploadEntry.description, uploadEntry.tags, uploadEntry.timeout,retries=1,  uploadFrom=None) == None:
            writeToLog("INFO","FAILED to upload media from category page: " + uploadEntry.name)
            return False
        
        # Click 'Go To Category'
        if self.click(self.CATEGORY_GO_TO_CATEGORY_AFTER_UPLOAD, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on 'Go To Category'")
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
                parent_entry = parent_entry.find_element_by_xpath("..")
            except NoSuchElementException:
                writeToLog("INFO","FAILED to get entry '" + entryName + "' element")
                return False
             
            if self.click_child(parent_entry, self.CATEGORY_PLUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL, timeout=20, multipleElements=True) == False:
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
            if self.click_child(parent_entry, self.CATEGORY_MINUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL, timeout=20, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on the minus button in order to close entry details")
                return False
            
        writeToLog("INFO","Success, all entry details was verified successfully")
        return True
    
    
    # Author: Michal Zomper 
    def navigateToEditCategoryPage(self, categoryName):
        if self.navigateToCategory(categoryName) == False:
            writeToLog("INFO","FAILED navigate to category")
            return False
        sleep(2)
        
        if self.click(self.CATEGORY_ACTION_BUTTON) == False:
            writeToLog("INFO","FAILED to click on action button")
            return False 
        
        if self.click(self.CATEGORY_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on edit button")
            return False 
        
        if self.is_visible(self.CATEGORY_EDIT_PAGE_TITLE, multipleElements= False) == False:
            writeToLog("INFO","FAILED, can NOT find edit entry page title")
            return False 
            
        writeToLog("INFO","Success, Category edit page is dispaly")
        return True
    
    
    # Author: Michal Zomper 
    def navigateToEditSubCategoryPage(self, parentCategory, subCategory, forcrNavigate=False):
        if self.navigateToSubCateogry(parentCategory, subCategory, forcrNavigate) == False:
            writeToLog("INFO","FAILED navigate to category")
            return False
        sleep(3)
        
        if self.click(self.CATEGORY_ACTION_BUTTON) == False:
            writeToLog("INFO","FAILED to click on action button")
            return False 
        
        if self.click(self.CATEGORY_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on edit button")
            return False 
        
        if self.is_visible(self.CATEGORY_EDIT_PAGE_TITLE, multipleElements= False) == False:
            writeToLog("INFO","FAILED, can NOT find edit entry page title")
            return False 
            
        writeToLog("INFO","Success, Category edit page is dispaly")
        return True
    
    
    # @Author: Inbar Willman
    # Search entries in category
    def searchEntriesInCategory(self, entriesList, categoryName):
        # Navigate to category
        if self.navigateToCategory(categoryName) == False:
            writeToLog("INFO","FAILED to navigate to category")
            return False 
        
        # Search each entry in category
        for entry in entriesList:
            if self.searchEntryInCategory(entry) == False:
                writeToLog("INFO","FAILED to find entry in category")
                return False  
            
            # Clear search content  
            self.clsCommon.myMedia.clearSearch()
            
        return True  
    
    
    # @Author: Inbar Willman
    # Search in category when there are no results
    def searchInCategoryNoResults(self, search, categoryName):
        # Navigate to category
        if self.navigateToCategory(categoryName) == False:
            writeToLog("INFO","FAILED to navigate to category")
            return False 
        
        # Make a search that won't return any results
        if self.searchInCategoryWithoutVerifyResults(search) == False:
            writeToLog("INFO","FAILED to make a search in category page")
            return False  
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            no_results_msg = self.CATEGORY_NO_RESULTS_MSG_NEW_UI
        else:
            no_results_msg = self.CATEGORY_NO_RESULTS_MSG_OLD_UI
        
        # Verify that correct message is displayed  
        if self.is_visible(no_results_msg) == False:
            writeToLog("INFO","FAILED to displayed correct message")
            return False              
            
        # Clear search content  
        self.clsCommon.myMedia.clearSearch()
            
        return True 
    
    # @Author: Inbar Willman
    # Verify category table results before scrolling down in page and after scrolling down in page - After scrolling down number of table should be bigger AFTER SEARCH
    # noQuotationMarks = True will force and wont add quotation marks at the beginning and the end of searchText(when Elastic search is enabled)
    def verifyCategoryTableSizeBeforeAndAfterScrollingDownInPage(self, search, pageSizeBeforeScrolling, pageSizeAfterScrolling, noQuotationMarks=False):
        # Make a search in page that will return results that are bigger than the page side
        if self.searchInCategoryWithoutVerifyResults(search, noQuotationMarks) == False:
            writeToLog("INFO","FAILED to make a search in category")
            return False         
                  
        if self.clsCommon.isElasticSearchOnPage() == True:
            categoryTableSizeLocator = self.CATEGORY_TABLE_SIZE_AFTER_SEARCH
        else:
            categoryTableSizeLocator = self.CATEGORY_TABLE_SIZE
                      
        # Check page size before scrolling
        category_table_size = len(self.get_elements(categoryTableSizeLocator))
        if category_table_size != pageSizeBeforeScrolling:
            writeToLog("INFO","FAILED to display correct number of entries in results - Before scrolling down in page")
            return False   
        
        # Click outside search field
        self.click(self.CATEGORY_TITLE)
        
        # Scroll down in page in order get all entries in results for the search
        if self.clsCommon.myMedia.showAllEntries(searchIn = enums.Location.CATEGORY_PAGE, afterSearch=True) == False:
            writeToLog("INFO","FAILED to scroll down in page")
            return False      
                           
        # Check page size after scrolling
        category_table_size = len(self.get_elements(categoryTableSizeLocator))
        if category_table_size != pageSizeAfterScrolling:
            writeToLog("INFO","FAILED to display correct number of entries in results - after scrolling down in page")
            return False    
        
        return True
        
        
    # @Author: Inbar Willman
    # Navigate to edit entry page from category page without making a search in category page
    def navigateToEditEntryPageFromCategoryWhenNoSearchIsMade(self, entryName):
        # "+" icon on thunail
        tmp_entry_thumbnail = (self.CATEGORY_ENTRY_THUMBNAIL[0], self.CATEGORY_ENTRY_THUMBNAIL[1].replace('ENTRY NAME', entryName))
        
        # Edit entry icon
        tmp_entry_edit_btn = None
        
        # If we are in new UI - hover over edit button before clicking
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            #Set edit button
            tmp_entry_edit_btn = (self.CATEGORY_EDIT_ENTRY_BTN_NEW_UI[0], self.CATEGORY_EDIT_ENTRY_BTN_NEW_UI[1].replace('ENTRY_NAME', entryName))
            if self.hover_on_element(tmp_entry_edit_btn) == False:
                writeToLog("INFO","FAILED to hover edit entry button")
                return False
    
        # If we are in old UI we need to click first on "+" icon on entry's thumbnail
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            try:
                parent_entry = self.get_element(tmp_entry_thumbnail)
                parent_entry = parent_entry.find_element_by_xpath("..")
            except NoSuchElementException:
                writeToLog("INFO","FAILED to get entry '" + entryName + "' element")
                return False
            
            if self.click_child(parent_entry, self.CATEGORY_PLUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL, timeout=20, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on the plus button in order to see entry details")
                return False 
            
            #set edit button for old UI
            tmp_entry_edit_btn = (self.CATEGORY_EDIT_ENTRY_BTN_OLD_UI[0], self.CATEGORY_EDIT_ENTRY_BTN_OLD_UI[1].replace('ENTRY_NAME', entryName))   
        
        # Click on edit button
        if self.click(tmp_entry_edit_btn) == False:
            writeToLog("INFO","FAILED to click on edit button")
            return False   
        
        # Verify that we are in edit entry page - wait until you see edit entry page title
        tmp_entry_title = (self.clsCommon.editEntryPage.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[0], self.clsCommon.editEntryPage.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmp_entry_title) == False:
            writeToLog("INFO","FAILED to displayed edit entry page title")
            return False   
        
        return True           
    
    # Author: Michal Zomper
    def editCategoryMatedate(self, newCategoryName="", newCategorydescription="", newCategoryTags=""):
        if newCategoryName != "":
            if self.clear_and_send_keys(self.EDIT_CATEGORY_NAME_TEXTBOX, newCategoryName) == False:
                writeToLog("INFO","FAILED to replace category name to:'" + newCategoryName + "'")
                return False
        
        if newCategorydescription != "":
            if self.fillCategoryDescription(newCategorydescription, uploadboxId=-1) == False:
                writeToLog("INFO","FAILED to replace category description to:'" + newCategoryName + "'")    
                return False
        
        if newCategoryTags != "":
            if self.fillCategoryTags(newCategoryTags, uploadboxId=-1) == False:
                writeToLog("INFO","FAILED to replace category tags to:'" + newCategoryTags + "'")    
                return False  
            
        # Click Save
        if self.click(self.EDIT_CATEGORY_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False
        sleep(3)
        
        # Wait for loader to disappear
        self.clsCommon.general.waitForLoaderToDisappear()
        
        # Wait for 'Your changes have been saved.' message
        if self.wait_visible(self.EDIT_CATEGORY_SUCCESS_MESSAGE, 45) == False:                
            writeToLog("INFO","FAILED to find success message")
            return False

        return True
    
    
    # Author: Michal Zomper       
    # The method supports BOTH single and multiple upload    
    def fillCategoryDescription(self, text, uploadboxId=-1):
        if uploadboxId != -1:
            # Get the uploadbox element
            uploadBoxElement = self.get_element(self.replaceInLocator(self.UPLOAD_UPLOADBOX, '[ID]', str(uploadboxId)))
            
            # Switch to Description iFrame
            descpriptionIframe = self.get_child_element(uploadBoxElement, self.EDIT_CATEGORY_DESCRIPTION_IFRAME)
        else:
            # Switch to Description iFrame
            descpriptionIframe = self.get_element(self.EDIT_CATEGORY_DESCRIPTION_IFRAME)
        
        # Switch to iframe which is contains the description text box    
        self.driver.switch_to.frame(descpriptionIframe)
        
        # Click on Description text box
        el = self.get_element(self.EDIT_CATEGORY_DESCRIPTION_TEXT_BOX)
        if el.click() == False:
            writeToLog("INFO","FAILED to click on Description filed")
            return False               
        sleep(2)
        
        # Enter text Description
        if self.clear_and_send_keys(self.EDIT_CATEGORY_DETAILS_DESCRIPTION, text) == True:
            return True
        else:
            writeToLog("INFO","FAILED to type in Description")
            return False
        self.switch_to_default_content()
                             
     
    # Author: Michal Zomper                        
    # The method supports BOTH single and multiple upload
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillCategoryTags(self, tags, uploadboxId=-1):
        try:
            self.switch_to_default_content()
            if self.getAppUnderTest() == enums.Application.BLACK_BOARD:
                self.clsCommon.blackBoard.switchToBlackboardIframe()
            elif self.getAppUnderTest() == enums.Application.SHARE_POINT:
                self.clsCommon.sharePoint.switchToSharepointIframe()
                self.get_body_element().send_keys(Keys.PAGE_DOWN)
                sleep(1)
            # If upload single (method: uploadEntry)
            if uploadboxId == -1:
                tagsElement = self.get_element(self.EDIT_CATEGORY_DETAILS_TAGS)
            else:
                # Get the uploadbox element
                uploadBoxElement = self.get_element(self.replaceInLocator(self.UPLOAD_UPLOADBOX, '[ID]', str(uploadboxId)))            
                tagsElement = self.get_child_element(uploadBoxElement, self.EDIT_CATEGORY_DETAILS_TAGS)
                
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get Tags filed element")
            return False
                
        self.click(self.EDIT_CATEGORY_CLEAR_TAGS_RESULT, timeout=10, multipleElements=False)
        if self.clickElement(tagsElement) == False:
            writeToLog("INFO","FAILED to click on Tags filed")
            return False            
        sleep(1)

        if(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
            # Remove the Mask over all the screen (over tags filed also)
            maskOverElement = self.get_element(self.clsCommon.channel.CHANNEL_REMOVE_TAG_MASK)
            self.driver.execute_script("arguments[0].setAttribute('style','display: none;')",(maskOverElement))     
            
            if self.clickElement(tagsElement) == False:
                writeToLog("INFO","FAILED to click on Tags filed")
                return False    
             
        if uploadboxId == -1: # -1 stands for single
            if self.send_keys(self.EDIT_CATEGORY_DETAILS_TAGS_INPUT, tags) == False:
                writeToLog("INFO","FAILED to add new tags")
                return False
        else:
            if self.send_keys_to_child(uploadBoxElement, self.EDIT_CATEGORY_DETAILS_TAGS_INPUT, tags) == True:
                return True
            
        return True  


    # Author: Michal Zomper   
    def navigateToCategoryPageFronEditCategoryPage(self, categoryName):
        if self.click(self.EDIT_CATEGORY_BACK_TO_CATEGORY_BUTTON, timeout=15) == False:
            writeToLog("INFO","FAILED to click on back to category button")
            return False
        
        sleep(4)
        tmpCategoryName = (self.CATEGORY_TITLE_IN_CATEGORY_PAGE[0], self.CATEGORY_TITLE_IN_CATEGORY_PAGE[1].replace('CATEGORY_NAME', categoryName))
        if self.wait_visible(tmpCategoryName, 30) == False:
            writeToLog("INFO","FAILED to verify category page is display")
            return False
        
        return True
    
    
    # Author: Michal Zomper   
    def varifyCategoryMatedate(self, categoryName, categoryDescription, categoryTags):
        tmpCategoryName = (self.CATEGORY_TITLE_IN_CATEGORY_PAGE[0], self.CATEGORY_TITLE_IN_CATEGORY_PAGE[1].replace('CATEGORY_NAME', categoryName))
        if self.wait_visible(tmpCategoryName, 30) == False:
            writeToLog("INFO","FAILED to verify category name")
            return False
        
        tmpCategoryDescription = (self.CATEGORY_DESCRIPTION[0], self.CATEGORY_DESCRIPTION[1].replace('CATEGORY_DESCRIPTION', categoryDescription))
        if self.wait_visible(tmpCategoryDescription, 30) == False:
            writeToLog("INFO","FAILED to verify category description")
            return False
        
        tmpCategoryTags = (self.CATEGORY_TAGS[0], self.CATEGORY_TAGS[1].replace('CATEGORY_TAGS', categoryTags[:-1]))
        if self.wait_visible(tmpCategoryTags, 30) == False:
            writeToLog("INFO","FAILED to verify category tags")
            return False
        
        return True
    
   
    # @Author: Inbar Willman
    # Verify that galleries are sorted correctly by the chosen sort
    def verifySortInGalleries(self, sortBy, galleriesList):
        if self.clsCommon.channel.selectSortChannelOptionInMyChannelsPage(sortBy.value) == False:
            writeToLog("INFO","FAILED to sort galleries by: " + sortBy.value)
            return False
        
        if self.showAllGalleries() == False:
            writeToLog("INFO","FAILED to show all galleries")
            return False
            
        try:
            galleriesInPage = self.get_element(self.CATEGORIES_PAGE_ALL_GALLERIES_LIST).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get channels list in galley")
            return False
        galleriesInPage = galleriesInPage.split("\n")
        prevChannelIndex = -1
        
        for gallery in galleriesList:
            galleryCurrentIndex = galleriesInPage.index(gallery.lower())
            if prevChannelIndex > galleryCurrentIndex:
                writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct. gallery '" + gallery + "' isn't in the right place" )
                return False
            prevChannelIndex = galleryCurrentIndex
                
        writeToLog("INFO","Success, verify sort galleries by '" + sortBy.value + "' was successful")
        return True   
    
    
    #  @Author: Inbar Willman    
    def showAllGalleries(self, timeOut=60): 
        if len(self.get_elements(self.CATEGORIES_TABLE_SIZE)) < 5:
            writeToLog("INFO","Success, All galleries are display")
            return True 
                  
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)
        while wait_until > datetime.datetime.now():
            if self.is_present(self.CATEGORIES_NO_MORE_GALLERIES_ALERT, 2) == True:
                writeToLog("INFO","Success, All channels are display")
                return True 
             
            self.clsCommon.sendKeysToBodyElement(Keys.END)
             
        writeToLog("INFO","FAILED to show all channels")
        return False    

      
        # @Author: Michal Zomper
    # Go to members tab 
    def navigateToCategoryMembersTab(self):
        if self.click(self.CATEGORY_MEMBERS_TAB) == False:
            writeToLog("INFO","FAILED to click on members tab")
            return False     
        return True
    
    
    # @Author: Michal Zomper
    # membersList need to be like: [(userName, permission), (userName, permission) ......]
    def addMembersToCategory(self, categoryName, membersList):
        if self.navigateToEditCategoryPage(categoryName) == False:
            writeToLog("INFO","FAILED to navigate to edit category page")
            return False  
        sleep(1)   
        
        if self.navigateToCategoryMembersTab() == False:
            writeToLog("INFO","FAILED to click on members tab")
            return False  
        sleep(2)
        
        if type(membersList) is list:
            for member in membersList:
                if self.addMemberToCategory(categoryName, member[0], member[1], forceNavigate=False) == False:
                    writeToLog("INFO","FAILED to add user '" + member[0] + "' to category")
                    return False
                sleep(4)
        
        writeToLog("INFO","Success, All members was added to category")
        return True


#     # @Author: Michal Zomper
#     def addMemberToCategory(self, categoryName, username, permission=enums.CategoryMemberPermission.MEMBER, forceNavigate=True):
#         if forceNavigate:
#             if self.navigateToEditCategoryPage(categoryName) == False:
#                 writeToLog("INFO","Failed to navigate to edit category page")
#                 return False  
#             sleep(1)   
#              
#             # Navigate to members tab
#             if self.navigateToCategoryMembersTab() == False:
#                 writeToLog("INFO","Failed to click on members tab")
#                 return False  
#             sleep(2)
#         
#         # Wait until page contains add member button
#         if self.wait_visible(self.clsCommon.channel.CHANNEL_ADD_MEMBER_BUTTON) == False:
#             writeToLog("INFO","Failed to display add member tab content")
#             return False           
#         
#         # Click on add member button
#         if self.click(self.clsCommon.channel.CHANNEL_ADD_MEMBER_BUTTON) == False:
#             writeToLog("INFO","Failed to click on add members button")
#             return False   
#         
#         # Wait until add member modal is displayed
#         sleep(3)
#         
#         #Click on username field
#         if self.click(self.CATEGORY_ADD_MEMBER_MODAL_USERNAME_FIELD) == False:
#             writeToLog("INFO","Failed to click on username field")
#             return False             
#                     
#         # Insert username to field
#         if self.send_keys(self.CATEGORY_ADD_MEMBER_MODAL_USERNAME_FIELD, username) == False:
#             writeToLog("INFO","Failed to insert username")
#             return False 
#         
#         # Set permission
#         if self.chooseMemberPermissionInCategory(permission) == False:
#             writeToLog("INFO","Failed to set permission")
#             return False   
#         
#         #Click add button
#         if self.click(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_ADD_BUTTON) == False:
#             writeToLog("INFO","Failed to click on add button")
#             return False  
#         
#         # Wait until add member window isn't displayed
#         if self.wait_while_not_visible(self.CATEGORY_ADD_MEMBER_MODAL_USERNAME_FIELD, timeout=80) == False:
#             writeToLog("INFO","Failed to display add member window")
#             return False
#         sleep(3)
#         
#         
#         #Verify new member is added to member table
#         tmp_member_row = (self.clsCommon.channel.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[0], self.clsCommon.channel.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[1].replace('MEMBER', username))
#         if self.is_visible(tmp_member_row) == False:
#             writeToLog("INFO","Failed to add new member to table")
#             return False
#          
#         sleep(3)
#         writeToLog("INFO","Success, member '" + username + "' was added to category")
#         return True


    # @Author: Michal Zomper
    def addMemberToCategory(self, categoryName, username, permission=enums.CategoryMemberPermission.MEMBER, forceNavigate=True):
        if forceNavigate:
            if self.navigateToEditCategoryPage(categoryName) == False:
                writeToLog("INFO","FAILED to navigate to edit category page")
                return False  
            sleep(1)   
              
            # Navigate to members tab
            if self.navigateToCategoryMembersTab() == False:
                writeToLog("INFO","FAILED to click on members tab")
                return False  
            sleep(2)
         
        # Wait until page contains add member button
        if self.wait_visible(self.clsCommon.channel.CHANNEL_ADD_MEMBER_BUTTON) == False:
            writeToLog("INFO","FAILED to display add member tab content")
            return False           
         
        # Click on add member button
        if self.click(self.clsCommon.channel.CHANNEL_ADD_MEMBER_BUTTON) == False:
            writeToLog("INFO","FAILED to click on add members button")
            return False   
         
        # Wait until add member popup is displayed
        sleep(3)
        
        # Insert username to field
        if self.send_keys(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, username) == False:
            writeToLog("INFO","FAILED to insert username")
            return False
        
        sleep(3)
        tmpConfirmationLocator = (self.clsCommon.channel.CHANNEL_ADD_MEMBER_GROUP_CONFIRMATION[0], self.clsCommon.channel.CHANNEL_ADD_MEMBER_GROUP_CONFIRMATION[1].replace('USERNAME', username))
        if self.click(tmpConfirmationLocator) == False:
            writeToLog("INFO","FAILED to click on group search confirmation")
            return False   
                
        sleep(3)
        # Set permission
        if self.clsCommon.channel.chooseMemberPermissionInChannel(permission) == False:
            writeToLog("INFO","FAILED to set permission")
            return False   
        
        #Click add button
        if self.click(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_ADD_BUTTON) == False:
            writeToLog("INFO","FAILED to click on add button")
            return False 
         
        sleep(2)
        # Wait until add member modal isn't displayed
        if self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, timeout=80) == False:
            writeToLog("INFO","FAILED to display add member popup")
            return False    
        
        #Verify new member is added to member table
        tmp_member_row = (self.clsCommon.channel.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[0], self.clsCommon.channel.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[1].replace('MEMBER', username))
        if self.wait_visible(tmp_member_row) == False:
            writeToLog("INFO","FAILED new member was NOT added to members table")
            return False
        sleep(3)
        
        return True      
    
    
    # @Author: Michal Zomper 
    # Choose permission from drop down list
    def chooseMemberPermissionInCategory(self, permission = enums.CategoryMemberPermission.MEMBER):    
        # If permission is member click on member option       
        if permission ==  enums.CategoryMemberPermission.MEMBER:
            if self.select_from_combo_by_text(self.CATEGORY_ADD_MEMBER_MODAL_SET_PERMISSION, 'Member') == False:
                writeToLog("INFO","FAILED to click on member option")
                return False                    
       
        # If permission is contributor click on member option       
        elif permission ==  enums.CategoryMemberPermission.CONTRIBUTOR:
            if self.select_from_combo_by_text(self.CATEGORY_ADD_MEMBER_MODAL_SET_PERMISSION, 'Contributor') == False:
                writeToLog("INFO","FAILED to click on contributor option")
                return False  
            
        # If permission is moderator click on member option       
        elif permission ==  enums.CategoryMemberPermission.MODERATOR:
            if self.select_from_combo_by_text(self.CATEGORY_ADD_MEMBER_MODAL_SET_PERMISSION, 'Moderator') == False:
                writeToLog("INFO","FAILED to click on moderator option")
                return False 
        
        # If permission is manager click on member option       
        elif permission ==  enums.CategoryMemberPermission.MANAGER:
            if self.select_from_combo_by_text(self.CATEGORY_ADD_MEMBER_MODAL_SET_PERMISSION, 'Manager') == False:
                writeToLog("INFO","FAILED to click on manager option")
                return False   
            
        return True    
    
    
    # @Author: Oleg Sigalov
    # interval - interval between refresh
    def refreshNowCategory(self, timeout=30, interval=5):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while True:
            if self.click(self.CATEGORY_REFRESH_NOW_BUTTON, 5) == False:
                return True
            sleep(interval)
            if wait_until < datetime.datetime.now():
                writeToLog("INFO","WARNING 'Refresh Now' still appears, it possible because of an other entry in this category, timeout is:" + str(timeout))
                return True
            
            
    # @Author: Michal Zomper
    # Edit member permission
    def editCategoryMemberPermission(self,username, permission = enums.ChannelMemberPermission.MODERATOR): 
        #Click on edit button
        tmp_edit_button = (self.clsCommon.channel.CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON[0], self.clsCommon.channel.CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON[1].replace('MEMBER', username))
        if self.hover_on_element(tmp_edit_button) == False:
            writeToLog("INFO","FAILED to Hover above edit member button")
            return False
        
        if self.click(tmp_edit_button) == False:
            writeToLog("INFO","FAILED to click on edit button")
            return False               
                         
        # Set new permission
        if self.chooseMemberPermissionInCategory(permission) == False:
            writeToLog("INFO","FAILED to set new permission")
            return False   
        
        # Save new permission
        if self.click(tmp_edit_button) == False:
                writeToLog("INFO","FAILED to click on save button")
                return False                  
        
        return True
    
        
    def importMemberFormCategory(self):
        if self.navigateToCategoryMembersTab() == False:
            writeToLog("INFO","FAILED to click on members tab")
            return False  
        sleep(2)
        
        if self.click(self.CATEGORY_IMPORT_MEMBER_BUTTON) == False:
            writeToLog("INFO","FAILED to click on import member button")
            return False
        
        sleep(4)
        return True
    
    
    # @Author: Michal Zomper 
    def verifyMemberPermissionsInMemberTable(self, userId, permission):
        # Navigate to members tab
        if self.navigateToCategoryMembersTab() == False:
            writeToLog("INFO","FAILED to click on members tab")
            return False  
        sleep(2)
            
        tmpMember = (self.CATEGORY_MEMBERS_TAB_NEW_MEMBER_ROW[0], self.CATEGORY_MEMBERS_TAB_NEW_MEMBER_ROW[1].replace('MEMBER', userId))
        try:
            memberText = self.get_element_text(tmpMember, timeout=20)
            if memberText == None:
                writeToLog("INFO","FAILED to find member '" + userId +"' in members table")
                return False
                
        except NoSuchElementException:
            writeToLog("INFO","FAILED to find member '" + userId +"' in members table")
            return False
        
        if (permission.value in memberText) == False:
            writeToLog("INFO","FAILED, member '" + userId +"' permission does NOT match")
            return False
        
        writeToLog("INFO","Success, member '" + userId + "' was found in member table with the right permissions")
        return True
    
    
    # @Author: Michal Zomper 
    # membersList need to be like: [(userName, permission), (userName, permission) ......]
    def verifyMembersPermissionsInMemberTable(self, membersList):
        if self.navigateToCategoryMembersTab() == False:
            writeToLog("INFO","FAILED to click on members tab")
            return False  
        sleep(2)
        
        for member in membersList:
            if self.verifyMemberPermissionsInMemberTable(member[0], member[1]) == False:
                writeToLog("INFO","FAILED verify that user '" + member[0] + "' and permissions was found in members table")
                return False
            sleep(3)
        
        writeToLog("INFO","Success, All members display in members table") 
        return True
    
    
    # @Author: Michal Zomper 
    def inheritPermissionsFormCategory(self):
        if self.navigateToCategoryMembersTab() == False:
            writeToLog("INFO","FAILED to click on members tab")
            return False  
        sleep(2)
        
        if self.click(self.CATEGORY_INHERIT_PERMISSIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on inherit permissions button")
            return False
        sleep(2)
        
        if self.click(self.CATEGORY_COMFIRM_INHERIT_PERMISSIONS) == False:
            writeToLog("INFO","FAILED to click  on confirm inherit permissions button")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(4)
        return True


    #  @Author: Michal Zomper    
    # The function check and verify that the entries sort in category are in the correct order 
    def verifySortInCategory(self, sortBy, entriesList):
        if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.SORT_BY,sortBy) == False:
            writeToLog("INFO","FAILED to sort entries")
            return False
                
        if self.clsCommon.myMedia.showAllEntries(searchIn=enums.Location.CATEGORY_PAGE) == False:
            writeToLog("INFO","FAILED to show all entries in category page")
            return False
        sleep(10)
        
        try:
            entriesIncategory = self.wait_visible(self.CATEGORY_GALLEY_ALL_MEDIA_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False
        entriesIncategory = entriesIncategory.split("\n")
        
        if self.clsCommon.myMedia.verifySortOrder(entriesList, entriesIncategory) == False:
            writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct")
            return False

        writeToLog("INFO","Success, My media sort by '" + sortBy.value + "' was successful")
        return True



    # @Author: Inbar Willman
    # Navigate to add to category page
    def navigateToAddToCategory(self, categoryName):
        # Navigate to category
        if self.navigateToCategory(categoryName) == False:
            writeToLog("INFO","FAILED  to navigate to: " + categoryName)
            return False   
        
        # Click on 'Add to gallery'
        if self.click(self.CATEGORY_ADD_TO_CATEGORY_BUTTON) == False:
            writeToLog("INFO","Step 2: FAILED to to click on 'Add to Gallery' button")
            return 
        
        # wait until loading message disappear
        sleep(1)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30)  
        
        return True            
    
    
    
    #Author: Michal Zomper    
    def handlePendingEntriesInCategory(self, categoryName, toRejectEntriesNames, toApproveEntriesNames , navigate=True):
                       
        if navigate == True:
            if self.navigateToCategory(categoryName) == False:
                writeToLog("INFO","FAILED to navigate to  category: " +  categoryName)
                return False
            
            if self.click(self.CATEGORY_MODERATION_TAB, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on category moderation tab")
                return False        
        
        sleep(1)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30) 
        
        if self.clsCommon.channel.approveEntriesInPandingTab(toApproveEntriesNames) == False:
            writeToLog("INFO","FAILED to approve entries")
            return False  
        
        self.refresh()
        sleep(6)
        self.click(self.CATEGORY_MODERATION_TAB, timeout=60, multipleElements=True)
        
        if self.clsCommon.channel.rejectEntriesInPandingTab(toRejectEntriesNames) == False:
            writeToLog("INFO","FAILED to reject entries")
            return False 
       
        if self.navigateToCategory(categoryName, forceNavigate=True) == False:
            writeToLog("INFO","FAILED navigate to category page")
            return False  
            
        if self.verifyEntriesApprovedAndRejectedInCategory(toRejectEntriesNames, toApproveEntriesNames) == False:
            writeToLog("INFO","FAILED, not all entries was approved/ rejected as needed")
            return False 
        
        return True
    
    
    def verifyEntriesApprovedAndRejectedInCategory(self, toRejectEntriesNames, toApproveEntriesNames):
        if type(toRejectEntriesNames) is list:
            for rejectEntry in toRejectEntriesNames:
                if self.searchEntryInCategory(rejectEntry) == True:
                    writeToLog("INFO","FAILED, reject entry '" + rejectEntry + "' exist in category page although the entry was rejected")
                    return False 
                writeToLog("INFO","Preview step failed as expected - entry was rejected and should not be found")
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False 
        else:
            if toRejectEntriesNames != '':
                if self.searchEntryInCategory(toRejectEntriesNames) == True:
                    writeToLog("INFO","FAILED, reject entry '" + toRejectEntriesNames + "' exist in category page although the entry was rejected")
                    return False 
                writeToLog("INFO","Preview step failed as expected - entry was rejected and should not be found")
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False               
        
        if type(toApproveEntriesNames) is list:
            for approveEntry in toApproveEntriesNames:
                if self.searchEntryInCategory(approveEntry) == False:
                    writeToLog("INFO","FAILED, approved entry '" + approveEntry + "' doesn't exist in category page although the entry was approved")
                    return False 
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False 
        else:
            if toApproveEntriesNames != '':
                if self.searchEntryInCategory(toApproveEntriesNames) == False:
                    writeToLog("INFO","FAILED, approved entry '" + toApproveEntriesNames + "' doesn't exist in category page although the entry was approved")
                    return False 
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False 
        
        return True