from base import *
import clsTestService
import enums
from logger import writeToLog
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


class Admin(Base):
    driver = None
    clsCommon = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #My Media locators:
    #=============================================================================================================
    ADMIN_ENABLED                                   = ('id', 'enabled')
    ADMIN_SAVE_BUTTON                               = ('xpath', "//input[@class='save' and @value='Save']")
    ADMIN_AFTER_CLICK_SAVE_MSG                      = ('id', 'dialog')
    ADMIN_CONFIRMATION_MSG_OK_BUTTON                = ('xpath', "//span[@class='ui-button-text' and text()='OK']")
    ADMIN_DISCLAIMER_DISPLAY_AREA                   = ('id', 'displayArea')
    ADMIN_DISCLAIMER_AGREE_REQUIRED                 = ('id', 'agreeRequired')
    ADMIN_MEDIA_COLLABORATION_ENABLED               = ('id', 'mediaCollaborationEnabled-label')
    ADMIN_LOGOUT_BUTTON                             = ('id', 'logout-button')
    ADMIN_DOWNLOAD_ADD                              = ('xpath', "//a[@class='add']")
    ADMIN_DOWNLOAD_FLAVOR_NAME                      = ('xpath', "//input[@data-name='name']")
    ADMIN_DESCRIPTION_REQUIRED_ENABLE               = ('id', 'descriptionRequired')
    ADMIN_TAGS_REQUIRED_ENABLE                      = ('id', 'tagsRequired')
    ADMIN_DISCLAIMER_TEXT                           = ('xpath', "//textarea[@id='disclaimerText']")
    ADMIN_ADD_PLAYLIST_BUTTON                       = ('xpath', "//a[@class='add' and contains(text(), '+ Add \"lists\"')]")
    ADMIN_PLAYLIST_NAME                             = ('xpath', "//input[@value='PLAYLIST_NAME']")
    ADMIN_DELETE_PLAYLIST_BUTTON                    = ('xpath', "//a[@class='delete' and @data-setdelete='ID']")
    ADMIN_CAROUSEL_TYPE                             = ('xpath', "//select[@id='carousel-type' and @name='carousel[type]']")
    ADMIN_CAROUSEL_ID                               = ('xpath', "//input[@id='carousel-playlistId' and @name='carousel[playlistId]']")
    ADMIN_CAROUSEL_INTERVAL                         = ('xpath', "//input[@id='carouselInterval' and @name='carouselInterval']")
    ADMIN_LIKE_MODULE                               = ('xpath', "//select[@id='enableLike' and @name='enableLike']")
    ADMIN_SELECT_ENABLE                             = ('xpath', '//select[@id="enabled"]')
    ADMIN_RELATED_LIMIT                             = ('xpath', "//input[@id='limit']")
    ADMIN_CLEAR_CACHE_BUTTON                        = ('xpath', "//a[@href='/admin/clear-cache' and contains(text(),'CLEAR THE CACHE')]")
    ADMIN_CONFIRMATION_MSG_CLEAR_CACHE_BUTTON       = ('xpath', "//button[contains (@class, 'ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only')]")
    ADMIN_ENTRIES_PAGE_SIZE_IN_CHANNEL              = ('xpath', "//input[@id='entriesPageSize']")
    ADMIN_SERVICE_URL                               = ('xpath', "//input[@id='serviceUrl']")
    ADMIN_VERIFY_SSL                                = ('xpath', '//select[@id="verifySSL"]')
    ADMIN_NAVIGATION_STYLE                          = ('xpath', "//select[@id='navigationStyle' and @name='navigationStyle']")
    ADMIN_ADD_PRE_POST                              = ('xpath', "//a[@class='add' and contains(text(), '+ Add \"PRE_OR_POST\"')]")
    ADMIN_PRE_POST_ITEM_NAME                        = ('xpath', "//input[@data-name='name' and contains(@id, 'PRE_OR_POST')]")
    ADMIN_PRE_POST_ITEM_VALUE                       = ('xpath', "//input[@data-name='value' and contains(@id, 'PRE_OR_POST')]")
    ADMIN_PRE_POST_ITEM_SAME_WINDOW_OPTION          = ('xpath', "//select[contains(@id, 'PRE_OR_POST') and @data-name='sameWindow']")
    ADMIN_DELETE_PRE_POST_LINK_NAME                 = ('xpath', "//input[@value='LINK_NAME' and contains(@id, 'PRE_OR_POST')]")
    ADMIN_CUSTOM_DATA_PROFILE_ID_DROPDOWN           = ('xpath', '//dd[@id="profileId-element"]')
    ADMIN_CUSTOM_DATA_PROFILE_ID_OPTION             = ('xpath', '//option[@value="PROFILE_ID"]')
    ADMIN_SECURE_EMBED                              = ('id', 'secureEmbed')
    ADMIN_ASSIGNMENT_SUBMISSION                     = ('xpath', '//select[@id="enableAssignmentSubmission"]')
    ADMIN_GALLERY_PAGE_SIZE                         = ('xpath', "//input[@id='pageSize']")
    ADMIN_ADD_ALLOWEDUSERS                          = ('xpath', "//a[@class='add' and contains(text(),'+ Add \"allowedUsers\"')]")
    ADMIN_SELECT_USERS                              = ('xpath', "//a[@class='button' and contains(text(),'Select Users')]")
    ADMIN_ENTER_USER_TEXT_BOX                       = ('xpath', "//input[@id='SelectUsers-userName']")
    ADMIN_SELECT_USER_FROM_LIST                     = ('xpath', "//strong[contains(text(), 'USER_NAME')]")
    ADMIN_USER_IN_ALLOWEDUSER                       = ('xpath', "//input[@value='USER_NAME']")
    ADMIN_CLICK_ON_SUBMIT                           = ('xpath', "//span[@class='ui-button-text' and contains(text(),'Submit')]")
    #=============================================================================================================
    # @Author: Oleg Sigalov 
    def navigateToAdminPage(self):
        if self.clsCommon.myMedia.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL, False, 1) == True:
            writeToLog("INFO","Already on Admin page")
            return True
            
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL) == False:
            writeToLog("INFO","FAILED to load Admin page")
            return False
        return True

              
    # @Author: Oleg Sigalov           
    def loginToAdminPage(self, username='default', password='default', forceNavigate=False):
        if username == 'default':
            username = localSettings.LOCAL_SETTINGS_ADMIN_USERNAME
        if password == 'default':
            password = localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD
        
        if forceNavigate == False:    
            if self.verifyUrl("admin\/config" , True, 3) == True:
                return True  
                         
        if self.navigateToAdminPage() == False:
            return False
                
        # Verify if already logged in
        if self.wait_visible(self.ADMIN_LOGOUT_BUTTON, 3) != False:
            return True
        
        # Enter test partner username
        if self.send_keys(self.clsCommon.login.LOGIN_USERNAME_FIELD, username) == False:
            writeToLog("INFO","FAILED to enter username")
            return False 
                   
        # Enter test partner password
        if self.send_keys(self.clsCommon.login.LOGIN_PASSWORD_FIELD, password) == False:
            writeToLog("INFO","FAILED to enter password")
            return False
        
        # Click Sign In
        if self.click(self.clsCommon.login.LOGIN_SIGN_IN_BTN) == False:
            writeToLog("INFO","FAILED to click on Sign In button")
            return False
        
        # Wait page load
        self.wait_for_page_readyState()
        return True
    
    
    # @Author: Oleg Sigalov
    # NOT FINISHED    
    # isEnabled - True to enable, False to disable
    # displayArea - enums.DisclaimerDisplayArea
    # agreeRequired - True for Yes, False - No
    # disclaimerProfileId - TODO
    # disclaimerField - TODO
    # disclaimerText - TODO
    def adminDisclaimer(self, isEnabled, displayArea='', agreeRequired='', disclaimerProfileId='', disclaimerField='', disclaimerText='', agreeText=''):
        if displayArea == enums.DisclaimerDisplayArea.BEFORE_UPLOAD and agreeRequired == True:
            writeToLog("INFO","FAILED: You can't set displayArea = 'Before Upload' with agreeRequired = Yes, only with 'Before Publish'")
            return False
                    
        # Login to Admin
        if self.loginToAdminPage() == False:
            return False
        
        # Navigate to Disclaimer page
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/disclaimer#enabled') == False:
            writeToLog("INFO","FAILED to load Admin Disclaimer page")
            return False
        
        # Enable/Disable Disclaimer
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set disclaimer as: " + str(selection))
            return False
        
        # Set disclaimer Text
        if disclaimerText != '':
            if self.clear_and_send_keys(self.ADMIN_DISCLAIMER_TEXT, str(disclaimerText)) == False:
                writeToLog("INFO","FAILED to Set Disclaimer Text as: " + str(disclaimerText))
                return False
            else:
                writeToLog("INFO","KMS Admin: Module disclaimer - Disclaimer Text was set")

        # Set Display Area
        if displayArea != '':
            if self.select_from_combo_by_text(self.ADMIN_DISCLAIMER_DISPLAY_AREA, str(displayArea)) == False:
                writeToLog("INFO","FAILED to Set Display Area as: " + str(displayArea))
                return False
            else:
                writeToLog("INFO","KMS Admin: Module disclaimer - Display Area set to: '" + str(displayArea) + "'")
            
        # Set Agree Required
        if agreeRequired != '':
            selection = self.convertBooleanToYesNo(agreeRequired)
            if self.select_from_combo_by_text(self.ADMIN_DISCLAIMER_AGREE_REQUIRED, str(selection)) == False:
                writeToLog("INFO","FAILED to Set Display Area as: " + str(selection))
                return False            

        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","KMS Admin: Module disclaimer saved as: " + str(selection))
        return True

    
    # @Author: Oleg Sigalov 
    # Click Save on admin page and verify success message
    def adminSave(self):
        # Click Save
        if self.click(self.ADMIN_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Save button")
            return False            
        sleep(2)
        # Verify message - The cache was cleared...
        if self.wait_for_text(self.ADMIN_AFTER_CLICK_SAVE_MSG, 'The cache was cleared.', 20, True) == False:
            writeToLog("INFO","FAILED to verify success message: '...The cache was cleared.'")
            return False 
                        
        # Click OK
        if self.click(self.ADMIN_CONFIRMATION_MSG_OK_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Save button")
            return False 
        
        sleep(2)
        return True
    

    # @Author: Oleg Sigalov    
    # isEnabled - True to enable, False to disable
    # changeOwnerEnabled - True for Yes, False - No
    # allowGroupsCollaboration - True for Yes, False - No
    # collaborationEnabledInUploadForm - True for Yes, False - No
    # showInSearch - True for Yes, False - No
    def adminMediaCollaboration(self, isEnabled, changeOwnerEnabled='', allowGroupsCollaboration='', collaborationEnabledInUploadForm='', showInSearch=''):
        # Login to Admin
        if self.loginToAdminPage() == False:
            return False
        
        # Navigate to Media Collaboration page
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/mediaCollaboration#mediaCollaborationEnabled') == False:
            writeToLog("INFO","FAILED to load Admin Media Collaboration page")
            return False
        
        # Enable/Disable Media Collaboration
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_MEDIA_COLLABORATION_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set disclaimer as: " + str(selection))
            return False
            
            
    def adminDownloadMedia(self, isEnabled):
        # Login to Admin
        if self.loginToAdminPage() == False:
            return False
        
        # Navigate to Disclaimer page
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/downloadmedia#enabled') == False:
            writeToLog("INFO","FAILED to load Admin Download-media page")
            return False
        
        # Enable/Disable Disclaimer
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set Download as: " + str(selection))
            return False
        
        flavorsList = ["Source", "Mobile (3GP)", "Basic/Small - WEB/MBL (H264/400)","Basic/Small - WEB/MBL (H264/600)", "SD/Small - WEB/MBL (H264/900)", "SD/Large - WEB/MBL (H264/1500)","HD/720 - WEB (H264/2500)","HD/1080 - WEB (H264/4000)","WebM"] 
        for flavor in flavorsList:
            if self.click(self.ADMIN_DOWNLOAD_ADD) == False:
                writeToLog("INFO","FAILED to click on Add flavor button")
                return False
             
            asteriskElement = self.driver.find_element_by_xpath(".//legend[@class='num' and contains(text(), '*')]")
            parentAsteriskElement = asteriskElement.find_element_by_xpath("..")
            comboboxElement = parentAsteriskElement.find_element_by_tag_name("select")
            Select(comboboxElement).select_by_visible_text(flavor)

            textElement = parentAsteriskElement.find_element_by_tag_name("input")
            textElement.clear()
            textElement.send_keys(flavor)
            
            if self.adminSave() == False:
                writeToLog("INFO","FAILED to save changes in admin page")
                return False
            else:
                writeToLog("INFO","the following Flavor was added: " + flavor)
                
        return True
    
    
    # @Autor: Inbar Willman
    # isEnabled - True to enable, False to disable
    def enableRequiredField(self, isEnableDescripiton, isEnableTags, requiredFieldDescription, requiredFieldTags):
        # Login to Admin
        if self.loginToAdminPage() == False:
            return False
         
        #Navigate to required fields in metadata module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/metadata#descriptionRequired') == False:
            writeToLog("INFO","FAILED to load Admin Metadata page")
            return False  
         
        #Enable/Disable description field
        if requiredFieldDescription == True:
            selection_description = self.convertBooleanToYesNo(isEnableDescripiton)
            if self.select_from_combo_by_text(self.ADMIN_DESCRIPTION_REQUIRED_ENABLE, selection_description) == False:
                writeToLog("INFO","FAILED to set descriptionRequired as: " + str(selection_description))
                return False 
         
        #Enable/Disable tag field   
        if requiredFieldTags == True:
            selection_tags = self.convertBooleanToYesNo(isEnableTags)
            if self.select_from_combo_by_text(self.ADMIN_TAGS_REQUIRED_ENABLE, selection_tags) == False:
                writeToLog("INFO","FAILED to set tagsRequired as: " + str(selection_tags))
                return False
         
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save required fields")
            return False 
 
        return True    
    
    
    # @Autor: Michal zomper
    # the function set playlist in mediaSpace home page
    def setPlaylistToHomePage(self, playlistName, playlistId, listType):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED tologin to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/home') == False:
            writeToLog("INFO","FAILED to load home module page in admin")
            return False
        
        self.clsCommon.sendKeysToBodyElement(Keys.PAGE_DOWN)
        
        if self.click(self.ADMIN_ADD_PLAYLIST_BUTTON) == False:
            writeToLog("INFO","FAILED to click on add list button")
            return False
                       
        asteriskElement = self.driver.find_element_by_xpath(".//legend[@class='num' and contains(text(), '*')]")
        parentAsteriskElement = asteriskElement.find_element_by_xpath("..")
        comboboxElement = parentAsteriskElement.find_element_by_tag_name("select")
        Select(comboboxElement).select_by_visible_text(listType)
        
        sleep(1)
        playlistFildes = parentAsteriskElement.find_elements_by_tag_name("input")
        # Set playlist name
        if playlistFildes[0].send_keys(playlistName) == False:
            writeToLog("INFO","FAILED to set playlist name")
            return False
        
        sleep(1)
        # Set playlist id
        if playlistFildes[1].send_keys(playlistId) == False:
            writeToLog("INFO","FAILED to set playlist id")
            return False
            
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in home page")
            return False 
        
        writeToLog("INFO","Success, playlist '" + playlistName + "' was set to home page")
        return True  
    
    
    # @Autor: Michal Zomper
    # The function delete playlist from admin page 
    def deletePlaylistFromHomePage(self, playlistName):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/home') == False:
            writeToLog("INFO","FAILED to load home module page in admin")
            return False
        
        tmp_playlist_name = (self.ADMIN_PLAYLIST_NAME[0], self.ADMIN_PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
        try:
            playlist = self.get_element(tmp_playlist_name).get_attribute("id")
        
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get playlist attribute id")
            return False
        
        tmp = playlist.split('-')
        
        if tmp[1] == '':
            writeToLog("INFO","FAILED to get playlist attribute id")
            return False
        
        tmpDeleteButon = (self.ADMIN_DELETE_PLAYLIST_BUTTON[0], self.ADMIN_DELETE_PLAYLIST_BUTTON[1].replace('ID', tmp[1]))
        
        if self.click(tmpDeleteButon, 20) == False:
            writeToLog("INFO","FAILED to click on delete playlist button")
            return False
        
        sleep(2)
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in home page")
            return False 
        
        writeToLog("INFO","Success, playlist '" + playlistName + "' was deleted from admin")
        return True  
        
        
    # @Autor: Michal Zomper      
    def setCarouselForHomePage(self, listType, playlistId=''):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/home') == False:
            writeToLog("INFO","FAILED to load home module page in admin")
            return False
        
        sleep(1)               
        if self.select_from_combo_by_text(self.ADMIN_CAROUSEL_TYPE, listType) == False:
            writeToLog("INFO","FAILED to change carousel type to: " + listType)
            return False    
        
        if listType == "Custom Playlist":
            if self.clear_and_send_keys(self.ADMIN_CAROUSEL_ID, playlistId) == False:
                writeToLog("INFO","FAILED to insert playlist it to carousel info")
                return False   
            
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in home page")
            return False 
        
        writeToLog("INFO","Success, playlist was set to: " + listType)
        return True  
    
    
    # @Autor: Michal Zomper 
    def setCarouselInterval(self, carouselInterval):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/home') == False:
            writeToLog("INFO","FAILED to load home module page in admin")
            return False
        
        sleep(1) 
        tmp_carouselInterval = carouselInterval*1000
        if self.clear_and_send_keys(self.ADMIN_CAROUSEL_INTERVAL, tmp_carouselInterval) == False:
            writeToLog("INFO","FAILED to insert carousel interval" )
            return False   
        
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in home page")
            return False 
        
        writeToLog("INFO","Success, update carousel interval to: " + str(tmp_carouselInterval))
        return True  
         
         
    # @Autor: Michal Zomper      
    def enablelike(self, isEnabled):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/application') == False:
            writeToLog("INFO","FAILED to load application page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable like field
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_LIKE_MODULE, selection) == False:
            writeToLog("INFO","FAILED to set like as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, Like module was set to '" +  str(selection) + "'")
        return True  
    
    
    # @Autor: Michal Zomper      
    def enableChannelCatrgories(self, isEnabled):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/channelcategories') == False:
            writeToLog("INFO","FAILED to load application page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable channelcategories field
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set channelcategories as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, channelcategories module was set to '" + str(selection) + "'")
        return True
    
    
    # @Autor: Michal Zomper      
    def enableThumbnail(self, isEnabled):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/thumbnails') == False:
            writeToLog("INFO","FAILED to load thumbnails page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable thumbnails field
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set thumbnails as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, thumbnails module was set to '" + str(selection) + "'")
        return True
    
    
    # @Author: Inbar Willman
    # isEnable = True to enable module, isEnable = False to disabled module
    def enableSideMyMedia(self, isEnabled):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/sidemymedia') == False:
            writeToLog("INFO","FAILED to load SideMyMedia page in admin")
            return False
        sleep(1)    
        
        #Enable/Disable module
        selection_description = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_SELECT_ENABLE, selection_description) == False:
            writeToLog("INFO","FAILED to set sideMyMedia as: " + str(selection_description))
            return False 
        
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        
        return True         
    
    
    # @Author: Michal Zomper
    def clearCache(self):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        if self.click(self.ADMIN_CLEAR_CACHE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on clear cache button")
            return False
        
        sleep(2)  
        if self.click(self.ADMIN_CONFIRMATION_MSG_CLEAR_CACHE_BUTTON, 10, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on confirm clear cache button")
            return False
            
        writeToLog("INFO","Success, cache was clear")
        return True
    
    
    # @Autor: Michal Zomper      
    def enableChannelSubscription(self, isEnabled):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/channelsubscription') == False:
            writeToLog("INFO","FAILED to load channel subscription page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable thumbnails field
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set channel subscription as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, channel subscription module was set to '" + str(selection) + "'")
        return True
    
    
    # @Author: Inbar Willman
    # isEnable = True to enable module, isEnable = False to disabled module
    def enableRelatedMedia(self, isEnabled, limit=''):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/related') == False:
            writeToLog("INFO","FAILED to load Related page in admin")
            return False
        sleep(1)    
        
        #Enable/Disable module
        selection_description = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_SELECT_ENABLE, selection_description) == False:
            writeToLog("INFO","FAILED to set sideMyMedia as: " + str(selection_description))
            return False 
        
        if limit != '':
            if self.clear_and_send_keys(self.ADMIN_RELATED_LIMIT, str(limit)) == False:
                writeToLog("INFO","FAILED to set limit to related media: " + str(limit))
                return False         
            
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        return True   
    
    def changNumberEentriesPageSizeForChannel(self, numberOfEntries):   
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/channels') == False:
            writeToLog("INFO","FAILED to load Channels page in admin")
            return False
        sleep(1)  
        
        if self.clear_and_send_keys(self.ADMIN_ENTRIES_PAGE_SIZE_IN_CHANNEL, numberOfEntries) == False:
            writeToLog("INFO","FAILED to change number of entries to display in channel page")
            return False
        
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        return True
    
    
    # @Author: Oleg Sigalov
    # instance = instance number
    # verifySSL = True for 'yes', False for 'No'
    def setServiceUrl(self, instance, username, password, serviceUrl, verifySSL):
        # Set base URL
        baseUrlSplit = localSettings.LOCAL_SETTINGS_TEST_BASE_URL.split('.')
        localSettings.LOCAL_SETTINGS_TEST_BASE_URL = 'http://' + instance + '.' + '.'.join(baseUrlSplit[1:])
        localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL = localSettings.LOCAL_SETTINGS_TEST_BASE_URL + '/admin'
        if self.loginToAdminPage(username, password, True) == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/client') == False:
            writeToLog("INFO","FAILED to load client page in admin")
            return False
        sleep(0.5)
        
        # Set serviceUrl
        if self.clear_and_send_keys(self.ADMIN_SERVICE_URL, serviceUrl) == False:
            writeToLog("INFO","FAILED to set service url")
            return False
        
        # Set verifySSL
        selection = self.convertBooleanToYesNo(verifySSL)
        if self.select_from_combo_by_text(self.ADMIN_VERIFY_SSL, selection) == False:
            writeToLog("INFO","FAILED to set verifySSL as: " + str(selection))
            return False        
        
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        return True   
    
    
    # @Author: Inbar Willman
    # Enable category scheduling - enabling this module will enable scheduling sort by and filter in global search and categories
    def enableCategoryScheduling(self, isEnabled):
        #Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/categoryscheduling') == False:
            writeToLog("INFO","FAILED to load category scheduling page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable category scheduling module
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set category scheduling module as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, category scheduling module was set to: " + str(selection) + "'")
        return True        
    
    # @Author: Michal Zomper
    def setNavigationStyle(self, navigationStyle):
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/navigation') == False:
            writeToLog("INFO","FAILED to load navigation page in admin")
            return False
        sleep(1) 
        
        if self.select_from_combo_by_text(self.ADMIN_NAVIGATION_STYLE, navigationStyle.value) == False:
            writeToLog("INFO","FAILED to change navigate style to: " + navigationStyle.value)
            return False    
        
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, navigation style was set to: " + navigationStyle.value + "'")
        return True  
    
    # @Author: Michal Zomper
    # This function add link items to the pre post option in navigation tab
    def addPrePostLinkItem(self, preOrPost, name, url, sameWindow):
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/navigation') == False:
            writeToLog("INFO","FAILED to load navigation page in admin")
            return False
        sleep(1) 
        
        if preOrPost == enums.NavigationPrePost.PRE:
            addbuttontmp= (self.ADMIN_ADD_PRE_POST[0], self.ADMIN_ADD_PRE_POST[1].replace('PRE_OR_POST', enums.NavigationPrePost.PRE.value))
            if self.click(addbuttontmp,multipleElements=False) == False:
                writeToLog("INFO","FAILED to click on add pre option button")
                return False
            
            if self.addlinkItem(enums.NavigationPrePost.PRE, name, url, sameWindow) == False:
                writeToLog("INFO","FAILED to add pre like item")
                return False
            
        elif preOrPost == enums.NavigationPrePost.POST:
            addbuttontmp= (self.ADMIN_ADD_PRE_POST[0], self.ADMIN_ADD_PRE_POST[1].replace('PRE_OR_POST', enums.NavigationPrePost.POST.value))
            if self.click(addbuttontmp,multipleElements=False) == False:
                writeToLog("INFO","FAILED to click on add pre option button")
                return False
            
            if self.addlinkItem(enums.NavigationPrePost.POST, name, url, sameWindow) == False:
                writeToLog("INFO","FAILED to add post like item")
                return False
        
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, like item was added successfully")
        return True  

   
    # @Author: Michal Zomper
    # This function choose link option(for pre / post item) and set all its parameters
    def addlinkItem(self, preOrPost, name, url, sameWindow):
        asteriskElement = self.driver.find_element_by_xpath(".//legend[@class='num' and contains(text(), '*')]")
        parentAsteriskElement = asteriskElement.find_element_by_xpath("..")
        comboboxElement = parentAsteriskElement.find_element_by_tag_name("select")
        if Select(comboboxElement).select_by_visible_text("Link") == False:
            writeToLog("INFO","FAILED to select 'link' type")
            return False
        
        
        if preOrPost == enums.NavigationPrePost.PRE:
            linkNameTmp= (self.ADMIN_PRE_POST_ITEM_NAME[0], self.ADMIN_PRE_POST_ITEM_NAME[1].replace('PRE_OR_POST', enums.NavigationPrePost.PRE.value))
            elementLinkNameTmp = parentAsteriskElement.find_elements_by_xpath(linkNameTmp[1])[1]
            elementLinkNameTmp.clear() 
            if self.send_keys_to_element(elementLinkNameTmp, name) == False:
                writeToLog("INFO","FAILED to insert link item name")
                return False
            
            linkValueTmp= (self.ADMIN_PRE_POST_ITEM_VALUE[0], self.ADMIN_PRE_POST_ITEM_VALUE[1].replace('PRE_OR_POST', enums.NavigationPrePost.PRE.value))
            elementValueNameTmp = parentAsteriskElement.find_elements_by_xpath(linkValueTmp[1])[1]
            elementValueNameTmp.clear()
            if self.send_keys_to_element(elementValueNameTmp, url) == False:
                writeToLog("INFO","FAILED to insert link item value")
                return False
                
            sameWindowTmp = (self.ADMIN_PRE_POST_ITEM_SAME_WINDOW_OPTION[0], self.ADMIN_PRE_POST_ITEM_SAME_WINDOW_OPTION[1].replace('PRE_OR_POST', enums.NavigationPrePost.PRE.value))
            elementLinkSameWindowTmp = parentAsteriskElement.find_elements_by_xpath(sameWindowTmp[1])[1]  
            if Select(elementLinkSameWindowTmp).select_by_visible_text(sameWindow.value) == False:
                writeToLog("INFO","FAILED to set '" + sameWindow.value + "' value in same window option")
                return False
            
        elif preOrPost == enums.NavigationPrePost.POST:
            linkNameTmp= (self.ADMIN_PRE_POST_ITEM_NAME[0], self.ADMIN_PRE_POST_ITEM_NAME[1].replace('PRE_OR_POST', enums.NavigationPrePost.POST.value))
            elementLinkNameTmp = parentAsteriskElement.find_elements_by_xpath(linkNameTmp[1])[1]
            elementLinkNameTmp.clear()
            if self.send_keys_to_element(elementLinkNameTmp, name) == False:
                writeToLog("INFO","FAILED to insert link item name")
                return False
            
            linkValueTmp= (self.ADMIN_PRE_POST_ITEM_VALUE[0], self.ADMIN_PRE_POST_ITEM_VALUE[1].replace('PRE_OR_POST', enums.NavigationPrePost.POST.value))
            elementValueNameTmp = parentAsteriskElement.find_elements_by_xpath(linkValueTmp[1])[1]
            elementValueNameTmp.clear()
            if self.send_keys_to_element(elementValueNameTmp, url) == False:
                writeToLog("INFO","FAILED to insert link item value")
                return False 
            
            sameWindowTmp = (self.ADMIN_PRE_POST_ITEM_SAME_WINDOW_OPTION[0], self.ADMIN_PRE_POST_ITEM_SAME_WINDOW_OPTION[1].replace('PRE_OR_POST', enums.NavigationPrePost.POST.value))
            elementLinkSameWindowTmp = parentAsteriskElement.find_elements_by_xpath(sameWindowTmp[1])[1]
            if Select(elementLinkSameWindowTmp).select_by_visible_text(sameWindow.value) == False:
                writeToLog("INFO","FAILED to set '" + sameWindow.value + "' value in same window option")
                return False

        return True
    
    
    def logoutAdmin(self):
        if self.click(self.ADMIN_LOGOUT_BUTTON) == False:
            writeToLog("INFO","FAILED to click on logout from admin page")
            return False
        
    
    def deletePrePostLink(self, preOrPost, linkName):
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/navigation') == False:
            writeToLog("INFO","FAILED to load navigation page in admin")
            return False
        sleep(1) 
        
        if preOrPost == enums.NavigationPrePost.PRE:
            linkNameTmp= (self.ADMIN_DELETE_PRE_POST_LINK_NAME[0], self.ADMIN_DELETE_PRE_POST_LINK_NAME[1].replace('LINK_NAME',linkName).replace('PRE_OR_POST', enums.NavigationPrePost.PRE.value))
        if preOrPost == enums.NavigationPrePost.POST:
            linkNameTmp= (self.ADMIN_DELETE_PRE_POST_LINK_NAME[0], self.ADMIN_DELETE_PRE_POST_LINK_NAME[1].replace('LINK_NAME',linkName).replace('PRE_OR_POST', enums.NavigationPrePost.POST.value))
        
        try:
            linkName = self.get_element(linkNameTmp).get_attribute("id")
        
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get link name attribute id")
            return False
        
        tmp = linkName.split('-')
        
        if tmp[1] == '':
            writeToLog("INFO","FAILED to get link attribute id")
            return False
        
        tmpDeleteButon = (self.ADMIN_DELETE_PLAYLIST_BUTTON[0], self.ADMIN_DELETE_PLAYLIST_BUTTON[1].replace('ID', tmp[1]))
        
        if self.click(tmpDeleteButon, 20) == False:
            writeToLog("INFO","FAILED to click on delete playlist button")
            return False
        
        sleep(2)
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in home page")
            return False 
        
        writeToLog("INFO","Success, Pre / Post link was deleted from admin")
        return True  
    
    
    # @Author: Oded berihon
    # This function enables the custom metadata module 
    def enableCustomMetadata(self, isEnabled):
        #Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to Custometadata module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/customdata') == False:
            writeToLog("INFO","FAILED to load customdata page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable custometadata module
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set custom metadata module as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
            
        writeToLog("INFO","Success, custom metadata module was set to: " + str(selection) + "'")
        return True   
    
    
    # @Author: Inbar Willman
    # Choose customdata profile id
    def selectCustomdataProfileId(self, profileId):
        #Click on profile id dropdown
        if self.click(self.ADMIN_CUSTOM_DATA_PROFILE_ID_DROPDOWN) == False:
            writeToLog("INFO","FAILED to click on customdata profile id dropdown")
            return False
        
        # Click on custom profile id dropdown option
        tmp_selection = (self.ADMIN_CUSTOM_DATA_PROFILE_ID_OPTION[0], self.ADMIN_CUSTOM_DATA_PROFILE_ID_OPTION[1].replace('PROFILE_ID', profileId))
        if self.click(tmp_selection) == False:
            writeToLog("INFO","FAILED to click on customdata profile id dropdown option")
            return False  
        
        # Save customdata profile id
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False  
        
        writeToLog("INFO","Success, customdata profile id:" + profileId + " was set successfully")
        return True
    
    
    # @Author: Oleg Sigalov
    # This function enables the playlist secure embed module 
    def enableSecureEmbedPlaylist(self, isEnabled):
        #Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to Custometadata module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/embedplaylist#secureEmbed') == False:
            writeToLog("INFO","FAILED to load Embed playlist page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable custometadata module
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_SECURE_EMBED, selection) == False:
            writeToLog("INFO","FAILED to set secureEmbed as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
            
        writeToLog("INFO","Success, secureEmbed was set to: " + str(selection) + "'")
        return True    
    
    
    # @Author: Inbar Willman
    def enableDisabledAssignmentSubmission(self, isEnabled):     
        #Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        sleep(2)
        #Navigate to CustometadatabrowseAndEmbed module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/browseandembed') == False:
            writeToLog("INFO","FAILED to load 'browse and embed' page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable assignment submission
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ASSIGNMENT_SUBMISSION, selection) == False:
            writeToLog("INFO","FAILED to set assignment submission as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
            
        writeToLog("INFO","Success, assignment submission was set to: " + str(selection) + "'")
        return True            
    
    
    # @Autor: Michal Zomper 
    def setGallerypageSize(self, galleryPageSize):
        # Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/gallery') == False:
            writeToLog("INFO","FAILED to load gallery module page in admin")
            return False
        
        sleep(1) 
        if self.clear_and_send_keys(self.ADMIN_GALLERY_PAGE_SIZE, galleryPageSize) == False:
            writeToLog("INFO","FAILED to insert gallery page size" )
            return False   
        
        #Save changes
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in home page")
            return False 
        
        writeToLog("INFO","Success, Gallery page size was updated")
        return True
    
    
    # @Author: Horia Cus
    # This function will change the secure embed from Embed tab state
    # if isEnabled = True, secureEmbed will be activated
    # if isEnabled = False, secureEmbed will be deactivated
    def enabledSecureEmbed(self, isEnabled):
        #Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to Custometadata module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/embed') == False:
            writeToLog("INFO","FAILED to load Embed page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable custometadata module
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_SECURE_EMBED, selection) == False:
            writeToLog("INFO","FAILED to set secureEmbed as: " + str(selection))
            return False
         
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
            
        writeToLog("INFO","Success, secureEmbed was set to: " + str(selection) + "'")
        return True   
    
    
    # @Author: Michal Zomper
    # Enable / Disable Recscheduling
    def enableRecscheduling(self, isEnabled):
        #Login to Admin
        if self.loginToAdminPage() == False:
            writeToLog("INFO","FAILED to login to admin page")
            return False
        
        #Navigate to home module
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL + '/config/tab/recscheduling') == False:
            writeToLog("INFO","FAILED to load recscheduling page in admin")
            return False
        sleep(1) 
        
        #Enable/Disable category scheduling module
        selection = self.convertBooleanToYesNo(isEnabled)
        if self.select_from_combo_by_text(self.ADMIN_ENABLED, selection) == False:
            writeToLog("INFO","FAILED to set recscheduling module as: " + str(selection))
            return False
         
        #Check if the user is already in allowedUsers list
        tmpUser= (self.ADMIN_USER_IN_ALLOWEDUSER[0], self.ADMIN_USER_IN_ALLOWEDUSER[1].replace('USER_NAME', localSettings.LOCAL_SETTINGS_LOGIN_USERNAME.lower()))
        if self.wait_element(tmpUser, timeout=5) == False:
            #user isn't exist and need to be added to list
            if self.click(self.ADMIN_ADD_ALLOWEDUSERS) == False:
                writeToLog("INFO","FAILED to click on allowedUsers button")
                return False
            
            #set user
            asteriskElement = self.driver.find_element_by_xpath(".//legend[@class='num' and contains(text(), '*')]")
            parentAsteriskElement = asteriskElement.find_element_by_xpath("..")
    
            sleep(1)
            if self.click_child(parentAsteriskElement, self.ADMIN_SELECT_USERS, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on select users button")
                return False
            sleep(1)
           
            if self.click(self.ADMIN_ENTER_USER_TEXT_BOX) == False:
                writeToLog("INFO","FAILED to click on user textbox")
                return False
            
            if self.send_keys(self.ADMIN_ENTER_USER_TEXT_BOX, localSettings.LOCAL_SETTINGS_LOGIN_USERNAME) == False:
                writeToLog("INFO","FAILED to insert user name")
                return False
            sleep(2)
 
            self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN)
            sleep(1)
            self.clsCommon.sendKeysToBodyElement(Keys.ENTER)
            
            if self.click(self.ADMIN_CLICK_ON_SUBMIT) == False:
                writeToLog("INFO","FAILED to click on submit button")
                return False
        
        if self.adminSave() == False:
            writeToLog("INFO","FAILED to save changes in admin page")
            return False
        
        writeToLog("INFO","Success, recscheduling module was set to: " + str(selection) + "'")
        return True    