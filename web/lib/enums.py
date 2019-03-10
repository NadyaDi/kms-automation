from enum import Enum
#from selectors import PollSelector


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
    BLACKBOARD_ULTRA    = 'Black Board ultra'


class ChannelPrivacyType(Enum):
    def __str__(self):
        return str(self.value)

    OPEN                = 'open'       
    RESTRICTED          = "restricted"
    PRIVATE             = "private"
    SHAREDREPOSITORY    = "sharedrepository"
    PUBLIC              = "public"
    UNLISTED            = "Unlisted"
    
class PlayerObjects(Enum):
    def __str__(self):
        return str(self.value)

    QR                = 'QR code'
    CAPTIONS          = 'Caption'            
  
    
class QuizQuestionType(Enum):
    def __str__(self):
        return str(self.value)

    Multiple            = 'Multiple Choice'       
    TRUE_FALSE          = "True/False"
    REFLECTION          = "Reflection Point"
    
    
class DisclaimerDisplayArea(Enum):
    def __str__(self):
        return str(self.value)

    BEFORE_UPLOAD        = 'Before Upload'       
    BEFORE_PUBLISH       = 'Before Publish'


class Location(Enum):
    def __str__(self):
        return str(self.value)
    
    MY_MEDIA                    = 'my media'
    ENTRY_PAGE                  = 'entry page'
    UPLOAD_PAGE                 = 'upload page'
    CHANNEL_PAGE                = 'channel page'
    CATEGORY_PAGE               = 'category page'
    MY_CHANNELS_PAGE            = 'my channels page'
    CHANNELS_PAGE               = 'channels page'
    MY_PLAYLISTS                = 'my playlists'
    EDIT_ENTRY_PAGE             = 'edit entry page'
    MY_HISTORY                  = 'my history'
    PENDING_TAB                 = 'channel - Pending tab' 
    HOME                        = 'home'
    CHANNEL_PLAYLIST            = 'channel playlist'
    ADD_TO_CHANNEL_MY_MEDIA     = 'Add to channel My Media'
    ADD_TO_CHANNEL_SR           = 'Add to channel SR'
    EDITOR_PAGE                 = 'Editor page'
    PENDING_TAB_CATEGORY        = 'category - Pending tab'
    MEDIA_GALLARY               = 'channel page'
    SHARED_REPOSITORY           = 'Shared Repository'
    UPLOAD_PAGE_EMBED           = 'Upload page embed'
    GALLERY_PAGE                = 'Gallery Page'
    KEA_PAGE                    = "KEA PAGE"


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
      
    DEFAULT                                 = 'DEFAULT'
    PLAYER                                  = 'PLAYER'
    KEA                                     = 'KEA'
    KEA_QUIZ_PLAYER                         = 'KEA_QUIZ_PLAYER'
    KEA_QUIZ_BLANK                          = 'KEA_BLANK'
    KEA_PREVIEW_PLAYER                      = 'KEA_PREVIEW_PLAYER'
    EMBED_PLAYER                            = 'EMBED_PLAYER'
    KAF_BLACKBOARD                          = 'KAF_BLACKBOARD'
    KAF_BLACKBOARD_EMBED_KALTURA_MEDIA      = 'KAF_BLACKBOARD_EMBED_KALTURA_MEDIA'
    KAF_SHAREPOINT                          = 'KAF_SHAREPOINT'
    KAF_MOODLE                              = 'KAF_MOODLE'
    KAF_CANVAS                              = 'KAF_CANVAS'
    KAF_D2L                                 = 'KAF_D2L'
    KAF_JIVE                                = 'KAF_JIVE'
    KAF_SAKAI                               = 'KAF_SAKAI'
    KAF_BLACKBOARD_ULTRA                    = 'KAF_BLACKBOARD_ULTRA'

    
    
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

    MOST_RECENT             = 'Creation Date' # Changed from 'Most Recent' 
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
    UPDATE_ASC              = 'Update Date - Ascending'
    UPDATE_DESC             = 'Update Date - Descending'
    
class MediaType(Enum):
    def __str__(self):
        return str(self.value)

    ALL_MEDIA               = 'All Media'  
    VIDEO                   = 'Video'      
    QUIZ                    = "Quiz"
    AUDIO                   = "Audio"
    IMAGE                   = "Image" 
    WEBCAST_EVENTS          = "Webcast Events"
    
    
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


class Captions(Enum):
    def __str__(self):
        return str(self.value)

    ALL                     = "All"  
    AVAILABLE               = "Available"      
    NOT_AVAILABLE           = "Not Available"  
    
class Duration(Enum):
    def __str__(self):
        return str(self.value)

    ANY_DURATION             = "Any Duration"  
    TEN_MINUTES              = "00:00-10:00 min"      
    THIRTY_MINUTES           = "10:00-30:00 min"
    SIXTY_MINUTES            = "30:00-60:00 min"      
    CUSTOM                   = "Custom"
    
    
class Creation(Enum):
    def __str__(self):
        return str(self.value)

    ANY_DATE          = "Any Date"  
    LAST_SEVEN        = "Last 7 days"      
    LAST_THIRTY       = "Last 30 days"
    CUSTOM            = "Custom"      
    
    
class SortAndFilter(Enum):
    def __str__(self):
        return str(self.value)

    SORT_BY                   = 'Sort by'  
    PRIVACY                   = 'Privacy Type'      
    MEDIA_TYPE                = "MediaType"
    COLLABORATION             = "Collaboration"
    SCHEDULING                = 'Scheduling'
    CAPTIONS                  = 'Captions'
    DURATION                  = 'Duration'
    CREATION_DATE             = 'Creation Date'
    PUBLISH_STATUS            = 'Publish Status'
    SINGLE_LIST               = 'Single Text selected list' 
    SINGLE_DATE               = 'Single Date'
    FREE_TEXT                 = 'Free Text'
    OWNERSHIP                 = 'Ownership'
    CHANNEL_MEMBERSHIP        = 'Channel Membership'
    

class KeaQuizButtons(Enum):
    def __str__(self):
        return str(self.value)

    SAVE                       = 'Save'  
    DELETE                     = 'Delete'      
    START                      = 'Start'
    DONE                       = 'Done'
    GO_TO_MEDIA_PAGE           = 'Go to Media Page'
    EDIT_QUIZ                  = 'Edit Quiz'
    APPLY                      = 'Apply'

    
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

    CREATION_DATE             = 'Creation Date' # Changed from 'Most Recent'   
    ALPHABETICAL_NEWUI        = "Alphabetically - A to Z" # "Alphabetically A-Z"
    ALPHABETICAL_OLDUI        = "Alphabetical"
    MEMBERS_AND_SUBSCRIBERS   = "Members & Subscribers"
    MEDIA_COUNT               = "Media Count"
    ALPHABETICAL_Z_A_NEWUI    = "Alphabetically - Z to A" #"Alphabetically Z-A"
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
    
    
class CustomdataType(Enum):
    def __str__(self):
        return str(self.value)
    
    TEXT_SINGLE                 = 'Text Single'
    DATE                        = 'Date'
    TEXT_UNLIMITED              = 'Text Unlimited'
    LIST                        = 'List'    
    
    
class SearchInDropDown(Enum):
    def __str__(self):
        return str(self.value)
    
    ALL_FIELDS                 = 'All Fields'
    DETAILS                    = 'Details'
    CHAPTERS_AND_SLIDES        = 'Chapters/Slides'
    CAPTIONS                   = 'Captions'    
    POLLS                      = 'Polls'             
    QUIZ                       = 'Quiz'
    COMMENTS                   = 'Comments'
    
    
class EntryFields(Enum):
    def __str__(self):
        return str(self.value)
    
    DETAILS                    = 'Details'
    CHAPTER                    = 'Chapter'
    CHAPTERS                   = 'Chapters'
    SLIDE                      = 'Slide'
    SLIDES                     = 'Slides'
    TAG                        = 'Tag'
    TAGS                       = 'Tags'
    QUIZ                       = 'Quiz'
    COMMENT                    = 'Comment'
    COMMENTS                   = 'Comments'
    POLL                       = 'Poll'
    POLLS                      = 'Polls'
    CAPTION                    = 'Caption'
    CAPTIONS                   = 'Captions'
    
    
class BBCoursePages(Enum):
    def __str__(self):
        return str(self.value)    
    
    HOME_PAGE                 = 'Home Page'
    CONTENT                   = 'Content'
    
    
class BBContentPageMenus(Enum):
    def __str__(self):
        return str(self.value)  
    
    BUILD_CONTENT             = 'Build Content' 
    ASSESSMENTS               = 'Assessments'   
    TOOLS                     = 'Tools'
    
    
class BBContentPageMenusOptions(Enum):
    def __str__(self):
        return str(self.value)     
    
    ITEM                      = 'Item'
    FILE                      = 'File'
    KALTURA_MEDIA             = 'Kaltura Media' 
    MORE_TOOLS                = 'More Tools'
    ANNOUNCEMENTS             = 'Announcements' 
    KALTURA_VIDEO_QUIZ        = 'Kaltura Video Quiz'
    

class SingleList(Enum):
    def __str__(self):
        return str(self.value)

    LIST_ONE           = "Search in - One"  
    LIST_TWO           = "Search in - Two"  
    LIST_THREE         = "Search in - Three"  
    LIST_FOUR          = "Search in - Four"  
    LIST_FIVE          = "Search in - Five"  
    LIST_SIX           = "Search in - Six"
    
    
class SingleDate(Enum):
    def __str__(self):
        return str(self.value)

    DATE           = "Single Date"  
    

class FreeText(Enum):
    def __str__(self):
        return str(self.value)

    SINGLE_TEXT           = "SIngle Text" 
    UNLIMITED_TEXT        = "Unlimited Text" 

    
class MoodleActivities(Enum):
    def __str__(self):
        return str(self.value)   
    
    KALTURA_VIDEO_RESOURCE    = 'Kaltura Video Resource'    
    SITE_BLOG                 = 'Site blog'
    EXTERNAL_TOOL             = 'External Tool'
    
    
class Ownership(Enum):
    def __str__(self):
        return str(self.value)

    ANY_OWNER          = "Any Owner"
    MEDIA_OWN          = "Media I Own" 
    MEDIA_EDIT         = "Media I Can Edit" 
    MEDIA_PUBLISH      = "Media I Can Publish"     
    

class PendingModerateAction(Enum):
    def __str__(self):
        return str(self.value)

    REJECT           = "Reject"
    APPROVE          = "Approve" 
    
    
class KEAQuizSection(Enum):
    def __str__(self):
        return str(self.value)

    DETAILS           = "Details"
    SCORES            = "Scores"
    EXPERIENCE        = "Experience"
    
    
class KEAQuizOptions(Enum):
    def __str__(self):
        return str(self.value)

    QUIZ_NAME           = "Quiz Name"
    SHOW_WELCOME_PAGE   = "Show Welcome Page"
    ALLOW_DOWNLOAD      = "Allow Download of Questions List"
    INSTRUCTIONS        = "Instructions" 
    DO_NOT_SHOW_SCORES  = "Do Not Show Scores"
    SHOW_SCORES         = "Show Scores"
    INCLUDE_ANSWERS     = "Include Answers"
    ALLOW_ANSWER_CHANGE = "Allow Answers Change"
    ALLOW_SKIP          = "Allow Skip"
    DO_NOT_ALLOW_SKIP   = "Do not Allow Skip"
    NO_SEEKING_FORWARD  = "No seeking forward"
    
    
class KAFGradebookGradeOptions(Enum):
    def __str__(self):
        return str(self.value)
    
    PERCENTAGE            = 'Percentage'
    COMPLETE_INCOMPLETE   = 'Complete Incomplete'
    LETTER                = 'Letter'
    SCORE                 = 'Score'
    TEXT                  = 'Text' 
    
    
class RecschedulingResourceOptions(Enum):
    def __str__(self):
        return str(self.value)
    
    MAIN_AUDITORIUM             = 'Main Auditorium'
    MAIN_CONFERENCE_ROOM        = 'Main Conference Room'
    AUTOMATION_ROOM             = 'Automation Room'
    SUMMER_CONFERENCE_ROOM      = 'Summer Conference Room'
    FALL_CONFERENCE_ROOM        = 'Fall Conference Room' 
    MAIN_STUDENT_LOUNGE         = 'Main Student Lounge'
    QA_APP_ROOM                 = 'Qa App Room'
    

class scheduleRecurrenceInterval(Enum):
    def __str__(self):
        return str(self.value)
    
    NONE            = 'none'
    DAYS            = 'days'
    WEEKS           = 'weeks'
    MONTHS          = 'months'


class scheduleRecurrenceDailyOption(Enum):
    def __str__(self):
        return str(self.value)
    
    EVERY_X_DAYS     = 'none'
    EVERY_WEEKDAY    = 'Every Weekday'
    

class scheduleRecurrenceMonthlyOption(Enum):
    def __str__(self):
        return str(self.value)
    
    DAY_X_OF_EVERY_Y_MONTHS     = 'day x of every y months'
    BY_WEEKDAY                  = 'by weekday'


class scheduleRecurrenceDayOfTheWeek(Enum):
    def __str__(self):
        return str(self.value)
    
    SUNDAY              = 'Sunday'
    MONDAY              = 'Monday'
    TUESDAY             = 'Tuesday'
    WEDNESDAY           = 'Wednesday'
    THURSDAY            = 'Thursday'
    FRIDAY              = 'Friday'
    SATURDAY            = 'Saturday'
    SUNDAY_SHORT        = 'SU'
    MONDAY_SHORT        = 'MO'
    TUESDAY_SHORT       = 'TU'
    WEDNESDAY_SHORT     = 'WE'
    THURSDAY_SHORT      = 'TH'
    FRIDAY_SHORT        = 'FR'
    SATURDAY_SHORT      = 'SA'
    
    
class scheduleRecurrenceEndDateOption(Enum):
    def __str__(self):
        return str(self.value)
    
    END_AFTER_X_OCCURRENCES     = 'endAfter'
    END_BY                      = 'endBy'


class scheduleRecurrenceMonthlyIndex(Enum):
    def __str__(self):
        return str(self.value)
    
    first           = 'first'
    second          = 'second'
    third           = 'third'
    fourth          = 'fourth'
    last            = 'last'
