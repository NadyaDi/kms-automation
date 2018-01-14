from base import *
import clsTestService
import clsCommon


class EditEntryPage(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Entry Page locators:
    #=============================================================================================================
    EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE            = ('xpath', "//span[@id='entryName' and contains(text(), 'ENTRY_NAME')]")
    EDIT_ENTRY_COLLABORATION_TAB                = ('id', "collaboration-tab")
    EDIT_ENTRY_ADD_COLLABORATOR_BUTTON          = ('class_name', "icon-plus icon-white")   
    #=============================================================================================================
    
    def navigateToEditEntryPageFromMyMedia(self, entryName):
        tmp_entry_name = (self.MY_MEDIA_ENRTY_DELETE_BUTTON[0], self.MY_MEDIA_ENRTY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 15) == True:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True        
        
        if self.clsCommon.myMedia.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to find: '" + entryName + "'")
            return False
                    
        if self.clsCommon.myMedia.clickEditEntryAfterSearchInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to on entry Edit button, Entry name: '" + entryName + "'")
            return False
        
        #Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 15) == False:
            writeToLog("INFO","FAILED to open edit entry page, Entry name: '" + entryName + "'")
            return False

    def navigateToEditEntryPageFromEntryPage(self,entryName):
        tmp_entry_name = (self.MY_MEDIA_ENRTY_DELETE_BUTTON[0], self.MY_MEDIA_ENRTY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 15) == True:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True  
        
        #Open "Actions" drop-down list 
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
            writeToLog("INFO","FAILED to click on Actions button")
            return False
        
        #Wait up to 5s
        self.wait_visible(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON, 5)  
         
        #Click on Edit button
        if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Edit button")
            return False    
        
        #Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 15) == False:
            writeToLog("INFO","FAILED to open edit entry page")
            return False
        
    def addCollaborator(self, entryName, userId, isCoPublisher, isCoEditor):
        if self.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to navigate to edit entry page")
            return False    
        
        #Click on collaboration tab
        if self.click(self.EDIT_ENTRY_COLLABORATION_TAB, "30") == False:
            writeToLog("INFO","FAILED to click on collaboration tab")
            return False    
        
        #click on add collaborator
        if self.click(self.EDIT_ENTRY_ADD_COLLABORATOR_BUTTON, "30") == False:
            writeToLog("INFO","FAILED to click on add collaborator button")
            return False                  
        