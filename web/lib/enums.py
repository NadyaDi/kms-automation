from enum import Enum


class Application(Enum):
    def __str__(self):
        return str(self.value)

    MEDIA_SPACE         = 'Media Space'
    BLACK_BOARD         = 'Black Board'       
    CANVAS              = 'Canvas'
    MOODLE              = 'Moodle'
    D2L                 = 'D2L'
    JIVE                = 'Jive'
    SHARE_POINT         = 'Share Point'
    SAKAI               = 'Sakai'


class ChannelPrivacyType(Enum):
    def __str__(self):
        return str(self.value)

    OPEN                = 'open'       
    RESTRICTED          = "restricted"
    PRIVATE             = "private"
    SHAREDREPOSITORY    = "sharedrepository"
    PUBLIC              = "public"
    UNLISTED            = "Unlisted"
    
    
class DisclaimerDisplayArea(Enum):
    def __str__(self):
        return str(self.value)

    BEFORE_UPLOAD        = 'Before Upload'       
    BEFORE_PUBLISH       = 'Before Publish'


class Location(Enum):
    def __str__(self):
        return str(self.value)
    
    MY_MEDIA                = 'my media'
    ENTRY_PAGE              = 'entry page'
    UPLOAD_PAGE             = 'upload page'
    CHANNEL_PAGE            = 'channel page'
    CATEGORY_PAGE           = 'category page'
    MY_CHANNELS_PAGE        = 'my channels page'
    CHANNELS_PAGE           = 'channels page'
    MY_PLAYLISTS            = 'my playlists'
    EDIT_ENTRY_PAGE         = 'edit entry page'
    MY_HISTORY              = 'my history'
    PENDING_TAB             = 'channel - Pending tab' 
    HOME                    = 'home'
    CHANNEL_PLAYLIST        = 'channel playlist'
    ADD_TO_CHANNEL_MY_MEDIA = 'Add to channel My Media'
    ADD_TO_CHANNEL_SR       = 'Add to channel SR'
    EDITOR_PAGE             = ('Editor page') 


class EditEntryPageTabName(Enum):
    def __str__(self):
        return str(self.value)
    
    
    DETAILS                = 'details'
    OPTIONS                = 'options'
    COLLABORATION          = 'collaboration'
    THUMBNAILS             = 'thumbnails'
    CAPTIONS               = 'captions'
    DOWNLOADS              = 'downloads'
    TIMELINE               = 'timeline'
    REPLACE_VIDEO          = 'replace video'
    ATTACHMENTS            = 'Attachments'
    
    
class IframeName(Enum):
    def __str__(self):
        return str(self.value)

    DEFAULT                             = 'DEFAULT'
    PLAYER                              = 'PLAYER'
    KEA                                 = 'KEA'
    KEA_QUIZ_PLAYER                     = 'KEA_QUIZ_PLAYER'
    EMBED_PLAYER                        = 'EMBED_PLAYER'
    KAF_BLACKBOARD                      = 'KAF_BLACKBOARD'
    KAF_SHAREPOINT                      = 'KAF_SHAREPOINT'
    
    
class PlayerView(Enum):
    def __str__(self):
        return str(self.value)
    
    PIP                = 'pip'
    SIDEBYSIDE         = 'sideBySide' 
    SINGLEVIEW         = 'singleView'
    SWITCHVIEW         = 'switchView'
    
    
class EntryPrivacyType(Enum):
    def __str__(self):
        return str(self.value)
    
    ALL_STATUSSES      = 'All Statuses'
    PRIVATE            = 'Private'       
    UNLISTED           = "Unlisted"
    PUBLISHED          = "Published"
    PENDING            = "Pending"
    REJECTED           = "Rejected"
    
    
class SortBy(Enum):
    def __str__(self):
        return str(self.value)

    MOST_RECENT             = 'Most Recent'  
    VIEWS                   = 'Views'
    LIKES                   = 'Likes'
    ALPHABETICAL            = "Alphabetically - A to Z"
    ALPHABETICAL_Z_A        = "Alphabetically - Z to A"
    COMMENTS                = "Comments"
    SCHEDULING_ASC          = "Scheduling Ascending"
    SCHEDULING_DESC         = "Scheduling Descending" 
    CREATION_DATE_DESC      = "Creation Date - Descending"
    CREATION_DATE_ASC       = "Creation Date - Ascending"
    PLAYS                   = "Plays"
    RELEVANCE               = 'Relevance'
    
class MediaType(Enum):
    def __str__(self):
        return str(self.value)

    ALL_MEDIA               = 'All Media'  
    VIDEO                   = 'Video'      
    QUIZ                    = "Quiz"
    AUDIO                   = "Audio"
    IMAGE                   = "Image"
    
    
class Collaboration(Enum):
    def __str__(self):
        return str(self.value)

    MEDIA_I_OWN               = 'Media I Own'  
    CO_PUBLISH                = 'Media I Can Publish'      
    CO_EDIT                   = "Media I Can Edit"
    
    
class Scheduling(Enum):
    def __str__(self):
        return str(self.value)

    ALL                       = 'All Availabilities'  
    FUTURE_SCHEDULING         = 'Future Scheduling'      
    AVAILABLE_NOW             = "Available Now"
    PAST_SCHEDULING           = "Past Scheduling" 


class SortAndFilter(Enum):
    def __str__(self):
        return str(self.value)

    SORT_BY                   = 'Sort by'  
    PRIVACY                   = 'Privacy Type'      
    MEDIA_TYPE                = "MediaType"
    COLLABORATION             = "Collaboration"
    SCHEDULING                = 'Scheduling'
    

class KeaQuizButtons(Enum):
    def __str__(self):
        return str(self.value)

    SAVE                       = 'Save'  
    DELETE                     = 'Delete'      
    START                      = 'Start'
    DONE                       = 'Done'
    GO_TO_MEDIA_PAGE           = 'Go to Media Page'
    EDIT_QUIZ                  = 'Edit Quiz'

    
class PlayerPart(Enum):
    def __str__(self):
        return str(self.value)

    TOP                       = 'top'  
    BOTTOM                    = 'bottom'
    

class ProgressBarStatus(Enum):
    def __str__(self):
        return str(self.value)
    
    COMPLETE                  = 'Complete'  
    STARTED                   = 'Started'


class EntryPageShareOptions(Enum):
    def __str__(self):
        return str(self.value)
    
    LINK_TO_MEDIA_PAGE      = 'Link to Media Page'  
    EMBED                   = 'Embed'
    EMAIL                   = 'Email'
    

class ChannelMemberPermission(Enum):
    def __str__(self):
        return str(self.value)
    
    MEMBER                  = 'Member'
    CONTRIBUTOR             = 'Contributor'   
    MODERATOR               = 'Moderator'
    MANAGER                 = 'Manager'
    
    
class CategoryMemberPermission(Enum):
    def __str__(self):
        return str(self.value)
    
    MEMBER                  = 'Member'
    CONTRIBUTOR             = 'Contributor'   
    MODERATOR               = 'Moderator'
    MANAGER                 = 'Manager'
    

class ReleatedMedia(Enum):
    def __str__(self):
        return str(self.value)
    
    MY_MEDIA               = 'My Media'
    RELATED_MEDIA          = 'Related Media'  
    
    
class MyMediaView(Enum):
    def __str__(self):
        return str(self.value)
    
    COLLAPSED               = 'collapsed'
    DETAILED                = 'detailed'   
    
    
class ChannelsSortByMembership(Enum):
    def __str__(self):
        return str(self.value)
    
    MANAGER_NEWUI               = 'Manager'
    MEMBER_NEWUI                = 'Member' 
    SUBSCRIBER_NEWUI            = 'Subscriber'
    SHAREDREPOSITORIES_NEWUI    = 'Shared Repositories'
    MANAGER_OLDUI               = ' I Manage'
    MEMBER_OLDUI                = ' I am a member of' 
    SUBSCRIBER_OLDUI            = ' I am subscribed to'
    SHAREDREPOSITORIES_OLDUI    = 'Shared Repositories I am a member of'  
    
class ChannelsSortBy(Enum):
    def __str__(self):
        return str(self.value)

    MOST_RECENT               = 'Most Recent'  
    ALPHABETICAL_NEWUI        = "Alphabetical A-Z"
    ALPHABETICAL_OLDUI        = "Alphabetical"
    MEMBERS_AND_SUBSCRIBERS   = "Members & Subscribers"
    MEDIA_COUNT_NEWUI         = "Media count"
    MEDIA_COUNT_OLDUI         = "Media Count"
    ALPHABETICAL_Z_A_NEWUI    = "Alphabetical Z-A"
    RELEVANCE                 = 'Relevance'

class MyHistoryFilters(Enum):
    def __str__(self):
        return str(self.value)
    
    MEDIA_TYPE                = "type-menu"
    WATCH_STATUS_MENU         = "watch-status-menu"
    TIME_MENU                 = "time-menu"
    
class MyHistoryWatcheStatusItems(Enum):
    def __str__(self):
        return str(self.value)
    
    ALL_HISTORY                = "All History"
    COMPLETED_WATCHING         = "Completed Watching"
    STARTED_WATCHING           = "Started Watching"
    
class MyHistoryTimeItems(Enum):
    def __str__(self):
        return str(self.value)
    
    ALL_TIME                   = "All Time"
    LAST_7_DAYS                = "Last 7 Days"
    LAST_30_DAYS               = "Last 30 Days"
    CUSTOM                     = "Custom"    
    
class DepartmentDivision(Enum):
    def __str__(self):
        return str(self.value)
    
    MARKETING                  = "Marketing"
    PRODUCT                    = "Product"
    ENGINEERING                = "Engineering"
    FINANCE                    = "FInance"      
    SALES                      = "Sales"   
    HR                         = "HR"  
    MANAGMENT                  = "Management"  
    
class AddToChannelTabs(Enum):
    def __str__(self):
        return str(self.value)
    
    MY_MEDIA                   = 'My Media'
    SHARED_REPOSITORY          = 'Shared Repository'  
    
class NavigationStyle(Enum):
    def __str__(self):
        return str(self.value)
    
    HORIZONTAL                 = 'Horizontal'
    VERTICAL                   = 'Vertical' 
    
class NavigationPrePost(Enum):
    def __str__(self):
        return str(self.value)
    
    PRE                         = 'pre'
    POST                        = 'post'   
    
class SameWindowPrePost(Enum):
    def __str__(self):
        return str(self.value)
    
    YES                         = 'Yes'
    NO                          = 'No'   