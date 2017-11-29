from urllib.parse import urlencode
from urllib.request import Request, urlopen
from localSettings import *
from logger import *
from utilityTestFunc import *
import xml.etree.ElementTree as ET

#============================================================================================================
#The class contains functions that relates to backend API
#============================================================================================================

class clsBackendAPI:
    
    #============================================================================================================
    # Function that request a new ks from backend web api
    #============================================================================================================
    
    def getKS(self):

        getKSURL        = LOCAL_SETTINGS_QA_BACKEND_API_URL + '/api_v3/?service=session&action=start' 
        getKSPostFields = {
                            'secret'     : LOCAL_SETTINGS_PARTNER_SECRET, 
                            'partnerId'  : LOCAL_SETTINGS_PARTNER,
                            'type'       : LOCAL_SETTINGS_KS_TYPE
                           }     
        try:
            ksRequest  = Request(getKSURL, urlencode(getKSPostFields).encode())
            ksResponse = urlopen(ksRequest).read().decode()
            rootXMLResponse = ET.fromstring(ksResponse)
            ks = rootXMLResponse[0].text
        except Exception as inst:
            writeToLog("INFO","Failed to produce KS, exception thrown")  
            raise

        return ks

    #============================================================================================================
    # Function that updates the HTML5 path of the player to a specific release
    #============================================================================================================
    
    def updateUIConfhtml5Url(self,ks,uiConfList,html5Url):

        uiConfPath = "/html5/html5lib/" + html5Url + "/mwEmbedLoader.php"
        updateUIConfURL = LOCAL_SETTINGS_QA_BACKEND_API_URL + '/api_v3/'
        
        for uiConf in uiConfList:
            updateUIConfPostFields = {
                                      'ks'                  : ks,
                                      'id'                  : uiConf,
                                      'uiConf:html5Url'     : uiConfPath,
                                      'uiConf:objectType'   : 'KalturaUiConf',
                                      'service'             : 'uiConf',
                                      'action'              : 'update'
                                      }
            try:     
                updateUIConfRequest    = Request(updateUIConfURL, urlencode(updateUIConfPostFields).encode())
                updateUIConfksResponse = urlopen(updateUIConfRequest).read().decode()
                rootXMLResponse = ET.fromstring(updateUIConfksResponse)
                found = False
                for child in rootXMLResponse[0]:
                    if (child.tag == "html5Url"):
                        found = True
                        if (child.text == uiConfPath): 
                            writeToLog("INFO","Updated uiConf " + uiConf + " html5Url to : " + html5Url)                           
                        else:
                            writeToLog("INFO","Failed to update uiConf html5Url, html5Url is not equal to : " + html5Url + " for uiConf "  + uiConf )
                if (found == False):
                    writeToLog("INFO","Failed to update uiConf html5Url, html5Url wan't found in the response for uiConf "  + uiConf )
                    writeToLog("INFO",updateUIConfksResponse)
                    writeToLog("INFO",ks)
                    writeToLog("INFO",uiConf) 
                    writeToLog("INFO",uiConfPath) 
                    
                    return False
            except Exception as inst:
                writeToLog("INFO","Failed to update uiConf html5Url. Exception thrown for uiConf "  + uiConf )
                raise
            time.sleep(1)
                                
        return True
        

