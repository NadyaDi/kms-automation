import enums
from base import *
import clsTestService
from general import General
from selenium.webdriver.common.keys import Keys

class MyPlaylists(Base):
    driver = None
    clsCommon = None
         
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
    #=============================================================================================================
    #Playlist locators:
    #=============================================================================================================
    CREATE_PLAYLIST_TEXT_FIELD               = ('xpath' ,"//input[@value='Create new playlist']")
    CREATE_PLAYLIST_CREATE_BUTTON            = ('xpath', "//button[@id='playlistAddButton']")
    CREATE_PLAYLIST_SAVE_BUTTON              = ('xpath', "//button[@id='playlists-submit']")
    CREATE_PLAYLIST_CONFIRM_MSG              = ('xpath', "//div[contains(@class,'alert alert-success') and contains(text(),'Now your selected media is part of the selected playlist(s).')]")
    CREATE_PLAYLIST_CONFIRM_MSG_MULTIPLE     = ('xpath', "//div[contains(@class,'alert alert-success') and contains(text(),'Media added to selected playlist(s):')]")
    PLAYLIST_CHECKBOX                        = ('xpath', "//span[text() = 'PLAYLIST_NAME']")
    PLAYLIST_NAME                            = ('xpath', "//a[contains(@data-original-title,'PLAYLIST_NAME')]")
    PLAYLIST_DELETE_BUTTON                   = ('xpath', "//i[contains(@class,'icon-trash')]")
    PLAYLIST_DELETE_BUTTON_CONFIRM           = ('xpath', "//a[@class='btn btn-danger']")
    PLAYLIST_ENTRY_NAME_IN_PLAYLIST          = ('xpath', "//a[contains(@href,'/media/') and contains(text(), 'ENTRY_NAME')]")
    PLAYLIST_SAVE_BUTTON                     = ('xpath', "//button[@class='btn btn-primary saveBtn']")
    PLAYLIST_SAVED_ALERT                     = ('xpath', "//div[@class='alert alert-success ']")
    MY_PLAYLIST_TABLE_SIZE                   = ('xpath',"//table[@id='playlist-table']/tbody/tr")
    GO_TO_PLAYLIST_BUTTON                    = ('id', 'manage_playlists')
    PLAYLIST_EMBED_BUTTON                    = ('xpath', '//i[@class="v2ui-embedplaylistButton-PLAYLIST_ID icon-code"]')
    PLAYLIST_EMBED_TEXTAREA                  = ('xpath', '//textarea[@id="embed_code-PLAYLIST_ID"]')
    PLAYLIST_EMBED_PLAYER_SIZES              = ('xpath', '//iframe[@width="WIDTH_SIZE" and @height="HEIGHT_SIZE"]')
    PLAYLIST_TABLE                           = ('xpath', '//table[@id="playlist-table"]')
    CREATE_PLAYLIST_CONFIRM_MSG_ENTRY_PAGE   = ('xpath', '//div[contains(@class, "alert alert-success ") and contains(text(),"Media added to selected playlist(s): PLAYLIST_NAME.")]')
    #============================================================================================================

    #  @Author: Tzachi Guetta      
    # This method handles single and multiple add entry or entries to playlist.
    # If 'entryName' is a list of entries names, it will check them in my media and then add to playlist at once. Better use 'addEntriesToPlaylist' method for multiple.
    # If you want to create new playlist pass 'playlistName' and toCreateNewPlaylist = True
    # If you want to add to existing playlist pass 'playlistName' and toCreateNewPlaylist = False
    def addSingleEntryToPlaylist(self, entryName, playlistName='', toCreateNewPlaylist = False, currentLocation = enums.Location.MY_MEDIA):
        try:
            if currentLocation == enums.Location.MY_MEDIA: 
                if self.clsCommon.myMedia.navigateToMyMedia() == False:
                    writeToLog("INFO","FAILED to navigate to my media")
                    return False
                
                if type(entryName) is list: 
                    if self.clsCommon.myMedia.checkEntriesInMyMedia(entryName) == False:
                        writeToLog("INFO","FAILED to check entries in My-Media")
                        return False
                else: 
                    if self.clsCommon.myMedia.serachAndCheckSingleEntryInMyMedia(entryName) == False:
                        writeToLog("INFO","FAILED to check entry '" + entryName + "' check box")
                        return False
             
                if self.clsCommon.myMedia.clickActionsAndAddToPlaylistFromMyMedia() == False:
                    writeToLog("INFO","FAILED to click on action button")
                    return False
                    sleep(7)  
                      
            elif currentLocation == enums.Location.ENTRY_PAGE: 
                sleep(1)
                # Click on action tab
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, 30) == False:
                    writeToLog("INFO","FAILED to click on action button in entry page '" + entryName + "'")
                    return False  
                
                sleep(1)
                # Click on publish button
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ADDTOPLAYLIST_BUTTON, 30) == False:
                    writeToLog("INFO","FAILED to click on publish button in entry page '" + entryName + "'")
                    return False
            
            else:
                writeToLog("INFO","FAILED, Add entry to playlist: the provided ""currentLocation"" Value is not accepted ")
                return False
            
            
            if toCreateNewPlaylist != False:
                self.clear_and_send_keys(self.CREATE_PLAYLIST_TEXT_FIELD, playlistName)
                sleep(1)
            
                if self.click(self.CREATE_PLAYLIST_CREATE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on create playlist Button")
                    return False
                
                self.clsCommon.general.waitForLoaderToDisappear()
                
                sleep(1)
                if self.click(self.CREATE_PLAYLIST_SAVE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on create playlist Button")
                    return False
                
                if currentLocation == enums.Location.MY_MEDIA:
                    if self.wait_visible(self.CREATE_PLAYLIST_CONFIRM_MSG, 10) == False:
                        writeToLog("INFO","FAILED to to create playlist: " + playlistName)
                        return False
                
                else:
                    tmp_success_msg =(self.CREATE_PLAYLIST_CONFIRM_MSG_ENTRY_PAGE[0], self.CREATE_PLAYLIST_CONFIRM_MSG_ENTRY_PAGE[1].replace('PLAYLIST_NAME', playlistName))
                    if self.wait_visible(tmp_success_msg, 10) == False:
                        writeToLog("INFO","FAILED to to create playlist: " + playlistName)
                        return False
                
                writeToLog("INFO","Playlist: '" + playlistName + "' successfully created")
            
            else:
                tmp_playlist_name = (self.PLAYLIST_CHECKBOX[0], self.PLAYLIST_CHECKBOX[1].replace('PLAYLIST_NAME', playlistName))   
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to Check for playlist: '" + playlistName + "' something went wrong")
                    return False
                
                if self.click(self.CREATE_PLAYLIST_SAVE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on create playlist Button")
                    return False
                
                self.clsCommon.general.waitForLoaderToDisappear()
                sleep(1)
                
                if currentLocation == enums.Location.MY_MEDIA:
                    if self.wait_visible(self.CREATE_PLAYLIST_CONFIRM_MSG, 10) == False:
                        writeToLog("INFO","FAILED to to create playlist: " + playlistName)
                        return False
                
                else:
                    tmp_success_msg =(self.CREATE_PLAYLIST_CONFIRM_MSG_ENTRY_PAGE[0], self.CREATE_PLAYLIST_CONFIRM_MSG_ENTRY_PAGE[1].replace('PLAYLIST_NAME', playlistName))
                    if self.wait_visible(tmp_success_msg, 10) == False:
                        writeToLog("INFO","FAILED to to create playlist: " + playlistName)
                        return False
                
                writeToLog("INFO","Entry: """ + str(entryName) + """ added to Playlist: """ + playlistName + "")
                                       
        except NoSuchElementException:
            return False
            
        return True

    #  @Author: Tzachi Guetta
    def addEntriesToPlaylist(self, entriesName, playlistName, toCreateNewPlaylist):
        try:
            if self.addSingleEntryToPlaylist(entriesName, playlistName, toCreateNewPlaylist, currentLocation = enums.Location.MY_MEDIA) == False:
                writeToLog("INFO","FAILED to add the entries to play-list")
                return False
                
        except NoSuchElementException:
            return False
         
        writeToLog("INFO","Success, playlist '" + playlistName + "' was created successfully") 
        return True
    
    
    #  @Author: Tzachi Guetta      
    def navigateToMyPlaylists(self, forceNavigate = False):
        # Check if we are already in my media page
        if forceNavigate == False:
            if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL, False, 1) == True:
                return True
        
        # Click on User Menu Toggle Button
        if self.click(self.clsCommon.general.USER_MENU_TOGGLE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on User Menu Toggle Button")
            return False
        
        # Click on My Media
        if self.click(self.clsCommon.general.USER_MENU_MY_PLAYLISTS_BUTTON) == False:
            writeToLog("INFO","FAILED to on My playlists from the menu")
            return False
        
        if self.verifyUrl(localSettings.LOCAL_SETTINGS_KMS_MY_PLAYLISTS_URL, False) == False:
            writeToLog("INFO","FAILED to navigate to My playlists")
            return False
        
        return True
    
    
    #  @Author: Tzachi Guetta      
    def deletePlaylist(self, playlistName):
        try:
            if playlistName != '':
                if self.navigateToMyPlaylists() == False:
                    writeToLog("INFO","FAILED to navigate to my Playlists")
                    return False
                 
                tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
                    return False
    
                sleep(5)
                if self.click(self.PLAYLIST_DELETE_BUTTON, multipleElements=True) == False:
                    writeToLog("INFO","FAILED to click on playlist delete button (at my playlist page)")
                    return False
                
                sleep(2)
                if self.click(self.PLAYLIST_DELETE_BUTTON_CONFIRM, 30) == False:
                    writeToLog("INFO","FAILED to click on delete button confirmation, playlist name: '" + playlistName + "'")
                    return False
                
                self.clsCommon.general.waitForLoaderToDisappear()
                
                tmp_playlist_name_after_delete = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name_after_delete, timeout=3) == False:
                    writeToLog("INFO","Playlist: '" + playlistName + "' Was Deleted")
                    return True
                        
            else:
                writeToLog("INFO","FAILED, Not provided acceptable value playlistName")
                return False
                        
        except NoSuchElementException:
            return False
            
        return True
    
    
    #  @Author: Tzachi Guetta
    # Verify that there is only one entry displayed with the same name in the playlist     
    def verifySingleEntryInPlaylist(self, playlistName, entryName, isExpected=True):
        try:                
            if playlistName != '':
                if self.navigateToMyPlaylists() == False:
                    writeToLog("INFO","FAILED to navigate to my Playlists")
                    return False
                 
                tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
                    return False

                # Get entry element
                tmp_entry = (self.PLAYLIST_ENTRY_NAME_IN_PLAYLIST[0], self.PLAYLIST_ENTRY_NAME_IN_PLAYLIST[1].replace('ENTRY_NAME', entryName))
                
                # Check if entry is displayed more than once
                tmp_entry_display_list = self.get_elements(tmp_entry)
                
                # Get the number of displayed of the entry
                numberOfDisplay = len(tmp_entry_display_list)
                
                # Check that entry is displayed just once
                if numberOfDisplay == 1:
                    if isExpected == True:
                        writeToLog("INFO","As Expected: Entry was found in the Playlists")
                        return True
                    else:
                        writeToLog("INFO","NOT Expected: Entry was found " + str(numberOfDisplay) + " in the Playlists")
                        return False
                else:
                    if isExpected == False:
                        writeToLog("INFO","As Expected: Entry was not found in the Playlists")
                        return True
                    else:
                        writeToLog("INFO","NOT Expected: Entry was " + str(numberOfDisplay) + " found in the Playlists")
                        return False                    
            else:
                writeToLog("INFO","FAILED, Not provided acceptable value playlistName")
                return False                
                
        except NoSuchElementException:
            return False
            
        return True    
    
    #  @Author: Tzachi Guetta
    # indexEntryFrom - index of entry from entriesList we wish to move
    # indexEntryTo - The index of wished place to move in playlist, for example: 1 will move to the top of the list
    def shufflePlaylistEntries(self, playlistName, entriesList, indexEntryFrom, indexEntryTo):
        try:
            if playlistName != '':
                if self.navigateToMyPlaylists() == False:
                    writeToLog("INFO","FAILED to navigate to my Playlists")
                    return False
                 
                tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
                    return False
                
                tmp_entry_name = (self.PLAYLIST_ENTRY_NAME_IN_PLAYLIST[0], self.PLAYLIST_ENTRY_NAME_IN_PLAYLIST[1].replace('ENTRY_NAME', entriesList[indexEntryFrom]))
                source_element = self.get_element(tmp_entry_name)
                
                self.clsCommon.sendKeysToBodyElement(Keys.END)
                heightOfEntry = self.get_elements(self.MY_PLAYLIST_TABLE_SIZE)[0].size['height']
                moveX = 800
                moveY = int((indexEntryTo * heightOfEntry) +  heightOfEntry)
                writeToLog("INFO","FOR DEBUG: X = " + str(moveX) + "; Y = " + str(moveY))
                ActionChains(self.driver).drag_and_drop_by_offset(source_element, moveX, moveY).perform()
                
                sleep(2)
                if self.click(self.PLAYLIST_SAVE_BUTTON) == False:
                    writeToLog("INFO","FAILED to click on playlist 'Save' Button")
                    return False
                
                if self.is_present(self.PLAYLIST_SAVED_ALERT, 10) == False:
                    writeToLog("INFO","FAILED confirmation of save msg wasn't presented")
                    return False
                        
        except NoSuchElementException:
            return False
            
        return True
    
    
    # @author: Michal Zomper
    # the function return the playlist id 
    def getPlaylistID(self, playListName): 
        if self.navigateToMyPlaylists() == False:
            writeToLog("INFO","FAILED navigate to my playlist page")
            return False 
        
        tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playListName))
        if self.is_visible(tmp_playlist_name) == False:
            writeToLog("INFO","FAILED to find playlist '" + playListName + "' in my playlist page")
            return False 
        try:
            playlistID = self.get_element(tmp_playlist_name).get_attribute("id")
        
        except NoSuchElementException:
            writeToLog("INFO","FAILED to get playlist id")
            return False
        
        tmp = playlistID.split('-')
        
        if tmp[1] == '':
            writeToLog("INFO","FAILED to get playlist id")
            return False
        
        writeToLog("INFO","Success, successfully get playlist ID")
        return tmp[1]
    
    
    # @ Author: Inbar Willman
    # Click on embed playlist button and return the playlist embed code
    def clickEmbedPlaylistAndGetEmbedCode(self, playListName):
        #Get playlist id
        playlist_id = self.getPlaylistID(playListName)
        if playlist_id == False:
            writeToLog("INFO","FAILED to get playlist id")
            return False 
        
        #Click on playlist embed button
        tmpPlaylistEmbedBtm = (self.PLAYLIST_EMBED_BUTTON[0], self.PLAYLIST_EMBED_BUTTON[1].replace('PLAYLIST_ID', playlist_id))
        if self.click(tmpPlaylistEmbedBtm) == False:
            writeToLog("INFO","FAILED to click on playlist embed button")
            return False   
        
        #Wait until text section will be visible 
        tmpEmbedTextArea = (self.PLAYLIST_EMBED_TEXTAREA [0], self.PLAYLIST_EMBED_TEXTAREA [1].replace('PLAYLIST_ID', playlist_id))
        if self.wait_visible(tmpEmbedTextArea) == False:
            writeToLog("INFO","FAILED to get embed text area")
            return False  
        
        #Get embed code from embed text area 
        embed_code = self.getEmbedCode(tmpEmbedTextArea)
        if embed_code:
            return embed_code
        
        writeToLog("INFO","FAILED to get embed code")
        return False  
            
            
    # @ Author: Inbar Willman.
    # @ Refactor: Oleg Sigalov.
    # Return playlist embed code, if embed code doesn't contains matching phrase, return False
    def getEmbedCode(self, embedTextArea, timeout=60):
        wait_until = datetime.datetime.now() + datetime.timedelta(seconds=timeout)   
        while wait_until > datetime.datetime.now():
            try:
                #Get embed code
                embed_text = self.wait_element(embedTextArea).get_attribute('value')
                #Check if text contains 'iframe'
                if embed_text:
                    embedIframeText = "iframe"
                    if embedIframeText in embed_text:
                        return embed_text
            except:
                pass
        writeToLog("INFO","FAILED to get embed code")
        return False
    
    
    # @Author: Inbar Willman
    # Check player width and height (in order to check if we are in got the correct layout)
    def verifyEmbedPlayerSizes(self, width, height):
        tmp_playler_laylout = (self.PLAYLIST_EMBED_PLAYER_SIZES [0], self.PLAYLIST_EMBED_PLAYER_SIZES [1].replace('WIDTH_SIZE', width).replace('HEIGHT_SIZE', height))
        if self.is_visible(tmp_playler_laylout) == False:
            writeToLog("INFO","FAILED to get correct player sizes")
            return False
        return True
    
    
    # @Author: Ori Flchtman
    # Create new Empty Playlist
    def createEmptyPlaylist(self, entryName, playlistName):
        if self.clsCommon.myMedia.serachAndCheckSingleEntryInMyMedia(entryName) == False:
            writeToLog("INFO","FAILED to check entry '" + entryName + "' check box")
            return False
        
        if self.clsCommon.myMedia.clickActionsAndAddToPlaylistFromMyMedia() == False:
            writeToLog("INFO","FAILED to click on action button")
            return False
        
        if self.clear_and_send_keys(self.CREATE_PLAYLIST_TEXT_FIELD, playlistName) == False:
            writeToLog("INFO","FAILED to type playlist name")
            return False
        sleep(2)
    
        if self.click(self.CREATE_PLAYLIST_CREATE_BUTTON) == False:
            writeToLog("INFO","FAILED to click on create playlist Button")
            return False
        
        self.clsCommon.general.waitForLoaderToDisappear()
        sleep(1)
        return True
    
        
    def verifyEmptyPlaylistInMyPlaylists(self, playlistName):
        if self.navigateToMyPlaylists() == False:
            writeToLog("INFO","FAILED to navigate to my Playlists")
            return False
         
        tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
        if self.click(tmp_playlist_name) == False:
            writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
            return False        
        
        return True
    
    
    # @Author: Ori Flchtman
    # Add Entry from My Media to Several Playlists
    # ! TODO: toCreateNewPlaylist - need to implement create new playlist if needed.
    def addSingleEntryToMultiplePlaylists(self, entryName, playlistsName='', toCreateNewPlaylist = False, currentLocation = enums.Location.MY_MEDIA):
        try:
            if currentLocation == enums.Location.MY_MEDIA: 
                if self.clsCommon.myMedia.navigateToMyMedia() == False:
                    writeToLog("INFO","FAILED to navigate to my media")
                    return False
                
                if type(entryName) is list: 
                    if self.clsCommon.myMedia.checkEntriesInMyMedia(entryName) == False:
                        writeToLog("INFO","FAILED to check entries in My-Media")
                        return False
                else: 
                    if self.clsCommon.myMedia.serachAndCheckSingleEntryInMyMedia(entryName) == False:
                        writeToLog("INFO","FAILED to check entry '" + entryName + "' check box")
                        return False
             
                if self.clsCommon.myMedia.clickActionsAndAddToPlaylistFromMyMedia() == False:
                    writeToLog("INFO","FAILED to click on action button")
                    return False
                    sleep(7)  
                      
            elif currentLocation == enums.Location.ENTRY_PAGE: 
                sleep(1)
                # Click on action tab
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ACTIONS_DROPDOWNLIST, 30) == False:
                    writeToLog("INFO","FAILED to click on action button in entry page '" + entryName + "'")
                    return False  
                
                sleep(1)
                # Click on publish button
                if self.click(self.clsCommon.entryPage.ENTRY_PAGE_ADDTOPLAYLIST_BUTTON, 30) == False:
                    writeToLog("INFO","FAILED to click on publish button in entry page '" + entryName + "'")
                    return False
            
            else:
                writeToLog("INFO","FAILED, Add entry to playlist: the provided ""currentLocation"" Value is not accepted ")
                return False
            
            for playlist in playlistsName:
                tmp_playlist_name = (self.PLAYLIST_CHECKBOX[0], self.PLAYLIST_CHECKBOX[1].replace('PLAYLIST_NAME', playlist))   
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to Check for playlists, something went wrong")
                    return False
            
            if self.click(self.CREATE_PLAYLIST_SAVE_BUTTON) == False:
                writeToLog("INFO","FAILED to click on create playlist Button")
                return False
            
            self.clsCommon.general.waitForLoaderToDisappear()
            sleep(1)
            
            if self.wait_visible(self.CREATE_PLAYLIST_CONFIRM_MSG, 10) == False:
                writeToLog("INFO","FAILED to add entry: " + entryName + " to Playlists")
                return False
            
            writeToLog("INFO","Entry: '" + entryName + "' added to Playlists")
                                       
        except NoSuchElementException:
            return False
            
        return True
    
    
    # Verify entry is in given playlists, isExpected is for all playlists
    def verifySingleEntryInMultiplePlaylists(self, entryName, playlistsName='', isExpected=True):
        try:                
            if playlistsName != '':
                if self.navigateToMyPlaylists() == False:
                    writeToLog("INFO","FAILED to navigate to my Playlists")
                    return False
            else:
                writeToLog("INFO","FAILED, Not provided acceptable value playlists name")
                return False 
                             
            for playlist in playlistsName:    
                tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlist))
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
                    return False

                sleep(3)# DO NOT REMOVE
                
                # Get playlist list text
                playlist_text = self.wait_element(self.PLAYLIST_TABLE, multipleElements=True).text
                
                # Split playlist text
                playlist_entries_list = playlist_text.split()
                
                # Check that entry displayed just once in playlist
                numberOfDisplay = playlist_entries_list.count(entryName)
                if numberOfDisplay == 1:
                    if isExpected == True:
                        writeToLog("INFO","As Expected: Entry was found in the Playlists")
                    else:
                        writeToLog("INFO","NOT Expected: Entry was found " + str(numberOfDisplay) + " in the Playlists")
                        return False
                else:
                    if isExpected == False:
                        writeToLog("INFO","As Expected: Entry was not found in the Playlists")
                    else:
                        writeToLog("INFO","NOT Expected: Entry was " + str(numberOfDisplay) + " found in the Playlists")
                        return False                    
               
            return True   
        except NoSuchElementException:
            return False
            
        return True
    
    # @Author: Inbar Willman
    # Verify multiple entries in single playlist
    def verifyMultipleEntriesInPlaylist(self, playlistName, entriesList, isExpected=True):
        try:                
            if playlistName != '':
                if self.navigateToMyPlaylists() == False:
                    writeToLog("INFO","FAILED to navigate to my Playlists")
                    return False
                 
                tmp_playlist_name = (self.PLAYLIST_NAME[0], self.PLAYLIST_NAME[1].replace('PLAYLIST_NAME', playlistName))
                if self.click(tmp_playlist_name) == False:
                    writeToLog("INFO","FAILED to click on playlist name (at my playlist page)")
                    return False

                # Get playlist list text
                playlist_text= self.get_element_text(self.PLAYLIST_TABLE)
                
                # Split playlist text
                playlist_entries_list = playlist_text.split()
                
                # Check that each entry displayed in playlist and just once
                for entry in entriesList:
                    numberOfDisplay = playlist_entries_list.count(entry)
                    if numberOfDisplay == 1:
                        if isExpected == True:
                            writeToLog("INFO","As Expected: Entry " + entry + " was found in the Playlists")
                        else:
                            writeToLog("INFO","NOT Expected: Entry " + entry + "  was found " + str(numberOfDisplay) + " in the Playlists")
                            return False
                    else:
                        if isExpected == False:
                            writeToLog("INFO","As Expected: Entry " + entry + "  was not found in the Playlists")
                        else:
                            writeToLog("INFO","NOT Expected: Entry " + entry + "  was " + str(numberOfDisplay) + " found in the Playlists")
                            return False                    
            else:
                writeToLog("INFO","FAILED, Not provided acceptable value playlistName")
                return False                
                
        except NoSuchElementException:
            return False
            
        return True
    
    
    # @Author:Inbar Willman
    # Delete nultiple playlist
    def deleteMultiplePlaylists(self, playlistList):
        for playlist in playlistList:
            if self.deletePlaylist(playlist) == False:
                writeToLog("INFO","FAILED to delete:" + playlist)
                return False  
               
        return True          