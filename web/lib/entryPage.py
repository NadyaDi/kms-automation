from base import *
import clsTestService
import enums



class EntryPage(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Entry Page locators:
    #=============================================================================================================
    ENTRY_PAGE_ENTRY_TITLE                                 = ('xpath', "//h3[@class='entryTitle' and contains(text(), 'ENTRY_NAME')]") # When using this locator, replace 'ENTRY_NAME' string with your real entry name
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST                        = ('id', "entryActionsMenuBtn")    
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON            = ('id', "tabLabel-Edit")      
    ENTRY_PAGE_DESCRIPTION                                 = ('xpath', "//div[@class='row-fluid normalWordBreak']")
    ENTRY_PAGE_TAGS                                        = ('class_name', "tagsWrapper")    
    ENTRY_PAGE_PUBLISH_BUTTON                              = ('id', "tab-Publish")  
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_DELETE_BUTTON          = ('id', "tabLabel-Delete")
    ENTRY_PAGE_CONFIRM_DELETE_BUTTON                       = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    #=============================================================================================================
    
    def navigateToEntryPageFromMyMedia(self, entryName):
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True    
        
        self.clsCommon.myMedia.searchEntryMyMedia(entryName)
        self.clsCommon.myMedia.clickEntryAfterSearchInMyMedia(entryName)
        # Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
        
        return True
        
    # Author: Michal Zomper     
    def navigateToEntryPageFromCategoryPage(self, entryName, categoryName):
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in entry page: '" + entryName + "'")
            return True
        
        if self.clsCommon.category.navigateToCategory(categoryName) == False:
            writeToLog("INFO","FAILED navigate to category:" + categoryName)
            return False             
            
        if self.clsCommon.category.searchEntryInCategory(entryName) == False:
            writeToLog("INFO","FAILED to search entry'" + entryName + "' in category" + categoryName)
            return False  
            
        # click on the entry
        if self.clsCommon.category.clickOnEntryAfterSearchInCategory(entryName) == False:
            writeToLog("INFO","FAILED to click on entry " + entryName)
            return False 
        
        if self.wait_visible(tmp_entry_name, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
           
        return True
        
        
    # Author: Michal Zomper     
    def verifyEntryMetadata(self, entryName, entryDescription, entryTags):
        # Verify entry name
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        # Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 20) == False:
            writeToLog("INFO","FAILED to verify entry name: '" + entryName + "'")
            return True     
        
        # Verify description
        # First get the description frame
        parentEldescription = self.get_element(self.ENTRY_PAGE_DESCRIPTION)
        if parentEldescription == None:
            writeToLog("INFO","FAILED to find description frame in entry page")
            return False   
        
        # Check that the description is the correct description
        if self.wait_for_text(self.ENTRY_PAGE_DESCRIPTION, entryDescription, 30, False) == False:
            writeToLog("INFO","FAILED to verify entry description: '" + entryName + "'")
            return True   
        
        # Verify tags
        # First get the tags frame
        parentEltags = self.get_element(self.ENTRY_PAGE_TAGS)
        if parentEltags == None:
            writeToLog("INFO","FAILED to find tags frame in entry page")
            return False   
        
        # Check that the description is the correct description
        if self.wait_for_text(self.ENTRY_PAGE_TAGS, entryTags, 30, True) == False:
            writeToLog("INFO","FAILED to verify entry tags: '" + entryTags + "'")
            return True   
        
        writeToLog("INFO","Success, all entry '" + entryName + "' metadata are correct")
        return True  
    
    
    
    def navigateToEntry(self, entryName, navigateFrom = enums.Location.MY_MEDIA, categoryName ="", channelName= ""):
        if navigateFrom == enums.Location.MY_MEDIA:
            if self.navigateToEntryPageFromMyMedia(entryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + enums.Location.MY_MEDIA)
                return False  
            
        elif navigateFrom == enums.Location.CATEGORY_PAGE:
            if self.navigateToEntryPageFromCategoryPage(entryName, categoryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + enums.Location.CATEGORY_PAGE)
                return False  
                
        elif navigateFrom == enums.Location.CHANNEL_PAGE:
            if self.clsCommon.channel.naviagteToEntryFromChannelPage(entryName, channelName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + enums.Location.CHANNEL_PAGE)
                return False
        
        return True
        
    def deleteEntryFromEntryPage(self, entryName, deleteFrom= enums.Location.MY_MEDIA, categoryName="", channelName=""):
        if self.navigateToEntry(entryName, deleteFrom, categoryName, channelName) == False:
            writeToLog("INFO","FAILED navigate to entry page")
            return False             
        
        if self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, 20) == False:
            writeToLog("INFO","FAILED to click on 'Actions' button")
            return False
        
        if self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_DELETE_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on delete button")
            return False
        
        if self.click(self.ENTRY_PAGE_CONFIRM_DELETE_BUTTON, 20) == False:
            writeToLog("INFO","FAILED to click confirm delete button")
            return False
        
        # Verify entry was delete: after entry delete the page that will display is the page that we enter the entry from
        if deleteFrom == enums.Location.MY_MEDIA:
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 1) == False:
                writeToLog("INFO","FAILED to verify that entry deleted")
                return False      
 
        elif deleteFrom == enums.Location.CATEGORY_PAGE:
            tmpCategoryName = (self.clsCommon.category.CATEGORY_TITLE_IN_CATEGORY_PAGE[0], self.clsCommon.category.CATEGORY_TITLE_IN_CATEGORY_PAGE[1].replace('CATEGORY_NAME', categoryName))
            if self.wait_visible(tmpCategoryName, 20) == False:
                writeToLog("INFO","FAILED to verify that entry deleted")
                return False
        
        elif deleteFrom == enums.Location.CHANNEL_PAGE:
            tmp_channel_title = (self.clsCommon.channel.CHANNEL_PAGE_TITLE[0], self.clsCommon.channel.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
            if self.wait_visible(tmp_channel_title, 20) == False:
                writeToLog("INFO","FAILED to verify that entry deleted")
                return False

        writeToLog("INFO","FAILED to verify that entry deleted")
        return True
        
            
        
        