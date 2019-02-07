from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from base import *
import clsTestService
import enums
from general import General
from enums import Location


class Channel(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #                                   Channel locators:                                                        #
    #=============================================================================================================
    #MY_CHANNELS_CREATE_CHANNEL_BUTTON               = ('id', 'createChannelBtnGo To Channel')
    MY_CHANNELS_CREATE_CHANNEL_BUTTON                   = ('id', 'createChannelBtn')
    CHANNEL_DETAILS_NAME_FIELD                          = ('id', 'Category-name')
    CHANNEL_DETAILS_CHANNEL_TAGS                        = ('id', 's2id_tags')
    CHANNEL_REMOVE_TAG_MASK                             = ('xpath', "//div[@id='select2-drop-mask']")
    CHANNEL_DETAILS_PRIVACY_OPEN                        = ('xpath', "//strong[contains(text(),'Open')]")
    CHANNEL_DETAILS_PRIVACY_RESTRICTED                  = ('xpath', "//strong[contains(text(),'Restricted')]")
    CHANNEL_DETAILS_PRIVACY_PRIVATE                     = ('xpath', "//strong[contains(text(),'Private')]")
    CHANNEL_DETAILS_PRIVACY_SHARED_REPOSITORY           = ('xpath', "//strong[contains(text(),'Shared Repository')]")
    CHANNEL_DETAILS_PRIVACY_PUBLIC                      = ('xpath', "//strong[contains(text(),'Public')]")
    CHANNEL_DETAILS_OPTION_MODARATE                     = ('id', 'Category-options-moderation')
    CHANNEL_DETAILS_OPTION_COMMENT                      = ('id', 'Category-options-enableComments')
    CHANNEL_DETAILS_OPTION_SUBSCRIPTION                 = ('id', 'Category-options-enableChannelSubscription')
    CHANNEL_SAVE_BUTTON                                 = ('id', 'Category-submit')
    CHANNEL_CREATION_DONE                               = ('xpath', "//div[contains(@class,'alert alert-success') and contains(text(),'The information was saved successfully')]")
    MY_CHANNELS_SERACH_FIELD_OLD_UI                     = ('xpath', "//input[@id='searchBar']")
    MY_CHANNELS_SERACH_FIELD                            = ('xpath', "//input[@class='searchForm__text' and @placeholder='Search For Channels']")
    MY_CHANNELS_EDIT_BUTTON                             = ('xpath', "//a[contains(@class,'edit')]")
    MY_CHANNELS_HOVER                                   = ('xpath', "//*[@class='channel_content' and contains(text(), 'CHANNEL_NAME')]")
    EDIT_CHANNEL_DELETE                                 = ('xpath', "//a[@class='btn btn-danger' and contains(@href,'/channels/delete/')]")
    EDIT_CHANNEL_DELETE_CONFIRM                         = ('xpath', "//a[@class='btn btn-danger' and text()='Delete']")
    CHANNEL_PAGE_TITLE                                  = ('xpath', "//h1[@id='channel_title' and contains(text(), 'CHANNEL_TITLE')]")
    CHANNEL_PAGE_SEARCH_TAB                             = ('id', 'channelSearch-tab')
    CHANNEL_PAGE_SEARCH_BAR                             = ('id', 'searchBar')
    CHANNEL_PAGE_NO_RESULT_ALERT                        = ('xpath', "//div[@class='no-results_body' and contains(text(),'No Media results were found')]")
    CHANNEL_PAGE_ENTRY_THUMBNAIL                        = ('xpath', "//div[@class='photo-group thumb_wrapper' and contains(@title,'ENTRY_NAME')]")
    CHANNEL_DELETE_ALERT                                = ('xpath', "//div[@class='alert alert-success ']")
    CHANNEL_ACTION_BUTTON                               = ('id', 'channelActionsDropdown')
    CHANNEL_IMPORT_MENU                                 = ('xpath', "//a[contains(@href,'/importchannel/') and @role='menuitem']")
    CHANNEL_IMPORT_CHANNEL                              = ('xpath', "//label[@class='radio' and text()='CHANNEL_NAME']")
    CHANNEL_IMPORT_BUTTON                               = ('xpath', "//a[@class='btn btn-primary importButton']")
    CHANNEL_IMPORT_ALERT                                = ('xpath', "//div[contains(@class,'alert alert-success') and contains(text(),'Importing completed successfully. To refresh the page and view the imported entries')]")
    CHANNEL_CLICKHERE_REFRESH_BUTTON                    = ('xpath', "//a[@href='#' and text()='click here.']")
    CHANNEL_CLICK_ON_CHANNEL_AFTER_SEARCH               = ('xpath', "//p[@class='channel_content' and text()='CHANNEL_NAME']")
    CHANNEL_EDIT_DROP_DOWN_MENU                         = ('id', "channelActionsDropdown")
    CHANNEL_EDIT_BUTTON                                 = ('xpath', "//i[@class='icon-wrench']")
    CHANNEL_EDIT_CHANNNEL_PAGE                          = ('xpath', "//a[contains(@href,'/channel/') and text()= 'CHANNEL_NAME']")
    CHANNEL_PLAYLISTS_TAB                               = ('id', 'channelPlaylists-tab')
    CHANNEL_CREATE_NEW_PLAYLIST_DROP_DOWN               = ('id', 'typeLabel')
    CHANNEL_MANUAL_PLAYLIST_BUTTON                      = ('xpath', "//ul[@id='typeLabelMenu']")
    CHANNEL_ENTER_PLAYLIST_TITLE                        = ('id', 'playlistTitle')
    CHANNEL_PLAYLISTS_DESCRIPTION                       = ('id', 'playlistDescription')
    CHANNEL_PLAYLISTS_TAG                               = ('id', 's2id_StaticPlaylist-tags')
    CHANNEL_PLAYLISTS_ADD_MEDIA_URL                     = ('xpath', "//a[@class='accordion-toggle collapsed' and @data-toggle= 'collapse']")
    CHANNEL_PLAYLISTS_HEADER                            = ('xpath', "//h3[ text()= 'Create a Manual Playlist']")
    CHANNEL_ADD_TO_CHANNEL_BUTTON                       = ('xpath', "//a[@id='tab-addcontent']")
    CHANNEL_LOADING_MSG                                 = ('xpath', "//div[contains(.,'Loading')]")
    CHANNEL_PUBLISH_BUTTON                              = ('xpath', "//a[contains(@class,'btn tight btn-primary addMedia')]")
    CHANNEL_MODARATE_PUBLISH_MSG                        = ('xpath', "//div[text() ='All media was published successfully. Note that your media will not be listed until a moderator approves it.']")
    CHANNEL_PUBLISH_MSG                                 = ('xpath', "//div[text() ='All media was published successfully. ']")
    CHANNEL_MODERATION_TAB                              = ('id', 'channelmoderation-tab')
    CHANNEL_ENTRY_IN_PENDING_TAB_PARENT                 = ('xpath', "//a[contains(@href, '/media/') and contains(text(), 'ENTRY_NAME')]") 
    CHANNEL_REJECT_BUTTON                               = ('xpath', "//button[contains(@id,'reject_btn_ENTRY_ID')]")
    CHANNEL_APPROVE_BUTTON                              = ('xpath', "//button[contains(@id,'accept_btn_ENTRY_ID')]")
    CHANNEL_ADD_MEDIA_TO_CHANNEL_PLAYLIST               = ('xpath', "//span[@class='searchme' and text() ='ENTRY_NAME']/ancestor::div[@class='fullsize']")
    CHANNEL_ADD_MEDIA_BUTTON                            = ('xpath', "//a[@class='playlist-entry-select action' and @title='Add to Playlist']")
    CHANNEL_SEARCH_BUTTON_CHANNEL_PLAYLIST              = ('xpath', "//form[@id='navbar-search' and @class= 'navbar-search']")
    CHANNEL_SEARCH_BUTTON_FIELD                         = ('xpath', "//input[@id='searchBar' and @placeholder= 'Search Media']")
    CHANNEL_SAVE_PLAYLIST_BUTTON                        = ('xpath', "//a[@class='btn btn-primary' and contains(text(),'Save')]")
    CHANNEL_CHANNEL_PLAYLIST_SAVED_MASSAGE              = ('xpath', "//div[@class='alert alert-success ']")  
    CHANNEL_PLAYLIST_DELETE_CONFIRMATION                = ('xpath', "//a[@class='btn btn-danger' and contains(text(),'Delete')]")
    CHANNEL_PLAYLIST_NAME_COLUMN                        = ('xpath', "//p[@class='playlistNameColumn' and text()= 'PLYLIST_TITLE']")
    CHANNEL_PLAYLIST_DELETE_ICON_TABLE                  = ('xpath', "//a[@onclick=\"channelPlaylistsjs.deletePlaylist('PLAYLIST_ID')\"]")   
    CHANNEL_MEMBERS_TAB                                 = ('xpath', '//a[@id="channelmembers-tab"]')  
    CHANNEL_ADD_MEMBER_BUTTON                           = ('xpath', '//a[@id="addmember"]') 
#     CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD             = ('xpath', '//input[@id="addChannelMember-userId"]')
    CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD             = ('xpath', '//input[contains(@id,"react-select-")]')
    CHANNEL_ADD_MEMBER_GROUP_CONFIRMATION               = ('xpath', "//span[@class='user-selection-option__label' and contains(text(),'USERNAME')]")
    CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION_EDIT             = ('xpath', '//select[@id="addChannelMember-permission"]')
    CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION             = ('xpath', '//span[text()="PERMISSION"]')
    CHANNEL_ADD_MEMBER_MODAL_ADD_BUTTON                 = ('xpath', '//a[@data-handler="1" and @class="btn btn-primary" and text()="Add"]')   
    CHANNEL_ADD_MEMBER_MODAL_CONTENT                    = ('xpath', '//p[@class="help-block" and contains(text(),"Please input at least 3")]')
    CHANNEL_SET_MEMBER_PERMISSION                       = ('xpath', '//option[@value="3" and text()="Member"]')        
    CHANNEL_SET_CONTRIBUTOR_PERMISSION                  = ('xpath', '//option[@value="2" and text()="Contributor"]') 
    CHANNEL_SET_MODERATOR_PERMISSION                    = ('xpath', '//option[@value="1" and text()="Moderator"]')
    CHANNEL_SET_MANAGER_PERMISSION                      = ('xpath', '//option[@value="0" and text()="Manager"]')      
    CHANNEL_MEMBERS_TAB_CONTENT                         = ('xpath', '//div[@id="channelmembers-pane"]') 
    CHANNEL_MEMBERS_TAB_NEW_MEMBER_ROW                  = ('xpath', '//div[@class="row-fluid memberRow" and @data-id="MEMBER"]')      
    CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON              = ('xpath', '//a[contains(@class, "editMemberBtn") and contains(@href,"MEMBER")]') 
    CHANNEL_MEMBERS_TAB_SET_AS_OWNER_BUTTON             = ('xpath', '//a[@class="setOwnerBtn " and contains(@href,"MEMBER")]')
    CHANNEL_MEMBERS_TAB_DELETE_MEMBER_BUTTON            = ('xpath', '//a[@class="deleteMemberBtn " and contains(@href,"MEMBER")]')  
    CHANNEL_REMOVE_USER_MODAL_CONTENT                   = ('xpath', '//div[@class="modal-body" and text()="Remove private as a member of this channel?"]')    
    CHANNEL_SET_OWNER_MODAL_CONTENT                     = ('xpath', '//div[@class="modal-body" and contains(text(),"only one owner can be assigned")]')        
    CHANNEL_YES_MODAL_BUTTON                            = ('xpath', '//a[@data-handler="1" and @class="btn btn-danger" and text()="Yes"]')
    CHANNEL_SUBSCRIBE_BUTTON                            = ('xpath', "//label[@id='v2uiSubscribeSwitch' and @class='checkbox span12 toggle off']")
    CHANNEL_SUBSCRIBE_BUTTON_OLD_UI                     = ('xpath', "//span[@class='toggle-on ' and contains(text(),'Subscribed')]")    
    CHANNEL_SUBSCRIBER_COUNT                            = ('xpath', "//div[@id='Channelsubscription_persons']")
    CHANNEL_TYPE                                        = ('xpath', "//div[@id='membership']")
    CHANNEL_MEDIA_COUNT                                 = ('xpath', "//div[@id='media_persons']")
    CHANNEL_CHANNEL_INFO_OLD_UI                         = ('xpath', "//div[@id='channelSidebarInner']")
    CHANNEL_PLAYLISTS_TAG_AFTER_CLICK                   = ('xpath', "//input[contains(@id, 's2id_autogen')]")
    CHANNEL_MEMBER_COUNT                                = ('xpath', "//div[@id='Channelmembers_persons']")
    CHANNEL_MANGERS_BUTTON                              = ('xpath', "//div[contains(@class,'btn-group right-sep')]")
    CHANNEL_MANGER_NAME_NEW_UI                          = ('xpath', "//a[@href='javascript:;']")
    CHANNEL_MANGER_NAME_OLD_UI                          = ('xpath', "//dd[@id='functionaries-Managers']")
    CHANNEL_APPEARS_IN_BUTTON                           = ('xpath', "//a[@class='btn dropdown-toggle func-group' and contains(text(),'Appears in')]")
    CHANNEL_APPEARS_IN_CATEGORY_NAME                    = ('xpath', "//span[@data-toggle='tooltip' and @data-original-title='CATEGORY_NAME']")
    CHANNEL_PLAYLIST_VERIFICATION                       = ('xpath', "//a[@class='channel-playlist-link' and contains(@href,'/playlist/dedicated/')]")
    MY_CHANNELS_VIEW_CHANNELS_FILTER_BUTTON             = ('xpath', "//a[@id='type-btn' and @class='dropdown-toggle responsiveSize']")
    MY_CHANNELS_CHOOSE_VIEW_CHANNEL_FILTER              = ('xpath', "//a[@role='menuitem' and contains(text(),'VIEW_CHANNEL_FILTER')]")
    CHANNEL_REMOVE_SEARCH_ICON                          = ('xpath', "//i[@class='icon-remove']")
    CHANNEL_NO_RESULT_FOR_CHANNEL_SEARCH                = ('xpath', "//div[@class='alert alert-info fade in out alert-block']")
    CHANNELS_PAGE_ALL_CHANNELS_LIST                     = ('xpath', "//ul[@id='channelGallery']")
    MY_CHANNELS_SORT_CHANNELS_FILTER_BUTTON             = ('xpath', "//a[@id='sort-btn' and @class='dropdown-toggle responsiveSize']")
    MY_CHANNELS_SORT_CHANNELS_FILTER_BUTTON_NEWUI       = ('xpath', "//a[@id='sortBy-menu-toggle' and @class='  dropdown-toggle DropdownFilter__toggle ']")
    MY_CHANNELS_SORTBY_BUTTON_OLDUI                     = ('xpath', "//a[@id='sort-btn' and @class='dropdown-toggle responsiveSize']")
    MY_CHANNELS_SORTBY_BUTTON_NEWUI                     = ('xpath', "//a[@id='sortBy-menu-toggle' and @class='  dropdown-toggle DropdownFilter__toggle ']")
    CHANNEL_CANCEL_PLAYLIST_BUTTON                      = ('xpath', "//a[@class='btn null' and contains(text(),'Cancel')]")
    MY_CHANNELS_CHOOSE_SORT_CHANNEL_FILTER              = ('xpath', "//a[@role='menuitem' and contains(text(),'SORT_CHANNEL_FILTER')]")
    CHANNEL_PLAYLIST_EMBED_BUTTON                       = ('xpath', "//a[@id='tab-Embed' and contains(@href,'/embedplaylist/index/')]")
    CHANNEL_PLAYLIST_NAME                               = ('xpath', "//p[@data-lorem='3w' and text() ='PLAYLIST_TITLE']/ancestor::tr[contains(@data-playlistid, '')]")
    CHANNEL_PLAYLIST_EMBED_TEXT_AREA                    = ('xpath', '//textarea[@id="embed_code-CHANNEL_PLAYLIST_ID" and @class="span11 embedCodeText"]')
    CHANNELS_NO_MORE_CHANNELS_ALERT                     = ('xpath', "//div[@id='channels_scroller_alert' and contains(text(),'There are no more channels.')]")
    CHANNELS_TABLE_SIZE                                 = ('xpath', "//li[contains(@class,'span3 hidden-phone visible-v2ui')]")
    CHANNEL_ADD_CONTENT_FOR_SHAREDREPOSITORY            = ('xpath', "//a[@id='addcontent-repositories-tab' and @class='dropdown-toggle addcontent-repositories-tab']")
    CHANNEL_CHOOSE_SHAREDREPOSITORY_CHANNEL             = ('xpath', "//a[@data-original-title='CHANNEL_NAME' and @role='menuitem']")
    CHANNEL_DETAILS_ON_THUMBNAIL                        = ('xpath', "//img[@alt='Thumbnail for channel CHANNEL_NAME']/ancestor::div[contains (@class,'wrapper')]")
    CHANNEL_SEARCH_ENTRY                                = ('xpath', "//input[@class='searchForm__text' and @placeholder='Search this channel']")
    CHANNEL_EDIT_BUTTON_AFTER_SEARCH                    = ('xpath', '//*[@aria-label= "Edit ENTRY_NAME"]')
    CHANNEL_DELETE_FROM_EDIT_ENTRY_PAGE                 = ('xpath', "//a[@id='deleteMediaBtnForm' and contains(@href,'/entry/delete/')]")
    CHANNEL_CONFIRM_ENTRY_DELETE                        = ('xpath', "//a[@class='btn btn-danger' and text()='Remove']")
    CHANNEL_ENTRY_THUMBNAIL                             = ('xpath', "//div[@class='photo-group thumb_wrapper' and @title='ENTRY NAME']")
    CHANNEL_ENTRY_THUMBNAIL_EXPAND_BUTTON               = ('xpath', "//div[@class='hidden buttons-expand']")
    CHANNEL_EDIT_BUTTON_NO_SEARCH                       = ('xpath', "//i[@class='icon-pencil']")
    CHANNELS_DEFAULT_SORT                               = ('xpath', "//a[@id='sortBy-menu-toggle' and @class='  dropdown-toggle DropdownFilter__toggle ' and text()='DEFAULT_SORT']")
    CHANNEL_ENTRY_DELETE_BUTTON                         = ('xpath', '//a[contains(@aria-label,"Remove ENTRY_NAME")]')
    CHANNEL_GO_TO_CHANNEL_AFTER_UPLOAD                  = ('xpath', "//a[@id='next' and text()='Go To Channel']")
    CHANNEL_GO_BACK_TO_CHANNEL_BUTTON                   = ('xpath', "//a[@class='btn btn-link' and text()='Back to Channel']")
    CHANNEL_MEMEBER_TAB_OWNER_LABLE                     = ('xpath', "//div[@class='span3' and contains(text(),'Owner')]")
    ADD_TO_CHANNEL_SEARCH_BAR                           = ('xpath', '//input[@class="searchForm__text" and @placeholder="SEARCH_TAB"]')
    ADD_TO_CHANNEL_MY_MEDIA_TABLE                       = ('xpath', '//table[@class="table table-condensed table-hover bulkCheckbox mymediaTable mediaTable "]')
    ADD_TO_CHANNEL_MY_MEDIA_TABLE_SIZE                  = ('xpath', '//table[@class="table table-condensed table-hover bulkCheckbox mymediaTable mediaTable "]/tbody/tr')
    ADD_TO_CHANNEL_MY_MEDIA_NO_MORE_MEDIA_FOUND_MSG     = ('xpath', '//div[@id="myMedia_scroller_alert" and text()="There are no more media items."]')
    ADD_TO_CHANNEL_SR_NO_MORE_MEDIA_FOUND_MSG           = ('xpath', '//div[contains(@id, "sharedRepoEndless") and @class="alert alert-info endlessScrollAlert" and text()="There are no more media items."]')
    ADD_TO_CHANNEL_SR_DROP_DOWN_MENU                    = ('xpath', '//a[@id="addcontent-repositories-tab"]')
    ADD_TO_CHANNEL_SR_DROP_DOWN_MENU_OPTION             = ('xpath', '//a[@data-original-title="SR_NAME"]')
    ADD_TO_CHANNEL_SR_TABLE                             = ('xpath', '//table[@class="table table-condensed table-hover bulkCheckbox mymediaTable mediaTable full"]')
    ADD_TO_CHANNEL_SR_TABLE_SIZE                        = ('xpath', '//table[@class="table table-condensed table-hover bulkCheckbox mymediaTable mediaTable full"]/tbody/tr')
    CHANNEL_PENDING_TAB_TABLE                           = ('xpath', '//table[@class="table table-hover bulkCheckbox mediaTable moderation-table"]')
    CHANNEL_PENDING_TAB_TABLE_SIZE                      = ('xpath', '//table[@class="table table-hover bulkCheckbox mediaTable moderation-table"]/tbody/tr')
    CHANNEL_PENDING_TAB_NO_MORE_MEDIA_MSG               = ('xpath', '//div[@class="alert alert-info endlessScrollAlert"]')
    CHANNEL_PENDING_TAB_SEARCH_BAR                      = ('xpath', '//input[@placeholder="Search in Pending" and @class="searchForm__text"]')
    CHANNEL_PENDING_TAB_LOADING_ENTRIES_MSG             = ('xpath', '//div[@class="message" and text()="Loading..."]')
    CHANNEL_CHANNEL_PAGE_TABLE_SIZE                     = ('xpath', '//li[contains(@class,"galleryItem visible-v2ui hidden-phone")]')
    CHANNEL_NO_RESULT_FILTER                            = ('xpath', "//div[contains(@class,'alert alert-info') and text()='No Media Found' or text()='No media found']")
    CHANNEL_NO_RESULT_FILTER_MODERATION                 = ('xpath', "//div[@id='js-categoryModerationTable-container']//div[contains(@class,'alert alert-info')]")
    CHANNEL_ENTRY_ID_CHECKBOX                           = ('xpath', "//input[@id='ENTRY_ID']")
    CHANNEL_APPROVE_BUTTON_BULK                         = ('xpath', "//button[@id='bulk_accept']")
    CHANNEL_REJECT_BUTTON_BULK                          = ('xpath', "//button[@id='bulk_reject']")
    CHANNEL_BULK_POP_UP                                 = ('xpath', "//div[@class='modal-body']")
    CHANNEL_BULK_POP_UP_APPROVE                         = ('xpath', "//a[contains(@class,'btn btn-primary')][contains(text(),'Approve')]")
    CHANNEL_MEDIA_TAB_ACTIVE                            = ('xpath', "//a[@id='media-tab' and @aria-selected='true']")
    CHANNEL_ENTRY_PARENT_CHECKBOX                       = ('xpath', "//input[@type='checkbox' and @title='ENTRY_NAME']") 
    CHANNEL_GO_TO_MEDIA_GALLERY_AFTER_UPLOAD            = ('xpath', '//a[@id="next" and text()="Go To Media Gallery"]')
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
            if self.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED navigate to my channels")
                return False
                
            
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
        
        sleep(2)
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
            
            sleep(1)
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
    def navigateToMyChannels(self, forceNavigate=False):
        if forceNavigate == False:
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
    def navigateToChannels(self, forceNavigate=False):
        if forceNavigate == False:
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
    def searchAChannelInMyChannels(self, channelName, needToBeFound=True, exactName=True):
        try:                
            if self.navigateToMyChannels() == False:
                writeToLog("INFO","FAILED to navigate to my channels page")
                return False
            sleep(3)
            if self.clsCommon.isElasticSearchOnPage() == True:
                if self.click(self.MY_CHANNELS_SERACH_FIELD, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on name text field")
                    return False
                sleep(1)
                if exactName == True: 
                    searchString = '"' + channelName + '"'
                else:
                    searchString = channelName
                if self.send_keys(self.MY_CHANNELS_SERACH_FIELD, searchString + Keys.ENTER, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to type in 'name' text field")
                    return False
            else:
                if self.click(self.MY_CHANNELS_SERACH_FIELD_OLD_UI, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on name text field")
                    return False
                sleep(1)
                
                if self.send_keys(self.MY_CHANNELS_SERACH_FIELD_OLD_UI, channelName, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to type in 'name' text field")
                    return False
                
            self.clsCommon.general.waitForLoaderToDisappear()
            sleep(3)
            
            if needToBeFound == True:
                tmp_channelName = (self.MY_CHANNELS_HOVER[0], self.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', channelName))
                if self.is_visible(tmp_channelName) == False:
                    writeToLog("INFO","FAILED to find channel '" + channelName + "' after search in my channels")
                    return False
            
                writeToLog("INFO","Success, channel '" + channelName + "' was found after search")
                return True
            
            elif needToBeFound == False:
                try:
                    tmp_alert = self.get_element(self.CHANNEL_NO_RESULT_FOR_CHANNEL_SEARCH)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find alert element after search")
                    return False   
                
                if 'Your search for \"' + channelName + '\" did not match any channels.' in tmp_alert.text == False:
                    writeToLog("INFO","FAILED to find alert message  that channel is not found after search")
                    return False 
                
                writeToLog("INFO","Success, channel '" + channelName + "' was not found after search as expected")
                return True 
                    
        except NoSuchElementException:
            return False
        
    
    #  @Author: Tzachi Guetta  
    def searchAChannelInChannels(self, channelName):
        try:                
            if self.navigateToChannels() == False:
                writeToLog("INFO","FAILED to navigate to my channels page")
                return False
            
            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
                if self.click(self.MY_CHANNELS_SERACH_FIELD, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on name text field")
                    return False
                sleep(1)
                
                if self.send_keys(self.MY_CHANNELS_SERACH_FIELD,  '"' + channelName +  '"' + Keys.ENTER, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to type in 'name' text field")
                    return False
            else:
                if self.click(self.MY_CHANNELS_SERACH_FIELD_OLD_UI, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on name text field")
                    return False
                sleep(1)
                
                if self.send_keys(self.MY_CHANNELS_SERACH_FIELD_OLD_UI, channelName, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to type in 'name' text field")
                    return False
            
        except NoSuchElementException:
            return False
        
        return True
    
    
    #  @Author: Tzachi Guetta  
    def navigateToChannel(self, channelName, navigateFrom=enums.Location.MY_CHANNELS_PAGE, forceNavigate=False):
        try:                
            if navigateFrom == enums.Location.MY_CHANNELS_PAGE:
                if self.navigateToMyChannels(forceNavigate) == False:
                    writeToLog("INFO","FAILED navigate to my channels page")
                    return False
                    
                if self.searchAChannelInMyChannels(channelName) == False:
                    writeToLog("INFO","FAILED to search in my channels")
                    return False
                
            elif navigateFrom == enums.Location.CHANNELS_PAGE:
                if self.navigateToChannels(forceNavigate) == False:
                    writeToLog("INFO","FAILED navigate to my channels page")
                    return False
                
                if self.searchAChannelInChannels(channelName) == False:
                    writeToLog("INFO","FAILED to search in channels")
                    return False    
                
            self.clsCommon.general.waitForLoaderToDisappear()        
            sleep(2)
            tmp_channel_name = (self.MY_CHANNELS_HOVER[0], self.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', channelName))
            if self.click(tmp_channel_name) == False:
                writeToLog("INFO","FAILED to click on Channel's thumbnail")
                return False
            
            sleep(3)
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

            if self.clsCommon.isElasticSearchOnPage() == False:
                if self.click(self.CHANNEL_PAGE_SEARCH_TAB) == False:
                    writeToLog("INFO","FAILED to click on Channel's search Tab icon")
                    return False
                sleep(2)
                # Search Entry     
                self.clsCommon.myMedia.getSearchBarElement().click()
                
            if self.clsCommon.isElasticSearchOnPage() == True:
                searchLine = '"' + entryName + '"'
            else:
                searchLine = entryName        
            self.clsCommon.myMedia.getSearchBarElement().send_keys(searchLine)
            sleep(2)
            self.clsCommon.general.waitForLoaderToDisappear()
            
            if self.wait_visible(self.CHANNEL_PAGE_NO_RESULT_ALERT, 5) == False:
                if isExpected == True:
                    if self.clsCommon.myMedia.getResultAfterSearch(entryName) == False:
                        writeToLog("INFO","NOT Expected: Entry was not found in the channel")
                        return False                        
                        writeToLog("INFO","As Expected: Entry was found in the channel")
                        return True
                    else:
                        writeToLog("INFO","As Expected: Entry was found in the channel")
                        return True
                else:
                    if self.clsCommon.myMedia.getResultAfterSearch(entryName) == False:
                        writeToLog("INFO","As Expected: Entry was not found in the channel")
                        return True                         
                    else:
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
            
            sleep(3)
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

            
    def naviagteToEntryFromChannelPage(self, entryName, channelName, exactSearch=True):
        # Check if we are already in channel page
        tmp_channel_title = (self.CHANNEL_PAGE_TITLE[0], self.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
        if self.wait_visible(tmp_channel_title, 5) != False:
            writeToLog("INFO","Success, Already in channel page")
            return True
        
        if self.navigateToChannel(channelName) == False:
            writeToLog("INFO","FAILED to navigate to Channel page '" + channelName + "'")
            return False
        
        if self.clsCommon.isElasticSearchOnPage() == False:
            if self.click(self.CHANNEL_PAGE_SEARCH_TAB) == False:
                writeToLog("INFO","FAILED to click on Channel's search Tab icon")
                return False
            sleep(2)
            # Search Entry     
            self.clsCommon.myMedia.getSearchBarElement().click()
            
        if exactSearch == True:
            searchLine = '"' + entryName + '"'
        else:
            searchLine = entryName        
        self.clsCommon.myMedia.getSearchBarElement().send_keys(searchLine)
        sleep(2)
        self.clsCommon.general.waitForLoaderToDisappear()
        
        if self.clsCommon.isElasticSearchOnPage() == False:
            tmpEntry = self.CHANNEL_PAGE_ENTRY_THUMBNAIL[0], self.CHANNEL_PAGE_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName)
            if self.click(tmpEntry, 20, True) == False:
                writeToLog("INFO","FAILED to click on entry")
                return False
        else:
            if self.clsCommon.myMedia.clickResultEntryAfterSearch(entryName) == False:
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
        sleep(3)
        
        if self.click(self.CHANNEL_EDIT_DROP_DOWN_MENU) == False:
            writeToLog("INFO","FAILED to Click on edit drop down menu")
            return False  
        sleep(2)
        
        if self.click(self.CHANNEL_EDIT_BUTTON) == False:
            writeToLog("INFO","FAILED to Click on edit drop down menu")
            return False  
        sleep(2)
        
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
    def createChannelPlaylist(self, channelName, playlisTitle, playlistDescription, playlistTag, entriesNames): 
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
       
#         if self.fillChannelPlaylistTags(playlistTag) == False:
#             writeToLog("INFO","FAILED to fill a playlisttags title :'" + playlistTag + "'")
#             return False   
      
        if(localSettings.LOCAL_RUNNING_BROWSER == clsTestService.PC_BROWSER_CHROME):
            # Remove the Mask over all the screen (over tags filed also)
            maskOverElement = self.get_element(self.clsCommon.channel.CHANNEL_REMOVE_TAG_MASK)
            self.driver.execute_script("arguments[0].setAttribute('style','display: none;')",(maskOverElement))          
       
            if self.send_keys(self.CHANNEL_PLAYLISTS_TAG_AFTER_CLICK, playlistTag, multipleElements=True) == False:
                writeToLog("INFO","FAILED to fill a playlisttags  :'" + playlistTag + "'")
                return False      
        else:    
            
            if self.fillChannelPlaylistTags(playlistTag) == False:
                writeToLog("INFO","FAILED to fill a playlisttags  :'" + playlistTag + "'")
                return False     
               
        if self.click(self.CHANNEL_PLAYLISTS_ADD_MEDIA_URL) == False:
            writeToLog("INFO","FAILED to click on add media url title :'" +  + "'")
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
        sleep(4)    
        
        tmp_check = (self.CHANNEL_EDIT_CHANNNEL_PAGE[0], self.CHANNEL_EDIT_CHANNNEL_PAGE[1].replace('CHANNEL_NAME', channelName))
        if self.click(tmp_check) == False:
            writeToLog("INFO","FAILED to click on Channel name")
            return False      
        sleep(4) 
       
        tmp_channel_playlist = (self.CHANNEL_PLAYLIST_VERIFICATION[0], self.CHANNEL_PLAYLIST_VERIFICATION[1].replace('PLAYLIST_TITLE', playlisTitle))
        if self.click(tmp_channel_playlist) == False:
            writeToLog("INFO","FAILED to click on playlist name")
            return False         
                   
        return True
    
    
    # Author : Michal Zomper
    # tags - should provided with ',' as a delimiter and comma (',') again in the end of the string
    #        for example 'tags1,tags2,'
    def fillChannelPlaylistTags(self, tags):
        try:
            self.switch_to_default_content()
            tagsElement = self.get_element(self.CHANNEL_PLAYLISTS_TAG)
            
        except NoSuchElementException:
            writeToLog("DEBUG","FAILED to get Tags filed element")
            return False
        sleep(2)       
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
        

    def sortAndFilterInChannelPlaylist(self, channelName, playlisTitle, playlistDescription, playlistTag, sortBy='', filterMediaType=''):
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
        
        # Remove the Mask over all the screen (over tags filed also)
        maskOverElement = self.get_element(self.clsCommon.channel.CHANNEL_REMOVE_TAG_MASK)
        self.driver.execute_script("arguments[0].setAttribute('style','display: none;')",(maskOverElement))          
   
        if self.send_keys(self.CHANNEL_PLAYLISTS_TAG_AFTER_CLICK, playlistTag, multipleElements=True) == False:
            writeToLog("INFO","FAILED to fill a playlisttags  :'" + playlistTag + "'")
            return False 
             
        if self.click(self.CHANNEL_PLAYLISTS_ADD_MEDIA_URL) == False:
            writeToLog("INFO","FAILED to click on add media url title :'" +  + "'")
            return False        
                       
        if sortBy != '':
            if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.SORT_BY, sortBy) == False:
                writeToLog("INFO","FAILED to set sortBy: " + str(sortBy) + " in my media")
                return False

        if filterMediaType != '':
            if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, filterMediaType) == False:
                writeToLog("INFO","FAILED to set filter: " + str(filterMediaType) + " in my media")
                return False       
        sleep(3)
        
       
        if self.click(self.CHANNEL_CANCEL_PLAYLIST_BUTTON) == False:
            writeToLog("INFO","FAILED to click on cancel")
            return False 
               
        return True  
    
    
    def getChannelPlaylistID(self, playlisTitle):
        tmp_channelplaylist_name = (self.CHANNEL_PLAYLIST_NAME[0], self.CHANNEL_PLAYLIST_NAME[1].replace('PLAYLIST_TITLE', playlisTitle))
        if self.is_visible(tmp_channelplaylist_name) == False:
            writeToLog("INFO","FAILED to find playlist '" + playlisTitle + "' in my playlist page")
            return False 
        try:
            channelPlaylistID = self.get_element(tmp_channelplaylist_name).get_attribute("data-playlistid")
        
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get playlist id")
            return False
        
        writeToLog("INFO","Success, successfully get playlist ID")
        return channelPlaylistID


    def clickEmbedChannelPlaylistAndGetEmbedCode(self, playlisTitle):
        channelPlaylist_id = self.getChannelPlaylistID(playlisTitle)
        if channelPlaylist_id == False:
            writeToLog("INFO","FAILED to get playlist id")
            return False 
        
        if self.click(self.CHANNEL_PLAYLIST_EMBED_BUTTON) == False:
            writeToLog("INFO","FAILED to click on cancel")
            return False 
        sleep(3) 
                
        tmpEmbedTextArea = (self.CHANNEL_PLAYLIST_EMBED_TEXT_AREA[0], self.CHANNEL_PLAYLIST_EMBED_TEXT_AREA[1].replace('CHANNEL_PLAYLIST_ID', channelPlaylist_id))
        if self.wait_visible(tmpEmbedTextArea) == False:
            writeToLog("INFO","FAILED to get embed text area")
            return False  
        
        #Get embed code from embed text area 
        embed_code =  self.clsCommon.myPlaylists.getEmbedCode(tmpEmbedTextArea)
        if embed_code:
            return embed_code
                
#         embed_text = self.is_element_checked(self.CHANNEL_PLAYLIST_EMBED_TEXT_AREA)
#         return embed_text
                  
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

    
    #@Author: Oded Berihon and Oleg Sigalov
    def removeEntryFromChannel(self, channelName, entryName):
        if self.searchAChannelInMyChannels(channelName) == False:
            writeToLog("INFO","FAILED to find to channel: " +  channelName)
            return False 
            
        tmpChannelName = (self.CHANNEL_CLICK_ON_CHANNEL_AFTER_SEARCH[0], self.CHANNEL_CLICK_ON_CHANNEL_AFTER_SEARCH[1].replace('CHANNEL_NAME', channelName))
        if self.click(tmpChannelName) == False:
            writeToLog("INFO","FAILED to Click on Channel name: '" + channelName + "'")
            return False   
        sleep(5)
            
        if self.removeEntry(entryName) == False:
            writeToLog("INFO","FAILED to remove entry")
            return False 
        
        return True


    #Author: Michal Zomper
    def removeEntry(self, entryName):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            parent_entry = self.expandEntryDetails(entryName)
            if parent_entry == False:
                return False
            
        # If we are in old UI we need to click first on "+" icon on entry's thumbnail
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if self.clickEntryPlusIcon(entryName) == False:
                return False
            
        # Set Remove button locator for old UI
        tmpEntryEemoveBtn = (self.CHANNEL_ENTRY_DELETE_BUTTON[0], self.CHANNEL_ENTRY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName))   

        sleep(2)
        if self.click(tmpEntryEemoveBtn) == False:
            writeToLog("INFO","FAILED to click on Remove button")
            return False 
        sleep(2)
        
        if self.click(self.CHANNEL_CONFIRM_ENTRY_DELETE, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False
        sleep(4)
        
        self.clsCommon.general.waitForLoaderToDisappear()
        writeToLog("INFO","Success, entry '" + entryName + "' was removed successfully")
        return True
        
        
    #@Author: Oded Berihon
    def addCommentToEntryFromChannel(self, channelName, entryName, comment):
        if self.navigateToEntryFromChannel(channelName, entryName) == False:
            writeToLog("INFO","FAILED to find entry in channel")
            return False
         
        if self.clsCommon.entryPage.addComment(comment) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False    

        return True
    
   
    #@Author: Oded Berihon
    def enableDisableCommentsInChannel(self, channelName, isCommentsEnabled):
        if isCommentsEnabled == True:
            if self.is_element_checked(self.CHANNEL_DETAILS_OPTION_COMMENT)==True:
                return True
            else:
                if self.click(self.CHANNEL_DETAILS_OPTION_COMMENT, 30) == False:
                    writeToLog("INFO","FAILED to click on comments checkbox")
                    return False
        else:#Disable comments
            if self.is_element_checked(self.CHANNEL_DETAILS_OPTION_COMMENT)==False:
                return True
            else:
                if self.click(self.CHANNEL_DETAILS_OPTION_COMMENT, 30) == False:
                    writeToLog("INFO","FAILED to click on comments checkbox")
                    return False            
          
        if self.click(self.CHANNEL_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Save button")
            return False     
         
        return True

    
    #  @Author: Oded berihon
    def navigateToEntryFromChannel(self, channelName, entryName): 
        if self.navigateToChannel(channelName) == False:
            writeToLog("INFO","FAILED to navigate to Channel page")
            return False
        
        if self.searchEntryInChannel(entryName) == False:
            writeToLog("INFO","FAILED to search for entry in channel page")
            return False
        
        if self.clsCommon.myMedia.clickEntryAfterSearchInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to click on Channel's search Tab icon")
            return False 
        
        tmp_entry_name = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmp_entry_name, 15) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
            return False
        
        return True

   
    def navigateToEditEntryPageFromChannelWhenNoSearchIsMade(self, entryName):
        tmp_entry_edit_btn = None
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            parent_entry = self.expandEntryDetails(entryName)
            if parent_entry == False:
                return False
        
            sleep(1)
            if self.click_child(parent_entry, self.CHANNEL_EDIT_BUTTON_NO_SEARCH, timeout=20, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on the edit icon")
                return False        # Edit entry icon
            
        # If we are in old UI we need to click first on "+" icon on entry's thumbnail
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if self.clickEntryPlusIcon(entryName) == False:
                return False
            
            #set edit button for old UI
            tmp_entry_edit_btn = (self.clsCommon.category.CATEGORY_EDIT_ENTRY_BTN_OLD_UI[0], self.clsCommon.category.CATEGORY_EDIT_ENTRY_BTN_OLD_UI[1].replace('ENTRY_NAME', entryName))   

            sleep(3)
            if self.click(tmp_entry_edit_btn) == False:
                writeToLog("INFO","FAILED to click on edit button")
                return False   
        
        # Verify that we are in edit entry page - wait until you see edit entry page title
        tmp_entry_title = (self.clsCommon.editEntryPage.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[0], self.clsCommon.editEntryPage.EDIT_ENTRY_PAGE_ENTRY_NAME_TITLE[1].replace('ENTRY_NAME', entryName))
        if self.wait_visible(tmp_entry_title) == False:
            writeToLog("INFO","FAILED to displayed edit entry page title")
            return False          
               
        return True                      
    
    
    # @Author: Oleg Sigalov
    def clickEntryPlusIcon(self, entryName):
        tmp_entry_thumbnail = (self.clsCommon.category.CATEGORY_ENTRY_THUMBNAIL[0], self.clsCommon.category.CATEGORY_ENTRY_THUMBNAIL[1].replace('ENTRY NAME', entryName))    
        try:
            parent_entry = self.get_element(tmp_entry_thumbnail)
            parent_entry = parent_entry.find_element_by_xpath("..")
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entry '" + entryName + "' element")
            return False
        
        if self.click_child(parent_entry, self.clsCommon.category.CATEGORY_PLUS_SIGN_BUTTON_ON_ENTRY_THUMBNAIL, timeout=20, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on the plus button in order to see entry details")
            return False
        
        return True
    
    
    # @Author: Oleg Sigalov
    def expandEntryDetails(self, entryName):
        tmp_entry_thumbnail = (self.CHANNEL_ENTRY_THUMBNAIL[0], self.CHANNEL_ENTRY_THUMBNAIL[1].replace('ENTRY NAME', entryName))
        try:
            parent_entry = self.get_element(tmp_entry_thumbnail)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entry '" + entryName + "' element")
            return False            
    
        if self.click_child(parent_entry, self.CHANNEL_ENTRY_THUMBNAIL_EXPAND_BUTTON, timeout=20, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on expand button")
            return False
        
        return parent_entry      
    

    # @Author: Tzachi Guetta  
    # Ths function adding an existing content to channel   
    def addExistingContentToChannel(self, channelName, entriesNames, isChannelModerate, publishFrom=enums.Location.MY_CHANNELS_PAGE, channelType="", sharedReposiytyChannel=""):
        try:                
            if self.navigateToChannel(channelName, publishFrom) == False:
                writeToLog("INFO","FAILED to navigate to  channel: " +  channelName)
                return False
            
            if self.click(self.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
                writeToLog("INFO","FAILED to click add to channel button")
                return False           
            
            sleep(1)
            self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
            
            if channelType == enums.ChannelPrivacyType.SHAREDREPOSITORY:
                # open shared repository list
                if self.click(self.CHANNEL_ADD_CONTENT_FOR_SHAREDREPOSITORY) == False:
                    writeToLog("INFO","FAILED to open shared repository channels list")
                    return False
                
                #chose shared repository channel 
                tmpSharedRepositoryChannel = (self.CHANNEL_CHOOSE_SHAREDREPOSITORY_CHANNEL[0], self.CHANNEL_CHOOSE_SHAREDREPOSITORY_CHANNEL[1].replace('CHANNEL_NAME', sharedReposiytyChannel))
                if self.click(tmpSharedRepositoryChannel) == False:
                    writeToLog("INFO","FAILED to select channel '" + sharedReposiytyChannel + "' as the shared repository channel to add content from")
                    return False
                self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
                
            if self.addContentFromMyMedia(entriesNames) == False:
                writeToLog("INFO","FAILED to publish entries to channel: " + channelName)
                return False
                
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
    
    
    # Author: Michal Zomper
    def addContentFromMyMedia(self, entriesNames):
        # Checking if entriesNames list type
        if type(entriesNames) is list: 
            for entryName in entriesNames: 
                if self.clsCommon.myMedia.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to CHECK the entry: " + entryName + ", At add content -> my media flow")
                    return False
                
                writeToLog("INFO","Going to publish Entry: " + entryName)
        else:
            if self.clsCommon.myMedia.checkSingleEntryInMyMedia(entriesNames) == False:
                    writeToLog("INFO","FAILED to CHECK the entry: " + entriesNames + ", At add content -> my media flow")
                    return False
                
            writeToLog("INFO","Going to publish Entry: " + entriesNames)
            
        if self.click(self.CHANNEL_PUBLISH_BUTTON) == False:
            writeToLog("INFO","FAILED to CHECK the entry: " + entriesNames + ", At add content -> my media flow")
            return False             
        
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        
        return True
    
    
    
    #   @Author: Tzachi Guetta    
    def handlePendingEntriesInChannel(self, channelName, toRejectEntriesNames, toApproveEntriesNames , navigate=True):
                       
        if navigate == True:
            if self.navigateToChannel(channelName) == False:
                writeToLog("INFO","FAILED to navigate to  channel: " +  channelName)
                return False
            
            if self.click(self.CHANNEL_MODERATION_TAB, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on channel's moderation tab")
                return False        
        
        sleep(1)
        self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30) 
        
        if self.approveEntriesInPandingTab(toApproveEntriesNames) == False:
            writeToLog("INFO","FAILED to approve entries")
            return False  
        
        self.refresh()
        sleep(6)
        self.click(self.CHANNEL_MODERATION_TAB, timeout=60, multipleElements=True)
        
        if self.rejectEntriesInPandingTab(toRejectEntriesNames) == False:
            writeToLog("INFO","FAILED to reject entries")
            return False 
       
        if self.navigateToChannel(channelName) == False:
            writeToLog("INFO","FAILED navigate to channel page")
            return False  
            
        if self.verifyEntriesApprovedAndRejectedInChannelOrGallery(toRejectEntriesNames, toApproveEntriesNames) == False:
            writeToLog("INFO","FAILED, not all entries was approved/ rejected as needed")
            return False 
        
        return True
    
    
    # Author: Tzachi Guetta 
    def approveEntriesInPandingTab(self, toApproveEntriesNames, location=''):
        if type(toApproveEntriesNames) is list:
            for approveEntry in toApproveEntriesNames:
                if self.method_helper_approveEntry(approveEntry, location) == False:
                    writeToLog("INFO","FAILED to approve entry: " + approveEntry)
                    return False 
                sleep(3)
                self.clsCommon.general.waitForLoaderToDisappear()
        else:
            if toApproveEntriesNames != '':
                if self.method_helper_approveEntry(toApproveEntriesNames, location) == False:
                    writeToLog("INFO","FAILED to approve entry: " + toApproveEntriesNames)
                    return False
                sleep(3) 
                self.clsCommon.general.waitForLoaderToDisappear()
        
        return True
    
    
        # Author: Tzachi Guetta 
    def rejectEntriesInPandingTab(self, toRejectEntriesNames, location=''):
        if type(toRejectEntriesNames) is list:
            for rejectEntry in toRejectEntriesNames:
                if self.method_helper_rejectEntry(rejectEntry, location) == False:
                    writeToLog("INFO","FAILED to reject entry: " + rejectEntry)
                    return False 
                sleep(3)
                self.clsCommon.general.waitForLoaderToDisappear()
            
        else:
            if toRejectEntriesNames != '':
                if self.method_helper_rejectEntry(toRejectEntriesNames, location) == False:
                    writeToLog("INFO","FAILED to reject entry: " + toRejectEntriesNames)
                    return False 
                sleep(3)
                self.clsCommon.general.waitForLoaderToDisappear()               
        
        return True
    
    
    
    def verifyEntriesApprovedAndRejectedInChannelOrGallery(self, toRejectEntriesNames, toApproveEntriesNames):
        if type(toRejectEntriesNames) is list:
            for rejectEntry in toRejectEntriesNames:
                if self.searchEntryInChannel(rejectEntry) == True:
                    writeToLog("INFO","FAILED, reject entry '" + rejectEntry + "' exist in gallery/channel page although the entry was rejected")
                    return False 
                writeToLog("INFO","Preview step failed as expected - entry was rejected and should not be found")
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False 
        else:
            if toRejectEntriesNames != '':
                if self.searchEntryInChannel(toRejectEntriesNames) == True:
                    writeToLog("INFO","FAILED, reject entry '" + toRejectEntriesNames + "' exist in gallery/channel page although the entry was rejected")
                    return False 
                writeToLog("INFO","Preview step failed as expected - entry was rejected and should not be found")
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False               
        
        if type(toApproveEntriesNames) is list:
            for approveEntry in toApproveEntriesNames:
                if self.searchEntryInChannel(approveEntry) == False:
                    writeToLog("INFO","FAILED, approved entry '" + approveEntry + "' doesn't exist in gallery/channel page although the entry was approved")
                    return False 
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False 
        else:
            if toApproveEntriesNames != '':
                if self.searchEntryInChannel(toApproveEntriesNames) == False:
                    writeToLog("INFO","FAILED, approved entry '" + toApproveEntriesNames + "' doesn't exist in gallery/channel page although the entry was approved")
                    return False 
                
                if self.clsCommon.myMedia.clearSearch() == False:
                    writeToLog("INFO","FAILED to clear search")
                    return False 
        
        return True
                
    
    # Author: Tzachi Guetta     
    def method_helper_rejectEntry(self, rejectEntry, location=''):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            self.switch_to_default_content()
            self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            self.clsCommon.sharePoint.switchToSharepointIframe()
            self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB)
        
#         if location == enums.Location.PENDING_TAB:
        tmpEntry = (self.CHANNEL_ENTRY_PARENT_CHECKBOX[0], self.CHANNEL_ENTRY_PARENT_CHECKBOX[1].replace('ENTRY_NAME', rejectEntry))
        entryId = self.clsCommon.upload.extractEntryIDFromCheckBox(tmpEntry)
        if entryId == False:
            return False 
        tmpRejectBtn = (self.CHANNEL_REJECT_BUTTON[0], self.CHANNEL_REJECT_BUTTON[1].replace('ENTRY_ID', entryId))
            
#         else:
#             tmpEntry = (self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[0], self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[1].replace('ENTRY_NAME', rejectEntry))
#             entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
#             tmpRejectBtn = (self.CHANNEL_REJECT_BUTTON[0], self.CHANNEL_REJECT_BUTTON[1].replace('ENTRY_ID', entryId))
        sleep(1)
        if self.click(tmpRejectBtn) == False:
            writeToLog("INFO","FAILED to reject entry: " + rejectEntry)
            return False 
        
        writeToLog("INFO","The following entry was rejected : " + rejectEntry)  
        return True
        
        
    # Author: Tzachi Guetta     
    def method_helper_approveEntry(self, approveEntry, location=''):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            self.switch_to_default_content()
            self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
            self.clsCommon.sharePoint.switchToSharepointIframe()
            self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB)
            
#         if location == enums.Location.PENDING_TAB:
        tmpEntry = (self.CHANNEL_ENTRY_PARENT_CHECKBOX[0], self.CHANNEL_ENTRY_PARENT_CHECKBOX[1].replace('ENTRY_NAME', approveEntry))
        entryId = self.clsCommon.upload.extractEntryIDFromCheckBox(tmpEntry)
        if entryId == False:
            return False 
        tmpApproveBtn = (self.CHANNEL_APPROVE_BUTTON[0], self.CHANNEL_APPROVE_BUTTON[1].replace('ENTRY_ID', entryId)) 
                       
#         else:    
#             tmpEntry = (self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[0], self.CHANNEL_ENTRY_IN_PENDING_TAB_PARENT[1].replace('ENTRY_NAME', approveEntry))
#             entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
#             if entryId == False:
#                 return False 
#             tmpApproveBtn = (self.CHANNEL_APPROVE_BUTTON[0], self.CHANNEL_APPROVE_BUTTON[1].replace('ENTRY_ID', entryId))
        sleep(1)
        if self.click(tmpApproveBtn) == False:
            writeToLog("INFO","FAILED to approve entry: " + approveEntry)
            return False   
        
        self.clsCommon.general.waitForLoaderToDisappear()                
        writeToLog("INFO","The following entry was approved : " + approveEntry)
        return True
        
        
    # Author: Tzachi Guetta 
    def sortAndFilterInPendingTab(self, sortBy='', filterMediaType='', channelName='', navigate=True, location=enums.Location.CHANNEL_PAGE):
        try:         
            if navigate == True:
                if self.navigateToPendingaTab(channelName, location) == False:
                    writeToLog("INFO","FAILED to navigate to pending tab in: " + channelName)
                    return False   
                   
            sleep(2)
            
#             if self.clsCommon.isElasticSearchOnPage() == True:
#                     sortBy = sortBy.value
                    
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
    def addMembersToChannel(self, channelName, username, permission=enums.ChannelMemberPermission.MEMBER):
        if self.navigateToEditChannelPage(channelName) == False:
            writeToLog("INFO","Failed to navigate to edit channel page")
            return False  
        sleep(1)   
        
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
        
        # Wait until add member popup is displayed
        sleep(3)
         
        # Insert username to field
        if self.send_keys(self.CHANNEL_ADD_MEMBER_MODAL_USERNAME_FIELD, username) == False:
            writeToLog("INFO","Failed to insert username")
            return False
        
        sleep(3)
        tmpConfirmationLocator = (self.CHANNEL_ADD_MEMBER_GROUP_CONFIRMATION[0], self.CHANNEL_ADD_MEMBER_GROUP_CONFIRMATION[1].replace('USERNAME', username))
        if self.click(tmpConfirmationLocator) == False:
            writeToLog("INFO","FAILED to click on group search confirmation")
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
        if self.wait_visible(tmp_member_row) == False:
            writeToLog("INFO","Failed new member was NOT added to members table")
            return False
        sleep(3)
        
        return True                                         
             
                           
    ##################################This method is deprecated, don't remove yet
    # @Author: Inbar Willman 
    # Edit permission from drop down list
    def editMemberPermissionInChannel(self, permission = enums.ChannelMemberPermission.MEMBER):    
        # If permission is member click on member option       
        if permission ==  enums.ChannelMemberPermission.MEMBER:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION_EDIT, 'Member') == False:
                writeToLog("INFO","Failed to click on member option")
                return False                    
       
        # If permission is contributor click on member option       
        elif permission ==  enums.ChannelMemberPermission.CONTRIBUTOR:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION_EDIT, 'Contributor') == False:
                writeToLog("INFO","Failed to click on contributor option")
                return False  
            
        # If permission is moderator click on member option       
        elif permission ==  enums.ChannelMemberPermission.MODERATOR:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION_EDIT, 'Moderator') == False:
                writeToLog("INFO","Failed to click on moderator option")
                return False 
        
        # If permission is manager click on member option       
        elif permission ==  enums.ChannelMemberPermission.MANAGER:
            if self.select_from_combo_by_text(self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION_EDIT, 'Manager') == False:
                writeToLog("INFO","Failed to click on manager option")
                return False   
            
        return True


    # @Author: Oleg Sigalov
    # Choose permission from combo box list
    def chooseMemberPermissionInChannel(self, permission=enums.ChannelMemberPermission.MEMBER):    
        tmpPermissionLocator = (self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION[0], self.CHANNEL_ADD_MEMBER_MODAL_SET_PERMISSION[1].replace('PERMISSION', permission.value))
        if self.click(tmpPermissionLocator) == False:
            writeToLog("INFO","Failed to click on " + permission.value + " option")
            return False                    
              
        return True    
    
    
    # @Author: Inbar Willman
    # Edit member permission
    def editChannelMemberPermission(self,username, permission = enums.ChannelMemberPermission.MODERATOR): 
        #Click on edit button
        tmp_edit_button = (self.CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON[0], self.CHANNEL_MEMBERS_TAB_EDIT_MEMBER_BUTTON[1].replace('MEMBER', username))
        if self.hover_on_element(tmp_edit_button) == False:
            writeToLog("INFO","FAILED to Hover above edit member button")
            return False
        
        if self.click(tmp_edit_button) == False:
                writeToLog("INFO","Failed to click on edit button")
                return False               
                         
        # Set new permission
        if self.editMemberPermissionInChannel(permission) == False:
            writeToLog("INFO","Failed to set new permission")
            return False   
        
        # Save new permission
        if self.click(tmp_edit_button) == False:
                writeToLog("INFO","Failed to click on save button")
                return False                  
        
        return True
  
    
    # @Author: Inbar Willman
    # Delete member from channel
    def deleteChannelMember(self,username): 
        sleep(2)
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
        
        sleep (6)
            
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
        
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(4)
        # Wait until set owner modal isn't visible anymore
#         if self.wait_while_not_visible(self.CHANNEL_SET_OWNER_MODAL_CONTENT, timeout=30) == False:
#             writeToLog("INFO","Failed to wait until set owner modal isn't visible")
#             return False              
#          
        sleep(2)
        #Verify that user have the owner label under action
        try:
            ownerLabel = self.get_element(self.CHANNEL_MEMEBER_TAB_OWNER_LABLE) 
            ownerLabelParent = ownerLabel.find_element_by_xpath("..")
            if ownerLabelParent.get_attribute("data-id") != username:
                writeToLog("INFO","Failed to set user as owner")
                return False 
        except :
            writeToLog("INFO","Failed to verify user was set as owner")
            return False 
        
        sleep(2)
        return True
    
    
    # Author: Michal Zomper                                                                     
    def subscribeUserToChannel(self, channelName, countOfSubscribers, navigateFrom=enums.Location.CHANNELS_PAGE):
        if self.navigateToChannel(channelName, navigateFrom) == False:
            writeToLog("INFO","Failed navigate to channel '" + channelName + "' page")
            return False  
        
        sleep(2)
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            if self.click(self.CHANNEL_SUBSCRIBE_BUTTON, 20, multipleElements=True) == False:
                writeToLog("INFO","Failed to click on subscribe button")
                return False  
        
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if self.click(self.CHANNEL_SUBSCRIBE_BUTTON_OLD_UI, 20, multipleElements=True) == False:
                writeToLog("INFO","Failed to click on subscribe button")
                return False 
        
        sleep(2)
        self.driver.refresh()      
        sleep(6)   
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:     
            if countOfSubscribers + " Subscribers" != self.get_element_text(self.CHANNEL_SUBSCRIBER_COUNT, timeout=20):
                writeToLog("INFO","Failed to find subscriber count in channel page")
                return False  
            
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if countOfSubscribers+ "\nsubscribers" != self.get_element_text(self.CHANNEL_SUBSCRIBER_COUNT, timeout=20).lower():
                writeToLog("INFO","Failed to find subscriber count in channel page")
                return False  
        writeToLog("INFO","Success, user was added as subscriber to channel")
        return True
            
                               
    # Author: Michal Zomper
    def verifyChannelInformation(self, channelType, entriesCount, memberCount, subscriberCount, managerName, appearsInCategoryName=''):  
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True: 
            if channelType in self.get_element_text(self.CHANNEL_TYPE, 20).lower() == False:
                writeToLog("INFO","Failed to verify that channel type is : " + channelType)
                return False  
            
            if entriesCount + " Media" != self.get_element_text(self.CHANNEL_MEDIA_COUNT, 20):
                writeToLog("INFO","Failed to verify that channel media count is: " + entriesCount)
                return False 
        
            if memberCount + " Members" != self.get_element_text(self.CHANNEL_MEMBER_COUNT, 20):
                writeToLog("INFO","Failed to verify that channel member count is: " + memberCount)
                return False 
            
            if subscriberCount + " Subscribers" != self.get_element_text(self.CHANNEL_SUBSCRIBER_COUNT, timeout=20):
                writeToLog("INFO","Failed to verify that channel subscriber count is: " + subscriberCount)
                return False 
            
            if self.click(self.CHANNEL_MANGERS_BUTTON, 20, multipleElements=True) == False:
                writeToLog("INFO","Failed to click on managers button")
                return False
            
            try:
                parent = self.wait_element(self.CHANNEL_MANGERS_BUTTON, 20, multipleElements=True)
                elManagerName = self.get_child_element(parent, self.CHANNEL_MANGER_NAME_NEW_UI, multipleElements=True)
            except NoSuchElementException:
                writeToLog("INFO","Failed to get channel manager element")
                return False
            
            if managerName.lower() != elManagerName.text.lower():
                writeToLog("INFO","Failed to verify channel manager name: " + managerName)
                return False 
            
            # close mangers list
            if self.click(self.CHANNEL_MANGERS_BUTTON, 20, multipleElements=True) == False:
                writeToLog("INFO","Failed to click on managers button")
                return False
            
            if appearsInCategoryName != '':
                tmp_chnnelAppearIn = (self.CHANNEL_APPEARS_IN_CATEGORY_NAME[0], self.CHANNEL_APPEARS_IN_CATEGORY_NAME[1].replace('CATEGORY_NAME', appearsInCategoryName))
                if self.click(self.CHANNEL_APPEARS_IN_BUTTON, 20, multipleElements=True) == False:
                    writeToLog("INFO","Failed to click on appears in button")
                    return False
                
                if self.is_visible(tmp_chnnelAppearIn) == False:
                    writeToLog("INFO","Failed to verify channel appear in category: " + appearsInCategoryName)
                    return False 
        
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            try:
                details= self.get_element_text(self.CHANNEL_CHANNEL_INFO_OLD_UI)
            except NoSuchElementException:
                writeToLog("INFO","Failed to get channel information element")
                return False
            
            tmp_channelDetails = details.split('\n')
            if channelType in tmp_channelDetails[0].lower() == False:
                writeToLog("INFO","FAILED to verify that channel type is: " + channelType)
                return False
                
            if entriesCount + "\nmedia" != self.get_element_text(self.CHANNEL_MEDIA_COUNT, 20).lower():
                writeToLog("INFO","Failed to verify that channel media count is: " + entriesCount)
                return False 
    
            if memberCount + "\nmembers" != self.get_element_text(self.CHANNEL_MEMBER_COUNT, 20).lower():
                writeToLog("INFO","Failed to verify that channel member count is: " + memberCount)
                return False 
            
            if subscriberCount + "\nsubscribers" != self.get_element_text(self.CHANNEL_SUBSCRIBER_COUNT, timeout=20).lower():
                writeToLog("INFO","Failed to verify that channel subscriber count is: " + subscriberCount)
                return False 
            
            if (managerName.lower() in self.get_element_text(self.CHANNEL_MANGER_NAME_OLD_UI, timeout=20).lower()) == False:
                writeToLog("INFO","Failed to verify channel manager name: " + managerName)
                return False 
            
            if appearsInCategoryName != '':
                tmp_chnnelAppearIn = (self.CHANNEL_APPEARS_IN_CATEGORY_NAME[0], self.CHANNEL_APPEARS_IN_CATEGORY_NAME[1].replace('CATEGORY_NAME', appearsInCategoryName))
                if self.is_visible(tmp_chnnelAppearIn) == False:
                    writeToLog("INFO","Failed to verify channel appear in category: " + appearsInCategoryName)
                    return False 
            
        writeToLog("INFO","Success, All channel information was verified")
        return True
        
    # Author: Michal Zomper
    # filter type name need to be without the word channels only type like, for exp: filter type 'Channels I am subscribed to' the filter type will be 'I am subscribed to' 
    def selectViewChannelFilterInMyChannelsPage(self, filterType):
        if self.clsCommon.isElasticSearchOnPage() == True:
            if self.click(self.clsCommon.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                writeToLog("INFO","FAILED to click on filters button in my channels page")
                return False
            sleep(2)
                
            tmp_filter = (self.clsCommon.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.clsCommon.myMedia.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace('DROPDOWNLIST_ITEM', filterType.value)) 
            if self.click(tmp_filter, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on filter type: channels " + filterType.value)
                return False
            
            # close filters
            if self.click(self.clsCommon.myMedia.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20) == False:
                writeToLog("INFO","FAILED to click on filters button in my channels page")
                return False
            sleep(2)
                
        else:
            if self.click(self.MY_CHANNELS_VIEW_CHANNELS_FILTER_BUTTON, 15) == False:
                writeToLog("INFO","FAILED to click on view channel filter button")
                return False  
            
            tmp_filter = (self.MY_CHANNELS_CHOOSE_VIEW_CHANNEL_FILTER[0], self.MY_CHANNELS_CHOOSE_VIEW_CHANNEL_FILTER[1].replace('VIEW_CHANNEL_FILTER', filterType.value))
            if self.click(tmp_filter, 10, multipleElements=True) == False:
                writeToLog("INFO","FAILED to select filter type: channels " + filterType.value)
                return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        writeToLog("INFO","Success, filter 'channels " + filterType.value + "' was set")
        return True
    
    
    # Author: Michal Zomper
    def verifyChannelsViaFilter(self, filterBy, channelList):
        if self.selectViewChannelFilterInMyChannelsPage(filterBy) == False:
            writeToLog("INFO","FAILED to filter view channels by: " + filterBy.value)
            return False
        
        if self.showAllChannels() == False:
            writeToLog("INFO","FAILED to show all channels")
            return False
        
        try:
            channelsInGalley = self.get_element(self.CHANNELS_PAGE_ALL_CHANNELS_LIST).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get channels list in galley")
            return False
        
        for channel in channelList:
            if channel[1] == True:
                if (channel[0].lower() in channelsInGalley) == False:
                    writeToLog("INFO","FAILED, channel '" + channel[0] + "' wasn't found in channels galley although he need to be found")
                    return False
                
            elif channel[1] == False:
                if (channel[0].lower() in channelsInGalley) == True:
                    writeToLog("INFO","FAILED, channel '" + channel[0] + "' was found in channels galley although he doesn't need to be found")
                    return False
                
        writeToLog("INFO","Success, filter and verify view channels by 'channels " + filterBy.value + "' was successful")
        return True
                    
    
    # Author: Michal Zomper
    def selectSortChannelOptionInMyChannelsPage(self, sortType):
        if self.clsCommon.isElasticSearchOnPage() == True:
            if self.click(self.MY_CHANNELS_SORTBY_BUTTON_NEWUI, 15) == False:
                writeToLog("INFO","FAILED to click on sort channel filter button")
                return False  
        else:
            if self.click(self.MY_CHANNELS_SORTBY_BUTTON_OLDUI, 15) == False:
                writeToLog("INFO","FAILED to click on sort channel filter button")
                return False  
            
        tmpSort = (self.MY_CHANNELS_CHOOSE_SORT_CHANNEL_FILTER[0], self.MY_CHANNELS_CHOOSE_SORT_CHANNEL_FILTER[1].replace('SORT_CHANNEL_FILTER', sortType))
        if self.click(tmpSort, 10, multipleElements=True) == False:
            writeToLog("INFO","FAILED to select sort type: " + sortType)
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        writeToLog("INFO","Success, sort channels by '" + sortType + "' was set")
        
        sleep(2)
        return True    
    
    
    def verifySortInMyChannels(self, sortBy, channelsList):
        if self.selectSortChannelOptionInMyChannelsPage(sortBy.value) == False:
            writeToLog("INFO","FAILED to sort channels by: " + sortBy.value)
            return False
        
        if self.showAllChannels() == False:
            writeToLog("INFO","FAILED to show all channels")
            return False
            
        try:
            channelsInGalley = self.get_element(self.CHANNELS_PAGE_ALL_CHANNELS_LIST).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get channels list in galley")
            return False
        channelsInGalley = channelsInGalley.split("\n")
        prevChannelIndex = -1
        
        for channel in channelsList:
            channelCurrentIndex = channelsInGalley.index(channel.lower())
            if prevChannelIndex > channelCurrentIndex:
                writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct. channel '" + channel + "' isn't in the right place" )
                return False
            prevChannelIndex = channelCurrentIndex
                
        writeToLog("INFO","Success, verify sort channels by '" + sortBy.value + "' was successful, all channels display in the correct order")
        return True   
    
    
    #  @Author: Michal Zomper    
    def showAllChannels(self, timeOut=60):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if len(self.get_elements(self.CHANNELS_TABLE_SIZE)) < 9:
                    writeToLog("INFO","Success, All channels are display")
                    return True 
                
        elif localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:  
            if len(self.get_elements(self.CHANNELS_TABLE_SIZE)) < 5:
                writeToLog("INFO","Success, All channels are display")
                return True 
                  
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)
        while wait_until > datetime.datetime.now():
            if self.is_present(self.CHANNELS_NO_MORE_CHANNELS_ALERT, 2) == True:
                writeToLog("INFO","Success, All channels are display")
                return True 
             
            self.clsCommon.sendKeysToBodyElement(Keys.END)
             
        writeToLog("INFO","FAILED to show all channels")
        return False  
    
    
      
    def verifyChannelDetailsOnThumbnail(self, channelName, mediaCount, memberCount, subscriberCount):
        tmpChannelDetails = (self.CHANNEL_DETAILS_ON_THUMBNAIL[0], self.CHANNEL_DETAILS_ON_THUMBNAIL[1].replace('CHANNEL_NAME', channelName))
        try:
            channelDetails = self.get_element(tmpChannelDetails).text
        except NoSuchElementException:
            writeToLog("INFO","FAILED to find channel details on thumbnail element ")
            return False
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            details = mediaCount + " Media  " + memberCount + " Members" + subscriberCount + " Subscribers"
            if details in channelDetails == False:
                writeToLog("INFO","FAILED to find channel details on thumbnail element ")
                return False
            
        else:
            mediaDetails = mediaCount + " Media  "
            if mediaDetails in channelDetails == False:
                writeToLog("INFO","FAILED to find entries details on thumbnail element")
                return False
            
            memberAndSubscriberDetails = memberCount + " Members" + subscriberCount + " Subscribers"
            if memberAndSubscriberDetails in channelDetails == False:
                writeToLog("INFO","FAILED to find members and subscribers details on thumbnail element")
                return False
            
        writeToLog("INFO","Success, All channel details that appear on the thmbnail was verified")
        return True  
    
    
    #@Author: Michal Zomper   
    def enableDisableSubscriptionOptionToChannel(self, channelName):
        if self.navigateToEditChannelPage(channelName) == False:
            writeToLog("INFO","FAILED navigate to edit channel page: " + channelName)
            return False
        
        if self.click(self.CHANNEL_DETAILS_OPTION_SUBSCRIPTION, 30) == False:
            writeToLog("INFO","FAILED to click on subscription checkbox")
            return False  
        
        if self.click(self.CHANNEL_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Save button")
            return False 
        
        if self.wait_visible(self.CHANNEL_CREATION_DONE, 45) == False:
            writeToLog("INFO","FAILED to create a Channel")
            return False 
        
        writeToLog("INFO","Success, Channel subscription option was changed successfully")
        return True 
    
    
        # Author: Tzachi Guetta
    def searchEntriesInChannel(self, entriesNames, navigateFrom, channelName):        
        # Checking if entriesNames list type
        if type(entriesNames) is list:             
            if self.clsCommon.navigateTo(enums.Location.ENTRY_PAGE, navigateFrom, channelName, True) == False:
                writeToLog("INFO","FAILED to navigate to  channel: " +  channelName)
                return False
            for entryName in entriesNames: 
                if self.searchInChannelWithoutVerifyResults(entryName) == False:
                    writeToLog("INFO","FAILED to make a search")
                    return False              
        
                if self.clsCommon.myMedia.getResultAfterSearch(entryName) == False:
                    writeToLog("INFO","FAILED to find entry '" + entryName + "' in search result")
                    return False   
                     
                writeToLog("INFO","Success entry '" + entryName + "' was found")
            return True
        
        return False
    
    
    # Author: Michal Zomper
    def searchEntryInChannel(self, entryName):
        if self.searchInChannelWithoutVerifyResults(entryName) == False:
            writeToLog("INFO","FAILED to make a search")
            return False              

        if self.clsCommon.myMedia.getResultAfterSearch(entryName) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' in search result")
            return False   
                     
        writeToLog("INFO","Success entry '" + entryName + "' was found")
        return True
    
    
    # @Author: Michal Zomper
    # Search in category without verify results
    # noQuotationMarks = True will force and wont add quotation marks at the beginning and the end of searchText(when Elastic search is enabled)
    def searchInChannelWithoutVerifyResults(self, searchText, noQuotationMarks=False):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            # Click on the magnafine glass
            if self.click(self.CHANNEL_PAGE_SEARCH_TAB, 30) == False:
                writeToLog("INFO","FAILED to click on magnafine glass in channel page")
                return False
            sleep(2)
            # Search Entry     
            try:
                self.clsCommon.myMedia.getSearchBarElement().click()
            except NoSuchElementException:
                writeToLog("INFO","FAILED to click on search bar element")
                return False
        if noQuotationMarks == False:   
            if self.clsCommon.isElasticSearchOnPage() == True:
                searchLine = '"' + searchText + '"'
            else:
                searchLine = searchText
        else: 
            searchLine = searchText
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS \
          or localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE \
          or localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
            self.clsCommon.myMedia.getSearchBarElement().send_keys(searchLine + Keys.ENTER)
        else:
            self.clsCommon.myMedia.getSearchBarElement().send_keys(searchLine)
        sleep(2)
        self.clsCommon.general.waitForLoaderToDisappear()
        
        return True
    
    
    # @Author: Inbar Willman
    # Verify that correct default sort is displayed
    def verifyChannelsDefaultSort(self, sortBy):
        tmpDefaultSort = (self.CHANNELS_DEFAULT_SORT[0], self.CHANNELS_DEFAULT_SORT[1].replace('DEFAULT_SORT', str(sortBy)))
        
        try:
            self.get_element(tmpDefaultSort)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get default sort element")
            return False
        
        return True    
    
    
    # @Author: Inbar Willman
    # Make a search in my channels page without verify results
    def searchInMyChannelsAndChannelsWithoutVerifyResults(self, search, exactName=True):
        if self.clsCommon.isElasticSearchOnPage() == True:
            if self.click(self.MY_CHANNELS_SERACH_FIELD, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
                
            sleep(1)
                
            if exactName == True: 
                searchString = '"' + search + '"'
            else:
                searchString = search
            if self.send_keys(self.MY_CHANNELS_SERACH_FIELD, searchString + Keys.ENTER, multipleElements=True) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
        else:
            if self.click(self.MY_CHANNELS_SERACH_FIELD_OLD_UI, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on name text field")
                return False
                
            sleep(1)
                
            if self.send_keys(self.MY_CHANNELS_SERACH_FIELD_OLD_UI, search, multipleElements=True) == False:
                writeToLog("INFO","FAILED to type in 'name' text field")
                return False
                
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(3) 
            
        writeToLog("INFO","Search is made successfully in my channels page")
        return True     

      
    # Author: Michal Zomper
    # The function perform upload to new media from channel page
    # each item in uploadEntrieList need to have to value from type  "UploadEntry":  
    # UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
    # if we need only 1 upload we can set :self.entry1 = UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3) 
    # and pass only self.entry1
    # if we need to upload more then 1 entry we need to pass a list of UploadEntry : self.uploadEntrieList = [self.entry1, self.entry2,....]
    def addNewContentToChannel(self, channelName, uploadEntrieList, navigateFrom= ''):
        try:
            if self.clsCommon.navigateTo(navigateTo = enums.Location.CHANNEL_PAGE, navigateFrom=navigateFrom, nameValue=channelName) == False:
                writeToLog("INFO","FAILED navigate to channel: " + self.channelName)
                return False      
            
            if type(uploadEntrieList) is list:
                for entry in uploadEntrieList:
                    if self.addNewContentToChannelWithoutNavigate(entry) == False:
                        writeToLog("INFO","FAILED to upload new media to channel")
                        return False 
            else:
                if self.addNewContentToChannelWithoutNavigate(uploadEntrieList) == False:
                    writeToLog("INFO","FAILED to upload new media to channel")
                    return False  
        except:
            return False
        
        writeToLog("INFO","Success, media was added to channel successfully")
        return True


    # Author: Michal Zomper
    #UploadEntry parameter need to have : UploadEntry(self.filePath, self.entryName1, self.description, self.tags, timeout=60, retries=3)
    def addNewContentToChannelWithoutNavigate(self, uploadEntry, application=enums.Application.MEDIA_SPACE):
        if self.click(self.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
            writeToLog("INFO","FAILED to click add to Gallery button")
            return False     
            
        sleep(4)
        self.wait_while_not_visible(self.clsCommon.channel.CHANNEL_LOADING_MSG, 30)
        
        if self.click(self.clsCommon.category.CATEGORY_ADD_NEW_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Add New at channel page")
            return False
        sleep(2)
        
        if self.click(self.clsCommon.category.CATEGORY_ADD_NEW_MEDIA_UPLOAD_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Add New -> Media upload, at channel page")
            return False
        sleep(3)
        
        if self.clsCommon.upload.uploadEntry(uploadEntry.filePath, uploadEntry.name, uploadEntry.description, uploadEntry.tags, uploadEntry.timeout,retries=1,  uploadFrom=None) == None:
            writeToLog("INFO","FAILED to upload media from channel page: " + uploadEntry.name)
            return False
        
        if application == enums.Application.MEDIA_SPACE:
            # Click 'Go To Channel'
            if self.click(self.CHANNEL_GO_TO_CHANNEL_AFTER_UPLOAD, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on 'Go To Channel'")
                return False
        else:
            if self.click(self.CHANNEL_GO_TO_MEDIA_GALLERY_AFTER_UPLOAD) == False:
                writeToLog("INFO","FAILED to click on 'Go To Media Gallery'")
                return False                
        
        return True
    
    
    # @Author: Michal Zomper
    # Search in channel when there are no results
    def searchInChannelNoResults(self, search, channelName, navigateFrom=enums.Location.MY_CHANNELS_PAGE):
        # Navigate to channel
        if self.navigateToChannel(channelName, navigateFrom) == False:
            writeToLog("INFO","FAILED navigate to channel")
            return False 
        
        # Make a search that won't return any results
        if self.searchInChannelWithoutVerifyResults(search) == False:
            writeToLog("INFO","FAILED to make a search in channel page")
            return False  
        
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == True:
            no_results_msg = self.clsCommon.category.CATEGORY_NO_RESULTS_MSG_NEW_UI
        else:
            no_results_msg = self.clsCommon.category.CATEGORY_NO_RESULTS_MSG_OLD_UI
        
        # Verify that correct message is displayed  
        if self.is_visible(no_results_msg) == False:
            writeToLog("INFO","FAILED to displayed correct message")
            return False              
            
        # Clear search content  
        self.clsCommon.myMedia.clearSearch()
            
        return True 
    
    
    # @Author: Michal Zomper
    # Verify channel table results before scrolling down in page and after scrolling down in page - After scrolling down number of table should be bigger AFTER SEARCH
    # noQuotationMarks = True will force and wont add quotation marks at the beginning and the end of searchText(when Elastic search is enabled)
    def verifyChannelTableSizeBeforeAndAfterScrollingDownInPage(self, search, pageSizeBeforeScrolling, pageSizeAfterScrolling, noQuotationMarks=False):
        # Make a search in page that will return results that are bigger than the page side
        if self.searchInChannelWithoutVerifyResults(search, noQuotationMarks) == False:
            writeToLog("INFO","FAILED to make a search in channel")
            return False         
        
        if self.clsCommon.isElasticSearchOnPage() == True:
            channelTableSizeLocator = self.clsCommon.category.CATEGORY_TABLE_SIZE_AFTER_SEARCH
        else:
            channelTableSizeLocator =  self.clsCommon.category.CATEGORY_TABLE_SIZE
            
        # due to bug in old ui that show all the entries in the page without the show more option we only check to see that all the entries are dispaly 
        if self.clsCommon.isElasticSearchOnPage() == True:                     
            # Check page size before scrolling
            channelTableSize = len(self.get_elements(channelTableSizeLocator))
            if channelTableSize != pageSizeBeforeScrolling:
                writeToLog("INFO","FAILED to display correct number of entries in results - Before scrolling down in page")
                return False   
            
            # Click outside search field
            self.click(self.CHANNEL_TYPE)
            
            # Scroll down in page in order get all entries in results for the search
            if self.clsCommon.myMedia.showAllEntries(searchIn = enums.Location.CATEGORY_PAGE, afterSearch=True) == False:
                writeToLog("INFO","FAILED to scroll down in page")
                return False      
                           
        # Check page size after scrolling
        channelTableSize = len(self.get_elements(channelTableSizeLocator))
        if channelTableSize != pageSizeAfterScrolling:
            writeToLog("INFO","FAILED to display correct number of entries in results - after scrolling down in page")
            return False   
        
        return True 
    
    
    # Author: Michal Zomper
    def editChannelMatedate(self, newChannelName="", newChanneldescription="", newchannelTags="", newChannelType='', CategoriesList=''):
        if newChannelName != "":
            if self.clear_and_send_keys(self.clsCommon.category.EDIT_CATEGORY_NAME_TEXTBOX, newChannelName) == False:
                writeToLog("INFO","FAILED to replace channel name to:'" + newChannelName + "'")
                return False
        
        if newChanneldescription != "":
            if self.clsCommon.category.fillCategoryDescription(newChanneldescription, uploadboxId=-1) == False:
                writeToLog("INFO","FAILED to replace channel description to:'" + newChanneldescription + "'")    
                return False
        
        if newchannelTags != "":
            if self.clsCommon.category.fillCategoryTags(newchannelTags, uploadboxId=-1) == False:
                writeToLog("INFO","FAILED to replace channel tags to:'" + newchannelTags + "'")    
                return False  
            
        if newChannelType != '':
            if self.selectChannelPrivacy(newChannelType) == False:
                writeToLog("INFO","FAILED to change channel type")
                return False
            
        # Click if category list is empty
        if len(CategoriesList) != 0:            
            # choose all the  categories to publish to
            for category in CategoriesList:
                tmoCategoryName = (self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.clsCommon.myMedia.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', category))
                if self.click(tmoCategoryName, 30) == False:
                    writeToLog("INFO","FAILED to select published category '" + category + "'")
                    return False  
            
        # Click Save
        if self.click(self.clsCommon.category.EDIT_CATEGORY_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'Save' button")
            return False
        sleep(3)
        
        # Wait for loader to disappear
        self.clsCommon.general.waitForLoaderToDisappear()
        
        # Wait for 'Your changes have been saved.' message
        if self.wait_visible(self.clsCommon.category.EDIT_CATEGORY_SUCCESS_MESSAGE, 45) == False:                
            writeToLog("INFO","FAILED to find success message")
            return False

        return True
    
    
    # Author: Michal Zomper
    def navigateToChannelPageFromEditChannelPage(self, channelName):
        if self.click(self.CHANNEL_GO_BACK_TO_CHANNEL_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'back to channel' button")
            return False
        
        tmpChannelName = (self.CHANNEL_PAGE_TITLE[0], self.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
        if self.wait_visible(tmpChannelName, 30) == False:
            writeToLog("INFO","FAILED navigate to Channel page")
            return False
        
        return True
    
    
    #@ Author: Inbar willman   
    # Make a search in add to channel page
    # There are two option for search - in My media tab or in SR tab
    def searchInAddToChannel(self, searchTerm, exactSearch=True, tabToSearcFrom=enums.AddToChannelTabs.MY_MEDIA):
        if tabToSearcFrom == enums.AddToChannelTabs.MY_MEDIA:
            tmpSearchBar = (self.ADD_TO_CHANNEL_SEARCH_BAR[0], self.ADD_TO_CHANNEL_SEARCH_BAR[1].replace('SEARCH_TAB', 'Search My Media'))
        
        elif tabToSearcFrom == enums.AddToChannelTabs.SHARED_REPOSITORY:
            tmpSearchBar = (self.ADD_TO_CHANNEL_SEARCH_BAR[0], self.ADD_TO_CHANNEL_SEARCH_BAR[1].replace('SEARCH_TAB', 'Search Repository'))
            
        searchBarElement = self.get_element(tmpSearchBar)
        if searchBarElement == False:
            writeToLog("INFO","FAILED to get search bar element")
            return False
        searchBarElement.click()
        if exactSearch == True:
            searchLine = '"' + searchTerm + '"'
        else:
            if self.clsCommon.isElasticSearchOnPage():
                searchLine = '"' + searchTerm + '"'
            else:
                searchLine = searchTerm
            
        searchBarElement.send_keys(searchLine + Keys.ENTER)
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
    

    #  @Author: Inbar Willman     
    # The function check the the entries add to channel (my media and SR tab) are filter correctly
    def verifySortInAddToChannel(self, sortBy, entriesList, searchIn = enums.Location.ADD_TO_CHANNEL_MY_MEDIA):
        if self.clsCommon.myMedia.SortAndFilter(enums.SortAndFilter.SORT_BY, sortBy) == False:
            writeToLog("INFO","FAILED to sort entries")
            return False
                
        if self.clsCommon.myMedia.showAllEntries(searchIn) == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False
        sleep(10)
        
        try:
            if searchIn == enums.Location.ADD_TO_CHANNEL_MY_MEDIA:
                entriesInPage = self.wait_visible(self.ADD_TO_CHANNEL_MY_MEDIA_TABLE).text.lower()
                
            elif searchIn == enums.Location.ADD_TO_CHANNEL_SR:
                    entriesInPage = self.wait_visible(self.ADD_TO_CHANNEL_SR_TABLE).text.lower() 
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False
        entriesInPage = entriesInPage.split("\n")
        
        if self.clsCommon.myMedia.verifySortOrder(entriesList, entriesInPage) == False:
            writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct")
            return False

        writeToLog("INFO","Success, My media sort by '" + sortBy.value + "' was successful")
        return True
        
        
    # @Author: Inbar Willman 
    def clearSearchInAddToChannel(self, tab = enums.AddToChannelTabs.MY_MEDIA):
        if self.clsCommon.isElasticSearchOnPage() == True:
            try:
                clear_button = self.get_elements(self.clsCommon.myMedia.MY_MEDIA_REMOVE_SEARCH_ICON_NEW_UI)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find clear search icon")
                return False
            
            if tab == enums.AddToChannelTabs.MY_MEDIA:
                clearBtn = clear_button[2]
            elif tab == enums.AddToChannelTabs.SHARED_REPOSITORY:
                clearBtn = clear_button[3]
            
            if self.clickElement(clearBtn) == False:
                writeToLog("INFO","FAILED click on the remove search icon")
                return False
        else:
            if self.click(self.clsCommon.myMedia.MY_MEDIA_REMOVE_SEARCH_ICON_OLD_UI, 15, multipleElements=True) == False:
                writeToLog("INFO","FAILED click on the remove search icon")
                return False
        self.clsCommon.general.waitForLoaderToDisappear()
             
        writeToLog("INFO","Success, search was clear from search textbox")
        return True   
    
    
    # @Author: Inbar Willman
    # Click on SR drop down menu in add to channel page   
    def navigateToSrTabInAddToChannel(self, sharedRepositoryName):
        # Click on SR drop down menu
        if self.click(self.ADD_TO_CHANNEL_SR_DROP_DOWN_MENU) == False:
            writeToLog("INFO","FAILED to click on SR drop down menu")
            return False   
        
        tmpSR = (self.ADD_TO_CHANNEL_SR_DROP_DOWN_MENU_OPTION[0], self.ADD_TO_CHANNEL_SR_DROP_DOWN_MENU_OPTION[1].replace('SR_NAME', sharedRepositoryName)) 
        
        # Click on the SR that you want to navigate to
        if self.click(tmpSR) == False:
            writeToLog("INFO","FAILED to click on SR drop down menu option")
            return False 
        
        sleep(2)
        self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
        return True       
    
    
    # @Author: Inbar Willamn
    # The function check and verify that the entries sort in the correct order in pending tab in channel and category 
    # Default location is channel page
    def verifySortAndFiltersInPendingTab(self, sortBy='', filterMediaType='',channelName ='',entriesList='', navigate=False, location=enums.Location.CHANNEL_PAGE):
        if self.sortAndFilterInPendingTab(sortBy, filterMediaType, channelName, navigate, location) == False:
            writeToLog("INFO","FAILED to sort entries")
            return False
         
        if self.showAllEntriesPendingTab() == False:
            writeToLog("INFO","FAILED to show all entries in pending tab page")
            return False
        sleep(10)
        
        try:
            entriesIncategory = self.wait_visible(self.CHANNEL_PENDING_TAB_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in pending tab")
            return False
        entriesIncategory = entriesIncategory.split("\n")
        
        # run over the list and delete tab before the entry name
        for idx, entry in enumerate(entriesIncategory):
            entriesIncategory[idx] = entry.lstrip()
        
        if self.clsCommon.myMedia.verifySortOrder(entriesList, entriesIncategory) == False:
            writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct")
            return False
        
        writeToLog("INFO","Success, Pending sort by '" + sortBy.value + "' was successful")
        return True
        
        
    # @Author: Inbar Willman
    # Navigate to pending tab - in channel and category
    def navigateToPendingaTab(self,channelName, location=enums.Location.CHANNEL_PAGE):
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
                
        elif location == enums.Location.GALLERY_PAGE:
            if self.clsCommon.kafGeneric.navigateToGallery(channelName) == False:
                writeToLog("INFO","FAILED to navigate to  gallery: " +  channelName)
                return False
                
            if self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on gallery's moderation tab")
                return False 
                
        self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
        return True
    
    
    # @Author: Inbar WIllman
    # Make a search in pending tab - channel and category - for eSearch tests
    def makeSearchInPending(self, searchTerm, exactSearch=True):
        try:
            searchBarElement = self.get_element(self.CHANNEL_PENDING_TAB_SEARCH_BAR)
        except:
            writeToLog("INFO","FAILED get Search Bar element")
            return False 
        
        if searchBarElement == False:
            writeToLog("INFO","FAILED to get search bar element")
            return False
        
        searchBarElement.click()
        if exactSearch == True:
            searchLine = '"' + searchTerm + '"'
        else:
            if self.clsCommon.isElasticSearchOnPage():
                searchLine = '"' + searchTerm + '"'
            else:
                searchLine = searchTerm
            
        searchBarElement.send_keys(searchLine + Keys.ENTER)
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True
    
    
    # @Author: Inbar Willman
    # Show all entries in pending tab
    def showAllEntriesPendingTab(self, timeOut=240):
        tmp_table_size = self.CHANNEL_PENDING_TAB_TABLE_SIZE
        loading_message = self.CHANNEL_PENDING_TAB_LOADING_ENTRIES_MSG
        no_entries_page_msg = self.CHANNEL_PENDING_TAB_NO_MORE_MEDIA_MSG                       
                
        if len(self.get_elements(tmp_table_size)) < 4:
                writeToLog("INFO","Success, All media is display")
                return True 
              
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)  
       #while wait_until > datetime.datetime.now() and self.wait_while_not_visible(self.CHANNEL_PENDING_TAB_NO_MORE_MEDIA_MSG, 1) == True:  
        while wait_until > datetime.datetime.now(): 
            if self.wait_while_not_visible(loading_message, 7) == True:
                self.clsCommon.sendKeysToBodyElement(Keys.END)
                if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
                    self.switch_to_default_content()
                    self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
                    self.get_body_element().send_keys(Keys.PAGE_DOWN)
                    self.clsCommon.sharePoint.switchToSharepointIframe()
                    self.click(self.clsCommon.channel.CHANNEL_MODERATION_TAB, multipleElements=True)
                if self.wait_element(self.CHANNEL_PENDING_TAB_NO_MORE_MEDIA_MSG, 1, multipleElements=True) != False:
                    break
                
        if self.is_present(no_entries_page_msg, 5) == True:
            writeToLog("INFO","Success, All media is display")
            sleep(1)
            # go back to the top of the page
            self.clsCommon.sendKeysToBodyElement(Keys.HOME)
            return True    
        else:
            writeToLog("INFO","FAILED to show all media")
            return False  
        
        return True
    
    # @Author: Inbar Willman
    # Verify filter in channel - media tab    
    def verifyFiltersInAddToChannel(self, entriesDict, searchIn = enums.Location.ADD_TO_CHANNEL_MY_MEDIA, noEntriesExpected=False):
        if noEntriesExpected == True:
            if self.wait_element(self.CHANNEL_NO_RESULT_FILTER, 5, multipleElements=True) != False:
                writeToLog("INFO", "PASSED, no entries are displayed")
                return True
            else:
                writeToLog("INFO", "Some entries are present, we will verify the dictionaries")
                
        if self.clsCommon.myMedia.showAllEntries(searchIn) == False:
            writeToLog("INFO","FAILED to show all entries in Add to channel")
            return False
        
        if searchIn == enums.Location.ADD_TO_CHANNEL_MY_MEDIA:            
            entriesInAddToChannel = self.wait_visible(self.ADD_TO_CHANNEL_MY_MEDIA_TABLE).text.lower()
            if entriesInAddToChannel == False:
                writeToLog("INFO","FAILED to get entries list in channel")
                return False                
            
        elif searchIn == enums.Location.ADD_TO_CHANNEL_SR:
            entriesInAddToChannel = self.wait_visible(self.ADD_TO_CHANNEL_SR_TABLE).text.lower()
            if entriesInAddToChannel == False:
                writeToLog("INFO","FAILED to get entries list in channel")
                return False 

        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInAddToChannel == False:
                if (entry.lower() in entriesInAddToChannel) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in add to channel although he need to be found")
                    return False
                 
            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInAddToChannel == True:
                if (entry.lower() in entriesInAddToChannel) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in add to channel although he doesn't need to be found")
                    return False
                 
        writeToLog("INFO","Success, Only the correct media display in add to channel")
        return True
    
    
    # @Author: Inbar Willman
    # Verify filter in channel - pending tab    
    def verifyFiltersInPendingTab(self, entriesDict, noEntriesExpected=False, searchIn = enums.Location.ADD_TO_CHANNEL_MY_MEDIA):
        if noEntriesExpected == True:
            if self.wait_visible(self.CHANNEL_NO_RESULT_FILTER_MODERATION, 1, multipleElements=True) != False:
                writeToLog("INFO", "PASSED, no entries are displayed")
                return True
            else:
                writeToLog("INFO", "Some entries are present, we will verify the dictionaries")
                
        if self.showAllEntriesPendingTab() == False:
            writeToLog("INFO","FAILED to show all entries in pending tab page")
            return False
        sleep(10)
        
        entriesIncategory = self.wait_visible(self.CHANNEL_PENDING_TAB_TABLE).text.lower()
        if entriesIncategory == False:
            writeToLog("INFO","FAILED to get entries list in channel")
            return False
             
        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInAddToChannel == False:
                if (entry.lower() in entriesIncategory) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in channel - pending tab although he need to be found")
                    return False
                 
            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInAddToChannel == True:
                if (entry.lower() in entriesIncategory) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in channel - pending tab although he doesn't need to be found")
                    return False
                 
        writeToLog("INFO","Success, Only the correct media display in channel - pending tab")
        return True   
    
    
    # @Author: Oded.berihon
    # Verify filter in channel - channel page   
    def verifyEntriesDisplay(self, entriesDict, verifyIn=enums.Location.CHANNEL_PAGE, noEntriesExpected=False):
        if noEntriesExpected == True:
            if self.wait_visible(self.CHANNEL_NO_RESULT_FILTER, 1, multipleElements=True) != False:
                writeToLog("INFO", "PASSED, no entries are displayed")
                return True
            else:
                writeToLog("INFO", "Some entries are present, we will verify the dictionaries")
                
        if self.showAllEntriesInChannelCategoryPage() == False:
            writeToLog("INFO","FAILED to show all entries in pending tab page")
            return False
        sleep(10)
        
        if verifyIn == enums.Location.CHANNEL_PAGE or verifyIn == enums.Location.CATEGORY_PAGE:
            entriesTable = self.wait_visible(self.clsCommon.category.CATEGORY_GALLEY_ALL_MEDIA_TABLE).text.lower()
        else:
            writeToLog("INFO","Wrong enum page type")    
            
        if entriesTable == False:
            writeToLog("INFO","FAILED to get entries list in channel")
            return False
             
        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInAddToChannel == False:
                if (entry.lower() in entriesTable) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in gallery page although he need to be found")
                    return False
                 
            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInAddToChannel == True:
                if (entry.lower() in entriesTable) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in gallery page although he doesn't need to be found")
                    return False
                 
        writeToLog("INFO","Success, Only the correct media display in gallery page")
        return True
        
    
    # @Author: Inbar Willman
    # Navigate to add to category page
    def navigateToAddToChannel(self, channelName, navigateFrom=enums.Location.MY_CHANNELS_PAGE, forceNavigate=False):
        # Navigate to category
        if self.navigateToChannel(channelName, navigateFrom, forceNavigate) == False:
            writeToLog("INFO","FAILED  to navigate to: " + channelName)
            return False   
        
        # Click on 'Add to channel'
        if self.click(self.CHANNEL_ADD_TO_CHANNEL_BUTTON) == False:
            writeToLog("INFO","FAILED to click add to channel button")
            return False           
        
        # wait until loading message disappear    
        sleep(1)
        self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30)
        
        return True   
    
    
    # @Author: Oded.berihon
    # Show all entries both in channel and category page    
    def showAllEntriesInChannelCategoryPage(self, timeOut=30):
        tmp_table_size = self.CHANNEL_CHANNEL_PAGE_TABLE_SIZE
        loading_message = self.CHANNEL_PENDING_TAB_LOADING_ENTRIES_MSG
        no_entries_page_msg = self.CHANNEL_PENDING_TAB_NO_MORE_MEDIA_MSG                       
                
        if len(self.get_elements(tmp_table_size)) < 4:
            writeToLog("INFO","Success, All media is display")
            return True 
              
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)  
        while wait_until > datetime.datetime.now():                       
            if self.wait_while_not_visible(loading_message, 10) == True:
                    self.clsCommon.sendKeysToBodyElement(Keys.END)
            
        if self.is_present(no_entries_page_msg, 5) == True:
            writeToLog("INFO","Success, All media is display")
            sleep(1)
            # go back to the top of the page
            self.clsCommon.sendKeysToBodyElement(Keys.HOME)
            return True    
        else:
            writeToLog("INFO","FAILED to show all media")
            return False  
        
        return True    
    
    
    # Author: Michal Zomper   
    def varifyChannelyMatedate(self, channelName, channelDescription, channelTags, channelType, appearsInCategoryName):
        tmpChannelName = (self.CHANNEL_PAGE_TITLE[0], self.CHANNEL_PAGE_TITLE[1].replace('CHANNEL_TITLE', channelName))
        if self.wait_visible(tmpChannelName, 30) == False:
            writeToLog("INFO","FAILED to verify channel name")
            return False
        
        tmpChannelDescription = (self.clsCommon.category.CATEGORY_DESCRIPTION[0], self.clsCommon.category.CATEGORY_DESCRIPTION[1].replace('CATEGORY_DESCRIPTION', channelDescription))
        if self.wait_visible(tmpChannelDescription, 30) == False:
            writeToLog("INFO","FAILED to verify channel description")
            return False
        
        tmpChannelTags = (self.clsCommon.category.CATEGORY_TAGS[0], self.clsCommon.category.CATEGORY_TAGS[1].replace('CATEGORY_TAGS', channelTags[:-1]))
        if self.wait_visible(tmpChannelTags, 30) == False:
            writeToLog("INFO","FAILED to verify channel tags")
            return False
        
        if channelType.value in self.get_element_text(self.CHANNEL_TYPE, 20).lower() == False:
            writeToLog("INFO","Failed to verify that channel type is : " + channelType)
            return False 
        
        tmp_chnnelAppearIn = (self.CHANNEL_APPEARS_IN_CATEGORY_NAME[0], self.CHANNEL_APPEARS_IN_CATEGORY_NAME[1].replace('CATEGORY_NAME', appearsInCategoryName))
        if self.click(self.CHANNEL_APPEARS_IN_BUTTON, 20, multipleElements=True) == False:
            writeToLog("INFO","Failed to click on appears in button")
            return False
        
        if self.is_visible(tmp_chnnelAppearIn) == False:
            writeToLog("INFO","Failed to verify channel appear in category: " + appearsInCategoryName)
            return False
        
        writeToLog("INFO","Success, channel metadata was verified successfully")
        return True
    
    
    # Author: Horia Cus
    # This function switches between the media and pending tab and then refreshes the page
    def switchBetweenMediaAndPendingWithRefresh(self, switchToPending=False, switchToMedia=False, location=enums.Location.CHANNEL_PAGE):
        if location == enums.Location.CHANNEL_PAGE:  
            tmpLocator = self.CHANNEL_MODERATION_TAB
            
        elif location == enums.Location.CATEGORY_PAGE:
            tmpLocator = self.clsCommon.category.CATEGORY_MODERATION_TAB
            
        else:
            writeToLog("INFO", "Please specify a location")
            return False    
               
        if switchToPending == True:
            self.driver.refresh() 
            
            if self.wait_element(tmpLocator, 15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to load the page after refresh")
                return False     
                        
            if self.click(tmpLocator, 3, multipleElements=True) == False:
                writeToLog("INFO","FAILED to switch from media tab to pending tab")
                return False
                
            if self.wait_while_not_visible(self.CHANNEL_LOADING_MSG, 30) == False:
                writeToLog("INFO","FAILED to load the pending tab entries")
                return False                        
            
        elif switchToMedia == True:                     
            self.driver.refresh() 
            
            if self.wait_visible(self.CHANNEL_MEDIA_TAB_ACTIVE, 15, multipleElements=True) == False:
                writeToLog("INFO","FAILED to load the page after refresh")
                return False
            
        return True
                    
    
    # Author: Horia Cus
    # This function selects a specific entry or entryList and then approves or rejects them using bulk option
    def pendingBulkRejectAndApprove(self, entryList, moderateAction=''):
        if moderateAction == enums.PendingModerateAction.APPROVE:
            tmpLocator = self.CHANNEL_APPROVE_BUTTON_BULK
        elif moderateAction == enums.PendingModerateAction.REJECT:
            tmpLocator = self.CHANNEL_REJECT_BUTTON_BULK
        
        else:
            writeToLog("INFO", "Please specify a moderate action for the pending tab")
            return False
        
        if self.showAllEntriesPendingTab(240) == False:
            writeToLog("INFO", "Failed to displayed the entries")
            return False
            
        if type(entryList) is list:
            for entry in entryList:
                tmpEntry = (self.CHANNEL_ENTRY_PARENT_CHECKBOX[0], self.CHANNEL_ENTRY_PARENT_CHECKBOX[1].replace('ENTRY_NAME', entry))
                entryId = self.clsCommon.upload.extractEntryIDFromCheckBox(tmpEntry)
                if entryId == False:
                    return False 
                
                tmpEntryCheckBox = (self.CHANNEL_ENTRY_ID_CHECKBOX[0], self.CHANNEL_ENTRY_ID_CHECKBOX[1].replace('ENTRY_ID', entryId))
                if self.click(tmpEntryCheckBox) == False:
                    writeToLog("INFO","FAILED to select the checkbox entry for: " + entry)
                    return False
        else:
            if entryList != '':
                tmpEntry = (self.CHANNEL_ENTRY_PARENT_CHECKBOX[0], self.CHANNEL_ENTRY_PARENT_CHECKBOX[1].replace('ENTRY_NAME', entryList))
                entryId = self.clsCommon.upload.extractEntryIDFromCheckBox(tmpEntry)
                if entryId == False:
                    return False 
                
                tmpEntryCheckBox = (self.CHANNEL_ENTRY_ID_CHECKBOX[0], self.CHANNEL_ENTRY_ID_CHECKBOX[1].replace('ENTRY_ID', entryId))
                if self.click(tmpEntryCheckBox) == False:
                    writeToLog("INFO","FAILED to select the checkbox entry for: " + entryList)
                    return False
        
        if self.click(tmpLocator, timeout=5, multipleElements=True) == False:
            writeToLog("INFO", "Failed to click on the approve/reject bulk button")
            return False
        
        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "Failed to save the changes")
            return False
        
        if self.wait_element(self.CHANNEL_BULK_POP_UP, timeout=4, multipleElements=True) != False:
            if self.click(self.CHANNEL_BULK_POP_UP_APPROVE, timeout=3, multipleElements=True) == False:
                writeToLog("INFO", "Failed to moderate the bulk entries")
            
            if self.clsCommon.general.waitForLoaderToDisappear() == False:
                writeToLog("INFO", "Failed to save the changes")
                return False    
        
        return True
    

    # Author: Horia Cus
    # This function verifies that all the specified channels are displayed
    def verifyChannelIsPresent(self, channelList):
        if self.showAllChannels(60) == False:
            writeToLog("INFO", "Failed to display all the entries")
            return False

        for entry in channelList:           
            if channelList[entry] == True:
                tmp_channelName = (self.MY_CHANNELS_HOVER[0], self.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', entry))
                if self.is_visible(tmp_channelName) == False:
                    writeToLog("INFO","FAILED to find channel '" + entry + "' after search in my channels")
                    return False
                 
            elif channelList[entry] == False:
                tmp_channelName = (self.MY_CHANNELS_HOVER[0], self.MY_CHANNELS_HOVER[1].replace('CHANNEL_NAME', entry))
                if self.is_present(tmp_channelName, 1) == True:
                    writeToLog("INFO","FAILED to find channel '" + entry + "' after search in my channels")
                    return False
            
            else:
                writeToLog("INFO", "Please specify if the channel should be displayed or not")
                return False
            
        return True    