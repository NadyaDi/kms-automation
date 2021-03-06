from base import *
import clsTestService
from general import General
from logger import writeToLog
from editEntryPage import EditEntryPage
import enums
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.common import action_chains
import datetime
import calendar



class MyMedia(Base):
    driver = None
    clsCommon = None

    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #My Media locators:
    #=============================================================================================================
    MY_MEDIA_TITLE                                              = ('xpath', "//h1[@class='inline' and text()='My Media']")
    MY_MEDIA_SEARCH_BAR                                         = ('id', 'searchBar')
    MY_MEDIA_SEARCH_BAR_OLD_UI                                  = ('id', 'searchBar')
    MY_MEDIA_ELASTIC_SEARCH_BAR                                 = ('xpath', "//input[@class='searchForm__text']")
    MY_MEDIA_NO_RESULTS_ALERT                                   = ('xpath', "//div[@id='myMedia_scroller_alert' and contains(text(),'There are no more media items.')]")
    MY_MEDIA_ENRTY_DELETE_BUTTON                                = ('xpath', '//*[@title = "Delete ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
    MY_MEDIA_ENRTY_EDIT_BUTTON                                  = ('xpath', '//*[@title = "Edit ENTRY_NAME"]')# When using this locator, replace 'ENTRY_NAME' string with your real entry name
#    MY_MEDIA_CONFIRM_ENTRY_DELETE                               = ('xpath', "//a[contains(@id,'delete_button_') and @class='btn btn-danger']")
    MY_MEDIA_CONFIRM_ENTRY_DELETE                               = ('xpath', "//a[@data-handler='1' and text()='Delete']")
    MY_MEDIA_ENTRY_CHECKBOX                                     = ('xpath', '//*[@title = "ENTRY_NAME"]')
    MY_MEDIA_ACTIONS_BUTTON                                     = ('id', 'actionsDropDown')
    MY_MEDIA_ACTIONS_BUTTON_PUBLISH_BUTTON                      = ('id', 'Publish')
    MY_MEDIA_ACTIONS_BUTTON_DELETE_BUTTON                       = ('id', 'tab-Delete')
    MY_MEDIA_ACTIONS_BUTTON_ADDTOPLAYLIST_BUTTON                = ('id', 'Addtoplaylists')
    MY_MEDIA_PUBLISH_UNLISTED                                   = ('id', 'unlisted')
    MY_MEDIA_PUBLISH_PRIVATE                                    = ('id', 'private')
    MY_MEDIA_PUBLISH_SAVE_BUTTON                                = ('xpath', "//button[@class='btn btn-primary pblSave' and text()='Save']")
    MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG                          = ('xpath', "//div[contains(.,'Media successfully set to Unlisted')]")
    MY_MEDIA_PUBLISHED_AS_PRIVATE_MSG                           = ('xpath', "//div[contains(.,'Media successfully set to Private')]")
    MY_MEDIA_PAGE_TITLE                                         = ('xpath', "//h1[@class='inline' and contains(text(), 'My Media')]")
#     MY_MEDIA_PUBLISHED_RADIO_BUTTON                             = ('id', 'published') #This refers to the publish radio button after clicking action > publish
    MY_MEDIA_PUBLISHED_RADIO_BUTTON                             = ('xpath', "//input[@id='published']") #This refers to the publish radio button after clicking action > publish
    MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION                         = ('class_name', 'pblTabCategory')
    MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION                          = ('class_name', 'pblTabChannel')
    MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH                         = ('xpath', "//span[contains(.,'PUBLISHED_CATEGORY')]")# When using this locator, replace 'PUBLISHED_CATEGORY' string with your real category/channel name
    MY_MEDIA_SAVE_MESSAGE_CONFIRM                               = ('xpath', "//div[@class='alert alert-success ' and contains(text(), 'Media successfully published')]")
    MY_MEDIA_DISCLAIMER_MSG                                     = ('xpath', "//div[@class='alert ' and contains(text(), 'Complete all the required fields and save the entry before you can select to publish it to categories or channels.')]")
    #MY_MEDIA_ENTRY_PARNET                                       = ('xpath', "//div[@class='photo-group thumb_wrapper' and @title='ENTRY_NAME']")
    MY_MEDIA_ENTRY_CHILD                                        = ('xpath', "//p[@class='status_content' and contains(text(), 'ENTRY_PRIVACY')]")
    MY_MEDIA_ENTRY_PARNET                                       = ('xpath', "//span[@class='entry-name' and text() ='ENTRY_NAME']/ancestor::a[@class='entryTitle tight']")
    #MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI                         = ('xpath', "//a[@id ='accordion-ENTRY_ID']")
    MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI                         = ('xpath', "//div[@id ='accordion_ENTRY_ID']")
    MY_MEDIA_ENTRY_PUBLISHED_BTN                                = ('xpath', "//a[@id ='accordion-ENTRY_ID']/i[@class='icon-plus-sign kmstooltip']")
    MY_MEDIA_ENTRY_CHILD_POPUP                                  = ('xpath', "//strong[@class='valign-top']")
    MY_MEDIA_SORT_BY_DROPDOWNLIST_OLD_UI                        = ('xpath', "//a[@id='sort-btn']")
    MY_MEDIA_SORT_BY_DROPDOWNLIST_NEW_UI                        = ('xpath', "//a[@id='sortBy-menu-toggle']")
    MY_MEDIA_FILTER_BY_STATUS_DROPDOWNLIST                      = ('xpath', "//a[@id='status-btn']")
    MY_MEDIA_FILTER_BY_TYPE_DROPDOWNLIST                        = ('xpath', "//a[@id='type-btn']")
    MY_MEDIA_FILTER_BY_COLLABORATION_DROPDOWNLIST               = ('xpath', "//a[@id='mediaCollaboration-btn']")
    MY_MEDIA_FILTER_BY_SCHEDULING_DROPDOWNLIST                  = ('xpath', "//a[@id='sched-btn']")
    MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI                           = ('xpath', "//a[@role='menuitem' and contains(text(), 'DROPDOWNLIST_ITEM')]")
    MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI                           = ('xpath', "//span[@class='filter-checkbox__label' and text()='DROPDOWNLIST_ITEM']")
    MY_MEDIA_ENTRY_TOP                                          = ('xpath', "//span[@class='entry-name' and text()='ENTRY_NAME']")
    MY_MEDIA_END_OF_PAGE                                        = ('xpath', "//div[@class='alert alert-info endlessScrollAlert']")
    MY_MEDIA_TABLE_SIZE                                         = ('xpath', "//table[@class='table table-condensed table-hover bulkCheckbox mymediaTable mediaTable full']/tbody/tr")
    MY_MEDIA_CONFIRM_CHANGING_STATUS                            = ('xpath', "//a[@class='btn btn-primary' and text()='OK']")
    MY_MEDIA_ENTRY_THUMBNAIL                                    = ('xpath', "//img[@class='thumb_img' and @alt='Thumbnail for entry ENTRY_NAME']")
    MY_MEDIA_ENTRY_THUMBNAIL_ELASTIC_SEARCH                     = ("xpath", "//img[@class='entryThumbnail__img']")
    MY_MEDIA_REMOVE_SEARCH_ICON_OLD_UI                          = ('xpath', "//i[@class='icon-remove']")
    MY_MEDIA_REMOVE_SEARCH_ICON_NEW_UI                          = ('xpath', "//a[@class='clear searchForm_icon']")
    MY_MEDIA_NO_ENTRIES_FOUND                                   = ('xpath', "//div[@class='alert alert-info no-results' and contains(text(), 'No Entries Found')]")
    MY_MEDIA_TABLE                                              = ('xpath', "//table[@class='table table-condensed table-hover bulkCheckbox mymediaTable mediaTable full']")
    MY_MEDIA_IMAGE_ICON                                         = ('xpath', "//i[@class='icon-picture icon-white']")
    MY_MEDIA_IMAGE_ICON_AFTER_SEARCH                            = ('xpath', "//i[@class='entryThumbnail__icon v2ui-photo2-icon']")
    MY_MEDIA_AUDIO_ICON                                         = ('xpath', "//i[@class='icon-music icon-white']")
    MY_MEDIA_AUDIO_ICON_AFTER_SEARCH                            = ('xpath', "//i[@class='entryThumbnail__icon v2ui-audio2-icon']")
    MY_MEDIA_QUIZ_ICON                                          = ('xpath', "//i[@class='icomoon-quiz icon-white']")
    MY_MEDIA_QUIZ_ICON_AFTER_SEARCH                             = ('xpath', "//i[@class='entryThumbnail__icon icomoon-quiz']")
    MY_MEDIA_VIDEO_ICON_OLD_UI                                  = ('xpath', "//i[@class='icon-film icon-white']")
    MY_MEDIA_EXPEND_MEDIA_DETAILS                               = ('xpath', "//div[@class='accordion-body in collapse contentLoaded' and @id='collapse_ENTRY_ID']")
    MY_MEDIA_COLLAPSED_VIEW_BUTTON                              = ('xpath', "//button[@id='MyMediaList' and @data-original-title='Collapsed view']")
    MY_MEDIA_DETAILED_VIEW_BUTTON                               = ('xpath', "//button[@id='MyMediaThumbs' and @data-original-title='Detailed view']")
    SEARCH_RESULTS_ENTRY_NAME                                   = ('xpath', "//span[@class='results-entry__name']")
    MY_MEDIA_FILTERS_BUTTON_NEW_UI                              = ('xpath', "//button[contains(@class,'toggleButton btn shrink-container__button hidden-phone') and text()='Filters']")
    MY_MEDIA_FILTERS_BUTTON_NEW_UI_ACTIVE                       = ('xpath', "//button[contains(@class,'toggleButton btn shrink-container__button hidden-phone active')]")
    SEARCH_RESULTS_ENTRY_NAME_OLD_UI                            = ('xpath', '//span[@class="searchTerm" and text()="ENTRY_NAME"]/ancestor::span[@class="searchme"]')
    EDIT_BUTTON_REQUIRED_FIELD_MASSAGE                          = ('xpath', '//a[@class="hidden-phone" and text()="Edit"]')
    CUSTOM_FIELD                                                = ('xpath', '//input[@id="customdata-DepartmentName"]')
    CUSTOM_FIELD_DROP_DOWN                                      = ('xpath', '//select[@id="customdata-DepartmentDivision"]')
    SET_DATE_FROM_CALENDAR                                      = ('xpath', "//input[@id='customdata-DateEstablished']")
    EDIT_ENTRY_CUSTOM_DATA_CALENDAR_DAY                         = ('xpath', "//td[@class='today day']")
    CLICK_ON_CALENDAR                                           = ('xpath', "//i[@class='icon-th']")
    CLICK_ON_CALENDAR_DATE_ESTABLISHED                          = ('xpath', "//div[@class='input-append date datepicker']")
    SEARCH_IN_DROPDOWN_DISABLED                                 = ('xpath', '//a[@id="fields-menu-toggle" and @class="  disabled dropdown-toggle DropdownFilter__toggle "]')
    SEARCH_IN_DROPDOWN_ENABLED                                  = ('xpath', '//a[@id="fields-menu-toggle" and @class="  dropdown-toggle DropdownFilter__toggle "]')
    SEARCH_IN_DROP_DOWN_OPTION                                  = ('xpath', '//a[@role="menuitem" and text()="FIELD_NAME"]')
    ENTRY_FIELD_IN_RESULTS                                      = ('xpath', '//span[@class="hidden-phone" and contains(text(),"FIELD_NAME")]')
    ENTRY_FIELD_ICON_IN_RESULTS                                 = ('xpath', '//i[contains(@class,"icon icon icon--vertical-align-sub search-results-icon") and @title="FIELD_NAME"]')
    ENTRY_TAG_VALUES_IN_RESULTS                                 = ('xpath', '//span[@class="tag search-results__tag"]')
    ENTRY_FIELD_VALUES_IN_RESULTS                               = ('xpath', '//span[@class="results__result-item--text"]')
    ENTRY_FIELD_IN_RESULTS_SHOW_MORE_BTN                        = ('xpath', '//span[@aria-label="Show More"]')
    ENTRY_FIELD_IN_RESULTS_SHOW_LESS_BTN                        = ('xpath', '//a[@aria-label="Show Less"]')
    ENTRY_FIELD_IN_RESULTS_SHOW_ALL_BTN                         = ('xpath', '//a[@aria-label="Show All"]')
    ENTRY_FIELD_VALUES_SCETION                                  = ('xpath', '//div[@class="results-details-container"]')
    ENTRY_OWNER_DETAILS                                         = ('xpath', '//a[contains(@href,"/createdby/") and text()="OWNER_NAME"]')
    ENTRY_CREATION_DETAILS                                      = ('xpath', '//span[@class="from-now hidden-phone"]')
    ENTRY_CATEGORIES_DETAILS                                    = ('xpath', '//a[@class="results-preview__category"]')
    ENTRY_DETAILS_COMMENTS_ICON                                 = ('xpath', '//i[@class="entryStatistics__stat__icon icon-comment"]')
    ENTRY_DETAILS_HEART_ICON                                    = ('xpath', '//i[@class="entryStatistics__stat__icon icon-heart"]')
    ENTRY_DETAILS_EYE_ICON                                      = ('xpath', '//i[@class="entryStatistics__stat__icon icon-eye-open"]')
    CAPTION_FILTER_INACTIVE                                     = ('xpath', '//a[@aria-checked="false" and  @aria-label="DROPDOWNLIST_ITEM"]')
    FILTER_BUTTON_DROPDOWN_MENU                                 = ('xpath', "//div[contains(@class,'filterBar__filters')]//button[contains(@class,'')]")
    FILTER_CLEAR_ALL_BUTTON                                     = ('xpath', "//div//a[contains(@class,'filters__clear-all')][contains(text(),'Clear All')]")
    FILTER_CHECKBOX_INACTIVE                                    = ('xpath', '//a[@aria-checked="false" and  @aria-label="DROPDOWNLIST_ITEM"]')
    FILTER_NEXT_ARROW                                           = ('xpath', "//button[@class='search-filters__arrow search-filters__arrow--next']")
    FILTER_PREVIOUS_ARROW                                       = ('xpath', "//button[contains(@class,'search-filters__arrow search-filters__arrow--previous')]")
    FILTER_CUSTOM_DURATION                                      = ('xpath', "//div[@class='input-range__slider' and @aria-valuenow='VALUE_TO_REPLACE']")
    FILTER_SINGLE_DATE_CALENDAR                                 = ('xpath', "//div[contains(@class,'date-input')]//input[contains(@type,'text')]")
    FILTER_SINGLE_DATE_CURRENT_MONTH                            = ('xpath', "//div[@class='react-datepicker__current-month' and text()='MONTH YEAR']")
    FILTER_SINGLE_DATE_BACK_BUTTON                              = ('xpath', "//div[contains(@class,'react-datepicker')]//button[1]")
    FILTER_SINGLE_DATE_NEXT_BUTTON                              = ('xpath', "//div[contains(@class,'react-datepicker')]//button[2]")
    FILTER_SINGLE_DATE_DAY                                      = ('xpath', "//div[contains(@class,'react-datepicker__day') and @aria-label='day-DAY_NUMBER']")
    FILTER_SELECT_FIELD_TEXT                                    = ('xpath', "//div[contains(text(),'DROPDOWNLIST_ITEM')]")
    FILTER_SELECT_FIELD_CATEGORY                                = ('xpath', "//span[@class='search-filters-group__title--desktop'][contains(text(),'DROPDOWNLIST_NAME')]")
    ENTRY_NO_MEDIA_FOUND_MESSAGE                                = ('xpath', "//div[contains(@class,'alert alert-info') and text()='No media found.' or text()='No Entries Found' or text()='There are no more media items.']")
    CHANNEL_PENDING_TAB_ICON                                    = ('xpath', "//input[@type='checkbox' and @title='ENTRY_NAME']")
    CHANNEL_PENDING_ENTRY_DATA                                  = ('xpath', "//tr[@id='ENTRY_ID_tr']")
    SEARCH_IN_CHOSEN_OPTION                                     = ('xpath', '//a[@id="fields-menu-toggle" and @data-toggle="dropdown"]')
    ACTION_TAB_OPTION_DISABLED                                  = ('xpath', "//a[@id='tab-ACTIONID' and contains(@class,'disabled')]")
    ACTION_TAB_OPTION_NORMAL                                    = ('xpath', "//a[@id='tab-ACTIONID']")
    EDIT_OPTION_PRESENT_ANY_ENTRY                               = ('xpath', "//a[contains(@title,'Edit')]//i[contains(@class,'icon-pencil')]")
    EDIT_OPTION_PRESENT_PUBLISH_ENTRY                           = ('xpath', "//i[@class='icon-pencil']")
    FILTER_SORT_TYPE_ENABLED                                    = ('xpath', '//a[@aria-checked="true" and @aria-label="DROPDOWNLIST_ITEM undefined"]')
    FILTER_SORT_TYPE_DISABLED                                   = ('xpath', '//a[@aria-checked="false" and @aria-label="DROPDOWNLIST_ITEM undefined"]')
    FILTER_SORT_TYPE_REMOVE_BUTTON                              = ('xpath', "//a[@class='cursor-pointer bubble__a' and @aria-label='DROPDOWNLIST_ITEM']")
    FILTER_CUSTOM_DURATION_SIDEBAR                              = ('xpath', "//div[@class='input-range__track input-range__track--active' and contains(@style,'left:')]")
    #=============================================================================================================
    def getSearchBarElement(self):
        try:
            # Check which search bar do we have: old or new (elastic)
            if self.clsCommon.isElasticSearchOnPage():
                if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
                    if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA:
                        self.clsCommon.blackBoardUltra.switchToBlackboardUltraIframe()
                    return self.get_element(self.MY_MEDIA_ELASTIC_SEARCH_BAR)
                else:
                    return self.get_elements(self.MY_MEDIA_ELASTIC_SEARCH_BAR)[1]
            else:
                return self.wait_visible(self.MY_MEDIA_SEARCH_BAR, 30, True)
        except:
            writeToLog("INFO","FAILED get Search Bar element")
            return False


    # This method, clicks on the menu and My Media
    def navigateToMyMedia(self, forceNavigate=False):
        # KAF
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
            if self.clsCommon.kafGeneric.navigateToMyMediaKAF() == False:
                writeToLog("INFO","FAILED navigate to my media in " + localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST.value)
                return False

        else:
            # Check if we are already in my media page
            if forceNavigate == False:
                if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False, 5) == True:
                    return True

            # Click on User Menu Toggle Button
            if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on User Menu Toggle Button while trying to navigate to My Media during the first try")
                self.switch_to_default_content()
                sleep(5)
                if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON, 20) == False:
                    writeToLog("INFO","FAILED to click on User Menu Toggle Button while trying to navigate to My Media after two tries")
                    return False

            # Click on My Media
            if self.click(self.clsCommon.general.USER_MENU_MY_MEDIA_BUTTON) == False:
                writeToLog("INFO","FAILED to click on My Media from the user menu")
                return False

            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_MEDIA_URL, False) == False:
                writeToLog("INFO","FAILED to navigate to My Media")
                return False

        return True


    # Author: Michal Zomper
    def deleteSingleEntryFromMyMedia(self, entryName):
        # Search for entry in my media
        if self.searchEntryMyMedia(entryName) == False:
            return False

        # Click on delete button
        tmp_entry_name = (self.MY_MEDIA_ENRTY_DELETE_BUTTON[0], self.MY_MEDIA_ENRTY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            writeToLog("INFO","FAILED to click on delete entry button")
            return False
        sleep(5)

        # Click on confirm delete
        if self.click(self.MY_MEDIA_CONFIRM_ENTRY_DELETE, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False
        self.clsCommon.general.waitForLoaderToDisappear()

        writeToLog("INFO","Entry: '" + entryName + "' Was Deleted")
        return True


    #  @Author: Tzachi Guetta
    # The following method can handle list of entries and a single entry:
    #    in order to delete list of entries pass a List[] of entries name, for single entry - just pass the entry name
    #    also: the method will navigate to My media
    # Known limitation: entries MUST be presented on the first page of my media
    def deleteEntriesFromMyMedia(self, entriesNames, showAllEntries=False):
        if self.navigateToMyMedia(forceNavigate=True) == False:
            writeToLog("INFO","FAILED Navigate to my media page")
            return False

        success = True
        # Checking if entriesNames list type
        if type(entriesNames) is list:
            if showAllEntries == True:
                if self.showAllEntries() == False:
                    return False
            for entryName in entriesNames:
                if self.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                    success = False

                writeToLog("INFO","Going to delete Entry: " + entryName)
        else:
            if self.checkSingleEntryInMyMedia(entriesNames) == False:
                    writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                    success = False

            writeToLog("INFO","Going to delete Entry: " + entriesNames)

        if self.clickActionsAndDeleteFromMyMedia() == False:
            writeToLog("INFO","FAILED to click Action -> Delete")
            return False

        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()

        if self.click(self.MY_MEDIA_CONFIRM_ENTRY_DELETE) == False:
            writeToLog("INFO","FAILED to click on confirm delete button")
            return False

        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()

        # Printing the deleted entries
        if success == True:
            if type(entriesNames) is list:
                entries = ", ".join(entriesNames)
                writeToLog("INFO","The following entries were deleted: " + entries + "")
            else:
                writeToLog("INFO","The following entry was deleted: " + entriesNames + "")
        else:
            writeToLog("INFO","Failed, Not all entries were deleted")

        return success


    def searchEntryMyMedia(self, entryName, forceNavigate=True, exactSearch=False):
        # Check if my media page is already open
        # Navigate to My Media
        if self.navigateToMyMedia(forceNavigate) == False:
            return False

        sleep(5)
        # Search Entry
        searchBarElement = self.getSearchBarElement()
        if searchBarElement == False:
            writeToLog("INFO","FAILED to get search bar element")
            return False
        searchBarElement.click()
        if exactSearch == True:
            searchLine = '"' + entryName + '"'
        else:
            if self.clsCommon.isElasticSearchOnPage():
                searchLine = '"' + entryName + '"'
            else:
                searchLine = entryName

        self.getSearchBarElement().send_keys(searchLine + Keys.ENTER)
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()
        return True


    def clickEntryAfterSearchInMyMedia(self, entryName):
        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if self.click(('xpath', "//span[@class='entry-name' and text()='" + entryName + "']"), 10) == False:
                writeToLog("INFO","FAILED to click on Entry: '" + entryName + "' during the first try")
                self.getSearchBarElement().send_keys(Keys.ENTER)
                sleep(1)
                self.clsCommon.general.waitForLoaderToDisappear()
                if self.click(('xpath', "//span[@class='entry-name' and text()='" + entryName + "']"), 10) == False:
                    writeToLog("INFO","FAILED to click on Entry: '" + entryName + "' at the second try")
                    return False
        else:
            result = self.getResultAfterSearch(entryName)
            if result == False:
                return False

            if self.clickElement(result) == False:
                writeToLog("INFO","FAILED to click on Entry: '" + entryName + "'")
                return False
        return True



    # This method for Elastic Search (new UI), returns the result element.
    def getResultAfterSearch(self, searchString):
        #If we are in new UI with Elastic search
        if self.clsCommon.isElasticSearchOnPage() == True:
            results = self.wait_elements(self.SEARCH_RESULTS_ENTRY_NAME, 30)

        #If we are in old UI
        else:
            tmp_results = (self.SEARCH_RESULTS_ENTRY_NAME_OLD_UI[0], self.SEARCH_RESULTS_ENTRY_NAME_OLD_UI[1].replace('ENTRY_NAME', searchString))
            results = self.wait_elements(tmp_results, 30)

        if results == False:
                writeToLog("INFO","No entries found")
                return False

        for result in results:
            if result.text == searchString:
                return result

        writeToLog("INFO","No entries found after search entry: '" + searchString + "'")
        return False


    # This method for Elastic Search (new UI), clicks on the returned result element.
    def clickResultEntryAfterSearch(self, entryName):
        result = self.getResultAfterSearch(entryName)
        if result == False:
            writeToLog("INFO","FAILED to click on Entry: '" + entryName + "'")
            return False
        else:
            if self.clickElement(result) == False:
                writeToLog("INFO","FAILED to click on Entry: '" + entryName + "'")
                return False
        return True


    # Author: Michal Zomper
    def clickEditEntryAfterSearchInMyMedia(self, entryName):
        # Click on the Edit Entry button
        tmp_entry_name = (self.MY_MEDIA_ENRTY_EDIT_BUTTON[0], self.MY_MEDIA_ENRTY_EDIT_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            # If entry not found, search for 'No Entries Found' alert
            if self.wait_for_text(self.MY_MEDIA_NO_RESULTS_ALERT, 'No Entries Found', 5) == True:
                writeToLog("INFO","No Entry: '" + entryName + "' was found")
            else:
                writeToLog("INFO","FAILED search for Entry: '" + entryName + "' something went wrong")

        return True


    #  @Author: Tzachi Guetta
    def serachAndCheckSingleEntryInMyMedia(self, entryName):
        if self.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to find: '" + entryName + "'")
            return False

        # Click on the Entry's check-box in MyMedia page
        if self.checkSingleEntryInMyMedia(entryName) == False:
            return False

        return True


    #  @Author: Tzachi Guetta
    def checkSingleEntryInMyMedia(self, entryName):
        # Click on the Entry's check-box in MyMedia page
        tmp_entry_name = (self.MY_MEDIA_ENTRY_CHECKBOX[0], self.MY_MEDIA_ENTRY_CHECKBOX[1].replace('ENTRY_NAME', entryName))
        if self.click(tmp_entry_name) == False:
            # If entry not found, search for 'No Entries Found' alert
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False

        return True


    #  @Author: Tzachi Guetta
    def checkEntriesInMyMedia(self, entriesNames):
        if type(entriesNames) is list:
            for entryName in entriesNames:
                if self.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to CHECK the entry: " + entryName + ", in my media page")
                    return False

        else:
            writeToLog("INFO","FAILED, Entries list was not provided")
            return False
        return True


    #  @Author: Tzachi Guetta
    def clickActionsAndPublishFromMyMedia(self):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Action button")
            return False
        sleep(5)

        if self.click(self.MY_MEDIA_ACTIONS_BUTTON_PUBLISH_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Publish button")
            return False

        sleep(1)
        return True


    #  @Author: Tzachi Guetta
    def clickActionsAndDeleteFromMyMedia(self):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Action button")
            return False

        if self.click(self.MY_MEDIA_ACTIONS_BUTTON_DELETE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Publish button")
            return False

        sleep(1)
        return True


    #  @Author: Tzachi Guetta
    def clickActionsAndAddToPlaylistFromMyMedia(self):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Action button")
            return False

        if self.click(self.MY_MEDIA_ACTIONS_BUTTON_ADDTOPLAYLIST_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Publish button")
            return False

        sleep(1)
        return True


    #  @Author: Tzachi Guetta
    def publishSingleEntryPrivacyToUnlistedInMyMedia(self, entryName):
        if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False

        if self.clickActionsAndPublishFromMyMedia() == False:
            writeToLog("INFO","FAILED to click on Action button, Entry: '" + entryName + "' something went wrong")
            return False
        
        sleep(3)
        if self.click(self.MY_MEDIA_PUBLISH_UNLISTED, 30, multipleElements=True) == False:
            writeToLog("INFO","FAILED to click on Unlisted button")
            return False

        if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on Unlisted button")
            return False
        sleep(1)
        self.clsCommon.general.waitForLoaderToDisappear()

        if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG, 20) == False:
            writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
            return False

        writeToLog("INFO","Success, Entry '" + entryName + "' was set to unlisted successfully")
        return True


    #  @Author: Tzachi Guetta
    def handleDisclaimerBeforePublish(self, entryName):
        if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
            return False

        if self.clickActionsAndPublishFromMyMedia() == False:
            writeToLog("INFO","FAILED to click on Action button, Entry: '" + entryName + "' something went wrong")
            return False

        if self.wait_visible(self.MY_MEDIA_DISCLAIMER_MSG) == False:
            writeToLog("INFO","FAILED, Disclaimer alert (before publish) wasn't presented although Disclaimer module is turned on")
            return False

        if self.clsCommon.editEntryPage.navigateToEditEntryPageFromMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to navigate to Edit entry page, Entry: '" + entryName + "' something went wrong")
            return False

        if self.click(self.clsCommon.upload.UPLOAD_ENTRY_DISCLAIMER_CHECKBOX) == False:
            writeToLog("INFO","FAILED to click on disclaimer check-box")
            return False

        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SAVE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on save button at edit entry page")
            return False

        self.clsCommon.general.waitForLoaderToDisappear()

        if self.navigateToMyMedia() == False:
            writeToLog("INFO","FAILED to navigate to my media")
            return False

        return True


    # Author: Michal Zomper
    # publishFrom - enums.Location
    # in categoryList / channelList will have all the names of the categories / channels to publish to
    def publishSingleEntry(self, entryName, categoryList, channelList, galleryList='',  publishFrom=enums.Location.MY_MEDIA, disclaimer=False):
        #checking if disclaimer is turned on for "Before publish"
        if disclaimer == True:
            if self.handleDisclaimerBeforePublish(entryName) == False:
                writeToLog("INFO","FAILED, Handle disclaimer before Publish failed")
                return False

        if publishFrom == enums.Location.MY_MEDIA:
            if self.navigateToMyMedia() == False:
                writeToLog("INFO","FAILED to navigate to my media")
                return False

            sleep(1)
            if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to check entry '" + entryName + "' check box")
                return False

            if self.clickActionsAndPublishFromMyMedia() == False:
                writeToLog("INFO","FAILED to click on action button")
                return False
            sleep(5)

            if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 30) == False:
                writeToLog("DEBUG","FAILED to click on publish button")
                return False

        elif publishFrom == enums.Location.ENTRY_PAGE:
            sleep(1)
            # Click on publish button
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
                self.click((self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName)))
                self.get_body_element().send_keys(Keys.PAGE_DOWN)

            # Click on action tab
            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, 30) == False:
                writeToLog("INFO","FAILED to click on action button in entry page '" + entryName + "'")
                return False

            if self.click(self.clsCommon.entryPage.ENTRY_PAGE_PUBLISH_BUTTON, 30) == False:
                writeToLog("INFO","FAILED to click on publish button in entry page '" + entryName + "'")
                return False
            
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
                self.click((self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName)))
                self.get_body_element().send_keys(Keys.PAGE_DOWN)
                
            sleep(5)
            if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 45, multipleElements=True) == False:
                writeToLog("DEBUG","FAILED to click on publish button")
                return False

        elif publishFrom == enums.Location.UPLOAD_PAGE:
            writeToLog("INFO","Publishing from Upload page, Entry name: '" + entryName + "'")
            sleep(2)
            # When the radio is disabled, it still clickable, self.click() wont return false
            # The solution is to check button attribute "disabled" == "disabled"
            if self.wait_visible(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 45).get_attribute("disabled") == 'true':
                writeToLog("DEBUG","FAILED to click on publish button - button is disabled")
                return False

            if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 45) == False:
                writeToLog("DEBUG","FAILED to click on publish button")
                return False


        sleep(2)
        # Click if category list is empty
        if type(categoryList) is list:
            # Click on Publish in Category
            if self.click(self.MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION, 30) == False:
                writeToLog("INFO","FAILED to click on Publish in Category")
                return False

            # choose all the  categories to publish to
            for category in categoryList:
                tmpCategoryName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', category))

                if self.click(tmpCategoryName, 30) == False:
                    writeToLog("INFO","FAILED to select published category '" + category + "'")
                    return False
                
        elif categoryList != '':
            # Click on Publish in Category
            if self.click(self.MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION, 30) == False:
                writeToLog("INFO","FAILED to click on Publish in Category")
                return False

            tmpCategoryName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', categoryList))
            if self.click(tmpCategoryName, 30, True) == False:
                writeToLog("INFO","FAILED to select published category '" + categoryList + "'")
                return False

        sleep(2)
        # Click if channel list is empty
        if len(channelList) != 0 or len(galleryList) != 0:
            if len(galleryList) != 0:
                channelList = galleryList
            # Click on Publish in Channel
            if self.click(self.MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION, 30) == False:
                writeToLog("INFO","FAILED to click on Publish in channel")
                return False
            sleep(2)
            
            if type(channelList) is list:
                # choose all the  channels to publish to
                for channel in channelList:
                    tmpChannelName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', channel))
    
                    if self.click(tmpChannelName, 20, multipleElements=True) == False:
                        writeToLog("INFO","FAILED to select published channel '" + channel + "'")
                        return False
                    
            elif channelList != '':
                tmpChannelName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', channelList))

                if self.click(tmpChannelName, 20, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to select published channel '" + channel + "'")
                    return False

        sleep(1)
        if publishFrom == enums.Location.MY_MEDIA or publishFrom == enums.Location.ENTRY_PAGE:
            if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON, 30) == False:
                writeToLog("INFO","FAILED to click on save button")
                return False
            
            # Wait for loader to disappear
            self.clsCommon.general.waitForLoaderToDisappear()            

            if self.wait_visible(self.MY_MEDIA_SAVE_MESSAGE_CONFIRM, 45) == False:
                writeToLog("INFO","FAILED to find confirm save message")
                return False
        else:
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD:
                self.click(self.clsCommon.upload.UPLOAD_PAGE_TITLE)
                self.get_body_element().send_keys(Keys.PAGE_DOWN)

            if self.click(self.clsCommon.upload.UPLOAD_ENTRY_SAVE_BUTTON, multipleElements=True) == False:
                writeToLog("DEBUG","FAILED to click on 'Save' button")
                return None
            sleep(2)

            # Wait for loader to disappear
            self.clsCommon.general.waitForLoaderToDisappear()

        sleep(3)
        writeToLog("INFO","Success, publish entry '" + entryName + "' was successful")
        return True


    # Author: Tzachi Guetta
    def verifyEntryPrivacyInMyMedia(self, entryName, expectedEntryPrivacy, forceNavigate=True):
        try:
            if forceNavigate == True:
                if self.navigateToMyMedia() == False:
                    writeToLog("INFO","FAILED to navigate to  my media")
                    return False

            if expectedEntryPrivacy == enums.EntryPrivacyType.UNLISTED:

                parent = self.wait_visible(self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName))
                child = self.replaceInLocator(self.MY_MEDIA_ENTRY_CHILD, "ENTRY_PRIVACY", 'Unlisted')
                if self.clsCommon.base.get_child_element(parent, child) != None:
                    writeToLog("INFO","As Expected: The privacy of: '" + entryName + "' in My-media page is: '" + str(enums.EntryPrivacyType.UNLISTED) + "'")
                    return True

            elif expectedEntryPrivacy == enums.EntryPrivacyType.PRIVATE:

                parent = self.wait_visible(self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName))
                child = self.replaceInLocator(self.MY_MEDIA_ENTRY_CHILD, "ENTRY_PRIVACY", 'Private')
                if self.clsCommon.base.get_child_element(parent, child) != None:
                    writeToLog("INFO","As Expected: The privacy of: '" + entryName + "' in My-media page is: '" + str(enums.EntryPrivacyType.PRIVATE) + "'")
                    return True

            elif expectedEntryPrivacy == enums.EntryPrivacyType.REJECTED or expectedEntryPrivacy == enums.EntryPrivacyType.PENDING or expectedEntryPrivacy == enums.EntryPrivacyType.PUBLISHED:

                tmpEntry = self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName)
                entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
                tmpBtn = (self.MY_MEDIA_ENTRY_PUBLISHED_BTN[0], self.MY_MEDIA_ENTRY_PUBLISHED_BTN[1].replace('ENTRY_ID', entryId))
                
                if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
                    self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN,5)
                    sleep(1)
                    
                if self.click(tmpBtn) == False:
                    writeToLog("INFO","FAILED to click on the 'published' pop-up of: " + entryName)
                    return False
                sleep(3)

                tmpBtn = (self.MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI[0], self.MY_MEDIA_ENTRY_PUBLISHED_BTN_OLD_UI[1].replace('ENTRY_ID', entryId) + "/descendant::strong[@class='valign-top']")
                if str(expectedEntryPrivacy) in self.get_element_text(tmpBtn):
                    writeToLog("INFO","As Expected: The privacy of: '" + entryName + "' in My-media page is: '" + str(expectedEntryPrivacy) + "'")
                    return True

        except NoSuchElementException:
            writeToLog("INFO","FAILED to verify that entry '" + entryName + "' label is " + expectedEntryPrivacy.value)
            return False


    # Author: Michal Zomper
    def verifyEntriesPrivacyInMyMedia(self, entriesList):
        for entry in entriesList:
            sleep(1)
            if self.verifyEntryPrivacyInMyMedia(entry, entriesList[entry], forceNavigate=False) == False:
                writeToLog("INFO","FAILED to verify entry '" + entry + "' label")
                return False

        writeToLog("INFO","Success, All entries label were verified")
        return True


    # Author: Tzachi Guetta
    def SortAndFilter(self, dropDownListName='' ,dropDownListItem='', year=None, month=None, day='', text=''):
        if self.clsCommon.isElasticSearchOnPage() == True:
            if dropDownListName == enums.SortAndFilter.SORT_BY:
                tmpSortlocator = self.MY_MEDIA_SORT_BY_DROPDOWNLIST_NEW_UI
                if self.click(tmpSortlocator, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on :" + dropDownListItem.value + " filter in my media")
                    return False

                # only sort filter use the locater of the dropdownlist_item_old_ui
                tmpSortBy = (self.MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI[0], self.MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI[1].replace('DROPDOWNLIST_ITEM', dropDownListItem.value))
                if self.click(tmpSortBy, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on sort by  :" + dropDownListItem.value + " filter in my media")
                    return False
            else:
                if self.wait_element(self.MY_MEDIA_FILTERS_BUTTON_NEW_UI_ACTIVE, timeout=1, multipleElements=True) == False:
                    if self.click(self.MY_MEDIA_FILTERS_BUTTON_NEW_UI, 20, multipleElements=True) == False:
                        writeToLog("INFO","FAILED to click on filters button in my media")
                        return False
                sleep(3)

                if dropDownListName == enums.SortAndFilter.DURATION or dropDownListName == enums.SortAndFilter.CAPTIONS or dropDownListName == enums.SortAndFilter.SINGLE_LIST:
                    tmpLocator = (self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace('DROPDOWNLIST_ITEM', dropDownListItem.value))
                    if self.is_visible(tmpLocator, multipleElements=True) != True:
                        if self.click(self.FILTER_NEXT_ARROW, multipleElements=True) != False:
                            if self.wait_element(self.FILTER_PREVIOUS_ARROW, 2, multipleElements=True) == False:
                                writeToLog("INFO", "Failed to properly displayed the second filter page")
                                return False
                            if self.click(tmpLocator, multipleElements=True) == False:
                                writeToLog("INFO","FAILED to click on the drop-down list item: " + dropDownListItem.value)
                                return False
                    else:
                        if self.click(tmpLocator, multipleElements=True) == False:
                            writeToLog("INFO","FAILED to click on the drop-down list item: " + dropDownListItem.value)
                            return False

                elif dropDownListName == enums.SortAndFilter.SINGLE_DATE:
                    if self.is_visible(self.FILTER_SINGLE_DATE_CALENDAR, multipleElements=True) != True:
                        if self.click(self.FILTER_NEXT_ARROW, multipleElements=True) != False:
                            if self.filterSelectDate(year, month, day) == False:
                                writeToLog("INFO", "Failed to select a specific single date")
                                return False
                    else:
                        if self.filterSelectDate(year, month, day) == False:
                            writeToLog("INFO", "Failed to select a specific single date")
                            return False

                elif dropDownListName == enums.SortAndFilter.FREE_TEXT:
                    tmpLocator = (self.FILTER_SELECT_FIELD_TEXT[0], self.FILTER_SELECT_FIELD_TEXT[1].replace('DROPDOWNLIST_ITEM', dropDownListItem.value))
                    tmpCategory = (self.FILTER_SELECT_FIELD_CATEGORY[0], self.FILTER_SELECT_FIELD_CATEGORY[1].replace('DROPDOWNLIST_NAME', dropDownListName.value))
                    if self.is_visible(tmpLocator, multipleElements=True) != True:
                        if self.click(self.FILTER_NEXT_ARROW, multipleElements=True) != False:
                            if self.click(tmpLocator, multipleElements=True) == False:
                                writeToLog("INFO", "Failed to click on the " + dropDownListItem.value)
                                return False
                            sleep(1)
                            action = ActionChains(self.driver)
                            try:
                                action.send_keys(text).perform()
                            except Exception:
                                writeToLog("INFO", "FAILED to insert a text into the " + dropDownListItem.value + " field")
                                return False

                            if self.click(tmpCategory, 2, multipleElements=True) == False:
                                writeToLog("INFO", "Failed to deactivate the active status for " + dropDownListItem.value)
                                return False
                    else:
                        if self.click(tmpLocator, multipleElements=True) == False:
                            writeToLog("INFO", "Failed to click on the locator")
                            return False
                        sleep(1)
                        action = ActionChains(self.driver)
                        try:
                            action.send_keys(text).perform()
                        except Exception:
                            writeToLog("INFO", "FAILED to insert a text into the " + dropDownListItem.value + " field")
                            return False

                        if self.click(tmpCategory, 2, multipleElements=True) == False:
                            writeToLog("INFO", "Failed to deactivate the active status for the " + dropDownListItem.value)
                            return False

                else:
                    if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
                        self.switch_to_default_content()
                        self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
                        self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN,3) 
                        self.clsCommon.sharePoint.switchToSharepointIframe() 
                        
                    tmpEntry = (self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace('DROPDOWNLIST_ITEM', dropDownListItem.value))
                    if self.click(tmpEntry, multipleElements=True) == False:
                        writeToLog("INFO","FAILED to click on the drop-down list item: " + dropDownListItem.value)
                        return False

        else:
            if dropDownListName == enums.SortAndFilter.SORT_BY:
                tmplocator = self.MY_MEDIA_SORT_BY_DROPDOWNLIST_OLD_UI

            elif dropDownListName == enums.SortAndFilter.PRIVACY:
                tmplocator = self.MY_MEDIA_FILTER_BY_STATUS_DROPDOWNLIST

            elif dropDownListName == enums.SortAndFilter.MEDIA_TYPE:
                tmplocator = self.MY_MEDIA_FILTER_BY_TYPE_DROPDOWNLIST

            elif dropDownListName == enums.SortAndFilter.COLLABORATION:
                tmplocator = self.MY_MEDIA_FILTER_BY_COLLABORATION_DROPDOWNLIST

            elif dropDownListName == enums.SortAndFilter.SCHEDULING:
                tmplocator = self.MY_MEDIA_FILTER_BY_SCHEDULING_DROPDOWNLIST

            else:
                writeToLog("INFO","FAILED, drop-down-list name was not provided")
                return False

            if self.click(tmplocator, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on: " + dropDownListName.value + " in my media")
                return False

            tmpEntry = self.replaceInLocator(self.MY_MEDIA_DROPDOWNLIST_ITEM_OLD_UI, "DROPDOWNLIST_ITEM", dropDownListItem.value)
            if self.click(tmpEntry, multipleElements=True) == False:
                writeToLog("INFO","FAILED to click on the drop-down list item: " + dropDownListItem.value)
                return False


        self.clsCommon.general.waitForLoaderToDisappear()
        # If there is any problem regarding the next block, please talk to Oleg or Inbar
        if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
            if self.showAllEntries(searchIn = enums.Location.MY_MEDIA, timeOut=60) == False:
                writeToLog("INFO","FAILED to show all entries")
                return False

        writeToLog("INFO","Success, sort/filter by '" + dropDownListName.value + " - " + dropDownListItem.value + "' was set successfully")
        return True


        # Author: Tzachi Guetta
    def sortAndFilterInMyMedia(self, sortBy='', filterPrivacy='', filterMediaType='', filterCollaboration='', filterScheduling='', resetFields=False):
        try:
            if self.navigateToMyMedia(forceNavigate = resetFields) == False:
                writeToLog("INFO","FAILED to navigate to  my media")
                return False

            if sortBy != '':
                if self.SortAndFilter(enums.SortAndFilter.SORT_BY, sortBy) == False:
                    writeToLog("INFO","FAILED to set sortBy: " + str(sortBy) + " in my media")
                    return False

            if filterPrivacy != '':
                if self.SortAndFilter(enums.SortAndFilter.PRIVACY, filterPrivacy) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterPrivacy) + " in my media")
                    return False

            if filterMediaType != '':
                if self.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, filterMediaType) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterMediaType) + " in my media")
                    return False

            if filterCollaboration != '':
                if self.SortAndFilter(enums.SortAndFilter.COLLABORATION, filterCollaboration) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterCollaboration) + " in my media")
                    return False

            if filterScheduling != '':
                if self.SortAndFilter(enums.SortAndFilter.SCHEDULING, filterScheduling) == False:
                    writeToLog("INFO","FAILED to set filter: " + str(filterScheduling) + " in my media")
                    return False

        except NoSuchElementException:
            return False

        return True


    # Author: Tzachi Guetta
    # MUST: enableLoadButton must be turned off in KMS admin
    def scrollToBottom(self, retries=5):
        try:
            if len(self.get_elements(self.MY_MEDIA_TABLE_SIZE)) < 4:
                return True
            else:
                count = 0
                while count < retries:
                    self.driver.find_element_by_xpath('//body').send_keys(Keys.END)
                    writeToLog("INFO","Scrolling to bottom, retry #: " + str(count+1))
                    sleep(2)
                    if self.wait_visible(self.MY_MEDIA_END_OF_PAGE, 1) != False:
                        writeToLog("INFO","*** Reached the End of page ***")
                        return True
                    count += 1

                writeToLog("INFO","FAILED, scrolled " + str(retries) + " times and didn't reached the bottom of the page, maybe you need add more retries")

        except NoSuchElementException:
            return False

        return False

        # Author: Tzachi Guetta
    def getTop(self, entryName, location=enums.Location.MY_MEDIA):
        try:
            if location == enums.Location.MY_MEDIA:
                tmpEntry = self.replaceInLocator(self.clsCommon.myMedia.MY_MEDIA_ENTRY_TOP, "ENTRY_NAME", entryName)

            elif location == enums.Location.MY_PLAYLISTS or location == enums.Location.PENDING_TAB:
                tmpEntry = self.replaceInLocator(self.clsCommon.myPlaylists.PLAYLIST_ENTRY_NAME_IN_PLAYLIST, "ENTRY_NAME", entryName)
            
            elif location == enums.Location.CHANNEL_PLAYLIST:
                tmpEntry = self.replaceInLocator(self.clsCommon.channel.CHANNEL_PLAYLIST_ENTRY_NAME, "ENTRY_NAME", entryName)
                 
            entrytop = self.get_element_attributes(tmpEntry, multipleElements=True)['top']
            writeToLog("INFO","The top of: '" + entryName + "' is: " + str(entrytop))
            return entrytop

        except NoSuchElementException:
            writeToLog("INFO","The top of: '" + entryName + "' could not be located")
            return False


    # Author: Tzachi Guetta
    def verifyEntriesOrder(self, expectedEntriesOrder, location = enums.Location.MY_MEDIA):
        try:
            if location == enums.Location.MY_MEDIA:
                if self.clsCommon.myMedia.navigateToMyMedia() == False:
                    return False

                if self.scrollToBottom() == False:
                    writeToLog("INFO","FAILED to scroll to bottom in my-media")
                    return False

            elif location == enums.Location.MY_PLAYLISTS:
                if self.clsCommon.myPlaylists.navigateToMyPlaylists(True) == False:
                    return False

            tmpTop = -9999
            for entry in expectedEntriesOrder:
                currentEntryTop = self.getTop(entry, location)
                if currentEntryTop != False and currentEntryTop!= 0:
                    if currentEntryTop <= tmpTop:
                        writeToLog("INFO","FAILED, the location of: '" + entry + "' is not as expected. (the top is '" + str(currentEntryTop) + "' and it should be higher than: '" + str(tmpTop) + "')")
                        return False
                else:
                    return False
                tmpTop = currentEntryTop

        except NoSuchElementException:
            return False

        return True


    # Author: Tzachi Guetta
    def isEntryPresented(self, entryName, isExpected):
        try:
            tmpEntry = self.replaceInLocator(self.MY_MEDIA_ENTRY_TOP, "ENTRY_NAME", entryName)
            isPresented = self.is_present(tmpEntry, 5)

            strPresented = "Not Presented"
            if isPresented == True:
                strPresented = "Presented"

            if isPresented == isExpected:
                writeToLog("INFO","Passed, As expected, Entry: '" + entryName + "' is " + strPresented)
                return True
            else:
                writeToLog("INFO","FAILED, Not expected, Entry: '" + entryName + "' is " + strPresented)
                return False

        except NoSuchElementException:
            return False

        return True

    # Author: Tzachi Guetta
    def areEntriesPresented(self, entriesDict):
        try:
            for entry in entriesDict:
                if self.isEntryPresented(entry, entriesDict.get(entry)) == False:
                    writeToLog("INFO","FAILED to verify if entry presented for entry: " + str(entry))
                    return False

        except NoSuchElementException:
            return False

        return True

    # @Author: Inbar Willman
    def publishSingleEntryToUnlistedOrPrivate(self, entryName, privacy, alreadyPublished=False, publishFrom=enums.Location.MY_MEDIA):
        if publishFrom == enums.Location.MY_MEDIA:
            if self.serachAndCheckSingleEntryInMyMedia(entryName) == False:
                writeToLog("INFO","FAILED to Check for Entry: '" + entryName + "' something went wrong")
                return False

            if self.clickActionsAndPublishFromMyMedia() == False:
                writeToLog("INFO","FAILED to click on Action button, Entry: '" + entryName + "' something went wrong")
                return False
            sleep(7)

            if privacy == enums.ChannelPrivacyType.UNLISTED:
                    if self.wait_visible(self.MY_MEDIA_PUBLISH_UNLISTED, 60, True) == False:
                        writeToLog("INFO", "FAILED to display the Media Publish Unlisted button")
                        return False
                    
                    if self.click(self.MY_MEDIA_PUBLISH_UNLISTED) == False:
                        writeToLog("INFO","FAILED to click on Unlisted button")
                        return False

                    if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON) == False:
                        writeToLog("INFO","FAILED to click on Unlisted button")
                        return False

                    if alreadyPublished == True:
                        #Click on confirm modal
                        if self.click(self.MY_MEDIA_CONFIRM_CHANGING_STATUS) == False:
                            writeToLog("INFO","FAILED to click on confirm button")
                            return False

                    sleep(1)
                    self.clsCommon.general.waitForLoaderToDisappear()

                    if self.wait_element(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG, 20) == False:
                        writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
                        return False

            elif privacy == enums.ChannelPrivacyType.PRIVATE:                
                    if self.wait_visible(self.MY_MEDIA_PUBLISH_PRIVATE, 60, True) == False:
                        writeToLog("INFO", "FAILED to display the Media Publish Private button")
                        return False
                    
                    if self.click(self.MY_MEDIA_PUBLISH_PRIVATE) == False:
                        writeToLog("INFO","FAILED to click on Private button")
                        return False

                    if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON) == False:
                        writeToLog("INFO","FAILED to click on Private button")
                        return False

                    if alreadyPublished == True:
                        #Click on confirm modal
                        if self.click(self.MY_MEDIA_CONFIRM_CHANGING_STATUS) == False:
                            writeToLog("INFO","FAILED to click on confirm button")
                            return False

                    sleep(1)
                    self.clsCommon.general.waitForLoaderToDisappear()

                    if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_PRIVATE_MSG, 20) == False:
                        writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
                        return False

            else:
                writeToLog("INFO","FAILED to get valid privacy:" + str(privacy))
                return False

        elif publishFrom == enums.Location.UPLOAD_PAGE:
            writeToLog("INFO","Publishing from Upload page, Entry name: '" + entryName + "'")
            sleep(2)
            if self.click(self.MY_MEDIA_PUBLISH_UNLISTED) == False:
                writeToLog("INFO","FAILED to click on Unlisted button")
                return False

            if self.click(self.clsCommon.upload.UPLOAD_ENTRY_SAVE_BUTTON) == False:
                writeToLog("DEBUG","FAILED to click on 'Save' button")
                return None

            sleep(2)
            # Wait for loader to disappear
            self.clsCommon.general.waitForLoaderToDisappear()

            if self.wait_visible(self.clsCommon.myMedia.MY_MEDIA_PUBLISHED_AS_UNLISTED_MSG, 20) == False:
                writeToLog("INFO","FAILED to Publish Entry: '" + entryName + "' something went wrong")
                return False

        return True

    # @Author: Michal Zomper
    def navigateToEntryPageFromMyMediaViaThubnail(self, entryName):
        tmp_entry_name = (self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[0], self.clsCommon.entryPage.ENTRY_PAGE_ENTRY_TITLE[1].replace('ENTRY_NAME', entryName))
        #Check if we already in edit entry page
        if self.wait_visible(tmp_entry_name, 5) != False:
            writeToLog("INFO","Already in edit entry page, Entry name: '" + entryName + "'")
            return True

        if self.clsCommon.myMedia.searchEntryMyMedia(entryName) == False:
            writeToLog("INFO","FAILD to search entry name: '" + entryName + "' in my media")
            return False

        if self.clsCommon.isElasticSearchOnPage() == False:
            tmp_entryThumbnail = (self.MY_MEDIA_ENTRY_THUMBNAIL[0], self.MY_MEDIA_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName))
            if self.click(tmp_entryThumbnail, 20) == False:
                writeToLog("INFO","FAILED to click on entry thumbnail: " + entryName)
                return False
        else:
            if self.click(self.MY_MEDIA_ENTRY_THUMBNAIL_ELASTIC_SEARCH, 20) == False:
                writeToLog("INFO","FAILED to click on entry thumbnail: " + entryName)
                return False

        if self.wait_visible(tmp_entry_name, 30) == False:
            writeToLog("INFO","FAILED to enter entry page: '" + entryName + "' via my media page thumbnail")
            return False

        sleep(2)
        writeToLog("INFO","Success, entry was open successfully")
        return True


    # @Author: Michal Zomper
    def verifyEntriesExistInMyMedia(self, searchKey, entriesList, entriesCount):
        if self.searchEntryMyMedia(searchKey) == False:
            writeToLog("INFO","FAILED to search entry: '" + searchKey + "' in my media")
            return False

        try:
            searchedEntries = self.get_elements(self.MY_MEDIA_TABLE_SIZE)
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list")
            return False

        # Check that number of entries that display is correct
        if len(searchedEntries) != entriesCount:
            writeToLog("INFO","FAILED, number of entries after search is '" + str(len(self.get_elements(self.MY_MEDIA_TABLE_SIZE))) + "' but need to be '" + str(entriesCount) + "'")
            return False

        if self.clsCommon.isElasticSearchOnPage() == False:
            if type(entriesList) is list:
                i=1
                for entry in entriesList:
                    if (entry in searchedEntries[len(searchedEntries)-i].text) == False:
                        writeToLog("INFO","FAILED to find entry: '" + entry + "'  after search in my media")
                        return False
                    i = i+1
            # only one entry
            else:
                if (entriesList in searchedEntries[0].text) == False:
                    writeToLog("INFO","FAILED to find entry: '" + entriesList + "' after search in my media")
                    return False
        else:
            if type(entriesList) is list:
                for entry in entriesList:
                    if (self.getResultAfterSearch(entry)) == False:
                        writeToLog("INFO","FAILED to find entry: '" + entry + "'  after search in my media")
                        return False
            # only one entry
            else:
                if (self.getResultAfterSearch(entriesList)) == False:
                    writeToLog("INFO","FAILED to find entry: '" + entriesList + "' after search in my media")
                    return False

        if self.clearSearch() == False:
            writeToLog("INFO","FAILED to clear search textbox")
            return False

        sleep(1)
        writeToLog("INFO","Success, All searched entries were found after search")
        return True




    # Author: Michal Zomper
    def clearSearch(self):
        if self.clsCommon.isElasticSearchOnPage() == True:
            try:
                clear_button = self.get_elements(self.MY_MEDIA_REMOVE_SEARCH_ICON_NEW_UI)
            except NoSuchElementException:
                writeToLog("INFO","FAILED to find clear search icon")
                return False
            
            if localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST != enums.Application.MEDIA_SPACE:
                if self.clickElement(clear_button[0]) == False:
                    writeToLog("INFO","FAILED click on the remove search icon")
                    return False
            else:
                if self.clickElement(clear_button[1]) == False:
                    writeToLog("INFO","FAILED click on the remove search icon")
                    return False
        else:
            if self.click(self.MY_MEDIA_REMOVE_SEARCH_ICON_OLD_UI, 15, multipleElements=True) == False:
                writeToLog("INFO","FAILED click on the remove search icon")
                return False
        self.clsCommon.general.waitForLoaderToDisappear()

        writeToLog("INFO","Success, search was clear from search textbox")
        return True


    #  @Author: Michal Zomper
    # The following method can handle list of entries and a single entry:
    #    in order to publish list of entries pass a List[] of entries name, for single entry - just pass the entry name
    #    also: the method will navigate to My media
    #    in categoryList / channelList will have all the names of the categories / channels to publish to
    # Known limitation: entries MUST be presented on the first page of my media
    def publishEntriesFromMyMedia(self, entriesName, categoryList='', channelList='', galleryList='',  disclaimer=False, showAllEntries=False):
        if self.navigateToMyMedia(forceNavigate = True) == False:
            writeToLog("INFO","FAILED Navigate to my media page")
            return False

        if showAllEntries == True:
            if self.showAllEntries() == False:
                return False

        # Checking if entriesNames list type
        if type(entriesName) is list:
            if disclaimer == True:
                for entryName in entriesName:
                    sleep(2)
                    if self.handleDisclaimerBeforePublish(entryName) == False:
                        writeToLog("INFO","FAILED, Handle disclaimer before Publish failed for entry:" + entryName)
                        return False

            for entryName in entriesName:
                if self.checkSingleEntryInMyMedia(entryName) == False:
                    writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                    return False
        else:
            if disclaimer == True:
                if self.handleDisclaimerBeforePublish(entriesName) == False:
                    writeToLog("INFO","FAILED, Handle disclaimer before Publish failed")
                    return False

            if self.checkSingleEntryInMyMedia(entriesName) == False:
                writeToLog("INFO","FAILED to CHECK the entry in my-media page")
                return False

        if self.clickActionsAndPublishFromMyMedia() == False:
            writeToLog("INFO","FAILED to click on action button")
            return False

        sleep(10)

        if self.click(self.MY_MEDIA_PUBLISHED_RADIO_BUTTON, 40, True) == False:
            writeToLog("INFO","FAILED to click on publish button")
            return False

        sleep(2)
        # Click if category list is empty
        if len(categoryList) != 0:
            # Click on Publish in Category
            if self.click(self.MY_MEIDA_PUBLISH_TO_CATEGORY_OPTION, 30) == False:
                writeToLog("INFO","FAILED to click on Publish in Category")
                return False

            # choose all the  categories to publish to
            for category in categoryList:
                tmoCategoryName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', category))

                if self.click(tmoCategoryName, 30) == False:
                    writeToLog("INFO","FAILED to select published category '" + category + "'")
                    return False

        sleep(2)
        # Click if channel list is empty
        if len(channelList) != 0 or len(galleryList) != 0:
            if len(galleryList) != 0:
                channelList = galleryList
            # Click on Publish in Channel
            if self.click(self.MY_MEIDA_PUBLISH_TO_CHANNEL_OPTION, 30) == False:
                writeToLog("INFO","FAILED to click on Publish in channel")
                return False
            sleep(2)

            # choose all the  channels to publish to
            for channel in channelList:
                tmpChannelName = (self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[0], self.MY_MEDIA_CHOSEN_CATEGORY_TO_PUBLISH[1].replace('PUBLISHED_CATEGORY', channel))

                if self.click(tmpChannelName, 20, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to select published channel '" + channel + "'")
                    return False

        sleep(1)
        if self.click(self.MY_MEDIA_PUBLISH_SAVE_BUTTON, 30) == False:
            writeToLog("INFO","FAILED to click on save button")
            return False

        if self.wait_visible(self.MY_MEDIA_SAVE_MESSAGE_CONFIRM, 45) == False:
            writeToLog("INFO","FAILED to find confirm save message")
            return False

        sleep(3)
        if type(entriesName) is list:
            entries = ", ".join(entriesName)
            writeToLog("INFO","Success, The entries '" + entries + "' were published successfully")
        else:
            writeToLog("INFO","Success, The entry '" + entriesName + "' was publish  successfully")
        return True


    #  @Author: Oded berihon
    def addCustomDataAndPublish(self, customfield, customFieldDropdwon=enums.DepartmentDivision.FINANCE):
        if self.click(self.EDIT_BUTTON_REQUIRED_FIELD_MASSAGE) == False:
            writeToLog("INFO","FAILED to click on edit button")
            return False

        if self.send_keys(self.CUSTOM_FIELD, customfield) == False:
            writeToLog("INFO","FAILED to fill a customfield:'" + customfield + "'")
            return False

        if customFieldDropdwon == enums.DepartmentDivision.FINANCE:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'FInance') == False:
                writeToLog("INFO","Failed select finance devision")
                return False

        elif customFieldDropdwon == enums.DepartmentDivision.MARKETING:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Marketing') == False:
                writeToLog("INFO","Failed select finance devision")
                return False

        elif customFieldDropdwon == enums.DepartmentDivision.PRODUCT:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Product') == False:
                writeToLog("INFO","Failed select finance devision")
                return False

        elif customFieldDropdwon == enums.DepartmentDivision.ENGINEERING:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Engineering') == False:
                writeToLog("INFO","Failed select finance devision")
                return False

        elif customFieldDropdwon == enums.DepartmentDivision.SALES:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Sales') == False:
                writeToLog("INFO","Failed select finance devision")
                return False

        elif customFieldDropdwon == enums.DepartmentDivision.HR:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'HR') == False:
                writeToLog("INFO","Failed select finance devision")
                return False

        elif customFieldDropdwon == enums.DepartmentDivision.MANAGMENT:
            if self.select_from_combo_by_text(self.CUSTOM_FIELD_DROP_DOWN, 'Management') == False:
                writeToLog("INFO","Failed select finance devision")
                return False

        parentElement = self.wait_visible(self.CLICK_ON_CALENDAR_DATE_ESTABLISHED)
        self.get_child_element(parentElement, self.CLICK_ON_CALENDAR).click()

        if self.click(self.EDIT_ENTRY_CUSTOM_DATA_CALENDAR_DAY) == False:
            writeToLog("INFO","Failed select finance devision")
            return False

        if self.click(self.clsCommon.editEntryPage.EDIT_ENTRY_SAVE_BUTTON, 15) == False:
            writeToLog("INFO","FAILED to click on Edit button")
            return False

        return True


    #  @Author: Michal Zomper
    # The function check and verify that the entries sort in my media are in the correct order
    def verifySortInMyMedia(self, sortBy, entriesList):
        if self.SortAndFilter(enums.SortAndFilter.SORT_BY, sortBy) == False:
            writeToLog("INFO","FAILED to sort entries")
            return False

        if self.showAllEntries() == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False
        sleep(10)

        try:
            entriesInMyMedia = self.wait_visible(self.MY_MEDIA_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False
#        entriesInMyMedia = entriesInMyMedia.split("\n")
        entriesInMyMedia = entriesInMyMedia.split("\n")
        # run over the list and delete tab before the entry name
        for idx, entry in enumerate(entriesInMyMedia):
            entriesInMyMedia[idx] = entry.lstrip()

        if self.verifySortOrder(entriesList, entriesInMyMedia) == False:
            writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct")
            return False

        writeToLog("INFO","Success, My media sort by '" + sortBy.value + "' was successful")
        return True


    # @Author: Michal Zomper
    # The function is checking that the sort order is correct
    # entriesOrderAfterSor is the parameter of all the text in the sort page
    def verifySortOrder(self, entriesList, entriesOrderAfterSort):
        prevEntryIndex = -1

        if self.clsCommon.isElasticSearchOnPage() == True:
            for entry in entriesList:
                try:
                    currentEntryIndex = entriesOrderAfterSort.index(entry.lower())
                except:
                    writeToLog("INFO","FAILED , entry '" + entry + "' was not found" )
                    return False

                #if prevEntryIndex > currentEntryIndex:
                if (prevEntryIndex < currentEntryIndex) == False:
                    #writeToLog("INFO","FAILED ,sort by '" + sortBy + "' isn't correct. entry '" + entry + "' isn't in the right place" )
                    writeToLog("INFO","FAILED , entry '" + entry + "' isn't in the right place")
                    return False
                prevEntryIndex = currentEntryIndex
            #writeToLog("INFO","Success, My media sort by '" + sortBy + "' was successful")
            writeToLog("INFO","Success, entries sort was successful")
            return True
        else:
            for entry in entriesList:
                currentEntryIndex = entriesOrderAfterSort.index(entry.lower())
                #if prevEntryIndex > currentEntryIndex:
                if (prevEntryIndex < currentEntryIndex) == False:
                    #writeToLog("INFO","FAILED ,sort by '" + sortBy.value + "' isn't correct. entry '" + entry + "' isn't in the right place" )
                    writeToLog("INFO","FAILED , entry '" + entry + "' isn't in the right place")
                    return False
                prevEntryIndex = currentEntryIndex

            #writeToLog("INFO","Success, My media sort by '" + sortBy.value + "' was successful")
            writeToLog("INFO","Success, entries sort  was successful")
            return True


    def showAllEntries(self, searchIn = enums.Location.MY_MEDIA, timeOut=600, afterSearch=False):
        # Check if we are in My Media page
        if searchIn == enums.Location.MY_MEDIA:
            tmp_table_size = self.MY_MEDIA_TABLE_SIZE
            no_entries_page_msg = self.MY_MEDIA_NO_RESULTS_ALERT

        # Check if we are in category page
        elif searchIn == enums.Location.CATEGORY_PAGE:
            if self.clsCommon.isElasticSearchOnPage() == True:
                if afterSearch == False:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE_NEW_UI
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_ITEMS_MSG
                else:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE_AFTER_SEARCH
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_FOUND_NEW_UI_MSG
            else:#TODO OLD UI
                if afterSearch == False:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_FOUND_MSG
                else:
                    tmp_table_size = self.clsCommon.category.CATEGORY_TABLE_SIZE
                    no_entries_page_msg = self.clsCommon.category.CATEGORY_NO_MORE_MEDIA_FOUND_MSG

        elif searchIn == enums.Location.MY_HISTORY:
            tmp_table_size = self.clsCommon.myHistory.MY_HISTORY_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.myHistory.MY_HISTORY_NO_MORE_RESULTS_ALERT

        elif searchIn == enums.Location.ADD_TO_CHANNEL_MY_MEDIA:
            tmp_table_size = self.clsCommon.channel.ADD_TO_CHANNEL_MY_MEDIA_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.channel.ADD_TO_CHANNEL_MY_MEDIA_NO_MORE_MEDIA_FOUND_MSG

        elif searchIn == enums.Location.ADD_TO_CHANNEL_SR:
            tmp_table_size = self.clsCommon.channel.ADD_TO_CHANNEL_MY_MEDIA_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.channel.ADD_TO_CHANNEL_SR_NO_MORE_MEDIA_FOUND_MSG

        elif searchIn == enums.Location.EDITOR_PAGE:
            tmp_table_size = self.clsCommon.kea.EDITOR_TABLE_SIZE
            no_entries_page_msg = self.clsCommon.kea.EDITOR_NO_MORE_MEDIA_FOUND_MSG

        else:
            writeToLog("INFO","Failed to get valid location page")
            return False

        if len(self.get_elements(tmp_table_size)) < 5:
                writeToLog("INFO","Success, All media is display")
                return True

        self.clsCommon.sendKeysToBodyElement(Keys.END)
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeOut)
        while wait_until > datetime.datetime.now():
            if self.is_present(no_entries_page_msg, 2) == True or self.is_present(self.ENTRY_NO_MEDIA_FOUND_MESSAGE, 2) == True:
                writeToLog("INFO","Success, All media is display")
                sleep(1)
                # go back to the top of the page
                self.clsCommon.sendKeysToBodyElement(Keys.HOME)
                return True 
            
            if (localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACK_BOARD) or \
                (localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.CANVAS) or \
                (localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.D2L) or \
                (localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.BLACKBOARD_ULTRA) or \
                (localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.JIVE):
                    self.click(self.MY_MEDIA_TITLE, multipleElements=True)
            
            elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SAKAI:
                self.click(self.clsCommon.myMedia.MY_MEDIA_ACTIONS_BUTTON)
                

            elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.MOODLE:
                self.click(self.MY_MEDIA_ACTIONS_BUTTON)
            
            elif localSettings.LOCAL_SETTINGS_APPLICATION_UNDER_TEST == enums.Application.SHARE_POINT:
                    self.switch_to_default_content()
                    self.click(self.clsCommon.sharePoint.SP_PAGE_TITLE_IN_SP_IFRAME)
                    self.get_body_element().send_keys(Keys.PAGE_DOWN)
                    self.clsCommon.sharePoint.switchToSharepointIframe()
                    self.click(self.clsCommon.category.CATEGORY_DETAILS_VIEW)

            self.clsCommon.sendKeysToBodyElement(Keys.END)

        writeToLog("INFO","FAILED to show all media")
        return False


    #  @Author: Michal Zomper
    # The function check the the entries in my media are filter correctly
    def verifyFiltersInMyMedia(self, entriesDict, noEntriesExpected=False):
        if noEntriesExpected == True:
            if self.wait_element(self.ENTRY_NO_MEDIA_FOUND_MESSAGE, 1, multipleElements=True) != False:
                writeToLog("INFO", "PASSED, no entries are displayed")
                return True
            else:
                writeToLog("INFO", "Some entries are present, we will verify the dictionaries")
        
        if self.showAllEntries() == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False

        try:
            entriesInMyMedia = self.get_element(self.MY_MEDIA_TABLE).text.lower()
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get entries list in galley")
            return False

        for entry in entriesDict:
            #if entry[1] == True:
            if entriesDict[entry] == True:
                #if entry[0].lower() in entriesInMyMedia == False:
                if (entry.lower() in entriesInMyMedia) == False:
                    writeToLog("INFO","FAILED, entry '" + entry + "' wasn't found in my media although he need to be found")
                    return False

            #elif entry[1] == False:
            if entriesDict[entry] == False:
                # if entry[0].lower() in entriesInMyMedia == True:
                if (entry.lower() in entriesInMyMedia) == True:
                    writeToLog("INFO","FAILED, entry '" + entry + "' was found in my media although he doesn't need to be found")
                    return False

        writeToLog("INFO","Success, Only the correct media display in my media")
        return True
   
    
    #@Author: Michal Zomper
    # The function going over the entries list and check that the entries icon that display on the thumbnail are  match the 'entryType' parameter    
    def verifyEntryTypeIcon(self, entriesList, entryType, location=enums.Location.CHANNEL_PAGE):
        for entry in entriesList:
            
            if location == enums.Location.PENDING_TAB:
                tmpEntry = (self.CHANNEL_PENDING_TAB_ICON[0], self.CHANNEL_PENDING_TAB_ICON[1].replace('ENTRY_NAME', entry)) 
                element = self.wait_element(tmpEntry)
                      
                entryId = element.get_attribute("id")
                tmpEntryID = (self.CHANNEL_PENDING_ENTRY_DATA[0], self.CHANNEL_PENDING_ENTRY_DATA[1].replace('ENTRY_ID', entryId))           
                try:
                    entryThumbnail = self.get_element(tmpEntryID)
                except Exception:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' element")
                    return False
            else:
                tmpEntry = (self.MY_MEDIA_ENTRY_THUMBNAIL[0], self.MY_MEDIA_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entry))
                try:
                    entryThumbnail = self.get_element(tmpEntry)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' element")
                    return False        

            if entryType == enums.MediaType.IMAGE:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_IMAGE_ICON)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Image icon")
                    return False

            if entryType == enums.MediaType.AUDIO:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_AUDIO_ICON)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Audio icon")
                    return False

            if entryType == enums.MediaType.QUIZ:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_QUIZ_ICON)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Quiz icon")
                    return False

            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                if entryType == enums.MediaType.VIDEO:
                    try:
                        self.get_child_element(entryThumbnail, self.MY_MEDIA_VIDEO_ICON_OLD_UI)
                    except NoSuchElementException:
                        writeToLog("INFO","FAILED to find entry '" + entry + "' Video icon")
                        return False

        if self.verifyFilterUniqueIconType(entryType) == False:
            writeToLog("INFO","FAILED entries from different types display although the filter set to " + entryType.value)
            return False

        writeToLog("INFO","Success, All entry '" + entry + "' " + entryType.value + "  icon was verify")
        return True

      
    #@Author: Oded berihon 
    # The function going over the entries list and check that the entries icon that display on the thumbnail are  match the 'entryType' parameter
    def verifyEntryTypeIconAferSearch(self, entriesList, entryType):
        for entry in entriesList:
            entryThumbnail = self.wait_element(self.MY_MEDIA_ENTRY_THUMBNAIL_ELASTIC_SEARCH)
            if entryThumbnail == False:
                writeToLog("INFO","FAILED to find entry '" + entry + "' element")
                return False

            if entryType == enums.MediaType.IMAGE:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_IMAGE_ICON_AFTER_SEARCH)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Image icon")
                    return False

            if entryType == enums.MediaType.AUDIO:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_AUDIO_ICON_AFTER_SEARCH)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Audio icon")
                    return False

            if entryType == enums.MediaType.QUIZ:
                try:
                    self.get_child_element(entryThumbnail, self.MY_MEDIA_QUIZ_ICON_AFTER_SEARCH)
                except NoSuchElementException:
                    writeToLog("INFO","FAILED to find entry '" + entry + "' Quiz icon")
                    return False

            if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
                if entryType == enums.MediaType.VIDEO:
                    try:
                        self.get_child_element(entryThumbnail, self.MY_MEDIA_VIDEO_ICON_OLD_UI)
                    except NoSuchElementException:
                        writeToLog("INFO","FAILED to find entry '" + entry + "' Video icon")
                        return False

        if self.verifyFilterUniqueIconType(entryType) == False:
            writeToLog("INFO","FAILED entries from different types display although the filter set to " + entryType.value)
            return False

        writeToLog("INFO","Success, All entry '" + entry + "' " + entryType.value + "  icon was verify")
        return True


    #@Author: Michal Zomper
    # The function check that only the entries type with that match the 'iconType' parameter display in the list in my media
    # the function verify that their entries with diffrent iconType find in the filter
    # for exm: if i filter by Image i will check that only image entry display (checking by icon type)
    def verifyFilterUniqueIconType(self, iconType):
        if self.showAllEntries() == False:
            writeToLog("INFO","FAILED to show all entries in my media")
            return False

        if iconType != enums.MediaType.IMAGE:
            if self.wait_elements(self.MY_MEDIA_IMAGE_ICON) != False:
                writeToLog("INFO","FAILED, Image icon display in the list although only " + iconType.value + "need to be display")
                return False

        if iconType != enums.MediaType.AUDIO:
            if self.wait_elements(self.MY_MEDIA_AUDIO_ICON) != False:
                writeToLog("INFO","FAILED, Audio icon display in the list although only " + iconType.value + "need to be display")
                return False

        if localSettings.LOCAL_SETTINGS_IS_NEW_UI == False:
            if iconType != enums.MediaType.VIDEO:
                if self.wait_elements(self.MY_MEDIA_VIDEO_ICON_OLD_UI) != False:
                    writeToLog("INFO","FAILED, Video icon display in the list although only " + iconType.value + "need to be display")
                    return False

        writeToLog("INFO","Success, only " + iconType.value + " type entries display")
        return True


    #@Author: Michal Zomper
    def expendAndVerifyPublishedEntriesDetails(self, entryName, categoris, channels):
        if self.verifyEntryPrivacyInMyMedia(entryName, enums.EntryPrivacyType.PUBLISHED, forceNavigate=False) == False:
                writeToLog("INFO","FAILED to verify entry '" + entryName + "' privacy")
                return False

        if self.verifyPublishedInExpendEntryDeatails(entryName, categoris, len(categoris), channels, len(channels)) == False:
            writeToLog("INFO","FAILED to verify entry '" + entryName + "' published categories/channels")
            return False

        writeToLog("INFO","Success, Entry published details were verified successfully")
        return True


    #@Author: Michal Zomper
    # pre condition to this function : need to open the publish option (the '+' button) in order to see all the publish details
    # the function verifyEntryPrivacyInMyMedia have the option to open the details
    def verifyPublishedInExpendEntryDeatails(self, entryName, categories="", categoryCount="",  channels="", channelCount=""):
        tmpEntry = self.replaceInLocator(self.MY_MEDIA_ENTRY_PARNET, "ENTRY_NAME", entryName)
        entryId = self.clsCommon.upload.extractEntryID(tmpEntry)
        detailsBody = (self.MY_MEDIA_EXPEND_MEDIA_DETAILS[0], self.MY_MEDIA_EXPEND_MEDIA_DETAILS[1].replace('ENTRY_ID', entryId))

        tmpDetails = self.get_element(detailsBody).text
        tmpDetails = tmpDetails.split("\n")

        if len(categories) > 0:
            # verify number of published categories
            if len(categories) == 1:
                if (str(categoryCount) + " Category:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(categoryCount) + " categories")
                    return False
            else:
                if (str(categoryCount) + " Categories:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(categoryCount) + " categories")
                    return False

            # Verify categories names
            listOfCategories =""
            for category in categories:
                listOfCategories = listOfCategories + category + " "
            listOfCategories = (listOfCategories.strip())

            if listOfCategories in tmpDetails == False:
                writeToLog("INFO","FAILED to find category '" + category + "' under the entry '" + entryName + "' published in option")
                return False

        if len(channels) > 0:
            # verify number of published categories
            if len(channels) == 1:
                if (str(channelCount) + " Channel:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(channelCount) + " channels")
                    return False
            else:
                if (str(channelCount) + " Channels:") in tmpDetails == False:
                    writeToLog("INFO","FAILED to verify entry '" + entryName + "' have " + str(channelCount) + " channels")
                    return False

            # Verify channels names
            listOfChannels =""
            for channel in channels:
                listOfChannels = listOfChannels + channel + " "
            listOfChannels = (listOfChannels.strip())

            if listOfChannels in tmpDetails == False:
                writeToLog("INFO","FAILED to find channel '" + channel + "' under the entry '" + entryName + "' published in option")
                return False

        writeToLog("INFO","Success, All entry '" + entryName + "' categories/channels display under published in option")
        return True


    #@Author: Michal Zomper
    def verifyMyMediaView(self, entryName, view=enums.MyMediaView.DETAILED):
        tmpEntryCheckBox = (self.MY_MEDIA_ENTRY_CHECKBOX[0], self.MY_MEDIA_ENTRY_CHECKBOX[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryCheckBox) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' checkbox")
            return False

        tmpEntryName = (self.MY_MEDIA_ENTRY_TOP[0], self.MY_MEDIA_ENTRY_TOP[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryName) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' title")
            return False

        tmpEntryEditButton = (self.MY_MEDIA_ENRTY_EDIT_BUTTON[0], self.MY_MEDIA_ENRTY_EDIT_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryEditButton) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' edit Button")
            return False

        tmpEntryDeleteButton = (self.MY_MEDIA_ENRTY_DELETE_BUTTON[0], self.MY_MEDIA_ENRTY_DELETE_BUTTON[1].replace('ENTRY_NAME', entryName))
        if self.is_visible(tmpEntryDeleteButton) == False:
            writeToLog("INFO","FAILED to find entry '" + entryName + "' delete button")
            return False

        if view == enums.MyMediaView.DETAILED:
            tmpEntryThmbnail = (self.MY_MEDIA_ENTRY_THUMBNAIL[0], self.MY_MEDIA_ENTRY_THUMBNAIL[1].replace('ENTRY_NAME', entryName))
            if self.is_visible(tmpEntryThmbnail) == False:
                writeToLog("INFO","FAILED to find entry '" + entryName + "' thumbnail")
                return False

        writeToLog("INFO","Success, my media '" + view.value + " view' was verify for entry '" + entryName + "'")
        return True


    #@Author: Michal Zomper
    def verifyMyMediaViewForEntris(self, entrisList, viewType):
        # Checking if entriesNames list type
        if type(entrisList) is list:
            for entry in entrisList:
                if self.verifyMyMediaView(entry, viewType) == False:
                    writeToLog("INFO","FAILED to verify my media view '" + viewType.value + "' for entry" + entry + "'")
                    return False

        else:
            if self.verifyMyMediaView(entrisList) == False:
                writeToLog("INFO","FAILED to verify my media view '" + viewType.value + "' for entry" + entrisList + "'")
                return False

        writeToLog("INFO","Success, my media '" + viewType.value + " view' was verified")
        return True


    def verifyNoResultAfterSearchInMyMedia(self, entryName, forceNavigate=False):
        if self.searchEntryMyMedia(entryName, forceNavigate) == False:
            writeToLog("INFO","FAILED to search entry '" + entryName + "' in my media")
            return False

        if self.wait_visible(self.MY_MEDIA_NO_ENTRIES_FOUND, timeout=15) == False:
            writeToLog("INFO","FAILED to verify 'No Result' text was found after search")
            return False

        writeToLog("INFO","Success, 'No Result' text display after search")
        return True


    # @Author: Inbar Willman
    # Verify if 'Search in' drop down in enabled or disabled
    def verifySearchInDropDownState(self, isEnabled=True):
        # If search in dropdown should be visible
        if isEnabled == True:
            if self.is_visible(self.SEARCH_IN_DROPDOWN_ENABLED, True) == False:
                writeToLog("INFO","FAILED to enabled 'search in' dropdown")
                return False

        # If search in dropdown should be disabled
        elif isEnabled == False:
            if self.is_visible(self.SEARCH_IN_DROPDOWN_DISABLED, True) == False:
                writeToLog("INFO","FAILED to disabled 'search in' dropdown")
                return False

        return True


    # @Author: Inbar Willman
    # Select search in value
    def selectSearchInDropDownOption(self, option=enums.SearchInDropDown.ALL_FIELDS, location=enums.Location.MY_MEDIA):
        # Click on 'Search in' drop down
        if self.click(self.SEARCH_IN_DROPDOWN_ENABLED) == False:
            writeToLog("INFO","FAILED to click on 'search in' dropdown")
            return False

        sleep(5)

        #Get option locator
        tmp_option = (self.SEARCH_IN_DROP_DOWN_OPTION[0], self.SEARCH_IN_DROP_DOWN_OPTION[1].replace('FIELD_NAME', option.value))

        # Check if we are in add to channel page - media tab
        if location == enums.Location.ADD_TO_CHANNEL_MY_MEDIA:
            # If option is comments choose the third element in page
            if option == enums.SearchInDropDown.COMMENTS:
                tmp_option = self.get_elements(tmp_option)[2]
            else:
                tmp_option = self.get_elements(tmp_option)[1]

            if tmp_option.click() == False:
                writeToLog("INFO","FAILED to select " + option.value + " option")
                return False

        # Check if we are in add to channel page - pending tab
        elif location == enums.Location.ADD_TO_CHANNEL_SR:
            # If option is comments choose the third element in page
            if option == enums.SearchInDropDown.COMMENTS:
                tmp_option = self.get_elements(tmp_option)[4]
            else:
                tmp_option = self.get_elements(tmp_option)[2]

            if tmp_option.click() == False:
                writeToLog("INFO","FAILED to select " + option.value + " option")
                return False

        else:
            if self.click(tmp_option) == False:
                writeToLog("INFO","FAILED to select " + option.value + " option")
                return False

        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(5)
        
        if self.verifySearchInSelectedOption(option.value) == False:
            writeToLog("INFO","FAILED to display " + option.value + " option in 'Search in' ")
            return False
            
        return True


    # @Author: Inbar Willman
    # Check entries fields in results
    # fieldDict = True - the field should be displayed in results
    # fieldDict = False - the field shouldn't be displayed in results
    def checkEntriesFieldsInResults(self, fieldDict):
        for field in fieldDict:
            tmp_field = (self.ENTRY_FIELD_IN_RESULTS[0], self.ENTRY_FIELD_IN_RESULTS[1].replace('FIELD_NAME', field))

            #if field[1] == True:
            # Check if field is visible - should be visible
            if fieldDict[field] == True:
                if self.is_visible(tmp_field) == False:
                    writeToLog("INFO","FAILED to displayed " + str(field) + " in results, although field should be displayed")
                    return False

            #if field[1] == False:
            # Check if field is visible - shouldn't be visible
            else:
                if self.is_present(tmp_field, timeout=3) == True:
                    writeToLog("INFO","FAILED to displayed " + str(field) + " in results, although it shouldn't be displayed")
                    return False

        writeToLog("INFO", "Success, Fields display in results is correct")
        return True


    # @Author: Inbar Willman
    # Verify that field display is correct:
    # isSingle=True - there is just single display of the field
    # isSingle=False - There is more than single display of the field
    def verifyFieldDisplayInResultAfterClickingOnField(self, isSingle, field, numOfDisplay=1):
        # Click on field in order to see field values
        if self.clickOnFieldInResults(isSingle, field, numOfDisplay) == False:
            writeToLog("INFO","FAILED to click on field in 'keyword found in:'")
            return False

        # Verify that correct icon is displayed after clicking on field with correct number of display - before clicking show all
        if self.verifyFieldIconAndNumberOfDisplayInResults(isSingle, field, numOfDisplay, showAll=False) == False:
            writeToLog("INFO","FAILED to display correct number of values for " + field.value + " field")
            return False

        # Click again on field in order to close field values section
        if self.clickOnFieldInResults(isSingle, field, numOfDisplay) == False:
            writeToLog("INFO","FAILED to click on field in 'keyword found in:'")
            return False

        #Verify that values section isn't display anymore
        if self.wait_visible(self.ENTRY_FIELD_VALUES_SCETION, timeout=3) != False:
            writeToLog("INFO","FAILED: Field values section shouldn't be displayed anymore")
            return False

        return True


    # @Author: Inbar Willman
    # Verify that field display is correct:
    # iSingle=True - There is just once matching value of the field
    # iSingle=False - There is more than one matching value of the field
    def verifyFieldDisplayInResultAfterClickingOnShowMore(self, isSingle, field, entryOwner, categoriesList, numOfDisplay=1, isWebcast=False):
        # Click on show more button
        if self.click(self.ENTRY_FIELD_IN_RESULTS_SHOW_MORE_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Show more' button")
            return False

        # Verify that correct icon is displayed after clicking on field with correct number of display - before clicking show all
        if self.verifyFieldIconAndNumberOfDisplayInResults(isSingle, field, numOfDisplay, showAll=False) == False:
            writeToLog("INFO","FAILED to display correct number of values for " + field + " field")
            return False

        # Verify that correct entry details are displayed
        if self.verifyEntryDetailsAfterClickingShowMore(entryOwner, categoriesList) == False:
            writeToLog("INFO","FAILED to display correct entry's details")
            return False

        # Verify that correct icons are displayed
        if self.verifyEntryIconsAfterClickingShowMore(isWebcast)== False:
            writeToLog("INFO","FAILED to display correct entry icons")
            return False

        # Click on show less in order to close section
        if self.click(self.ENTRY_FIELD_IN_RESULTS_SHOW_LESS_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Show less' button")
            return False

        #Verify that values section isn't display anymore
        if self.wait_visible(self.ENTRY_FIELD_VALUES_SCETION, timeout=3) != False:
            writeToLog("INFO","FAILED: Field values section shouldn't be displayed anymore")
            return False

        return True


    # @Author: Inbar Willman
    # Verify that field display is correct:
    # Single - there is just single display of the field - There is no option to click 'show all'
    # Multiple - More than one matching value per field
    # Field is enums
    def verifyFieldDisplayInResultAfterClickingOnShowAll(self, isSingle, field, numOfDisplay=1):
        # Click on show more button
        if self.click(self.ENTRY_FIELD_IN_RESULTS_SHOW_MORE_BTN) == False:
            writeToLog("INFO","FAILED to click on 'Show more' button")
            return False

        # If there is just single value
        if isSingle == True:
            if self.is_visible(self.ENTRY_FIELD_IN_RESULTS_SHOW_ALL_BTN) == True:
                writeToLog("INFO","FAILED: 'Show All' button shouldn't be displayed")
                return False

        # If there is more single value, but lees than 5 displays
        elif isSingle == False and numOfDisplay < 5:
            if self.is_visible(self.ENTRY_FIELD_IN_RESULTS_SHOW_ALL_BTN) == True:
                writeToLog("INFO","FAILED: 'Show All' button shouldn't be displayed")
                return False

        # If there is more than single value, but the field is tag
        elif isSingle == False and field == enums.EntryFields.TAGS:
            if self.is_visible(self.ENTRY_FIELD_IN_RESULTS_SHOW_ALL_BTN) == True:
                writeToLog("INFO","FAILED: 'Show All' button shouldn't be displayed")
                return False

        else:
            sleep(2)
            if self.click(self.ENTRY_FIELD_IN_RESULTS_SHOW_ALL_BTN) == False:
                writeToLog("INFO","FAILED to click on 'Show All' button")
                return False

            sleep(5)

            # Verify that correct icon is displayed after clicking on field with correct number of display - before clicking show all
            if self.verifyFieldIconAndNumberOfDisplayInResults(isSingle, field, numOfDisplay, showAll=True) == False:
                writeToLog("INFO","FAILED to display correct number of values for " + field.value + " field")
                return False

            #Verify that icons of other fields aren't displayed
            if self.verifyIconsDisplay(field) == False:
                writeToLog("INFO","FAILED to display just " + field.value + " icon")
                return False

        return True


    # @Author: Inbar Willman
    # Click on field in 'keyword found in:'
    # Field is enums
    def clickOnFieldInResults(self, isSingle, field, numOfDisplay):
        if isSingle == True:
            # Get field element in 'keyword found in:' - single value per field
            tmp_field = (self.ENTRY_FIELD_IN_RESULTS[0], self.ENTRY_FIELD_IN_RESULTS[1].replace('FIELD_NAME', "1 " + field.value))
        else:
            # Get field element in 'keyword found in:' - multiple values per field
            tmp_field = (self.ENTRY_FIELD_IN_RESULTS[0], self.ENTRY_FIELD_IN_RESULTS[1].replace('FIELD_NAME', str(numOfDisplay) + " "  + field.value))

        # Click on field element in 'keyword found in:'
        if self.click(tmp_field) == False:
            writeToLog("INFO","FAILED to click on " + field.value + " field")
            return False

        writeToLog("INFO", "Success, field was clicked in 'keyword found in:'")
        return True


    # @Author: Inbar Willman
    # Verify the correct icon is displayed after clicking on field
    # Verify that correct number of fields value is displayed
    # Field is enums
    def verifyFieldIconAndNumberOfDisplayInResults(self, isSingle, field, numOfDisplay, showAll):
        if isSingle == False:
            if field == enums.EntryFields.QUIZ:
                fieldName = field.value
            elif field == enums.EntryFields.DETAILS:
                fieldName = field.value
            elif field == enums.EntryFields.TAGS:
                fieldName = field.value

            else:
                fieldName = field.value[:-1]

        elif field == enums.EntryFields.TAG:
            fieldName = field.value +"s"

        else:
            fieldName = field.value

        tmp_field_icon = (self.ENTRY_FIELD_ICON_IN_RESULTS[0], self.ENTRY_FIELD_ICON_IN_RESULTS[1].replace('FIELD_NAME', fieldName))
        tmp_field_icon_num_of_display = self.get_elements(tmp_field_icon)

        # Check that field icon is visible
        if self.is_visible(tmp_field_icon) == False:
            writeToLog("INFO","FAILED to display correct icon field")
            return False

        if isSingle == True:
            # Check that icon is displayed just once
            if len(tmp_field_icon_num_of_display) !=1:
                writeToLog("INFO","FAILED to display correct number of icon display")
                return False

        else:
            # Check that tag icon is displayed just once although there are more than one matching tag value
            if field == enums.EntryFields.TAGS:
                if len(tmp_field_icon_num_of_display) !=1:
                    writeToLog("INFO","FAILED to display tag icon just once")
                    return False

                # Check that if number of matching tags is smaller than 7, all tags are displayed
                tmp_tags_values = self.get_elements(self.ENTRY_TAG_VALUES_IN_RESULTS)
                if numOfDisplay < 8:
                    if len(tmp_tags_values) != numOfDisplay:
                        writeToLog("INFO","FAILED to display correct number of tags values when there are less than 8 tag values")
                        return False

                # If number of matching tags is bigger than 7, just 7 tags are displayed
                else:
                    if len(tmp_tags_values) != 7:
                        writeToLog("INFO","FAILED to display correct number of tags values when there are more than 7 tag values")
                        return False

            elif field == enums.EntryFields.DETAILS:
                # Check that if number of matching details is smaller than 11, all details are displayed before clicking show all are displayed
                if numOfDisplay > 10 and showAll == False:
                    if len(tmp_field_icon_num_of_display) != 10:
                        writeToLog("INFO","FAILED to display correct number of details values when there are more than 10 details")
                        return False
                else:
                    # All matching details should be displayed when there are less than 10 matching details or that 'Show All' was clicked
                    if len(tmp_field_icon_num_of_display) != numOfDisplay:
                        writeToLog("INFO","FAILED to display correct number of details values when there are less than 11 details")
                        return False

            else:
                # If number of display is bigger than 5, 'Show All' wasn't clicked and field is different than 'Details'
                if numOfDisplay > 5 and showAll == False:
                    if len(tmp_field_icon_num_of_display) !=5:
                        writeToLog("INFO","FAILED to display correct number of field values")
                        return False

                # If number of display is smaller than 5, or that all field values should be display
                else:
                    if len(tmp_field_icon_num_of_display) != numOfDisplay:
                        writeToLog("INFO","FAILED to display correct number of field values")
                        return False

        writeToLog("INFO", "Success, field values display is correct")
        return True


    # @Author: Inbar Willman
    # Verify that correct entry details are displayed below thumbnail when clicking show more
    def verifyEntryDetailsAfterClickingShowMore(self, entryOwner, categoriesList):
        # Check entry's owner details
        if self.verifyEntryOwnerDetails(entryOwner) == False:
            writeToLog("INFO", "FAILED to displayed correct entry's owner details")
            return False

        # Check entry's creation date
        if self.verifyEntryCreationDetails() == False:
            writeToLog("INFO", "FAILED to displayed correct entry's creation details")
            return False

        if self.verifyEntryCategories(categoriesList) == False:
            writeToLog("INFO", "FAILED to displayed correct entry's categories details")
            return False

        return True


    # @Author: Inbar Willman
    # Verify that correct owner is displayed
    def verifyEntryOwnerDetails(self, entryOwner):
        tmp_entry_owner = (self.ENTRY_OWNER_DETAILS[0], self.ENTRY_OWNER_DETAILS[1].replace('OWNER_NAME', entryOwner))
        if self.is_visible(tmp_entry_owner) == False:
            writeToLog("INFO", "FAILED to displayed correct entry's owner details")
            return False

        return True


    # @Author: Inbar Willman
    # Verify that creation details are displayed
    def verifyEntryCreationDetails(self):
        if self.is_visible(self.ENTRY_CREATION_DETAILS) == False:
            writeToLog("INFO", "FAILED to displayed correct entry's creation details")
            return False

        return True


    # @Author: Inbar Willman
    # Verify that correct categories that entry is published in are displayed
    def verifyEntryCategories(self, categoriesList):
        tmp_categoriesList = self.get_elements(self.ENTRY_CATEGORIES_DETAILS)
        for dx, category in enumerate(categoriesList):
            tmp_category= tmp_categoriesList[dx]
            if tmp_category.text != category:
                writeToLog("INFO", "FAILED to displayed correct entry's categories details")
                return False

        return True


    # @Author: Inbar Willman
    # verify entry icons after clicking show more
    def verifyEntryIconsAfterClickingShowMore(self, isWebcast=False):
        if self.is_visible(self.ENTRY_DETAILS_COMMENTS_ICON) == False:
            writeToLog("INFO", "FAILED to displayed comment icon")
            return False

        if isWebcast == False:
            if self.is_visible(self.ENTRY_DETAILS_EYE_ICON) == False:
                writeToLog("INFO", "FAILED to displayed eye icon")
                return False
        else:
            if self.is_visible(self.ENTRY_DETAILS_EYE_ICON) == True:
                writeToLog("INFO", "FAILED - eye icon shouoldn't be displayed")
                return False

        if self.is_visible(self.ENTRY_DETAILS_HEART_ICON) == False:
            writeToLog("INFO", "FAILED to displayed eye icon")
            return False

        return True


    # @Author: Inbar Willman
    # Verify that when there is one matching field, after clicking 'show all' just the matching field values are displayed
    def verifyIconsDisplay(self, fieldName):
        fieldsList = ['Details', 'Tags', 'Caption', 'Chapter', 'Comment', 'Slide', 'Quiz', 'Poll']
        for field in fieldsList:
            if (field in fieldName.value) == False:
                tmp_field_icon = (self.ENTRY_FIELD_ICON_IN_RESULTS[0], self.ENTRY_FIELD_ICON_IN_RESULTS[1].replace('FIELD_NAME', field))
                if self.wait_visible(tmp_field_icon, timeout=3) != False:
                    writeToLog("INFO", "FAILED: Non matching fields are displayed after clicking show All")
                    return False

        return True


    # @Author: Horia Cus
    # Verify that the specific filter option is available or disabled on the first or second screen, based on the selected media type
    # If status=True, the checkbox should be enabled
    # If status=False, the checkbox should be disabled
    # checkBoxLabelValue = the filter type that should / shouldn't be displayed while filtering it by a specific media type
    def verifyFilterCheckBox(self, mediaType, checkBoxLabelValue, status=True, clearFilter=True):
        if self.SortAndFilter(enums.SortAndFilter.MEDIA_TYPE, mediaType) == False:
                writeToLog("INFO","FAILED to filter my media entries")
                return False

        tmpEntry = (self.FILTER_CHECKBOX_INACTIVE[0], self.FILTER_CHECKBOX_INACTIVE[1].replace('DROPDOWNLIST_ITEM', checkBoxLabelValue))
        if self.is_visible(tmpEntry, multipleElements=True) != True:
            if self.click(self.FILTER_NEXT_ARROW, multipleElements=True) == False:
                writeToLog("INFO", "Failed to enter on the second page ")
                return False

            if self.click(tmpEntry, timeout=3) == False:
                self.status = "Fail"
                writeToLog("INFO","FAILED to identify captions filters")
                return False

            if status == True:
                if self.wait_visible(tmpEntry, timeout=3) != False:
                    writeToLog("INFO","FAILED, the caption filter option is disabled")
                    return False
            else:
                if self.wait_visible(tmpEntry, timeout=3) == False:
                    writeToLog("INFO","FAILED, the caption filter option is enabled")
                    return False
                
            if clearFilter == True:
                if self.click(self.FILTER_PREVIOUS_ARROW) == False:
                    writeToLog("INFO", "Failed to enter on the second page ")
                    return False
            
                if self.filterClearAllWhenOpened() == False:
                    writeToLog("INFO","FAILED to clear all the search filters")
                    return False

        else:
            if self.click(tmpEntry, timeout=3) == False:
                self.status = "Fail"
                writeToLog("INFO","FAILED to identify captions filters")
                return False

            if status == True:
                if self.wait_visible(tmpEntry, timeout=3) != False:
                    writeToLog("INFO","FAILED, the caption filter option is disabled")
                    return False
            else:
                if self.wait_visible(tmpEntry, timeout=3) == False:
                    writeToLog("INFO","FAILED, the caption filter option is enabled")
                    return False
            
            if clearFilter == True:
                if self.filterClearAllWhenOpened() == False:
                    writeToLog("INFO","FAILED to clear all the search filters")
                    return False

        return True


    # @Author: Horia Cus
    # The function clears all the filter option while the filter menu is opened and then closes it
    def filterClearAllWhenOpened(self):
        if self.click(self.FILTER_CLEAR_ALL_BUTTON, 20, multipleElements=True) == False:
            writeToLog("INFO","FAILED to clear all the search filters")
            return False

        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "FAILED to process the clear all request")
            return False

        if self.click(self.FILTER_BUTTON_DROPDOWN_MENU, 20, multipleElements=True) == False:
            writeToLog("INFO","FAILED to close the filters drop down menu")
            return False

        return True


    # @Author: Horia Cus
    # The function selects a specific element and moves it by width
    # Use value 0 in order to select the start pointer
    # Use value 10800 in order to select the end pointer
    def filterCustomDuration(self, size, value='0'):
        tmpLocator = (self.FILTER_CUSTOM_DURATION[0], self.FILTER_CUSTOM_DURATION[1].replace('VALUE_TO_REPLACE', value))

        elementToBeMoved = self.wait_element(tmpLocator, multipleElements=True)
        if elementToBeMoved == False:
            writeToLog("INFO", "Failed to get " + tmpLocator[1] + "'")
            return False

        action = ActionChains(self.driver)
        try:
            action.move_to_element(elementToBeMoved).click_and_hold().move_by_offset(size, 0).pause(1).release().perform()
        except Exception:
            self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN, 6)
            sleep(1)
            try:
                action.move_to_element(elementToBeMoved).click_and_hold().move_by_offset(size, 0).pause(1).release().perform()
            except Exception:
                writeToLog("INFO", "FAILED to move the specific element")
                return False

        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "FAILED to save the filter changes")
            return False

        return True


    # @Author: Horia Cus
    # This function selects a specific date from the calendar menu while being used in the filters menu
    # year must be integer
    # month must be integer
    # day must be string
    # If the desired date is not found within the number of tries, the function will return false
    def filterSelectDate(self, year, month, day, tries=36):
        if self.click(self.FILTER_SINGLE_DATE_CALENDAR, multipleElements=True) == False:
            writeToLog("INFO", "Failed to activate the calendar menu")
            return False

        now = datetime.datetime.now()

        current_year = now.year
        current_month = now.month

        tmp_locator = (self.FILTER_SINGLE_DATE_CURRENT_MONTH[0], self.FILTER_SINGLE_DATE_CURRENT_MONTH[1].replace('YEAR', str(year)))
        selected_month = calendar.month_name[month]
        tmp_locator = (tmp_locator[0], tmp_locator[1].replace('MONTH', selected_month))
        
        if year == current_year and month == current_month:
            tmp_locator = (self.FILTER_SINGLE_DATE_DAY[0], self.FILTER_SINGLE_DATE_DAY[1].replace('DAY_NUMBER', day))
            if self.click(tmp_locator) == False:
                writeToLog("INFO", "Failed to select a date from calendar menu")
                return False

        elif year < current_year:
            i = 0
            while self.wait_visible(tmp_locator, timeout=1, multipleElements=True) == False and i < tries:
                i = i
                if self.click(self.FILTER_SINGLE_DATE_BACK_BUTTON, timeout=5, multipleElements=True) == False:
                    writeToLog("INFO", "Failed to navigate through the calendar menu")
                    return False
                i = i + 1

            tmp_locator = (self.FILTER_SINGLE_DATE_DAY[0], self.FILTER_SINGLE_DATE_DAY[1].replace('DAY_NUMBER', day))
            if self.click(tmp_locator) == False:
                writeToLog("INFO", "Failed to select a date from calendar menu")
                return False
            
        elif year == current_year and month < current_month:
            i = 0
            while self.wait_visible(tmp_locator, timeout=1, multipleElements=True) == False and i < tries:
                i = i
                if self.click(self.FILTER_SINGLE_DATE_BACK_BUTTON, timeout=5, multipleElements=True) == False:
                    writeToLog("INFO", "Failed to navigate through the calendar menu")
                    return False
                i = i + 1

            tmp_locator = (self.FILTER_SINGLE_DATE_DAY[0], self.FILTER_SINGLE_DATE_DAY[1].replace('DAY_NUMBER', day))
            if self.click(tmp_locator) == False:
                writeToLog("INFO", "Failed to select a date from calendar menu")
                return False

        elif year > current_year:
            i = 0
            while self.wait_visible(tmp_locator, timeout=1, multipleElements=True) == False and i < tries:
                i = i
                if self.click(self.FILTER_SINGLE_DATE_NEXT_BUTTON, timeout=5, multipleElements=True) == False:
                    writeToLog("INFO", "Failed to navigate through the calendar menu")
                    return False
                i = i + 1

            tmp_locator = (self.FILTER_SINGLE_DATE_DAY[0], self.FILTER_SINGLE_DATE_DAY[1].replace('DAY_NUMBER', day))
            if self.click(tmp_locator) == False:
                writeToLog("INFO", "Failed to select a date from calendar menu")
                return False

        elif year == current_year and month > current_month:
            i = 0
            while self.wait_visible(tmp_locator, timeout=1, multipleElements=True) == False and i < tries:
                i = i
                if self.click(self.FILTER_SINGLE_DATE_NEXT_BUTTON, timeout=5, multipleElements=True) == False:
                    writeToLog("INFO", "Failed to navigate through the calendar menu")
                    return False
                i = i + 1

            tmp_locator = (self.FILTER_SINGLE_DATE_DAY[0], self.FILTER_SINGLE_DATE_DAY[1].replace('DAY_NUMBER', day))
            if self.click(tmp_locator) == False:
                writeToLog("INFO", "Failed to select a date from calendar menu")
                return False

        else:
            writeToLog("INFO", "FAILED: To select a date, please make sure that you inserted a valid date, using year and month as integer and day as string")
            return False

        return True
   
    
    # @Author: Inbar Willman
    # Verify chosen field is displayed in 'Search in' after selected in dropdown
    def verifySearchInSelectedOption(self, chosenOption, timeout=10):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        self.setImplicitlyWait(0)
        while True:
            try:
                elements = self.get_elements(self.SEARCH_IN_CHOSEN_OPTION)
                for el in elements:
                    if el.size['width']!=0 and el.size['height']!=0:
                        if el.text == "Search In: " + chosenOption:
                            self.setImplicitlyWaitToDefault()
                            return True
                        else:
                            writeToLog("INFO", "Failed to find the element")
                            return False
            except:
                if wait_until < datetime.datetime.now():
                    self.setImplicitlyWaitToDefault()
                    return False                 
                pass   


    # @Author: Horia Cus
    # The function verifies if a specific action option is disabled or enabled
    def verifyActionOptionStatus(self, actionID='', disabled=False):
        if self.click(self.MY_MEDIA_ACTIONS_BUTTON) == False:
            writeToLog("INFO", "Failed to open the actions drop down menu")
            return False
                
        if disabled == True:
            tmp_locator = (self.ACTION_TAB_OPTION_NORMAL[0], self.ACTION_TAB_OPTION_NORMAL[1].replace('ACTIONID', actionID))
            if self.is_visible(tmp_locator, multipleElements=True) == False:
                writeToLog("INFO", "The specific action option is not present")
                return False
            
            tmp_locator = (self.ACTION_TAB_OPTION_DISABLED[0], self.ACTION_TAB_OPTION_DISABLED[1].replace('ACTIONID', actionID))
            if self.is_visible(tmp_locator) != True:
                writeToLog("INFO", "The specific action option is enabled")
                return False
        else:
            tmp_locator = (self.ACTION_TAB_OPTION_DISABLED[0], self.ACTION_TAB_OPTION_DISABLED[1].replace('ACTIONID', actionID))
            if self.is_present(tmp_locator, 1) == True:
                writeToLog("INFO", "The specific action option is disabled")
                return False
                
            tmp_locator = (self.ACTION_TAB_OPTION_NORMAL[0], self.ACTION_TAB_OPTION_NORMAL[1].replace('ACTIONID', actionID))
            if self.is_visible(tmp_locator, multipleElements=True) == False:
                writeToLog("INFO", "The specific action option is not present")
                return False

        return True


    # @Author: Horia Cus
    # Verify that the user is able to select and un-select any sort filter option and that the checkbox and remove options are properly displayed
    # enable = True, it will enable each desired sort filter option and verify that the checbkox is checked and the remove option is present
    # disable = True, it will disable the desired sort filter option and verify that the checkbox is un checked and the remove option is no longer present
    def verifyFilterSection(self, filterType='', filterOption='', enable=False, disable=False, clearFilterMenu=False):
        if filterType == enums.SortAndFilter.MEDIA_TYPE:
            tmpEntryAll = (self.FILTER_SORT_TYPE_ENABLED[0], self.FILTER_SORT_TYPE_ENABLED[1].replace('DROPDOWNLIST_ITEM', enums.MediaType.ALL_MEDIA.value))

        elif filterType == enums.SortAndFilter.SCHEDULING:
            tmpEntryAll = (self.FILTER_SORT_TYPE_ENABLED[0], self.FILTER_SORT_TYPE_ENABLED[1].replace('DROPDOWNLIST_ITEM', enums.Scheduling.ALL.value))

        elif filterType == enums.SortAndFilter.DURATION:
            tmpEntryAll = (self.FILTER_SORT_TYPE_ENABLED[0], self.FILTER_SORT_TYPE_ENABLED[1].replace('DROPDOWNLIST_ITEM', enums.Duration.ANY_DURATION.value))

        elif filterType == enums.SortAndFilter.CREATION_DATE:
            tmpEntryAll = (self.FILTER_SORT_TYPE_ENABLED[0], self.FILTER_SORT_TYPE_ENABLED[1].replace('DROPDOWNLIST_ITEM', enums.Creation.ANY_DATE.value))
        
        else:
            tmpEntryAll = ''

        if enable == True:
            if type(filterOption) is list:
                filterList = {filterType:filterOption}
                i = 0
                for entry in filterList:
                    while True:
                        i = i
                        try:
                            tmpEntryRemoveOption = (self.FILTER_SORT_TYPE_REMOVE_BUTTON[0], self.FILTER_SORT_TYPE_REMOVE_BUTTON[1].replace('DROPDOWNLIST_ITEM', filterList[entry][i].value))
                        except Exception:
                            break

                        tmpLocator = (self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[0], self.MY_MEDIA_DROPDOWNLIST_ITEM_NEW_UI[1].replace('DROPDOWNLIST_ITEM', filterList[entry][i].value))
                        tmpEntryCheckBox = (self.FILTER_SORT_TYPE_ENABLED[0], self.FILTER_SORT_TYPE_ENABLED[1].replace('DROPDOWNLIST_ITEM', filterList[entry][i].value))
                        if self.wait_element(tmpLocator, 1, multipleElements=True) != False and self.wait_element(tmpEntryRemoveOption, 1, multipleElements=True) == False:
                            if self.SortAndFilter(entry, filterList[entry][i]) == False:
                                return False

                            try:
                                if i >= 1 and self.wait_element(tmpEntryAll, 1, multipleElements=True) != False:
                                    if self.wait_element(tmpEntryRemoveOption, 1, multipleElements=True) != False or self.wait_element(tmpEntryCheckBox, 1, multipleElements=True) != False:
                                        writeToLog("INFO", "Failed, the remove option or checkbox for " + filterList[entry][i].value + " is still present while ALL the sort type options are selected")
                                        return False
                                    else:
                                        break
                            except Exception:
                                break

                            if self.verifyFilterRemoveOptionAndCheckbox(filterList[entry][i], True) == False:
                                return False
                            else:
                                i = i + 1
                        else:
                            writeToLog("INFO", "Some elements are not properly displayed while filtering them by " + filterList[entry][i].value )
                            return False

                    i = i - 1
                    while True:
                        i = i
                        tmpEntryRemoveOption = (self.FILTER_SORT_TYPE_REMOVE_BUTTON[0], self.FILTER_SORT_TYPE_REMOVE_BUTTON[1].replace('DROPDOWNLIST_ITEM', filterList[entry][i].value))
                        tmpEntryCheckBox = (self.FILTER_SORT_TYPE_ENABLED[0], self.FILTER_SORT_TYPE_ENABLED[1].replace('DROPDOWNLIST_ITEM', filterList[entry][i].value))
                        try:
                            if i >= 0 and self.wait_element(tmpEntryAll, 1, multipleElements=True) != False:
                                if self.wait_element(tmpEntryRemoveOption, 1, multipleElements=True) != False or self.wait_element(tmpEntryCheckBox, 1, multipleElements=True) != False:
                                    writeToLog("INFO", "Failed, the remove option or checkbox for " + filterList[entry][i].value + " is still present while ALL the sort type options are selected")
                                    return False
                                else:
                                    break
                        except Exception:
                            break

                        if i != -1:
                            if self.verifyFilterRemoveOptionAndCheckbox(filterList[entry][i], True) == False:
                                return False
                            else:
                                i = i - 1
                        else:
                            break

            elif filterType != '' and filterOption != '':
                if self.SortAndFilter(filterType, filterOption) == False:
                    return False

                if self.verifyFilterRemoveOptionAndCheckbox(filterOption, True) == False:
                    return False

            else:
                writeToLog("INFO", "Please make sure that only the sortOption is list")
                return False

        if disable == True:
            if type(filterOption) is list:
                filterList = {filterType:filterOption}
                i = 0
                for entry in filterList:
                    while True:
                        i = i
                        try:
                            tmpEntryRemoveOption = (self.FILTER_SORT_TYPE_REMOVE_BUTTON[0], self.FILTER_SORT_TYPE_REMOVE_BUTTON[1].replace('DROPDOWNLIST_ITEM', filterList[entry][i].value))
                        except Exception:
                            break
                        tmpEntryCheckBox = (self.FILTER_SORT_TYPE_DISABLED[0], self.FILTER_SORT_TYPE_DISABLED[1].replace('DROPDOWNLIST_ITEM', filterList[entry][i].value))


                        if self.removeFilterOptionWithXButton(filterList[entry][i])== False:
                            return False

                        try:
                            if i >= 1 and self.wait_element(tmpEntryAll, 1, multipleElements=True) != False:
                                if self.wait_element(tmpEntryRemoveOption, 1, multipleElements=True) != False and self.wait_element(tmpEntryCheckBox, 1, multipleElements=True) == False and self.wait_element(tmpEntryAll, 5, multipleElements=True) == False:
                                    writeToLog("INFO", "Failed, the remove option or checkbox for " + filterList[entry][i].value + " is still present while ALL the sort type options are selected")
                                    return False
                                else:
                                    break
                        except Exception:
                            break

                        if self.verifyFilterRemoveOptionAndCheckbox(filterList[entry][i], False) == False:
                            return False
                        else:
                            i = i + 1

            elif filterType != '' and filterOption != '':

                if self.removeFilterOptionWithXButton(filterOption)== False:
                    return False

                if self.verifyFilterRemoveOptionAndCheckbox(filterOption, False) == False:
                    return False

            else:
                writeToLog("INFO", "Please make sure that only the sortOption is list")
                return False

        if enable == True or disable == True:
            writeToLog("INFO", "All the filter options were properly displayed")
        else:
            writeToLog("INFO", "Please specify if the filter option should be enabled or disabled")
            return False

        if clearFilterMenu == True:
            if self.wait_element(self.FILTER_NEXT_ARROW, 1, multipleElements=True) == False:
                if self.click(self.FILTER_PREVIOUS_ARROW, 1, multipleElements=True) == False:
                    writeToLog("INFO", "Failed to use the previous arrow button")
                    return False

                if self.filterClearAllWhenOpened() == False:
                    return False
            else:
                if self.filterClearAllWhenOpened() == False:
                    return False

        return True

    
    # @Author: Horia Cus
    # Verify that the checkbox option and remove options are properly displayed
    # enabled = True, the checkbox should be enabled and the remove option should be present
    # disabled = True, the checkbox should be disabled and the remove option should not be present
    def verifyFilterRemoveOptionAndCheckbox(self, filterOption='', stateEnabled=True):
        if stateEnabled == True:
            tmpEntryCheckBox = (self.FILTER_SORT_TYPE_ENABLED[0], self.FILTER_SORT_TYPE_ENABLED[1].replace('DROPDOWNLIST_ITEM', filterOption.value))
            if self.wait_element(tmpEntryCheckBox, timeout=5, multipleElements=True) == False:
                writeToLog("INFO", "The " + filterOption.value + " checkbox is not checked")
                return False
            
            tmpEntryRemoveOption = (self.FILTER_SORT_TYPE_REMOVE_BUTTON[0], self.FILTER_SORT_TYPE_REMOVE_BUTTON[1].replace('DROPDOWNLIST_ITEM', filterOption.value))
            if self.wait_element(tmpEntryRemoveOption, timeout=5, multipleElements=True) == False:
                writeToLog("INFO", "The " + filterOption.value + " remove option is not present")
                return False

        else:
            tmpEntryCheckBox = (self.FILTER_SORT_TYPE_DISABLED[0], self.FILTER_SORT_TYPE_DISABLED[1].replace('DROPDOWNLIST_ITEM', filterOption.value))
            if self.wait_element(tmpEntryCheckBox, timeout=5, multipleElements=True) == False:
                writeToLog("INFO", "The " + filterOption.value + " checkbox is checked")
                return False
            
            tmpEntryRemoveOption = (self.FILTER_SORT_TYPE_REMOVE_BUTTON[0], self.FILTER_SORT_TYPE_REMOVE_BUTTON[1].replace('DROPDOWNLIST_ITEM', filterOption.value))
            if self.wait_element(tmpEntryRemoveOption, timeout=5, multipleElements=True) != False:
                writeToLog("INFO", "The " + filterOption.value + " remove option is still present")
                return False
      
        return True
    
    
    # @Author: Horia Cus
    # This function removes an enabled Filter Option by clicking on the "X" button
    # For filterOption you must use enums
    def removeFilterOptionWithXButton(self, filterOption=''):
        tmpEntryRemoveOption = (self.FILTER_SORT_TYPE_REMOVE_BUTTON[0], self.FILTER_SORT_TYPE_REMOVE_BUTTON[1].replace('DROPDOWNLIST_ITEM', filterOption.value))
        if self.wait_element(tmpEntryRemoveOption, timeout=5, multipleElements=True) == False:
            writeToLog("INFO", "The remove option for the " + filterOption.value + " is not present")
            return False 
        
        if self.click(tmpEntryRemoveOption, timeout=5, multipleElements=True) == False:
            writeToLog("INFO", "The remove option for the " + filterOption.value + " could not be used")
            return False       
        
        self.clsCommon.general.waitForLoaderToDisappear()
        
        if self.wait_element(tmpEntryRemoveOption, timeout=1, multipleElements=True) != False:
            writeToLog("INFO", "The remove option for the " + filterOption.value + " is still present after being used")
            return False
        
        return True
    

    # @Author: Horia Cus
    # The function filters the custom duration by clicking directing on the sidebbar
    # size must be integer
    # size must be positive if you filter from the start
    # size must be negative if you filter from the end
    # filterFromStart = True, it will filter the duration from the start point
    # filterFromStart = False, it will filter the duration from the end point
    def filterCustomDurationUsingSidebar(self, size, filterFromStart=True):
        if filterFromStart == True:
            locatorPointButton = (self.FILTER_CUSTOM_DURATION[0], self.FILTER_CUSTOM_DURATION[1].replace('VALUE_TO_REPLACE', '0'))
        else:
            locatorPointButton = (self.FILTER_CUSTOM_DURATION[0], self.FILTER_CUSTOM_DURATION[1].replace('VALUE_TO_REPLACE', '10800'))

        elementToBeMoved = self.wait_element(locatorPointButton, multipleElements=True)
        if elementToBeMoved == False:
            writeToLog("INFO", "Failed to get " + locatorPointButton[1] + "'")
            return False
        
        if self.wait_element(self.FILTER_CUSTOM_DURATION_SIDEBAR, 5, True) == False:
            writeToLog("INFO", "Custom duration sidebar is missing")
            return False

        action = ActionChains(self.driver)
        try:
            action.move_to_element(elementToBeMoved).move_by_offset(size, 0).pause(1).click().perform()
        except Exception:
            self.clsCommon.sendKeysToBodyElement(Keys.ARROW_DOWN, 6)
            sleep(1)
            try:
                action.move_to_element(elementToBeMoved).move_by_offset(size, 0).pause(1).click().perform()
            except Exception:
                writeToLog("INFO", "FAILED to move the specific element")
                return False
    
        if self.clsCommon.general.waitForLoaderToDisappear() == False:
            writeToLog("INFO", "FAILED to save the filter changes")
            return False

        return True        