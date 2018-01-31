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
        if self.click(tmpNavCategoryName, 30) == False:
            writeToLog("INFO","FAILED to click on category name '" + tmpNavCategoryName + "' in the nav bar")
            return False
        
        # Verify category page open
        if self.wait_visible(tmpCategoryName, 30) == False:
            writeToLog("INFO","FAILED to verify category page is display")
            return False
        
        writeToLog("INFO","Success Category page display")
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
    # TODO Not complete
#     def navigateToEditEntryPageFromCategoryPage(self, categoryName, entryName): 
#         tmp_entry_name = (self.clsCommon.editEntryPage.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[0], self.clsCommon.editEntryPage.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[1].replace('ENTRY_NAME', entryName))
#         #Check if we already in edit entry page
#         if self.wait_visible(tmp_entry_name, 5) != False:
#             writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
#             return True  
#         
#         if self.navigateToCategory(categoryName) == False:
#             writeToLog("INFO","FAILED to navigate to category: " + categoryName)
#             return False 
#         sleep(3)
#         
#         tmp_entry = (self.CATEGORY_ENTRY_SEARCH_RESULT[0], self.CATEGORY_ENTRY_SEARCH_RESULT[1].replace('ENTRY_NAME', entryName))
#         tmp_entryParentEl = self.get_element(tmp_entry)
#         if tmp_entryParentEl == None:
#             writeToLog("INFO","FAILED to find entry '" + entryName +"' in category '" + categoryName + "'")
#             return False      
#         
#         if self.hover_on_element(tmp_entry) == False:
#             writeToLog("INFO","FAILED to hover on entry '" + entryName +"' in category '" + categoryName + "'")
#             return False                
#         
#         # Check the 3 dots on the entry thumbnail
#         try:
#             EntryDotsButton = self.get_child_element(tmp_entryParentEl, self.EDIT_ENTRY_3_DOTS_ON_ENTRY_THUMBNAIL)
#             EntryDotsButton.click()
#         except NoSuchElementException:
#             writeToLog("INFO","FAILED to find 3 dots on entry '" + entryName + "' thumbnail")
#             return False  
#          
#         
#         # Check the edit button on the thumbnail
#         try:
#             editEntryButton = self.get_child_element(tmp_entryParentEl, self.EDIT_ENTRY_EDIT_ENTRY_BUTTON_ON_THUMBNAIL)
#             editEntryButton.click()
#         except NoSuchElementException:
#             writeToLog("INFO","FAILED to find edit button on entry '" + entryName + "' thumbnail")
#             return False              # verify image was add
#             if self.wait_visible(self.EDIT_ENTRY_VERIFY_IMAGE_ADDED_TO_THUMBNAIL_AREA, 20) == False:
#                 writeToLog("INFO","FAILED to verify capture was added to thumbnail area")
#                 return False
#          
# 
# 
#         #Check if we already in edit entry page
#         if self.wait_visible(tmp_entry_name, 5) == False:
#             writeToLog("INFO","FAILED to verify edit entry '" + entryName + "'page display")
#             return False         
#         return True          