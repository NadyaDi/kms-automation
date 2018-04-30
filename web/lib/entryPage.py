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
    ENTRY_PAGE_ADDTOPLAYLIST_BUTTON                        = ('id', "Addtoplaylists")  
    ENTRY_PAGE_PUBLISH_BUTTON                              = ('id', "tab-Publish")
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_DELETE_BUTTON          = ('id', "tab-Delete")                        
    ENTRY_PAGE_CONFIRM_DELETE_BUTTON                       = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    ENTRY_PAGE_DOWNLOAD_TAB                                = ('xpath', "//a[contains(@class,'btn responsiveSizePhone tab-download-tab')]")
    ENTRY_PAGE_MEDIA_IS_BEING_PROCESSED                    = ('xpath', "//h3[@class='muted' and contains(text(), 'Media is being processed')]")
    ENTRY_PAGE_PLAYER_IFRAME                               = ('xpath',"//iframe[@id='kplayer_ifp' and @class='mwEmbedKalturaIframe']") 
    ENTRY_PAGE_PLAYER_IFRAME1                              = ('class_name','mwEmbedKalturaIframe')
    ENTRY_PAGE_PLAYER_IFRAME2                              = ('id','kplayer_ifp')
    ENTRY_PAGE_CHAPTER_MENU_ON_THE_PLAYER                  = ('id', 'sideBarContainerReminderContainer') # This is the icon on the top left of the player that show all the slides that were added 
    ENTRY_PAGE_SHARE_TAB                                   = ('xpath', '//a[@id="tab-share-tab" and @class="btn responsiveSizePhone tab-share-tab"]')
    ENTRY_PAGE_SHARE_LINK_TO_MEDIA_OPTION                  = ('xpath', '//li[@id="directLink-tab" and @class="active"]')
    ENTRY_PAGE_SHARE_EMBED_OPTION                          = ('id', 'embedTextArea-pane-tab')
    ENTRY_PAGE_SHARE_EMAIL_OPTION                          = ('id', 'emailLink-tab')
    ENTRY_PAGE_LOADING                                     = ('xpath', '//div[@class="message" and text()="Loading..."]')
    ENTRY_PAGE_EMBED_TEXT_AREA                             = ('id', 'embedTextArea') 
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
        if self.wait_visible(tmp_entry_name, 30) == False:
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
    
    
    # @Author: Inbar Willman
    def navigateToEntryPageFromMyHistory(self, entryName):
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True      
        
        self.clsCommon.myHistory.searchEntryMyHistory(entryName)
        self.clsCommon.myHistory.clickEntryAfterSearchInMyHistory(entryName)
        # Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
        
        return True 
    
    
    # @Author: Inbar Willman
    # Click on entry from home page playlist
    def navigateToEntryPageFromHomePage(self, entryName):
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True 
        
        tmp_home_entry_name = (self.clsCommon.home.HOME_PLAYLIST_ENTRY[0], self.clsCommon.home.HOME_PLAYLIST_ENTRY[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_home_entry_name) == False:
            writeToLog("INFO","FAILED to click on entry")
            return False
        
        if self.wait_visible(tmp_entry_name, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
     
        
    # Author: Michal Zomper     
    def verifyEntryMetadata(self, entryName, entryDescription, entryTags):
        # Verify entry name
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        # Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 20) == False:
            writeToLog("INFO","FAILED to verify entry name: '" + entryName + "'")
            return False     
        
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
            return False   
        
        writeToLog("INFO","Success, all entry '" + entryName + "' metadata are correct")
        return True  
    
    
    
    def navigateToEntry(self, entryName="", navigateFrom = enums.Location.MY_MEDIA, categoryName ="", channelName= ""):
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
            
        elif navigateFrom == enums.Location.UPLOAD_PAGE:
            if self.clsCommon.upload.click(self.clsCommon.upload.UPLOAD_GO_TO_MEDIA_BUTTON) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + enums.Location.UPLOAD_PAGE)
                return False  
            
        elif navigateFrom == enums.Location.MY_HISTORY:
            if self.navigateToEntryPageFromMyHistory(entryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + enums.Location.MY_HISTORY)
                return False   
                
        elif navigateFrom == enums.Location.HOME:
            if self.navigateToEntryPageFromHomePage(entryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + enums.Location.MY_HISTORY)
                return False               
        sleep(2)
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
        
        sleep(2)
        if self.click(self.ENTRY_PAGE_CONFIRM_DELETE_BUTTON, 20, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click confirm delete button")
            # Click on the actions button to close the drop down list 
            self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_DELETE_BUTTON, 15)
            return False
        
        sleep(5)
        # Verify entry was delete: after entry delete the page that will display is the page that we enter the entry from
        if deleteFrom == enums.Location.MY_MEDIA or deleteFrom == enums.Location.ENTRY_PAGE:
            sleep(5)
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 30) == False:
                writeToLog("INFO","FAILED to verify that entry deleted")
                return False   
                
        elif deleteFrom == enums.Location.CATEGORY_PAGE:
            tmpCategoryName = (self.clsCommon.category.CATEGORY_TITLE_IN_CATEGORY_PAGE[0], self.clsCommon.category.CATEGORY_TITLE_IN_CATEGORY_PAGE[1].replace('CATEGORY_NAME', categoryName))
            if self.wait_visible(tmpCategoryName, 30) == False:
                writeToLog("INFO","FAILED to verify that entry deleted")
                return False
        
        elif deleteFrom == enums.Location.CHANNEL_PAGE:
            tmp_channel_title = (self.clsCommon.channel.CHANNEL_PAGE_TITLE[0], self.clsCommon.channel.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
            if self.wait_visible(tmp_channel_title, 30) == False:
                writeToLog("INFO","FAILED to verify that entry deleted")
                return False

        writeToLog("INFO","Verify that entry deleted")
        return True
        
        
#   TODO:not finished
    def downloadAFlavor(self, entryName, flavorName):
        try:                
            if self.navigateToEntryPageFromMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to navigate to entry page, Entry name: " + entryName)
                return False
            
            if self.click(self.ENTRY_PAGE_DOWNLOAD_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on download tab")
                return False
            
            sleep(2)
            
            asteriskElement = self.driver.find_element_by_xpath(".//tr[@class='download_flavors_item' and contains(text(), " + flavorName + ")]")
            parentAsteriskElement = asteriskElement.find_element_by_xpath("..")
            downloadbutton = parentAsteriskElement.find_element_by_tag_name("a")
            downloadbutton.click()


        except NoSuchElementException:
            writeToLog("INFO","FAILED to click on download button, that located near: " + flavorName)
            return False
        return True        
    
    
    def waitTillMediaIsBeingProcessed(self, timeout=150):
        sleep(3)
        self.wait_while_not_visible(self.ENTRY_PAGE_MEDIA_IS_BEING_PROCESSED, timeout)
        if self.wait_visible(self.clsCommon.player.PLAYER_IFRAME, 60) == False:
            return False
        return True

      
    def VerifySlidesonThePlayerInEntryPage(self, entryName):
        if self.navigateToEntry(entryName, navigateFrom = enums.Location.MY_MEDIA) == False:
            writeToLog("INFO","FAILED navigate to entry: " + entryName)
            return False
        
        el = self.get_element(self.ENTRY_PAGE_PLAYER_IFRAME)
        self.driver.switch_to.frame(el)
        ch = self.driver.get_child_element(el, "//div[@id='sideBarContainerReminderContainer']")
        
        # Verify chapter menu display on the player
        if self.is_visible(self.ENTRY_PAGE_CHAPTER_MENU_ON_THE_PLAYER) == False:
            writeToLog("INFO","FAILED to find chapter menu on the player")
            return False


    # @Author: Inbar Willman    
    def clickOnShareTab(self):
        if self.click(self.ENTRY_PAGE_SHARE_TAB, 30) == False:
            writeToLog("INFO","FAILED to click on download tab")
            return False
    
    
    # @Author: Inbar Willman     
    def chooseShareOption(self, shareOption = enums.EntryPageShareOptions.EMBED):
        if shareOption == enums.EntryPageShareOptions.EMBED:
            embed_tab = self.get_elements(self.ENTRY_PAGE_SHARE_EMBED_OPTION)[1]
            if embed_tab.click() == False:
                writeToLog("INFO","FAILED to click on embed tab option")
                return False
        elif shareOption == enums.EntryPageShareOptions.LINK_TO_MEDIA_PAGE:
            if self.click(self.ENTRY_PAGE_SHARE_LINK_TO_MEDIA_OPTION) == False:
                writeToLog("INFO","FAILED to click on link to media tab option")
                return False            
        elif shareOption == enums.EntryPageShareOptions.EMAIL:
            email_tab = self.get_elements(self.ENTRY_PAGE_SHARE_EMAIL_OPTION)[1]
            if email_tab.click() == False:
                writeToLog("INFO","FAILED to click on link to media tab option")
                return False             
        else:
            writeToLog("INFO","FAILED to get valid share option")
            return False   
        
        return True       
    
    
    def getEmbedLink(self):
        if self.clickOnShareTab() == False:
            writeToLog("INFO","FAILED to click on share tab")
            return False  
        if self.chooseShareOption() == False:
            writeToLog("INFO","FAILED to click on embed tab")
            return False    
        if self.wait_while_not_visible(self.ENTRY_PAGE_LOADING) == False:
            writeToLog("INFO","FAILED - Loading message is still displayed")
            return False   
        embed_text = self.get_element_text(self.ENTRY_PAGE_EMBED_TEXT_AREA)
        return embed_text