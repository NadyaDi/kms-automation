from base import *
import clsTestService
from general import General
import enums
from selenium.webdriver.common.action_chains import ActionChains



class Channel(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #                                   Channel locators:                                                        #
    #=============================================================================================================
    MY_CHANNELS_CREATE_CHANNEL_BUTTON               = ('id', 'createChannelBtn')
    CHANNEL_DETAILS_NAME_FIELD                      = ('id', 'Category-name')
    CHANNEL_DETAILS_CHANNEL_TAGS                    = ('id', 's2id_tags')
    CHANNEL_DETAILS_PRIVACY_OPEN                    = ('xpath', "//strong[contains(text(),'Open')]")
    CHANNEL_DETAILS_PRIVACY_RESTRICTED              = ('xpath', "//strong[contains(text(),'Restricted')]")
    CHANNEL_DETAILS_PRIVACY_PRIVATE                 = ('xpath', "//strong[contains(text(),'Private')]")
    CHANNEL_DETAILS_PRIVACY_SHARED_REPOSITORY       = ('xpath', "//strong[contains(text(),'Shared Repository')]")
    CHANNEL_DETAILS_PRIVACY_PUBLIC                  = ('xpath', "//strong[contains(text(),'Public')]")
    CHANNEL_DETAILS_OPTION_MODARATE                 = ('id', 'Category-options-moderation')
    CHANNEL_DETAILS_OPTION_COMMENT                  = ('id', 'Category-options-enableComments')
    CHANNEL_DETAILS_OPTION_SUBSCRIPTION             = ('id', 'Category-options-enableChannelSubscription')
    CHANNEL_SAVE_BUTTON                             = ('id', 'Category-submit')
    CHANNEL_CREATION_DONE                           = ('xpath', "//div[contains(@class,'alert alert-success') and contains(text(),'The information was saved successfully')]")
    MY_CHANNELS_SERACH_FIELD                        = ('id', 'searchBar')
    MY_CHANNELS_EDIT_BUTTON                         = ('xpath', "//a[contains(@class,'edit')]")
    MY_CHANNELS_HOVER                               = ('xpath', "//*[@class='channel_content' and contains(text(), 'CHANNEL_NAME')]")
    EDIT_CHANNEL_DELETE                             = ('xpath', "//a[@class='btn btn-danger' and contains(@href,'/channels/delete/')]")
    EDIT_CHANNEL_DELETE_CONFIRM                     = ('xpath', "//a[@class='btn btn-danger' and text()='Delete']")
    CHANNEL_PAGE_TITLE                              = ('xpath', "//h1[@id='channel_title' and contains(text(), 'CHANNEL_TITLE')]")
    CHANNEL_PAGE_SEARCH_TAB                         = ('id', 'channelSearch-tab')
    CHANNEL_PAGE_SEARCH_BAR                         = ('id', 'searchBar')
    CHANNEL_PAGE_NO_RESULT_ALERT                    = ('xpath', "//div[contains(@class,'alert alert-info') and contains(text(),'No Search Results...')]")
    CHANNEL_PAGE_ENTRY_THUMBNAIL                    = ('xpath', "//div[@class='photo-group thumb_wrapper' and contains(@title,'ENTRY_NAME')]")
    CHANNEL_DELETE_ALERT                            = ('xpath', "//div[@class='alert alert-success ']")
    CHANNEL_ACTION_BUTTON                           = ('id', 'channelActionsDropdown')
    CHANNEL_IMPORT_MENU                             = ('xpath', "//a[contains(@href,'/importchannel/') and @role='menuitem']")
    CHANNEL_IMPORT_CHANNEL                          = ('xpath', "//label[@class='radio' and text()='CHANNEL_NAME']")
    CHANNEL_IMPORT_BUTTON                           = ('xpath', "//a[@class='btn btn-primary importButton']")
    CHANNEL_IMPORT_ALERT                            = ('xpath', "//div[contains(@class,'alert alert-success') and contains(text(),'Importing completed successfully. To refresh the page and view the imported entries')]")
    CHANNEL_CLICKHERE_REFRESH_BUTTON                = ('xpath', "//a[@href='#' and text()='click here.']")
    CHANNEL_CLICK_ON_CHANNEL_AFTER_SEARCH           = ('xpath', "//p[@class='channel_content' and text()='CHANNEL_NAME']")
    CHANNEL_EDIT_DROP_DOWN_MENU                     = ('id', "channelActionsDropdown")
    CHANNEL_EDIT_BUTTON                             = ('xpath', "//i[@class='icon-wrench']")
    CHANNEL_EDIT_CHANNNEL_PAGE                      = ('xpath', "//a[contains(@href,'/channel/') and text()= 'CHANNEL_NAME']")
    CHANNEL_PLAYLISTS_TAB                           = ('id', 'channelPlaylists-tab')
    CHANNEL_CREATE_NEW_PLAYLIST_DROP_DOWN           = ('id', 'typeLabel')
    CHANNEL_MANUAL_PLAYLIST_BUTTON                  = ('xpath', "//ul[@id='typeLabelMenu']")
    CHANNEL_ENTER_PLAYLIST_TITLE                    = ('id', 'playlistTitle')
    CHANNEL_PLAYLISTS_DESCRIPTION                   = ('id', 'playlistDescription')
    CHANNEL_PLAYLISTS_TAG                           = ('id', 's2id_StaticPlaylist-tags')
    CHANNEL_PLAYLISTS_ADD_MEDIA_URL                 = ('xpath', "//a[@class='accordion-toggle collapsed' and @data-toggle= 'collapse']")
    CHANNEL_PLAYLISTS_HEADER                        = ('xpath', "//h3[ text()= 'Create a Manual Playlist']")

    #============================================================================================================
    
    #  @Author: Tzachi Guetta    
    def clickDeleteChannel(self):
        try:
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
                self.get_elements(self.EDIT_CHANNEL_DELETE)[1].click()
            else:
                self.get_elements(self.EDIT_CHANNEL_DELETE)[0].click()
            return True
        except:
            return False
        
 
    #  @Author: Tzachi Guetta        
    def deleteChannel(self, channelName):
        try:
            if self.searchAChannelInMyChannels(channelName) == False:
                writeToLog("INFO","FAILED to search in my channels")
                return False
            
            sleep(1)
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
                tmp_entry_name = (self.MY_CHANNELS_HOVER[0], self.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', channelName))
                if self.hover_on_element(tmp_entry_name) == False:
                    writeToLog("INFO","FAILED to Hover above Channel's thumbnail")
                    return False
    
            sleep(1)
            if self.click(self.MY_CHANNELS_EDIT_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Edit channel button")
                return False
            
            if self.clickDeleteChannel() == False:
                writeToLog("INFO","FAILED to click on Delete channel button (at Edit channel page)")
                return False
            sleep(2)
            
            if self.click(self.EDIT_CHANNEL_DELETE_CONFIRM) == False:
                writeToLog("INFO","FAILED to click on Delete confirmation button")
                return False
            
            # Verify delete channel confirmation
            strDeleteConf = "was deleted"
            elementdeleteconf = self.get_element(self.CHANNEL_DELETE_ALERT)
            if strDeleteConf in elementdeleteconf.text:
                writeToLog("INFO","Channel: '" + channelName + "' Was Deleted")
            else:
                writeToLog("INFO","The Alert delete Channel message was not found")
                return False 
            
        except NoSuchElementException:
            return False
        
        return True

 
    #  @Author: Tzachi Guetta
    # This function will create a Channel, please follow the following instructions:
    # in order to choose the Channel's privacy please use enums.ChannelPrivacyType
    # for isModarated, isCommnets, isSubscription - use boolean
    # TODO: handle fillFileUploadEntryDescription for both Http and https
    def createChannel(self, channelName, channelDescription, channelTags, privacyType, isModarated, isCommnets, isSubscription, linkToCategoriesList=''):
        try:
            if self.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED to native to my channels page")
                return False
            if self.click(self.MY_CHANNELS_CREATE_CHANNEL_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Create channel button")
                return False
            
            # Starting filling channel Data
            if self.click(self.CHANNEL_DETAILS_NAME_FIELD) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
            if self.send_keys(self.CHANNEL_DETAILS_NAME_FIELD, channelName) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
            if self.clsCommon.upload.fillFileUploadEntryDescription(channelDescription) == False:
                writeToLog("INFO","FAILED to type in 'description' text field")
                return False
            if self.fillChannelTags(channelTags) == False:
                writeToLog("INFO","FAILED to type in 'Tags' field")
                return False
            if self.selectChannelPrivacy(privacyType) == False:
                writeToLog("INFO","FAILED to Choose Channel privacy")
                return False
            
            # Checking Channel options
            if isModarated == True:
                if self.click(self.CHANNEL_DETAILS_OPTION_MODARATE, 30) == False:
                    writeToLog("INFO","FAILED to click on Moderate checkbox")
                    return False
 
            if isCommnets == False:
                if self.click(self.CHANNEL_DETAILS_OPTION_COMMENT, 30) == False:
                    writeToLog("INFO","FAILED to click on comments checkbox")
                    return False
                
            if isSubscription == True:
                if self.click(self.CHANNEL_DETAILS_OPTION_SUBSCRIPTION, 30) == False:
                    writeToLog("INFO","FAILED to click on subscription checkbox")
                    return False  
            
            # Click if category list is empty
            if len(linkToCategoriesList) != 0:            
                # choose all the  categories to publish to
                for category in linkToCategoriesList:
                    tmoCategoryName = (self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', category))
                    if self.click(tmoCategoryName, 30) == False:
                        writeToLog("INFO","FAILED to select published category '" + category + "'")
                        return False
            
            if self.click(self.CHANNEL_SAVE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on Save button")
                return False 
            
            if self.wait_visible(self.CHANNEL_CREATION_DONE, 45) == False:
                writeToLog("INFO","FAILED to create a Channel")
                return False                                        
            else:
                writeToLog("INFO","Channel successfully created")
                
        except NoSuchElementException:
            return False
        
        return True
        

    #  @Author: Tzachi Guetta        
    def navigateToMyChannels(self):
        # Check if we are already in my Channels page
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_CHANNELS_URL, False, 3) == True:
            writeToLog("INFO","Already in my Channels page")
            return True     
           
        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False
        
        # Click on My Channels
        if self.click(self.clsCommon.general.USER_MENU_MY_CHANNELS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on My Channels from the menu")
            return False
        
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_CHANNELS_URL, False) == False:
            writeToLog("INFO","FAILED to navigate to My Channels")
            return False
        
        return True
       
       
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillChannelTags(self, tags):
        try:
            self.switch_to_default_content()
            tagsElement = self.get_element(self.CHANNEL_DETAILS_CHANNEL_TAGS)
            
        except NoSuchElementException:
            writeToLog("DEBUG","FAILED to get Tags filed element")
            return False
                
        if tagsElement.click() == False:
            writeToLog("DEBUG","FAILED to click on Tags filed")
            return False            
        sleep(2)
        
        if self.send_keys(self.CHANNEL_DETAILS_CHANNEL_TAGS, tags) == True:
            return True
        else:
            writeToLog("DEBUG","FAILED to type in Tags")
            return False
  
    
    #  @Author: Tzachi Guetta    
    # privacy - is ChannelPrivacyType enum type
    def selectChannelPrivacy(self, privacy):
        if privacy == enums.ChannelPrivacyType.OPEN:
            if self.click(self.CHANNEL_DETAILS_PRIVACY_OPEN) == False:
                writeToLog("INFO","FAILED to click on open option")
                return False
            
        elif privacy == enums.ChannelPrivacyType.RESTRICTED:
            if self.click(self.CHANNEL_DETAILS_PRIVACY_RESTRICTED) == False:
                writeToLog("INFO","FAILED to click on restricted option")
                return False
            
        elif privacy == enums.ChannelPrivacyType.PRIVATE:
            if self.click(self.CHANNEL_DETAILS_PRIVACY_PRIVATE) == False:
                writeToLog("INFO","FAILED to click on private option")
                return False
            
        elif privacy == enums.ChannelPrivacyType.SHAREDREPOSITORY:
            if self.click(self.CHANNEL_DETAILS_PRIVACY_SHARED_REPOSITORY) == False:
                writeToLog("INFO","FAILED to click on shared-repository option")
                return False
            
        elif privacy == enums.ChannelPrivacyType.PUBLIC:
            if self.click(self.CHANNEL_DETAILS_PRIVACY_PUBLIC) == False:
                writeToLog("INFO","FAILED to click on public option")
                return False  
        else:
            writeToLog("DEBUG","FAILED to choose Channel privacy")
            return False
        
        return True
    
 
    def searchAChannelInMyChannels(self, channelName):
        try:                
            if self.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED to navigate to my channels page")
                return False
            
            if self.click(self.MY_CHANNELS_SERACH_FIELD) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
            
            if self.send_keys(self.MY_CHANNELS_SERACH_FIELD, channelName) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
            
        except NoSuchElementException:
            return False
        
        return True
    
 
    def navigateToChannel(self, channelName):
        try:                
            if self.searchAChannelInMyChannels(channelName) == False:
                writeToLog("INFO","FAILED to search in my channels")
                return False
            
            tmp_channel_name = (self.MY_CHANNELS_HOVER[0], self.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', channelName))
            if self.click(tmp_channel_name) == False:
                writeToLog("INFO","FAILED to click on Channel's thumbnail")
                return False
            
            tmp_channel_title = (self.CHANNEL_PAGE_TITLE[0], self.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
            if self.wait_visible(tmp_channel_title, 30) == False:
                writeToLog("INFO","FAILED to navigate to Channel page")
                return False

        except NoSuchElementException:
            return False
        sleep(2)
        return True
    
 
    def verifyIfSingleEntryInChannel(self, channelName, entryName, isExpected=True):
        try:                
            if self.navigateToChannel(channelName) == False:
                writeToLog("INFO","FAILED to navigate to Channel page")
                return False

            if self.click(self.CHANNEL_PAGE_SEARCH_TAB) == False:
                writeToLog("INFO","FAILED to click on Channel's search Tab")
                return False
            
            if self.click(self.CHANNEL_PAGE_SEARCH_BAR) == False:
                writeToLog("INFO","FAILED to click on Channel's search bar")
                return False
            
            if self.send_keys(self.CHANNEL_PAGE_SEARCH_BAR, entryName) == False:
                writeToLog("INFO","FAILED to type in channel search bar")
                return False
            
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_visible(self.CHANNEL_PAGE_NO_RESULT_ALERT, 5) == False:
                if isExpected == True:
                    self.get_element((self.CHANNEL_PAGE_ENTRY_THUMBNAIL[0], self.CHANNEL_PAGE_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName)))
                    writeToLog("INFO","As Expected: Entry was found in the channel")
                    return True
                else:
                    self.get_element((self.CHANNEL_PAGE_ENTRY_THUMBNAIL[0], self.CHANNEL_PAGE_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName)))
                    writeToLog("INFO","NOT Expected: Entry was found in the channel")
                    return False
            else:
                if isExpected == False:
                    writeToLog("INFO","As Expected: Entry wasn't found in the channel")
                    return True
                else:
                    writeToLog("INFO","NOT Expected: Entry wasn't found in the channel")
                    return False
                
        except NoSuchElementException:
            if isExpected == False:
                writeToLog("INFO","NOT Expected: Entry was found in the channel")
                return False
            else:
                writeToLog("INFO","NOT Expected: Entry wasn't found in the channel")
                return False
            

    #@Author: Elad Binyamin 
    #Description:Import entries channel to another channel
    def importChannel (self, channelNameFrom, channelNameTo, entryName):
        try:
            if self.navigateToChannel(channelNameTo) == False:
                writeToLog("INFO","FAILED to native to my channels page")
                return False
            
            if self.click(self.CHANNEL_ACTION_BUTTON) == False:
                writeToLog("INFO","FAILED to click on channel action button")
                return False 
            
            if self.click(self.CHANNEL_IMPORT_MENU) == False:
                writeToLog("INFO","FAILED to click on channel import menu button")
                return False 
            sleep(2)
            
            importchanneltmp = (self.CHANNEL_IMPORT_CHANNEL[0], self.CHANNEL_IMPORT_CHANNEL[1].replace('CHANNEL_NAME', channelNameFrom))
            if self.click(importchanneltmp) == False:
                writeToLog("INFO","FAILED to click on import channel option button")
                return False 
            
            if self.click(self.CHANNEL_IMPORT_BUTTON) == False:
                writeToLog("INFO","FAILED to click on import button")
                return False
            
            if self.wait_visible(self.CHANNEL_IMPORT_ALERT, 180) == False:
                writeToLog("INFO","FAILED to get the import alert message")
                return False
            
            if self.click(self.CHANNEL_CLICKHERE_REFRESH_BUTTON) == False:
                writeToLog("INFO","FAILED to click on click here ")
                return False
            sleep(3)
            
            if self.verifyIfSingleEntryInChannel(channelNameTo, entryName, isExpected=True) == False:
                writeToLog("INFO","FAILED to verify entry on channel ")
                return False
             
        except NoSuchElementException:
            return False
        
        return True    

            
    def naviagteToEntryFromChannelPage(self, entryName, channelName):
        # Check if we are already in channel page
        tmp_channel_title = (self.CHANNEL_PAGE_TITLE[0], self.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
        if self.wait_visible(tmp_channel_title, 5) == True:
            writeToLog("INFO","Success, Already in channel page")
            return True
        
        if self.navigateToChannel(channelName) == False:
            writeToLog("INFO","FAILED to navigate to Channel page '" + channelName + "'")
            return False
        
        if self.click(self.CHANNEL_PAGE_SEARCH_TAB) == False:
            writeToLog("INFO","FAILED to click on Channel's search Tab icon")
            return False
            
        if self.click(self.CHANNEL_PAGE_SEARCH_BAR) == False:
            writeToLog("INFO","FAILED to click on Channel's search bar text box")
            return False
            
        if self.send_keys(self.CHANNEL_PAGE_SEARCH_BAR, entryName) == False:
            writeToLog("INFO","FAILED to type in channel search bar")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        
        tmpEntry = self.CHANNEL_PAGE_ENTRY_THUMBNAIL[0], self.CHANNEL_PAGE_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName)
        if self.click(tmpEntry, 20, True) == False:
            writeToLog("INFO","FAILED to click on entry thumbnail")
            return False
        
        tmp_entry_name = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmp_entry_name, 20) == False:
            writeToLog("INFO","FAILED to verify entry page display")
            return False
                
        writeToLog("INFO","Success, Entry page display")
        sleep(2)
        return True


    #@Author: Oded Berihon 
    #Description:Creating channel playlist
    def navigateToEditChannelPage(self, channelName):
        if self.searchAChannelInMyChannels(channelName) == False: 
            writeToLog("INFO","FAILED to find Channel: '" + channelName + "'" )
            return False
        
        tmpChannelName = (self.CHANNEL_CLICK_ON_CHANNEL_AFTER_SEARCH[0], self.CHANNEL_CLICK_ON_CHANNEL_AFTER_SEARCH[1].replace('CHANNEL_NAME', channelName))
        if self.click(tmpChannelName) == False:
            writeToLog("INFO","FAILED to Click on Channel name: '" + channelName + "'")
            return False   
        
        if self.click(self.CHANNEL_EDIT_DROP_DOWN_MENU) == False:
            writeToLog("INFO","FAILED to Click on edit drop down menu")
            return False  
        sleep(1)
        
        if self.click(self.CHANNEL_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to Click on edit drop down menu")
            return False  
        
        tmpChannelName = (self.CHANNEL_EDIT_CHANNNEL_PAGE[0], self.CHANNEL_EDIT_CHANNNEL_PAGE[1].replace('CHANNEL_NAME', channelName))
        if self.wait_visible(tmpChannelName, 30) == False:
            writeToLog("INFO","creation didn't finish after timeout: " )
            return False
        
        return True


    #@Author: Oded Berihon     
    def navigateToChannelPlaylistTab(self, channelName):
        if self.navigateToEditChannelPage(channelName) == False:
            writeToLog("INFO","FAILED to go to channel edit page: '" + channelName + "'" )
            return False

        if self.click(self.CHANNEL_PLAYLISTS_TAB) == False:
            writeToLog("INFO","FAILED to Click on play-lists tab button")
            return False  

        return True

    #TODO NOT FINISHED
    #@Author: Oded Berihon     
    def createChannelPlaylist(self, channelName, playlisTitle, playlistDescription, playlistTag): 
        if self.navigateToChannelPlaylistTab(channelName) == False:
            writeToLog("INFO","FAILED to go to channel-playlist tab button: '" + channelName + "'" )
            return False 
        
        if self.click(self.CHANNEL_CREATE_NEW_PLAYLIST_DROP_DOWN) == False:
            writeToLog("INFO","FAILED to Click on drop down play-lists tab button")
            return False           

        if self.click(self.CHANNEL_MANUAL_PLAYLIST_BUTTON) == False:
            writeToLog("INFO","FAILED to Click on play-lists tab button")
            return False
        
        if self.wait_visible(self.CHANNEL_PLAYLISTS_HEADER) == False:
            writeToLog("INFO","FAILED to open 'Create a Manual Playlist' window")
            return False    
        sleep(3)
  
        if self.send_keys(self.CHANNEL_ENTER_PLAYLIST_TITLE, playlisTitle) == False:
            writeToLog("INFO","FAILED to fill a playlist title :'" + playlisTitle + "'")
            return False
        
        if self.send_keys(self.CHANNEL_PLAYLISTS_DESCRIPTION, playlistDescription) == False:
            writeToLog("INFO","FAILED to fill a playlistDescription title :'" + playlistDescription + "'")
            return False    
       
        if self.click(self.CHANNEL_PLAYLISTS_TAG) == False:
            writeToLog("INFO","FAILED to fill a playlisttags title :'" + playlistTag + "'")
            return False   
      
        if self.send_keys(self.CHANNEL_PLAYLISTS_TAG, playlistTag) == False:
            writeToLog("INFO","FAILED to fill a playlisttags  :'" + playlistTag + "'")
            return False     
        
        if self.click(self.CHANNEL_PLAYLISTS_ADD_MEDIA_URL) == False:
            writeToLog("INFO","FAILED to click on add media url title :'" +  + "'")
            return False  
      
        return True
    
    
    
    
     
