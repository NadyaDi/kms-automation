from base import *
import clsTestService
import enums
from logger import writeToLog
from selenium.webdriver.support.ui import Select


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
    #=============================================================================================================
    # @Author: Oleg Sigalov 
    def navigateToAdminPage(self):
        if self.clsCommon.myMedia.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL, False, 1) == True:
            writeToLog("INFO","Already on Admin page")
            return True
            
        if self.navigate(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL) == False:
            writeToLog("INFO","FAILED to load Admin page")
            return False
                    
        if self.clsCommon.myMedia.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_ADMIN_URL, False) == False:
            return False
        else:
            return True
              
              
    # @Author: Oleg Sigalov           
    def loginToAdminPage(self):
        if self.navigateToAdminPage() == False:
            return False
                
        # Verify if already logged in
        if self.wait_visible(self.ADMIN_LOGOUT_BUTTON, 3) != False:
            return True
        
        # Enter test partner username
        if self.send_keys(self.clsCommon.login.LOGIN_USERNAME_FIELD, localSettings.LOCAL_SETTINGS_ADMIN_USERNAME) == False:
            writeToLog("INFO","FAILED to enter username")
            return False 
                   
        # Enter test partner password
        if self.send_keys(self.clsCommon.login.LOGIN_PASSWORD_FIELD, localSettings.LOCAL_SETTINGS_ADMIN_PASSWORD) == False:
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
    