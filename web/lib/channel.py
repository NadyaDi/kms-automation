from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from base import *
import clsTestService
import enums
from general import General


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
    CHANNEL_REMOVE_TAG_MASK                         = ('xpath', "//div[@id='select2-drop-mask']")
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
    MY_CHANNELS_SERACH_FIELD                        = ('xpath', "//input[@id='searchBar']")
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
    CHANNEL_ADD_TO_CHANNEL_BUTTON                   = ('xpath', "//a[@id='tab-addcontent']")
    CHANNEL_LOADING_MSG                             = ('xpath', "//div[contains(.,'Loading')]")
    CHANNEL_PUBLISH_BUTTON                          = ('xpath', "//a[contains(@class,'btn tight btn-primary addMedia')]")
    CHANNEL_MODARATE_PUBLISH_MSG                    = ('xpath', "//div[text() ='All media was published successfully. Note that your media will not be listed until a moderator approves it.']")
    CHANNEL_PUBLISH_MSG                             = ('xpath', "//div[text() ='All media was published successfully. ']")
    CHANNEL_MODERATION_TAB                          = ('id', 'channelmoderation-tab')
    CHANNEL_ENTRY_IN_PENDING_TAB_PARENT             = ('xpath', "//a[contains(@href, '/media/') and contains(text(), 'ENTRY_NAME')]") 
    CHANNEL_REJECT_BUTTON                           = ('xpath', "//button[contains(@id,'reject_btn_ENTRY_ID')]")
    CHANNEL_APPROVE_BUTTON                          = ('xpath', "//button[contains(@id,'accept_btn_ENTRY_ID')]")
    CHANNEL_ADD_MEDIA_TO_CHANNEL_PLAYLIST           = ('xpath', "//span[@class='searchme' and text() ='ENTRY_NAME']/ancestor::div[@class='fullsize']")
    CHANNEL_ADD_MEDIA_BUTTON                        = ('xpath', "//a[@class='playlist-entry-select action' and @title='Add to Playlist']")
    CHANNEL_SEARCH_BUTTON_CHANNEL_PLAYLIST          = ('xpath', "//form[@id='navbar-search' and @class= 'navbar-search']")
    CHANNEL_SEARCH_BUTTON_FIELD                     = ('xpath', "//input[@id='searchBar' and @placeholder= 'Search Media']")
    CHANNEL_SAVE_PLAYLIST_BUTTON                    = ('xpath', "//a[@class='btn btn-primary' and contains(text(),'Save')]")
    CHANNEL_CHANNEL_PLAYLIST_SAVED_MASSAGE          = ('xpath', "//div[@class='alert alert-success ']")  
    CHANNEL_PLAYLIST_DELETE_CONFIRMATION            = ('xpath', "//a[@class='btn btn-danger' and contains(text(),'Delete')]")
    CHANNEL_PLAYLIST_NAME_COLUMN                    = ('xpath', "//p[@class='playlistNameColumn' and text()= 'PLYLIST_TITLE']")
    CHANNEL_PLAYLIST_DELETE_ICON_TABLE              = ('xpath', "//a[@onclick=\"channelPlaylistsjs.deletePlaylist('PLAYLIST_ID')\"]")   
    CHANNEL_MEMBERS_TAB                             = ('xpath', '//a[@id="channelmembers-tab"]')  
    CHANNEL_ADD_MEMBER_BUTTON                       = ('xpath', '//a[@id="addmember"]') 
    CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD         = ('xpath', '//input[@id="addChannelMember-userId"]')   
    CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION         = ('xpath', '//select[@id="addChannelMember-permission"]')     
    CHANNEL_ADD_MEMBER_MODAL_ADD_BUTTON             = ('xpath', '//a[@data-handler="1" and @class="btn btn-primary" and text()="Add"]')   
    CHANNEL_ADD_MEMBER_MODAL_CONTENT                = ('xpath', '//p[@class="help-block" and contains(text(),"Please input at least 3")]')
    CHANNEL_SET_MEMBER_PERMISSION                   = ('xpath', '//option[@value="3" and text()="Member"]')        
    CHANNEL_SET_CONTRIBUTOR_PERMISSION              = ('xpath', '//option[@value="2" and text()="Contributor"]') 
    CHANNEL_SET_MODERATOR_PERMISSION                = ('xpath', '//option[@value="1" and text()="Moderator"]')
    CHANNEL_SET_MANAGER_PERMISSION                  = ('xpath', '//option[@value="0" and text()="Manager"]')      
    CHANNEL_MEMBERS_TAB_CONTENT                     = ('xpath', '//div[@id="channelmembers-pane"]') 
    CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW              = ('xpath', '//div[@class="row-fluid memberRow" and @data-id="MEMBER"]')      
    CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON          = ('xpath', '//a[contains(@class, "editMemberBtn") and contains(@href,"MEMBER")]') 
    CHANNEL_MEMBERS_TAB_SET_AS_OWNER_BUTTON         = ('xpath', '//a[@class="setOwnerBtn " and contains(@href,"MEMBER")]')
    CHANNEL_MEMBERS_TAB_DELETE_MEMBER_BUTTON        = ('xpath', '//a[@class="deleteMemberBtn " and contains(@href,"MEMBER")]') 
    CHANNEL_YES_MODAL_BUTTON                        = ('xpath', '//a[@data-handler="1" and @class="btn btn-danger" and text()="Yes"]')    
    CHANNEL_REMOVE_USER_MODAL_CONTENT               = ('xpath', '//div[@class="modal-body" and text()="Remove private as a member of this channel?"]')    
    CHANNEL_SET_OWNER_MODAL_CONTENT                 = ('xpath', '//div[@class="modal-body" and contains(text(),"only one owner can be assigned")]')        
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
    
    #  @Author: Tzachi Guetta        
    def navigateToChannels(self):
        # Check if we are already in my Channels page
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_CHANNELS_URL, False, 3) == True:
            writeToLog("INFO","Already in my Channels page")
            return True     
        
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_CHANNELS_URL) == False:
            writeToLog("INFO","FAILED to navigate to Channels")
            return False
        
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_CHANNELS_URL, False) == False:
            writeToLog("INFO","FAILED to navigate to Channels")
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
        
        if(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
            temp = self.get_element(self.CHANNEL_REMOVE_TAG_MASK)
            self.driver.execute_script("arguments[0].setAttribute('style','display: none;')",(temp))
        
            if tagsElement.click() == False:
                writeToLog("DEBUG","FAILED to click on Tags filed")
                return False                
            
        if self.send_keys(self.clsCommon.upload.UPLOAD_ENTRY_DETAILS_ENTRY_TAGS_INPUT, tags) == True:
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
    
    # Author: Tzachi Guetta
    def searchAChannelInMyChannels(self, channelName):
        try:                
            if self.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED to navigate to my channels page")
                return False
            
            if self.click(self.MY_CHANNELS_SERACH_FIELD, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
            
            if self.send_keys(self.MY_CHANNELS_SERACH_FIELD, channelName, multipleElements=True) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
            
        except NoSuchElementException:
            return False
        
        return True
    

    #  @Author: Tzachi Guetta  
    def searchAChannelInChannels(self, channelName):
        try:                
            if self.navigateToChannels() == False:
                writeToLog("INFO","FAILED to navigate to my channels page")
                return False
            
            if self.click(self.MY_CHANNELS_SERACH_FIELD, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
            
            if self.send_keys(self.MY_CHANNELS_SERACH_FIELD, channelName, multipleElements=True) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
            
        except NoSuchElementException:
            return False
        
        return True
    
    
    #  @Author: Tzachi Guetta  
    def navigateToChannel(self, channelName, navigateFrom=enums.Location.MY_CHANNELS_PAGE):
        try:                
            if navigateFrom == enums.Location.MY_CHANNELS_PAGE:
                if self.searchAChannelInMyChannels(channelName) == False:
                    writeToLog("INFO","FAILED to search in my channels")
                    return False
            elif navigateFrom == enums.Location.CHANNELS_PAGE:
                if self.searchAChannelInChannels(channelName) == False:
                    writeToLog("INFO","FAILED to search in channels")
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
    
    #  Author: Tzachi Guetta
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
            
    #  Author: Elad
    #  Description:Verify multi entries in channel
    def verifyIfMultipleEntriesInChannel(self, channelName, entriesList, isExpected=True):
        try:                
            for entry in entriesList:
                if self.verifyIfSingleEntryInChannel(channelName, entry, isExpected=True) == False:
                    writeToLog("INFO","FAILED to verify entry on channel " + entry)
                    return False    
        except NoSuchElementException:
            if isExpected == False:
                writeToLog("INFO","NOT Expected: Entry wasn't found in the channel as expected")
                return True
            else:
                writeToLog("INFO","NOT Expected: Entry wasn't found in the channel")
                return False
            
        return True
    
    
    #@Author: Elad Binyamin 
    #Description:Import entries channel to another channel
    def importChannel(self, channelNameFrom, channelNameTo, entriesList, toVerify=False):
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
            
            if toVerify == True:
                if self.verifyIfMultipleEntriesInChannel(channelNameTo, entriesList, isExpected = True) == False:
                    writeToLog("INFO","FAILED to verify entries on channel ")
                    return False
             
        except NoSuchElementException:
            return False
        
        return True    

            
    def naviagteToEntryFromChannelPage(self, entryName, channelName):
        # Check if we are already in channel page
        tmp_channel_title = (self.CHANNEL_PAGE_TITLE[0], self.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
        if self.wait_visible(tmp_channel_title, 5) != False:
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

      
   
    #@Author: Oded Berihon     
    def createChannelPlaylist(self, channelName, playlisTitle, playlistDescription, playlistTag, entriesNames, SortBy='', MediaType='',): 
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
         
        if self.sortAndFilterInChannelPlaylist(SortBy ,MediaType)== False:
            writeToLog("INFO","FAILED to click on search button")
            return False  
        
        if self.click(self.CHANNEL_SEARCH_BUTTON_CHANNEL_PLAYLIST) == False:
            writeToLog("INFO","FAILED to click on search button")
            return False   

        if self.click(self.CHANNEL_SEARCH_BUTTON_FIELD) == False:
            writeToLog("INFO","FAILED to click on search field")
            return False  
        sleep(1)
        
        if len (entriesNames)!= 0:
            for entryName in entriesNames:
                if self.send_keys(self.CHANNEL_SEARCH_BUTTON_FIELD, Keys.CONTROL + 'a') == False:
                    writeToLog("INFO","FAILED to enter entry name  :'" + entryName + "'")
                    return False        
                        
                if self.send_keys(self.CHANNEL_SEARCH_BUTTON_FIELD, entryName + Keys.ENTER) == False:
                    writeToLog("INFO","FAILED to enter entry name  :'" + entryName + "'")
                    return False
                
                # Wait for loader to disappear
                self.clsCommon.general.waitForLoaderToDisappear()
                
                if self.click(self.CHANNEL_ADD_MEDIA_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on add button")
                    return False             
                sleep(1)   
            
        if self.click(self.CHANNEL_SAVE_PLAYLIST_BUTTON) == False:
            writeToLog("INFO","FAILED to click on save")
            return False             
 
        el = self.get_element(self.CHANNEL_CHANNEL_PLAYLIST_SAVED_MASSAGE)
        if not playlisTitle in el.text:
            writeToLog("INFO","FAILED to LOCATE SUCCESS MASSAGE")
            return False
                                         
        return True
    

    def sortAndFilterInChannelPlaylist(self, sortBy='', mediaType=''):
        if sortBy != '':
            if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.SORT_BY, sortBy) == False:
                writeToLog("INFO","FAILED to set sortBy: " + str(sortBy) + " in my media")
                return False

        if mediaType != '':
            if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, mediaType) == False:
                writeToLog("INFO","FAILED to set filter: " + str(mediaType) + " in my media")
                return False
            
        return True
    
    
    #@Author: Oded Berihon   
    def deleteChannelPlaylist(self, channelName, playlisTitle):
        if self.navigateToChannelPlaylistTab(channelName) == False:
            writeToLog("INFO","FAILED to go to channel-playlist tab button: '" + channelName + "'" )
            return False 
        
        templocator = (self.CHANNEL_PLAYLIST_NAME_COLUMN[0], self.CHANNEL_PLAYLIST_NAME_COLUMN[1].replace('PLYLIST_TITLE', playlisTitle))        
        playlistId = self.wait_visible(templocator).find_element_by_xpath("../..").get_attribute("data-playlistid")
        templocator = (self.CHANNEL_PLAYLIST_DELETE_ICON_TABLE[0], self.CHANNEL_PLAYLIST_DELETE_ICON_TABLE[1].replace('PLAYLIST_ID', playlistId))
                            
        if self.click(templocator) == False:
            writeToLog("INFO","FAILED to Click on delete button: '" + playlisTitle + "'")
            return False
        
        sleep(2)
        if self.click(self.CHANNEL_PLAYLIST_DELETE_CONFIRMATION, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on delete button")
            return False  
        
        el = self.wait_visible(self.CHANNEL_CHANNEL_PLAYLIST_SAVED_MASSAGE, 45)
        if not "The playlist " + playlisTitle + " was deleted successfully" in el.text:
            writeToLog("INFO","FAILED to LOCATE Deleted MASSAGE")
            return False
            
        return True 

    
    #  @Author: Tzachi Guetta    
    def addContentToChannel(self, channelName, entriesNames, isChannelModerate, publishFrom=enums.Location.MY_CHANNELS_PAGE):
        try:                
            if self.navigateToChannel(channelName, publishFrom) == False:
                writeToLog("INFO","FAILED to navigate to  channel: " +  channelName)
                return False
            
            if self.click(self.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
                writeToLog("INFO","FAILED to click add to channel button")
                return False           
            
            sleep(1)
            self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
            
            # Checking if entriesNames list type
            if type(entriesNames) is list: 
                for entryName in entriesNames: 
                    if self.clsCommon.myMedia.checkSingleEntryInMyMedia(entryName) == False:
                        writeToLog("INFO","FAILED to CHECK the entry: " + entryName + ", At add content -> my media flow")
                        return False
                    
                    writeToLog("INFO","Going to publish Entry: " + entryName + " to: " + channelName)
            else:
                if self.clsCommon.myMedia.checkSingleEntryInMyMedia(entriesNames) == False:
                        writeToLog("INFO","FAILED to CHECK the entry: " + entriesNames + ", At add content -> my media flow")
                        return False
                    
                writeToLog("INFO","Going to publish Entry: " + entriesNames + " to: " + channelName)
                
            if self.click(self.CHANNEL_PUBLISH_BUTTON) == False:
                writeToLog("INFO","FAILED to CHECK the entry: " + entriesNames + ", At add content -> my media flow")
                return False             
            
            sleep(1)
            self.clsCommon.general.waitForLoaderToDisappear()
            
            published = False
            
            if isChannelModerate == True:
                if self.wait_visible(self.CHANNEL_MODARATE_PUBLISH_MSG, 30) != False:
                    published = True
            else:
                if self.wait_visible(self.CHANNEL_PUBLISH_MSG, 30) != False:
                    published = True
            
            if published == True:
                if type(entriesNames) is list: 
                    entries = ", ".join(entriesNames)
                    writeToLog("INFO","The following entries were published: " + entries + "")
                else:
                    writeToLog("INFO","The following entry was published: " + entriesNames + "")
            else:
                if isChannelModerate == True:
                    writeToLog("INFO","Publish to channel: confirmation massage was not presented")
                    return False
                else:
                    writeToLog("INFO","Publish to moderate channel: confirmation massage was not presented")
                    return False
            
        except NoSuchElementException:
            return False
        
        return True
    
    
    #   @Author: Tzachi Guetta    
    def handlePendingEntriesInChannel(self, channelName, toRejectEntriesNames, toApproveEntriesNames , navigate=True):
        try:                
            if navigate == True:
                if self.navigateToChannel(channelName) == False:
                    writeToLog("INFO","FAILED to navigate to  channel: " +  channelName)
                    return False
                
                if self.click(self.CHANNEL_MODERATION_TAB, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on channel's moderation tab")
                    return False        
            
            sleep(1)
            self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30) 
            
            if type(toRejectEntriesNames) is list:
                for rejectEntry in toRejectEntriesNames:
                    self.method_helper_rejectEntry(rejectEntry)
            else:
                self.method_helper_rejectEntry(toRejectEntriesNames)                
                
            
            if type(toApproveEntriesNames) is list:
                for approveEntry in toApproveEntriesNames:
                    self.method_helper_approveEntry(approveEntry)
                    
            else:
                self.method_helper_approveEntry(toApproveEntriesNames)
        
        except NoSuchElementException:
            return False
        
        return True
    
    
    # Author: Tzachi Guetta     
    def method_helper_rejectEntry(self, rejectEntry):
        tmpEntry = (self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[0], self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[1].replace('ENTRY_NAME', rejectEntry))
        entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
        tmpRejectBtn = (self.CHANNEL_REJECT_BUTTON[0], self.CHANNEL_REJECT_BUTTON[1].replace('ENTRY_ID', entryId))
        if self.click(tmpRejectBtn) == False:
            writeToLog("INFO","FAILED to reject entry: " + rejectEntry)
            return False 
        writeToLog("INFO","The following entry was rejected : " + rejectEntry)  
        
        
    # Author: Tzachi Guetta     
    def method_helper_approveEntry(self, approveEntry):
        tmpEntry = (self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[0], self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[1].replace('ENTRY_NAME', approveEntry))
        entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
        tmpApproveBtn = (self.CHANNEL_APPROVE_BUTTON[0], self.CHANNEL_APPROVE_BUTTON[1].replace('ENTRY_ID', entryId))
        if self.click(tmpApproveBtn) == False:
            writeToLog("INFO","FAILED to approve entry: " + approveEntry)
            return False                    
        
        writeToLog("INFO","The following entry was approved : " + approveEntry)
        
        
        # Author: Tzachi Guetta 
    def sortAndFilterInPendingTab(self, sortBy='', filterMediaType='', channelName='', navigate = True, location = enums.Location.CHANNEL_PAGE):
        try:         
            if navigate == True:
                if location == enums.Location.CHANNEL_PAGE:
                    if self.navigateToChannel(channelName) == False:
                        writeToLog("INFO","FAILED to navigate to  channel: " +  channelName)
                        return False
                    
                    if self.click(self.CHANNEL_MODERATION_TAB, multipleElements=True) == False:
                        writeToLog("INFO","FAILED to click on channel's moderation tab")
                        return False
                    
                elif location == enums.Location.CATEGORY_PAGE:
                    if self.clsCommon.category.navigateToCategory(channelName) == False:
                        writeToLog("INFO","FAILED to navigate to  category: " +  channelName)
                        return False
                    
                    if self.click(self.clsCommon.category.CATEGORY_PENDING_TAB, multipleElements=True) == False:
                        writeToLog("INFO","FAILED to click on category's moderation tab")
                        return False     
            sleep(2)
            
            if sortBy != '':
                if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.SORT_BY, sortBy) == False:
                    writeToLog("INFO","FAILED to set sortBy: " + str(sortBy) + " in my media")
                    return False
                
            if filterMediaType != '':
                if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, filterMediaType) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterMediaType) + " in my media")
                    return False                                                   
        
        except NoSuchElementException:
            return False
    
        return True      
  
    
    # @Author: Inbar Willman
    # Go to members tab in edit channel page
    def navigateToMembersTab(self):
        if self.click(self.CHANNEL_MEMBERS_TAB) == False:
            writeToLog("INFO","Failed to click on members tab")
            return False     
        return True
    
    
    # @Author: Inbar Willman 
    def addMembersToChannel(self, username, permission = enums.ChannelMemberPermission.MEMBER):
        # Navigate to members tab
        if self.navigateToMembersTab() == False:
            writeToLog("INFO","Failed to click on members tab")
            return False  
        
        # Wait until page contains add member button
        if self.wait_visible(self.CHANNEL_ADD_MEMBER_BUTTON) == False:
            writeToLog("INFO","Failed to display add member tab content")
            return False           
        
        # Click on add member button
        if self.click(self.CHANNEL_ADD_MEMBER_BUTTON) == False:
            writeToLog("INFO","Failed to click on add members button")
            return False   
        
        # Wait until add member modal is displayed
        sleep(3)
        
        #Click on username field
        if self.click(self.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD) == False:
            writeToLog("INFO","Failed to click on username field")
            return False             
                    
        # Insert username to field
        if self.send_keys(self.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, username) == False:
            writeToLog("INFO","Failed to insert username")
            return False 
        
        # Set permission
        if self.chooseMemberPermissionInChannel(permission) == False:
            writeToLog("INFO","Failed to set permission")
            return False   
        
        #Click add button
        if self.click(self.CHANNEL_ADD_MEMBER_MODAL_ADD_BUTTON) == False:
            writeToLog("INFO","Failed to click on add button")
            return False  
        
        # Wait until add member modal isn't displayed
        if self.wait_while_not_visible(self.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, timeout=80) == False:
            writeToLog("INFO","Failed to display add member modal")
            return False    
        
        #Verify new member is added to member table
        tmp_member_row = (self.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[0], self.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[1].replace('MEMBER', username))
        if self.is_visible(tmp_member_row) == False:
            writeToLog("INFO","Failed to add new member to table")
            return False  
        
        return True                                         
                           
                                
    # @Author: Inbar Willman 
    # Choose permission from drop down list
    def chooseMemberPermissionInChannel(self, permission = enums.ChannelMemberPermission.MEMBER):    
        # If permission is member click on member option       
        if permission ==  enums.ChannelMemberPermission.MEMBER:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION, 'Member') == False:
                writeToLog("INFO","Failed to click on member option")
                return False                    
       
        # If permission is contributor click on member option       
        elif permission ==  enums.ChannelMemberPermission.CONTRIBUTOR:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION, 'Contributor') == False:
                writeToLog("INFO","Failed to click on contributor option")
                return False  
            
        # If permission is moderator click on member option       
        elif permission ==  enums.ChannelMemberPermission.MODERATOR:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION, 'Moderator') == False:
                writeToLog("INFO","Failed to click on moderator option")
                return False 
        
        # If permission is manager click on member option       
        elif permission ==  enums.ChannelMemberPermission.MANAGER:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION, 'Manager') == False:
                writeToLog("INFO","Failed to click on manager option")
                return False   
            
        return True    
    
    
    # @Author: Inbar Willman
    # Edit member permission
    def editChannlMemberPermission(self,username, permission = enums.ChannelMemberPermission.MODERATOR): 
        #Click on edit button
        tmp_edit_button = (self.CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON[0], self.CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON[1].replace('MEMBER', username))
        if self.hover_on_element(tmp_edit_button) == False:
            writeToLog("INFO","FAILED to Hover above edit member button")
            return False
        
        if self.click(tmp_edit_button) == False:
                writeToLog("INFO","Failed to click on edit button")
                return False               
                         
        # Set new permission
        if self.chooseMemberPermissionInChannel(permission) == False:
            writeToLog("INFO","Failed to set new permission")
            return False   
        
        # Save new permission
        if self.click(tmp_edit_button) == False:
                writeToLog("INFO","Failed to click on save button")
                return False                  
        
        return True
  
    
    # @Author: Inbar Willman
    # Delete member from channel
    def deleteChannlMember(self,username): 
        #Click on delete button
        tmp_delete_btn = (self.CHANNEL_MEMBERS_TAB_DELETE_MEMBER_BUTTON[0], self.CHANNEL_MEMBERS_TAB_DELETE_MEMBER_BUTTON[1].replace('MEMBER', username))
        if self.hover_on_element(tmp_delete_btn) == False:
            writeToLog("INFO","FAILED to Hover above delete member button")
            return False
                
        if self.click(tmp_delete_btn) == False:
                writeToLog("INFO","Failed to click on delete button")
                return False 
            
        # Wait until modal is displayed
        sleep(3)              
   
        # Click on 'Yes' in remove user modal
        if self.click(self.CHANNEL_YES_MODAL_BUTTON) == False:
                writeToLog("INFO","Failed to click on yes button")
                return False  
        
        # Wait until remove modal isn't displayed
        if self.wait_while_not_visible(self.CHANNEL_REMOVE_USER_MODAL_CONTENT,timeout=30) == False:
            writeToLog("INFO","Failed to wait until remove modal isn't visible")
            return False  
        
        sleep (2)
            
        # Verify user isn't displayed in members table
        tmp_member_row = (self.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[0], self.CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW[1].replace('MEMBER', username))
        if self.is_visible(tmp_member_row) == True:
            writeToLog("INFO","Failed to delete member - user still displayed in member table")
            return False  
        
        return True   
    
    
    # Author: Inbar Willman
    # Set channel member as owner
    def setChannelMemberAsOwner(self, username):
        # Click on set as owner button
        tmp_set_as_owner = (self.CHANNEL_MEMBERS_TAB_SET_AS_OWNER_BUTTON[0], self.CHANNEL_MEMBERS_TAB_SET_AS_OWNER_BUTTON[1].replace("MEMBER", username)) 
        if self.hover_on_element(tmp_set_as_owner) == False:
            writeToLog("INFO","FAILED to Hover above set as owner button")
            return False
                
        if self.click(tmp_set_as_owner) == False:
            writeToLog("INFO","Failed to click on set as owner button")
            return False 
        
        # Wait until set owner modal is displayed
        sleep(3)
        
        # Click on 'Yes' in set owner modal
        if self.click(self.CHANNEL_YES_MODAL_BUTTON) == False:
            writeToLog("INFO","Failed to click on yes button")
            return False  
        
        # Wait until set owner modal isn't visible anymore
        if self.wait_while_not_visible(self.CHANNEL_SET_OWNER_MODAL_CONTENT, timeout=30) == False:
            writeToLog("INFO","Failed to wait until set owner modal isn't visible")
            return False              
         
        #Verify that user don't have set as owner button
        if self.hover_on_element(tmp_set_as_owner) == True:
            writeToLog("INFO","Failed to set user as owner - set as owner button still displayed")
            return False  
        
        return True