from base import *
import clsTestService
import enums
from selenium.webdriver.common.keys import Keys
from PIL import Image


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
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST                        = ('xpath', "//button[@id='entryActionsMenuBtn']")
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_EDIT_BUTTON            = ('xpath', "//span[@id='tabLabel-Edit']")  
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_KEA_BUTTON             = ('xpath', "//span[@id='tabLabel-editor']")    
    ENTRY_PAGE_DESCRIPTION                                 = ('xpath', "//div[@class='row-fluid normalWordBreak']")
    ENTRY_PAGE_TAGS                                        = ('class_name', "tagsWrapper")    
    ENTRY_PAGE_ADDTOPLAYLIST_BUTTON                        = ('id', "Addtoplaylists")  
    ENTRY_PAGE_PUBLISH_BUTTON                              = ('id', "tab-Publish")
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_DELETE_BUTTON          = ('id', "tab-Delete")
    ENTRY_PAGE_CONFIRM_DELETE_BUTTON                       = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    ENTRY_PAGE_DOWNLOAD_TAB                                = ('xpath', "//a[@id='tab-download-tab']")
    ENTRY_PAGE_MEDIA_IS_BEING_PROCESSED                    = ('xpath', "//span[contains(@class,'media-processing') and contains(text(),'is being processed')]")
    ENTRY_PAGE_PLAYER_IFRAME                               = ('xpath',"//iframe[@id='kplayer_ifp' and @class='mwEmbedKalturaIframe']") 
    ENTRY_PAGE_PLAYER_IFRAME1                              = ('class_name','mwEmbedKalturaIframe')
    ENTRY_PAGE_PLAYER_IFRAME2                              = ('id','kplayer_ifp')
    ENTRY_PAGE_CHAPTER_MENU_ON_THE_PLAYER                  = ('id', 'sideBarContainerReminderContainer') # This is the icon on the top left of the player that show all the slides that were added 
    ENTRY_PAGE_SHARE_TAB                                   = ('xpath', '//a[@id="tab-share-tab"]')
    ENTRY_PAGE_SHARE_LINK_TO_MEDIA_OPTION                  = ('xpath', '//li[@id="directLink-tab" and @class="active"]')
    ENTRY_PAGE_SHARE_EMBED_OPTION                          = ('id', 'embedTextArea-pane-tab')
    ENTRY_PAGE_SHARE_EMAIL_OPTION                          = ('id', 'emailLink-tab')
    ENTRY_PAGE_LOADING                                     = ('xpath', '//div[@class="message" and text()="Loading..."]')
    ENTRY_PAGE_EMBED_TEXT_AREA                             = ('id', 'embedTextArea')
    ENTRY_PAGE_COMMENT_TEXT_AREA                           = ('xpath', '//textarea[@id="commentsbox"]')
    ENTRY_PAGE_COMMENT_TIME_CHECKBOX                       = ('xpath', "//label[contains(@class,'control-label inline')]")
    ENTRY_PAGE_COMMENT_TIME_STAMP                          = ('xpath', '//a[@href="#" and @data-seconds="TIME_INTEGER"]')
    ENTRY_PAGE_COMMENT_TEXT_SECTION                        = ('xpath', '//div[@class="commentText"]')
    ENTRY_PAGE_COMMENT_ADD_BUTTON                          = ('xpath', '//input[@id="add-comment"]')
    ENTRY_PAGE_COMMENTS_PANEL                              = ('xpath', "//div[@id='commentsWrapper']")
    ENTRY_PAGE_DETAILS_BUTTON                              = ('xpath', "//a[@id='tab-Details' and contains(@class, 'btn responsiveSizePhone tabs-container__button tab-Details')]")
    ENTRY_PAGE_LIKE_BUTTON                                 = ('xpath', "//span[@id='likes']")
    ENTRY_PAGE_COMMENT_SECTION                             = ('xpath', '//div[@class="commentText"]/p[text()="COMMENT_TEXT"]')
    ENTRY_PAGE_CLOSE_DISCUSSION_MSG                        = ('xpath', '//h4[@class="muted" and text()="Discussion is closed"]')
    ENTRY_PAGE_COMMENT_ID                                  = ('xpath', '//div[@class="comment row-fluid "]')
    ENTRY_PAGE_REPLY_COMMENT                               = ('xpath', '//a[contains(@href, "/commentId/COMMENT_ID") and @data-track="Comment Reply"]')
    ENTRY_PAGE_REPLY_COMMENT_TEXT_AREA                     = ('xpath', '//textarea[@id="commentsbox" and @title="Add a Reply"]')
    ENTRY_PAGE_REPLY_COMMENT_ADD_BUTTON                    = ('xpath', '//form[@id="addComment_COMMENT_ID"]/div[@class="pull-right"]')
    ENTRY_PAGE_RELATED_MEDIA                               = ('xpath', '//div[@id="sideSelectWrap"]')
    ENTRY_PAGE_RELATED_MEDIA_OPTION                        = ('xpath', "//a[contains(@id,'Related')]")
    ENTRY_PAGE_MY_MEDIA_OPTION                             = ('xpath', "//a[contains(@id,'Sidemymedia')]")
    ENTRY_PAGE_MY_MEDIA_SIDE_BAR_ENTRIES                   = ('xpath', '//div[@class="photo-group thumb_wrapper" and @title="ENTRY_NAME"]')
    ENTRY_PAGE_ATTACHMENTS_TAB                             = ('xpath', '//a[contains(@id,"attachments-tab")]')# USE multipleElements=True
    ENTRY_PAGE_DOWNLOAD_ATTACHMENTS_ICON                   = ('xpath', '//i[@class="icon-download icon-large"]')
    ENTRY_PAGE_RELATED_MEDIA_TABLE                         = ('xpath', '//table[@class="table table-hover table-bordered thumbnails table-condensed"]/tbody/tr')
    ENTRY_PAGE_CAPTION_SEARCH_BAR_OLD_UI                   = ('xpath', "//input[@id='captionSearch']")
    ENRTY_PAGE_SEARCH_ICON                                 = ('xpath', "//div[@id='entryeSearchForm']") 
    ENTRY_PAGE_CAPTION_SEARCH_BAR                          = ('xpath', "//input[@class='searchForm__text' and @placeholder='Search in video']")
    ENTRY_PAGE_CAPTION_TIME_RESULT                         = ('xpath', "//a[@class='results__result-item--time cursor-pointer' and contains(text(), 'CAPTION_TIME')]") 
    ENTRY_PAGE_CAPTION_TIME_RESULT_OLD_UI                  = ('xpath', "//a[@class='captions_search_result' and contains(text(), 'CAPTION_TIME')]") 
    ENTRY_PAGE_CAPTION_SEARCH_RESULT_OLD_UI                = ('xpath', "//ul[@id='kitems']")
    ENTRY_PAGE_CAPTION_SEARCH_RESULT                       = ('xpath', "//div[@class='results-details-container__group']")
    ENTRY_SEARCH_CLOSE_ICON                                = ('xpath', "//form[contains(@class,'noBorder searchForm')]//div//div//i[contains(@class,'v2ui-close-icon')]")
    ENTRY_SEARCH_NO_RESULTS_TEXT                           = ('xpath', "//div[@class='results-details-container' and text()='No results found']")
    ENTRY_FIELD_ICON_IN_RESULTS                            = ('xpath', '//i[contains(@title,"FIELD_NAME")]')
    ENTRY_SEARCH_SHOW_LESS                                 = ('xpath', "//a[contains(@aria-label,'Show Less')]")
    ENTRY_SEARCH_TRIGGER                                   = ('xpath', "//form[contains(@class,'noBorder searchForm')]//div//div//i[contains(@class,'icon-search')]")
    ENTRY_SEARCH_SHOW_MORE                                 = ('xpath', "//span[contains(@class,'results-summary__show-more--text hidden-phone')]")
    ENTRY_SEARCH_SHOW_ALL                                  = ('xpath', "//a[contains(@aria-label,'Show All')]")
    ENTRY_SEARCH_DROP_DOWN_MENU                            = ('xpath', "//span[contains(@class,'hidden-phone hidden-tablet')]")
    ENTRY_SEARCH_DROP_DOWN_MENU_LIST                       = ('xpath', "//a[@role='menuitem' and text()='LABEL']")  
    ENTRY_SEARCH_RESULTS_CONTAINER                         = ('xpath', "//div[contains(@class,'results-details-container__group')]//div[2]//span[contains(., 'TEXT')]")
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_CREATE_CLIP_BUTTON     = ('xpath', '//span[@id="tabLabel-editor" and text()="Create Clip"]')
    ENTRY_PAGE_COMMENTS_PART_TITLE                         = ('xpath', '//a[@id="comments-tab-tab"]')
    ENTRY_PAGE_ELEMENT_LOADER_SHARE                        = ('xpath', '//div[@class="elementLoader"]')
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_ANALYTICS_OPTION       = ('xpath', '//span[@id="tabLabel-userreports" and text()="Analytics"]')
    ENTRY_PAGE_CAPTIONS_REQUESTS_OPTION                    = ('xpath', '//span[@class="tabLabel" and text()=" Captions Requests"]')
    ENTRY_PAGE_BODY                                        = ('xpath', '//body[contains(@class,"entry")]')
    ENTRY_PAGE_HEADER_NAVBAR                               = ('xpath', '//div[contains(@class,"navbar") and @id="header"]')
    ENTRY_PAGE_FOOTER_NAVBAR                               = ('xpath', '//div[contains(@class,"navbar") and @id="footer"]')
    ENTRY_PAGE_HEADER_LOGO                                 = ('xpath', '//a[contains(@href,"/") and contains(@class,"brand")]')
    ENTRY_PAGE_HEADER_LOGO_IMAGE                           = ('xpath', '//a[contains(@href,"/") and contains(@class,"logoImg brand")]')
    ENTRY_PAGE_SIDEBAR                                     = ('xpath', '//div[@id="mySidebar"]')
    ENTRY_PAGE_ENTRY_PROPERTIES                            = ('xpath', '//div[@class="row-fluid tight"]')
    ENTRY_PAGE_ENTRY_TABS_CONTAINER                        = ('xpath', '//ul[contains(@class,"inline tabs-container")]')
    ENTRY_PAGE_COMMENT_TAB_PANEL                           = ('xpath', '//div[@id="comments-tab-pane"]')
    #=============================================================================================================
    
    def navigateToEntryPageFromMyMedia(self, entryName):
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in entry page, Entry name: '" + entryName + "'")
            return True      
        
        self.clsCommon.myMedia.searchEntryMyMedia(entryName)
        self.clsCommon.myMedia.clickEntryAfterSearchInMyMedia(entryName)
        # Wait page load - wait for entry title
        if self.wait_visible(tmp_entry_name, 30) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "' during the first try")
            # Because the search may have not be triggered, we added this redundancy step
            self.clsCommon.myMedia.getSearchBarElement().send_keys(Keys.ENTER)
            sleep(1)
            self.clsCommon.general.waitForLoaderToDisappear()
            self.clsCommon.myMedia.clickEntryAfterSearchInMyMedia(entryName)
            if self.wait_visible(tmp_entry_name, 20) == False:
                writeToLog("INFO","FAILED to enter entry page: '" + entryName + "' during the second try")
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
        sleep(2)
           
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
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + str(enums.Location.MY_MEDIA))
                return False  
            
            tmpEntryName = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
            if self.wait_element(tmpEntryName, 15) == False:
                writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
                return False
            
        elif navigateFrom == enums.Location.CATEGORY_PAGE:
            if self.navigateToEntryPageFromCategoryPage(entryName, categoryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + str(enums.Location.CATEGORY_PAGE))
                return False  
                
        elif navigateFrom == enums.Location.CHANNEL_PAGE:
            if self.clsCommon.channel.naviagteToEntryFromChannelPage(entryName, channelName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + str(enums.Location.CHANNEL_PAGE))
                return False
            
        elif navigateFrom == enums.Location.UPLOAD_PAGE:
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
                self.click(self.clsCommon.upload.UPLOAD_PAGE_TITLE)
                self.get_body_element().send_keys(Keys.PAGE_DOWN)
                
            sleep(2)
            if self.click(self.clsCommon.upload.UPLOAD_GO_TO_MEDIA_BUTTON, multipleElements=True) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + str(enums.Location.UPLOAD_PAGE))
                return False  
            
            sleep(5)
            tmpEntryName = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
            if self.wait_element(tmpEntryName, 15) == False:
                writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
                return False
            
        elif navigateFrom == enums.Location.MY_HISTORY:
            if self.navigateToEntryPageFromMyHistory(entryName) == False:
                writeToLog("INFO","FAILED to navigate to entry '" + entryName + "' from " + str(enums.Location.MY_HISTORY))
                return False   
                
        elif navigateFrom == enums.Location.HOME:
            if self.navigateToEntryPageFromHomePage(entryName) == False:
                writeToLog("INFO","FAILED to navigate to entry '" + entryName + "' from " + str(enums.Location.HOME))
                return False 
            
        elif navigateFrom == enums.Location.KEA_PAGE:
            if self.clsCommon.kea.navigateToEntryPageFromKEA(entryName) == False:
                writeToLog("INFO","FAILED to navigate to entry '" + entryName + "' from " + str(enums.Location.KEA_PAGE))
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
        
        sleep(3)
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
            
            if self.click(self.ENTRY_PAGE_DOWNLOAD_TAB, 30, multipleElements=True) == False:
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
    
    
    def waitTillMediaIsBeingProcessed(self, timeout=450):
        sleep(6)
        self.wait_while_not_visible(self.ENTRY_PAGE_MEDIA_IS_BEING_PROCESSED, timeout)
        if self.wait_visible(self.clsCommon.player.PLAYER_IFRAME, 90) == False:
            writeToLog("INFO", "FAILED to verify the player Iframe while waiting for the media to be processed ")
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
        if self.click(self.ENTRY_PAGE_SHARE_TAB, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on share tab")
            return False
    
    
    # @Author: Inbar Willman     
    def chooseShareOption(self, shareOption = enums.EntryPageShareOptions.EMBED):
        if shareOption == enums.EntryPageShareOptions.EMBED:
            if self.click(self.ENTRY_PAGE_SHARE_EMBED_OPTION, multipleElements=True) == False:
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
        sleep(3)  
        
        if self.chooseShareOption() == False:
            writeToLog("INFO","FAILED to click on embed tab")
            return False
        sleep(3)
        
        if self.wait_while_not_visible(self.ENTRY_PAGE_ELEMENT_LOADER_SHARE, 30) == False:
            writeToLog("INFO", "FAILED, during the transition to embed tab, it remained in infinite loading")
            return False
        
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        if self.wait_while_not_visible(self.ENTRY_PAGE_LOADING) == False:
            writeToLog("INFO","FAILED - Loading message is still displayed")
            return False  
        embed_text = self.get_element_text(self.ENTRY_PAGE_EMBED_TEXT_AREA)
        if embed_text == None:
            return False
        
        sleep(3)
        return embed_text
    
    
    # Author: Michal Zomper 
    def addComment(self, comment):
        if self.insertCommentToTextField(comment) == False:
            writeToLog("INFO", "FAILED to add the following comment " + str(comment) + " to the text field")
            return False

        if self.clickAddComment(comment) == False:
            writeToLog("INFO", "FAILED to add the following comment " + str(comment) + " to the entry list")
            return False
           
        return True
    
    
    # Author: Michal Zomper 
    def addComments(self, commentsList):
        for comment in commentsList:
            if self.addComment(comment) == False:
                writeToLog("INFO","FAILED to add comment")
                return False
                
        writeToLog("INFO","Success, All comments were added successfully to entry")       
        return True
        
        
    # Author: Michal Zomper   
    def LikeUnlikeEntry(self, isLike):
        self.clsCommon.sendKeysToBodyElement(Keys.HOME)
        
        # Check the amount of likes for the entry before click the like\unlike button
        prev_likeAmount = self.wait_visible(self.ENTRY_PAGE_LIKE_BUTTON, timeout=15)
        if prev_likeAmount == False:
            writeToLog("INFO","FAILED to find like button")
            return False
        
        sleep(2)
        prev_likeAmount = prev_likeAmount.text
        
        if self.click(self.ENTRY_PAGE_LIKE_BUTTON, 10) == False:
            writeToLog("INFO","FAILED to click on like button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        
        # Check the amount of likes for the entry after click the like\unlike button
        after_likeAmount = self.wait_visible(self.ENTRY_PAGE_LIKE_BUTTON, timeout=15)
        if after_likeAmount == False:
            writeToLog("INFO","FAILED to find like button")
            return False
        
        after_likeAmount = after_likeAmount.text

        # like the page
        if isLike == True:
            if int(prev_likeAmount) >= int(after_likeAmount):
                writeToLog("INFO","FAILED to click on like button, the number of likes are: " + str(after_likeAmount) + " and need to be: " + str(prev_likeAmount))
                return False
            writeToLog("INFO","Success, entry was liked successfully")
            return True
                 
        # unlike the page
        elif isLike == False:
            if int(prev_likeAmount) <= int(after_likeAmount):
                writeToLog("INFO","FAILED to click on unlike button, the number of likes are: " + int(after_likeAmount) + " and need to be: " + int(prev_likeAmount))
                return False
            writeToLog("INFO","Success, entry was unlike successfully")
            return True
    
    
    # @Author: Inbar Willman
    def checkEntryCommentsSection(self, comment, isCommentsDisabled, isDiscussionClose):
        # Scroll down in page to comment section
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
         
        comment_section = (self.ENTRY_PAGE_COMMENT_SECTION[0], self.ENTRY_PAGE_COMMENT_SECTION[1].replace('COMMENT_TEXT', comment))
        # If disabled comments is enabled (includes if close discussion is enabled)
        if isCommentsDisabled == True:
            # Check that entry's comments isn't displayed
            if self.is_visible(comment_section) == True:
                writeToLog("INFO","FAILED - comments still displayed")
                return False 
        
        # If close discussion is enabled but disabled comments is disabled     
        if isDiscussionClose == True and isCommentsDisabled == False:
                # Wait until close discussion message is displayed 
                if self.wait_visible(self.ENTRY_PAGE_CLOSE_DISCUSSION_MSG, timeout=20) == False:
                    writeToLog("INFO","FAILED to displayed close discussion message")
                    return False             
            
                # Check that entry's comments is displayed
                if self.is_visible(comment_section) == False:
                    writeToLog("INFO","FAILED - comments isn't displayed")
                    return False           
            
        # Check that there is no option to add comments - relevant for both close discussion and disabled comments
        if self.wait_element(self.ENTRY_PAGE_COMMENT_TEXT_AREA, timeout=10) == True:
            writeToLog("INFO","FAILED - add new comment box is still displayed")
            return False                  
        
        return True       
    
       
    # @Author: Inbar Willman
    def replyComment(self, replyComment):
        sleep(2)
        # Get comment Id
        tmp_comment_id = self.get_element(self.ENTRY_PAGE_COMMENT_ID)
        comment_id = tmp_comment_id.get_attribute("data-comment-id")
        
        # Click on replay button
        tmp_replay_btn = (self.ENTRY_PAGE_REPLY_COMMENT[0], self.ENTRY_PAGE_REPLY_COMMENT[1].replace('COMMENT_ID', comment_id))
        if self.click(tmp_replay_btn, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on replay button")
            return False   
        sleep(1)
        # Add new replay comment
        # Click on replay comment area
        if self.click(self. ENTRY_PAGE_REPLY_COMMENT_TEXT_AREA, 5, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click in the comment text box area")
            return False
        
        # Insert comment text
        if self.send_keys(self. ENTRY_PAGE_REPLY_COMMENT_TEXT_AREA, replyComment + Keys.SPACE, multipleElements=True) == False:
            writeToLog("INFO","FAILED to add comment")
            return False
        sleep(2)
        
        #Click on add button
        self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN)
        tmp_add_btn = (self.ENTRY_PAGE_REPLY_COMMENT_ADD_BUTTON[0], self.ENTRY_PAGE_REPLY_COMMENT_ADD_BUTTON[1].replace('COMMENT_ID', comment_id))
        if self.click(tmp_add_btn, 15) == False:
            writeToLog("INFO","FAILED to click on add comment button")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        
        # verify reply was added
        tmp_comments = self.get_element_text(self.ENTRY_PAGE_COMMENTS_PANEL)
        if replyComment in tmp_comments == False:
            writeToLog("INFO","FAILED to find added comment")
            return False
           
        writeToLog("INFO","Success, comment: '" + replyComment +"'  was added to entry")
        return True
    
    
    # @Author: Inbar Willman
    # Choose option in related media drop down in media side bar
    # Related media (default) or My Media
    def selectRelatedMediaOption(self, relatedMediaOption=enums.ReleatedMedia.MY_MEDIA):
        # Click on related media drop down
        if self.click(self.ENTRY_PAGE_RELATED_MEDIA) == False:
            writeToLog("INFO","FAILED to click on related media drop down menu")       
            return False
        
        # Choose related media option
        if relatedMediaOption == enums.ReleatedMedia.MY_MEDIA:
            if self.click(self.ENTRY_PAGE_MY_MEDIA_OPTION) == False:
                writeToLog("INFO","FAILED to click on My media option")       
                return False
            
        elif relatedMediaOption == enums.ReleatedMedia.RELATED_MEDIA:
            if self.click(self.ENTRY_PAGE_MY_MEDIA_OPTION) == False:
                writeToLog("INFO","FAILED to click on Related media option")       
                return False      
        else: 
            writeToLog("INFO","FAILED to click on Related media drop down options - No valid option was given")       
            return False          
        
        return True  
    
    
    # @Author: Inbar Willman
    # Verify that My Media entry are displayed in My Media side bar
    def checkMyMediaSideBarEntries(self, entrisList):
        #Check uploaded entries in My Media Side bar
        for entry in entrisList:
            tmp_entry = (self.ENTRY_PAGE_MY_MEDIA_SIDE_BAR_ENTRIES[0], self.ENTRY_PAGE_MY_MEDIA_SIDE_BAR_ENTRIES[1].replace('ENTRY_NAME', entry))
            if self.is_visible(tmp_entry) == False:
                writeToLog("INFO","FAILED to displayed My Media entry:" + entry)       
                return False                 
                
        return True    
    
    
    # @Author: Inbar Willman
    # Click on attachments tab
    def clickOnAttachmentTab(self):        
        # Click on attachment tab   
        if self.click(self.ENTRY_PAGE_ATTACHMENTS_TAB, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on attachments tab")       
            return False              
    
    
    # @Author: Inbar Willman 
    # Download attachments file
    def downloadAttachmentFromEntryPage(self, originalPath, downloadPath):
        # Click on download tab
        if self.clickOnAttachmentTab() == False:
            writeToLog("INFO","FAILED to click on attachments tab")       
            return False   
        
        # Click on download icon   
        if self.click(self.ENTRY_PAGE_DOWNLOAD_ATTACHMENTS_ICON, 30) == False:
            writeToLog("INFO","FAILED to click on download attachments icon")       
            return False   
        
        # Wait to download file
        sleep(10)
        
        # Compare between uploaded file and download file 
        if self.clsCommon.compareBetweenTwoFilesBinary(originalPath, downloadPath) == False:
            writeToLog("INFO","Failed to click on to download file correctly")
            return False    
                
        return True    
    
    
    # @Author: Inbar Willman
    # Verify that correct count of related media is displayed
    # By default = 10
    def verifyRelatedMediaCount(self, realtedLimit):
        # get related media table length
        related_media_length = len(self.get_elements(self.ENTRY_PAGE_RELATED_MEDIA_TABLE))
        if related_media_length != realtedLimit:
            writeToLog("INFO","Failed to displayed correct number of media in Related section")
            return False   
        
        return True 
    
    
    # @Author: Michal Zomper
    # The function check that the correct media display in the player via type
    def verifyEntryViaType(self, entryType, entryLangth='', timeToStop='', entryQRResult=''):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE:
            self.clsCommon.jive.switchToJiveIframe()
            self.driver.execute_script("window.scrollTo(0, 180)") 
            self.clsCommon.player.switchToPlayerIframe()
        elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            self.switch_to_default_content()
            self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
            self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN,5)
            sleep(1)
            self.clsCommon.player.switchToPlayerIframe()
        else:
            self.clsCommon.player.switchToPlayerIframe()
            
        if entryType == enums.MediaType.VIDEO:
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                self.click(self.clsCommon.d2l.D2L_HEANDL_ENTRY_WIDGET_IN_ENTRY_PAGE, timeout=3)
                self.get_body_element().send_keys(Keys.PAGE_DOWN)
            
            try:
                videoLangth = self.get_element(self.clsCommon.player.PLAYER_TOTAL_VIDEO_LENGTH).text
            except NoSuchElementException:
                writeToLog("INFO","Failed to get video length element")
                return False
            
            if (entryLangth in videoLangth) == False:
                writeToLog("INFO","Failed, video length is NOT correct")
                return False
            
            if self.clsCommon.player.clickPlayAndPause(timeToStop, timeout=45) == False:
                writeToLog("INFO","FAILED to stop player at time: " + str(timeToStop))
                return False
            
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                self.click(self.clsCommon.d2l.D2L_HEANDL_ENTRY_WIDGET_IN_ENTRY_PAGE, timeout=3)
                self.get_body_element().send_keys(Keys.PAGE_UP)
                
            qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
            if qrCodeSc == False:
                writeToLog("INFO","FAILED to take qr screen shot")
                return False
            
            result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
            if result == None:
                writeToLog("INFO","FAILED to resolve qr code")
                return False
            
            # check the result is correct ... 
            # for example:
            # 1. if entryQRResult =5 and result =4 we will return true
            # 2. if entryQRResult =5 and result =5 we will return true
            # 3. if entryQRResult =5 and result =6 we will return true  
            if ((str(int(result)+1) == entryQRResult) or (entryQRResult == result) or (str(int(result)-1) == entryQRResult)) == False:
                writeToLog("INFO","FAILED to verify video, QR code isn't correct: the Qr code in the player is " + str(result) + "' but need to be '" + str(entryQRResult) + "'")
                return False
        
        if entryType == enums.MediaType.AUDIO:
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L:
                self.click(self.clsCommon.d2l.D2L_HEANDL_ENTRY_WIDGET_IN_ENTRY_PAGE, timeout=3)
                self.get_body_element().send_keys(Keys.PAGE_DOWN)

            try:
                audioLangth = self.get_element(self.clsCommon.player.PLAYER_TOTAL_VIDEO_LENGTH).text
            except NoSuchElementException:
                writeToLog("INFO","Failed to get audio length element")
                return False
            
            if (entryLangth in audioLangth) == False:
                writeToLog("INFO","Failed, audio length is NOT correct")
                return False
            
        if entryType == enums.MediaType.IMAGE: 
            qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
            if qrCodeSc == False:
                writeToLog("INFO","FAILED to take qr screen shot")
                return False
            
            result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
            if result == None:
                writeToLog("INFO","FAILED to resolve qr code")
                return False
            
            if str(entryQRResult) != result:
                writeToLog("INFO","FAILED to verify image, QR code isn't correct: the Qr code in the player is " + str(result) + "' but need to be '" + str(entryQRResult) + "'")
                return False
        
        self.clsCommon.base.switch_to_default_content()
        writeToLog("INFO","Success, entry type '" + entryType.value + "' was verify successfully")
        return True
    
    
    # Author: Michal Zomper
    # The function search and verify caption in the caption section in entry page
    def verifyCaptionsSearchResult(self, captionTime, captionText):
        if self.click(self.ENRTY_PAGE_SEARCH_ICON) == False:
            writeToLog("INFO","FAILED to click on search icon")
            return False
        
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE \
            or localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS:
            if self.send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR, captionText + Keys.ENTER, multipleElements=False) == False:
                writeToLog("INFO","FAILED to insert caption search")
                return False
        else:
            if self.send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR, captionText, multipleElements=False) == False:
                writeToLog("INFO","FAILED to insert caption search")
                return False
        sleep(4)
     
        try:
            captionResult = self.get_element(self.ENTRY_PAGE_CAPTION_SEARCH_RESULT).text
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get caption search result element")
            return False
            
        captionResult = captionResult.split("\n")
        for result in captionResult:
            if (captionTime in result) and (captionText in result) == True:
                writeToLog("INFO","Success, caption was found and verified in caption search results section")
                return True
            
        writeToLog("INFO","FAILED to find caption search result")
        return False        
        
            
    # Author: Michal Zomper
    # The function click on the caption time in the caption section in entry page and the verify that the caption appear on the player with the correct time              
    def clickOnCaptionSearchResult(self, captionTime, captionText, entryName=''):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L or\
        localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
            tmpEntryName = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
            self.click(tmpEntryName)
            sleep(1)
            self.get_body_element().send_keys(Keys.PAGE_DOWN)
        
        sleep(2)
        tmpCaptionTime = (self.ENTRY_PAGE_CAPTION_TIME_RESULT[0], self.ENTRY_PAGE_CAPTION_TIME_RESULT[1].replace('CAPTION_TIME', captionTime))
        if self.click(tmpCaptionTime, timeout=15) == False:
            writeToLog("INFO","FAILED to click on caption time in caption search result")
            return False
        sleep(2)
            
        if self.clsCommon.player.switchToPlayerIframe() == False:
            writeToLog("INFO","FAILED to switch to player frame in order to check caption on the player ")
            return False
        
        if self.clsCommon.player.verifyCaptionText(captionText) == False:
            writeToLog("INFO","FAILED to find caption in the player")
            return False
        
        try:
            playerTime = self.get_element_text(self.clsCommon.player.PLAYER_CURRENT_TIME_LABEL)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get player current time label")
            return False
        
        if playerTime != captionTime[1:]:
            writeToLog("INFO","FAILED, caption time in the player isn't correct")
            return False
        
        writeToLog("INFO","Success, caption was found and verified in the player")
        return True
      
        
    # Author: Michal Zomper
    # The function search the caption in the caption section in entry page, then clicking on the caption time in the caption section and check the caption in the player 
    # captionText - the search caption
    # expectedCaptionAfterSearch - after clicking on the time in the caption section the player jump to the expected time but move back a few milliseconds so we see the caption befor the one that we are looking for
    def verifyAndClickCaptionSearchResult(self, captionTime, captionText, expectedCaptionAfterSearch, entryName=''):
        if self.verifyCaptionsSearchResult(captionTime, captionText) == False:
            writeToLog("INFO","FAILED to verify caption in  entry caption search section")
            return False
        
        if self.clickOnCaptionSearchResult(captionTime, expectedCaptionAfterSearch, entryName) == False:
            writeToLog("INFO","FAILED to find and verify caption in the player")
            return False
        
        writeToLog("INFO","Success, caption was found and verified")
        return True
           
    
    # Author: Cus Horia
    # The function verifies that the entryName and description are not displayed in the search results
    def verifyEntryNameAndDescriptionInSearch(self, entryName):          
        if self.click(self.ENRTY_PAGE_SEARCH_ICON) == False:
            writeToLog("INFO","FAILED to click on search icon")
            return False
        
        if self.click_and_send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR, '"' + entryName + '"') == False:
            writeToLog("INFO", "Failed to search for the " + entryName + " entry")
            return False
        
        if self.click(self.ENTRY_SEARCH_TRIGGER) == False:
            writeToLog("INFO", "Failed to trigger the search process")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()

        if self.is_visible(self.ENTRY_SEARCH_NO_RESULTS_TEXT) == False:
            writeToLog("INFO", "Entry name has been found in the search results")
            return False
        
        if self.click(self.ENTRY_SEARCH_CLOSE_ICON) == False:
            writeToLog("INFO", "Failed to close the search bar")
            return False
                    
        return True
    
    
    # Author: Cus Horia
    # The function verifies that the proper elements are displayed while being in show more and show less screen
    def verifyFieldDisplayInEntryPage(self, field, number):
        if self.clsCommon.myMedia.verifyFieldIconAndNumberOfDisplayInResults(False, field, number, True) == False:
            writeToLog("INFO", "Failed to display the" '"' + field.value + '"' "values")
            return False
         
        if self.is_visible(self.ENTRY_SEARCH_SHOW_LESS) == False:
            writeToLog("INFO", "Search show less option is missing")
            return False
        
        if self.is_visible(self.ENTRY_SEARCH_SHOW_ALL) == True:
            writeToLog("INFO", "Show all option is displayed")
            return False
         
        if self.click(self.ENTRY_SEARCH_SHOW_LESS) == False:
            writeToLog("INFO", "Failed to click on the show less button")
            return False
          
        if self.wait_visible(self.clsCommon.myMedia.ENTRY_FIELD_VALUES_SCETION, timeout=3) != False:
            writeToLog("INFO","FAILED: Field values section shouldn't be displayed anymore")
            return False
        
        writeToLog("INFO","Success, all the proper elements are displayed in the show more and show less screen")
        return True
    
    
    # Author: Cus Horia
    # The function searches for a specific term and then verifies that proper elements are displayed while being in show less and show more screen   
    def verifyFieldDisplayInEntryPageAfterMakingASearch(self, searchTerm, field, number):
        if self.searchForAnEntryTerm(searchTerm) == False:
            writeToLog("INFO", "Failed to verify field display after making a search")
            return False 
        
        if self.verifyFieldDisplayInEntryPage(field, number) == False:
            writeToLog("INFO", "Failed to verify field display after making a search")
            return False 
          
        if self.is_visible(self.ENTRY_SEARCH_SHOW_MORE) == False:
            writeToLog("INFO", "Failed, search show more option is missing")
            return False
         
        if self.click(self.ENTRY_SEARCH_SHOW_MORE) == False:
            writeToLog("INFO", "Failed to click on the show more button")
            return False
        
        if self.clsCommon.myMedia.verifyFieldIconAndNumberOfDisplayInResults(False, field, number, True) == False:
            writeToLog("INFO", "Failed to display the" + searchTerm + "values")
            return False
        
        if self.click(self.ENTRY_SEARCH_CLOSE_ICON) == False:
            writeToLog("INFO", "Failed to close the search bar")
            return False      
        
        writeToLog("INFO","Success, all the proper elements for the searchTerm are displayed in the show more and show less screen")        
        return True       
    
    
    # Author: Cus Horia
    # The function searches for a specific entry term  
    def searchForAnEntryTerm(self, searchTerm):
        if self.click(self.ENRTY_PAGE_SEARCH_ICON) == False:
            writeToLog("INFO","FAILED to click on search icon")
            return False
        
        if self.click_and_send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR, '"' + searchTerm + '"') == False:
            writeToLog("INFO", "Failed to search for the " + searchTerm + " element")
            return False
        
        if self.click(self.ENTRY_SEARCH_TRIGGER) == False:
            writeToLog("INFO", "Failed to perform a search within the entry")
            return False
        
        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "Failed to upload the search results screen")
            return False
        
        writeToLog("INFO","Success, the search term has been successfully displayed")                
        return True
    

    # Author: Cus Horia
    # The function verifies that all the search label list elements are displayed in the drop down menu
    def verifySearchDropDownLabels(self, searchTerm, labelList):
        if self.searchForAnEntryTerm(searchTerm) == False:
            writeToLog("INFO", "Failed to verify field display after making a search")
            return False 
        
        if self.click(self.ENTRY_SEARCH_DROP_DOWN_MENU) == False:
            writeToLog("INFO", "Failed to perform a search within the entry")
            return False
        
        for label in labelList:
            tmpLabel = (self.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[0], self.ENTRY_SEARCH_DROP_DOWN_MENU_LIST[1].replace('LABEL', label))
            if self.is_visible(tmpLabel) == False:
                writeToLog("INFO", "Failed, a specific label is not displayed in the drop down menu")
                return False
        
        if self.click(self.ENTRY_SEARCH_DROP_DOWN_MENU) == False:
            writeToLog("INFO", "Failed to perform a search within the entry")
            return False
        
        if self.click(self.ENTRY_SEARCH_CLOSE_ICON) == False:
            writeToLog("INFO", "Failed to close the search bar")
            return False
        
        writeToLog("INFO","Success, all the labels are displayed in the drop down menu")                
        return True 
                

    # Author: Cus Horia
    # The function selects a specific search label from the drop down menu
    def selectLabelFromDropDown(self, labelNumber):       
        if self.click(self.ENTRY_SEARCH_DROP_DOWN_MENU) == False:
            writeToLog("INFO", "Failed to perform a search within the entry")
            return False
         
        if self.click(labelNumber) == False:
            writeToLog("INFO", "Failed to perform a search within the entry")
            return False
        
        writeToLog("INFO","Success, the specific label has been successfully selected")                        
        return True
    
    
    # Author: Cus Horia
    # The function verifies that all the specific elements for the selected label are displayed in the search results and no other elements are displayed
    def searchLabelElements(self, searchTerm, labelNumber, elementsNumber, searchElement, allElements):
        if self.searchForAnEntryTerm(searchTerm) == False:
            writeToLog("INFO", "Failed to search for " + searchTerm + "element")
            return False 
         
        if self.selectLabelFromDropDown(labelNumber) == False:
            writeToLog("INFO", "Failed to select a label number from the drop down menu")
            return False

        searchName = (self.ENTRY_SEARCH_RESULTS_CONTAINER[0], self.ENTRY_SEARCH_RESULTS_CONTAINER[1].replace('TEXT', allElements))
        tmpSearch = self.get_elements(searchName)
        if len(tmpSearch) != elementsNumber == False:
            writeToLog("INFO", "Failed, more than the specific entries are displayed")
            
        searchName = (self.ENTRY_SEARCH_RESULTS_CONTAINER[0], self.ENTRY_SEARCH_RESULTS_CONTAINER[1].replace('TEXT', searchElement))
        if self.is_visible(searchName) == False:
            writeToLog("INFO", "Failed, elements that should be displayed in the search results are missing")
            return False
        
        if self.click(self.ENTRY_SEARCH_CLOSE_ICON) == False:
            writeToLog("INFO", "Failed to close the search bar")
            return False
        
        writeToLog("INFO","Success, only the specific elements for the selected label are displayed")                                
        return True     
    
    
    # @Author: Horia Cus
    # This function verifies if the status of any KEA Option is enabled or disabled or that a specific element is present or not
    # keaSection must be enum
    # keaOption must be enum and have a map
    # keaElement must contain the text specific for the selected kea option
    # entryName must be specified if you want to navigate to entry page from kea
    def verifyQuizOptionsInEntryPage(self, keaSection, keaOption, keaElement, keaOptionEnabled=True, navigateToEntryPageFromKEA=False, entryName=''):
        if navigateToEntryPageFromKEA == True:
            if self.navigateToEntry(entryName, enums.Location.KEA_PAGE) == False:
                return False
        
        if keaSection == enums.KEAQuizSection.DETAILS or keaSection == enums.KEAQuizSection.SCORES or keaSection == enums.KEAQuizSection.EXPERIENCE:            
            if keaOptionEnabled == True:
                if keaOption == enums.KEAQuizOptions.QUIZ_NAME:
                    if self.verifyEntryNamePresent(keaElement) == False:
                        return False
    
                elif keaOption == enums.KEAQuizOptions.INCLUDE_ANSWERS:
                    if self.clsCommon.player.verifyIncludedAnswers(keaElement) == False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.ALLOW_ANSWER_CHANGE:
                    if self.clsCommon.player.changeQuizAnswer(keaElement) == False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.NO_SEEKING_FORWARD:
                    if self.clsCommon.player.clickAndSeekOnSlider(keaElement, noSeekingForwardEnabled=True) == False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.ALLOW_SKIP:
                    if self.clsCommon.player.skipQuizAnswers() == False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP:
                    if self.clsCommon.player.verifySkipOptionDisabled() == False:
                        return False
                    
                else:
                    if self.clsCommon.player.verifyQuizElementsInPlayer(keaSection, keaOption, keaElement, location=enums.Location.ENTRY_PAGE, timeOut=45, isPresent=True) == False:
                        return False
                
            elif keaOptionEnabled == False:
                if keaOption == enums.KEAQuizOptions.QUIZ_NAME:
                    if self.verifyEntryNamePresent(keaElement) != False:
                        return False
    
                elif keaOption == enums.KEAQuizOptions.INCLUDE_ANSWERS:
                    if self.clsCommon.player.verifyIncludedAnswers(keaElement) != False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.ALLOW_ANSWER_CHANGE:
                    if self.clsCommon.player.verifyChangeQuizAnswerOptionDisabled(keaElement) == False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.NO_SEEKING_FORWARD:
                    if self.clsCommon.player.clickAndSeekOnSlider(keaElement, noSeekingForwardEnabled=False) == False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.ALLOW_SKIP:
                    if self.clsCommon.player.verifySkipOptionDisabled() == False:
                        return False
                    
                elif keaOption == enums.KEAQuizOptions.DO_NOT_ALLOW_SKIP:
                    if self.clsCommon.player.skipQuizAnswers() == False:
                        return False
                    
                else:
                    if self.clsCommon.player.verifyQuizElementsInPlayer(keaSection, keaOption, keaElement, location=enums.Location.ENTRY_PAGE, timeOut=30, isPresent=False) == False:
                        return False
        else:
            writeToLog("INFO", "FAILED, please make sure that you're using a supported KEA section")

        return True  
    
    
    # @Author: Horia Cus
    # This function verifies if the desired entry name is present in the entry page    
    def verifyEntryNamePresent(self, entryName, timeOut=30):
        tmp_entry_name = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        
        if self.wait_element(tmp_entry_name, timeOut, True) == False:
            writeToLog("INFO","The " + entryName + " is not present")
            return False
        
        return True
    
    
    # @Author: Inbar Willman
    def chooseCreateClipOption(self):
        if self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
            writeToLog("INFO","FAILED to click on 'Actions' dropdown")
            return False  
        
        if self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_CREATE_CLIP_BUTTON) == False:
            writeToLog("INFO","FAILED to click on 'Create clip' option")
            return False  
        
        writeToLog("INFO","Success: 'create clip' option was chosen")  
        return True   
    
    
    # @Author: Inbar Willman
    # Navigate to Quiz quizAnalytics page - Quiz users tab or Quiz questions tab
    def navigateToQuizAnalyticsPage(self, entryName='', forceNavigate=False, analyticsTab=enums.quizAnalytics.QUIZ_QUESTIONS):
        if forceNavigate == True:
            if self.navigateToEntryPageFromMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to navigate to " + entryName + " page")
                return False  
            
        if self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
            writeToLog("INFO","FAILED to click on action dropdown list")
            return False        
              
        if self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST_ANALYTICS_OPTION) == False:
            writeToLog("INFO","FAILED to click on quizAnalytics option")
            return False 
                    
        if analyticsTab == enums.quizAnalytics.QUIZ_QUESTIONS:
            if self.click(self.clsCommon.quizAnalytics.QUIZ_ANALYTICS_QUIZ_QUESTIONS_TAB) == False:
                writeToLog("INFO","FAILED to click on " + enums.quizAnalytics.QUIZ_QUESTIONS.value)
                return False 
            
        elif analyticsTab == enums.quizAnalytics.QUIZ_USERS:
            if self.click(self.clsCommon.quizAnalytics.QUIZ_ANALYTICS_QUIZ_USERS_TAB) == False:
                writeToLog("INFO","FAILED to click on " + enums.quizAnalytics.QUIZ_USERS.value)
                return False  
            
        writeToLog("INFO","Succeed to navigate to " + analyticsTab.value)           
        return True
    
    
    # Author: Michal Zomper 
    def clickAddComment(self, comment):
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
            self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN,5)
            sleep(2)
            self.switch_to_default_content()
            self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
            self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
            self.clsCommon.sharePoint.switchToSharepointIframe() 
            
        if self.click(self.ENTRY_PAGE_COMMENT_ADD_BUTTON, 15, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on add comment button")
            return False
          
        self.clsCommon.general.waitForLoaderToDisappear()
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        sleep(2)
        
        # verify comment was added
        tmp_comments = self.get_element_text(self.ENTRY_PAGE_COMMENTS_PANEL)
        if comment in tmp_comments == False:
            writeToLog("INFO","FAILED to find added comment")
            return False
           
        writeToLog("INFO","Success, comment: '" + comment +"'  was added to entry")  
        return True
    
    
    # Author: Michal Zomper
    def insertCommentToTextField(self, comment):
        sleep(2)
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
        
        # Wait for comments module to load - wait for 'Add' button
        if self.wait_visible(self.ENTRY_PAGE_COMMENT_TEXT_AREA, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to load Comments module")
            return False  
          
        sleep(1)
        if self.click(self.ENTRY_PAGE_COMMENT_TEXT_AREA, 5) == False:
            writeToLog("INFO","FAILED to click in the comment text box area")
            return False

        if self.send_keys(self.ENTRY_PAGE_COMMENT_TEXT_AREA, comment + Keys.SPACE, multipleElements=True) == False:
            writeToLog("INFO","FAILED to add the: " + comment + " comment inside the text area")
            return False
        sleep(2)
        
        writeToLog("INFO", "The " + comment + " comment has been properly add to the text area")
        return True
    
    
    # Author: Horia Cus
    # This function will place a comment at any desired timeLocation available on the entry
    # timeStamp must contain the following format m:ss, mm:ss ( e.g 0:15)
    def addCommentWithTimeStamp(self, comment, timeStamp, embed=False):
        # Make sure that we reach the top of the entry in order to proper resume the entry from beginning if needed
        for x in range(0, 60):
            self.clsCommon.sendKeysToBodyElement(Keys.ARROW_UP)
            
        self.clsCommon.player.switchToPlayerIframe(embed)
        if self.wait_element(self.clsCommon.player.PLAYER_CONTROLS_CONTAINER_REAL_TIME, 35, True).text != '0:00':
            if self.clsCommon.player.resumeFromBeginningEntry(False) == False:
                writeToLog("INFO","FAILED to resume from the beginning the entry")
                return False
        
        # Run and pause the player at the timeStamp
        if self.clsCommon.player.clickPlayAndPause(timeStamp) == False:
            writeToLog("INFO","FAILED to stop player at time: " + str(timeStamp))
            return False
        
        self.switch_to_default_content()
        if self.insertCommentToTextField(comment) == False:
            writeToLog("INFO", "FAILED to add the following comment " + str(comment) + " to the text field")
            return False
        
        commentTimeLocation = self.wait_element(self.ENTRY_PAGE_COMMENT_TIME_CHECKBOX, 1)
        
        if commentTimeLocation == False:
            writeToLog("INFO", "FAILED to find the element for 'Add comment at time'")
            return False

        if commentTimeLocation.text.count(timeStamp) != 1:
            writeToLog("INFO", "FAILED to find the time stamp " + timeStamp + " inside the ;Add Comment at time' field")
            return False
            
        if self.clickElement(commentTimeLocation)== False:
            writeToLog("INFO", "FAILED to fill the Add Comment at time location checkbox")
            return False

        if self.clickAddComment(comment) == False:
            writeToLog("INFO", "FAILED to add the following comment " + str(comment) + " to the entry list")
            return False
                
        writeToLog("INFO", "The commnet: " + comment + " has been successfully added at time location: " + timeStamp)
        return True  
    
    
    # @Author: Inbar Willman
    # Choose Captions requests option in 'Actions' menu
    def chooseCaptionsRequestsOption(self, entryName='', forceNavigate=False):
        if forceNavigate == True:
            if self.navigateToEntryPageFromMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to navigate to " + entryName + " page")
                return False  
            
        if self.click(self.ENTRY_PAGE_ACTIONS_DROPDOWNLIST) == False:
            writeToLog("INFO","FAILED to click on action dropdown list")
            return False        
              
        if self.click(self.ENTRY_PAGE_CAPTIONS_REQUESTS_OPTION) == False:
            writeToLog("INFO","FAILED to click on 'Captions Requests' option")
            return False    
        
        writeToLog("INFO", "'Captions Requests' option was successfully chosen")
        return True
    
    
    # Author: Horia Cus
    # This function will verify the changes performed within the Entry Design
    # You may verify only the desired design elements from the Entry Page, by leaving the ones that should not be verified as empty ''
    # expectedElementsDict must contain the enum class and the status of the element ( True or False ) and must have inside, a list with all the available elements
    # expectedElementDict must contain the following structure {enums.EditEntryDisplayElements.DESIRED_ELEMENT:True}
        # If True, it will verify that the Element is presented
        # If false, it will verify that the Element is not presented
    # expectedBackgroundColor must contain the HEX code of the background color (e.g #C06C84)
    # expectedCSSFilePath and expectedLogoFilePath must contain the path, where the specific files are saved ( e.g localSettings.LOCAL_SETTINGS_MEDIA_PATH + r'\images\kaltura_logo.png')
    def verifyEntryDisplay(self, expectedElementsDict, expectedBackgroundColor, expectedCSSFilePath, expectedLogoFilePath):
        # Verify that the Player Screen is always displayed
        if self.wait_element(self.clsCommon.player.PLAYER_SCREEN, 30, True) == False:
            writeToLog("INFO", "FAILED, the player screen was not displayed, although it should be always present, despite of the Entry Desing changes")
            return False
        
        # Verify if we want to verify the presented elements specific for Entry Design from the Entry Page
        if expectedElementsDict != '':
            # Take the status of the presented elements from the entry page
            headerElement                = self.wait_element(self.ENTRY_PAGE_HEADER_NAVBAR, 0.3, True)
            headerLogoElement            = self.wait_element(self.ENTRY_PAGE_HEADER_LOGO, 0.3, True)
            sideBarElement               = self.wait_element(self.ENTRY_PAGE_SIDEBAR, 0.3, True)
            entryPropertiesElement       = self.wait_element(self.ENTRY_PAGE_ENTRY_PROPERTIES, 0.3, True)
            entryTabsElement             = self.wait_element(self.ENTRY_PAGE_ENTRY_TABS_CONTAINER, 0.3, True)
            commentTabElement            = self.wait_element(self.ENTRY_PAGE_COMMENT_TAB_PANEL, 0.3, True)
            footerElement                = self.wait_element(self.ENTRY_PAGE_FOOTER_NAVBAR, 0.3, True)
            
            # Each index from the List is used in order to append the results in the presentedElementsDict, using this exact order
            presentedElementList        = [headerElement, headerLogoElement, sideBarElement, entryPropertiesElement, entryTabsElement, commentTabElement, footerElement]
            
            # Create a list with the boolean status of the element
            presentedElementListBoolean = []
            for presentedElement in presentedElementList:
                # If an element has been found, we will return it as True
                if type(presentedElement) is not bool:
                    presentedElement = True
                    
                presentedElementListBoolean.append(presentedElement)
            
            # Create a dictionary that contains the status of the presented elements from the entry page
            presentedElementsDict    = {enums.EditEntryDisplayElements.HEADER:presentedElementListBoolean[0], 
                                        enums.EditEntryDisplayElements.HEADER_LOGO:presentedElementListBoolean[1], 
                                        enums.EditEntryDisplayElements.SIDEBAR:presentedElementListBoolean[2],
                                        enums.EditEntryDisplayElements.ENTRY_PROPERTIES:presentedElementListBoolean[3],
                                        enums.EditEntryDisplayElements.ENTRY_TABS:presentedElementListBoolean[4],
                                        enums.EditEntryDisplayElements.COMMENTS:presentedElementListBoolean[5],
                                        enums.EditEntryDisplayElements.FOOTER:presentedElementListBoolean[6]} 
            
            # Compare the expected elements status with the presented element status
            if expectedElementsDict != presentedElementsDict:
                # Take the string out of the expected and presented dictionaries
                expectedElementDictString       = ', '.join("{!s}={!r}".format(key,val) for (key,val) in expectedElementsDict.items())
                presentedElementsDictString     = ', '.join("{!s}={!r}".format(key,val) for (key,val) in presentedElementsDict.items())
                
                # Print the presented and expected dictionaries
                writeToLog("INFO", "\nPresented Dictionary:\n" + presentedElementsDictString + "\nExpected Dictionary:\n" + expectedElementDictString)
                inconsitencyList = []
                
                # Create an inconsistency list in order to highlight where it failed
                try:
                    for expectedElement in expectedElementsDict:
                        if expectedElementsDict[expectedElement] != presentedElementsDict[expectedElement]:
                            if expectedElementsDict[expectedElement] == False:
                                expectedStatus = "to not be displayed but it was presented"
                            else:
                                expectedStatus = "to be displayed, at it was not presented" 
                            inconsitencyList.append("FAILED, Inconsistency for the element " + expectedElement.value + " we expected that the element " + expectedStatus)
                    
                    if len(inconsitencyList) > 1:
                        inconsistencies = "\n".join(inconsitencyList)
                    else:
                        inconsistencies = inconsitencyList[0]
                except Exception:
                    inconsistencies = 'Exception'
                    
                writeToLog("INFO", "FAILED, the following inconsistencies were noticed in the Entry Page " + str(inconsistencies))
                return  False
        
        # Verify if we want to verify the expected background color
        if expectedBackgroundColor != '':
            # Take the presented background color from the body element using css property
            try:
                bodyElementBackgroundColor = self.wait_element(self.ENTRY_PAGE_BODY, 1, True).value_of_css_property('background-color').replace('rgb','').split(',')
            except Exception:
                writeToLog("INFO", "FAILED to take the background color details from the body element")
                return False
            
            # Take the R,G,B numbers
            R,G,B                               = bodyElementBackgroundColor[0].replace('(',''), bodyElementBackgroundColor[1].replace('(',''), bodyElementBackgroundColor[2].replace('(','')
            # Make sure that the R,G,B are returned integer
            R,G,B                               = int(re.search(r'\d+', R).group()), int(re.search(r'\d+', G).group()), int(re.search(r'\d+', B).group())
            # Create a Tuple with the R,G,B integers
            bodyElementBackgroundColorTuple     = (R,G,B)
            # Convert the R,G,B Tuple to HEX
            bodyElementBackgroundColorHEX       = ('#%02x%02x%02x' % bodyElementBackgroundColorTuple).upper()
            
            if bodyElementBackgroundColorHEX != expectedBackgroundColor:
                writeToLog("INFO", "FAILED, the " + bodyElementBackgroundColorHEX + " background color has been presented, while we expected: " + expectedBackgroundColor)
                return False
            
        # Verify if the changes were performed within the CSS
        if expectedCSSFilePath != '':
            try:
                expectedCSSString       = open(expectedCSSFilePath).read()
            except Exception:
                writeToLog("INFO", "FAILED to read the expected CSS file")
                return False
            
            # Take a list with all the expected CSS list attributes and values
            expectedCSSList            = expectedCSSString.strip('body').replace('{','').replace('}','').split()
            
            # Create a list with the attribute changes in order to proper iterate through the dictionary
            expectedCSSAtributeChangesList      = []
            expectedCSSChangesDict              = {}
            for x in range(0,len(expectedCSSList)):
                # Verify that we reached an attribute within the expectedCSSList
                if expectedCSSList[x][-1] == ':':
                    attributeCSSExpected    = expectedCSSList[x].replace(':','')
                    # Supports only one value
                    valueCSSExpected        = expectedCSSList[x+1].replace(';','')
                    # Create a list that contains all the attributes that are expected to be changed
                    expectedCSSAtributeChangesList.append(attributeCSSExpected)
                    # Create a dictionary that contains the expected attributes and values
                    expectedCSSChangesDict.update({attributeCSSExpected:valueCSSExpected})                   
            
            # CSS changes affects the body element
            bodyElement             = self.wait_element(self.ENTRY_PAGE_BODY, 15, True)
            
            # Verify that we were able to take the body element
            if bodyElement == False:
                writeToLog("INFO", "FAILED to take the body element")
                return False
            
            # Verify that we were able to find at least one attribute with the expected CSS File path
            if len(expectedCSSAtributeChangesList) == 0:
                writeToLog("INFO", "FAILED to find any attributes within the expected CSS file path")
                return False
            
            # Verify that the value for the expected changed attributes matches with the presented values
            for x in range(0, len(expectedCSSAtributeChangesList)):
                # Take the changed attribute name
                currentAttribute         = expectedCSSAtributeChangesList[x]
                # Take the presented value of the current attribute
                presentedAttributeValue  = bodyElement.value_of_css_property(currentAttribute)
                # Take the expected value of the current attribute
                expectedAttributeValue   = expectedCSSChangesDict[expectedCSSAtributeChangesList[x]]
                
                # Verify that the presented and expected values for the current attribute matches
                if presentedAttributeValue != expectedAttributeValue:
                    writeToLog("INFO", "FAILED, we expected for the attribute: " + currentAttribute + " to have a value of: " + expectedAttributeValue + " but the value was: " + presentedAttributeValue)
                    return False
        
        # Verify if we expect to have a Logo Image in the header
        if expectedLogoFilePath != '':
            # Take the element for the header logo
            headerLogoElement = self.wait_element(self.ENTRY_PAGE_HEADER_LOGO_IMAGE, 1, True)
            
            # Verify that a header logo element is presented
            if headerLogoElement == False:
                writeToLog("INFO", "FAILED, we expected to have a Logo Image, but there's no logo image displayed")
                return False
            
            # Take the element for the logo image
            try:
                imageElement = self.get_child_element_by_type(headerLogoElement, 'tag_name', 'img')
            except Exception:
                writeToLog("INFO", "FAILED to take the logo image element")
                return False
            
            # Take the presented width and height of the logo
            try:
                presentedWidth, presentedHeight = imageElement.rect['width'], imageElement.rect['height']
            except Exception:
                writeToLog("INFO", "FAILED to take the presented width and height")
                return False
            
            # Take the expected width and height of the logo
            with Image.open(expectedLogoFilePath) as expectedImage:
                expectedWidth, expectedHeight = expectedImage.size
            
            # Compare the width and height of the presented with the expected logo image, in order to verify that the expected logo is displayed
            if int(presentedWidth) != int(expectedWidth):
                writeToLog("INFO", "FAILED, we expected a Logo image with width size of " + str(expectedWidth) + " but the width size was " + str(presentedWidth))
                return False
            
            if int(presentedHeight) != int(expectedHeight):
                writeToLog("INFO", "FAILED, we expected a Logo image with height size of " + str(expectedHeight) + " but the height size was " + str(presentedHeight))
                return False           
        
        # Verify that the HEADER logo is not displayed, but a Text
        else:
            if self.wait_element(self.ENTRY_PAGE_HEADER_LOGO_IMAGE, 1, True) != False:
                writeToLog("INFO", "FAILED, we expected to not have a Logo Image, but a Logo Image is displayed in the header")
                return False      
        
        writeToLog("INFO", "Entry Design changes were displayed as expected")           
        return True