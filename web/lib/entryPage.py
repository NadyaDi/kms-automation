from base import *
import clsTestService
import enums
from selenium.webdriver.common.keys import Keys



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
    ENTRY_PAGE_DESCRIPTION                                 = ('xpath', "//div[@class='row-fluid normalWordBreak']")
    ENTRY_PAGE_TAGS                                        = ('class_name', "tagsWrapper")    
    ENTRY_PAGE_ADDTOPLAYLIST_BUTTON                        = ('id', "Addtoplaylists")  
    ENTRY_PAGE_PUBLISH_BUTTON                              = ('id', "tab-Publish")
    ENTRY_PAGE_ACTIONS_DROPDOWNLIST_DELETE_BUTTON          = ('id', "tab-Delete")
    ENTRY_PAGE_CONFIRM_DELETE_BUTTON                       = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    ENTRY_PAGE_DOWNLOAD_TAB                                = ('xpath', "//a[@id='tab-download-tab']")
    ENTRY_PAGE_MEDIA_IS_BEING_PROCESSED                    = ('xpath', "//h3[@class='muted' and contains(text(), 'Media is being processed')]")
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
    ENTRY_PAGE_COMMENT_ADD_BUTTON                          = ('xpath', '//input[@id="add-comment"]')
    ENTRY_PAGE_COMMENTS_PANEL                              = ('xpath', "//div[@id='commentsWrapper']")
    ENTRY_PAGE_DETAILS_BUTTON                              = ('xpath', "//a[@id='tab-Details' and @class='btn responsiveSizePhone tabs-container__button tab-Details active']")
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
    #ENTRY_PAGE_ATTACHMENTS_TAB                             = ('xpath', '//a[@id="tab-attachments-tab" and @class="btn responsiveSizePhone tab-attachments-tab attachments-tab-tab"]')
    ENTRY_PAGE_ATTACHMENTS_TAB                             = ('xpath', '//a[@id="tab-attachments-tab"]')
    ENTRY_PAGE_DOWNLOAD_ATTACHMENTS_ICON                   = ('xpath', '//i[@class="icon-download icon-large"]')
    ENTRY_PAGE_RELATED_MEDIA_TABLE                         = ('xpath', '//table[@class="table table-hover table-bordered thumbnails table-condensed"]/tbody/tr')
    ENTRY_PAGE_CAPTION_SEARCH_BAR_OLD_UI                   = ('xpath', "//input[@id='captionSearch']")
    ENRTY_PAGE_SEARCH_ICON                                 = ('xpath', "//div[@id='entryeSearchForm']") 
    ENTRY_PAGE_CAPTION_SEARCH_BAR                          = ('xpath', "//input[@class='searchForm__text' and @placeholder='Search in video']")
    ENTRY_PAGE_CAPTION_TIME_RESULT                         = ('xpath', "//a[@class='results__result-item--time cursor-pointer' and contains(text(), 'CAPTION_TIME')]") 
    ENTRY_PAGE_CAPTION_TIME_RESULT_OLD_UI                  = ('xpath', "//a[@class='captions_search_result' and contains(text(), 'CAPTION_TIME')]") 
    ENTRY_PAGE_CAPTION_SEARCH_RESULT_OLD_UI                = ('xpath', "//ul[@id='kitems']")
    ENTRY_PAGE_CAPTION_SEARCH_RESULT                       = ('xpath', "//div[@class='results-details-container__group']")
    ENTRY_SEARCH_HEADER                                    = ('xpath', "//a[@id='HeaderAccordion-toggle0']//span[contains(@class,'hidden-tablet')][contains(text(),'Search')]")
    ENTRY_SEARCH_HEADER_INPUT                              = ('xpath', "//form[contains(@class,'headerSearchForm__searchForm searchForm')]//div[contains(@class,'input-prepend input-append searchForm__prepend')]//div//div//input[contains(@placeholder,'Search all media')]")
    ENTRY_SEARCH_HEADER_CONFIRM                            = ('xpath', "//form[contains(@class,'headerSearchForm__searchForm searchForm')]//div//div//i[contains(@class,'icon-search')]")
    ENTRY_SELECT_FROM_SEARCH                               = ('xpath', "//a[contains(@href,'ENTRY_ID')]")
    ENTRY_SEARCH_CLOSE_ICON                                = ('xpath', "//form[contains(@class,'noBorder searchForm')]//div//div//i[contains(@class,'v2ui-close-icon')]")
    ENTRY_SEARCH_NO_RESULTS_TEXT                           = ('xpath', "//div[@class='results-details-container' and text()='No results found']")
    ENTRY_FIELD_ICON_IN_RESULTS                            = ('xpath', '//i[contains(@title,"FIELD_NAME")]')
    ENTRY_SEARCH_SHOW_LESS                                 = ('xpath', "//a[contains(@aria-label,'Show Less')]")
    ENTRY_SEARCH_TRIGGER                                   = ('xpath', "//form[contains(@class,'noBorder searchForm')]//div//div//i[contains(@class,'icon-search')]")
    ENTRY_SEARCH_SHOW_MORE                                 = ('xpath', "//span[contains(@class,'results-summary__show-more--text hidden-phone')]")
    ENTRY_SEARCH_SHOW_ALL                                  = ('xpath', "//a[contains(@aria-label,'Show All')]")
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
            if self.wait_visible(tmpEntryName, 15) == False:
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
            if self.click(self.clsCommon.upload.UPLOAD_GO_TO_MEDIA_BUTTON, multipleElements=True) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + str(enums.Location.UPLOAD_PAGE))
                return False  
            
            tmpEntryName = (self.ENTRY_PAGE_ENTRY_TITLE[0], self.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
            if self.wait_visible(tmpEntryName, 15) == False:
                writeToLog("INFO","FAILED to enter entry page: '" + entryName + "'")
                return False
            
        elif navigateFrom == enums.Location.MY_HISTORY:
            if self.navigateToEntryPageFromMyHistory(entryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + str(enums.Location.MY_HISTORY))
                return False   
                
        elif navigateFrom == enums.Location.HOME:
            if self.navigateToEntryPageFromHomePage(entryName) == False:
                writeToLog("INFO","FAILED navigate to entry '" + entryName + "' from " + str(enums.Location.MY_HISTORY))
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
        
        if self.chooseShareOption() == False:
            writeToLog("INFO","FAILED to click on embed tab")
            return False
        sleep(3)
        
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
            writeToLog("INFO","FAILED to add comment")
            return False
        sleep(2)
        
        if self.click(self.ENTRY_PAGE_COMMENT_ADD_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on add comment button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()
        self.clsCommon.sendKeysToBodyElement(Keys.END)
        
        # verify comment was added
        tmp_comments = self.get_element_text(self.ENTRY_PAGE_COMMENTS_PANEL)
        if comment in tmp_comments == False:
            writeToLog("INFO","FAILED to find added comment")
            return False
           
        writeToLog("INFO","Success, comment: '" + comment +"'  was added to entry")       
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
        if self.is_visible(self.ENTRY_PAGE_COMMENT_TEXT_AREA) == True:
            writeToLog("INFO","FAILED - add new comment box is still displayed")
            return False                  
        
        return True       
    
       
    # @Author: Inbar Willman
    def replyComment(self, replyComment):  
        # Get comment Id
        tmp_comment_id = self.get_element(self.ENTRY_PAGE_COMMENT_ID)
        comment_id = tmp_comment_id.get_attribute("data-comment-id")
        
        # Click on replay button
        tmp_replay_btn = (self.ENTRY_PAGE_REPLY_COMMENT[0], self.ENTRY_PAGE_REPLY_COMMENT[1].replace('COMMENT_ID', comment_id))
        if self.click(tmp_replay_btn) == False:
            writeToLog("INFO","FAILED to click on replay button")
            return False   
        
        # Add new replay comment
        # Click on replay comment area
        if self.click(self. ENTRY_PAGE_REPLY_COMMENT_TEXT_AREA, 5) == False:
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
        if self.click(self.ENTRY_PAGE_ATTACHMENTS_TAB, 30) == False:
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
        self.clsCommon.player.switchToPlayerIframe()
        if entryType == enums.MediaType.VIDEO:
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
            
            qrCodeSc = self.clsCommon.qrcode.takeQrCodeScreenshot()
            if qrCodeSc == False:
                writeToLog("INFO","FAILED to take qr screen shot")
                return False
            
            result = self.clsCommon.qrcode.resolveQrCode(qrCodeSc)
            if result == None:
                writeToLog("INFO","FAILED to resolve qr code")
                return False
            
            if str(entryQRResult) != result:
                writeToLog("INFO","FAILED to verify video, QR code isn't correct: the Qr code in the player is " + str(result) + "' but need to be '" + str(entryQRResult) + "'")
                return False
        
        if entryType == enums.MediaType.AUDIO:
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
        if self.clsCommon.isElasticSearchOnPage() == True:
            if self.click(self.ENRTY_PAGE_SEARCH_ICON) == False:
                writeToLog("INFO","FAILED to click on search icon")
                return False
            
            if self.send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR, captionText, multipleElements=False) == False:
                writeToLog("INFO","FAILED to insert caption search")
                return False
            sleep(4)
         
            try:
                captionResult = self.get_element(self.ENTRY_PAGE_CAPTION_SEARCH_RESULT).text
            except NoSuchElementException:
                writeToLog("INFO","FAILED to get caption search result element")
                return False
        else:
            if self.send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR_OLD_UI, captionText, multipleElements=False) == False:
                writeToLog("INFO","FAILED to insert caption search")
                return False
            sleep(4)
            
            try:
                captionResult = self.get_element(self.ENTRY_PAGE_CAPTION_SEARCH_RESULT_OLD_UI).text
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
    def clickOnCaptionSearchResult(self, captionTime, captionText):
        if self.clsCommon.isElasticSearchOnPage() == True:
            tmpCaptionTime = (self.ENTRY_PAGE_CAPTION_TIME_RESULT[0], self.ENTRY_PAGE_CAPTION_TIME_RESULT[1].replace('CAPTION_TIME', captionTime))
            if self.click(tmpCaptionTime, timeout=15) == False:
                writeToLog("INFO","FAILED to click on caption time in caption search result")
                return False
            sleep(2)
        else:
            tmpCaptionTime = (self.ENTRY_PAGE_CAPTION_TIME_RESULT_OLD_UI[0], self.ENTRY_PAGE_CAPTION_TIME_RESULT_OLD_UI[1].replace('CAPTION_TIME', captionTime))
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
            
        self.clsCommon.blackBoard.switchToBlackboardIframe()
        
        writeToLog("INFO","Success, caption was found and verified in the player")
        return True
      
        
    # Author: Michal Zomper
    # The function search the caption in the caption section in entry page, then clicking on the caption time in the caption section and check the caption in the player 
    # captionText - the search caption
    # expectedCaptionAfterSearch - after clicking on the time in the caption section the player jump to the expected time but move back a few milliseconds so we see the caption befor the one that we are looking for
    def verifyAndClickCaptionSearchResult(self, captionTime, captionText, expectedCaptionAfterSearch):
        if self.verifyCaptionsSearchResult(captionTime, captionText) == False:
            writeToLog("INFO","FAILED to verify caption in  entry caption search section")
            return False
        
        if self.clickOnCaptionSearchResult(captionTime, expectedCaptionAfterSearch) == False:
            writeToLog("INFO","FAILED to find and verify caption in the player")
            return False
        
        writeToLog("INFO","Success, caption was found and verified")
        return True
           
    
    # Author: Cus Horia
    # The function verifies that the entryName and description are not displayed in the search results
    # expectedCaptionAfterSearch - after clicking on the time in the caption section the player jump to the expected time but move back a few milliseconds so we see the caption befor the one that we are looking for
    def verifyEntryNameAndDescriptionInSearch(self, searchElement):          
        if self.click(self.ENRTY_PAGE_SEARCH_ICON) == False:
            writeToLog("INFO","FAILED to click on search icon")
            return False
        
        if self.click_and_send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR, '"' + searchElement + '"') == False:
            writeToLog("INFO", "Failed to search for the " + searchElement + "element")
            return False
        
        if self.click(self.ENTRY_SEARCH_TRIGGER) == False:
            writeToLog("INFO", "Failed to perform a search within the entry")
            return False
        
        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "Failed to upload the search results screen")
            return False

        if self.is_visible(self.ENTRY_SEARCH_NO_RESULTS_TEXT) == False:
            writeToLog("INFO", "Description is displayed in the search results")
            return False
        
        if self.click(self.ENTRY_SEARCH_CLOSE_ICON) == False:
            writeToLog("INFO", "Failed to close the search bar")
            return False
                    
        writeToLog("INFO","Success, caption was found and verified")
        return True
    
    
    # Author: Cus Horia
    # The function verifies that the proper elements are displayed while being in show more or show less screen
    def verifyFieldDisplayInEntryPage(self, field, number):
        if self.clsCommon.myMedia.verifyFieldIconAndNumberOfDisplayInResults(False, field, number, True) == False:
            writeToLog("INFO", "Failed to display the" '"' + field + '"' "values")
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
        
        return True
    
    
    # Author: Cus Horia
    # The function searches for a specific term and then verifies that proper elements are displayed while being in show less and show more screen   
    def verifyFieldDisplayInEntryPageAfterMakingASearch(self, searchTerm, field, number):
        if self.click(self.ENRTY_PAGE_SEARCH_ICON) == False:
            writeToLog("INFO","FAILED to click on search icon")
            return False
        
        if self.click_and_send_keys(self.ENTRY_PAGE_CAPTION_SEARCH_BAR, '"' + searchTerm + '"') == False:
            writeToLog("INFO", "Failed to search for the description")
            return False
        
        if self.click(self.ENTRY_SEARCH_TRIGGER) == False:
            writeToLog("INFO", "Failed to perform a search within the entry")
            return False
        
        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "Failed to upload the search results screen")
            return False
        
        if self.verifyFieldDisplayInEntryPage(field, number) == False:
            writeToLog("INFO", "Failed to verify field display after making a search")
            return False 
          
        if self.is_visible(self.ENTRY_SEARCH_SHOW_MORE) == False:
            writeToLog("INFO", "Search show more option is missing")
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
        
        return True           