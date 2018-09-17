from KalturaClient import *
from KalturaClient.Plugins.Core import KalturaSessionType, KalturaCategory, \
    KalturaPrivacyType, KalturaNullableBoolean, KalturaAppearInListType, \
    KalturaInheritanceType, KalturaCategoryUserPermissionLevel, \
    KalturaCategoryFilter,KalturaContributionPolicyType, KalturaAppearInListType

from utilityTestFunc import *

# This is class for KALTURA API
# Before use call for self.common.apiClientSession.startCurrentApiClientSession() to start session of current (under test) partner
# Or call startApiClientSession(partnerId, dcUrl, secret) for specific partner


class ApiClientSession:
    driver      = None
    clsCommon   = None
    client      = None
          
    def __init__(self, clsCommon, driver):
        self.driver = driver
        self.clsCommon = clsCommon
            
            
    def startApiClientSession(self, partnerId, dcUrl, secret, userId=None, impersonateID=None):
        self.partnerId = partnerId
        self.dcUrl = dcUrl
        self.secret = secret
        self.userId= userId
        self.impersonateID = impersonateID
        if self.client == None:
            self.client = self.openSession(None,None,"all:*,disableentitlement")
            if self.client == False:
                return False
        return True
        
            
    def startCurrentApiClientSession(self):
        # Get Partner Details from partnerDetails.csv file: partnerId,serverUrl,adminSecret
        serverUrl,adminSecret = getPartnerDetails(localSettings.LOCAL_SETTINGS_PARTNER)
        if serverUrl == None or adminSecret == None:
            writeToLog("INFO","FAILED to get partner details: service URL and Admin Secret")
            return False
        if self.startApiClientSession(localSettings.LOCAL_SETTINGS_PARTNER, serverUrl, adminSecret) == False:
            writeToLog("INFO","FAILED to start KALTURA API client session")
            return False
        return True
        
    
    def getKs(self,userType=2, privileges=None, userId=None):
        config = KalturaConfiguration(self.partnerId)
        if userId==None:
            userId = self.userId
        config.serviceUrl = self.dcUrl
        #=======================================================================
        # config.logger = self.logger
        #=======================================================================
        client = KalturaClient(config)
        result = client.session.start(self.secret, userId, userType, self.partnerId, None, privileges)
        if self.impersonateID != None:
            client.setPartnerId(self.impersonateID)
        
        dictKs = {1:client,2:result}
        return dictKs
    
    
    #Open a session
    def openSession(self, userID=None, userType=None, privileges=None):
        if userType!=None:
            dictKs = self.getKs(userType,privileges,userID)
        else:
            dictKs = self.getKs(2, privileges, userID)
        try:
            dictKs[1].setKs(dictKs[2])
        except Exception as exp:
            return False
            
        return dictKs[1]
    
    
    def startSession(self,privileges='scenario_default:* privileges',userType=0):
        userTypeDict = {0:KalturaSessionType.USER,
                        1: KalturaSessionType.ADMIN}
        
        config = KalturaConfiguration(self.partnerId)
        config.serviceUrl = self.dcUrl
        client = KalturaClient(config)
        userType = userTypeDict[userType]
        userId = None
        expiry = None
        return client.session.start(self.secret, userId, userType, self.partnerId, expiry, privileges)
 
 
        class CategoryApi:
            def __init__(self, publisherID, serverURL , userSecret):
                mySess = ApiClientSession(publisherID, serverURL, userSecret)
                self.client = mySess.openSession(None,None,"all:*,disableentitlement")


################################################# CATEGORY METHODS ############################################################
# Flow example for create and delete category:
#             startApiClientSession(self, partnerId, dcUrl, secret, userId=None, impersonateID=None):
#             parentId = self.common.apiClientSession.getParentId('galleries')
#             self.common.apiClientSession.createCategory(parentId, 'python_automation', 'testCategory', 'description', 'tags')
#             self.common.apiClientSession.deleteCategory('testCategory')
###############################################################################################################################        
    def createCategoryApi(self, client, parentId, owner, name, description=None, tags=None, privacy=KalturaPrivacyType.ALL, addContentToCategory= KalturaContributionPolicyType.ALL, whoCanSeeTheCategory=KalturaAppearInListType.PARTNER_ONLY):
        category = KalturaCategory()
        category.parentId = parentId
        category.name = name
        category.description = description
        category.tags = tags
        category.owner = owner
        
        category.privacy = privacy
        category.moderation = KalturaNullableBoolean.FALSE_VALUE
        category.appearInList = KalturaAppearInListType.PARTNER_ONLY
        category.privacyContext = "public"
        category.inheritanceType = KalturaInheritanceType.MANUAL
        category.defaultPermissionLevel =  KalturaCategoryUserPermissionLevel.MANAGER
        category.defaultOrderBy = None
        category.contributionPolicy = addContentToCategory
        category.appearInList = whoCanSeeTheCategory
        
        try:
            result = client.category.add(category)
        except Exception as exp:
            if "DUPLICATE_CATEGORY" in str(exp):
                print("DUPLICATE_CATEGORY")
                return -1
                    
        return result.id
                   
                                
    def getCategoryByName(self, catName):
        filter = KalturaCategoryFilter()
        filter.nameOrReferenceIdStartsWith = catName
        pager = None
        try:
            result = self.client.category.list(filter, pager)
            
        except Exception as exp:
            print(exp)
            result = -1
        
        if len(result.objects) == 0:
            writeToLog("INFO","No category was found named: " + catName)
            return -1
        else:
            return result.objects[0].id
            
            
    def deleteCategory(self, categoryName):
        moveEntriesToParentCategory = KalturaNullableBoolean.TRUE_VALUE
        categoryId = self.getCategoryByName(categoryName)
        if categoryId != -1:
            try:
                self.client.category.delete(categoryId, moveEntriesToParentCategory)
            except Exception as exp:
                writeToLog("INFO","FAILED to delete category")
                return False
            writeToLog("INFO","Category deleted: " + str(categoryName) + "; ID: " + str(categoryId))
            return True
        else:
            return False
                
                
    def createCategory(self, parentId, owner, name, description, tags, privacy=KalturaPrivacyType.ALL, addContentToCategory= KalturaContributionPolicyType.ALL, whoCanSeeTheCategory=KalturaAppearInListType.PARTNER_ONLY):
        categoryId = self.createCategoryApi(self.client, parentId, owner, name, description, tags, privacy, addContentToCategory, whoCanSeeTheCategory)
        if categoryId == -1:
            writeToLog("INFO","FAILED to create category")
            return False
        else:
            writeToLog("INFO","Category created: " + str(name) + "; ID: " + str(categoryId))
            return True
            
            
    # If parent id not a number, then we got a parent category name, which we need to translate to category ID        
    def getParentId(self, parentId):
        if parentId.isdigit():
            return parentId
        else:
            return self.getCategoryByName(parentId)