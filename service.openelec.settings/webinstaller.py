import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,binascii,shutil
#import utils
#import socket, fcntl, struct
import downloader
import extract

ADDON = xbmcaddon.Addon(id='plugin.program.webinstaller')
AddonID      =  'plugin.program.webinstaller'
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
restore_dir  = '/storage/.restore'
backup_dir   = '/storage/backup/'
path         =  xbmc.translatePath(os.path.join('special://home/addons','packages'))

#def GetMac():
#        mac=xbmc.getInfoLabel("Network.MacAddress")
#        print "MAC: "+str(mac)
#        if mac=="Busy":
#            xbmc.sleep(100)
#            mac=xbmc.getInfoLabel("Network.MacAddress")
#            GetMac()
    # eno = getHwAddr('en0')
    # print"en0: "+eno
    # etho = getHwAddr('eth0')
    # print"eth0: "+etho
    # wlan = getHwAddr('wlan0')
    # print"wlan: "+wlan
                 
      
def KEYWORD_SEARCH():
        count = len(sys.argv) - 1
        if count > 0:
            url=str(sys.argv[0].join(sys.argv[1:]))
        downloadurl=''
        if url == 'url_installer':
            title='Enter URL'
        else:
            title='Enter Keyword'
        keyword      =  SEARCH(title)
        if url=='trkey':
            downloadurl ='http://bit.ly/TotalRev'+keyword
        if url=='tlbbkey':
            downloadurl ='http://bit.ly/tlbb'+keyword
        if url=='armadakey':
            downloadurl ='http://urlshortbot.com/cloudword'+keyword
        lib          =  os.path.join(path, keyword+'.zip')
        addonfolder  =  xbmc.translatePath(os.path.join('special://home',''))
        if keyword !='':
            try:
                dp.create("Web Installer","Downloading ",'', 'Please Wait')
                downloader.download(downloadurl,lib)
                dp.update(0,"", "Extracting Zip Please Wait")
                extract.all(lib,addonfolder,dp)
                xbmc.executebuiltin('UpdateLocalAddons')
                xbmc.executebuiltin( 'UpdateAddonRepos' )
                dialog.ok("Web Installer", "","Content now installed", "")
                dp.close()
            except: xbmcgui.Dialog().ok("Keyword error",'The keyword you typed could not be installed.','Please check the spelling and if you continue to receive','this message it probably means that keyword is no longer available.')
    
    
def SEARCH(title):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, title)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText() .replace(' ','%20')
            if search_entered == None:
                return False          
        return search_entered    

if __name__ == '__main__':
    KEYWORD_SEARCH()
# xbmcplugin.endOfDirectory(int(sys.argv[1]))