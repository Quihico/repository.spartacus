import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, time, xbmcvfs, glob, shutil, datetime, zipfile, ntpath
import subprocess, threading
import yt, downloader, checkPath, SF, clean, TXT, kll
import binascii
import hashlib
import speedtest
import extract
import pyxbmct

try:
    from sqlite3 import dbapi2 as database

except:
    from pysqlite2 import dbapi2 as database

######################################################
# SET THIS TO TRUE TO SEE ALL THE OUTPUT IN THE LOG  #
debug = 'false'
######################################################

AddonID='plugin.program.tbs'
AddonName='Maintenance'
ADDON            =  xbmcaddon.Addon(id=AddonID)
zip              =  ADDON.getSetting('zip')
thirdparty       =  ADDON.getSetting('thirdparty')
localcopy        =  ADDON.getSetting('localcopy')
privatebuilds    =  ADDON.getSetting('private')
reseller         =  ADDON.getSetting('reseller')
openelec         =  ADDON.getSetting('openelec')
I1IiiI           =  ADDON.getSetting('resellername')
IIi1IiiiI1Ii     =  ADDON.getSetting('resellerid')
keepfaves        =  ADDON.getSetting('favourites')
keepsources      =  ADDON.getSetting('sources')
keeprepos        =  ADDON.getSetting('repositories')
enablekeyword    =  ADDON.getSetting('enablekeyword')
keywordpath      =  ADDON.getSetting('keywordpath')
keywordname      =  ADDON.getSetting('keywordname')
mastercopy       =  ADDON.getSetting('mastercopy')
username         =  ADDON.getSetting('username').replace(' ','%20')
password         =  ADDON.getSetting('password')
versionoverride  =  ADDON.getSetting('versionoverride')
addonportal      =  ADDON.getSetting('addonportal')
commbuilds       =  ADDON.getSetting('maintenance')
hardware         =  ADDON.getSetting('hardwareportal')
maintenance      =  ADDON.getSetting('maintenance')
newsportal       =  ADDON.getSetting('latestnews')
tutorials        =  ADDON.getSetting('tutorialportal')
startupvideo     =  ADDON.getSetting('startupvideo')
startupvideopath =  ADDON.getSetting('startupvideopath')
wizard           =  ADDON.getSetting('wizard')
wizardurl1       =  ADDON.getSetting('wizardurl1')
wizardname1      =  ADDON.getSetting('wizardname1')
wizardurl2       =  ADDON.getSetting('wizardurl2')
wizardname2      =  ADDON.getSetting('wizardname2')
wizardurl3       =  ADDON.getSetting('wizardurl3')
wizardname3      =  ADDON.getSetting('wizardname3')
wizardurl4       =  ADDON.getSetting('wizardurl4')
wizardname4      =  ADDON.getSetting('wizardname4')
wizardurl5       =  ADDON.getSetting('wizardurl5')
wizardname5      =  ADDON.getSetting('wizardname5')
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath('special://profile/')
ADDON_DATA       =  os.path.join(USERDATA,'addon_data')
PLAYLISTS        =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
MEDIA            =  xbmc.translatePath(os.path.join(USERDATA,'media'))
DATABASE         =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
CP_PROFILE       =  os.path.join(HOME,'CP_Profiles')
ADDONS_MASTER    =  os.path.join(CP_PROFILE,'Master')
THUMBNAILS       =  os.path.join(USERDATA,'Thumbnails')
ADDONS           =  xbmc.translatePath(os.path.join('special://home','addons'))
KODI_ADDONS      =  xbmc.translatePath(os.path.join('special://xbmc','addons'))
CBADDONPATH      =  os.path.join(ADDONS,AddonID,'default.py')
FANART           =  os.path.join(ADDONS,AddonID,'fanart.jpg')
ADDONXMLTEMP     =  os.path.join(ADDONS,AddonID,'resources','addonxml')
SETTINGSXML      =  os.path.join(ADDONS,AddonID,'service.py')
GUI              =  os.path.join(USERDATA,'guisettings.xml')
GUIFIX           =  os.path.join(USERDATA,'guifix.xml')
ARTPATH          =  '' #Enter URL here for artwork
defaulticon      =  os.path.join(ADDONS,AddonID,'icon_menu.png')
FAVS             =  os.path.join(USERDATA,'favourites.xml')
SOURCE           =  os.path.join(USERDATA,'sources.xml')
ADVANCED         =  os.path.join(USERDATA,'advancedsettings.xml')
PROFILES         =  os.path.join(USERDATA,'profiles.xml')
RSS              =  os.path.join(USERDATA,'RssFeeds.xml')
KEYMAPS          =  os.path.join(USERDATA,'keymaps','keyboard.xml')
USB              =  xbmc.translatePath(os.path.join(zip))
CBPATH           =  os.path.join(USB,'Community_Builds','')
startuppath      =  os.path.join(ADDON_DATA,AddonID,'startup.xml')
tempfile         =  os.path.join(ADDON_DATA,AddonID,'temp.xml')
idfile           =  os.path.join(ADDON_DATA,AddonID,'id.xml')
progresstemp     =  os.path.join(ADDON_DATA,AddonID,'progresstemp')
sleeper          =  os.path.join(ADDONS,AddonID,'resources','tmr')
idfiletemp       =  os.path.join(ADDON_DATA,AddonID,'idtemp.xml')
cookie           =  os.path.join(ADDON_DATA,AddonID,'temp')
ascii_results    =  os.path.join(ADDON_DATA,AddonID,'ascii_results')
ascii_results1   =  os.path.join(ADDON_DATA,AddonID,'ascii_results1')
ascii_results2   =  os.path.join(ADDON_DATA,AddonID,'ascii_results2')
GUIzipfolder     =  os.path.join(ADDON_DATA,AddonID,'guizip')
successtxt       =  os.path.join(ADDON_DATA,AddonID,'successtxt.txt')
notifyart        =  os.path.join(ADDONS,AddonID,'resources/')
installfile      =  os.path.join(ADDONS,AddonID,'default.py')
testmodefile     =  os.path.join(ADDON_DATA,AddonID,'testmode')
skin             =  xbmc.getSkinDir()
log_path         =  xbmc.translatePath('special://logpath/')
backup_dir       =  '/storage/backup'
restore_dir      =  '/storage/.restore/'
CONFIG           =  '/storage/.config/'
STORAGE          =  '/storage/'
userdatafolder   =  os.path.join(ADDON_DATA,AddonID)
GUINEW           =  os.path.join(userdatafolder,'guinew.xml')
guitemp          =  os.path.join(userdatafolder,'guitemp')
scriptfolder     =  os.path.join(ADDON_DATA,AddonID,'scripts')
tempdbpath       =  os.path.join(USB,'Database')
packages         =  os.path.join(ADDONS,'packages')
addonstemp       =  os.path.join(USERDATA,'addontemp')
backupaddonspath =  os.path.join(USERDATA,'.cbcfg')
checkicon        =  os.path.join(ADDONS,AddonID,'resources','tick.png')
codename         =  'Venztech'
keywordpath      =  'http://urlshortbot.com/venztech'
EXCLUDES         =  ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml']
EXCLUDES2        =  ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml','guisettings.xml','CP_Profiles','temp']
max_Bps          =  0.0
downloaded_bytes =  0.0
localversioncheck=  '0'
BACKUP_DIRS      =  ['/storage/.kodi','/storage/.cache','/storage/.config','/storage/.ssh']
sign             =  '1889903'
xbmc_version     =  xbmc.getInfoLabel("System.BuildVersion")
AddonID2         =  'script.trtv'
#ADDON2           =  xbmcaddon.Addon(id=AddonID2)
dialog           =  xbmcgui.Dialog()
updateurl        =  'http://tlbb.me/updates/update.jpeg'
updatedst        =  xbmc.translatePath('special://home/addons/packages/update')
epgurl           =  'http://tlbb.me/updates/epg.jpeg'
epgdst           =  xbmc.translatePath('special://home/addons/packages/epg')
tvguide          =  xbmc.translatePath('special://home/userdata/addon_data/script.trtv.tools/skip.txt')
remlist          =  xbmc.translatePath('special://profile/addon_data/plugin.program.tbs/remlist')
remarray         =  []
pos              =  0
listicon         =  ''
ACTION_NAV_BACK  = 92
ACTION_MOVE_UP   = 3
ACTION_MOVE_DOWN = 4
try:
    avivfile = open(xbmc.translatePath('special://home/userdata/addon_data/plugin.video.tfctv/settings.xml'),'r')
    readfile = avivfile.read()
    avivfile.close()

    if 'aviv4494' in readfile:
        tvgskip = 1
    else:
        tvgskip = 0
except:
        tvgskip = 0
#-----------------------------------------------------------------------------------------------------------------    
def Check_File_Date(url, datefile, localdate, dst):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        conn = urllib2.urlopen(req)
        last_modified = conn.info().getdate('last-modified')
        last_modified = time.strftime('%Y%m%d%H%M%S', last_modified)
        if int(last_modified) > int(localdate):
            urllib.urlretrieve(url,dst)
            if dst==epgdst:
                extract.all(dst,ADDON_DATA)         
            else:
                extract.all(dst,STORAGE)
            writefile = open(datefile, 'w+')
            writefile.write(last_modified)
            writefile.close()
        try:
            if os.path.exists(dst):
                os.remove(dst)
        except:
            pass
    except Exception as e:
        xbmc.log("Failed with update: %s" % str(url))
        xbmc.log(str(e))
    Remove_Files()
#-----------------------------------------------------------------------------------------------------------------    
def Check_Updates(url, datefile, dst):
    if os.path.exists(datefile):
        readfile = open(datefile,'r')
        localdate = readfile.read()
        readfile.close()
    else:
        localdate = 0
    Check_File_Date(url, datefile, int(localdate), dst)
#-----------------------------------------------------------------------------------------------------------------    
def Dependency_Check():
    dp.create('Checking dependencies','','Please Wait...')
    depfiles = []

    for name in os.listdir(ADDONS):
        if name != 'packages':
            try:
                addonxml = os.path.join(ADDONS,name,'addon.xml')
                addonsource  = open(addonxml, mode = 'r')
                readxml      = addonsource.read()
                addonsource.close()
                dmatch       = re.compile('import addon="(.+?)"').findall(readxml)
    
                for requires in dmatch:
        
                    if not 'xbmc.python' in requires and not requires in depfiles:
                        depfiles.append(requires)
                        if debug == 'true':
                            xbmc.log('Script Requires --- %s' % requires)
            except:
                pass
                
    return depfiles
#-----------------------------------------------------------------------------------------------------------------    
def Remove_Files():
    if os.path.exists(remlist):
        readfile = open(remlist,'r')
        content  = readfile.read()
        readfile.close()
        remarray = content.split('|')
        for item in remarray:
            rempath = xbmc.translatePath('special://home')+item
            if os.path.exists(rempath):
                try:
                    os.remove(rempath)
                except:
                    try:
                        shutil.rmtree(rempath)
                    except:
                        xbmc.log("Failed to remove: %s" %rempath)
        os.remove(remlist)
#-----------------------------------------------------------------------------------------------------------------    
#Popup class - thanks to whoever codes the help popup in TVAddons Maintenance for this section. Unfortunately there doesn't appear to be any author details in that code so unable to credit by name.
class SPLASH(xbmcgui.WindowXMLDialog):
    
    def __init__(self,*args,**kwargs):
        self.shut=kwargs['close_time']
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
        xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")
    
    def onFocus(self,controlID):
        pass
    
    def onClick(self,controlID): 
        if controlID==12:
            xbmc.Player().stop()
            self._close_dialog()
    
    def onAction(self,action):
        if action in [5,6,7,9,10,92,117] or action.getButtonCode() in [275,257,261]:
            xbmc.Player().stop()
            self._close_dialog()
    
    def _close_dialog(self):
        xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
        time.sleep( .4 )
        self.close()
#-----------------------------------------------------------------------------------------------------------------    
#Add a standard directory for the builds. Essentially the same as above but grabs unique artwork from previous call
def Add_Build_Dir(name,url,mode,iconimage,fanart,video,description,skins,guisettingslink,artpack):
        u  = sys.argv[0]
        u += "?url="            +urllib.quote_plus(url)
        u += "&mode="           +str(mode)
        u += "&name="           +urllib.quote_plus(name)
        u += "&iconimage="      +urllib.quote_plus(iconimage)
        u += "&fanart="         +urllib.quote_plus(fanart)
        u += "&video="          +urllib.quote_plus(video)
        u += "&description="    +urllib.quote_plus(description)
        u += "&skins="          +urllib.quote_plus(skins)
        u += "&guisettingslink="+urllib.quote_plus(guisettingslink)
        u += "&artpack="        +urllib.quote_plus(artpack)
        
        ok  = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        
        if (mode==None) or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries') or (mode=='update_build') or (url==None) or (len(url)<1):

            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
        return ok
#---------------------------------------------------------------------------------------------------
#Main Iiectory function - xbmcplugin.addDirectoryItem()
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
#---------------------------------------------------------------------------------------------------
#Add a directory for the description, this requires multiple string to be called from previous menu
def Add_Desc_Dir(name,url,mode,iconimage,fanart,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
#        iconimage = ARTPATH + iconimage
        iconimage = defaulticon
        
        u   = sys.argv[0]
        u += "?url="            +urllib.quote_plus(url)
        u += "&mode="           +str(mode)
        u += "&name="           +urllib.quote_plus(name)
        u += "&iconimage="      +urllib.quote_plus(iconimage)
        u += "&fanart="         +urllib.quote_plus(fanart)
        u += "&author="         +urllib.quote_plus(author)
        u += "&description="    +urllib.quote_plus(description)
        u += "&version="        +urllib.quote_plus(version)
        u += "&buildname="      +urllib.quote_plus(buildname)
        u += "&updated="        +urllib.quote_plus(updated)
        u += "&skins="          +urllib.quote_plus(skins)
        u += "&videoaddons="    +urllib.quote_plus(videoaddons)
        u += "&audioaddons="    +urllib.quote_plus(audioaddons)
        u += "&buildname="      +urllib.quote_plus(buildname)
        u += "&programaddons="  +urllib.quote_plus(programaddons)
        u += "&pictureaddons="  +urllib.quote_plus(pictureaddons)
        u += "&sources="        +urllib.quote_plus(sources)
        u += "&adult="          +urllib.quote_plus(adult)
        
        ok  = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
        return ok
#---------------------------------------------------------------------------------------------------
def Add_Install_Dir(title,name,url,mode,iconimage = '',fanart = '',video = '',description = '',zip_link = '',repo_link = '',repo_id = '',addon_id = '',provider_name = '',forum = '',data_path = ''):
    if len(iconimage) > 0:
#        iconimage = ARTPATH + iconimage
        iconimage = defaulticon
    
    else:
        iconimage = 'DefaultFolder.png'
    
    if fanart == '':
        fanart = FANART
    
    u   = sys.argv[0]
    u += "?url="            +urllib.quote_plus(url)
    u += "&zip_link="       +urllib.quote_plus(zip_link)
    u += "&repo_link="      +urllib.quote_plus(repo_link)
    u += "&data_path="      +urllib.quote_plus(data_path)
    u += "&provider_name="  +str(provider_name)
    u += "&forum="          +str(forum)
    u += "&repo_id="        +str(repo_id)
    u += "&addon_id="       +str(addon_id)
    u += "&mode="           +str(mode)
    u += "&name="           +urllib.quote_plus(name)
    u += "&fanart="         +urllib.quote_plus(fanart)
    u += "&video="          +urllib.quote_plus(video)
    u += "&description="    +urllib.quote_plus(description)
    
    ok  = True
    liz = xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    
    Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
#-----------------------------------------------------------------------------------------------------------------  
#Add a standard directory and grab fanart and iconimage from artpath defined in global variables
def o0oO(type,name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
    if not 'addon' in type:

        if len(iconimage) > 0:
            iconimage = ARTPATH + iconimage
        
        else:
            iconimage = defaulticon

    if 'addon' in type:
        
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = 'DefaultFolder.png'
    
    if fanart == '':
        fanart = FANART
    
    u   = sys.argv[0]
    u += "?url="            +urllib.quote_plus(url)
    u += "&mode="           +str(mode)
    u += "&name="           +urllib.quote_plus(name)
    u += "&iconimage="      +urllib.quote_plus(iconimage)
    u += "&fanart="         +urllib.quote_plus(fanart)
    u += "&video="          +urllib.quote_plus(video)
    u += "&description="    +urllib.quote_plus(description)
        
    ok  = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setProperty( "Build.Video", video )
    
    if 'folder' in type:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    
    else:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    
    return ok
#---------------------------------------------------------------------------------------------------
#Build Categories Menu
def Addon_Categories(url):
    o0oO('folder','[COLOR=darkcyan][PLUGIN][/COLOR] Audio',url+'&typex=audio','grab_addons','audio.png','','','')
    o0oO('folder','[COLOR=darkcyan][PLUGIN][/COLOR] Image (Picture)',url+'&typex=image','grab_addons','pictures.png','','','')
    o0oO('folder','[COLOR=darkcyan][PLUGIN][/COLOR] Program',url+'&typex=program','grab_addons','programs.png','','','')
    o0oO('folder','[COLOR=darkcyan][PLUGIN][/COLOR] Video',url+'&typex=video','grab_addons','video.png','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] Movies (Used for library scanning)',url+'&typex=movie%20scraper','grab_addons','movies.png','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] TV Shows (Used for library scanning)',url+'&typex=tv%20show%20scraper','grab_addons','tvshows.png','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] Music Artists (Used for library scanning)',url+'&typex=artist%20scraper','grab_addons','artists.png','','','')
    o0oO('folder','[COLOR=lime][SCRAPER][/COLOR] Music Videos (Used for library scanning)',url+'&typex=music%20video%20scraper','grab_addons','musicvideos.png','','','')
    o0oO('folder','[COLOR=orange][SERVICE][/COLOR] All Services',url+'&typex=service','grab_addons','services.png','','','')
    o0oO('folder','[COLOR=orange][SERVICE][/COLOR] Weather Service',url+'&typex=weather','grab_addons','weather.png','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Repositories',url+'&typex=repository','grab_addons','repositories.png','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Scripts (Program Add-ons)',url+'&typex=executable','grab_addons','scripts.png','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Screensavers',url+'&typex=screensaver','grab_addons','screensaver.png','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Script Modules',url+'&typex=script%20module','grab_addons','scriptmodules.png','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Skins',url+'&typex=skin','grab_addons','skins.png','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Subtitles',url+'&typex=subtitles','grab_addons','subtitles.png','','','')
    o0oO('folder','[COLOR=dodgerblue][OTHER][/COLOR] Web Interface',url+'&typex=web%20interface','grab_addons','webinterface.png','','','')
#    o0oO('folder','Lyrics','&typex=lyrics','grab_addons','lyrics.png','','','')
#---------------------------------------------------------------------------------------------------
def Addon_Check_Updates():
    Update_Repo()
    xbmc.executebuiltin('ActivateWindow(10040,"addons://outdated/",return)')
#---------------------------------------------------------------------------------------------------
#Build Countries Menu   
def Addon_Countries(url):
    o0oO('folder','African',url+'&genre=african','grab_addons','african.png','','','')
    o0oO('folder','Arabic',url+'&genre=arabic','grab_addons','arabic.png','','','')
    o0oO('folder','Asian',url+'&genre=asian','grab_addons','asian.png','','','')
    o0oO('folder','Australian',url+'&genre=australian','grab_addons','australian.png','','','')
    o0oO('folder','Austrian',url+'&genre=austrian','grab_addons','austrian.png','','','')
    o0oO('folder','Belgian',url+'&genre=belgian','grab_addons','belgian.png','','','')
    o0oO('folder','Brazilian',url+'&genre=brazilian','grab_addons','brazilian.png','','','')
    o0oO('folder','Canadian',url+'&genre=canadian','grab_addons','canadian.png','','','')
    o0oO('folder','Chinese',url+'&genre=chinese','grab_addons','chinese.png','','','')
    o0oO('folder','Colombian',url+'&genre=columbian','grab_addons','columbian.png','','','')
    o0oO('folder','Croatian',url+'&genre=croatian','grab_addons','croatian.png','','','')
    o0oO('folder','Czech',url+'&genre=czech','grab_addons','czech.png','','','')
    o0oO('folder','Danish',url+'&genre=danish','grab_addons','danish.png','','','')
    o0oO('folder','Dominican',url+'&genre=dominican','grab_addons','dominican.png','','','')
    o0oO('folder','Dutch',url+'&genre=dutch','grab_addons','dutch.png','','','')
    o0oO('folder','Egyptian',url+'&genre=egyptian','grab_addons','egyptian.png','','','')
    o0oO('folder','Filipino',url+'&genre=filipino','grab_addons','filipino.png','','','')
    o0oO('folder','Finnish',url+'&genre=finnish','grab_addons','finnish.png','','','')
    o0oO('folder','French',url+'&genre=french','grab_addons','french.png','','','')
    o0oO('folder','German',url+'&genre=german','grab_addons','german.png','','','')
    o0oO('folder','Greek',url+'&genre=greek','grab_addons','greek.png','','','')
    o0oO('folder','Hebrew',url+'&genre=hebrew','grab_addons','hebrew.png','','','')
    o0oO('folder','Hungarian',url+'&genre=hungarian','grab_addons','hungarian.png','','','')
    o0oO('folder','Icelandic',url+'&genre=icelandic','grab_addons','icelandic.png','','','')
    o0oO('folder','Indian',url+'&genre=indian','grab_addons','indian.png','','','')
    o0oO('folder','Irish',url+'&genre=irish','grab_addons','irish.png','','','')
    o0oO('folder','Italian',url+'&genre=italian','grab_addons','italian.png','','','')
    o0oO('folder','Japanese',url+'&genre=japanese','grab_addons','japanese.png','','','')
    o0oO('folder','Korean',url+'&genre=korean','grab_addons','korean.png','','','')
    o0oO('folder','Lebanese',url+'&genre=lebanese','grab_addons','lebanese.png','','','')
    o0oO('folder','Mongolian',url+'&genre=mongolian','grab_addons','mongolian.png','','','')
    o0oO('folder','Moroccan',url+'&genre=moroccan','grab_addons','moroccan.png','','','')
    o0oO('folder','Nepali',url+'&genre=nepali','grab_addons','nepali.png','','','')
    o0oO('folder','New Zealand',url+'&genre=newzealand','grab_addons','newzealand.png','','','')
    o0oO('folder','Norwegian',url+'&genre=norwegian','grab_addons','norwegian.png','','','')
    o0oO('folder','Pakistani',url+'&genre=pakistani','grab_addons','pakistani.png','','','')
    o0oO('folder','Polish',url+'&genre=polish','grab_addons','polish.png','','','')
    o0oO('folder','Portuguese',url+'&genre=portuguese','grab_addons','portuguese.png','','','')
    o0oO('folder','Romanian',url+'&genre=romanian','grab_addons','romanian.png','','','')
    o0oO('folder','Russian',url+'&genre=russian','grab_addons','russian.png','','','')
    o0oO('folder','Singapore',url+'&genre=singapore','grab_addons','singapore.png','','','')
    o0oO('folder','Spanish',url+'&genre=spanish','grab_addons','spanish.png','','','')
    o0oO('folder','Swedish',url+'&genre=swedish','grab_addons','swedish.png','','','')
    o0oO('folder','Swiss',url+'&genre=swiss','grab_addons','swiss.png','','','')
    o0oO('folder','Syrian',url+'&genre=syrian','grab_addons','syrian.png','','','')
    o0oO('folder','Tamil',url+'&genre=tamil','grab_addons','tamil.png','','','')
    o0oO('folder','Thai',url+'&genre=thai','grab_addons','thai.png','','','')
    o0oO('folder','Turkish',url+'&genre=turkish','grab_addons','turkish.png','','','')
    o0oO('folder','UK',url+'&genre=uk','grab_addons','uk.png','','','')
    o0oO('folder','USA',url+'&genre=usa','grab_addons','usa.png','','','')
    o0oO('folder','Vietnamese',url+'&genre=vietnamese','grab_addons','vietnamese.png','','','')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Addon_Final_Menu(url):
    BaseURL                = 'http://noobsandnerds.com/TI/AddonPortal/addondetails.php?id=%s' % (url)
    link                   = Open_URL(BaseURL).replace('\n','').replace('\r','')
    approvedmatch          = re.compile('approved="(.+?)"').findall(link)
    contenttypematch       = re.compile('addon_types="(.+?)"').findall(link)
    namematch              = re.compile('name="(.+?)"').findall(link)
    UIDmatch               = re.compile('UID="(.+?)"').findall(link)
    idmatch                = re.compile('id="(.+?)"').findall(link)
    providernamematch      = re.compile('provider_name="(.+?)"').findall(link)
    versionmatch           = re.compile('version="(.+?)"').findall(link)
    createdmatch           = re.compile('created="(.+?)"').findall(link)
    contentmatch           = re.compile('addon_types="(.+?)"').findall(link)
    updatedmatch           = re.compile('updated="(.+?)"').findall(link)
    downloadsmatch         = re.compile('downloads="(.+?)"').findall(link)
    descriptionmatch       = re.compile('description="(.+?)"').findall(link)
    devbrokenmatch         = re.compile('devbroke="(.+?)"').findall(link)
    brokenmatch            = re.compile('broken="(.+?)"').findall(link)
    deletedmatch           = re.compile('deleted="(.+?)"').findall(link)
    notesmatch             = re.compile('mainbranch_notes="(.+?)"').findall(link)
    repourlmatch           = re.compile('repo_url="(.+?)"').findall(link)
    dataurlmatch           = re.compile('data_url="(.+?)"').findall(link)
    zipurlmatch            = re.compile('zip_url="(.+?)"').findall(link)
    genresmatch            = re.compile('genres="(.+?)"').findall(link)
    forummatch             = re.compile('forum="(.+?)"').findall(link)
    repoidmatch            = re.compile('repo_id="(.+?)"').findall(link)
    licensematch           = re.compile('license="(.+?)"').findall(link)
    platformmatch          = re.compile('platform="(.+?)"').findall(link)
    visiblematch           = re.compile('visible="(.+?)"').findall(link)
    scriptmatch            = re.compile('script="(.+?)"').findall(link)
    programpluginmatch     = re.compile('program_plugin="(.+?)"').findall(link)
    scriptmodulematch      = re.compile('script_module="(.+?)"').findall(link)
    videopluginmatch       = re.compile('video_plugin="(.+?)"').findall(link)
    audiopluginmatch       = re.compile('audio_plugin="(.+?)"').findall(link)
    imagepluginmatch       = re.compile('image_plugin="(.+?)"').findall(link)
    repositorymatch        = re.compile('repository="(.+?)"').findall(link)
    weatherservicematch    = re.compile('weather_service="(.+?)"').findall(link)
    skinmatch              = re.compile('skin="(.+?)"').findall(link)
    servicematch           = re.compile('service="(.+?)"').findall(link)
    warningmatch           = re.compile('warning="(.+?)"').findall(link)
    webinterfacematch      = re.compile('web_interface="(.+?)"').findall(link)
    moviescrapermatch      = re.compile('movie_scraper="(.+?)"').findall(link)
    tvscrapermatch         = re.compile('tv_scraper="(.+?)"').findall(link)
    artistscrapermatch     = re.compile('artist_scraper="(.+?)"').findall(link)
    musicvideoscrapermatch = re.compile('music_video_scraper="(.+?)"').findall(link)
    subtitlesmatch         = re.compile('subtitles="(.+?)"').findall(link)
    requiresmatch          = re.compile('requires="(.+?)"').findall(link)
    modulesmatch           = re.compile('modules="(.+?)"').findall(link)
    iconmatch              = re.compile('icon="(.+?)"').findall(link)
    videopreviewmatch      = re.compile('video_preview="(.+?)"').findall(link)
    videoguidematch        = re.compile('video_guide="(.+?)"').findall(link)
    videoguidematch1       = re.compile('video_guide1="(.+?)"').findall(link)
    videoguidematch2       = re.compile('video_guide2="(.+?)"').findall(link)
    videoguidematch3       = re.compile('video_guide3="(.+?)"').findall(link)
    videoguidematch4       = re.compile('video_guide4="(.+?)"').findall(link)
    videoguidematch5       = re.compile('video_guide5="(.+?)"').findall(link)
    videoguidematch6       = re.compile('video_guide6="(.+?)"').findall(link)
    videoguidematch7       = re.compile('video_guide7="(.+?)"').findall(link)
    videoguidematch8       = re.compile('video_guide8="(.+?)"').findall(link)
    videoguidematch9       = re.compile('video_guide9="(.+?)"').findall(link)
    videoguidematch10      = re.compile('video_guide10="(.+?)"').findall(link)
    videolabelmatch1       = re.compile('video_label1="(.+?)"').findall(link)
    videolabelmatch2       = re.compile('video_label2="(.+?)"').findall(link)
    videolabelmatch3       = re.compile('video_label3="(.+?)"').findall(link)
    videolabelmatch4       = re.compile('video_label4="(.+?)"').findall(link)
    videolabelmatch5       = re.compile('video_label5="(.+?)"').findall(link)
    videolabelmatch6       = re.compile('video_label6="(.+?)"').findall(link)
    videolabelmatch7       = re.compile('video_label7="(.+?)"').findall(link)
    videolabelmatch8       = re.compile('video_label8="(.+?)"').findall(link)
    videolabelmatch9       = re.compile('video_label9="(.+?)"').findall(link)
    videolabelmatch10      = re.compile('video_label10="(.+?)"').findall(link)

#Need to add if broken version > current version statement   
    approved            = approvedmatch[0] if (len(approvedmatch) > 0) else ''
    contenttypes        = contenttypematch[0] if (len(contenttypematch) > 0) else ''
    name                = namematch[0] if (len(namematch) > 0) else ''
    UID                 = UIDmatch[0] if (len(UIDmatch) > 0) else ''
    addon_id            = idmatch[0] if (len(idmatch) > 0) else ''
    provider_name       = providernamematch[0] if (len(providernamematch) > 0) else ''
    version             = versionmatch[0] if (len(versionmatch) > 0) else ''
    created             = createdmatch[0] if (len(createdmatch) > 0) else ''
    content_types       = contentmatch[0] if (len(contentmatch) > 0) else ''
    updated             = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    downloads           = downloadsmatch[0] if (len(downloadsmatch) > 0) else ''
    desc                = '[CR][CR][COLOR=dodgerblue]Description: [/COLOR]'+descriptionmatch[0] if (len(descriptionmatch) > 0) else ''
    devbroken           = devbrokenmatch[0] if (len(devbrokenmatch) > 0) else ''
    broken              = brokenmatch[0] if (len(brokenmatch) > 0) else ''
    deleted             = '[CR]'+deletedmatch[0] if (len(deletedmatch) > 0) else ''
    notes               = '[CR][CR][COLOR=dodgerblue]User Notes: [/COLOR]'+notesmatch[0] if (len(notesmatch) > 0) else ''
    repo_url            = repourlmatch[0] if (len(repourlmatch) > 0) else ''
    data_url            = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
    zip_url             = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
    genres              = genresmatch[0] if (len(genresmatch) > 0) else ''
    forum               = '[CR][CR][COLOR=dodgerblue]Support Forum: [/COLOR]'+forummatch[0] if (len(forummatch) > 0) else '[CR][CR][COLOR=dodgerblue]Support Forum: [/COLOR]No forum details given by developer'
    forumclean          = forummatch[0] if (len(forummatch) > 0) else 'None'
    repo_id             = repoidmatch[0] if (len(repoidmatch) > 0) else ''
    license             = licensematch[0] if (len(licensematch) > 0) else ''
    platform            = '[COLOR=orange]     Platform: [/COLOR]'+platformmatch[0] if (len(platformmatch) > 0) else ''
    visible             = visiblematch[0] if (len(visiblematch) > 0) else ''
    script              = scriptmatch[0] if (len(scriptmatch) > 0) else ''
    program_plugin      = programpluginmatch[0] if (len(programpluginmatch) > 0) else ''
    script_module       = scriptmodulematch[0] if (len(scriptmodulematch) > 0) else ''
    video_plugin        = videopluginmatch[0] if (len(videopluginmatch) > 0) else ''
    audio_plugin        = audiopluginmatch[0] if (len(audiopluginmatch) > 0) else ''
    image_plugin        = imagepluginmatch[0] if (len(imagepluginmatch) > 0) else ''
    repository          = repositorymatch[0] if (len(repositorymatch) > 0) else ''
    service             = servicematch[0] if (len(servicematch) > 0) else ''
    skin                = skinmatch[0] if (len(skinmatch) > 0) else ''
    warning             = warningmatch[0] if (len(warningmatch) > 0) else ''
    web_interface       = webinterfacematch[0] if (len(webinterfacematch) > 0) else ''
    weather_service     = weatherservicematch[0] if (len(weatherservicematch) > 0) else ''
    movie_scraper       = moviescrapermatch[0] if (len(moviescrapermatch) > 0) else ''
    tv_scraper          = tvscrapermatch[0] if (len(tvscrapermatch) > 0) else ''
    artist_scraper      = artistscrapermatch[0] if (len(artistscrapermatch) > 0) else ''
    music_video_scraper = musicvideoscrapermatch[0] if (len(musicvideoscrapermatch) > 0) else ''
    subtitles           = subtitlesmatch[0] if (len(subtitlesmatch) > 0) else ''
    requires            = requiresmatch[0] if (len(requiresmatch) > 0) else ''
    modules             = modulesmatch[0] if (len(modulesmatch) > 0) else ''
    icon                = iconmatch[0] if (len(iconmatch) > 0) else ''
    videopreview        = videopreviewmatch[0] if (len(videopreviewmatch) > 0) else 'None'
    videoguide          = videoguidematch[0] if (len(videoguidematch) > 0) else 'None'
    videoguide1         = videoguidematch1[0] if (len(videoguidematch1) > 0) else 'None'
    videoguide2         = videoguidematch2[0] if (len(videoguidematch2) > 0) else 'None'
    videoguide3         = videoguidematch3[0] if (len(videoguidematch3) > 0) else 'None'
    videoguide4         = videoguidematch4[0] if (len(videoguidematch4) > 0) else 'None'
    videoguide5         = videoguidematch5[0] if (len(videoguidematch5) > 0) else 'None'
    videoguide6         = videoguidematch6[0] if (len(videoguidematch6) > 0) else 'None'
    videoguide7         = videoguidematch7[0] if (len(videoguidematch7) > 0) else 'None'
    videoguide8         = videoguidematch8[0] if (len(videoguidematch8) > 0) else 'None'
    videoguide9         = videoguidematch9[0] if (len(videoguidematch9) > 0) else 'None'
    videoguide10        = videoguidematch10[0] if (len(videoguidematch10) > 0) else 'None'
    videolabel1         = videolabelmatch1[0] if (len(videolabelmatch1) > 0) else 'None'
    videolabel2         = videolabelmatch2[0] if (len(videolabelmatch2) > 0) else 'None'
    videolabel3         = videolabelmatch3[0] if (len(videolabelmatch3) > 0) else 'None'
    videolabel4         = videolabelmatch4[0] if (len(videolabelmatch4) > 0) else 'None'
    videolabel5         = videolabelmatch5[0] if (len(videolabelmatch5) > 0) else 'None'
    videolabel6         = videolabelmatch6[0] if (len(videolabelmatch6) > 0) else 'None'
    videolabel7         = videolabelmatch7[0] if (len(videolabelmatch7) > 0) else 'None'
    videolabel8         = videolabelmatch8[0] if (len(videolabelmatch8) > 0) else 'None'
    videolabel9         = videolabelmatch9[0] if (len(videolabelmatch9) > 0) else 'None'
    videolabel10        = videolabelmatch10[0] if (len(videolabelmatch10) > 0) else 'None'
    
    xbmc.log("### Addon Details: %s" %name)
    if deleted != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=red]This add-on is depreciated, it\'s no longer available.[/COLOR]'
    
    elif broken == '' and devbroken == '' and warning =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=lime]No reported problems[/COLOR]'
    
    elif broken == '' and devbroken == '' and warning !='' and deleted =='':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR][COLOR=orange]Although there have been no reported problems there may be issues with this add-on, see below.[/COLOR]'
    
    elif broken == '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by the add-on developer.[CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken
    
    elif broken != '' and devbroken == '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by a member of the community at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR][CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken
    
    elif broken != '' and devbroken != '':
        brokenfinal  = '[CR][CR][COLOR=dodgerblue]Status: [/COLOR]Marked as broken by both the add-on developer and a member of the community at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR][CR][COLOR=dodgerblue]Developer Comments: [/COLOR]'+devbroken+'[CR][COLOR=dodgerblue]User Comments: [/COLOR]'+broken

# Create the main description template
    description = str('[COLOR=orange]Name: [/COLOR]'+name+'[COLOR=orange]     Author(s): [/COLOR]'+provider_name+'[COLOR=orange][CR][CR]Version: [/COLOR]'+version+'[COLOR=orange]     Created: [/COLOR]'+created+'[COLOR=orange]     Updated: [/COLOR]'+updated+'[COLOR=orange][CR][CR]Repository: [/COLOR]'+repo_id+platform+'[COLOR=orange]     Add-on Type(s): [/COLOR]'+content_types+requires+brokenfinal+deleted+warning+forum+desc+notes)

# If addon already exists notify or give option to run
    if os.path.exists(os.path.join(ADDONS,addon_id)):
        if 'script.module' in addon_id or 'repo' in addon_id:
            o0oO('','[COLOR=orange]Already installed[/COLOR]','','',icon,'','','')
        else:
            o0oO('','[COLOR=orange]Already installed -[/COLOR] Click here to run the add-on',addon_id,'run_addon',icon,'','','')

# If server is having a slow day and cannot get the name notify user
    if name =='':
        o0oO('','[COLOR=darkcyan]Sorry request failed due to high traffic on server, please try again[/COLOR]','','',icon,'','','')

# Show any known issues with addon
    elif name != '':
        
        if (broken == '') and (devbroken =='') and (deleted =='') and (warning ==''):
            o0oO('addon','[COLOR=darkcyan][FULL DETAILS][/COLOR] No problems reported',description,'text_guide',icon,'','',description)    
        
        if (broken != '' and deleted == '') or (devbroken != '' and deleted == '') or (warning != '' and deleted ==''):
            o0oO('addon','[COLOR=darkcyan][FULL DETAILS][/COLOR][COLOR=orange] Possbile problems reported[/COLOR]',description,'text_guide',icon,'','',description)            
        
        if deleted != '':
            o0oO('addon','[COLOR=darkcyan][FULL DETAILS][/COLOR][COLOR=red] Add-on now depreciated[/COLOR]',description,'text_guide',icon,'','',description)            

######################################################################################################################
# CHECK TO SEE IF MARKED AS ILLEGAL CONTENT. IF MARKED AS DODGY DO NOT SHOW INSTALL OPTIONS UNLESS REPO IS INSTALLED #
######################################################################################################################
        repopath = xbmc.translatePath(os.path.join(ADDONS, repo_id))
        
        if approved=='0':
            
            if repo_id != '' and 'superrepo' not in repo_id and deleted =='':
                Add_Install_Dir('[COLOR=lime][INSTALL] [/COLOR]'+name,name,'','addon_install_na','Install.png','','',desc,contenttypes,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    
            
            if (repo_id == '' or 'superrepo' in repo_id) and deleted =='':
                Add_Install_Dir('[COLOR=lime][INSTALL] [/COLOR]'+name,name,'','addon_install_badzip','Install.png','','',desc,contenttypes,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    
#                    Add_Install_Dir('[COLOR=lime][INSTALL - Backup Option] [/COLOR]'+name,name,'','addon_install','Install.png','','',desc,zip_url,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    

# If addon isn't deleted show download options
        elif deleted =='':
            
            if repo_id != '' and 'superrepo' not in repo_id:
                Add_Install_Dir('[COLOR=lime][INSTALL - Recommended] [/COLOR]'+name,name,'','addon_install_zero','Install.png','','',desc,contenttypes,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    
                Add_Install_Dir('[COLOR=lime][INSTALL - Backup Option] [/COLOR]'+name,name,'','addon_install','Install.png','','',desc,zip_url,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    
            
            if repo_id == '' or 'superrepo' in repo_id:
                Add_Install_Dir('[COLOR=lime][INSTALL] [/COLOR]'+name+' - THIS IS NOT IN A SELF UPDATING REPO',name,'','addon_install','Install.png','','',desc,zip_url,repo_url,repo_id,addon_id,provider_name,forumclean,data_url)    

# Show various video links
        if videopreview != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  Preview',videoguide1,'play_video','Video_Guide.png','','','')    
        
        if videoguide1 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video','Video_Guide.png','','','')    
        
        if videoguide2 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video','Video_Guide.png','','','')    
        
        if videoguide3 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video','Video_Guide.png','','','')    
        
        if videoguide4 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video','Video_Guide.png','','','')    
        
        if videoguide5 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video','Video_Guide.png','','','')    
        
        if videoguide6 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel6,videoguide6,'play_video','Video_Guide.png','','','')    
        
        if videoguide7 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel7,videoguide7,'play_video','Video_Guide.png','','','')    
        
        if videoguide8 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel8,videoguide8,'play_video','Video_Guide.png','','','')    
        
        if videoguide9 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel9,videoguide9,'play_video','Video_Guide.png','','','')    
        
        if videoguide10 != 'None':
            o0oO('','[COLOR=dodgerblue][VIDEO][/COLOR]  '+videolabel10,videoguide10,'play_video','Video_Guide.png','','','')    
#---------------------------------------------------------------------------------------------------
#Build Genres Menu
def Addon_Genres(url):       
    o0oO('folder','Anime',url+'&genre=anime','grab_addons','anime.png','','','')
    o0oO('folder','Audiobooks',url+'&genre=audiobooks','grab_addons','audiobooks.png','','','')
    o0oO('folder','Comedy',url+'&genre=comedy','grab_addons','comedy.png','','','')
    o0oO('folder','Comics',url+'&genre=comics','grab_addons','comics.png','','','')
    o0oO('folder','Documentary',url+'&genre=documentary','grab_addons','documentary.png','','','')
    o0oO('folder','Downloads',url+'&genre=downloads','grab_addons','downloads.png','','','')
    o0oO('folder','Food',url+'&genre=food','grab_addons','food.png','','','')
    o0oO('folder','Gaming',url+'&genre=gaming','grab_addons','gaming.png','','','')
    o0oO('folder','Health',url+'&genre=health','grab_addons','health.png','','','')
    o0oO('folder','How To...',url+'&genre=howto','grab_addons','howto.png','','','')
    o0oO('folder','Kids',url+'&genre=kids','grab_addons','kids.png','','','')
    o0oO('folder','Live TV',url+'&genre=livetv','grab_addons','livetv.png','','','')
    o0oO('folder','Movies',url+'&genre=movies','grab_addons','movies.png','','','')
    o0oO('folder','Music',url+'&genre=music','grab_addons','music.png','','','')
    o0oO('folder','News',url+'&genre=news','grab_addons','news.png','','','')
    o0oO('folder','Photos',url+'&genre=photos','grab_addons','photos.png','','','')
    o0oO('folder','Podcasts',url+'&genre=podcasts','grab_addons','podcasts.png','','','')
    o0oO('folder','Radio',url+'&genre=radio','grab_addons','radio.png','','','')
    o0oO('folder','Religion',url+'&genre=religion','grab_addons','religion.png','','','')
    o0oO('folder','Space',url+'&genre=space','grab_addons','space.png','','','')
    o0oO('folder','Sports',url+'&genre=sports','grab_addons','sports.png','','','')
    o0oO('folder','Technology',url+'&genre=tech','grab_addons','tech.png','','','')
    o0oO('folder','Trailers',url+'&genre=trailers','grab_addons','trailers.png','','','')
    o0oO('folder','TV Shows',url+'&genre=tv','grab_addons','tv.png','','','')
    o0oO('folder','Misc.',url+'&genre=other','grab_addons','other.png','','','')
    
    if ADDON.getSetting('adult') == 'true':
        o0oO('folder','XXX',url+'&genre=adult','grab_addons','adult.png','','','')
#---------------------------------------------------------------------------------------------------
#Step 1 of the addon install process (installs the actual addon)
def Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path):
    xbmc.log("############# ADDON INSTALL #################")
    forum        = str(forum)
    repo_id      = str(repo_id)
    status       = 1
    repostatus   = 1
    modulestatus = 1
    addonpath    = xbmc.translatePath(os.path.join(ADDONS, addon_id))
    
    if os.path.exists(addonpath):
        addonexists = 1
    
    else:
        addonexists = 0
    
    addondownload = xbmc.translatePath(os.path.join(packages,name+'.zip'))
    addonlocation = xbmc.translatePath(os.path.join(ADDONS,addon_id))
    
    dp.create("Installing Addon","Please wait whilst your addon is installed",'', '')
    
    try:
        downloader.download(repo_link, addondownload, dp)
        extract.all(addondownload, ADDONS, dp)
    
    except:
        
        try:
            downloader.download(zip_link, addondownload, dp)
            extract.all(addondownload, ADDONS, dp)
        
        except:
            
            try:
                if not os.path.exists(addonlocation):
                    os.makedirs(addonlocation)
                
                link  = Open_URL(data_path).replace('\n','').replace('\r','')
                match = re.compile('href="(.+?)"', re.DOTALL).findall(link)
                
                for href in match:
                    filepath=xbmc.translatePath(os.path.join(addonlocation,href))
                    
                    if addon_id not in href and '/' not in href:
                        
                        try:
                            dp.update(0,"Downloading [COLOR=darkcyan]"+href+'[/COLOR]','','Please wait...')
                            downloader.download(data_path+href, filepath, dp)
                        
                        except:
                            xbmc.log("failed to install %s" %href)
                    
                    if '/' in href and '..' not in href and 'http' not in href:
                        remote_path = data_path+href
                        Recursive_Loop(filepath,remote_path)
            
            except:
                dialog.ok("Error downloading add-on", 'There was an error downloading [COLOR=darkcyan]'+name,'[/COLOR]Please consider updating the add-on portal with details or report the error on the forum at [COLOR=lime][B]noobsandnerds.com[/COLOR][/B]') 
                status=0
    
    if status==1:
        time.sleep(1)
        dp.update(0,"[COLOR=darkcyan]"+name+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Now installing repository')
        time.sleep(1)
        repopath = xbmc.translatePath(os.path.join(ADDONS, repo_id))
        
        if (repo_id != 'repository.xbmc.org') and not (os.path.exists(repopath)) and (repo_id != '') and ('superrepo' not in repo_id):
            Install_Repo(repo_id)
        
        xbmc.sleep(2000)
        
        if os.path.exists(addonpath) and addonexists == 0:
            incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (addon_id)
            try:
                Open_URL(incremental)
            except:
                pass        
        Dependency_Install(name,addon_id)
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.sleep(1000)
        xbmc.executebuiltin( 'UpdateAddonRepos' )
        
        if repostatus == 0:
            dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing the repository.','This will mean the add-on fails to update')
        
        if modulestatus == 0:
            dialog.ok(name+" Install Complete",'The add-on has been successfully installed but','there was an error installing modules.','This could result in errors with the add-on.')
        
        if modulestatus != 0 and repostatus != 0 and forum != 'None':
            dialog.ok(name+" Install Complete",'Please support the developer(s) [COLOR=dodgerblue]'+provider_name,'[/COLOR]Support for this add-on can be found at [COLOR=darkcyan]'+forum,'[/COLOR][CR]Visit [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR] for all your Kodi needs.')
        
        if modulestatus != 0 and repostatus != 0 and forum == 'None':
            dialog.ok(name+" Install Complete",'Please support the developer(s) [COLOR=dodgerblue]'+provider_name,'[/COLOR]No details of forum support have been given.')
    
    xbmc.executebuiltin('Container.Refresh')         
#---------------------------------------------------------------------------------------------------
#Step 1 of the addon install process (installs the actual addon)
def Addon_Install_Zero(name,contenttypes,repo_link,repo_id,addon_id,provider_name,forum,data_path):
    xbmc.log("############# RECOMMENDED ADDON INSTALL #################")
    addonpath = xbmc.translatePath(os.path.join(ADDONS, addon_id))
    forum     = str(forum)
    
    if not os.path.exists(addonpath):
        cont=1
    
    else:
        cont=0
    
    repo_id  = str(repo_id)
    repopath = xbmc.translatePath(os.path.join(ADDONS, repo_id))
    
    if os.path.exists(addonpath):
        addonexists=1
        choice = dialog.yesno('Add-on Already Installed','This add-on has already been detected on your system. Would you like to remove the old version and re-install? There should be no need for this unless you\'ve manually opened up the add-on code and edited in a text editor.')
        
        if choice == 1:
            Remove_Addons(addonpath)
            cont=1
    else:
        addonexists = 0
    
    if cont==1:
        
        if (repo_id != 'repository.xbmc.org') and not (os.path.exists(repopath)) and (repo_id != '') and ('superrepo' not in repo_id):
            Install_Repo(repo_id)
        
        if not os.path.exists(addonpath): # Create new placeholder for addon.xml and default.py
            os.makedirs(addonpath)
        
        newpath        = os.path.join(ADDONS,addon_id,'addon.xml')
        newpathdefault = os.path.join(ADDONS,addon_id,'default.py')
        
        shutil.copyfile(ADDONXMLTEMP, newpath) # Copy template addon.xml
        
        filefix = open(os.path.join(newpath), mode='r')
        content = filefix.read()
        filefix.close()
        
    # Section to find and replace strings in template addon.xml
        localidmatch       = re.compile('testid[\s\S]*?').findall(content)
        idmatch            = localidmatch[0] if (len(localidmatch) > 0) else 'None'
        localnamematch     = re.compile('testname[\s\S]*?').findall(content)
        namematch          = localnamematch[0] if (len(localnamematch) > 0) else 'None'
        localprovidermatch = re.compile('testprovider[\s\S]*?').findall(content)
        providermatch      = localprovidermatch[0] if (len(localprovidermatch) > 0) else 'None'
        localprovidesmatch = re.compile('testprovides[\s\S]*?').findall(content)
        providesmatch      = localprovidesmatch[0] if (len(localprovidesmatch) > 0) else 'None'
        replacefile        = content.replace(idmatch,addon_id).replace(namematch,name).replace(providermatch,provider_name).replace(providesmatch,contenttypes)
        
        writefile = open(newpath, mode='w+')
        writefile.write(str(replacefile))
        writefile.close()
        
        writefile2 = open(newpathdefault, mode='w')
        writefile2.write('import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys\nAddonID="'+addon_id+'"\nAddonName="'+name+'"\ndialog=xbmcgui.Dialog()\nxbmc.executebuiltin("UpdateLocalAddons")\nxbmc.executebuiltin("UpdateAddonRepos")\nchoice=dialog.yesno(AddonName+" Add-on Requires Update","This add-on may still be in the process of the updating. We recommend waiting but if you\'ve already tried that and it\'s not updating you can try re-installing via the backup method in Maintenance.",yeslabel="Install Option 2", nolabel="Wait...")\nif choice == 1: xbmc.executebuiltin(\'ActivateWindow(10001,"plugin://plugin.program.tbs/?mode=grab_addons&url=%26redirect%26addonid%3d\'+AddonID+\'")\')\nxbmcplugin.endOfDirectory(int(sys.argv[1]))')
        writefile2.close()
        
        xbmc.sleep(1000)
        
        if os.path.exists(addonpath) and addonexists == 0:
            incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (addon_id)
            try:
                Open_URL(incremental)
            except:
                pass        
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.executebuiltin( 'UpdateAddonRepos' )
        dialog.ok(name+" Install Complete",'[COLOR=dodgerblue]'+name+'[/COLOR] has now been installed, please allow a few moments for Kodi to update the add-on and it\'s dependencies.')
    
    xbmc.executebuiltin('Container.Refresh')         
#---------------------------------------------------------------------------------------------------
#Option to install a non-approved addon via the repo in kodi
def Addon_Install_NA(name,contenttypes,repo_link,repo_id,addon_id,provider_name,forum,data_path):
    xbmc.log("############# INSTALL NON APPROVED ADDON #################")
    repopath  = xbmc.translatePath(os.path.join(ADDONS, repo_id))
    addonpath = xbmc.translatePath(os.path.join(ADDONS, addon_id))
    
    if os.path.exists(addonpath):
        
        choice = dialog.yesno('Add-on Already Installed','This add-on has already been detected on your system. Would you like to remove the old version and re-install? There should be no need for this unless you\'ve manually opened up the add-on code and edited in a text editor.')
        
        if choice == 1:
            Remove_Addons(addonpath)
    
    if os.path.exists(repopath):
        
        if os.path.exists(addonpath):
             addonexists=1
        
        else:
            addonexists = 0
        
        choice = dialog.yesno('WARNING!','[COLOR=orange]This Add-on may be unlawful in your region.[/COLOR][CR]The repository required for installation of this add-on has been detected on your system. Would you like to continue to the Kodi addon browser to install?')
        
        if choice == 1:
            
            if 'video' in contenttypes:
                xbmc.executebuiltin('ActivateWindow(10040,"addons://'+repo_id+'/xbmc.addon.video/?",return)')
            
            elif 'executable' in contenttypes:
                xbmc.executebuiltin('ActivateWindow(10040,"addons://'+repo_id+'/xbmc.addon.executable/?",return)')
            
            elif 'audio' in contenttypes:
                xbmc.executebuiltin('ActivateWindow(10040,"addons://'+repo_id+'/xbmc.addon.audio/?",return)')
        
        xbmc.sleep(2000)
        
        if os.path.exists(addonpath) and addonexists == 0:
            incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (addon_id)
            try:
                Open_URL(incremental)
            except:
                pass    
    else:
        dialog.ok('WARNING!','[COLOR=orange]This add-on may possibly be unlawful in your region.[/COLOR][CR]If you\'ve investigated the legality of it and are happy to install then you must have the following repository installed: [COLOR=dodgerblue]'+repo_id+'[/COLOR]')
    
    xbmc.executebuiltin('Container.Refresh')         
#---------------------------------------------------------------------------------------------------
#Option to install a non-approved addon via the repo in kodi
def Addon_Install_BadZip(name,contenttypes,repo_link,repo_id,addon_id,provider_name,forum,data_path):
    dialog.ok('Add-on Not Approved','Sorry there are no repository details for this add-on and it\'s been marked as potentially giving access to unlawful content. The most likely cause for this is the add-on has only been released via social media groups.')
#---------------------------------------------------------------------------------------------------
#Addons section
def Addon_Menu(sign):
    o0oO('folder','[COLOR=gold][TOP 100][/COLOR] Show the most downloaded add-ons','popular','grab_addons','','','','')
    o0oO('folder','[COLOR=darkcyan][Manual Search][/COLOR] Type in author/name/content','desc=','search_addons','','','','')
    o0oO('folder','[COLOR=dodgerblue][Filter Results][/COLOR] By Genres', 'p', 'addon_genres', '','','','')
    o0oO('folder','[COLOR=dodgerblue][Filter Results][/COLOR] By Countries', 'p', 'addon_countries', '','','','')
    o0oO('folder','[COLOR=dodgerblue][Filter Results][/COLOR] By Kodi Categories', 'p', 'addon_categories', '','','','')
    o0oO('','[COLOR=orange][Kodi Add-on Browser][/COLOR] Install From Zip','','install_from_zip','','','','')
    o0oO('','[COLOR=orange][Kodi Add-on Browser][/COLOR] Browse My Repositories','','browse_repos','','','','')
    o0oO('','[COLOR=orange][Kodi Add-on Browser][/COLOR] Check For Add-on Updates','','check_updates','','','','')
#---------------------------------------------------------------------------------------------------
#Addon removal menu
def Addon_Removal_Menu():
    for file in glob.glob(os.path.join(ADDONS,'*')):
        name      = str(file).replace(ADDONS,'[COLOR=red]REMOVE [/COLOR]').replace('plugin.','[COLOR=dodgerblue](PLUGIN) [/COLOR]').replace('audio.','').replace('video.','').replace('skin.','[COLOR=darkcyan](SKIN) [/COLOR]').replace('repository.','[COLOR=orange](REPOSITORY) [/COLOR]').replace('script.','[COLOR=cyan](SCRIPT) [/COLOR]').replace('metadata.','[COLOR=orange](METADATA) [/COLOR]').replace('service.','[COLOR=pink](SERVICE) [/COLOR]').replace('weather.','[COLOR=green](WEATHER) [/COLOR]').replace('module.','[COLOR=orange](MODULE) [/COLOR]')
        iconimage = (os.path.join(file,'icon.png'))
        fanart    = (os.path.join(file,'fanart.jpg'))
        o0oO('',name,file,'remove_addons',iconimage,fanart,'','')
#-----------------------------------------------------------------------------------------------------------------
#Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
def Android_Path_Check():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        log_path_new = os.path.join(log_path,'xbmc.log')
    else:
        log_path_new = os.path.join(log_path,'kodi.log')
        
    try:
        localfile = open(log_path_new, mode='r')
        content   = localfile.read()
        localfile.close()
    except:
        try:
            localfile = open(os.path.join(HOME,'temp','kodi.log'), mode='r')
            content   = localfile.read()
            localfile.close()
        except:
            try:
                localfile = open(os.path.join(HOME,'temp','xbmc.log'), mode='r')
                content   = localfile.read()
                localfile.close()
            except:
                pass                

    localstoragematch  = re.compile('External storage path = (.+?);').findall(content)
    localstorage       = localstoragematch[0] if (len(localstoragematch) > 0) else ''
    return localstorage
#-----------------------------------------------------------------------------------------------------------------
# Zip up the contents of a directory and all subdirectories, this will exclude the global excludes files such as guisettings.xml
def Archive_Tree(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         =[]
    
    dp.create(message_header, message1, message2, message3)
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files and not 'crashlog' in f and not 'stacktrace' in f]
        
        for file in files:
            
            try:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(0,"Backing Up",'[COLOR darkcyan]%s[/COLOR]'%d, 'Please Wait')
                fn = os.path.join(base, file)
            
            except:
                xbmc.log("Unable to backup file: %s" %file)
            
            if not 'temp' in dirs:
                
                if not AddonID in dirs:
                    
                    try:
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:])  
                    
                    except:
                        xbmc.log("Unable to backup file: %s" %file)
    
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Zip up tree, essentially the same as above but doesn't exclude global excludes (such as guisettings & profiles)
def Archive_File(sourcefile, destfile):
    zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         = []
    
    dp.create("Backing Up Files","Archiving...",'', 'Please Wait')
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR darkcyan]%s[/COLOR]'%file, 'Please Wait')
            fn       = os.path.join(base, file)
            
            if not 'temp' in dirs:
                
                if not AddonID in dirs:
                   
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Check for non ascii files and folders
def ASCII_Check():
    sourcefile   = dialog.browse(3, 'Select the folder you want to scan', 'files', '', False, False)
    rootlen      = len(sourcefile)
    for_progress = []
    ITEM         = []
                
    dp.create('Checking File Structure','','Please wait...','')

    choice = dialog.yesno('Delete or Scan?','Do you want to delete all filenames with special characters or would you rather just scan and view the results in the log?',yeslabel='Delete',nolabel='Scan')
# Create temp files to store the deletion results in
    successascii = open(ascii_results1, mode='w+')
    failedascii  = open(ascii_results2, mode='w+')

    for base, dirs, files in os.walk(sourcefile):
        
        for file in files:
            ITEM.append(file)
    
    N_ITEM =len(ITEM)
    
    for base, dirs, files in os.walk(sourcefile):
        
        dirs[:] = [d for d in dirs]
        files[:] = [f for f in files]
        
        for file in files:

            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(0,"Checking for non ASCII files",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
            
            try:
                file.encode('ascii')

            except UnicodeDecodeError:
                badfile = (str(base)+'/'+str(file)).replace('\\','/').replace(':/',':\\')
#                badfile = unicodedata.normalize('NFKD',unicode(badfile,"ISO-8859-1")).encode("ascii","ignore")
                xbmc.log(" non-ASCII file status logged successfully: %s" % badfile)
                if choice != 1:
                    successascii.write('[COLOR=dodgerblue]Non-ASCII File:[/COLOR]\n')
                    for chunk in chunks(badfile, 75):
                        successascii.write(chunk+'[CR]')
                    successascii.write('\n')
                if choice == 1:
                    try:
                        os.remove(badfile)
                        xbmc.log("### SUCCESS - deleted %s" %badfile)
                        successascii.write('[COLOR=dodgerblue]SUCCESSFULLY DELETED:[/COLOR]\n')
                        for chunk in chunks(badfile, 75):
                            successascii.write(chunk+'[CR]')
                        successascii.write('\n')
                        
                    except:
                        xbmc.log("######## FAILED TO REMOVE: %s" %badfile)
                        xbmc.log("######## Make sure you manually remove this file ##########")
                        failedascii.write('[COLOR=red]FAILED TO DELETE:[/COLOR]\n')
                        for chunk in chunks(badfile, 75):
                            failedascii.write(chunk+'[CR]')
                        failedascii.write('\n')

    failedascii.close()
    successascii.close()

# Create final results by merging success and failed together
    successascii = open(ascii_results1, mode='r')
    successcontent = successascii.read()
    successascii.close()
    failedascii = open(ascii_results2, mode='r')
    failedcontent = failedascii.read()
    failedascii.close()
    if successcontent == '' and failedcontent == '':
        dialog.ok('No Special Characters Found','Great news, all filenames in the path you scanned are ASCII based - no special characters found.' )
    else:
        finalresults = open(ascii_results, mode='w+')
        finalresults.write(successcontent+'\n\n'+failedcontent)
        finalresults.close()
        results = open(ascii_results, mode='r')
        resultscontent = results.read()
        results.close()
        TXT.TXT('Final Results',resultscontent)
        os.remove(ascii_results)
    os.remove(ascii_results1)
    os.remove(ascii_results2)
#---------------------------------------------------------------------------------------------------
#Create backup menu
def Backup_Option():
    o0oO('','[COLOR=darkcyan][INSTRUCTIONS][/COLOR] How to create and share my build','','instructions_1','','','','Back Up Your Full System')
    o0oO('','Create [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Community Build (for sharing on CP)','url','community_backup','','','','Back Up Your Full System')
    if OpenELEC_Check():
        o0oO('','Create OpenELEC Backup (full backup can only be used on OpenELEC)','none','openelec_backup','','','','')
    o0oO('','[COLOR=gold]-----------------------------------------------------------------[/COLOR]','','','','','','')
    o0oO('','Create Universal Build (very old and dated - not recommended)','none','community_backup_2','','','','')
    o0oO('','Create Full Backup (will only work on THIS device)','local','local_backup','','','','Back Up Your Full System')
    o0oO('','Backup Addons Only','addons','restore_zip','','','','Back Up Your Addons')
    o0oO('','Backup Addon Data Only','addon_data','restore_zip','','','','Back Up Your Addon Userdata')
    o0oO('','Backup Guisettings.xml',GUI,'restore_backup','','','','Back Up Your guisettings.xml')
    
    if os.path.exists(FAVS):
        o0oO('','Backup Favourites.xml',FAVS,'restore_backup','Backup.png','','','Back Up Your favourites.xml')
    
    if os.path.exists(SOURCE):
        o0oO('','Backup Source.xml',SOURCE,'restore_backup','Backup.png','','','Back Up Your sources.xml')
    
    if os.path.exists(ADVANCED):
        o0oO('','Backup Advancedsettings.xml',ADVANCED,'restore_backup','Backup.png','','','Back Up Your advancedsettings.xml')
    
    if os.path.exists(KEYMAPS):
        o0oO('','Backup Advancedsettings.xml',KEYMAPS,'restore_backup','Backup.png','','','Back Up Your keyboard.xml')
    
    if os.path.exists(RSS):
        o0oO('','Backup RssFeeds.xml',RSS,'restore_backup','Backup.png','','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
#Backup/Restore root menu
def Backup_Restore():
    o0oO('folder','Backup My Content','none','backup_option','Backup.png','','','')
    o0oO('folder','Restore My Content','none','restore_option','Restore.png','','','')
#---------------------------------------------------------------------------------------------------
#Browse pre-installed repo's via the kodi add-on browser
def Browse_Repos():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://repos/",return)')
#---------------------------------------------------------------------------------------------------
def Build_Info():
    Build = ''
    if os.path.exists('/etc/release'):
        readfile = open('/etc/release','r')
        Build    = readfile.read()
        readfile.close()
    if Build == '':
        version=str(xbmc_version[:2])
        if version < 14:
            logfile = os.path.join(log_path, 'xbmc.log')
    
        else:
            logfile = os.path.join(log_path, 'kodi.log')

        filename    = open(logfile, 'r')
        logtext     = filename.read()
        filename.close()

        Buildmatch  = re.compile('Running on (.+?)\n').findall(logtext)
        Build       = Buildmatch[0] if (len(Buildmatch) > 0) else ''
    return Build.replace(' ','%20')
#---------------------------------------------------------------------------------------------------
#Main category list
def Categories2(localbuildcheck,localversioncheck,id,welcometext):
    if debug == 'true':
        o0oO('','[COLOR=red]WARNING: YOUR BOX IS IN TEST MODE[/COLOR] - Click to disable','', 'testoff', '','','','')
    if id != '0' and id != 'None':
        
        if id != 'Local':
            xbmc.log("### id IS NOT Local, performing update check")
            updatecheck = Check_For_Update(localbuildcheck,localversioncheck,id)
            
            if updatecheck == True:
                
                if not 'Partially installed' in localbuildcheck:
                    o0oO('folder','[COLOR=dodgerblue]'+localbuildcheck+':[/COLOR] [COLOR=lime]NEW VERSION AVAILABLE[/COLOR]',id,'showinfo','','','','')
                    
                if '(Partially installed)' in localbuildcheck:
                    o0oO('folder','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo2','','','','')
            else:
                o0oO('folder','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]'+localbuildcheck+'[/COLOR]',id,'showinfo','','','','')
            
        else:
                
            if localbuildcheck == 'Incomplete':
                o0oO('','[COLOR=darkcyan]Your last restore is not yet completed[/COLOR]','url',Check_Local_Install(),'','','','')
                
            else:
                o0oO('','[COLOR=darkcyan]Current Build Installed: [/COLOR][COLOR=dodgerblue]Local Build ('+localbuildcheck+')[/COLOR]','','','','','','')
    folders = 0
        
    if os.path.exists(CP_PROFILE):
        for name in os.listdir(CP_PROFILE):
            if name != 'Master':
                folders += 1

        if folders>1:
            o0oO('folder','[COLOR=darkcyan]Switch Build Profile[/COLOR]',localbuildcheck,'switch_profile_menu','','','','')

        o0oO('','[COLOR=orange]---------------------------------------[/COLOR]','None','','','','','')

    if OpenELEC_Check():
        o0oO('','[COLOR=darkcyan]Wi-Fi Settings[/COLOR]','', 'openelec_settings', 'Wi-Fi.png','','','')

    o0oO('','[COLOR=dodgerblue]Social TV[/COLOR]','', 'grab_updates', '','','','')
    o0oO('folder','Install Content',sign,'install_content', 'Search_Addons.png','','','')
    o0oO('','Startup Wizard',sign,'startup_wizard', 'Startup_Wizard.png','','','')
    o0oO('folder','Maintenance','none', 'tools', 'Additional_Tools.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Main process to create the addons folder for new community build
def CB_Addon_Install_Loop():
    deps = 'defaultskindependecycheck'
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    
    if not os.path.exists(addonstemp):
        os.makedirs(addonstemp)

    deps = Dependency_Check()
    portalcontent   = Open_URL('http://noobsandnerds.com/TI/AddonPortal/approved.php')

    dp.create('Backing Up Add-ons','','Please Wait...')
    
    for name in os.listdir(ADDONS):

#DO NOT copy over totalinstaller and any dependencies
        if not 'totalinstaller' in name and not 'plugin.program.tbs' in name and not 'packages' in name and not 'repo.' in name and not 'repository' in name and os.path.isdir(os.path.join(ADDONS, name)):

# Check the add-on has a valid repo and is not a dependency of the skin
            if name in portalcontent and not name in deps and not 'repo.' in name and not 'repository.' in name and os.path.isdir(os.path.join(ADDONS, name)):

# Check it's not something that's going to cause issues on startup and also make sure it's a valid directory
                if not 'service.xbmc.versioncheck' in name and not 'packages' in name and os.path.isdir(os.path.join(ADDONS, name)):
                    
                    try:
                        dp.update(0,"Backing Up",'[COLOR darkcyan]%s[/COLOR]'%name, 'Please Wait...')
                        os.makedirs(os.path.join(addonstemp,name))
                        
                        newpath        = os.path.join(addonstemp,name,'addon.xml')
                        newpathdefault = os.path.join(addonstemp,name,'default.py')
                        filefix        = open(os.path.join(ADDONS,name,'addon.xml'), mode='r')
                        content        = filefix.read()
                        filefix.close()
                        
                        localnamematch     = re.compile(' name="(.+?)"').findall(content)
                        localprovidermatch = re.compile('provider-name="(.+?)"').findall(content)
                        localmatch         = re.compile('<addon[\s\S]*?">').findall(content)
                        descmatch          = re.compile('<description[\s\S]*?<\/description>').findall(content)
                        namematch          = localnamematch[0] if (len(localnamematch) > 0) else 'None'
                        providernamematch  = localprovidermatch[0] if (len(localprovidermatch) > 0) else 'Anonymous'
                        localcontentmatch  = localmatch[0] if (len(localmatch) > 0) else 'None'
                        descriptionmatch   = descmatch[0] if (len(descmatch) > 0) else 'None'
                        
                        newversion = '<addon id="'+name+'" name="'+namematch+'" version="0" provider-name="'+providernamematch+'">'
                        description = '<description>If you\'re seeing this message it means the add-on is still updating, please wait for the update process to complete.</description>'
                        
                        if localcontentmatch!='None':
                            replacefile = content.replace(descriptionmatch,description).replace(localcontentmatch,newversion)
                        
                        else:
                            replacefile = content.replace(descriptionmatch,description)

                        writefile = open(newpath, mode='w+')
                        writefile.write(str(replacefile))
                        writefile.close()
                        writefile2 = open(newpathdefault, mode='w+')
                        writefile2.write('import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys\nAddonID="'+name+'"\nAddonName="'+namematch+'"\ndialog=xbmcgui.Dialog()\ndialog.ok(AddonName+" Add-on Requires Update","This add-on may still be in the process of the updating so we recommend waiting a few minutes to see if it updates naturally. If it hasn\'t updated after 5mins please try reinstalling via the Maintenance add-on")\nxbmcplugin.endOfDirectory(int(sys.argv[1]))')
                        writefile2.close()
                    
                    except:
                        xbmc.log("### Failed to backup: %s" %name)

# If it's not in a repo or it's a skin dependency copy the whole add-on over
            else:
                try:
                    shutil.copytree(os.path.join(ADDONS,name), os.path.join(addonstemp,name))
                except:
                    xbmc.log("### Failed to copy: %s" %name)
    
    dp.close()
    
    message_header = "Creating Backup"
    message1       = "Archiving..."
    message2       = ""
    message3       = "Please Wait"
    
    Archive_Tree(addonstemp, backupaddonspath, message_header, message1, message2, message3, '', '')
    
    try:
        shutil.rmtree(addonstemp)
    
    except:
        xbmc.log("### COMMUNITY BUILDS: Failed to remove temp addons folder - manual delete required ###")
#-----------------------------------------------------------------------------------------------------------------
# Final install process for CB (Addon loop)
def CB_Install_Final(url):
    dp.create('Cleaning Temp Paths','','Please wait...')
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    
    if not os.path.exists(addonstemp):
        os.makedirs(addonstemp)
    
    extract.all(backupaddonspath, addonstemp)
    portalcontent = Open_URL('http://noobsandnerds.com/TI/AddonPortal/approved.php')
    writefile = open(successtxt, mode='w+')
    writefile.write('[COLOR=dodgerblue][B]'+url+'[/B][/COLOR] - Install results[CR][CR][COLOR=darkcyan]IMPORTANT INFORMATION:[/COLOR][CR]Only content avaialable on the official Kodi repo and marked as approved will be installed via the Community Builds function. Please check the details below to see what was successfully installed and what was not. We realise some content may only be unlawful in certain countries so if you have the relevant repositories installed prior to installing a build then all the build content will install.[CR][CR][COLOR=dodgerblue]INSTALL REPORT:[/COLOR][CR]')
    
    for name in os.listdir(addonstemp):
        
        if not 'totalinstaller' in name and not 'plugin.program.tbs' in name and not 'packages' in name and not 'repo.' in name and not 'repository' in name:
            
            if name in portalcontent:
                repomatch = re.compile('i="'+name+'"r="(.+?)"').findall(portalcontent)
                reponame = repomatch[0] if (len(repomatch) > 0) else 'None'
                
                if os.path.exists(os.path.join(ADDONS,reponame)) or reponame=='repository.xbmc.org' and not 'metadata' in name:
                    
                    if not os.path.exists(os.path.join(ADDONS,name)):
                        os.rename(os.path.join(addonstemp,name),os.path.join(ADDONS,name))
                        xbmc.log("### Successfully installed: %s" %name)
                        writefile.write('[COLOR=lime][SUCCESS][/COLOR] '+name+'[CR]')
                    
                    else:
                        xbmc.log("### "+name+" Already exists on system")
                
                if reponame!="repository.xbmc.org" and not os.path.exists(os.path.join(ADDONS,reponame)):
                    xbmc.log("### Cannot install "+name+" - you need the following repo pre-installed: %s" %reponame)
                    writefile.write('[COLOR=red][FAILED][/COLOR] '+name+" - you need the following repo pre-installed: [COLOR=darkcyan]"+reponame+'[CR][/COLOR]')
            
            else:
                
                if not os.path.exists(os.path.join(ADDONS,name)):
                    choice=dialog.yesno('[COLOR=darkcyan]Unknown Add-on Detected[/COLOR]','This build contains content that can\'t be verified','against the Addon Portal. Would you like to install:[COLOR=dodgerblue]',name+'[/COLOR]')
                    
                    if choice==1:
                        os.rename(os.path.join(addonstemp,name),os.path.join(ADDONS,name))
                        xbmc.log("### Successfully installed: %s" %name)
                        writefile.write('[COLOR=lime][SUCCESS][/COLOR] '+name+" - [COLOR=darkcyan]This could not be verified but you accepted to install.[/COLOR][CR]")
                    
                    else:
                        xbmc.log("### "+name+" Not installed")
                        writefile.write('[COLOR=red][FAILED][/COLOR] '+name+" - [COLOR=darkcyan]This could not be verified and you chose not to instsall.[/COLOR][CR]")
                else:
                    xbmc.log("### "+name+" Already exists on system")
    
    writefile.close()
#---------------------------------------------------------------------------------------------------
#Show full description of build
def CB_Install_Results():
    successfile    = open(successtxt, mode='r')
    successcontent = successfile.read()
    successfile.close()
    TXT.TXT('Community Build Install Results',successcontent)
#---------------------------------------------------------------------------------------------------
# Disclaimer popup prior to opening the main CB menu. Means user has to click to proceed and also fixes issue with popup keep opening during backup
def CB_Root_Menu(welcometext):
    pop('disclaimer.xml')
    o0oO('folder','I have read and understand the disclaimer.','welcome','CB_Menu','Community_Builds.png','','','')        
#-----------------------------------------------------------------------------------------------------------------
#Build the root search menu for installing community builds    
def CB_Menu(welcometext):
    if xbmc.getCondVisibility('system.platform.android'):
        localstorage   = Android_Path_Check()
        downloadfolder = os.path.join(localstorage,'Download')
        try:
            if not os.path.exists(downloadfolder):
                os.makedirs(downloadfolder)
        except:
            xbmc.log("### Failed to make download folder")
    
        if not os.path.exists('/data/data/com.rechild.advancedtaskkiller'):
            choice = dialog.yesno('Advanced Task Killer Required','To be able to us features such as the backup/restore and community builds you need the Advanced Task Killer app installed. Would you like to download it now?')
            if choice == 1:
                dp.create('Downloading APK file','','','')
                try:
                    downloader.download('https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk',os.path.join(downloadfolder,'AdvancedTaskKiller.apk'))
                    dialog.ok('Download Complete',"The apk file has now been downloaded, you'll find this in your downloads folder. Just install this exactly the same as you would any other apk file - click on it and then click through the setup screen. The file is called AdvancedTaskKiller.apk")
                except:
                    try:
                        downloader.download('https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk',os.path.join('storage','emulated','legacy','Download','AdvancedTaskKiller.apk'))
                        dialog.ok('Download Complete',"The AdvancedTaskKiller.apk file has now been downloaded, you'll find this in your downloads folder. You'll need a File Manager app to install this file, we recommend installing ES File Explorer - just do a search for this on your box/stick.")
                    except:
                        dialog.ok('Download Failed','It wasn\'t possible to download the Advanced Task Killer, without it you will almost certainly run into problems so make sure you get it installed otherwise you\'ll need to manually force close and switching profiles may fail.')
                        
 
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    versionfloat = float(xbmc_version[:2])
    version      = int(versionfloat)
    
    if reseller=='true':
        
        if openelec=='true':
            Reseller_Check('yes')
        
        if openelec=='false':
            Reseller_Check('no')
    
    if privatebuilds=='true':
        o0oO('folder','[COLOR=dodgerblue]Show My Private List[/COLOR]','&visibility=private','grab_builds','Private_builds.png','','','')        
    
    if (version < 14) or (versionoverride=='true'):
        o0oO('folder','[COLOR=dodgerblue]Show All Gotham Compatible Builds[/COLOR]','&xbmc=gotham&visibility=public','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
        
    if (version == 14) or (versionoverride=='true'):
        o0oO('folder','[COLOR=dodgerblue]Show All Helix Compatible Builds[/COLOR]','&xbmc=helix&visibility=public','grab_builds','TRCOMMUNITYHELIXBUILDS.png','','','')
        
    if (version == 15) or (versionoverride=='true'):
        o0oO('folder','[COLOR=dodgerblue]Show All Isengard Compatible Builds[/COLOR]','&xbmc=isengard&visibility=public','grab_builds','TRCOMMUNITYHELIXBUILDS.png','','','')
    if (version == 16) or (versionoverride=='true'):
        o0oO('folder','[COLOR=dodgerblue]Show All Jarvis Compatible Builds[/COLOR]','&xbmc=jarvis&visibility=public','grab_builds','TRCOMMUNITYHELIXBUILDS.png','','','')
    if wizardurl1 != '':
        o0oO('folder','[COLOR=darkcyan]Show '+wizardname1+' Builds[/COLOR]','&id=1','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
    if wizardurl2 != '':
        o0oO('folder','[COLOR=darkcyan]Show '+wizardname2+' Builds[/COLOR]','&id=2','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
    if wizardurl3 != '':
        o0oO('folder','[COLOR=darkcyan]Show '+wizardname3+' Builds[/COLOR]','&id=3','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
    if wizardurl4 != '':
        o0oO('folder','[COLOR=darkcyan]Show '+wizardname4+' Builds[/COLOR]','&id=4','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
    if wizardurl5 != '':
        o0oO('folder','[COLOR=darkcyan]Show '+wizardname5+' Builds[/COLOR]','&id=5','grab_builds','TRCOMMUNITYGOTHAMBUILDS.png','','','')
    
    o0oO('','Create My Own Community Build','url','community_backup','Backup.png','','','Back Up Your Full System')
    
    if os.path.exists(successtxt):
        o0oO('','View Results Of Previous Community Build Install','','cb_install_results','View_Log.png','','','Community Build install results. Find out what installed and what didn\'t with details of why.')
#---------------------------------------------------------------------------------------------------
#gotham to helix skin function for keyboard fix
def changekeys(skin):
    left       = '<onleft>%s</onleft>'
    right      = '<onright>%s</onright>'
    up         = '<onup>%s</onup>'
    down       = '<ondown>%s</ondown>'
    button     = '<control type="button" id="%s">'    

# New keyboard letter codes
    LETTER     = [
        ('65','140'),
        ('66','164'),
        ('67','162'),
        ('68','142'),
        ('69','122'),
        ('70','143'),
        ('71','144'),
        ('72','145'),
        ('73','127'),
        ('74','146'),
        ('75','147'),
        ('76','148'),
        ('77','166'),
        ('78','165'),
        ('79','128'),
        ('80','129'),
        ('81','120'),
        ('82','123'),
        ('83','141'),
        ('84','124'),
        ('85','126'),
        ('86','163'),
        ('87','121'),
        ('88','161'),
        ('89','125'),
        ('90','160')]
    
    for old , new in LETTER:
        a      = open(skin).read()  
        CHANGE = a.replace(button%old,button%new).replace(left%old,left%new).replace(right%old,right%new).replace(up%old,up%new).replace(down%old,down%new)
        f      = open(skin, mode='w')
        f.write(CHANGE)
        f.close()   
#---------------------------------------------------------------------------------------------------
def changenumber(u,skin):
    left   = '<onleft>%s</onleft>'
    right  = '<onright>%s</onright>'
    up     = '<onup>%s</onup>'
    down   = '<ondown>%s</ondown>'
    button = '<control type="button" id="%s">'
    
    if u < 49:
        NEW=u+ 61
    
    else:    
        NEW=u+ 51
    
    a       = open(skin).read()
    CHANGE  = a.replace(left%u,left%NEW).replace(right%u,right%NEW).replace(up%u,up%NEW).replace(down%u,down%NEW).replace(button%u,button%NEW)
    f       = open(skin, mode='w')
    f.write(CHANGE)
    f.close()
#-----------------------------------------------------------------------------------------------------------------
def Check_Build_Addons(description):
    profile_path        = os.path.join(CP_PROFILE,'extracted')
    temp_path           = os.path.join(CP_PROFILE,'temp')
    profile_addon_path  = os.path.join(profile_path,'userdata','.cbcfg')
    profile_addons_list = os.path.join(CP_PROFILE, description, 'addonlist')
    profile_addons      = open(profile_addons_list, 'w+')
    mainaddons          = []

    if not os.path.exists(os.path.join(CP_PROFILE, description)):
        os.makedirs(os.path.join(CP_PROFILE, description))
        if debug == 'true':
            xbmc.log("### (line 1147) Created: "+os.path.join(CP_PROFILE, description))
    if not os.path.exists(ADDONS_MASTER):
        os.makedirs(ADDONS_MASTER)
        if debug == 'true':
            xbmc.log("### (line 1450) Created: "+ADDONS_MASTER)
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        if debug == 'true':
            xbmc.log("### (line 1453) Removed: "+temp_path)
# Create a temp directory for addons in zip
    if os.path.exists(profile_addon_path):
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
            if debug == 'true':
                xbmc.log("### (line 1458) Created: "+temp_path)
        extract.all(profile_addon_path, temp_path, dp)
        xbmc.log("### NEW STYLE BUILD")
        if debug == 'true':
            xbmc.log("### (line 1461) Extracted "+profile_addon_path+" to: "+temp_path)
    elif os.path.exists(os.path.join(profile_path,'addons')):
        os.rename(os.path.join(profile_path,'addons'), temp_path)
        xbmc.log("### OLD BUILD - RENAMED ADDONS FOLDER")
        if debug == 'true':
            xbmc.log("### (line 1465) renamed "+os.path.join(profile_path,'addons')+" to "+temp_path)
    
    dp.create('Copying Addons','','','')
# Create list of main 
    for name in os.listdir(KODI_ADDONS):
        mainaddons.append(name)

    for name in os.listdir(ADDONS):
        mainaddons.append(name)

    if os.path.exists(ADDONS_MASTER):
        for name in os.listdir(ADDONS_MASTER):
            if not name in mainaddons:
                mainaddons.append(name)

# copy all the addons to addonstemp folder in userdata and create a backup folder for any that may get uninstalled by a user but still required in other builds. Copying to backup folder now done when switching profile so commented that out for now.
    if not os.path.exists(os.path.join(ADDONS_MASTER, 'backups')):
        os.makedirs(os.path.join(ADDONS_MASTER, 'backups'))
        if debug == 'true':
            xbmc.log("### Created: "+os.path.join(ADDONS_MASTER, 'backups'))
    for name in os.listdir(temp_path):
        try:
#            shutil.copytree(os.path.join(temp_path, name), os.path.join(ADDONS_MASTER, 'backups', name))
#            dp.update(0,"Backing Up...",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
            profile_addons.write(name+'|')
            if debug == 'true':
                xbmc.log("### Added: %s" % os.path.join(ADDONS_MASTER, 'backups', name))
                xbmc.log("### Added %s to %s" % (name, profile_addons))
        except:
            pass

        if not name in mainaddons:
            try:
                os.rename(os.path.join(temp_path, name), os.path.join(ADDONS_MASTER, name))
                dp.update(0,"Configuring",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
                if debug == 'true':
                    xbmc.log("### Renamed from %s to %s" % (os.path.join(temp_path, name), os.path.join(ADDONS_MASTER, name)))
            except:
                pass

    profile_addons.close()
    shutil.rmtree(temp_path)
    shutil.rmtree(profile_path)
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def Check_Download_Path():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    
    if not os.path.exists(zip):
        dialog.ok('Download/Storage Path Check','The download location you have stored does not exist .\nPlease update the addon settings and try again.') 
        ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
#Check to see if a new version of a build is available
def Check_New_Menu():
    BaseURL = 'http://noobsandnerds.com/TI/menu_check'
    link    = Open_URL(BaseURL).replace('\n','').replace('\r','')
    menumatch = re.compile('d="(.+?)"').findall(link)
    menu  = menumatch[0] if (len(menumatch) > 0) else ''
    if menu != '':
        return menu
    else:
        return "none"
#---------------------------------------------------------------------------------------------------
#Check to see if a new version of a build is available
def Check_For_Update(localbuildcheck,localversioncheck,id):
    BaseURL = 'http://noobsandnerds.com/TI/Community_Builds/buildupdate.php?id=%s' % (id)
    link    = Open_URL(BaseURL).replace('\n','').replace('\r','')
    
    if id != 'None':
        versioncheckmatch = re.compile('version="(.+?)"').findall(link)
        versioncheck  = versioncheckmatch[0] if (len(versioncheckmatch) > 0) else ''
    
        if  localversioncheck < versioncheck:
            return True
    
    else:
        return False
#---------------------------------------------------------------------------------------------------
#Create restore menu
def Check_Local_Install():
    localfile        = open(idfile, mode='r')
    content          = localfile.read()
    localfile.close()
    
    localbuildmatch  = re.compile('name="(.+?)"').findall(content)
    localbuildcheck  = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''
    
    if localbuildcheck == "Incomplete":
        choice = xbmcgui.Dialog().yesno("Finish Restore Process", 'If you\'re certain the correct skin has now been set click OK', 'to finish the install process, once complete XBMC/Kodi will', ' then close. Do you want to finish the install process?', yeslabel='Yes',nolabel='No')
        
        if choice == 1:
            Finish_Local_Restore()
        
        elif choice == 0:
            return
#---------------------------------------------------------------------------------------------------
def CheckPath():
    path = xbmc.translatePath(os.path.join(zip,'testCBFolder'))
    
    try:
        os.makedirs(path)
        os.removedirs(path)
        dialog.ok('[COLOR=lime]SUCCESS[/COLOR]', 'Great news, the path you chose is writeable.', 'Some of these builds are rather big, we recommend a minimum of 1GB storage space.')
    
    except:
        dialog.ok('[COLOR=red]CANNOT WRITE TO PATH[/COLOR]', 'Kodi cannot write to the path you\'ve chosen. Please click OK in the settings menu to save the path then try again. Some devices give false results, we recommend using a USB stick as the backup path.')
#---------------------------------------------------------------------------------------------------
# Split string into arrays
def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]
#---------------------------------------------------------------------------------------------------
#Function to clean HTML into plain text. Not perfect but it's better than raw html code!
def Clean_HTML(data):        
    data = data.replace('</p><p>','[CR][CR]').replace('&ndash;','-').replace('&mdash;','-').replace("\n", " ").replace("\r", " ").replace("&rsquo;", "'").replace("&rdquo;", '"').replace("</a>", " ").replace("&hellip;", '...').replace("&lsquo;", "'").replace("&ldquo;", '"')
    data = " ".join(data.split())   
    p    = re.compile(r'< script[^<>]*?>.*?< / script >')
    data = p.sub('', data)
    p    = re.compile(r'< style[^<>]*?>.*?< / style >')
    data = p.sub('', data)
    p    = re.compile(r'')
    data = p.sub('', data)
    p    = re.compile(r'<[^<]*?>')
    data = p.sub('', data)
    data = data.replace('&nbsp;',' ')
    return data
#---------------------------------------------------------------------------------------------------
def Cleanup_Old_Textures():
# Thanks to xunity maintenance tool for this code, this will remove old stale textures not used in past 14 days
    path           = xbmc.translatePath('special://home/userdata/Database')
    files          = glob.glob(os.path.join(path, 'Textures*.db'))
    ver            = 0
    dbPath         = ''

    # Find the highest version number of textures, it's always been textures13.db but you can never be too careful!
    for file in files:
        dbversion = int(re.compile('extures(.+?).db').findall(file)[0])
        if ver < dbversion:
            ver     = dbversion
            dbPath  = file

    db   = xbmc.translatePath(dbPath)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

    # Set paramaters to check in db, cull = the datetime (we've set it to 14 days) and useCount is the amount of times the file has been accessed
    cull     = datetime.datetime.today() - datetime.timedelta(days = 14)
    useCount = 10

    # Create an array to store paths for images and ids for database
    ids    = []
    images = []

    c.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (useCount, str(cull)))

    for row in c:
        ids.append(row["idtexture"])

    for id in ids:
        c.execute("SELECT cachedurl FROM texture WHERE id = ?", (id,))
        for row in c:
            images.append(row["cachedurl"])

    xbmc.log("### Automatic Cache Removal: %d Old Textures removed" % len(images))

    #clean up database
    for id in ids:       
        c.execute("DELETE FROM sizes   WHERE idtexture = ?", (id,))
        c.execute("DELETE FROM texture WHERE id        = ?", (id,))

    c.execute("VACUUM")
    conn.commit()
    c.close()

    #delete files
    thumbfolder = xbmc.translatePath('special://home/userdata/Thumbnails')
    for image in images:
        path = os.path.join(thumbfolder, image)
        try:
            os.remove(path)
        except:
            pass

#---------------------------------------------------------------------------------------------------
#Function to clear all known cache files
def Cleanup_Partial_Install():
    if os.path.exists(os.path.join(CP_PROFILE,'extracted')):
        try:
            shutil.rmtree(os.path.join(CP_PROFILE,'extracted'))
        except:
            xbmc.log("### Unsuccessful Community Build Install detected, unabled to remove extracted folder")

    if os.path.exists(os.path.join(CP_PROFILE,'temp')):
        try:
            shutil.rmtree(os.path.join(CP_PROFILE,'temp'))
        except:
            xbmc.log("### Unsuccessful Community Build Install detected, unabled to remove temp folder")
#---------------------------------------------------------------------------------------------------
#Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear All Known Cache?', 'This will clear all known cache files and can help if you\'re encountering kick-outs during playback as well as other random issues. There is no harm in using this.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Wipe_Cache()
        Remove_Textures_Dialog()
#---------------------------------------------------------------------------------------------------
#Build Countries Menu (First Filter)    
def Countries(url):
    o0oO('folder','African',str(url)+'&genre=african','grab_builds','african.png','','','')
    o0oO('folder','Arabic',str(url)+'&genre=arabic','grab_builds','arabic.png','','','')
    o0oO('folder','Asian',str(url)+'&genre=asian','grab_builds','asian.png','','','')
    o0oO('folder','Australian',str(url)+'&genre=australian','grab_builds','australian.png','','','')
    o0oO('folder','Austrian',str(url)+'&genre=austrian','grab_builds','austrian.png','','','')
    o0oO('folder','Belgian',str(url)+'&genre=belgian','grab_builds','belgian.png','','','')
    o0oO('folder','Brazilian',str(url)+'&genre=brazilian','grab_builds','brazilian.png','','','')
    o0oO('folder','Canadian',str(url)+'&genre=canadian','grab_builds','canadian.png','','','')
    o0oO('folder','Columbian',str(url)+'&genre=columbian','grab_builds','columbian.png','','','')
    o0oO('folder','Czech',str(url)+'&genre=czech','grab_builds','czech.png','','','')
    o0oO('folder','Danish',str(url)+'&genre=danish','grab_builds','danish.png','','','')
    o0oO('folder','Dominican',str(url)+'&genre=dominican','grab_builds','dominican.png','','','')
    o0oO('folder','Dutch',str(url)+'&genre=dutch','grab_builds','dutch.png','','','')
    o0oO('folder','Egyptian',str(url)+'&genre=egyptian','grab_builds','egyptian.png','','','')
    o0oO('folder','Filipino',str(url)+'&genre=filipino','grab_builds','filipino.png','','','')
    o0oO('folder','Finnish',str(url)+'&genre=finnish','grab_builds','finnish.png','','','')
    o0oO('folder','French',str(url)+'&genre=french','grab_builds','french.png','','','')
    o0oO('folder','German',str(url)+'&genre=german','grab_builds','german.png','','','')
    o0oO('folder','Greek',str(url)+'&genre=greek','grab_builds','greek.png','','','')
    o0oO('folder','Hebrew',str(url)+'&genre=hebrew','grab_builds','hebrew.png','','','')
    o0oO('folder','Hungarian',str(url)+'&genre=hungarian','grab_builds','hungarian.png','','','')
    o0oO('folder','Icelandic',str(url)+'&genre=icelandic','grab_builds','icelandic.png','','','')
    o0oO('folder','Indian',str(url)+'&genre=indian','grab_builds','indian.png','','','')
    o0oO('folder','Irish',str(url)+'&genre=irish','grab_builds','irish.png','','','')
    o0oO('folder','Italian',str(url)+'&genre=italian','grab_builds','italian.png','','','')
    o0oO('folder','Japanese',str(url)+'&genre=japanese','grab_builds','japanese.png','','','')
    o0oO('folder','Korean',str(url)+'&genre=korean','grab_builds','korean.png','','','')
    o0oO('folder','Lebanese',str(url)+'&genre=lebanese','grab_builds','lebanese.png','','','')
    o0oO('folder','Mongolian',str(url)+'&genre=mongolian','grab_builds','mongolian.png','','','')
    o0oO('folder','Nepali',str(url)+'&genre=nepali','grab_builds','nepali.png','','','')
    o0oO('folder','New Zealand',str(url)+'&genre=newzealand','grab_builds','newzealand.png','','','')
    o0oO('folder','Norwegian',str(url)+'&genre=norwegian','grab_builds','norwegian.png','','','')
    o0oO('folder','Pakistani',str(url)+'&genre=pakistani','grab_builds','pakistani.png','','','')
    o0oO('folder','Polish',str(url)+'&genre=polish','grab_builds','polish.png','','','')
    o0oO('folder','Portuguese',str(url)+'&genre=portuguese','grab_builds','portuguese.png','','','')
    o0oO('folder','Romanian',str(url)+'&genre=romanian','grab_builds','romanian.png','','','')
    o0oO('folder','Russian',str(url)+'&genre=russian','grab_builds','russian.png','','','')
    o0oO('folder','Singapore',str(url)+'&genre=singapore','grab_builds','singapore.png','','','')
    o0oO('folder','Spanish',str(url)+'&genre=spanish','grab_builds','spanish.png','','','')
    o0oO('folder','Swedish',str(url)+'&genre=swedish','grab_builds','swedish.png','','','')
    o0oO('folder','Swiss',str(url)+'&genre=swiss','grab_builds','swiss.png','','','')
    o0oO('folder','Syrian',str(url)+'&genre=syrian','grab_builds','syrian.png','','','')
    o0oO('folder','Tamil',str(url)+'&genre=tamil','grab_builds','tamil.png','','','')
    o0oO('folder','Thai',str(url)+'&genre=thai','grab_builds','thai.png','','','')
    o0oO('folder','Turkish',str(url)+'&genre=turkish','grab_builds','turkish.png','','','')
    o0oO('folder','UK',str(url)+'&genre=uk','grab_builds','uk.png','','','')
    o0oO('folder','USA',str(url)+'&genre=usa','grab_builds','usa.png','','','')
    o0oO('folder','Vietnamese',str(url)+'&genre=vietnamese','grab_builds','vietnamese.png','','','')
#---------------------------------------------------------------------------------------------------
# OLD METHOD to create a community (universal) backup - this renames paths to special:// and removes unwanted folders
def Community_Backup_OLD():
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    guisuccess=1
    Check_Download_Path()
    fullbackuppath  = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds',''))
    myfullbackup    = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup.zip'))
    myfullbackupGUI = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup_GUI_Settings.zip'))
    
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    
    vq = Get_Keyboard( heading="Enter a name for this backup" )
    if ( not vq ):
        return False, 0
    
    title              = urllib.quote_plus(vq)
    backup_zip         = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs_full  =  [AddonID]
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
    exclude_dirs       =  [AddonID, 'cache', 'system', 'Thumbnails', "peripheral_data",'library','keymaps']
    exclude_files      = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    if mastercopy=='true':
        Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    
    choice = xbmcgui.Dialog().yesno("Do you want to include your addon_data folder?", 'This contains ALL addon settings including passwords but may also contain important information such as skin shortcuts. We recommend MANUALLY removing the addon_data folders that aren\'t required.', yeslabel='Yes',nolabel='No')
    
    if choice == 0:
        exclude_dirs = [AddonID, 'cache', 'system', 'peripheral_data','library','keymaps','addon_data','Thumbnails']

    elif choice == 1:
        pass
    
    Fix_Special(HOME)
    Archive_Tree(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)

    GUIname = xbmc.translatePath(os.path.join(fullbackuppath, title+'_guisettings.zip'))
    zf      = zipfile.ZipFile(GUIname, mode='w')
    
    try:
        zf.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
    except:
        guisuccess=0
    
    try:
        zf.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
    except:
        pass
    
    zf.close()
    
    if mastercopy=='true':
        zfgui = zipfile.ZipFile(myfullbackupGUI, mode='w')
        try:
            zfgui.write(GUI, 'guisettings.xml', zipfile.ZIP_DEFLATED) #Copy guisettings.xml
        except:
            guisuccess=0

        try:
            zfgui.write(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), 'profiles.xml', zipfile.ZIP_DEFLATED) #Copy profiles.xml
        except:
            pass
        zfgui.close()
    
        if guisuccess == 0:
            dialog.ok("FAILED!", 'The guisettings.xml file could not be found on your system, please reboot and try again.', '','')
        
        else:
            dialog.ok("SUCCESS!", 'You Are Now Backed Up and can share this build with the community.')
            
            if mastercopy=='true':
                dialog.ok("Build Locations", 'Full Backup (only used to restore on this device): [COLOR=dodgerblue]'+myfullbackup, '[/COLOR]Universal Backup: [COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
            
            else:
                dialog.ok("Build Location", 'Universal Backup:[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# Create a community (universal) backup - this does a whole load of clever stuff!
def Community_Backup():
    Check_Download_Path()

    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)

    choice = dialog.yesno('Create noobsandnerds Build','This backup will only work if you share your build on the [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] portal with the rest of the community. It will not work with any other installer/wizard, do you wish to continue?')
    
    if choice == 1:
        dp.create('Checking File Structure','','Please wait','')
        if not os.path.exists(GUIzipfolder):
            os.makedirs(GUIzipfolder)
            
        guisuccess      = 1
        fullbackuppath  = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds',''))
        myfullbackup    = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup.zip'))
        myfullbackupGUI = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup_GUI_Settings.zip'))
        
        if not os.path.exists(fullbackuppath):
            os.makedirs(fullbackuppath)
        
        vq = Get_Keyboard( heading="Enter a name for this backup" )
        
        if ( not vq ):
            return False, 0
        
        title      = urllib.quote_plus(vq)
        backup_zip = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))

    # Files and folders to exclude in backup process (FULL is for the full backup option - if enabled in settings)
        exclude_dirs_full  =  [AddonID]
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
        exclude_dirs       =  [AddonID, 'cache', 'system', 'addons', 'Thumbnails', "peripheral_data",'library','keymaps','script.module.metahandler','script.artistslideshow','ArtistSlideshow']
        exclude_files      = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Thumbs.db','.gitignore']
        message_header     = "Creating full backup of existing build"
        message_header2    = "Creating Community Build"
        message1           = "Archiving..."
        message2           = ""
        message3           = "Please Wait"
        
    # If option to create a full build is ticked in settings
        if mastercopy=='true':
            Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
        
        choice = xbmcgui.Dialog().yesno("Do you want to include your addon_data folder?", 'This contains ALL addon settings including passwords but may also contain important information such as skin shortcuts. We recommend MANUALLY removing the addon_data folders that aren\'t required.', yeslabel='Yes',nolabel='No')

    # If the user doesn't want to include addon_data in the backup add these exlude options
        if choice == 0:
            exclude_dirs = [AddonID, 'cache', 'system', 'addons', 'peripheral_data','library','keymaps','addon_data','Thumbnails']

        elif choice == 1:
            pass

    # Call functions to create the addons backup and change the paths to special then archive
        CB_Addon_Install_Loop()
        Fix_Special(HOME)
        Archive_Tree(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  

    # Clean up files
        try:
            os.remove(backupaddonspath)    
        except:
            pass
        
        try:
            os.remove(addonstemp)
        except:
            pass
        
        time.sleep(1)

    # Create a guisettings zip and add profiles if they exist
        GUIname = xbmc.translatePath(os.path.join(fullbackuppath, title+'_guisettings.zip'))
        
        try:
            shutil.copyfile(GUI,os.path.join(GUIzipfolder,'guisettings.xml'))
            if debug == 'true':
                xbmc.log("### Successfully copied guisettings to : "+os.path.join(GUIzipfolder,'guisettings.xml'))
        except:
            if debug == 'true':
                xbmc.log("### FAILED TO copy guisettings to : "+os.path.join(GUIzipfolder,'guisettings.xml'))
            guisuccess=0
        
        try:
            shutil.copyfile(xbmc.translatePath(os.path.join(HOME,'userdata','profiles.xml')), xbmc.translatePath(os.path.join(GUIzipfolder,'profiles.xml')))
            xbmc.log("### Successfully copied profiles to : "+os.path.join(GUIzipfolder,'profiles.xml'))
        except:
            pass
        
        skinshortcuts = os.path.join(ADDON_DATA,'script.skinshortcuts')
        if os.path.exists(skinshortcuts):
            try:
                shutil.copytree(os.path.join(ADDON_DATA,'script.skinshortcuts'), os.path.join(GUIzipfolder,'script.skinshortcuts'))
                if debug == 'true':
                    xbmc.log("### Successfully copied skinshortcuts to : "+os.path.join(GUIzipfolder,'script.skinshortcuts'))
            except:
                dialog.ok('Failed to copy Skin Shortcuts','There was an error trying to backup your script.skinshortcuts, please try again and if you continue to receive this message upload a log and send details to the noobsandnerds forum.')
                if debug == 'true':
                    xbmc.log("### FAILED to copy skinshortcuts to: %s" % os.path.join(GUIzipfolder,'script.skinshortcuts'))

        Archive_File(GUIzipfolder, GUIname)

#        zf.close()

# If it's the option to keep a full build then also create a guisettings.zip for that
        if mastercopy=='true':
            Archive_File(GUIzipfolder, myfullbackupGUI)

# Remove the temp guisettings, skinshortcuts and profiles folder
        if os.path.exists(GUIzipfolder):
            shutil.rmtree(GUIzipfolder)
            
        if guisuccess == 0:
            dialog.ok('ERROR','There was an error backing up your guisettings.xml, you cannot share a build without one so please try again. If this keeps happening please upload a log and contact the noobsandnerds forum with details.')
        
        else:
            dialog.ok("SUCCESS!", 'You Are Now Backed Up and can share this build with the community.')
            
            if mastercopy=='true':
                dialog.ok("Build Locations", 'Full Backup (only used to restore on this device): [COLOR=dodgerblue]'+myfullbackup, '[/COLOR]Universal Backup (this will ONLY work for sharing on the [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] portal):[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
            
            else:
                dialog.ok("Build Location", '[COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR] Backup (this will ONLY work for sharing on the Community Portal):[CR][COLOR=dodgerblue]'+backup_zip+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Community_Menu(url,video):
    Cleanup_Partial_Install()
    BaseURL            = 'http://noobsandnerds.com/TI/Community_Builds/community_builds_premium.php?id=%s' % (url)
    link               = Open_URL(BaseURL).replace('\n','').replace('\r','')
    pathmatch          = re.compile('path="(.+?)"').findall(link)
    artpathmatch       = re.compile('myart="(.+?)"').findall(link)
    artpackmatch       = re.compile('artpack="(.+?)"').findall(link)
    videopreviewmatch  = re.compile('videopreview="(.+?)"').findall(link)
    videoguide1match   = re.compile('videoguide1="(.+?)"').findall(link)
    videoguide2match   = re.compile('videoguide2="(.+?)"').findall(link)
    videoguide3match   = re.compile('videoguide3="(.+?)"').findall(link)
    videoguide4match   = re.compile('videoguide4="(.+?)"').findall(link)
    videoguide5match   = re.compile('videoguide5="(.+?)"').findall(link)
    videolabel1match   = re.compile('videolabel1="(.+?)"').findall(link)
    videolabel2match   = re.compile('videolabel2="(.+?)"').findall(link)
    videolabel3match   = re.compile('videolabel3="(.+?)"').findall(link)
    videolabel4match   = re.compile('videolabel4="(.+?)"').findall(link)
    videolabel5match   = re.compile('videolabel5="(.+?)"').findall(link)
    namematch          = re.compile('name="(.+?)"').findall(link)
    authormatch        = re.compile('author="(.+?)"').findall(link)
    versionmatch       = re.compile('version="(.+?)"').findall(link)
    descmatch          = re.compile('description="(.+?)"').findall(link)
    downloadmatch      = re.compile('DownloadURL="(.+?)"').findall(link)
    updateURLmatch     = re.compile('UpdateURL="(.+?)"').findall(link)
    updatedatematch    = re.compile('UpdateDate="(.+?)"').findall(link)
    updatedescmatch    = re.compile('UpdateDesc="(.+?)"').findall(link)
    updatedmatch       = re.compile('updated="(.+?)"').findall(link)
    defaultskinmatch   = re.compile('defaultskin="(.+?)"').findall(link)
    skinsmatch         = re.compile('skins="(.+?)"').findall(link)
    videoaddonsmatch   = re.compile('videoaddons="(.+?)"').findall(link)
    audioaddonsmatch   = re.compile('audioaddons="(.+?)"').findall(link)
    programaddonsmatch = re.compile('programaddons="(.+?)"').findall(link)
    pictureaddonsmatch = re.compile('pictureaddons="(.+?)"').findall(link)
    sourcesmatch       = re.compile('sources="(.+?)"').findall(link)
    adultmatch         = re.compile('adult="(.+?)"').findall(link)
    guisettingsmatch   = re.compile('guisettings="(.+?)"').findall(link)
    thumbmatch         = re.compile('thumb="(.+?)"').findall(link)
    fanartmatch        = re.compile('fanart="(.+?)"').findall(link)
    oedlmatch          = re.compile('openelec="(.+?)"').findall(link)
   
    artpath         = artpathmatch[0] if (len(artpathmatch) > 0) else ''
    artpack         = artpackmatch[0] if (len(artpackmatch) > 0) else ''
    path            = pathmatch[0] if (len(pathmatch) > 0) else ''
    name            = namematch[0] if (len(namematch) > 0) else ''
    author          = authormatch[0] if (len(authormatch) > 0) else ''
    version         = versionmatch[0] if (len(versionmatch) > 0) else ''
    description     = descmatch[0] if (len(descmatch) > 0) else 'No information available'
    updated         = updatedmatch[0] if (len(updatedmatch) > 0) else ''
    defaultskin     = defaultskinmatch[0] if (len(defaultskinmatch) > 0) else ''
    skins           = skinsmatch[0] if (len(skinsmatch) > 0) else ''
    videoaddons     = videoaddonsmatch[0] if (len(videoaddonsmatch) > 0) else ''
    audioaddons     = audioaddonsmatch[0] if (len(audioaddonsmatch) > 0) else ''
    programaddons   = programaddonsmatch[0] if (len(programaddonsmatch) > 0) else ''
    pictureaddons   = pictureaddonsmatch[0] if (len(pictureaddonsmatch) > 0) else ''
    sources         = sourcesmatch[0] if (len(sourcesmatch) > 0) else ''
    adult           = adultmatch[0] if (len(adultmatch) > 0) else ''
    guisettingslink = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    downloadURL     = downloadmatch[0] if (len(downloadmatch) > 0) else 'None'
    updateURL       = updateURLmatch[0] if (len(updateURLmatch) > 0) else 'None'
    updateDate      = updatedatematch[0] if (len(updatedatematch) > 0) else 'None'
    updateDesc      = updatedescmatch[0] if (len(updatedescmatch) > 0) else 'None'
    videopreview    = videopreviewmatch[0] if (len(videopreviewmatch) > 0) else 'None'
    videoguide1     = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2     = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3     = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4     = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5     = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1     = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2     = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3     = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4     = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5     = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    iconimage       = thumbmatch[0] if (len(thumbmatch) > 0) else 'None'
    fanart          = fanartmatch[0] if (len(fanartmatch) > 0) else 'None'
    oedownload      = oedlmatch[0] if (len(oedlmatch) > 0) else 'None'

    localfile       = open(tempfile, mode='w+')
    localfile.write('id="'+str(video)+'"\nname="'+name+'"\nversion="'+version+'"')
    localfile.close()

    localfile2      = open(idfile, mode='r')
    content2        = localfile2.read()
    localfile2.close()

    localidmatch      = re.compile('id="(.+?)"').findall(content2)
    localidcheck      = localidmatch[0] if (len(localidmatch) > 0) else 'None'
    localversmatch    = re.compile('version="(.+?)"').findall(content2)
    localversioncheck = localversmatch[0] if (len(localversmatch) > 0) else 'None'
    head, sep, tail   = url.partition('&')
    xbmc.log("### Community Build Details:")
    xbmc.log("### Name: "+name)
    xbmc.log("### URL: "+downloadURL)
    o0oO('','[COLOR=yellow]IMPORTANT:[/COLOR] Install Instructions','','instructions_2','','','','')
    Add_Desc_Dir('[COLOR=yellow]Description:[/COLOR] This contains important info from the build author','None','description','',fanart,name,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    
    if localidcheck == head and localversioncheck != version:
        o0oO('','[COLOR=orange]----------------- UPDATE AVAILABLE ------------------[/COLOR]','None','','','','','')
        Add_Build_Dir('[COLOR=dodgerblue]1. Update:[/COLOR] Overwrite My Current Setup & Install New Build',downloadURL,'restore_community',iconimage,'','update',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]2. Update:[/COLOR] Keep My Library & Profiles',downloadURL,'restore_community',iconimage,'','updatelibprofile',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]3. Update:[/COLOR] Keep My Library Only',downloadURL,'restore_community',iconimage,'','updatelibrary',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]4. Update:[/COLOR] Keep My Profiles Only',downloadURL,'restore_community',iconimage,'','updateprofiles',name,defaultskin,guisettingslink,artpack)
    
    if videopreview != 'None' or videoguide1 != 'None' or videoguide2 != 'None' or videoguide3 != 'None' or videoguide4 != 'None' or videoguide5 != 'None':
        o0oO('','[COLOR=orange]------------------ VIDEO GUIDES -----------------[/COLOR]','None','','','','','')
    
    if videopreview != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] Preview[/COLOR]',videopreview,'play_video','',fanart,'','')
    
    if videoguide1 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel1+'[/COLOR]',videoguide1,'play_video','',fanart,'','')    
    
    if videoguide2 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel2+'[/COLOR]',videoguide2,'play_video','',fanart,'','')    
    
    if videoguide3 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel3+'[/COLOR]',videoguide3,'play_video','',fanart,'','')    
    
    if videoguide4 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel4+'[/COLOR]',videoguide4,'play_video','',fanart,'','')    
    
    if videoguide5 != 'None':
        o0oO('','[COLOR=orange]Video:[/COLOR][COLOR=white] '+videolabel5+'[/COLOR]',videoguide5,'play_video','',fanart,'','')    
        
    if localidcheck != head:
        o0oO('','[COLOR=orange]------------------ INSTALL OPTIONS ------------------[/COLOR]','None','','','','','')
    
    if downloadURL=='None':
        Add_Build_Dir('[COLOR=orange]Sorry this build is currently unavailable[/COLOR]','','','','','','','','','')
    
    if localidcheck != head:
        if OpenELEC_Check() and oedownload != 'None':
#            o0oO('','[COLOR=darkcyan]OpenELEC FRESH INSTALL[/COLOR]',oedownload,'restore_openelec',iconimage,fanart,'','')
            Add_Build_Dir('[COLOR=darkcyan]OpenELEC FRESH INSTALL[/COLOR]',oedownload,'restore_openelec',iconimage,fanart,guisettingslink,name,'','','')
#        else:
#            Add_Build_Dir('[COLOR=dodgerblue]1. Fresh Install:[/COLOR] This will wipe all existing settings',downloadURL,'restore_community',iconimage,fanart,'fresh',name,defaultskin,guisettingslink,artpack)
        Add_Build_Dir('[COLOR=dodgerblue]Standard Install[/COLOR]',downloadURL,'restore_community',iconimage,fanart,'merge',name,defaultskin,guisettingslink,artpack)
#        Add_Build_Dir('[COLOR=dodgerblue]2. Install:[/COLOR] Keep My Library & Profiles',downloadURL,'restore_community',iconimage,fanart,'libprofile',name,defaultskin,guisettingslink,artpack)
#        Add_Build_Dir('[COLOR=dodgerblue]3. Install:[/COLOR] Keep My Library Only',downloadURL,'restore_community',iconimage,fanart,'library',name,defaultskin,guisettingslink,artpack)
#        Add_Build_Dir('[COLOR=dodgerblue]4. Install:[/COLOR] Keep My Profiles Only',downloadURL,'restore_community',iconimage,fanart,'profiles',name,defaultskin,guisettingslink,artpack)
         
    if guisettingslink!='None':
#        o0oO('','[COLOR=orange]---------- (OPTIONAL) Guisettings Fix ----------[/COLOR]','None','','','','','')
        o0oO('','[COLOR=dodgerblue](Optional) Apply guisettings.xml fix[/COLOR]',guisettingslink,'guisettingsfix','',fanart,'','')
#---------------------------------------------------------------------------------------------------
# Function to create an addon pack for NaN keywords
def Create_Addon_Pack(url):

    portalcontent = ''
    if url == 'create_pack':
        portalcontent   = Open_URL('http://noobsandnerds.com/TI/AddonPortal/approved.php')
        mykeyword = xbmcgui.Dialog().browse(3, 'Select the folder you want to store this file in', 'files', '', False, False)
        vq = Get_Keyboard( heading="Enter a name for this keyword" )
    
        if ( not vq ):
            return False, 0
    
        title     = urllib.quote_plus(vq)
    dp.create('Backing Up Addons & Repositories','','Please Wait...')

    if not os.path.exists(addonstemp):
        os.makedirs(addonstemp)

# copy all the addons to addonstemp folder in userdata
    for name in os.listdir(ADDONS):
        if not 'metadata' in name and not 'module' in name and not 'packages' in name and not 'service.xbmc.versioncheck' in name and os.path.isdir(os.path.join(ADDONS, name)):
            try:
                dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait...')
                                
# if the addon is on the approved list (in a repo found on NaN) or we're creating the backup addon list for profiles just copy addons.xml
                if name in portalcontent or url != 'create_pack':
# create a new directory with the repo id if it doesn't exist
                    if not os.path.exists(os.path.join(addonstemp,'addons',name)):
                        os.makedirs(os.path.join(addonstemp,'addons',name))
                    shutil.copyfile(os.path.join(ADDONS,name,'addon.xml'),os.path.join(addonstemp,'addons',name,'addon.xml'))
                if not name in portalcontent:
                    shutil.copytree(os.path.join(ADDONS,name),os.path.join(addonstemp,'addons',name))

                currentfile    = os.path.join(addonstemp,'addons',name,'addon.xml')                


# this is the new addon.xml file
                readfile = open(currentfile, mode='r')
                content = readfile.read()
                readfile.close()

# find version number, there are 2 version tags in the addon.xml, we need the second one.
                localmatch         = re.compile('<addon[\s\S]*?">').findall(content)
                localcontentmatch  = localmatch[0] if (len(localmatch) > 0) else 'None'
                localversion       = re.compile('version="[\s\S]*?"').findall(localcontentmatch)
                localversionmatch  = localversion[0] if (len(localversion) > 0) else '0'
               
# if we're changing the version number edit the temp addon.xml
                newaddons   = str(localcontentmatch).replace(localversionmatch,'version="0.0.0.1"')
                replacefile = content.replace(localcontentmatch,newaddons)

                writefile2  = open(currentfile, mode='w')
                writefile2.write(str(replacefile))
                writefile2.close()

            except:
                if debug == 'true':
                    xbmc.log("### Failed to create: "+name+' ###')
# archive files
    if url == 'create_pack':
        exclude_dirs  =  ['.svn','.git']
        exclude_files =  ['.DS_Store','Thumbs.db','.gitignore']
        destfile      = os.path.join(mykeyword,title+'.zip')
        Archive_Tree(addonstemp, destfile, 'Creating Addons Archive', '', '', '', exclude_dirs, exclude_files)
        try:
            shutil.rmtree(addonstemp)
        except:
            pass
        dialog.ok('New Keyword Created','Please read the instructions on how to share this keyword with the community. Your zip file can be found at:','[COLOR=dodgerblue]'+destfile+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# Create new CP Profile
def Create_Profile(name):
# Read the contents of id.xml
    localfile          = open(idfile, mode='r')
    content            = localfile.read()
    localfile.close()
    localbuildmatch    = re.compile('name="(.+?)"').findall(content)
    localbuildcheck    = localbuildmatch[0] if (len(localbuildmatch) > 0) else 'None'
    mainaddons         = []

# If no profile exists for currently running build then create one and add new id file
    if localbuildcheck == 'None':
        dialog.ok('No Profile Set',"There's no profile name set to the build you're currently running. Please enter a name for this build so we can save it and make sure no data is lost.")
        vq = Get_Keyboard( heading="Enter a name for this backup" )
        if ( not vq ):
            return False, 0
        vq          = vq.replace(' ','_')
        title       = urllib.quote_plus(vq)
        os.makedirs(os.path.join(CP_PROFILE,title))
        buildname   = title
        localfile   = open(idfile, 'w')
        replacefile = content.replace('id="None"','id="Local"').replace('name="None"','name="'+str(buildname)+'"')
        localfile.write(replacefile)
        localfile.close()

# List pre-installed Kodi addons, we don't need to copy these
        for item in os.listdir(KODI_ADDONS):
            mainaddons.append(item)
# Create an addonlist for new profile
        newlist = open(os.path.join(CP_PROFILE,title,'addonlist'), mode='w+')
        for item in os.listdir(ADDONS):
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'packages':
                newlist.write(item+'|')
        newlist.close()

        exclude_dirs_full =  ['addons','cache','CP_Profiles','system','temp','Thumbnails']
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore','addons*.db','textures13.db']
        message_header = "Creating backup of existing build"
        message1 = "Archiving..."
        message2 = ""
        message3 = "Please Wait"
        Archive_Tree(HOME, os.path.join(CP_PROFILE,title,'build.zip'), message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)

 
# If profile does exist copy latest info to profile directory
    else:
        buildname = localbuildcheck.replace(' ','_').replace(':','-').replace("'",'')
# Create an addonlist for new profile
        newlist = open(os.path.join(CP_PROFILE,buildname,'addonlist'), mode='w+')
        for item in os.listdir(ADDONS):
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'packages':
                newlist.write(item+'|')
        newlist.close()

        exclude_dirs_full =  ['addons','cache','CP_Profiles','system','temp','Thumbnails']
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore','addons*.db','textures13.db']
        message_header = "Creating backup of existing build"
        message1 = "Archiving..."
        message2 = ""
        message3 = "Please Wait"
        Archive_Tree(HOME, os.path.join(CP_PROFILE,buildname,'build.zip'), message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    return buildname
#---------------------------------------------------------------------------------------------------
#Function to delete the userdata/addon_data folder
def CPU_Check():
    version=str(xbmc_version[:2])
    if version < 14:
        logfile = os.path.join(log_path, 'xbmc.log')
    
    else:
        logfile = os.path.join(log_path, 'kodi.log')

    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()

    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
#---------------------------------------------------------------------------------------------------
def DeleteAddonData():
    xbmc.log('############################################################       DELETING USERDATA             ###############################################################')
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
        
        if file_count >= 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#---------------------------------------------------------------------------------------------------
#Function to delete crash logs
def Delete_Logs():  
    for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
         File   = infile
         os.remove(infile)
         dialog = xbmcgui.Dialog()
         dialog.ok("Crash Logs Deleted", "Your old crash logs have now been deleted.")
#-----------------------------------------------------------------------------------------------------------------    
#Function to delete the packages folder
def Delete_Packages():
    xbmc.log('############################################################       DELETING PACKAGES             ###############################################################')
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        
        if file_count > 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
#---------------------------------------------------------------------------------------------------
# Function to wipe path
def Delete_Path(path):
    choice = dialog.yesno('Are you certain?','This will completely wipe this folder, are you absolutely certain you want to continue? There is NO going back after this!')
    if choice == 1:
        dp.create("Wiping Data","Wiping...",'', 'Please Wait')
        shutil.rmtree(path, ignore_errors=True)
        dp.close()
        xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------  
# Menu for removing a build
def Delete_Profile_Menu(url):
    for name in os.listdir(CP_PROFILE):
        if name != 'Master' and name != url.replace(' ','_').replace("'",'').replace(':','-'):
            o0oO('','[COLOR=darkcyan]DELETE[/COLOR] '+name.replace('_',' '),os.path.join(CP_PROFILE,name),'delete_path','','','','')
#---------------------------------------------------------------------------------------------------
#Function to delete the userdata/addon_data folder
def Delete_Userdata():
    xbmc.log('############################################################       DELETING USERDATA             ###############################################################')
    addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', ''))
    
    for root, dirs, files in os.walk(addon_data_path):
        file_count = 0
        file_count += len(files)
        
        if file_count >= 0:
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))        
#-----------------------------------------------------------------------------------------------------------------  
# Check what dependencies each addon in the addons folder has
def Dependency_Check():
    dp.create('Checking dependencies','','Please Wait...')
    depfiles = []

    for name in os.listdir(ADDONS):
        if name != 'packages':
            try:
                addonxml = os.path.join(ADDONS,name,'addon.xml')
                addonsource  = open(addonxml, mode = 'r')
                readxml      = addonsource.read()
                addonsource.close()
                dmatch       = re.compile('import addon="(.+?)"').findall(readxml)
    
                for requires in dmatch:
        
                    if not 'xbmc.python' in requires and not requires in depfiles:
                        depfiles.append(requires)
                        xbmc.log('Script Requires --- %s' % requires)
            except:
                pass
                
    return depfiles
#-----------------------------------------------------------------------------------------------------------------    
#Step 3 of the addon install process (installs the dependencies)
def Dependency_Install(name,addon_id):
    modulestatus = 1
    status       = 1
    addonxml     = xbmc.translatePath(os.path.join(ADDONS,addon_id,'addon.xml'))    
    addonsource  = open(addonxml, mode = 'r')
    readxml      = addonsource.read()
    addonsource.close()
    dmatch       = re.compile('import addon="(.+?)"').findall(readxml)
    
    for requires in dmatch:
        
        if not 'xbmc.python' in requires:
            xbmc.log('Script Requires --- %s' % requires)
            dependencypath = xbmc.translatePath(os.path.join(ADDONS, requires))
            
            if not os.path.exists(dependencypath):
                BaseURL        = 'http://noobsandnerds.com/TI/AddonPortal/dependencyinstall.php?id=%s' % (requires)
                link           = Open_URL(BaseURL).replace('\n','').replace('\r','')
                namematch      = re.compile('name="(.+?)"').findall(link)
                versionmatch   = re.compile('version="(.+?)"').findall(link)
                repourlmatch   = re.compile('repo_url="(.+?)"').findall(link)
                dataurlmatch   = re.compile('data_url="(.+?)"').findall(link)
                zipurlmatch    = re.compile('zip_url="(.+?)"').findall(link)
                repoidmatch    = re.compile('repo_id="(.+?)"').findall(link)  
                depname        = namematch[0] if (len(namematch) > 0) else ''
                version        = versionmatch[0] if (len(versionmatch) > 0) else ''
                repourl        = repourlmatch[0] if (len(repourlmatch) > 0) else ''
                dataurl        = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
                zipurl         = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
                repoid         = repoidmatch[0] if (len(repoidmatch) > 0) else ''
                dependencyname = xbmc.translatePath(os.path.join(packages,depname+'.zip')) 
                
                try:
                    downloader.download(repourl, dependencyname, dp)
                    extract.all(dependencyname, ADDONS, dp)
                
                except:
                    
                    try:
                        downloader.download(zipurl, dependencyname, dp)
                        extract.all(dependencyname, ADDONS, dp)
                    
                    except:
                        
                        try:
                            
                            if not os.path.exists(dependencypath):
                                os.makedirs(dependencypath)
                            
                            link = Open_URL(dataurl).replace('\n','').replace('\r','')
                            match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                            
                            for href in match:
                                filepath=xbmc.translatePath(os.path.join(dependencypath,href))
                                
                                if addon_id not in href and '/' not in href:
                                    
                                    try:
                                        dp.update(0,"Downloading [COLOR=darkcyan]"+href+'[/COLOR]','','Please wait...')
                                        downloader.download(dataurl+href, filepath, dp)
                                    
                                    except:
                                        xbmc.log("failed to install"+href)
                                
                                if '/' in href and '..' not in href and 'http' not in href:
                                    remote_path = dataurl+href
                                    Recursive_Loop(filepath,remote_path)
                        
                        except:
                            dialog.ok("Error downloading dependency", 'There was an error downloading [COLOR=dodgerblue]'+depname+'[/COLOR]. Please consider updating the add-on portal with details or report the error on the forum at [COLOR=orange]noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds[/COLOR]')
                            status=0
                            modulestatus=0
                
                if status==1:
                    time.sleep(1)
                    dp.update(0,"[COLOR=darkcyan]"+depname+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Please wait...')
                    time.sleep(1)
                    incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (requires)
                    try:
                        Open_URL(incremental)
                    except:
                        pass
    dp.close()
    time.sleep(1)
#---------------------------------------------------------------------------------------------------
#Show full description of build
def Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult):
    TXT.TXT(buildname+'     v.'+version, '[COLOR=darkcyan][B]Author:   [/B][/COLOR]'+author+'[COLOR=darkcyan][B]               Last Updated:   [/B][/COLOR]'+updated+'[COLOR=darkcyan][B]               Adult Content:   [/B][/COLOR]'+adult+'[CR][CR][COLOR=darkcyan][B]Description:[CR][/B][/COLOR]'+description+
    '[CR][CR][COLOR=blue][B]Skins:   [/B][/COLOR]'+skins+'[CR][CR][COLOR=blue][B]Video Addons:   [/B][/COLOR]'+videoaddons+'[CR][CR][COLOR=blue][B]Audio Addons:   [/B][/COLOR]'+audioaddons+
    '[CR][CR][COLOR=blue][B]Program Addons:   [/B][/COLOR]'+programaddons+'[CR][CR][COLOR=blue][B]Picture Addons:   [/B][/COLOR]'+pictureaddons+'[CR][CR][COLOR=blue][B]Sources:   [/B][/COLOR]'+sources+
    '[CR][CR][COLOR=orange]Disclaimer: [/COLOR]These are community builds and they may overwrite some of your existing settings, '
    'It\'s purely the responsibility of the user to choose whether or not they wish to install these builds, the individual who uploads the build should state what\'s included and then it\'s the users decision to decide whether or not that content is suitable for them.')
#---------------------------------------------------------------------------------------------------
#Function to do a full wipe.
def Destroy_Path(path):
    dp.create("Cleaning Path","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)
#---------------------------------------------------------------------------------------------------
def encryptme(mode, message):
    if mode == 'e':
        import random
        count = 0
        finaltext = ''
        while count < 4:
            count += 1
            randomnum = random.randrange(1, 31)
            hexoffset = hex(randomnum)[2:]
            if len(hexoffset)==1:
                hexoffset = '0'+hexoffset
            finaltext = finaltext+hexoffset
        randomchar = random.randrange(1,4)
        if randomchar == 1: finaltext = finaltext+'0A'
        if randomchar == 2: finaltext = finaltext+'04'
        if randomchar == 3: finaltext = finaltext+'06'
        if randomchar == 4: finaltext = finaltext+'08'
        key1    = finaltext[-2:]
        key2    = int(key1,16)
        hexkey  = finaltext[-key2:-(key2-2)]
        key     = -int(hexkey,16)

# enctrypt/decrypt the message
        translated = ''
        finalstring = ''
        for symbol in message:
            num = ord(symbol)
            num2 = int(num) + key
            hexchar = hex(num2)[2:]
            if len(hexchar)==1:
                hexchar = '0'+hexchar
            finalstring = str(finalstring)+str(hexchar)
        return finalstring+finaltext
    else:
        key1    = message[-2:]
        key2    = int(key1,16)
        hexkey  = message[-key2:-(key2-2)]
        key     = int(hexkey,16)
        message = message [:-10]
        messagearray = [message[i:i+2] for i in range(0, len(message), 2)]
        numbers = [ int(x,16)+key for x in messagearray ]
        finalarray = [ str(unichr(x)) for x in numbers ]
        finaltext = ''.join(finalarray)
        return finaltext.encode('utf-8')
#---------------------------------------------------------------------------------------------------
def Finish_Local_Restore():
    os.remove(idfile)
    os.rename(idfiletemp,idfile)
    xbmc.executebuiltin('UnloadSkin')    
    xbmc.executebuiltin("ReloadSkin")
    dialog.ok("Local Restore Complete", 'XBMC/Kodi will now close.', '', '')
    xbmc.executebuiltin("Quit")      
#---------------------------------------------------------------------------------------------------
#Convert physical paths to special paths
def Fix_Special(url):
    dp.create("Changing Physical Paths To Special","Renaming paths...",'', 'Please Wait')
    
    for root, dirs, files in os.walk(url):  #Search all xml files and replace physical with special
        
        for file in files:
            
            if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
                 dp.update(0,"Fixing",file, 'Please Wait')
                 a = open((os.path.join(root, file))).read()
                 encodedpath  = HOME.replace(':','%3a').replace('\\','%5c')
                 extraslashes = HOME.replace('\\','\\\\')
                 b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(extraslashes, 'special://home/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()
#---------------------------------------------------------------------------------------------------
# Call the full backup option
def Full_Backup():
    if os.path.exists(addonstemp):
        shutil.rmtree(addonstemp)
    exclude_dirs_full  =  []
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
#---------------------------------------------------------------------------------------------------
def Full_Clean():
    size                      = 0
    atv2_cache_a              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
    atv2_cache_b              = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')        
    downloader_cache_path     = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    imageslideshow_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.image.music.slideshow/cache'), '')
    iplayer_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    itv_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    navix_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/script.navi-x/cache'), '')
    phoenix_cache_path        = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.phstreams/Cache'), '')
    ramfm_cache_path          = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.ramfm/cache'), '')
    wtf_cache_path            = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    genesisCache              = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
    tempdir                   = os.path.join(HOME,'temp')
    dp.create('Calculating Used Space','','Please wait','')
    if os.path.exists(atv2_cache_a):
        size = Get_Size(atv2_cache_a,size)
    if os.path.exists(atv2_cache_b):
        size = Get_Size(atv2_cache_b,size)
    if os.path.exists(downloader_cache_path):
        size = Get_Size(downloader_cache_path,size)
    if os.path.exists(imageslideshow_cache_path):
        size = Get_Size(imageslideshow_cache_path,size)
    if os.path.exists(iplayer_cache_path):
        size = Get_Size(iplayer_cache_path,size)
    if os.path.exists(itv_cache_path):
        size = Get_Size(itv_cache_path,size)
    if os.path.exists(navix_cache_path):
        size = Get_Size(navix_cache_path,size)
    if os.path.exists(phoenix_cache_path):
        size = Get_Size(phoenix_cache_path,size)
    if os.path.exists(ramfm_cache_path):
        size = Get_Size(ramfm_cache_path,size)
    if os.path.exists(wtf_cache_path):
        size = Get_Size(wtf_cache_path,size)
    if os.path.exists(genesisCache):
        size = Get_Size(genesisCache,size)
    if os.path.exists(tempdir):
        size = Get_Size(tempdir,size)
    size = Get_Size(THUMBNAILS,size)
    size = Get_Size(packages,size)/1000000
    choice = dialog.yesno('Results','You can free up [COLOR=dodgerblue]'+str(size)+'MB[/COLOR] of space if you run this cleanup program. Would you like to run the cleanup procedure?')
    if choice == 1:
        Wipe_Cache()
        try:
            shutil.rmtree(packages)
        except:
            pass
        choice = dialog.yesno('Thumbnail Cleanup','We highly recommend only wiping your OLD unused thumbnails. Do you want to clear just the old ones or all thumbnails?',yeslabel='ALL',nolabel='OLD ONLY')
        if choice == 1:
            Remove_Textures()
            Destroy_Path(THUMBNAILS)
            KLL()
        else:
            Cleanup_Old_Textures()
        xbmc.executebuiltin('reboot')
#---------------------------------------------------------------------------------------------------
#Build Genres Menu (First Filter)
def Genres(url):       
    o0oO('folder','Anime',str(url)+'&genre=anime','grab_builds','','','','')
    o0oO('folder','Audiobooks',str(url)+'&genre=audiobooks','grab_builds','','','','')
    o0oO('folder','Comedy',str(url)+'&genre=comedy','grab_builds','','','','')
    o0oO('folder','Comics',str(url)+'&genre=comics','grab_builds','','','','')
    o0oO('folder','Documentary',str(url)+'&genre=documentary','grab_builds','','','','')
    o0oO('folder','Downloads',str(url)+'&genre=downloads','grab_builds','','','','')
    o0oO('folder','Food',str(url)+'&genre=food','grab_builds','','','','')
    o0oO('folder','Gaming',str(url)+'&genre=gaming','grab_builds','','','','')
    o0oO('folder','Health',str(url)+'&genre=health','grab_builds','','','','')
    o0oO('folder','How To...',str(url)+'&genre=howto','grab_builds','','','','')
    o0oO('folder','Kids',str(url)+'&genre=kids','grab_builds','','','','')
    o0oO('folder','Live TV',str(url)+'&genre=livetv','grab_builds','','','','')
    o0oO('folder','Movies',str(url)+'&genre=movies','grab_builds','','','','')
    o0oO('folder','Music',str(url)+'&genre=music','grab_builds','','','','')
    o0oO('folder','News',str(url)+'&genre=news','grab_builds','','','','')
    o0oO('folder','Photos',str(url)+'&genre=photos','grab_builds','','','','')
    o0oO('folder','Podcasts',str(url)+'&genre=podcasts','grab_builds','','','','')
    o0oO('folder','Radio',str(url)+'&genre=radio','grab_builds','','','','')
    o0oO('folder','Religion',str(url)+'&genre=religion','grab_builds','','','','')
    o0oO('folder','Space',str(url)+'&genre=space','grab_builds','','','','')
    o0oO('folder','Sports',str(url)+'&genre=sports','grab_builds','','','','')
    o0oO('folder','Technology',str(url)+'&genre=tech','grab_builds','','','','')
    o0oO('folder','Trailers',str(url)+'&genre=trailers','grab_builds','','','','')
    o0oO('folder','TV Shows',str(url)+'&genre=tv','grab_builds','','','','')
    o0oO('folder','Misc.',str(url)+'&genre=other','grab_builds','','','','')
    
    if ADDON.getSetting('adult') == 'true':
        o0oO('folder','XXX',str(url)+'&genre=adult','grab_builds','','','','')
#---------------------------------------------------------------------------------------------------
# Send a path and an initial size to increment to and it will scan total file sizes of all subfolders
def Get_Size(path,size):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            dp.update(0,"Calulating...",'[COLOR=dodgerblue]'+f+'[/COLOR]', 'Please Wait')
            fp = os.path.join(dirpath, f)
            size += os.path.getsize(fp)
    return size
#---------------------------------------------------------------------------------------------------
def Get_Keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
#    return default
#-----------------------------------------------------------------------------------------------------------------  
#Get params and clean up into string or integer
def Get_Params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
#-----------------------------------------------------------------------------------------------------------------
def getMacAddress(protocol):
    cont = 0
    if sys.platform == 'win32': 
        mac = ''
        for line in os.popen("ipconfig /all"):
            if protocol == 'wifi':
                if line.startswith('Wireless LAN adapter Wi'):
                    cont = 1
                if line.lstrip().startswith('Physical Address') and cont == 1:
                    mac = line.split(':')[1].strip().replace('-',':')
                    break

            if protocol != 'wifi':
                if line.lstrip().startswith('Physical Address'): 
                    mac = line.split(':')[1].strip().replace('-',':')
                    break 

    if xbmc.getCondVisibility('System.Platform.Android'):
        mac = ''
        if os.path.exists('/sys/class/net/wlan0/address') and protocol == 'wifi':
            readfile = open('/sys/class/net/wlan0/address', mode='r')
        if os.path.exists('/sys/class/net/eth0/address') and protocol != 'wifi':
            readfile = open('/sys/class/net/eth0/address', mode='r')
        mac = readfile.read()
        try:
            mac = mac[:17]
        except:
            mac = ''
        readfile.close()
        if mac == '':
            xbmc.log('#### CANNOT FIND MAC DETAILS ON YOUR DEVICE. THIS UNIT CANNOT CURRENTLY BE USED WITH OUR SERVICE')
            mac = 'Unknown'

    else:
        if protocol == 'wifi':
            for line in os.popen("/sbin/ifconfig"): 
                if line.find('wlan0') > -1: 
                    mac = line.split()[4] 
                    break
        else:
           for line in os.popen("/sbin/ifconfig"): 
                if line.find('eth0') > -1: 
                    mac = line.split()[4] 
                    break
    return str(mac)
#---------------------------------------------------------------------------------------------------
def Gotham():
    path = xbmc.translatePath(os.path.join('special://home', 'addons'))
    dp   = xbmcgui.DialogProgress()
    dp.create("Gotham Addon Fix","Please wait whilst your addons",'', 'are being made Gotham compatible.')
    
    for infile in glob.glob(os.path.join(path, '*.*')):
        
        for file in glob.glob(os.path.join(infile, '*.*')):
            
            if 'addon.xml' in file:
                dp.update(0,"Fixing",file, 'Please Wait')
                a = open(file).read()
                b = a.replace('addon="xbmc.python" version="1.0"','addon="xbmc.python" version="2.1.0"').replace('addon="xbmc.python" version="2.0"','addon="xbmc.python" version="2.1.0"')
                f = open(file, mode='w')
                f.write(str(b))
                f.close()

    dialog = xbmcgui.Dialog()
    dialog.ok("Your addons have now been made compatible", "If you still find you have addons that aren't working please run the addon so it throws up a script error, upload a log and post details on the relevant support forum.")
#-----------------------------------------------------------------------------------------------------------------  
# Thanks to Mikey1234 for this code - taken from the xunity maintenance addon
def Gotham_Confirm():
    dialog = xbmcgui.Dialog()
    confirm = xbmcgui.Dialog().yesno('Convert Addons To Gotham', 'This will edit your addon.xml files so they show as Gotham compatible. It\'s doubtful this will have any effect on whether or not they work but it will get rid of the annoying incompatible pop-up message. Do you wish to continue?')
    
    if confirm == 1:
        Gotham()
#-----------------------------------------------------------------------------------------------------------------          
#Function to populate the search based on the initial first filter
def Grab_Addons(url):
    
    if ADDON.getSetting('adult') == 'true':
        adult = 'yes'
    
    else:
        adult = 'no'

    if url == 'popular':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/popular.php?adult=%s' % (adult)
    elif url != 'popular':
        buildsURL  = 'http://noobsandnerds.com/TI/AddonPortal/sortby_bak.php?sortx=name&user=%s&adult=%s&%s' % (username, adult, url)

    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> downloads="(.+?)"  <br> icon="(.+?)"  <br> broken="(.+?)"  <br> UID="(.+?)"  <br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match  = re.compile('name="(.+?)" <br> downloads="(.+?)" <br> icon="(.+?)" <br> broken="(.+?)" <br> UID="(.+?)" <br>', re.DOTALL).findall(link)
    
    if match !=[] and url != 'popular':
        Sort_By(buildsURL,'addons')
        
        for name,downloads,icon, broken, uid in match:
            
            if broken=='0':
                o0oO('addonfolder',name+'[COLOR=lime] ['+downloads+' downloads][/COLOR]',uid,'addon_final_menu',icon,'','')        
            
            if broken=='1':
                o0oO('addonfolder','[COLOR=red]'+name+' [REPORTED AS BROKEN][/COLOR]',uid,'addon_final_menu',icon,'','')        
    
    elif match !=[] and url == 'popular':
        for name,downloads,icon, broken, uid in match:
            
            if broken=='0':
                o0oO('addonfolder',name+'[COLOR=lime] ['+downloads+' downloads][/COLOR]',uid,'addon_final_menu',icon,'','')        
            
            if broken=='1':
                o0oO('addonfolder','[COLOR=red]'+name+' [REPORTED AS BROKEN][/COLOR]',uid,'addon_final_menu',icon,'','')        
        
    elif '&redirect' in url:
        choice=dialog.yesno('No Content Found','This add-on cannot be found on the Add-on Portal.','','Would you like to remove this item from your setup?')
        
        if choice == 1:
            xbmc.log("### Need to add remove function to code still")
    
    else:
        dialog.ok('No Content Found','Sorry no content can be found that matches','your search criteria.','')
#-----------------------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Builds(url):
    if zip == '':
        dialog.ok('Storage/Download Folder Not Set','You have not set your backup storage folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    
    if ADDON.getSetting('adult') == 'true':
        adult = ''
    
    else:
        adult = 'no'

    if not 'id=' in url:
        buildsURL  = 'http://noobsandnerds.com/TI/Community_Builds/sortby.php?sortx=name&orderx=ASC&adult=%s&%s' % (adult, url)
        link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare disabled
        match      = re.compile('name="(.+?)"  <br> id="(.+?)"  <br> Thumbnail="(.+?)"  <br> Fanart="(.+?)"  <br> downloads="(.+?)"  <br> <br>', re.DOTALL).findall(link)
        if match == []:
# match with cloudflare disabled
            match  = re.compile('name="(.+?)" <br> id="(.+?)" <br> Thumbnail="(.+?)" <br> Fanart="(.+?)" <br> downloads="(.+?)" <br> <br>', re.DOTALL).findall(link)
        Sort_By(url,'communitybuilds')
    
        for name,id,Thumbnail,Fanart,downloads in match:
            Add_Build_Dir(name+'[COLOR=lime] ('+downloads+' downloads)[/COLOR]',id+url,'community_menu',Thumbnail,Fanart,id,'','','','')
    
    if 'id=1' in url: buildsURL = wizardurl1
    if 'id=2' in url: buildsURL = wizardurl2
    if 'id=3' in url: buildsURL = wizardurl3
    if 'id=4' in url: buildsURL = wizardurl4
    if 'id=5' in url: buildsURL = wizardurl5

    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
    match      = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)

    for name,url,iconimage,fanart,description in match:
        if not 'viewport' in name:
            o0oO('addon',name,url,'restore_local_CB',iconimage,fanart,description,'')
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Hardware(url):
    buildsURL  = 'http://noobsandnerds.com/TI/HardwarePortal/sortby.php?sortx=Added&orderx=DESC&%s' % (url)
    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> id="(.+?)"  <br> thumb="(.+?)"  <br><br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match  = re.compile('name="(.+?)" <br> id="(.+?)" <br> thumb="(.+?)" <br><br>', re.DOTALL).findall(link)
    Sort_By(buildsURL,'hardware')
    
    for name, id, thumb in match:
        o0oO('folder2',name,id,'hardware_final_menu',thumb,'','')
#---------------------------------------------------------------------------------------------------
#Function to populate the news search
def Grab_News(url):
    buildsURL = 'http://noobsandnerds.com/TI/LatestNews/sortby.php?sortx=item_date&orderx=DESC&%s' % (url)
    link      = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match     = re.compile('name="(.+?)"  <br> date="(.+?)"  <br> source="(.+?)"  <br> id="(.+?)"  <br><br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match     = re.compile('name="(.+?)" <br> date="(.+?)" <br> source="(.+?)" <br> id="(.+?)" <br><br>', re.DOTALL).findall(link)
    for name, date, source, id in match:
        
        if "OpenELEC" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','OpenELEC.png','','')
        
        if "Official" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','XBMC.png','','')
        
        if "Raspbmc" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','Raspbmc.png','','')
        
        if "XBMC4Xbox" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','XBMC4Xbox.png','','')
        
        if "noobsandnerds" in source:
            o0oO('',name+'  ('+date+')',id,'news_menu','noobsandnerds.png','','')
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Grab_Tutorials(url):
    buildsURL  = 'http://noobsandnerds.com/TI/TutorialPortal/sortby.php?sortx=Name&orderx=ASC&%s' % (url)
    link       = Open_URL(buildsURL).replace('\n','').replace('\r','')
# match without cloudflare enabled
    match      = re.compile('name="(.+?)"  <br> about="(.+?)"  <br> id="(.+?)"  <br><br>', re.DOTALL).findall(link)
    if match == []:
# match with cloudflare enabled
        match      = re.compile('name="(.+?)" <br> about="(.+?)" <br> id="(.+?)" <br><br>', re.DOTALL).findall(link)
    Sort_By(buildsURL,'tutorials')
        
    for name, about, id in match:
        o0oO('folder',name,id,'tutorial_final_menu','Tutorials.png','',about)
#---------------------------------------------------------------------------------------------------
def Grab_Updates(url):
    isplaying = xbmc.Player().isPlaying()
    if not isplaying:
        urlparams   = URL_Params()
        mysuccess   = 0
        failed      = 0
        counter     = 0
        changetimer = 0
        multi       = 0
        previous    = ''

# SET TO 1 FOR TEST MODE - THIS WILL OUTPUT TO LOG AND DISPLAY COMMAND DIALOGS ON SCREEN
        showdialogs = 0

        if url == 'http://tlbb.me/comm.php?multi&z=c&x=':
            multi = 1
            url=url.replace('multi&','')
        if url == 'http://tlbb.me/comm.php?update&z=c&x=':
            Notify('Checking For Updates','Please wait...','1000',os.path.join(ADDONS,'script.openwindow','resources','images','update_software.png'))
            url=url.replace('update&','')
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        while mysuccess != 1 and failed != 1:

            try:
                if debug == 'true':
                    xbmc.log("### URL: "+url+encryptme('e',urlparams))
                link = Open_URL2(url+encryptme('e',urlparams))
                if link != '' and not 'sleep' in link:
                    link = encryptme('d',link).replace('\n',';').replace('|_|',' ').replace('|!|','\n').replace('http://venztech.com/repo_jpegs/','http://tlbb.me/repo_jpegs/')
                if debug == 'true':
                    try:
                        xbmc.log("### Return: "+link)
                    except:
                        pass

                if link == '':
                    xbmc.log("### Blank page returned")
                    counter += 1
                    if counter == 3:
                        failed = 1
#                    return

# Check that no body tag exists, if it does then we know TLBB is offline
                if not '<body' in link and link != '':
                    linematch  = re.compile('com(.+?)="').findall(link)
                    commline   = linematch[0] if (len(linematch) > 0) else ''
                    commatch   = re.compile('="(.+?)endcom"').findall(link)
                    command    = commatch[0] if (len(commatch) > 0) else 'End'
                
                    SF_match   = re.compile('<favourite[\s\S]*?</favourite>').findall(command)
                    SF_command = SF_match[0] if (len(SF_match) > 0) else 'None'

# Create array of commands so we can check if the install video needs to be played
                    previous += command

                    if debug == 'true':

                        xbmc.log("### command: "+command)
                        xbmc.log("### SF_command: "+SF_command)

                    Open_URL2(binascii.unhexlify('687474703a2f2f746c62622e6d652f636f6d6d2e7068703f783d')+encryptme('e',urlparams)+'&y='+commline)

                    if debug == 'true':
                        xbmc.log("### COMMAND *CLEANED: "+command.replace('|#|',';'))
                        xbmc.log("### LINK *ORIG: "+link)
                    if SF_command!='None':
                        localfile = open(progresstemp, mode='w+')
                        localfile.write(SF_command)
                        localfile.close()

                    elif command!='End' and not 'sleep' in link:
                        if ';' in command:
                            if debug == 'true':
                                xbmc.log(command)
                            newcommands = command.split(';')
                            for item in newcommands:
                                if 'branding/install.mp4' in item:
                                    item = ''

                                if 'extract.all' in item:
                                    try:
                                        exec item
                                        if showdialogs == 1:
                                            TXT.TXT('ITEM',item.replace('|#|',';'))
                                        if os.path.exists(os.path.join(packages,'updates.zip')):
                                            os.remove(os.path.join(packages,'updates.zip'))
                                    except Exception as e:
                                        xbmc.log(str(e))
                                else:
                                    try:
                                        if 'Dialog().ok(' in item:
                                            xbmc.sleep(1000)
                                            while xbmc.Player().isPlaying():
                                                xbmc.sleep(500)
                                        exec item.replace('|#|',';') # Change to semicolon for user agent otherwise it splits into a new command
                                        if showdialogs == 1:
                                            TXT.TXT('ITEM',item.replace('|#|',';'))
                                            xbmc.log("### RUNNING ITEM: "+item.replace('|#|',';'))
                                    except Exception as e:
                                        xbmc.log("### Failed with item: "+item.replace('|#|',';'))
                                        xbmc.log(str(e))
                                        if showdialogs == 1:
                                            TXT.TXT('FAILED ITEM',item.replace('|#|',';'))
#                                    while xbmc.Player().isPlaying():
#                                        xbmc.sleep(500)
                        else:
                            try:
                                if 'Dialog().ok(' in command:
                                    if not multi:
                                        xbmc.sleep(1000)
                                        xbmc.log("### Dialog.ok in this command, checking if xbmc is playing....")
                                        while xbmc.Player().isPlaying():
                                            xbmc.sleep(500)
                                    else: command = ''

                                if 'extract.all' in command:
                                    try:
                                        exec command
                                        if showdialogs == 1:
                                            TXT.TXT('ITEM',command.replace('|#|',';'))
                                        if os.path.exists(os.path.join(packages,'updates.zip')):
                                            os.remove(os.path.join(packages,'updates.zip'))
                                            TXT.TXT('ITEM','Successfully removed updates.zip')
                                    except Exception as e:
                                        xbmc.log("### Failed with command: "+command.replace('|#|',';'))
                                        xbmc.log(str(e))

                                if 'branding/install.mp4' in command:
                                    command = ''

                                else:
                                    exec command.replace('|#|',';') # Change to semicolon for user agent otherwise it splits into a new command
                                    if showdialogs == 1:
                                        TXT.TXT('COMMAND',item.replace('|#|',';'))
                                        xbmc.log("### RUNNING COMMAND: "+item.replace('|#|',';'))
                            except:
                                xbmc.log("### Failed with command: "+command.replace('|#|',';'))
#                        while xbmc.Player().isPlaying():
#                            xbmc.sleep(500)
                        previous = ''
                        if os.path.exists(progresstemp):
                            os.remove(progresstemp)
                        
                    elif command=='End':
                        if 'sleep' in link:
                            readfile = open(sleeper, 'r')
                            content = readfile.read()
                            readfile.close()
                            if content != "sleep=STOPALL":
                                sleep = str(link[6:])
                            else:
                                sleep = "23:59:59"
                                xbmc.log("### SLEEP MODE - SERVER MAINTENANCE")
                            if str(sleep) != str(content):
                                writefile = open(sleeper, 'w+')
                                writefile.write(sleep)
                                writefile.close()
                                xbmc.log("### Changed timer to "+sleep)
                                changetimer = 1
                            else:
                                if debug == 'true':
                                    xbmc.log("### Timer same, no changes required")
                        if sleep != '23:59:59':
                            Notify('Updates Complete','No more updates to show','1000',os.path.join(ADDONS,'plugin.program.tbs','resources','tick.png'))
#                            if not multi:
#                                xbmc.executebuiltin( 'Container.Refresh' )
                            xbmc.executebuiltin( 'UpdateLocalAddons' )
                            xbmc.executebuiltin( 'UpdateAddonRepos' )
                            mysuccess = 1
            except Exception as e:
                xbmc.log("### Failed with update command"+str(e))
                failed = 1
        try:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        except:
            pass

        if changetimer == 1:
            xbmc.executebuiltin('StopScript(special://home/addons/plugin.program.tbs/service.py)')
            xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/service.py)')
#---------------------------------------------------------------------------------------------------
#function to grab system info
def URL_Params():
        try:
            wifimac = getMacAddress('wifi').replace('\n','')
        except:
            wifimac = 'Unknown'
        try:
            ethmac  = getMacAddress('eth0').replace('\n','')
        except:
            ethmac  = 'Unknown'
        try:
            cpu     = CPU_Check().replace('\n','')
        except:
            cpu     = 'Unknown'
        try:
            build   = Build_Info().replace('\n','')
        except:
            build   = 'Unknown'

        xbmc.log("### BUILD:"+build)
        urlparams = wifimac+'&'+cpu+'&'+build+'&'+ethmac.replace(' ','%20')
        return urlparams
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Install_Menu():
    key = SEARCH('Enter Key Phrase To Search For')
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    urlparams  = URL_Params()
#    buildsURL  = 'http://tlbb.me/catmenu.php?x='+encryptme('e',urlparams)
    buildsURL  = 'http://tlbb.me/catsearch.php?search='+encryptme('e',urlparams)+'&k='+encryptme('e',key)
    try:
        link       = encryptme('d',Open_URL2(buildsURL))
        if debug == 'true':
            xbmc.log("### Return orig: "+link)
#    if link !='':
#        xbmc.log("### Return Decrypted: "+encryptme('d',link))
# match without cloudflare enabled
    #match      = re.compile('n="(.+?)"l="(.+?)"t="(.+?)"', re.DOTALL).findall(link)
        match      = re.compile('n="(.+?)"l="(.+?)"', re.DOTALL).findall(link)    
        for name, url in match:
            o0oO('folder',name,url,'install_venz','','','','')
    except:
        Notify('No Response from server','Sorry Please try later','1000',os.path.join(ADDONS,'plugin.program.tbs','resources','cross.png'))     
        xbmc.executebuiltin("Dialog.Close(busydialog)")
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Install_Venz(url):
    Notify('Installing Content','Please be patient during this process','5000',os.path.join(ADDONS,'plugin.program.tbs','resources','update.png'))
    link = Open_URL2(url)
    success = 0
    if debug == 'true':
        xbmc.log(link)
    if link == "record added sucessfully":
        Grab_Updates('http://tlbb.me/comm.php?z=c&x=')
        success = 1
#        xbmc.executebuiltin('Action(Back)')
    else:
        try:
            link = encryptme('d',link).replace('|_|',' ').replace('|!|','\n')
            if debug == 'true':
                xbmc.log('### Install_Venz: %s'%link)
            success = 1
        except:
            pass
    if success == 1:
        match      = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(link)
        for name, thumb, desc, link in match:
            o0oO('',name,link,'openlink',thumb,'','',desc)
#---------------------------------------------------------------------------------------------------
# Function to execute a command
def Exec_XBMC(command):
    xbmc.executebuiltin(command)
    xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
# Function to enable/disable the main menu items - added due to glitch on server
def Main_Menu_Install(menumode):
    if menumode == 'add':
        if xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)'):
            o0oO('','Enable Comedy','Skin.SetString(Custom6HomeItem.Disable,)','exec_xbmc','https://i.ytimg.com/vi/zZ_mFOG1H-o/maxresdefault.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)'):
            o0oO('','Enable Cooking','Skin.SetString(Custom3HomeItem.Disable,)','exec_xbmc','http://videos2.healthination.com/HN_BB_05_EasyCooking_ProRes_739/HN_BB_05_EasyCooking_ProRes_739-img_1280x720.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)'):
            o0oO('','Enable Fitness','Skin.SetString(Custom4HomeItem.Disable,)','exec_xbmc','http://www.fourseasons.com/content/dam/fourseasons/images/web/VGS/VGS_342_aspect16x9.jpg/jcr:content/renditions/cq5dam.web.1280.1280.jpeg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)'):
            o0oO('','Enable Gaming','Skin.SetString(Custom5HomeItem.Disable,)','exec_xbmc','https://cdn2.vox-cdn.com/thumbor/ez8SzxLVWcfCqRlgOdfWsh6lfRc=/0x0:1920x1080/1280x720/cdn0.vox-cdn.com/uploads/chorus_image/image/47030516/youtube-gaming-end-screen_1920.0.0.png','','','')
        if xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)'):
            o0oO('','Enable Kids','Skin.SetString(FavoritesHomeItem.Disable,)','exec_xbmc','http://b.fastcompany.net/multisite_files/fastcompany/imagecache/1280/poster/2014/04/3029893-poster-p-wearable-kid.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)'):
            o0oO('','Enable Live TV','Skin.SetString(LiveTVHomeItem.Disable,)','exec_xbmc','http://www.fci-wardrobes.co.uk/site-assets/import/Presotto/dama-tv-3.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)'):
            o0oO('','Enable Movies','Skin.SetString(MovieHomeItem.Disable,)','exec_xbmc','https://i.ytimg.com/vi/mohrB3ZDqu4/maxresdefault.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)'):
            o0oO('','Enable Music','Skin.SetString(MusicHomeItem.Disable,)','exec_xbmc','http://cienciaetecnologias.com/wp-content/uploads/2013/07/efeito-mozart-musica-inteligencia.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)'):
            o0oO('','Enable News','Skin.SetString(ProgramsHomeItem.Disable,)','exec_xbmc','http://cdn.abclocal.go.com/content/kfsn/images/cms/26184_1280x720.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)'):
            o0oO('','Enable Sports','Skin.SetString(VideosHomeItem.Disable,)','exec_xbmc','http://theartmad.com/wp-content/uploads/2015/08/Different-Sports-Wallpaper-4.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)'):
            o0oO('','Enable Technology','Skin.SetString(Custom2HomeItem.Disable,)','exec_xbmc','http://hpwallpaperku.com/wp-content/uploads/2016/01/Technology-Wallpaper.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)'):
            o0oO('','Enable Travel','Skin.SetString(WeatherHomeItem.Disable,)','exec_xbmc','http://www.travelafghanistan.co.uk/wp-content/uploads/2015/09/jour87ix9aoikm1zpjct.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)'):
            o0oO('','Enable TV Shows','Skin.SetString(TVShowHomeItem.Disable,)','exec_xbmc','http://cd8ba0b44a15c10065fd-24461f391e20b7336331d5789078af53.r23.cf1.rackcdn.com/plex.vanillacommunity.com/ipb/monthly_11_2010/post-25236-048502800%201289080759.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)'):
            o0oO('','Enable World','Skin.SetString(PicturesHomeItem.Disable,)','exec_xbmc','http://cdn.bulbagarden.net/upload/6/68/PokemonWorldAnime.png','','','')
        if xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)'):
            o0oO('','Enable YouTube','Skin.SetString(ShutdownHomeItem.Disable,)','exec_xbmc','https://i.ytimg.com/vi/s5y-4EpmfRQ/maxresdefault.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)'):
            o0oO('','Enable XXX','Skin.SetString(MusicVideoHomeItem.Disable,)','exec_xbmc','http://celebmafia.com/wp-content/uploads/2015/11/bella-thorne-photoshoot-for-glamour-magazine-mexico-december-2015-_1.jpg','','','')
    if menumode == 'remove':
        if not xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)'):
            o0oO('','Disable Comedy','Skin.SetString(Custom6HomeItem.Disable,True)','exec_xbmc','https://i.ytimg.com/vi/zZ_mFOG1H-o/maxresdefault.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)'):
            o0oO('','Disable Cooking','Skin.SetString(Custom3HomeItem.Disable,True)','exec_xbmc','http://videos2.healthination.com/HN_BB_05_EasyCooking_ProRes_739/HN_BB_05_EasyCooking_ProRes_739-img_1280x720.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)'):
            o0oO('','Disable Fitness','Skin.SetString(Custom4HomeItem.Disable,True)','exec_xbmc','http://www.fourseasons.com/content/dam/fourseasons/images/web/VGS/VGS_342_aspect16x9.jpg/jcr:content/renditions/cq5dam.web.1280.1280.jpeg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)'):
            o0oO('','Disable Gaming','Skin.SetString(Custom5HomeItem.Disable,True)','exec_xbmc','https://cdn2.vox-cdn.com/thumbor/ez8SzxLVWcfCqRlgOdfWsh6lfRc=/0x0:1920x1080/1280x720/cdn0.vox-cdn.com/uploads/chorus_image/image/47030516/youtube-gaming-end-screen_1920.0.0.png','','','')
        if not xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)'):
            o0oO('','Disable Kids','Skin.SetString(FavoritesHomeItem.Disable,True)','exec_xbmc','http://b.fastcompany.net/multisite_files/fastcompany/imagecache/1280/poster/2014/04/3029893-poster-p-wearable-kid.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)'):
            o0oO('','Disable Live TV','Skin.SetString(LiveTVHomeItem.Disable,True)','exec_xbmc','http://www.fci-wardrobes.co.uk/site-assets/import/Presotto/dama-tv-3.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)'):
            o0oO('','Disable Movies','Skin.SetString(MovieHomeItem.Disable,True)','exec_xbmc','https://i.ytimg.com/vi/mohrB3ZDqu4/maxresdefault.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)'):
            o0oO('','Disable Music','Skin.SetString(MusicHomeItem.Disable,True)','exec_xbmc','http://cienciaetecnologias.com/wp-content/uploads/2013/07/efeito-mozart-musica-inteligencia.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)'):
            o0oO('','Disable News','Skin.SetString(ProgramsHomeItem.Disable,True)','exec_xbmc','http://cdn.abclocal.go.com/content/kfsn/images/cms/26184_1280x720.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)'):
            o0oO('','Disable Sports','Skin.SetString(VideosHomeItem.Disable,True)','exec_xbmc','http://theartmad.com/wp-content/uploads/2015/08/Different-Sports-Wallpaper-4.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)'):
            o0oO('','Disable Technology','Skin.SetString(Custom2HomeItem.Disable,True)','exec_xbmc','http://hpwallpaperku.com/wp-content/uploads/2016/01/Technology-Wallpaper.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)'):
            o0oO('','Disable Travel','Skin.SetString(WeatherHomeItem.Disable,True)','exec_xbmc','http://www.travelafghanistan.co.uk/wp-content/uploads/2015/09/jour87ix9aoikm1zpjct.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)'):
            o0oO('','Disable TV Shows','Skin.SetString(TVShowHomeItem.Disable,True)','exec_xbmc','http://cd8ba0b44a15c10065fd-24461f391e20b7336331d5789078af53.r23.cf1.rackcdn.com/plex.vanillacommunity.com/ipb/monthly_11_2010/post-25236-048502800%201289080759.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)'):
            o0oO('','Disable World','Skin.SetString(PicturesHomeItem.Disable,True)','exec_xbmc','http://cdn.bulbagarden.net/upload/6/68/PokemonWorldAnime.png','','','')
        if not xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)'):
            o0oO('','Disable YouTube','Skin.SetString(ShutdownHomeItem.Disable,True)','exec_xbmc','https://i.ytimg.com/vi/s5y-4EpmfRQ/maxresdefault.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)'):
            o0oO('','Disable XXX','Skin.SetString(MusicVideoHomeItem.Disable,True)','exec_xbmc','http://celebmafia.com/wp-content/uploads/2015/11/bella-thorne-photoshoot-for-glamour-magazine-mexico-december-2015-_1.jpg','','','')
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog - try the built-in multiselect or fallback to pre-jarvis workaround
def multidialog(title, mylist, images, description):
    try:
        ret = dialog.multiselect(title, mylist)
    except:
        ret = multiselect(title, mylist, images, description)
    return ret if not ret == None else []
#---------------------------------------------------------------------------------------------------
# Multiselect Dialog for older Kodi versions (pre Jarvis)
def multiselect(title, mylist, images, description):
    global pos
    global listicon
    class MultiChoiceDialog(pyxbmct.AddonDialogWindow):
        def __init__(self, title="", items=None, images=None, description=None):
            super(MultiChoiceDialog, self).__init__(title)
            self.setGeometry(1100, 700, 9, 9)
            self.selected = []
            self.set_controls()
            self.connect_controls()
            self.listing.addItems(items or [])
            self.set_navigation()
            self.connect(ACTION_NAV_BACK, self.close)
            self.connect(ACTION_MOVE_UP, self.update_list)
            self.connect(ACTION_MOVE_DOWN, self.update_list)
            
        def set_controls(self):
            self.listing = pyxbmct.List(_imageWidth=15)
            self.placeControl(self.listing, 0, 0, rowspan=9, columnspan=5, pad_y=10) # grid reference, start top left and span 9 boxes down and 5 across
            Icon=pyxbmct.Image(images[0], aspectRatio=2) # set aspect ratio to keep original
            Icon.setImage(images[0])
            self.placeControl(Icon, 0, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox = pyxbmct.TextBox()
            self.placeControl(self.textbox, 4, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox.setText(description[0])
            self.ok_button = pyxbmct.Button("OK")
            self.placeControl(self.ok_button, 7, 5, pad_x=10, pad_y=10)
            self.cancel_button = pyxbmct.Button("Cancel")
            self.placeControl(self.cancel_button, 7, 6, pad_x=10, pad_y=10)

        def connect_controls(self):
            self.connect(self.listing, self.check_uncheck)
            self.connect(self.ok_button, self.ok)
            self.connect(self.cancel_button, self.close)

        def set_navigation(self):
            self.listing.controlLeft(self.ok_button)
            self.listing.controlRight(self.ok_button)
            self.ok_button.setNavigation(self.listing, self.listing, self.cancel_button, self.cancel_button)
            self.cancel_button.setNavigation(self.listing, self.listing, self.ok_button, self.ok_button)
            if self.listing.size():
                self.setFocus(self.listing)
            else:
                self.setFocus(self.cancel_button)
            
        def update_list(self):
            pos      = self.listing.getSelectedPosition()
            listicon = images[pos]
            Icon=pyxbmct.Image(listicon, aspectRatio=2)
            Icon.setImage(listicon)
            self.placeControl(Icon, 0, 5, rowspan=3, columnspan=3, pad_x=10, pad_y=10)
            self.textbox.setText(description[pos])

        def check_uncheck(self):
            list_item = self.listing.getSelectedItem()
            if list_item.getLabel2() == "checked":
                list_item.setIconImage("")
                list_item.setLabel2("unchecked")
            else:
                list_item.setIconImage(checkicon)
                list_item.setLabel2("checked")

        def ok(self):
            self.selected = [index for index in xrange(self.listing.size())
                            if self.listing.getListItem(index).getLabel2() == "checked"]
            super(MultiChoiceDialog, self).close()

        def close(self):
            self.selected = []
            super(MultiChoiceDialog, self).close()
            
    dialog = MultiChoiceDialog(title, mylist, images, description)
    dialog.doModal()
    return dialog.selected
    del dialog
#---------------------------------------------------------------------------------------------------
# Function to show add to menu items from online
def Install_Venz_Menu(function):
    function_orig = function
    urlparams  = URL_Params()
    try:
        if '||' in function:
            function,menutype,menu = function.split('||')
        else:
            menutype = ''
            menu     = ''
        menu = menu.replace('_',' ').lower()

        buildsURL  = 'http://tlbb.me/catsearch.php?search='+function+'&x='+encryptme('e',urlparams)
        xbmc.log(buildsURL)
        link_orig  = Open_URL2(buildsURL)
        link       = encryptme('d',link_orig).replace('|_|',' ').replace('|!|','\n')
        if debug == 'true':
            xbmc.log('#### '+encryptme('d',link_orig).replace('|_|',' ').replace('|!|','\n'))
        
        failed       = 0
        contentarray = []
        contenturl   = []
        imagearray   = []
        descarray    = []
#        tryagain = 0
#        if int(len(link_orig)) < 11:
#            failed = 1
#            choice = dialog.yesno('No Content Found','Sorry no content could be found that matches your criteria.[CR]There may be a temporary glitch with your internet connection at this time, would you like to try again?')
#            if choice:
#                tryagain = 1

#        if debug == 'true':
        xbmc.log("### Return orig: "+link)
        xbmc.log("### FUNCTION: "+function)
        if failed == 0:
            match      = re.compile('name="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(link)    
            for name, thumb, desc, url in match:
                if function == 'main_menu':
                    if not 'Remove' in name:
                        o0oO('',name.replace('_',' '),url,'install_venz',thumb,'','',desc)

                if menutype == 'add_main':
                        if thirdparty == 'false':
                            if menu+' menu' in name.lower() and not 'Remove' in name and not 'by box' in name:
#                                o0oO('',name.replace('_',' ').replace(' to the '+menu.replace('_',' ').title()+' Menu',''),url,'install_venz',thumb,'','',desc)
                                contenturl.append(url)
                                contentarray.append(name)
                                imagearray.append(thumb)
                                descarray.append(desc)
                        else:
                            if menu+' menu' in name.lower() and not 'Remove' in name:
#                                o0oO('',name.replace('_',' ').replace(' to the '+menu.replace('_',' ').title()+' Menu',''),url,'install_venz',thumb,'','',desc)
                                contenturl.append(url)
                                contentarray.append(name)
                                imagearray.append(thumb)
                                descarray.append(desc)

                elif menutype == 'add_sub':
                    if thirdparty == 'false':
                        if 'Remove' not in name and not 'by box' in name:
                            o0oO('',name.replace('_',' ').replace(' to the '+menu.title()+' SubMenu',''),url,'install_venz',thumb,'','',desc)
                    else:
                        if 'Remove' not in name:
                            o0oO('',name.replace('_',' ').replace(' to the '+menu.title()+' SubMenu',''),url,'install_venz',thumb,'','',desc)

                elif menutype == 'remove_main':
                    if menu+' menu' in name.lower() and not 'Add ' in name:
  #                      o0oO('',name.replace('_',' ').replace(' from the '+menu.replace('_',' ').title()+' Menu',''),url,'install_venz',thumb,'','',desc)
                        contenturl.append(url)
                        contentarray.append(name)
                        imagearray.append(thumb)
                        descarray.append(desc)

                elif menutype == 'remove_sub':
                    if 'Add ' not in name:
                        o0oO('',name.replace('_',' ').replace(' from the '+menu.title()+' SubMenu',''),url,'install_venz',thumb,'','',desc)

                elif menutype == '' and menu == '' and function != 'main_menu':
                    if 'Remove' not in name:
                        o0oO('',name.replace('_',' '),url,'install_venz',thumb,'','',desc)
    except:
        Notify('No Response from server','Sorry Please try later','1000',os.path.join(ADDONS,'plugin.program.tbs','resources','cross.png'))

    if menutype == 'add_main' or menutype == 'remove_main':
        if len(contentarray) > 0:
            choices = multiselect('Select from the list below',contentarray,imagearray,descarray)
            if len(choices) > 0:
                Notify('Installing Content','Please be patient during this process','5000',os.path.join(ADDONS,'plugin.program.tbs','resources','update.png'))
                for item in choices:
                    Open_URL2(contenturl[item])
                Grab_Updates('http://tlbb.me/comm.php?multi&z=c&x=')
                xbmc.executebuiltin('ActivateWindow(HOME)')
        else:
            dialog.ok('NO CONTENT AVAILABLE','Oops...', 'Sorry it looks like this section is a work in progress.', 'Please come back at a later date as new content is added on a regular basis.')
        #    if tryagain == 1:
  #      Install_Venz_Menu(function_orig)
#---------------------------------------------------------
#Function to pull commands and update
def DLE(command,repo_link,repo_id):
    check1='DLE'
    downloadpath = os.path.join(packages,'updates.zip')
    if not os.path.exists(packages):
        os.makedirs(packages)
    
    if command=='delete':
        shutil.rmtree(xbmc.translatePath(repo_link))
        Update_Repo()
    
    if command=='addons' or command=='ADDON_DATA' or command=='media' or command=='config' or command=='playlists' or command == 'custom':
#        dp.create('Installing Content','','')
        if not os.path.exists(os.path.join(ADDONS,repo_id)) or repo_id == '':
            try:
                downloader.download(repo_link, downloadpath)
            except:
                pass       
        if (command=="addons" and not os.path.exists(os.path.join(ADDONS,repo_id))) or (command=='addons' and repo_id==''):
            try:
                extract.all(downloadpath, ADDONS)
                Update_Repo()
            except:
                pass

        if command=='ADDON_DATA':
            try:
                extract.all(downloadpath, ADDON_DATA)
            except:
                xbmc.log("### FAILED TO EXTRACT TO "+ADDON_DATA)
        
        if command=='media':
            try:
                extract.all(downloadpath, MEDIA)
            except:
                pass
        
        if command=='config':
            try:
                extract.all(downloadpath, CONFIG)
            except:
                pass

        if command=='playlists':
            try:
                extract.all(downloadpath, PLAYLISTS)
            except:
                pass

        if command=='custom':
            try:
                extract.all(downloadpath, repo_id)
            except:
                xbmc.log("### Failed to extract update "+repo_link)
            
    if os.path.exists(downloadpath):
        try:
            os.remove(downloadpath)
        except:
            pass
#---------------------------------------------------------------------------------------------------
#Option to download guisettings fix that merges with existing settings.
def GUI_Settings_Fix(url,local):
    Check_Download_Path()
    choice = xbmcgui.Dialog().yesno(name, 'This will over-write your existing guisettings.xml.', 'Are you sure this is the build you have installed?', '', nolabel='No, Cancel',yeslabel='Yes, Fix')
    
    if choice == 1:
        GUI_Merge(url,local)
#---------------------------------------------------------------------------------------------------
def GUI_Install(path):
# Read the original skinsettings tags and store in memory ready to replace in guinew.xml
    localfile = open(GUI, mode='r')
    content   = localfile.read()
    localfile.close()

    skinsettingsorig  = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
    skindefault       = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
    lookandfeelorig   = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
    skinorig          = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
    skindefaultorig   = skindefault[0] if (len(skindefault) > 0) else ''
    lookandfeel       = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''

# Read the new guisettings file and get replace skin related settings with original
    localfile2 = open(path, mode='r')
    content2   = localfile2.read()
    localfile2.close()

    skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
    skindefaultcontent  = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
    lookandfeelcontent  = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
    skinsettingstext    = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
    skindefaulttext     = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
    lookandfeeltext     = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
    replacefile         = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)

    xbmc.log("### Attempting to create new guisettings at: %s" % path)
    writefile = open(path, mode='w+')
    writefile.write(str(replacefile))
    writefile.close()
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
def GUI_Merge(url,local):
    success           = False
    profiles_included = 0
    keep_profiles     = 1
    
    if os.path.exists(GUINEW):
        os.remove(GUINEW)
    
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
    
    if os.path.exists(PROFILES):
        os.remove(PROFILES)
    
    if not os.path.exists(guitemp):
        os.makedirs(guitemp)

#Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    try:
        shutil.copyfile(GUI,GUINEW)
    
    except:
        xbmc.log("No guisettings found, most likely due to a previously failed attempt at install")
    
    if local!=1:
        lib=os.path.join(USB, 'guifix.zip')
    
    else:
        lib=xbmc.translatePath(url)

    try:
        downloader.download(url,lib)
    except:
        xbmc.log("Failed to download guisettings")
# Get the size of the downloaded guisettings so we can later add to the id.xml
    guisize=str(os.path.getsize(lib))
    dp.create("Installing Skin Fix","Checking ",'', 'Please Wait')
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,guitemp,dp)
    
    if os.path.exists(os.path.join(guitemp,'script.skinshortcuts')):
        try:
            shutil.rmtree(os.path.join(ADDON_DATA,'script.skinshortcuts'))
        except:
            pass
        os.rename(os.path.join(guitemp,'script.skinshortcuts'),os.path.join(ADDON_DATA,'script.skinshortcuts'))
        
    if local != 'library' or local != 'updatelibrary' or local !='fresh':
        
        try:
            readfile = open(os.path.join(guitemp,'profiles.xml'), mode='r')
            default_contents = readfile.read()
            readfile.close()
            
            if os.path.exists(os.path.join(guitemp,'profiles.xml')):
                
                if local == None:
                    choice = xbmcgui.Dialog().yesno("PROFILES DETECTED", 'This build has profiles included (standard Kodi profiles, not CP Profiles), would you like to overwrite your existing profiles or keep the ones you have?', '','', nolabel='Keep my profiles',yeslabel='Use new profiles')
                
                if local != None:
                    choice = 1
                
                if choice == 1:
                    writefile = open(PROFILES, mode='w')
                    time.sleep(1)
                    writefile.write(default_contents)
                    time.sleep(1)
                    writefile.close()
                    keep_profiles=0
        
        except:
            xbmc.log("no profiles.xml file")

#Copy to addon_data folder so profiles can be dealt with
    os.rename(os.path.join(guitemp,'guisettings.xml'),GUIFIX)
    
    if local != 'fresh':
        choice2 = dialog.yesno("Keep Kodi Settings?", 'Do you want to keep your existing KODI settings (weather, screen calibration, PVR etc.) or wipe and install the ones in this build?', nolabel='Keep my settings',yeslabel='Replace my settings')
    
    if local == 'fresh':
        choice2 = 1
    
    if choice2 == 1:
        
        if os.path.exists(GUI):
            
            try:
                xbmc.log("### Attempting to remove guisettings")
                os.remove(GUI)
                success=True
            
            except:
                xbmc.log("### Problem removing guisettings")
                success=False
            
            try:
                xbmc.log("### Attempting to replace guisettings with new")
                os.rename(GUIFIX,GUI)
                success=True
            
            except:
                xbmc.log("### Failed to replace guisettings with new")
                success=False
    
# Read the original skinsettings tags and store in memory ready to replace in guinew.xml
    if choice2 == 0:
        localfile = open(GUINEW, mode='r')
        content   = localfile.read()
        localfile.close()

        skinsettingsorig  = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
        skindefault       = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
        lookandfeelorig   = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
        skinorig          = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
        skindefaultorig   = skindefault[0] if (len(skindefault) > 0) else ''
        lookandfeel       = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''

# Read the new guisettings file and get replace skin related settings with original
        localfile2 = open(GUIFIX, mode='r')
        content2   = localfile2.read()
        localfile2.close()

        skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
        skindefaultcontent  = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
        lookandfeelcontent  = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
        skinsettingstext    = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
        skindefaulttext     = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
        lookandfeeltext     = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
        replacefile         = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)

        writefile = open(GUINEW, mode='w+')
        writefile.write(str(replacefile))
        writefile.close()

# Replace guisettings with the new ones, check in place to make sure Kodi hasn't recreated them again
        if os.path.exists(GUI):
            
            try:
                os.remove(GUI)
                success=True
            
            except:
                success=False
        
        try:
            os.rename(GUINEW,GUI)
            os.remove(GUIFIX)
            success=True
        
        except:
            success=False
 
# If the guisettings were successfully installed and it's not a local install update the details for id.xml and startup.xml
    if success==True or local == None:
        
        try:
            localfile = open(tempfile, mode='r')
            content   = localfile.read()
            localfile.close()
            
            temp         = re.compile('id="(.+?)"').findall(content)
            tempname     = re.compile('name="(.+?)"').findall(content)
            tempversion  = re.compile('version="(.+?)"').findall(content)
            tempcheck    = temp[0] if (len(temp) > 0) else ''
            namecheck    = tempname[0] if (len(tempname) > 0) else ''
            versioncheck = tempversion[0] if (len(tempversion) > 0) else ''

            writefile = open(idfile, mode='w+')
            writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
            writefile.close()

            localfile = open(startuppath, mode='r')
            content = localfile.read()
            localfile.close()

            localversionmatch  = re.compile('version="(.+?)"').findall(content)
            localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
            replacefile        = content.replace(localversioncheck,versioncheck)

            writefile = open(startuppath, mode='w')
            writefile.write(str(replacefile))
            writefile.close()
            os.remove(tempfile)
        
        except:
            writefile = open(idfile, mode='w+')
            writefile.write('id="None"\nname="Unknown"\nversion="Unknown"\ngui="'+guisize+'"')
            writefile.close()                

# Clean up the temporary files
    if os.path.exists(os.path.join(guitemp,'profiles.xml')):
        os.remove(os.path.join(guitemp,'profiles.xml'))
        time.sleep(1)
    
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
    
    notifypath = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'notification.txt'))
    
    if os.path.exists(notifypath):
        os.remove(notifypath)
    
    if success == True:
        Remove_Textures()
        try:
            CB_Install_Results()
        except:
            pass
        KLL()
#---------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Hardware_Menu(url):
    BaseURL           = 'http://noobsandnerds.com/TI/HardwarePortal/hardwaredetails.php?id=%s' % (url)
    link              = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch         = re.compile('name="(.+?)"').findall(link)
    manufacturermatch = re.compile('manufacturer="(.+?)"').findall(link)
    videoguide1match  = re.compile('video_guide1="(.+?)"').findall(link)
    videoguide2match  = re.compile('video_guide2="(.+?)"').findall(link)
    videoguide3match  = re.compile('video_guide3="(.+?)"').findall(link)
    videoguide4match  = re.compile('video_guide4="(.+?)"').findall(link)
    videoguide5match  = re.compile('video_guide5="(.+?)"').findall(link)
    videolabel1match  = re.compile('video_label1="(.+?)"').findall(link)
    videolabel2match  = re.compile('video_label2="(.+?)"').findall(link)
    videolabel3match  = re.compile('video_label3="(.+?)"').findall(link)
    videolabel4match  = re.compile('video_label4="(.+?)"').findall(link)
    videolabel5match  = re.compile('video_label5="(.+?)"').findall(link)
    shopmatch         = re.compile('shops="(.+?)"').findall(link)
    descmatch         = re.compile('description="(.+?)"').findall(link)
    screenshot1match  = re.compile('screenshot1="(.+?)"').findall(link)
    screenshot2match  = re.compile('screenshot2="(.+?)"').findall(link)
    screenshot3match  = re.compile('screenshot3="(.+?)"').findall(link)
    screenshot4match  = re.compile('screenshot4="(.+?)"').findall(link)
    screenshot5match  = re.compile('screenshot5="(.+?)"').findall(link)
    screenshot6match  = re.compile('screenshot6="(.+?)"').findall(link)
    screenshot7match  = re.compile('screenshot7="(.+?)"').findall(link)
    screenshot8match  = re.compile('screenshot8="(.+?)"').findall(link)
    screenshot9match  = re.compile('screenshot9="(.+?)"').findall(link)
    screenshot10match = re.compile('screenshot10="(.+?)"').findall(link)
    screenshot11match = re.compile('screenshot11="(.+?)"').findall(link)
    screenshot12match = re.compile('screenshot12="(.+?)"').findall(link)
    screenshot13match = re.compile('screenshot13="(.+?)"').findall(link)
    screenshot14match = re.compile('screenshot14="(.+?)"').findall(link)
    addedmatch        = re.compile('added="(.+?)"').findall(link)
    platformmatch     = re.compile('platform="(.+?)"').findall(link)
    chipsetmatch      = re.compile('chipset="(.+?)"').findall(link)
    guidematch        = re.compile('official_guide="(.+?)"').findall(link)
    previewmatch      = re.compile('official_preview="(.+?)"').findall(link)
    thumbmatch        = re.compile('thumbnail="(.+?)"').findall(link)
    stockmatch        = re.compile('stock_rom="(.+?)"').findall(link)
    cpumatch          = re.compile('CPU="(.+?)"').findall(link)
    gpumatch          = re.compile('GPU="(.+?)"').findall(link)
    rammatch          = re.compile('RAM="(.+?)"').findall(link)
    flashmatch        = re.compile('flash="(.+?)"').findall(link)
    wifimatch         = re.compile('wifi="(.+?)"').findall(link)
    bluetoothmatch    = re.compile('bluetooth="(.+?)"').findall(link)
    lanmatch          = re.compile('LAN="(.+?)"').findall(link)
    xbmcmatch         = re.compile('xbmc_version="(.+?)"').findall(link)
    prosmatch         = re.compile('pros="(.+?)"').findall(link)
    consmatch         = re.compile('cons="(.+?)"').findall(link)
    librarymatch      = re.compile('library_scan="(.+?)"').findall(link)
    fourkmatch        = re.compile('4k="(.+?)"').findall(link)
    teneightymatch    = re.compile('1080="(.+?)"').findall(link)
    seventwentymatch  = re.compile('720="(.+?)"').findall(link)
    threedmatch       = re.compile('3D="(.+?)"').findall(link)
    dtsmatch          = re.compile('DTS="(.+?)"').findall(link)
    bootmatch         = re.compile('BootTime="(.+?)"').findall(link)
    copyfilesmatch    = re.compile('CopyFiles="(.+?)"').findall(link)
    copyvideomatch    = re.compile('CopyVideo="(.+?)"').findall(link)
    ethernetmatch     = re.compile('EthernetTest="(.+?)"').findall(link)
    slideshowmatch    = re.compile('Slideshow="(.+?)"').findall(link)
    reviewmatch       = re.compile('total_review="(.+?)"').findall(link)
    whufcleematch     = re.compile('whufclee_review="(.+?)"').findall(link)
    cbmatch           = re.compile('CB_Premium="(.+?)"').findall(link)
   
    name                  = namematch[0] if (len(namematch) > 0) else ''
    manufacturer          = manufacturermatch[0] if (len(manufacturermatch) > 0) else ''
    videoguide1           = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2           = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3           = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4           = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5           = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1           = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2           = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3           = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4           = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5           = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    shop                  = shopmatch[0] if (len(shopmatch) > 0) else ''    
    description           = descmatch[0] if (len(descmatch) > 0) else ''
    screenshot1           = screenshot1match[0] if (len(screenshot1match) > 0) else ''
    screenshot2           = screenshot2match[0] if (len(screenshot2match) > 0) else ''
    screenshot3           = screenshot3match[0] if (len(screenshot3match) > 0) else ''
    screenshot4           = screenshot4match[0] if (len(screenshot4match) > 0) else ''
    screenshot5           = screenshot5match[0] if (len(screenshot5match) > 0) else ''
    screenshot6           = screenshot6match[0] if (len(screenshot6match) > 0) else ''
    screenshot7           = screenshot7match[0] if (len(screenshot7match) > 0) else ''
    screenshot8           = screenshot8match[0] if (len(screenshot8match) > 0) else ''
    screenshot9           = screenshot9match[0] if (len(screenshot9match) > 0) else ''
    screenshot10          = screenshot10match[0] if (len(screenshot10match) > 0) else ''
    screenshot11          = screenshot11match[0] if (len(screenshot11match) > 0) else ''
    screenshot12          = screenshot12match[0] if (len(screenshot12match) > 0) else ''
    screenshot13          = screenshot13match[0] if (len(screenshot13match) > 0) else ''
    screenshot14          = screenshot14match[0] if (len(screenshot14match) > 0) else ''
    added                 = addedmatch[0] if (len(addedmatch) > 0) else ''
    platform              = platformmatch[0] if (len(platformmatch) > 0) else ''
    chipset               = chipsetmatch[0] if (len(chipsetmatch) > 0) else ''
    guide                 = guidematch[0] if (len(guidematch) > 0) else 'None'
    preview               = previewmatch[0] if (len(previewmatch) > 0) else 'None'
    thumb                 = thumbmatch[0] if (len(thumbmatch) > 0) else ''
    stock                 = stockmatch[0] if (len(stockmatch) > 0) else ''
    CPU                   = cpumatch[0] if (len(cpumatch) > 0) else ''
    GPU                   = gpumatch[0] if (len(gpumatch) > 0) else ''
    RAM                   = rammatch[0] if (len(rammatch) > 0) else ''
    flash                 = flashmatch[0] if (len(flashmatch) > 0) else ''
    wifi                  = wifimatch[0] if (len(wifimatch) > 0) else ''
    bluetooth             = bluetoothmatch[0] if (len(bluetoothmatch) > 0) else ''
    LAN                   = lanmatch[0] if (len(lanmatch) > 0) else ''
    xbmc_version          = xbmcmatch[0] if (len(xbmcmatch) > 0) else ''
    pros                  = prosmatch[0] if (len(prosmatch) > 0) else ''
    cons                  = consmatch[0] if (len(consmatch) > 0) else ''
    library               = librarymatch[0] if (len(librarymatch) > 0) else ''
    fourk                 = fourkmatch[0] if (len(fourkmatch) > 0) else ''
    teneighty             = teneightymatch[0] if (len(teneightymatch) > 0) else ''
    seventwenty           = seventwentymatch[0] if (len(seventwentymatch) > 0) else ''
    threed                = threedmatch[0] if (len(threedmatch) > 0) else ''
    DTS                   = dtsmatch[0] if (len(dtsmatch) > 0) else ''
    BootTime              = bootmatch[0] if (len(bootmatch) > 0) else ''
    CopyFiles             = copyfilesmatch[0] if (len(copyfilesmatch) > 0) else ''
    CopyVideo             = copyvideomatch[0] if (len(copyvideomatch) > 0) else ''
    EthernetTest          = ethernetmatch[0] if (len(ethernetmatch) > 0) else ''
    Slideshow             = slideshowmatch[0] if (len(slideshowmatch) > 0) else ''
    review                = reviewmatch[0] if (len(reviewmatch) > 0) else ''
    whufcleevid           = whufcleematch[0] if (len(whufcleematch) > 0) else 'None'
    cb                    = cbmatch[0] if (len(cbmatch) > 0) else ''
    official_description  = str('[COLOR=dodgerblue]Added: [/COLOR]'+added+'[CR][COLOR=dodgerblue]Manufacturer: [/COLOR]'+manufacturer+'[CR][COLOR=dodgerblue]Supported Roms: [/COLOR]'+platform+'[CR][COLOR=dodgerblue]Chipset: [/COLOR]'+chipset+'[CR][COLOR=dodgerblue]CPU: [/COLOR]'+CPU+'[CR][COLOR=dodgerblue]GPU: [/COLOR]'+GPU+'[CR][COLOR=dodgerblue]RAM: [/COLOR]'+RAM+'[CR][COLOR=dodgerblue]Flash: [/COLOR]'+flash+'[CR][COLOR=dodgerblue]Wi-Fi: [/COLOR]'+wifi+'[CR][COLOR=dodgerblue]Bluetooth: [/COLOR]'+bluetooth+'[CR][COLOR=dodgerblue]LAN: [/COLOR]'+LAN+'[CR][CR][COLOR=darkcyan]About: [/COLOR]'+description+'[CR][CR][COLOR=darkcyan]Summary:[/COLOR][CR][CR][COLOR=dodgerblue]Pros:[/COLOR]    '+pros+'[CR][CR][COLOR=dodgerblue]Cons:[/COLOR]  '+cons+'[CR][CR][COLOR=darkcyan]Benchmark Results:[/COLOR][CR][CR][COLOR=dodgerblue]Boot Time:[/COLOR][CR]'+BootTime+'[CR][CR][COLOR=dodgerblue]Time taken to scan 1,000 movies (local NFO files):[/COLOR][CR]'+library+'[CR][CR][COLOR=dodgerblue]Copy 4,000 files (660.8MB) locally:[/COLOR][CR]'+CopyFiles+'[CR][CR][COLOR=dodgerblue]Copy a MP4 file (339.4MB) locally:[/COLOR][CR]'+CopyVideo+'[CR][CR][COLOR=dodgerblue]Ethernet Speed - Copy MP4 (339.4MB) from SMB share to device:[/COLOR][CR]'+EthernetTest+'[CR][CR][COLOR=dodgerblue]4k Playback:[/COLOR][CR]'+fourk+'[CR][CR][COLOR=dodgerblue]1080p Playback:[/COLOR][CR]'+teneighty+'[CR][CR][COLOR=dodgerblue]720p Playback:[/COLOR][CR]'+seventwenty+'[CR][CR][COLOR=dodgerblue]Audio Playback:[/COLOR][CR]'+DTS+'[CR][CR][COLOR=dodgerblue]Image Slideshow:[/COLOR][CR]'+Slideshow)
    official_description2 = str('[COLOR=dodgerblue]Added: [/COLOR]'+added+'[CR][COLOR=dodgerblue]Manufacturer: [/COLOR]'+manufacturer+'[CR][COLOR=dodgerblue]Supported Roms: [/COLOR]'+platform+'[CR][COLOR=dodgerblue]Chipset: [/COLOR]'+chipset+'[CR][COLOR=dodgerblue]CPU: [/COLOR]'+CPU+'[CR][COLOR=dodgerblue]GPU: [/COLOR]'+GPU+'[CR][COLOR=dodgerblue]RAM: [/COLOR]'+RAM+'[CR][COLOR=dodgerblue]Flash: [/COLOR]'+flash+'[CR][COLOR=dodgerblue]Wi-Fi: [/COLOR]'+wifi+'[CR][COLOR=dodgerblue]Bluetooth: [/COLOR]'+bluetooth+'[CR][COLOR=dodgerblue]LAN: [/COLOR]'+LAN+'[CR][CR][COLOR=darkcyan]About: [/COLOR]'+description+'[CR][CR][COLOR=darkcyan]Summary:[/COLOR][CR][CR][COLOR=dodgerblue]Pros:[/COLOR]    '+pros+'[CR][CR][COLOR=dodgerblue]Cons:[/COLOR]  '+cons+'[CR][CR][COLOR=orange]4k Playback:[/COLOR]  '+fourk+'[CR][CR][COLOR=orange]1080p Playback:[/COLOR]  '+teneighty+'[CR][CR][COLOR=orange]720p Playback:[/COLOR]  '+seventwenty+'[CR][CR][COLOR=orange]DTS Compatibility:[/COLOR]  '+DTS+'[CR][CR][COLOR=orange]Time taken to scan 100 movies:[/COLOR]  '+library)
    
    if description != '' and shop !='':
        o0oO('','[COLOR=darkcyan][Text Guide][/COLOR]  Official Description',official_description,'text_guide','Tutorials.png',FANART,'','')    
    if description != '' and shop =='':
        o0oO('','[COLOR=darkcyan][Text Guide][/COLOR]  Official Description',official_description2,'text_guide','Tutorials.png',FANART,'','')    
    if whufcleevid != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]   Benchmark Review',whufcleevid,'play_video','Video_Guide.png',FANART,'','')    
    if preview != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]   Official Video Preview',preview,'play_video','Video_Guide.png',FANART,'','')    
    if guide != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]   Official Video Guide',guide,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide1 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide2 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide3 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide4 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide5 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video','Video_Guide.png',FANART,'','')    
#---------------------------------------------------------------------------------------------------
#Hardware Root menu listings
def Hardware_Root_Menu():
    o0oO('folder','[COLOR=darkcyan]Manual Search[/COLOR]', 'hardware', 'manual_search', 'Manual_Search.png','','','')
    o0oO('folder','[COLOR=lime]All Devices[/COLOR]', '', 'grab_hardware', 'All.png','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Game Consoles', 'device=Console', 'grab_hardware', 'Consoles.png','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] HTPC', 'device=HTPC', 'grab_hardware', 'HTPC.png','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Phones', 'device=Phone', 'grab_hardware', 'Phones.png','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Set Top Boxes', 'device=STB', 'grab_hardware', 'STB.png','','','')
    o0oO('folder','[COLOR=orange][Hardware][/COLOR] Tablets', 'device=Tablet', 'grab_hardware', 'Tablets.png','','','')
    o0oO('folder','[COLOR=dodgerblue][Accessories][/COLOR] Remotes/Keyboards', 'device=Remote', 'grab_hardware', 'Remotes.png','','','')
    o0oO('folder','[COLOR=dodgerblue][Accessories][/COLOR] Gaming Controllers', 'device=Controller', 'grab_hardware', 'Controllers.png','','','')
    o0oO('folder','[COLOR=dodgerblue][Accessories][/COLOR] Dongles', 'device=Dongle', 'grab_hardware', 'Dongles.png','','','')
#---------------------------------------------------------------------------------------------------
#CPU Root menu listings
def Hardware_Filter_Menu(url):
    o0oO('folder','[COLOR=darkcyan][CPU][/COLOR] Allwinner Devices', str(url)+'&chip=Allwinner', 'grab_hardware', 'Allwinner.png','','','')
    o0oO('folder','[COLOR=darkcyan][CPU][/COLOR] AMLogic Devices', str(url)+'&chip=AMLogic', 'grab_hardware', 'AMLogic.png','','','')
    o0oO('folder','[COLOR=darkcyan][CPU][/COLOR] Intel Devices', str(url)+'&chip=Intel', 'grab_hardware', 'Intel.png','','','')
    o0oO('folder','[COLOR=darkcyan][CPU][/COLOR] Rockchip Devices', str(url)+'&chip=Rockchip', 'grab_hardware', 'Rockchip.png','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Android', str(url)+'&platform=Android', 'grab_hardware', 'Android.png','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] iOS', str(url)+'&platform=iOS', 'grab_hardware', 'iOS.png','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Linux', str(url)+'&platform=Linux', 'grab_hardware', 'Linux.png','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] OpenELEC', str(url)+'&platform=OpenELEC', 'grab_hardware', 'OpenELEC.png','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] OSX', str(url)+'&platform=OSX', 'grab_hardware', 'OSX.png','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Pure Linux', str(url)+'&platform=Custom_Linux', 'grab_hardware', 'Custom_Linux.png','','','')
    o0oO('folder','[COLOR=lime][Platform][/COLOR] Windows', str(url)+'&platform=Windows', 'grab_hardware', 'Windows.png','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 4GB', str(url)+'&flash=4GB', 'grab_hardware', 'Flash.png','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 8GB', str(url)+'&flash=8GB', 'grab_hardware', 'Flash.png','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 16GB', str(url)+'&flash=16GB', 'grab_hardware', 'Flash.png','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 32GB', str(url)+'&flash=32GB', 'grab_hardware', 'Flash.png','','','')
    o0oO('folder','[COLOR=orange][Flash Storage][/COLOR] 64GB', str(url)+'&flash=64GB', 'grab_hardware', 'Flash.png','','','')
    o0oO('folder','[COLOR=dodgerblue][RAM][/COLOR] 1GB', str(url)+'&ram=1GB', 'grab_hardware', 'RAM.png','','','')
    o0oO('folder','[COLOR=dodgerblue][RAM][/COLOR] 2GB', str(url)+'&ram=2GB', 'grab_hardware', 'RAM.png','','','')
    o0oO('folder','[COLOR=dodgerblue][RAM][/COLOR] 4GB', str(url)+'&ram=4GB', 'grab_hardware', 'RAM.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Fix the blank on-screen keyboard when using Gotham skins on Helix.
#BIG THANKS TO MIKEY1234 FOR THIS SECTION OF CODE, IT HAS BEEN TAKEN FROM THE XUNITY MAINTENANCE ADDON.
def Helix():
    skin = xbmc.getSkinDir()
    path = xbmc.translatePath(os.path.join(ADDONS, skin))
    
    for root, dirs, files in os.walk(path):
       
       for f in files:
            
            if 'DialogKeyboard.xml' in f:
                skin   = os.path.join(root, f)
                a      = open(skin).read()
                CHANGE = a.replace('<control type="label" id="310"','<control type="edit" id="312"')
                f      = open(skin, mode='w')
                f.write(CHANGE)
                f.close()     
                changekeys(skin)
                
                for i in range(48, 58):
                    changenumber(i,skin)
    
    dialog = xbmcgui.Dialog()
    dialog.ok("Skin Changes Successful", 'A BIG thank you to Mikey1234 for this fix. The code used for this function was ported from the Xunity Maintenance add-on')
    xbmc.executebuiltin('ReloadSkin()')   
#---------------------------------------------------------------------------------------------------
def Helix_Confirm():
    dialog = xbmcgui.Dialog()
    confirm = xbmcgui.Dialog().yesno('Convert This Skin To Kodi (Helix)?', 'This will fix the problem with a blank on-screen keyboard showing in skins designed for Gotham (being run on Kodi). This will only affect the currently running skin.', nolabel='No, Cancel',yeslabel='Yes, Fix')
    
    if confirm == 1:
        Helix()
#-----------------------------------------------------------------------------------------------------------------          
#Hide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Hide_Passwords():
    if dialog.yesno("Hide Passwords", "This will hide all your passwords in your", "add-on settings, are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if not 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('/',' option="hidden"/') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok("Passwords Hidden", "Your passwords will now show as stars (hidden), if you want to undo this please use the option to unhide passwords.") 
#---------------------------------------------------------------------------------------------------
#Function to download guisettings.xml and merge with existing.
def INSTALL_PART2(url):
    BaseURL          = 'http://noobsandnerds.com/TI/Community_Builds/guisettings.php?id=%s' % (url)
    link             = Open_URL(BaseURL).replace('\n','').replace('\r','')
    guisettingsmatch = re.compile('guisettings="(.+?)"').findall(link)
    guisettingslink  = guisettingsmatch[0] if (len(guisettingsmatch) > 0) else 'None'
    
    GUI_Merge(guisettingslink,local)
#---------------------------------------------------------------------------------------------------
#Installs special art for premium.
def Install_Art(path):
    background_art = xbmc.translatePath(os.path.join(USERDATA,'background_art',''))
    
    if os.path.exists(background_art):
        Destroy_Path(background_art)
    
    time.sleep(1)
    
    if not os.path.exists(background_art):
        os.makedirs(background_art)
    
    try:
        dp.create("Installing Artwork","Downloading artwork pack",'', 'Please Wait')
        artpack=os.path.join(USB, I1IiiI+'_artpack.zip')
        downloader.download(path, artpack, dp)
        time.sleep(1)
        dp.create("Installing Artwork","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(artpack,background_art,dp)
    
    except:
        pass
#---------------------------------------------------------------------------------------------------
# Menu to install content via the TR add-on
def Install_Content(url):
#    o0oO('folder','Search For Content','','search_content', 'Search_Addons.png','','','')
    o0oO('','Install A Venztech Code', keywordpath, 'keywords', 'Keywords.png','','','')
    o0oO('','Install From Zip','','install_from_zip','','','','')
    o0oO('','Browse My Repositories','','browse_repos','','','','')
#---------------------------------------------------------------------------------------------------
#Browse pre-installed repo's via the kodi add-on browser
def Install_From_Zip():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://install/",return)')
#---------------------------------------------------------------------------------------------------
#Step 2 of the addon install process (installs the repo if one exists)
def Install_Repo(repo_id):
    repostatus   = 1
    BaseURL      = 'http://noobsandnerds.com/TI/AddonPortal/dependencyinstall.php?id=%s' % (repo_id)
    link         = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch    = re.compile('name="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    repourlmatch = re.compile('repo_url="(.+?)"').findall(link)
    dataurlmatch = re.compile('data_url="(.+?)"').findall(link)
    zipurlmatch  = re.compile('zip_url="(.+?)"').findall(link)
    repoidmatch  = re.compile('repo_id="(.+?)"').findall(link)  
    reponame     = namematch[0] if (len(namematch) > 0) else ''
    version      = versionmatch[0] if (len(versionmatch) > 0) else ''
    repourl      = repourlmatch[0] if (len(repourlmatch) > 0) else ''
    dataurl      = dataurlmatch[0] if (len(dataurlmatch) > 0) else ''
    zipurl       = zipurlmatch[0] if (len(zipurlmatch) > 0) else ''
    repoid       = repoidmatch[0] if (len(repoidmatch) > 0) else ''
    repozipname  = xbmc.translatePath(os.path.join(packages,repoid+'.zip')) 
    repolocation = xbmc.translatePath(os.path.join(ADDONS,repoid))

    dp.create('Installing Repository','Please wait...','')
    
    try:
        downloader.download(repourl, repozipname, dp)
        extract.all(repozipname, ADDONS, dp)
        xbmc.executebuiltin('UpdateLocalAddons')
        xbmc.executebuiltin( 'UpdateAddonRepos' )
    
    except:
        
        try:
            downloader.download(zipurl, repozipname, dp)
            extract.all(repozipname, ADDONS, dp)
            xbmc.executebuiltin('UpdateLocalAddons')
            xbmc.executebuiltin( 'UpdateAddonRepos' )
        
        except:
            
            try:
                
                if not os.path.exists(repolocation):
                    os.makedirs(repolocation)
                
                link = Open_URL(dataurl).replace('\n','').replace('\r','')
                match=re.compile('href="(.+?)"', re.DOTALL).findall(link)
                
                for href in match:
                    filepath=xbmc.translatePath(os.path.join(repolocation,href))
                    
                    if addon_id not in href and '/' not in href:
                        
                        try:
                            dp.update(0,"Downloading [COLOR=darkcyan]"+href+'[/COLOR]','','Please wait...')
                            downloader.download(dataurl+href, filepath, dp)
                        
                        except:
                            xbmc.log("failed to install"+href)
                    
                    if '/' in href and '..' not in href and 'http' not in href:
                        remote_path = dataurl+href
                        Recursive_Loop(filepath,remote_path)
            
            except:
                dialog.ok("Error downloading repository", 'There was an error downloading[CR][COLOR=dodgerblue]'+reponame+'[/COLOR]. Please consider updating the add-on portal with details or report the error on the forum at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR]')
                repostatus=0
    
# If repository successfully installed add increment
    if repostatus==1:
        time.sleep(1)
        dp.update(0,"[COLOR=darkcyan]"+reponame+'[/COLOR]  [COLOR=lime]Successfully Installed[/COLOR]','','Now installing dependencies')
        time.sleep(1)
        incremental = 'http://noobsandnerds.com/TI/AddonPortal/downloadcount.php?id=%s' % (repo_id)
        try:
            Open_URL(incremental)
        except:
            pass
#---------------------------------------------------------------------------------------------------
#Create How To (instructions) menu
def Instructions():
    o0oO('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  What is Community Builds?','url','instructions_3','How_To.png','','','')
    o0oO('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  Creating a Community Build','url','instructions_1','How_To.png','','','')
    o0oO('','[COLOR=dodgerblue][TEXT GUIDE][/COLOR]  Installing a Community Build','url','instructions_2','How_To.png','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Add Your Own Guides @ [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR]','K0XIxEodUhc','play_video','How_To.png','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Community Builds FULL GUIDE',"ewuxVfKZ3Fs",'play_video','howto.png','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  IMPORTANT initial settings',"1vXniHsEMEg",'play_video','howto.png','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Install a Community Build',"kLsVOapuM1A",'play_video','howto.png','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  Fixing a half installed build (guisettings.xml fix)',"X8QYLziFzQU",'play_video','howto.png','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  [COLOR=darkcyan](OLD METHOD)[/COLOR]Create a Community Build (part 1)',"3rMScZF2h_U",'play_video','howto.png','','','')
    o0oO('','[COLOR=lime][VIDEO GUIDE][/COLOR]  [COLOR=darkcyan](OLD METHOD)[/COLOR]Create a Community Build (part 2)',"C2IPhn0OSSw",'play_video','howto.png','','','')
#---------------------------------------------------------------------------------------------------
#(Instructions) Create a community backup
def Instructions_1():
    TXT.TXT('Creating A Backup To Share', 
    '[COLOR=gold]THE OPTIONS:[/COLOR][CR]There are 3 options when choosing to create a backup, we shall explain here the differences between them:[CR][CR]'
    '[COLOR=dodgerblue]1. noobsandnerds Community Build[/COLOR] - This is by far the best way to create a build that you want to share with others, it will create a zip file for you to share that can only be used on with this add-on. The size of the zip will be incredibly small compared to other backup options out there and it will also do lots of other clever stuff too such as error checking against the Addon Portal and the addons will always be updated via the relevant developer repositories. Added to this when it comes to updating it\'s a breeze, only the new addons not already on the system will be installed and for the majority of builds Kodi won\'t even have to restart after installing![CR][CR]'
    '[COLOR=dodgerblue]2. Universal Build[/COLOR] - This was the original method created by TotalXBMC, we would really only recommend this if for some strange reason you want your build available on other inferior wizards. The zip size is much larger and every time someone wants to update their build they have to download and install the whole thing again which can be very frustrating and time consuming. The whole build is backed up in full with the exception of the packages and thumbnails folder. Just like the option above all physical paths (so long as they exist somewhere in the Kodi environment) will be changed to special paths so they work on all devices.[CR][CR]'
    '[COLOR=dodgerblue]3. Full Backup[/COLOR] - It\'s highly unlikely you will ever want to use this option and it\'s more for the geeks out there. It will create a complete backup of your setup and not do any extra clever stuff. Things like packages will remain intact as will temp cache files, be warned the size could be VERY large![CR][CR]'
    '[CR][COLOR=gold]CREATING A COMMUNITY BUILD:[/COLOR][CR][CR][COLOR=blue][B]Step 1:[/COLOR] Remove any sensitive data[/B][CR]Make sure you\'ve removed any sensitive data such as passwords and usernames in your addon_data folder.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Backup your system[/B][CR]Choose the backup option you want from the list on the previous page, if you\'re sharing this via the CP Addon then please use the noobsandnerds backup option, this will create two zip files that you need to upload to a server.'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip files to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - archive.org and copy.com are two good examples. Do not use Dropbox unless you have a paid account, they have a fair useage policy and the chances are you\'ll find within 24 hours your download has been blocked and nobody can download it. [COLOR=lime]Top Tip: [/COLOR]The vast majority of problems occur when the wrong download URL has been entered in the online form, a good download URL normally ends in "=1" or "zip=true". Please double check when you copy the URL into a web browser it immediately starts downloading without the need to press any other button.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4:[/COLOR] Submit the build[/B]'
    '[CR]Create a thread on the Community Builds section of the forum at [COLOR=orange]www.noobs[/COLOR][COLOR=dodgerblue]and[/COLOR][COLOR=orange]nerds.com[/COLOR].[CR]Full details can be found on there of the template you should use when posting, once you\'ve created your support thread (NOT BEFORE) you can request to become a member of the Community Builder group and you\'ll then be able to add your build via the web form. As soon as you\'ve successfully added the details your build will be live, if you can\'t find it in the CP addon make sure you have XXX enabled (if you marked it as having adult content) and also make sure you\'re running the same version of Kodi that you said it was compatible with. If you\'re running another version then you can select the option to "show all community builds" in the addon settings and that will show even the builds that aren\'t marked as compatible with your version of Kodi.'
    '[CR][CR][COLOR=gold]PRIVATE BUILDS[/COLOR][CR]If you aren\'t interested in sharing your build with the community you can still use our system for private builds. Just follow the instructions above but you will not need to create a support thread and you WILL require a minimum of 5 useful (not spam) posts on the forum. The 5 post rule only applies to users that wish to use the private builds option. Once you have 5 posts you\'ll be able to access the web form and in there you can enter up to 3 IP addresses that you want to be able to view your build(s). Anybody caught disobeying the forum rules will be banned so please make sure you understand the forum rules before posting, we welcome everyone but there is strictly no spamming or nonsense posts just saying something like "Thanks" in order to bump up your post count. The site rules even have examples of how you can get to 5 posts without receiving a ban.')
#---------------------------------------------------------------------------------------------------
#(Instructions) Install a community build   
def Instructions_2():
    TXT.TXT('Installing a build', '[COLOR=dodgerblue][B]Step 1 (Optional):[/COLOR] Backup your system[/B][CR]When selecting an install option you\'ll be asked if you want to create a backup - we strongly recommend creating a backup of your system in case you don\'t like the build and want to revert back. Remember your backup may be quite large so if you\'re using a device with a very small amount of storage we recommend using a USB stick or SD card as the storage location otherwise you may run out of space and the install may fail.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Choose an install method:[/B][CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]1. Overwrite my current setup & install new build:[/COLOR] This copy over the whole build[CR]As the title suggests this will overwrite your existing setup with the one created by the community builder. We recommend using the wipe option in the maintenance section before running this, that will completely wipe your existing settings and will ensure you don\'t have any conflicting data left on the device. Once you\'ve wiped please restart Kodi and install the build, you can of course use this install option 1 without wiping but you may encounter problems. If you choose to do this DO NOT bombard the community builder with questions on how to fix certain things, they will expect you to have installed over a clean setup and if you\'ve installed over another build the responsibility for bug tracking lies solely with you!'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]2. Install:[/COLOR] Keep my library & profiles[CR]This will install a build over the top of your existing setup so you won\'t lose anything already installed in Kodi. Your library and any profiles you may have setup will also remain unchanged.'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]3. Install:[/COLOR] Keep my library only[CR]This will do exactly the same as number 2 (above) but it will delete any profiles you may have and replace them with the ones the build author has created.'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=gold]4. Install:[/COLOR] Keep my profiles only[CR]Again, the same as number 2 but your library will be replaced with the one created by the build author. If you\'ve spent a long time setting up your library and have it just how you want it then use this with caution and make sure you do a backup!'
    '[CR][CR]-------------------------------------------------------[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Replace or keep settings?[/B][CR]When completing the install process you\'ll be asked if you want to keep your existing Kodi settings or replace with the ones in the build. If you choose to keep your settings then only the important skin related settings are copied over from the build. All your other Kodi settings such as screen calibration, region, audio output, resolution etc. will remain intact. Choosing to replace your settings could possibly cause a few issues, unless the build author has specifically recommended you replace the settings with theirs we would always recommend keeping your own.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4: [/COLOR][COLOR=red]VERY IMPORTANT[/COLOR][/B][CR]For the install to complete properly Kodi MUST force close, this means forcing it to close via your operating system rather than elegantly via the Kodi menu. By default this add-on will attempt to make your operating system force close Kodi but there are systems that will not allow this (devices that do not allow Kodi to have root permissions).'
    ' Once the final step of the install process has been completed you\'ll see a dialog explaining Kodi is attempting a force close, please be patient and give it a minute. If after a minute Kodi hasn\'t closed or restarted you will need to manually force close. The recommended solution for force closing is to go into your operating system menu and make it force close the Kodi app but if you dont\'t know how to do that you can just pull the power from the unit.'
    ' Pulling the power is fairly safe these days, on most set top boxes it\'s the only way to switch them off - they rarely have a power switch. Even though it\'s considered fairly safe nowadays you do this at your own risk and we would always recommend force closing via the operating system menu.')
#---------------------------------------------------------------------------------------------------
#(Instructions) What is a keyword
def Instructions_3():
    TXT.TXT('What is a noobsandnerds keyword?', '[COLOR=gold]WHAT IS A KEYWORD?[/COLOR][CR]The noobsandnerds keywords are based on the ingenious TLBB keyword system that was introduced years ago. It\'s nothing new and unlike certain other people out there we\'re not going to claim it as our idea. If you\'re already familiar with TLBB Keywords or even some of the copies out there like Cloudwords you will already know how this works but for those of you that don\'t have one of those devices we\'ll just go through the details...'
    '[CR][CR]Anyone in the community can make their own keywords and share them with others, it\'s a simple word you type in and then the content you uploaded to the web is downloaded and installed. Previously keywords have mostly been used for addon packs, this is a great way to get whole packs of addons in one go without the need to install a whole new build. We are taking this to the next level and will be introducing artwork packs and also addon fixes. More details will be available in the Community Portal section of the forum on www.noobsandnerds.com'
    '[CR][CR][CR][COLOR=gold]HOW DO I FIND A KEYWORD?[/COLOR][CR]The full list of noobsandnerds keywords can be found on the forum, in the Community Portal section you\'ll see a section for the keywords at the top of the page. Just find the pack you would like to install then using this addon type the keyword in when prompted (after clicking "Install a noobsandnerds keyword"). Your content will now be installed, if installing addon packs please be patient while each addon updates to the latest version directly from the developers repo.'
    '[CR][CR][CR][COLOR=gold]CAN I USE OTHER KEYWORDS?[/COLOR] (Cloudwords, TLBB etc.)[CR]Yes you can, just go to the addon settings and enter the url shortener that particular company use. Again you will find full details of supported keywords on the forum.')
#---------------------------------------------------------------------------------------------------
#(Instructions) How to create a keyword
def Instructions_4():
    TXT.TXT('How to create a keyword?', '[COLOR=gold]NaN MAKE IT EASY![/COLOR][CR]The keywords can now be made very simply by anyone. We\'ve not locked this down to just our addon and others can use this on similar systems for creating keywords if they want...'
    '[CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Use a vanilla Kodi setup[/B][CR]You will require a complete fresh install of Kodi with absolutely nothing else installed and running the default skin. Decide what kind of pack you want to create, lets say we want to create a kids pack... Add all the kid related addons you want and make sure you also have the relevant repository installed too. In the unlikely event you\'ve found an addon that doesn\'t belong in a repository that\'s fine the system will create a full backup of that addon too (just means it won\'t auto update with future updates to the addon).'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Create the backup[/B][CR]Using this addon create your backup, currently only addon packs are supported but soon more packs will be added. When you create the keyword you\'ll be asked for a location to store the zip file that will be created and a name, this can be anywhwere you like and can be called whatever you want - you do not need to add the zip extension, that will automatically be added for you so in our example here we would call it "kids".'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Upload the zips[/B][CR]Upload the two zip file to a server that Kodi can access, it has to be a direct link and not somewhere that asks for captcha - archive.org and copy.com are two good examples. Do not use Dropbox unless you have a paid account, they have a fair useage policy and the chances are you\'ll find within 24 hours your download has been blocked and nobody can download it.[CR][CR][COLOR=lime]Top Tip: [/COLOR]The vast majority of problems occur when the wrong download URL has been entered in the online form, a good download URL normally ends in "=1" or "zip=true". Please double check when you copy the URL into a web browser it immediately starts downloading without the need to press any other button.'
    '[CR][CR][COLOR=dodgerblue][B]Step 4:[/COLOR] Create the keyword[/B][CR]Copy the download URL to your clipboard and then go to www.urlshortbot.com. In here you need to enter the URL in the "Long URL" field and then in the "Custom Keyword" field you need to enter "noobs" (without the quotation marks) followed by your keyword. We recommend always using a random test keyword for testing because once you have a keyword you can\'t change it, also when uploading make sure it\'s a link you can edit and still keep the same URL - that way it\'s easy to keep up to date and you can still use the same keyword. In our example of kids we would set the custom keyword as "noobskids". The noobs bit is ignored and is only for helping the addon know what to look for, the user would just type in "kids" for the kids pack to be installed.')
#---------------------------------------------------------------------------------------------------
#(Instructions) Adding other wizards
def Instructions_5():
    TXT.TXT('Adding Third Party Wizards', '[COLOR=gold]ONE WIZARD TO RULE THEM ALL![/COLOR][CR]Did you know the vast majority of wizards out there (every single one we\'ve tested) has just been a copy/paste of very old code created by the team here? We\'ve noticed a lot of the users installing builds via these third party wizards have run into many different problems so we thought we\'d take it upon ourselves to help out...'
    '[CR][CR][CR][COLOR=gold]WHAT BENEFITS DOES THIS HAVE?[/COLOR][CR]We\'ve added extra code that checks for common errors, unfortunately there are some people out there using inferior programs to create their backups and that is causing problems in their wizards. If such a problem exists when trying to use another wizard you can try adding the details to this addon and it automatically fixes any corrupt files it finds. Of course there are other benefits... installing code from an unknown source can give the author access to your system so make sure you always trust the author(s). Why take the risk of installing wizards created by anonymous usernames on social media sites when you can install from a trusted source like noobsandnerds and you\'ll also be safe in the knowledge that any new updates and improvements will be made here first - we do not copy/paste code, we are actively creating new exciting solutions!'
    '[CR][CR][CR][COLOR=gold]ADDING 3RD PARTY WIZARDS TO THIS ADDON[/COLOR][CR][CR][COLOR=dodgerblue][B]Step 1:[/COLOR] Enabling 3rd Party Wizards[/B][CR]In the addon settings under the Community Builds section you have the option to enable third party community builds, if you click on this you will be able to enter details of up to 5 different wizards.'
    '[CR][CR][COLOR=dodgerblue][B]Step 2:[/COLOR] Enter the URL[/B][CR]As virtually all wizards use exactly the same structure all you need to do is find out what URL they are looking up in the code, you can open the default.py file of the wizard in a text editor and search for "http" and you will more than likely find the URL straight away. Try entering it in a web address, it should show the details for all the builds in that wizard in a text based page. If the page is blank don\'t worry it may just be locked from web browsers and can only be opened in Kodi, try it out and see if it works.'
    '[CR][CR][COLOR=dodgerblue][B]Step 3:[/COLOR] Enter the name[/B][CR]Give the wizard a name, now when you go into the Community Builds section you\'ll have the official noobsandnerds builds as an option and also any new ones you\'ve added.')
#-----------------------------------------------------------------------------------------------------------------
#Thanks to metalkettle for his work on the original IP checker addon        
def IP_Check():
    try:
        BaseURL       = 'https://www.iplocation.net/find-ip-address'
        link          = Open_URL(BaseURL).replace('\n','').replace('\r','')
        segment       = re.compile('<table class="iptable">(.+?)<\/table>').finall(link)
        ipmatch       = re.compile('font-weight: bold;">(.+?)<\/span>').findall(segment[0])
        ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
        providermatch = re.compile('Host Name<\/th><td>(.+?)<\/td>').findall(segment[0])
        hostname      = details[0] if (len(details) > 0) else 'Unknown'
        locationmatch = re.compile('IP Location<\/th><td>(.+?)&nbsp;').findall(segment[0])
        location      = details[0] if (len(details) > 0) else 'Unknown'
        dialog.ok('www.iplocation.net',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Host: [/COLOR][/B] %s' % hostname, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
    except:
        dialog.ok('SERVICE UNAVAILABLE', 'It was not possible to contact the relevant website to check your details. Please check your internet connection and if that\'s ok try using an alternative site in the settings.')
#---------------------------------------------------------------------------------------------------
# Install a keyword
def Keyword_Search(url):
    if not os.path.exists(packages):
        os.makedirs(packages)
    xbmc.log("KEYWORD_SEARCH")
    counter = 0
    success = 0
    
    downloadurl = ''
    title       = 'Enter Keyword'
    keyword     = SEARCH(title)
    if keyword == 'testmode':
        ADDON.setSetting('debug','true')
    else:
        url         = 'http://urlshortbot.com/venztech'
        downloadurl = url+keyword
        lib         = os.path.join(packages, keyword+'.zip')

        try:
            wifimac = getMacAddress('wifi').replace('\n','')
        except:
            wifimac = 'Unknown'
        try:
            ethmac  = getMacAddress('eth0').replace('\n','')
        except:
            ethmac  = 'Unknown'
        try:
            cpu     = CPU_Check().replace('\n','')
        except:
            cpu     = 'Unknown'
        try:
            build   = Build_Info().replace('\n','')
        except:
            build   = 'Unknown'
        if not 'Unknown' in wifimac and not 'Unknown' in ethmac:
            urlparams = wifimac+'&'+cpu+'&'+build+'&'+ethmac.replace(' ','%20') 
            dp.create('Contacting Server','Attempt: 1', '', 'Please wait...')
            while counter <3 and success == 0:
                counter += 1
                dp.update(0,'Attempt: '+str(counter), '', 'Please wait...')
            if keyword.startswith('switchme'):
                keywordoem = keyword.replace('switchme','')
                try:
                    link = Open_URL('http://tlbb.me/boxer/addtooem.php?x='+encryptme('e',urlparams)+'&o='+encryptme('e',keywordoem))
                except:
                    link = 'fail'
            else:
                try:
                    link = Open_URL('http://tlbb.me/keyword.php?x='+encryptme('e',urlparams)+'k='+encryptme('e',keyword))
                except:
                    link = 'fail'
            if 'Success' in link:
                success = 1
                dp.close()
                dialog.ok('Venztech Code Success','Congratulations, your Venztech Code has successfully been installed.')
                xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/checknews.py')
        if success == 0:
            try:
                xbmc.log("Attempting download "+downloadurl+" to "+lib)
                dp.create("Web Installer","Downloading ",'', 'Please Wait')
                downloader.download(downloadurl,lib)
                xbmc.log("### Keyword "+keyword+" Successfully downloaded")
                dp.update(0,"", "Extracting Zip Please Wait")
            
                if zipfile.is_zipfile(lib):
                
                    try:
                        if 'venztech' in url:
                            extract.all(lib,'/storage',dp)
                        else:
                            extract.all(lib,HOME,dp)
                        xbmc.executebuiltin('UpdateLocalAddons')
                        xbmc.executebuiltin( 'UpdateAddonRepos' )
                        dialog.ok("Web Installer", "","Content now installed", "")
                        dp.close()
                
                    except:
                        xbmc.log("### Unable to install keyword (passed zip check): "+keyword)
            
                else:
                    try:
                        if os.path.getsize(lib) > 100000 and 'venztech' in url:
                            dp.create("Restoring Backup","Copying Files...",'', 'Please Wait')
                            os.rename(lib,restore_dir+'20150815123607.tar')
                            dp.update(0,"", "Kodi will now reboot")
                            xbmc.executebuiltin('reboot')
                        else: dialog.ok("Keyword error",'The keyword you typed could not be installed.','Please check the spelling and if you continue to receive','this message it probably means that keyword is no longer available.')
                    except:
                        dialog.ok("Error with zip",'The file you attempted to download is not in a valid zip format, please double check you typed in the correct word.')
                        xbmc.log("### UNABLE TO INSTALL BACKUP - IT IS NOT A ZIP")

                xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
                
            except:
                dialog.ok('Code Not Recognised','Sorry the code you entered has not been recognised, please check the spelling and try again.')

        if os.path.exists(lib):
            os.remove(lib)
#-----------------------------------------------------------------------------------------------------------------
#ANDROID ONLY WORKS WITH ROOT
def KLL():
#    dialog.ok('Kodi will now close','The system will now attempt to force close Kodi.','You may encounter a freeze, if that happens give it a minute','and if it doesn\'t close please restart your system.')
    if not os.path.exists(scriptfolder):
        os.makedirs(scriptfolder)
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if xbmc.getCondVisibility('system.platform.windows'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'win_xbmc.bat'), 'w+')
                writefile.write('@ECHO off\nTASKKILL /im XBMC.exe /f\ntskill XBMC.exe\nXBMC.exe')
                writefile.close()
                os.system(os.path.join(scriptfolder,'win_xbmc.bat'))
            except:
                xbmc.log("### Failed to run win_xbmc.bat")
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'win_kodi.bat'), 'w+')
                writefile.write('@ECHO off\nTASKKILL /im Kodi.exe /f\ntskill Kodi.exe\nKodi.exe')
                writefile.close()
                os.system(os.path.join(scriptfolder,'win_kodi.bat'))
            except:
                xbmc.log("### Failed to run win_kodi.bat")
    elif xbmc.getCondVisibility('system.platform.osx'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'osx_xbmc.sh'), 'w+')
                writefile.write('killall -9 XBMC\nXBMC')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod 755 '+os.path.join(scriptfolder,'osx_xbmc.sh'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'osx_xbmc.sh'))
            except:
                xbmc.log("### Failed to run osx_xbmc.sh")
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'osx_kodi.sh'), 'w+')
                writefile.write('killall -9 Kodi\nKodi')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod 755 '+os.path.join(scriptfolder,'osx_kodi.sh'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'osx_kodi.sh'))
            except:
                xbmc.log("### Failed to run osx_kodi.sh")
#    else:
    elif xbmc.getCondVisibility('system.platform.android'):
        if os.path.exists('/data/data/com.rechild.advancedtaskkiller'):
            dialog.ok('Attempting to force close','On the following screen please press the big button at the top which says "KILL selected apps". Kodi will restart, please be patient while your system updates the necessary files and your skin will automatically switch once fully updated.')
            try:
                xbmc.executebuiltin('StartAndroidActivity(com.rechild.advancedtaskkiller)')
            except:
                xbmc.log("### Failed to run Advanced Task Killer. Make sure you have it installed, you can download from https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk")
        else:
            dialog.ok('Advanced Task Killer Not Found',"The Advanced Task Killer app cannot be found on this system. Please make sure you actually installed it after downloading. We can't do everything for you - on Android you do have to physically click on the download to install an app.")
        try:
            os.system('adb shell am force-stop org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.kodi')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell am force-stop org.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.kodi')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc.xbmc')
        except:
            pass
        try:
            os.system('adb shell kill org.xbmc')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.kodi());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
        except:
            pass
        try:
            os.system('Process.killProcess(android.os.Process.org.xbmc());')
        except:
            pass
    elif xbmc.getCondVisibility('system.platform.linux'):
        if version < 14:
            try:
                writefile = open(os.path.join(scriptfolder,'linux_xbmc'), 'w+')
                writefile.write('killall XBMC\nkillall -9 xbmc.bin\nXBMC')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod a+x '+os.path.join(scriptfolder,'linux_xbmc'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'linux_xbmc'))
            except:
                xbmc.log("### Failed to run: linux_xbmc")
        else:
            try:
                writefile = open(os.path.join(scriptfolder,'linux_kodi'), 'w+')
                writefile.write('killall Kodi\nkillall -9 kodi.bin\nkodi')
                writefile.close()
            except:
                pass
            try:
                os.system('chmod a+x '+os.path.join(scriptfolder,'linux_kodi'))
            except:
                pass
            try:
                os.system(os.path.join(scriptfolder,'linux_kodi'))
            except:
                xbmc.log("### Failed to run: linux_kodi")
    else: #ATV and OSMC
        try:
            os.system('killall AppleTV')
        except:
            pass
        try:
            os.system('sudo initctl stop kodi')
        except:
            pass
        try:
            os.system('sudo initctl stop xbmc')
        except:
            pass
#---------------------------------------------------------------------------------------------------
#Open Kodi Settings
def Kodi_Settings():
    xbmc.executebuiltin('ReplaceWindow(settings)')
#---------------------------------------------------------------------------------------------------
#Create a FULL backup
def Local_Backup():
    Check_Download_Path()
    
    fullbackuppath  = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds',''))
    myfullbackup    = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup.zip'))
    myfullbackupGUI = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds','my_full_backup_GUI_Settings.zip'))
    
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    
    vq = Get_Keyboard( heading="Enter a name for this backup" )
    
    if ( not vq ):
        return False, 0
    
    title              = urllib.quote_plus(vq)
    backup_zip         = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    exclude_dirs_full  =  [AddonID]
    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
    message_header     = "Creating full backup of existing build"
    message_header2    = "Creating Community Build"
    message1           = "Archiving..."
    message2           = ""
    message3           = "Please Wait"
    
    Archive_Tree(HOME, myfullbackup, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    dialog.ok('Full Backup Complete','You can locate your backup at:[COLOR=dodgerblue]',myfullbackup+'[/COLOR]')
#---------------------------------------------------------------------------------------------------
# View the log from within Kodi
def Log_Viewer():
    xbmc_version  = xbmc.getInfoLabel("System.BuildVersion")
    version       = float(xbmc_version[:4])
    
    if version < 14:
        log = os.path.join(log_path, 'xbmc.log')
        TXT.TXT('XBMC Log', log)
    
    else:
        log = os.path.join(log_path, 'kodi.log')
        TXT.TXT('Kodi Log', log)
#---------------------------------------------------------------------------------------------------
# Dialog to warn users about local guisettings fix.
def Local_GUI_Dialog():
    dialog.ok("Restore local guisettings fix", "You should [COLOR=lime]ONLY[/COLOR] use this option if the guisettings fix is failing to download via the addon. Installing via this method means you do not receive notifications of updates")
    Restore_Local_GUI()
#---------------------------------------------------------------------------------------------------
#Search in description
def Manual_Search(mode):
    if not mode.endswith("premium") and not mode.endswith("public") and not mode.endswith("private"):
        vq = Get_Keyboard( heading="Search for content" )
        
        if ( not vq ):
            return False, 0
        
        title = urllib.quote_plus(vq)
        
        if mode == 'tutorials':
            Grab_Tutorials('name='+title)
        
        if mode == 'hardware':
            Grab_Hardware('name='+title)
        
        if mode == 'news':
            Grab_News('name='+title)
    
    if mode.endswith("premium") or mode.endswith("public") or mode.endswith("private"):
        o0oO('folder','Search By Name',mode+'&name=','search_builds','Manual_Search.png','','','')
        o0oO('folder','Search By Uploader',mode+'&author=','search_builds','Search_Genre.png','','','')
        o0oO('folder','Search By Audio Addons Installed',mode+'&audio=','search_builds','Search_Addons.png','','','')
        o0oO('folder','Search By Picture Addons Installed',mode+'&pics=','search_builds','Search_Addons.png','','','')
        o0oO('folder','Search By Program Addons Installed',mode+'&progs=','search_builds','Search_Addons.png','','','')
        o0oO('folder','Search By Video Addons Installed',mode+'&vids=','search_builds','Search_Addons.png','','','')
        o0oO('folder','Search By Skins Installed',mode+'&skins=','search_builds','Search_Addons.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def News_Menu(url):
    BaseURL      = 'http://noobsandnerds.com/TI/LatestNews/LatestNews.php?id=%s' % (url)
    link         = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch    = re.compile('name="(.+?)"').findall(link)
    authormatch  = re.compile('author="(.+?)"').findall(link)
    datematch    = re.compile('date="(.+?)"').findall(link)
    contentmatch = re.compile('content="(.+?)###END###"').findall(link)
   
    name        = namematch[0] if (len(namematch) > 0) else ''
    author      = authormatch[0] if (len(authormatch) > 0) else ''
    date        = datematch[0] if (len(datematch) > 0) else ''
    content     = contentmatch[0] if (len(contentmatch) > 0) else ''
    clean_text  = Clean_HTML(content)
    description = str('[COLOR=orange]Source: [/COLOR]'+author+'     [COLOR=orange]Date: [/COLOR]'+date+'[CR][CR][COLOR=lime]Details: [/COLOR][CR]'+clean_text)
    
    TXT.TXT(name,description)
#---------------------------------------------------------------------------------------------------
#News Menu
def News_Root_Menu(url):
    if reseller=='true':
        o0oO('','[COLOR=orange]Latest '+I1IiiI+' news[/COLOR]', I1IiiI, 'notify_msg', 'LatestNews.png','','','')
    o0oO('folder','[COLOR=darkcyan]Manual Search[/COLOR]', 'news', 'manual_search', 'Manual_Search.png','','','')
    o0oO('folder','Official Kodi.tv News', str(url)+'&author=Official%20Kodi', 'grab_news', 'XBMC.png','','','')
    o0oO('folder','OpenELEC News', str(url)+'&author=OpenELEC', 'grab_news', 'OpenELEC.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Simple shortcut to create a notification
def Notify(title,message,times,icon):
    icon = notifyart+icon
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
#---------------------------------------------------------------------------------------------------
#Open Kodi File Manager
def Open_Filemanager():
    xbmc.executebuiltin('ActivateWindow(filemanager,return)')
    return
#---------------------------------------------------------------------------------------------------
#Open Kodi File Manager
def Open_System_Info():
    xbmc.executebuiltin('ActivateWindow(systeminfo)')
#-----------------------------------------------------------------------------------------------------------------
## Function to open a URL
def Open_URL(url):
    if debug == 'true':
        xbmc.log(url)
#        url = url.replace('tlbb.me','test.tlbb.me')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    return link
#-----------------------------------------------------------------------------------------------------------------
## Function to open a URL, try 3 times then respond with blank
def Open_URL2(url):
    if debug == 'true':
        xbmc.log(url)
#        url = url.replace('tlbb.me','test.tlbb.me')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#    try:
    response = urllib2.urlopen(req, timeout = 10)
#    except:
#        try:
#            response = urllib2.urlopen(req, timeout = 10)
#        except:
#            try:
#                response = urllib2.urlopen(req, timeout = 10)
#            except:
#                response = ''
    if response != '':
        link     = response.read()
        response.close()
        return link.replace('\r','').replace('\n','').replace('\t','')
    else:
        return response

#---------------------------------------------------------------------------------------------------
# Function to install venz pack
def Open_Link(url):
    response = Open_URL2(url)
    if debug == 'true':
        xbmc.log("### "+response)
    if "record" in response:
        Grab_Updates('http://tlbb.me/comm.php?z=c&x=')
        xbmc.executebuiltin('Container.Refresh')
    else:
        dialog.ok('Problem Detected',"Sorry it wasn't possible to execute this command, please check your internet connection. If you're sure this is ok we may be experiencing some downtime on our servers, if that's the case we apologise and they will be back online asap.")

#---------------------------------------------------------------------------------------------------
# Function to create an OE tar backup
def OpenELEC_Backup():
    import tarfile

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    dp.create("Creating Backup","Adding files... ",'', 'Please Wait')
    tar = tarfile.open(os.path.join(backup_dir, Timestamp()+'.tar'), 'w')
    
    for directory in BACKUP_DIRS:
        dp.update(0,"Backing Up",'[COLOR blue]%s[/COLOR]'%directory, 'Please Wait')
        tar.add(directory)
    
    tar.close()
    dp.close()
#---------------------------------------------------------------------------------------------------
# Check if system is OE
def OpenELEC_Check():
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        log_path_new = os.path.join(log_path,'xbmc.log')
    else:
        log_path_new = os.path.join(log_path,'kodi.log')
        
    try:
        localfile = open(log_path_new, mode='r')
        content   = localfile.read()
        localfile.close()
    except:
        try:
            localfile = open(os.path.join(HOME,'temp','kodi.log'), mode='r')
            content   = localfile.read()
            localfile.close()
        except:
            try:
                localfile = open(os.path.join(HOME,'temp','xbmc.log'), mode='r')
                content   = localfile.read()
                localfile.close()
            except:
                pass                
            
    if 'OpenELEC' in content:
        return True
#---------------------------------------------------------------------------------------------------
#Open OE Settings
def OpenELEC_Settings():
    xbmc.executebuiltin('RunAddon(service.openelec.settings)')
#---------------------------------------------------------------------------------------------------
#Platform tutorial menu
def Platform_Menu(url):
    o0oO('folder','[COLOR=darkcyan]1. Install:[/COLOR]  Installation tutorials (e.g. flashing a new OS)', str(url)+'&thirdparty=InstallTools', 'grab_tutorials', 'Install.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Add-on Tools:[/COLOR]  Add-on maintenance and coding tutorials', str(url)+'&thirdparty=AddonTools', 'grab_tutorials', 'ADDONTOOLS.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Audio Tools:[/COLOR]  Audio related tutorials', str(url)+'&thirdparty=AudioTools', 'grab_tutorials', 'AUDIOTOOLS.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Gaming Tools:[/COLOR]  Integrate a gaming section into your setup', str(url)+'&thirdparty=GamingTools', 'grab_tutorials', 'gaming_portal.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Image Tools:[/COLOR]  Tutorials to assist with your pictures/photos', str(url)+'&thirdparty=ImageTools', 'grab_tutorials', 'IMAGETOOLS.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Library Tools:[/COLOR]  Music and Video Library Tutorials', str(url)+'&thirdparty=LibraryTools', 'grab_tutorials', 'LIBRARYTOOLS.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Skinning Tools:[/COLOR]  All your skinning advice', str(url)+'&thirdparty=SkinningTools', 'grab_tutorials', 'SKINNINGTOOLS.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Video Tools:[/COLOR]  All video related tools', str(url)+'&thirdparty=VideoTools', 'grab_tutorials', 'VIDEOTOOLS.png','','','')
#---------------------------------------------------------------------------------------------------
#Set popup xml based on platform
def pop(xmlfile):
# if popup is an advert from the web
    if 'http' in xmlfile:
        contents = 'none'
        filedate = xmlfile[-10:]
        filedate = filedate[:-4]
        latest = os.path.join(ADDON_DATA,AddonID,'latest')

        if os.path.exists(latest):
            readfile = open(latest, mode='r')
            contents = readfile.read()
            readfile.close()

        if contents == filedate:
            filedate = contents
                
        else:
            downloader.download(xmlfile,os.path.join(ADDONS,AddonID,'resources','skins','DefaultSkin','media','latest.jpg'))
            writefile = open(latest, mode='w+')
            writefile.write(filedate)
            writefile.close()
        xmlfile = 'latest.xml'
    popup = SPLASH(xmlfile,ADDON.getAddonInfo('path'),'DefaultSkin',close_time=34)
    popup.doModal()
    del popup
#-----------------------------------------------------------------------------------------------------------------    
#Recursive loop for downloading files from web
def Recursive_Loop(recursive_location,remote_path):
    if not os.path.exists(recursive_location):
        os.makedirs(recursive_location)
    
    link   = Open_URL(remote_path).replace('\n','').replace('\r','')
    match  = re.compile('href="(.+?)"', re.DOTALL).findall(link)
    
    for href in match:
        filepath=xbmc.translatePath(os.path.join(recursive_location,href)) #works
        
        if '/' not in href:
            
            try:
                dp.update(0,"Downloading [COLOR=darkcyan]"+href+'[/COLOR]','','Please wait...')
                downloader.download(remote_path+href, filepath, dp)
            
            except:
                xbmc.log("failed to install"+href)
        
        if '/' in href and '..' not in href and 'http' not in href:
            remote_path2 = remote_path+href
            Recursive_Loop(filepath,remote_path2)
        
        else:
            pass
#---------------------------------------------------------------------------------------------------
#Function to clear the addon_data
def Remove_Addon_Data():
    choice = xbmcgui.Dialog().yesno('Delete Addon_Data Folder?', 'This will free up space by deleting your addon_data folder. This contains all addon related settings including username and password info.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Delete_Userdata()
        dialog.ok("Addon_Data Removed", '', 'Your addon_data folder has now been removed.','')
#---------------------------------------------------------------------------------------------------
def Remove_Addons(url):
    data_path = str(url).replace(ADDONS,ADDON_DATA)
    
    if dialog.yesno("Remove", '', "Do you want to Remove"):
        
        for root, dirs, files in os.walk(url):
            
            for f in files:
                os.unlink(os.path.join(root, f))
            
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        os.rmdir(url)
        
        try:
            
            for root, dirs, files in os.walk(data_path):
                
                for f in files:
                    os.unlink(os.path.join(root, f))
                
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            
            os.rmdir(data_path)
        
        except:
            pass
        
        addonsdb=os.path.join(USERDATA,'Database','Addons16.db')
        
        try:
            os.remove(addonsdb)
        
        except:
            pass
        
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.sleep(1000)
        xbmc.executebuiltin( 'UpdateAddonRepos' )
        Remove_Packages()
        dialog.ok('Add-on removed','You may have to restart Kodi to repopulate','your add-on database. Until you restart you\'ll','find your add-on is still showing even though it\'s deleted')
        xbmc.executebuiltin('Container.Refresh')         
#---------------------------------------------------------------------------------------------------
#Function to restore a zip file 
def Remove_Build():
    Check_Download_Path()
    filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to DELETE', 'files', '.zip', False, False, USB)
    
    if filename != USB:
        clean_title = ntpath.basename(filename)
        choice = xbmcgui.Dialog().yesno('Delete Backup File', 'This will completely remove '+clean_title, 'Are you sure you want to delete?', '', nolabel='No, Cancel',yeslabel='Yes, Delete')
        
        if choice == 1:
            os.remove(filename)
#---------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Crash_Logs():
    choice = xbmcgui.Dialog().yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are log files generated when Kodi crashes and are only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Delete_Logs()
        dialog.ok("Crash Logs Removed", '', 'Your crash log files have now been removed.','')
#---------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('Delete Packages Folder', 'Do you want to clean the packages folder? This will free up space by deleting the old zip install files of your addons. Keeping these files can also sometimes cause problems when reinstalling addons', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Delete_Packages()
        dialog.ok("Packages Removed", '', 'Your zip install files have now been removed.','')
#---------------------------------------------------------------------------------------------------
#Function to clear the packages folder
def Remove_Textures_Dialog():
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your textures13.db file and remove your Thumbnails folder. These will automatically be repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Remove_Textures()
        Destroy_Path(THUMBNAILS)
        
        choice = xbmcgui.Dialog().yesno('Quit Kodi Now?', 'Cache has been successfully deleted.', 'You must now restart Kodi, would you like to quit now?','', nolabel='I\'ll restart later',yeslabel='Yes, quit')
        
        if choice == 1:
            try:
                xbmc.executebuiltin("RestartApp")
            
            except:
                KLL()
#---------------------------------------------------------------------------------------------------
#Function to remove textures13.db and thumbnails folder
def Remove_Textures():
    textures   =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
    try:
        dbcon = database.connect(textures)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS path")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS sizes")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS texture")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
        dbcon.commit()
    except:
        pass
#---------------------------------------------------------------------------------------------------
#check what directories to add to root CB menu
def Reseller_Check(url):
    BaseURL          = 'http://noobsandnerds.com/TI/Community_Builds/reseller_2?reseller=%s&token=%s&openelec=%s' % (I1IiiI, IIi1IiiiI1Ii, url)
    link             = Open_URL(BaseURL).replace('\n','').replace('\r','')
    pathmatch        = re.compile('path="(.+?)"').findall(link)
    resellerdirmatch = re.compile('reseller="(.+?)"').findall(link)
    premiumdirmatch  = re.compile('premium="(.+?)"').findall(link)
    openelecmatch    = re.compile('openelec="(.+?)"').findall(link)
    resellerdir      = resellerdirmatch[0] if (len(resellerdirmatch) > 0) else 'None'
    premiumdir       = premiumdirmatch[0] if (len(premiumdirmatch) > 0) else 'None'
    openelecdir      = openelecmatch[0] if (len(openelecmatch) > 0) else 'None'
    exec openelecdir
    exec resellerdir
    exec premiumdir
#---------------------------------------------------------------------------------------------------
#Function to restore a backup xml file (guisettings, sources, RSS)
def Restore_Backup_XML(name,url,description):
    if 'Backup' in name:
        Check_Download_Path()
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        f         = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
    
    else:
        if 'guisettings.xml' in description:
            a     = open(os.path.join(USB,description.split('Your ')[1])).read()
            r     ='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            match = re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        
        else:    
            TO_WRITE = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            f        = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  

    dialog.ok("Restore Complete", "", 'All Done !','')
#---------------------------------------------------------------------------------------------------
#Function to restore a community build
def Restore_Community(name,url,video,description,skins,guisettingslink,artpack):
    profilechoice = 1
    removeprofile = 0
    CP_Profiles   = os.path.join(HOME,'CP_Profiles')
    Profile_List  = os.path.join(CP_Profiles, 'list.txt')
    mainaddons    = []
    filename      = description.replace(' ','_').replace("'","").replace(":","-")
    
    if not os.path.exists(CP_Profiles):
        os.makedirs(CP_Profiles)

    clean_folder_name = os.path.join(CP_Profiles, filename)
    if not os.path.exists(clean_folder_name):
        os.makedirs(clean_folder_name)
    else:
        removeprofile = dialog.yesno('Profile Already Exists','This build is already installed on your system, would you like to remove the old one and reinstall?')
        if removeprofile == 1:
            try:
                shutil.rmtree(clean_folder_name)
                os.makedirs(clean_folder_name)
            except:
                pass
        else:
            profilechoice = 2

    if profilechoice == 1:
        lib=os.path.join(CBPATH, filename+'_gui.zip')
        if debug == 'true':
            xbmc.log("### Download path = %s" % lib)
# Download guisettings from the build
        try:
            downloader.download(guisettingslink, lib)
            if debug == 'true':
                xbmc.log("### successfully downloaded guisettings.xml")
        except:
            dialog.ok('Problem Detected','Sorry there was a problem downloading the guisettings file. Please check your storage location, if you\'re certain that\'s ok please notify the build author on the relevant support thread.')
            if debug == 'true':
                xbmc.log("### FAILED to download "+guisettingslink)

# Check that gui file is a real zip and the uploader hasn't put a bad link in the db
        if zipfile.is_zipfile(lib):
            guisize = str(os.path.getsize(lib))   
        else:
            guisize = '0'
            
        dp.create("Community Builds","Downloading "+description,'', 'Please Wait')
        lib=os.path.join(CBPATH, filename+'.zip')
        
        if not os.path.exists(CBPATH):
            try:
                os.makedirs(CBPATH)
            except:
                dialog.ok('Please Check Storage Path','Unable to create a folder in the storage location you\'ve provided. Please check your storage location in the add-on settings and try again')
                return

# Extract to a temporary folder so we can add new id.xml and rip out stuff not needed
        tempCPfolder = os.path.join(CP_PROFILE,'extracted')
        downloader.download(url, lib, dp)
        dp.create("Community Builds","Extracting "+description,'', 'Please Wait')
        extract.all(lib, tempCPfolder,dp)
        if os.path.exists(os.path.join(tempCPfolder,'userdata','.cbcfg')):
            os.makedirs(os.path.join(ADDON_DATA,AddonID,'updating'))
        if debug == 'true':
            xbmc.log("### Downloaded build to: "+lib)
            xbmc.log("### Extracted build to: "+tempCPfolder)
# Pull the details about the currently downloading build and add to new idfile in profile folder
        localfile = open(tempfile, mode='r')
        content   = localfile.read()
        localfile.close()

        temp         = re.compile('id="(.+?)"').findall(content)
        tempname     = re.compile('name="(.+?)"').findall(content)
        tempversion  = re.compile('version="(.+?)"').findall(content)

        tempcheck    = temp[0] if (len(temp) > 0) else ''
        namecheck    = tempname[0] if (len(tempname) > 0) else ''
        versioncheck = tempversion[0] if (len(tempversion) > 0) else ''

        xbmc.log("### Build name details to store in ti_id: "+namecheck)

        newaddondata = os.path.join(tempCPfolder,'userdata','addon_data','ti_id')
        newidfile    = os.path.join(newaddondata,'id.xml')
        if not os.path.exists(newaddondata):
            os.makedirs(newaddondata)

        writefile = open(newidfile, mode='w+')
        writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
        writefile.close()
# Update the startup.xml version number so it can check for update on next run of add-on
        startuppath = os.path.join(newaddondata,'startup.xml')
        writefile = open(startuppath, mode='w+')
        writefile.write('date="01011001"\nversion="'+versioncheck+'"')
        writefile.close()

        tempidfile = open(newidfile,'r')
        tempcontent = tempidfile.read()
        tempidfile.close()
        xbmc.log("### ti_id/id.xml contents: "+tempcontent)
        
# Give option to merge guisettings
        guichoice = dialog.yesno("Keep Kodi Settings?", 'Do you want to keep your existing KODI settings (weather, screen calibration, PVR etc.) or wipe and install the ones supplied in this build?', yeslabel='Replace my settings', nolabel='Keep my settings')
        if guichoice == 0:
            GUI_Install(os.path.join(CP_PROFILE,'extracted','userdata','guisettings.xml'))
# List pre-installed Kodi addons, we don't need to copy these
        for item in os.listdir(KODI_ADDONS):
            mainaddons.append(item)

# Create an addonlist for new profile
        newlist = open(os.path.join(clean_folder_name,'addonlist'), mode='w+')
        for item in os.listdir(ADDONS):
            if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'packages':
                newlist.write(item+'|')
        newlist.close()
        if debug == 'true':
            xbmc.log("### Created addonlist to: "+os.path.join(clean_folder_name,'addonlist'))
        exclude_dirs_full =  ['addons','cache','CP_Profiles','system','temp','Thumbnails']
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore','addons*.db','textures13.db','.cbcfg']
        message_header = "Creating Profile Data File"
        message1 = "Archiving..."
        message2 = ""
        message3 = "Please Wait"
        Archive_Tree(tempCPfolder, os.path.join(clean_folder_name,'build.zip'), message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
        if debug == 'true':
            xbmc.log("### Created: "+os.path.join(clean_folder_name,'build.zip'))
# Remove the downloaded build if not set to keep in add-on settings
        if localcopy == 'false':
            os.remove(lib)
            if debug == 'true':
                xbmc.log("### removed: "+lib)
        Check_Build_Addons(filename)
        incremental = 'http://noobsandnerds.com/TI/Community_Builds/downloadcount.php?id=%s' % (tempcheck)
        if not 'update' in video:
            try:
                Open_URL(incremental)
            except:
                pass
        dialog.ok('Successfully Updated','Congratulations the following build:[COLOR=dodgerblue]',description,'[/COLOR]has been successfully updated!')
        CB_Install_Results()
        Switch_Profile(clean_folder_name)
#---------------------------------------------------------------------------------------------------
#Function to restore a local backup
def Restore_Local_Community(url):
    exitfunction = 0
    choice4      = 0
    xbmc.log("### Local Build Restore Location: "+url)
#
    Check_Download_Path()

    if url == 'local':
        filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.zip', False, False, USB)
        if filename == '':
            exitfunction = 1

    if exitfunction == 1:
        xbmc.log("### No file selected, quitting restore process ###")
        return
        
    if url != 'local':
        dp.create("Community Builds","Downloading build.",'', 'Please Wait')
        filename=os.path.join(CBPATH, Timestamp()+'.zip')
    
        if not os.path.exists(CBPATH):
            os.makedirs(CBPATH)
    
        downloader.download(url, filename, dp)

    if os.path.exists(GUINEW):
        if os.path.exists(GUI):
            os.remove(GUINEW)
        else:
            os.rename(GUINEW,GUI)
            
    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)
        
#Function for debugging, creates a file that was created in previous call and subsequently deleted when run
    if not os.path.exists(tempfile):
        localfile = open(tempfile, mode='w+')
        
    if os.path.exists(guitemp):
        os.removedirs(guitemp)
        
#Rename guisettings.xml to guinew.xml so we can edit without XBMC interfering.
    try:
        os.rename(GUI,GUINEW)

    except:
        dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit XBMC and try again','')
        return

    choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before installing any builds. Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
    if choice == 0:
        mybackuppath = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds'))

        if not os.path.exists(mybackuppath):
            os.makedirs(mybackuppath)

        vq = Get_Keyboard( heading="Enter a name for this backup" )
        if ( not vq ):
            return False, 0
            
        title              = urllib.quote_plus(vq)
        backup_zip         = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
        exclude_dirs_full  =  [AddonID]
        exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
        message_header     = "Creating full backup of existing build"
        message1           = "Archiving..."
        message2           = ""
        message3           = "Please Wait"
        
        Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice3 = xbmcgui.Dialog().yesno(name, 'Would you like to keep your existing database files or overwrite? Overwriting will wipe any existing music or video library you may have scanned in.', nolabel='Overwrite',yeslabel='Keep Existing')
    if choice3 == 1:
        if os.path.exists(tempdbpath):
            shutil.rmtree(tempdbpath)

        try:
            shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library

        except:
            choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases. Continuing may wipe your existing library. Do you wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
            if choice4 == 1: pass
            if choice4 == 0: exitfunction=1;return

        backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
        Archive_File(tempdbpath,backup_zip)
    
    if exitfunction == 1:
        xbmc.log("### Chose to exit restore function ###")
        return
    
    else:
        time.sleep(1)
        readfile         = open(CBADDONPATH, mode='r')
        default_contents = readfile.read()
        readfile.close()

# check to see if the dickheads have used some piece of shit backup program that includes logs, if they have re-zip it up PROPERLY!!!       
        xbmc.log("### Checking zip file structure ###")
        z = zipfile.ZipFile(filename)
        if 'xbmc.log' in z.namelist() or 'kodi.log' in z.namelist() or '.git' in z.namelist() or '.svn' in z.namelist():
            xbmc.log("### Whoever created this build has used completely the wrong backup method, lets try and fix it! ###")
            dialog.ok('Fixing Bad Zip','Whoever created this build has used the wrong backup method, please wait while we fix it - this could take some time! Click OK to proceed')
            zin       = zipfile.ZipFile (filename, 'r')
            filename2 = os.path.join(CBPATH, 'fixed.zip')
            zout      = zipfile.ZipFile (filename2, 'w')

            dp.create("Fixing Build","Checking ",'', 'Please Wait')
            
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                clean_file = str(item.filename)

                if (item.filename[-4:] != '.log') and not '.git' in clean_file and not '.svn' in clean_file:
                    zout.writestr(item, buffer)
                    dp.update(0,"Fixing...",'[COLOR darkcyan]%s[/COLOR]'%item.filename, 'Please Wait')
            
            dp.close()
            zout.close()
            zin.close()
            filename = filename2
            
        dp.create("Restoring Backup Build","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        
        try:
            extract.all(filename,HOME,dp)
        except:
            dialog.ok('ERROR IN BUILD ZIP','Please contact the build author, there are errors in this zip file that has caused the install process to fail. Most likely cause is it contains files with special characters in the name.')
            return
        
        time.sleep(1)

        if choice3 == 1:
            extract.all(backup_zip,DATABASE,dp) #This folder first needs zipping up
            
            if choice4 !=1:
                shutil.rmtree(tempdbpath)
        
        cbdefaultpy = open(CBADDONPATH, mode='w+')
        cbdefaultpy.write(default_contents)
        cbdefaultpy.close()
        try:
            os.rename(GUI,GUIFIX)

        except:
            xbmc.log("NO GUISETTINGS DOWNLOADED")

        time.sleep(1)
        localfile = open(GUINEW, mode='r') #Read the original skinsettings tags and store in memory ready to replace in guinew.xml
        content = localfile.read()
        localfile.close()
        skinsettingsorig = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content)
        skinorig  = skinsettingsorig[0] if (len(skinsettingsorig) > 0) else ''
        skindefault = re.compile('<skin default[\s\S]*?<\/skin>').findall(content)
        skindefaultorig  = skindefault[0] if (len(skindefault) > 0) else ''
        lookandfeelorig = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content)
        lookandfeel  = lookandfeelorig[0] if (len(lookandfeelorig) > 0) else ''

        try:
            localfile2 = open(GUIFIX, mode='r')
            content2 = localfile2.read()
            localfile2.close()
            skinsettingscontent = re.compile('<skinsettings>[\s\S]*?<\/skinsettings>').findall(content2)
            skinsettingstext  = skinsettingscontent[0] if (len(skinsettingscontent) > 0) else ''
            skindefaultcontent = re.compile('<skin default[\s\S]*?<\/skin>').findall(content2)
            skindefaulttext  = skindefaultcontent[0] if (len(skindefaultcontent) > 0) else ''
            lookandfeelcontent = re.compile('<lookandfeel>[\s\S]*?<\/lookandfeel>').findall(content2)
            lookandfeeltext  = lookandfeelcontent[0] if (len(lookandfeelcontent) > 0) else ''
            replacefile = content.replace(skinorig,skinsettingstext).replace(lookandfeel,lookandfeeltext).replace(skindefaultorig,skindefaulttext)
            writefile = open(GUINEW, mode='w+')
            writefile.write(str(replacefile))
            writefile.close()

        except:
            xbmc.log("NO GUISETTINGS DOWNLOADED")

        if os.path.exists(GUI):
            os.remove(GUI)
        
        os.rename(GUINEW,GUI)
        try:
            os.remove(GUIFIX)
        
        except:
            pass
        
        os.makedirs(guitemp)
        time.sleep(1)
        KLL()
        # xbmc.executebuiltin('UnloadSkin()') 
        # time.sleep(1)
        # xbmc.executebuiltin('ReloadSkin()')
        # time.sleep(1)
        # xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
        
        # while xbmc.getCondVisibility("Window.IsActive(appearancesettings)"):
            # xbmc.sleep(500)
        
        # try:
            # xbmc.executebuiltin("LoadProfile(Master user)")

        # except:
            # pass
        
        # dialog.ok('Main Build Now Installed','Step 1 complete. Now please change the skin to the one this build was designed for. Once done come back to this addon and restore the guisettings_fix.zip')
        # xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
#---------------------------------------------------------------------------------------------------
#Function to restore a local copy of guisettings_fix
def Restore_Local_GUI():
    Check_Download_Path()
    guifilename = xbmcgui.Dialog().browse(1, 'Select the guisettings zip file you want to restore', 'files', '.zip', False, False, USB)

    if guifilename == '':
        return

    else:
        local=1
        GUI_Settings_Fix(guifilename,local)  
#---------------------------------------------------------------------------------------------------
#Function to restore an OE based community build
def Restore_OpenELEC(name,url,video):
    choice = xbmcgui.Dialog().yesno('Full Wipe And New Install', 'This is a great option for first time install or if you\'re encountering any issues with your device. This will wipe all your Kodi settings, do you wish to continue?', nolabel='Cancel',yeslabel='Accept')
    if choice == 0:
        return

    elif choice == 1:

        lib  = '/storage/openelec_temp/'
        dest = '/storage/.restore/'
        path = os.path.join(dest, Timestamp()+'.tar')
        if not os.path.exists(dest):
            try:
                os.makedirs(dest)
            except:
                pass
        try:
            downloader.download(url, path)
            success = True
        except:
            success = False
        time.sleep(2)

        if success==True:
        
            try:
                localfile = open(tempfile, mode='r')
                content   = localfile.read()
                localfile.close()
            
                temp         = re.compile('id="(.+?)"').findall(content)
                tempcheck    = temp[0] if (len(temp) > 0) else ''
        
            except:
                pass
            if tempcheck != '':
                incremental = 'http://noobsandnerds.com/TI/Community_Builds/downloadcount.php?id=%s' % (tempcheck)
            try:
                Open_URL(incremental)
            except:
                pass

# Create temp folder for checking if new build after restart              
            if not os.path.exists(lib):
                try:
                    os.makedirs(lib)
                except:
                    pass

            dialog.ok("Download Complete - Press OK To Reboot",'Once you press OK your device will attempt to reboot, if it hasn\'t rebooted within 30 seconds please pull the power to manually shutdown. When booting you may see lines of text, don\'t worry this is normal update behaviour!')
            xbmc.executebuiltin('Reboot')
#---------------------------------------------------------------------------------------------------
#Function to restore an OE based community build
def Restore_OpenELEC_Local():
    exitfunction = 0
    choice = xbmcgui.Dialog().yesno('Full Wipe And New Install', 'This is a great option if you\'re encountering any issues with your device. This will wipe all your Kodi settings and restore with whatever is in the backup, do you wish to continue?', nolabel='Cancel',yeslabel='Accept')
    if choice == 0:
        return

    elif choice == 1:
        filename = xbmcgui.Dialog().browse(1, 'Select the backup file you want to restore', 'files', '.tar', False, False, backup_dir)
        if filename == '':
            exitfunction = 1

        if exitfunction == 1:
            xbmc.log("### No file selected, quitting restore process ###")
            return
        path = os.path.join(restore_dir, Timestamp()+'.tar')
        if not os.path.exists(restore_dir):
            try:
                os.makedirs(restore_dir)
            except:
                pass
        dp.create('Copying File To Restore Folder','','Please wait...')
        shutil.copyfile(filename,path)
        xbmc.executebuiltin('Reboot')
#---------------------------------------------------------------------------------------------------
#Create restore menu
def Restore_Option():
    Check_Local_Install()
    if OpenELEC_Check():
        o0oO('','[COLOR=dodgerblue]Restore a locally stored OpenELEC Backup[/COLOR]','','restore_local_OE','Restore.png','','','Restore A Full OE System Backup')

    o0oO('','[COLOR=dodgerblue]Restore A Locally stored build[/COLOR]','local','restore_local_CB','Restore.png','','','Restore A Full System Backup')
    o0oO('','[COLOR=dodgerblue]Restore Local guisettings file[/COLOR]','url','LocalGUIDialog','Restore.png','','','Back Up Your Full System')
    
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        o0oO('','Restore Your Addons','addons','restore_zip','Restore.png','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        o0oO('','Restore Your Addon UserData','addon_data','restore_zip','Restore.png','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        o0oO('','Restore Guisettings.xml',GUI,'resore_backup','Restore.png','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        o0oO('','Restore Favourites.xml',FAVS,'resore_backup','Restore.png','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        o0oO('','Restore Source.xml',SOURCE,'resore_backup','Restore.png','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        o0oO('','Restore Advancedsettings.xml',ADVANCED,'resore_backup','Restore.png','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        o0oO('','Restore Advancedsettings.xml',KEYMAPS,'resore_backup','Restore.png','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        o0oO('','Restore RssFeeds.xml',RSS,'resore_backup','Restore.png','','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
#Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
def Restore_Zip_File(url):
    Check_Download_Path()
    if 'addons' in url:
        ZIPFILE    = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR        = ADDONS

    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

    if 'Backup' in name:
        Delete_Packages() 
        dp.create("Creating Backup","Backing Up",'', 'Please Wait')
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR darkcyan]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not AddonID in dirs:
                       import time
                       FORCE= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > FORCE:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        dialog.ok("Backup Complete", "You Are Now Backed Up", '','')   

    else:
        dp.create("Extracting Zip","Checking ",'', 'Please Wait')
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(ZIPFILE,DIR,dp)
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        

        if 'Backup' in name:
            dialog.ok("Install Complete", 'Kodi will now close. Just re-open Kodi and wait for all the updates to complete.')
            KLL()

        else:
            dialog.ok("SUCCESS!", "You Are Now Restored", '','')        
#---------------------------------------------------------------------------------------------------
# Basic function to run an add-on
def Run_Addon(url):
    xbmc.executebuiltin('RunAddon('+url+')')
#---------------------------------------------------------------------------------------------------
# Search text box (used in keyword search)
def SEARCH(title):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, title)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered =  keyboard.getText() .replace(' ','%20')
            if search_entered == None:
                return False          
        return search_entered    
#-----------------------------------------------------------------------------------------------------------------
#Search in description
def Search_Addons(url):
    vq = Get_Keyboard( heading="Search for add-ons" )
# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    url += title
    Grab_Addons(url)
#-----------------------------------------------------------------------------------------------------------------
#Search in description
def Search_Builds(url):
    vq = Get_Keyboard( heading="Search for content" )

# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    url += title
    Grab_Builds(url)
#-----------------------------------------------------------------------------------------------------------------
# Main search menu for Venz content
def Search_Content_Main(type):
    if 'from_the' in type and '_menu' in type:
        Install_Venz_Menu(type+'||remove_main||'+type.replace('from_the_','').replace('_menu',''))
    elif type == 'main_menu':
        Install_Venz_Menu(type)
    elif type == 'live_tv' and not os.path.exists(tvguide) and tvgskip == 0:
        xbmc.log("### PATH: %s" % tvguide)
        o0oO('folder','Add Channels - [COLOR=dodgerblue]Manual Search[/COLOR]','add_main||'+type,'search_content','Manual_Search.png','','','')
        o0oO('folder','Add Channels - [COLOR=dodgerblue]Browse All Channels[/COLOR]','to_the_live_tv_menu||add_main||'+type,'install_venz_menu','','','','')
    elif not 'from_the' in type and type != 'main_menu' and not "submenu" in type:
        o0oO('folder','Add To '+type.replace('_',' ')+' - [COLOR=dodgerblue]Manual Search[/COLOR]','add_main||'+type,'search_content','Manual_Search.png','','','')
        o0oO('folder','Add To '+type.replace('_',' ')+' - [COLOR=dodgerblue]Browse All[/COLOR]','to_the_'+type+'_menu||add_main||'+type,'install_venz_menu','','','','')
    elif "submenu" in type:
        o0oO('folder','Add To '+type.replace('_submenu','').replace('_',' ').title()+' Sub-menu','to_the_'+type+'||add_sub||'+type.replace('_submenu',''),'install_venz_menu','','','','')
        o0oO('folder','Remove From '+type.replace('_submenu','').replace('_',' ').title()+' Sub-menu','from_the_'+type+'||remove_sub||'+type.replace('_submenu',''),'install_venz_menu','','','','')   
#-----------------------------------------------------------------------------------------------------------------
# Search for Venz content
def Search_Content(menutype):
    vq = Get_Keyboard(heading='Type The Channel Name')
# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    Install_Venz_Menu(title+'||'+menutype)
#---------------------------------------------------------------------------------------------------
def SetNone():
    wifimac = getMacAddress('wifi').replace('\n','')
    ethmac  = getMacAddress('eho0').replace('\n','')
    cpu     = CPU_Check().replace('\n','')
    build   = Build_Info().replace('\n','')
    urlparams = wifimac+'&'+cpu+'&'+build+'&'+ethmac.replace(' ','%20')
    link = Open_URL(encryptme('d','6773736f392e2e736b61612d6c642e7264736d6e6d642d6f676f3e773c011510030A')+encryptme('e',urlparams))
#---------------------------------------------------------------------------------------------------
#Function to pull commands and update
def RMT():
    check3='RMT'
    Remove_Textures()
    Wipe_Cache()
#---------------------------------------------------------------------------------------------------
#Function to pull commands and update
def SF(command,SF_folder,SF_link):
    check4='SF'
# Check if folder exists, if not create folder and favourites.xml file
    folder = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.super.favourites','Super Favourites',SF_folder))
    SF_favs   = os.path.join(folder,'favourites.xml')
    
    if command=='add':

        if not os.path.exists(folder):
            os.makedirs(folder)
            localfile = open(SF_favs, mode='w+')
            localfile.write('<favourites>\n</favourites>')
            localfile.close()
        
# Grab content between favourites tags, we'll replace this later
        localfile2 = open(SF_favs, mode='r')
        content2 = localfile2.read()
        localfile2.close()

        favcontent    = re.compile('<favourite name="[\s\S]*?\/favourites>').findall(content2)
        faves_content = favcontent[0] if (len(favcontent) > 0) else '\n</favourites>'
        
# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
        localfile = open(progresstemp, mode='r')
        newcontent = localfile.read()
        localfile.close()
        
#Write new favourites file
        if not newcontent in content2:
            localfile = open(SF_favs, mode='w+')
            if faves_content == '\n</favourites>':
                newfile = localfile.write('<favourites>\n\t'+newcontent+faves_content)
            else:
                newfile = localfile.write('<favourites>\n\t'+newcontent+'\n\t'+faves_content)
            localfile.close()
        
    if command=='delete':

# Grab content between favourites tags, we'll replace this later
        try:
            localfile2 = open(SF_favs, mode='r')
            content2 = localfile2.read()
            localfile2.close()

# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
            localfile = open(progresstemp, mode='r')
            newcontent = localfile.read()
            localfile.close()
        
#Write new favourites file
            localfile = open(SF_favs, mode='w+')
            newfile = localfile.write(content2.replace('\n\t'+newcontent,''))
            localfile.close()
        except:
            pass

# Attempt to delete the SF folder
    if command=='delfolder':

        try:
            shutil.rmtree(folder)
        except:
            pass
#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def Show_Info(url):
    BaseURL      = 'http://noobsandnerds.com/TI/Community_Builds/community_builds.php?id=%s' % (url)
    link         = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch    = re.compile('name="(.+?)"').findall(link)
    authormatch  = re.compile('author="(.+?)"').findall(link)
    versionmatch = re.compile('version="(.+?)"').findall(link)
    name         = namematch[0] if (len(namematch) > 0) else ''
    author       = authormatch[0] if (len(authormatch) > 0) else ''
    version      = versionmatch[0] if (len(versionmatch) > 0) else ''
    dialog.ok(name,'Author: [COLOR=dodgerblue]'+author+ '[/COLOR]      Latest Version: [COLOR=dodgerblue]'+version+'[/COLOR]','','Click OK to view the build page.')
    try:
        Community_Menu(url+'&visibility=homepage',url)
    except:
        return
        xbmc.log("### Could not find build No. "+url)
        dialog.ok('Build Not Found','Sorry we couldn\'t find the build, it may be it\'s marked as private. Please try manually searching via the Community Builds section')
#---------------------------------------------------------------------------------------------------
# Check local file version name and number against db
def Show_Info2(url):
    dialog.ok("This build is not complete",'The guisettings.xml file was not copied over during the last install process. Click OK to go to the build page and complete Install Step 2 (guisettings fix).')

    try:
        Community_Menu(url+'&visibility=homepage',url)

    except:
        return
        xbmc.log("### Could not find build No. "+url)
        dialog.ok('Build Not Found','Sorry we couldn\'t find the build, it may be it\'s marked as private. Please try manually searching via the Community Builds section')
#---------------------------------------------------------------------------------------------------
# Social TV Menu
def Social_Menu():
    o0oO('','[COLOR=dodgerblue]Check For Social Updates[/COLOR]','', 'grab_updates', '','','','')
    o0oO('','[COLOR=grey]Friend Requests (Coming Soon)[/COLOR]', '', '', '','','','')
    o0oO('','[COLOR=grey]My Content (Coming Soon)[/COLOR]', '', '', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# menu to set the sort type when searching
def Sort_By(url,type):
    if type == 'communitybuilds':
        redirect = 'grab_builds'
        if url.endswith("visibility=premium"):
             o0oO('folder','[COLOR=darkcyan]Manual Search[/COLOR]','&reseller='+urllib.quote(I1IiiI)+'&token='+IIi1IiiiI1Ii+'&visibility=premium','manual_search','Manual_Search.png','','','')
        if url.endswith("visibility=reseller_private"):
             o0oO('folder','[COLOR=darkcyan]Manual Search[/COLOR]','&reseller='+urllib.quote(I1IiiI)+'&token='+IIi1IiiiI1Ii+'&visibility=reseller_private','manual_search','Manual_Search.png','','','')
        if url.endswith("visibility=public"):
             o0oO('folder','[COLOR=darkcyan]Manual Search[/COLOR]','&visibility=public','manual_search','Manual_Search.png','','','')
        if url.endswith("visibility=private"):
             o0oO('folder','[COLOR=darkcyan]Manual Search[/COLOR]','&visibility=private','manual_search','Manual_Search.png','','','')
    if type == 'tutorials':
        redirect = 'grab_tutorials'
    if type == 'hardware':
        redirect = 'grab_hardware'
    if type == 'addons':
        redirect = 'grab_addons'
        o0oO('folder','[COLOR=dodgerblue]Sort by Most Popular[/COLOR]',str(url)+'&sortx=downloads&orderx=DESC',redirect,'Popular.png','','','')
    if type == 'hardware':
        o0oO('folder','[COLOR=lime]Filter Results[/COLOR]',url,'hardware_filter_menu','Filter.png','','','')  
    if type != 'addons':
        o0oO('folder','[COLOR=dodgerblue]Sort by Most Popular[/COLOR]',str(url)+'&sortx=downloadcount&orderx=DESC',redirect,'Popular.png','','','')
    if type == 'tutorials' or type == 'hardware':
        o0oO('folder','[COLOR=dodgerblue]Sort by Newest[/COLOR]',str(url)+'&sortx=Added&orderx=DESC',redirect,'Latest.png','','','')
    else:
        o0oO('folder','[COLOR=dodgerblue]Sort by Newest[/COLOR]',str(url)+'&sortx=created&orderx=DESC',redirect,'Latest.png','','','')
        o0oO('folder','[COLOR=dodgerblue]Sort by Recently Updated[/COLOR]',str(url)+'&sortx=updated&orderx=DESC',redirect,'Recently_Updated.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Sort by A-Z[/COLOR]',str(url)+'&sortx=name&orderx=ASC',redirect,'AtoZ.png','','','')
    o0oO('folder','[COLOR=dodgerblue]Sort by Z-A[/COLOR]',str(url)+'&sortx=name&orderx=DESC',redirect,'ZtoA.png','','','')
    if type == 'public_CB':
        o0oO('folder','[COLOR=dodgerblue]Sort by Genre[/COLOR]',url,'genres','Search_Genre.png','','','')
        o0oO('folder','[COLOR=dodgerblue]Sort by Country/Language[/COLOR]',url,'countries','Search_Country.png','','','')
#---------------------------------------------------------------------------------------------------
#Instructions for the speed test
def Speed_Instructions():
    TXT.TXT('Speed Test Instructions', '[COLOR=blue][B]What file should I use: [/B][/COLOR][CR]This function will download a file and will work out your speed based on how long it took to download. You will then be notified of '
    'what quality streams you can expect to stream without buffering. You can choose to download a 10MB, 16MB, 32MB, 64MB or 128MB file to use with the test. Using the larger files will give you a better '
    'indication of how reliable your speeds are but obviously if you have a limited amount of bandwidth allowance you may want to opt for a smaller file.'
    '[CR][CR][COLOR=blue][B]How accurate is this speed test:[/B][/COLOR][CR]Not very accurate at all! As this test is based on downloading a file from a server it\'s reliant on the server not having a go-slow day '
    'but the servers used should be pretty reliable. The 10MB file is hosted on a different server to the others so if you\'re not getting the results expected please try another file. If you have a fast fiber '
    'connection the chances are your speed will show as considerably slower than your real download speed due to the server not being able to send the file as fast as your download speed allows. Essentially the '
    'test results will be limited by the speed of the server but you will at least be able to see if it\'s your connection that\'s causing buffering or if it\'s the host you\'re trying to stream from'
    '[CR][CR][COLOR=blue][B]What is the differnce between Live Streams and Online Video:[/COLOR][/B][CR]When you run the test you\'ll see results based on your speeds and these let you know the quality you should expect to '
    'be able stream with your connection. Live Streams as the title suggests are like traditional TV channels, they are being streamed live so for example if you wanted to watch CNN this would fall into this category. '
    'Online Videos relates to movies, tv shows, youtube clips etc. Basically anything that isn\'t live - if you\'re new to the world of streaming then think of it as On Demand content, this is content that\'s been recorded and stored on the web.'
    '[CR][CR][COLOR=blue][B]Why am I still getting buffering:[/COLOR][/B][CR]The results you get from this test are strictly based on your download speed, there are many other factors that can cause buffering and contrary to popular belief '
    'having a massively fast internet connection will not make any difference to your buffering issues if the server you\'re trying to get the content from is unable to send it fast enough. This can often happen and is usually '
    'down to heavy traffic (too many users accessing the same server). A 10 Mb/s connection should be plenty fast enough for almost all content as it\'s very rare a server can send it any quicker than that.'
    '[CR][CR][COLOR=blue][B]What\'s the difference between MB/s and Mb/s:[/COLOR][/B][CR]A lot of people think the speed they see advertised by their ISP is Megabytes (MB/S) per second - this is not true. Speeds are usually shown as Mb/s '
    'which is Megabit per second - there are 8 of these to a megabyte so if you want to work out how many megabytes per second you\'re getting you need to divide the speed by 8. It may sound sneaky but really it\'s just the unit that has always been used.'
    '[CR][CR]A direct link to the buffering thread explaining what you can do to improve your viewing experience can be found at [COLOR=darkcyan]http://bit.ly/bufferingfix[/COLOR]'
    '[CR][CR]Thank you, [COLOR=dodgerblue]T[/COLOR]otal[COLOR=dodgerblue]R[/COLOR]evolution Team.')
#-----------------------------------------------------------------------------------------------------------------
# Speedtest menu
def Speed_Test_Menu():
    o0oO('','[COLOR=blue]Instructions - Read me first[/COLOR]', 'none', 'speed_instructions', 'howto.png','','','')
    o0oO('','Download 16MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/16MB.txt', 'runtest', 'Download16.png','','','')
    o0oO('','Download 32MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/32MB.txt', 'runtest', 'Download32.png','','','')
    o0oO('','Download 64MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/64MB.txt', 'runtest', 'Download64.png','','','')
    o0oO('','Download 128MB file - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/128MB.txt', 'runtest', 'Download128.png','','','')
    o0oO('','Download 10MB file   - [COLOR=darkcyan]Server 2[/COLOR]', 'http://www.wswd.net/testdownloadfiles/10MB.zip', 'runtest', 'Download10.png','','','')
#-----------------------------------------------------------------------------------------------------------------
def Switch_Profile(name):
# Call the function to check if existing profile exists, if no profile exists it will create one.
    dp.create('Creating Profile','','','')
    buildname = Create_Profile(name)

# List pre-installed Kodi addons, we don't need to copy these
    mainaddons = []
    for item in os.listdir(KODI_ADDONS):
        mainaddons.append(item)

# Read contents of the addonslist for switching profile
        profileaddons     = open(os.path.join(CP_PROFILE,name,'addonlist'), mode='r')
        profilelist       = profileaddons.read()
        profileaddons.close()
        profilelist       = profilelist.split('|')

# Move any addons not in the profile list to the Master folder, Create_Addon_Pack makes addons small and we copy them to backup folder.
    Create_Addon_Pack('profiles')
    for item in os.listdir(ADDONS):
        if not item in mainaddons and item != 'plugin.program.totalinstaller' and item != 'repository.noobsandnerds' and item != 'packages':
            try:
                shutil.copytree(os.path.join(addonstemp,'addons',item),os.path.join(CP_PROFILE,'Master','backups',item))
                if debug == 'true':
                    xbmc.log("### Successfully copied "+item+" to "+os.path.join(CP_PROFILE,'Master','backups',item))
            except:
                xbmc.log("### Failed to copy "+item+" to backup folder, must already exist")
            if not item in profilelist and item != skin:
                try:
                    os.rename(os.path.join(ADDONS,item),os.path.join(CP_PROFILE,'Master',item))
                except:
                    try:
                        shutil.copytree(os.path.join(ADDONS,item),os.path.join(CP_PROFILE,'Master',item))
                    except:
                        try:
                            shutil.rmtree(os.path.join(ADDONS,item))
                        except:
                            xbmc.log("### Unable to move "+item+" as it's currently in use")
    shutil.rmtree(addonstemp)
                    
# Move addons in profile list from Master folder to main addons folder.
    for item in profilelist:
        if not item in mainaddons and not item in ADDONS:
            try:
                os.rename(os.path.join(CP_PROFILE,'Master',item),os.path.join(ADDONS,item))
            except:
                pass

    Wipe_Userdata()
    Wipe_Addon_Data()
    Wipe_Home2(EXCLUDES2)
    xbmc.log("### WIPE FUNCTIONS COMPLETE")
# Copy the rest of the data from profile folder to HOME
    try:
        localfile          = open(idfile, mode='r')
        content            = localfile.read()
        localfile.close()
        xbmc.log("### original idfile contents: "+content)
    except:
        xbmc.log("### original id file does not exist")

    try:
        extract.all(os.path.join(CP_PROFILE,name,'build.zip'), HOME, dp)
        success = 1
        xbmc.log("### Extraction of build successful")
    except:
        dialog.ok('Error',"Sorry it wasn't possible to extract your build, there is a problem with your build zip file.")
        success = 0
    if os.path.exists(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','id.xml')) and os.path.exists(os.path.join(ADDON_DATA,'ti_id','id.xml')):
        xbmc.log("### id.xml and temporary id.xml exists, attempting remove of original and replace with temp")
        os.remove(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','id.xml'))
        xbmc.log("### removal ok")
        os.rename(os.path.join(ADDON_DATA,'ti_id','id.xml'), os.path.join(ADDON_DATA,'plugin.program.totalinstaller','id.xml'))
        xbmc.log("### rename ok")
    if os.path.exists(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','startup.xml')) and os.path.exists(os.path.join(ADDON_DATA,'ti_id','startup.xml')):
        xbmc.log("### startup.xml and temporary startup.xml exists, attempting remove of original and replace with temp")
        os.remove(os.path.join(ADDON_DATA,'plugin.program.totalinstaller','startup.xml'))
        xbmc.log("### removal ok")
        os.rename(os.path.join(ADDON_DATA,'ti_id','startup.xml'), os.path.join(ADDON_DATA,'plugin.program.totalinstaller','startup.xml'))
        xbmc.log("### rename ok")
# Read the contents of id.xml
    localfile          = open(idfile, mode='r')
    content            = localfile.read()
    localfile.close()

    xbmc.log("### new idfile contents: "+content)

    if success == 1:
        KLL()
#---------------------------------------------------------------------------------------------------
# Menu for switching profiles - includes delete option
def Switch_Profile_Menu(url):
    o0oO('folder','[COLOR=darkcyan]DELETE A BUILD[/COLOR]',url,'delete_profile','','','')
    for name in os.listdir(CP_PROFILE):
        if name != 'Master' and name != url.replace(' ','_').replace("'",'').replace(':','-'):
            o0oO('','Load Profile: [COLOR=dodgerblue]'+name.replace('_',' ')+'[/COLOR]',name,'switch_profile','','','','')

#-----------------------------------------------------------------------------------------------------------------
#Show full description of build
def Test_Off():
    ADDON.setSetting('debug','false')
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
#Show full description of build
def Text_Guide(url):
    try:
        heading,text = url.split('|')
        TXT.TXT(heading, text)
    except:
        TXT.TXT('', url)
#---------------------------------------------------------------------------------------------------
# Get current timestamp in integer format
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
#-----------------------------------------------------------------------------------------------------------------
#Maintenance section
def Tools():
    if OpenELEC_Check():
        o0oO('','[COLOR=darkcyan]Wi-Fi Settings[/COLOR]','', 'openelec_settings', 'Wi-Fi.png','','','')
    o0oO('','[COLOR=gold]CLEAN MY KODI FOLDERS (Save Space)[/COLOR]', '', 'full_clean', '','','','')
    if codename!='':
        o0oO('',codename+' Keyword Install', keywordpath, 'keywords', 'Keywords.png','','','')
    o0oO('','Backup Download Folder Check','url','check_storage','','','','')
    o0oO('folder','Test My Download Speed', 'none', 'speedtest_menu', '','','','')
    o0oO('folder','Backup/Restore My Content','none','backup_restore','','','','')
    o0oO('folder','Advanced Options', '', 'advanced_tools', '','','','')
#-----------------------------------------------------------------------------------------------------------------
#Maintenance section
def Tools_Advanced():
    o0oO('','Check For Special Characters In Filenames','', 'ASCII_Check', '','','','')
    o0oO('','Check My IP Address', 'none', 'ipcheck', '','','','')
    o0oO('','Check XBMC/Kodi Version', 'none', 'xbmcversion', '','','','')
    o0oO('','Clear All Cache Folders','url','clear_cache','','','','')
    o0oO('','Clear Cached Artwork (thumbnails & textures)', 'none', 'remove_textures', '','','','')
    o0oO('','Clear Packages Folder','url','remove_packages','','','','')
    o0oO('folder','Completely remove an add-on (inc. passwords)','plugin','addon_removal_menu', '','','','')
    o0oO('','Convert Physical Paths To Special',HOME,'fix_special','','','','')
    o0oO('','Delete Addon_Data','url','remove_addon_data','','','','')
    o0oO('','Delete Old Builds/Zips From Device','url','remove_build','','','','')
    o0oO('','Delete Old Crash Logs','url','remove_crash_logs','','','','')
    o0oO('','Force Close Kodi','url','kill_xbmc','','','','')
    o0oO('','Make Add-ons Gotham/Helix Compatible','none','gotham', '','','','')
    o0oO('','Make Skins Kodi (Helix) Compatible','none','helix', '','','','')
    o0oO('','Passwords - Hide when typing in','none','hide_passwords', '','','','')
    o0oO('','Passwords - Unhide when typing in','none','unhide_passwords', '','','','')
    o0oO('','Update My Add-ons (Force Refresh)', 'none', 'update', '','','','')
    o0oO('','Upload Log','none','uploadlog', '','','','')
    o0oO('','View My Log','none','log', '','','','')
    o0oO('','Wipe My Install (Fresh Start)', 'none', 'wipe_xbmc', '','','','')
#-----------------------------------------------------------------------------------------------------------------
#Tutorials Addon Menu
def Tutorials_Addon_Menu(url):
    o0oO('folder','[COLOR=darkcyan]1. Add-on Maintenance[/COLOR]', str(url)+'&type=Maintenance', 'grab_tutorials', 'Maintenance.png','','','')
    o0oO('folder','Audio Add-ons', str(url)+'&type=Audio', 'grab_tutorials', 'Audio.png','','','')
    o0oO('folder','Picture Add-ons', str(url)+'&type=Pictures', 'grab_tutorials', 'Pictures.png','','','')
    o0oO('folder','Program Add-ons', str(url)+'&type=Programs', 'grab_tutorials', 'Programs.png','','','')
    o0oO('folder','Video Add-ons', str(url)+'&type=Video', 'grab_tutorials', 'Video.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# This creates the final menu showing build details, video and install link
def Tutorial_Menu(url):
    incremental = 'http://noobsandnerds.com/TI/TutorialPortal/downloadcount.php?id=%s' % (url)
    try:
        Open_URL(incremental)
    except:
        pass
    BaseURL           = 'http://noobsandnerds.com/TI/TutorialPortal/tutorialdetails.php?id=%s' % (url)
    link              = Open_URL(BaseURL).replace('\n','').replace('\r','')
    namematch         = re.compile('name="(.+?)"').findall(link)
    authormatch       = re.compile('author="(.+?)"').findall(link)
    videoguide1match  = re.compile('video_guide1="(.+?)"').findall(link)
    videoguide2match  = re.compile('video_guide2="(.+?)"').findall(link)
    videoguide3match  = re.compile('video_guide3="(.+?)"').findall(link)
    videoguide4match  = re.compile('video_guide4="(.+?)"').findall(link)
    videoguide5match  = re.compile('video_guide5="(.+?)"').findall(link)
    videolabel1match  = re.compile('video_label1="(.+?)"').findall(link)
    videolabel2match  = re.compile('video_label2="(.+?)"').findall(link)
    videolabel3match  = re.compile('video_label3="(.+?)"').findall(link)
    videolabel4match  = re.compile('video_label4="(.+?)"').findall(link)
    videolabel5match  = re.compile('video_label5="(.+?)"').findall(link)
    aboutmatch        = re.compile('about="(.+?)"').findall(link)
    step1match        = re.compile('step1="(.+?)"').findall(link)
    step2match        = re.compile('step2="(.+?)"').findall(link)
    step3match        = re.compile('step3="(.+?)"').findall(link)
    step4match        = re.compile('step4="(.+?)"').findall(link)
    step5match        = re.compile('step5="(.+?)"').findall(link)
    step6match        = re.compile('step6="(.+?)"').findall(link)
    step7match        = re.compile('step7="(.+?)"').findall(link)
    step8match        = re.compile('step8="(.+?)"').findall(link)
    step9match        = re.compile('step9="(.+?)"').findall(link)
    step10match       = re.compile('step10="(.+?)"').findall(link)
    step11match       = re.compile('step11="(.+?)"').findall(link)
    step12match       = re.compile('step12="(.+?)"').findall(link)
    step13match       = re.compile('step13="(.+?)"').findall(link)
    step14match       = re.compile('step14="(.+?)"').findall(link)
    step15match       = re.compile('step15="(.+?)"').findall(link)
    screenshot1match  = re.compile('screenshot1="(.+?)"').findall(link)
    screenshot2match  = re.compile('screenshot2="(.+?)"').findall(link)
    screenshot3match  = re.compile('screenshot3="(.+?)"').findall(link)
    screenshot4match  = re.compile('screenshot4="(.+?)"').findall(link)
    screenshot5match  = re.compile('screenshot5="(.+?)"').findall(link)
    screenshot6match  = re.compile('screenshot6="(.+?)"').findall(link)
    screenshot7match  = re.compile('screenshot7="(.+?)"').findall(link)
    screenshot8match  = re.compile('screenshot8="(.+?)"').findall(link)
    screenshot9match  = re.compile('screenshot9="(.+?)"').findall(link)
    screenshot10match = re.compile('screenshot10="(.+?)"').findall(link)
    screenshot11match = re.compile('screenshot11="(.+?)"').findall(link)
    screenshot12match = re.compile('screenshot12="(.+?)"').findall(link)
    screenshot13match = re.compile('screenshot13="(.+?)"').findall(link)
    screenshot14match = re.compile('screenshot14="(.+?)"').findall(link)
    screenshot15match = re.compile('screenshot15="(.+?)"').findall(link)
   
    name         = namematch[0] if (len(namematch) > 0) else ''
    author       = authormatch[0] if (len(authormatch) > 0) else ''
    videoguide1  = videoguide1match[0] if (len(videoguide1match) > 0) else 'None'
    videoguide2  = videoguide2match[0] if (len(videoguide2match) > 0) else 'None'
    videoguide3  = videoguide3match[0] if (len(videoguide3match) > 0) else 'None'
    videoguide4  = videoguide4match[0] if (len(videoguide4match) > 0) else 'None'
    videoguide5  = videoguide5match[0] if (len(videoguide5match) > 0) else 'None'
    videolabel1  = videolabel1match[0] if (len(videolabel1match) > 0) else 'None'
    videolabel2  = videolabel2match[0] if (len(videolabel2match) > 0) else 'None'
    videolabel3  = videolabel3match[0] if (len(videolabel3match) > 0) else 'None'
    videolabel4  = videolabel4match[0] if (len(videolabel4match) > 0) else 'None'
    videolabel5  = videolabel5match[0] if (len(videolabel5match) > 0) else 'None'
    about        = aboutmatch[0] if (len(aboutmatch) > 0) else ''
    step1        = '[CR][CR][COLOR=dodgerblue]Step 1:[/COLOR][CR]'+step1match[0] if (len(step1match) > 0) else ''
    step2        = '[CR][CR][COLOR=dodgerblue]Step 2:[/COLOR][CR]'+step2match[0] if (len(step2match) > 0) else ''
    step3        = '[CR][CR][COLOR=dodgerblue]Step 3:[/COLOR][CR]'+step3match[0] if (len(step3match) > 0) else ''
    step4        = '[CR][CR][COLOR=dodgerblue]Step 4:[/COLOR][CR]'+step4match[0] if (len(step4match) > 0) else ''
    step5        = '[CR][CR][COLOR=dodgerblue]Step 5:[/COLOR][CR]'+step5match[0] if (len(step5match) > 0) else ''
    step6        = '[CR][CR][COLOR=dodgerblue]Step 6:[/COLOR][CR]'+step6match[0] if (len(step6match) > 0) else ''
    step7        = '[CR][CR][COLOR=dodgerblue]Step 7:[/COLOR][CR]'+step7match[0] if (len(step7match) > 0) else ''
    step8        = '[CR][CR][COLOR=dodgerblue]Step 8:[/COLOR][CR]'+step8match[0] if (len(step8match) > 0) else ''
    step9        = '[CR][CR][COLOR=dodgerblue]Step 9:[/COLOR][CR]'+step9match[0] if (len(step9match) > 0) else ''
    step10       = '[CR][CR][COLOR=dodgerblue]Step 10:[/COLOR][CR]'+step10match[0] if (len(step10match) > 0) else ''
    step11       = '[CR][CR][COLOR=dodgerblue]Step 11:[/COLOR][CR]'+step11match[0] if (len(step11match) > 0) else ''
    step12       = '[CR][CR][COLOR=dodgerblue]Step 12:[/COLOR][CR]'+step12match[0] if (len(step12match) > 0) else ''
    step13       = '[CR][CR][COLOR=dodgerblue]Step 13:[/COLOR][CR]'+step13match[0] if (len(step13match) > 0) else ''
    step14       = '[CR][CR][COLOR=dodgerblue]Step 14:[/COLOR][CR]'+step14match[0] if (len(step14match) > 0) else ''
    step15       = '[CR][CR][COLOR=dodgerblue]Step 15:[/COLOR][CR]'+step15match[0] if (len(step15match) > 0) else ''
    screenshot1  = screenshot1match[0] if (len(screenshot1match) > 0) else ''
    screenshot2  = screenshot2match[0] if (len(screenshot2match) > 0) else ''
    screenshot3  = screenshot3match[0] if (len(screenshot3match) > 0) else ''
    screenshot4  = screenshot4match[0] if (len(screenshot4match) > 0) else ''
    screenshot5  = screenshot5match[0] if (len(screenshot5match) > 0) else ''
    screenshot6  = screenshot6match[0] if (len(screenshot6match) > 0) else ''
    screenshot7  = screenshot7match[0] if (len(screenshot7match) > 0) else ''
    screenshot8  = screenshot8match[0] if (len(screenshot8match) > 0) else ''
    screenshot9  = screenshot9match[0] if (len(screenshot9match) > 0) else ''
    screenshot10 = screenshot10match[0] if (len(screenshot10match) > 0) else ''
    screenshot11 = screenshot11match[0] if (len(screenshot11match) > 0) else ''
    screenshot12 = screenshot12match[0] if (len(screenshot12match) > 0) else ''
    screenshot13 = screenshot13match[0] if (len(screenshot13match) > 0) else ''
    screenshot14 = screenshot14match[0] if (len(screenshot14match) > 0) else ''
    screenshot15 = screenshot15match[0] if (len(screenshot15match) > 0) else ''
    description  = str('[COLOR=orange]Author: [/COLOR]'+author+'[CR][CR][COLOR=lime]About: [/COLOR]'+about+step1+step2+step3+step4+step5+step6+step7+step8+step9+step10+step11+step12+step13+step14+step15)

    if step1 != '':
        o0oO('','[COLOR=darkcyan][Text Guide][/COLOR]  '+name,description,'text_guide','How_To.png',FANART,about,'')    
    if videoguide1 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel1,videoguide1,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide2 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel2,videoguide2,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide3 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel3,videoguide3,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide4 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel4,videoguide4,'play_video','Video_Guide.png',FANART,'','')    
    if videoguide5 != 'None':
        o0oO('','[COLOR=lime][VIDEO][/COLOR]  '+videolabel5,videoguide5,'play_video','Video_Guide.png',FANART,'','')    
#-----------------------------------------------------------------------------------------------------------------
#Tutorials Root menu listings
def Tutorial_Root_Menu():
    if ADDON.getSetting('tutorial_manual_search')=='true':
        o0oO('folder','[COLOR=darkcyan]Manual Search[/COLOR]', 'tutorials', 'manual_search', 'Manual_Search.png','','','')
    if ADDON.getSetting('tutorial_all')=='true':
        o0oO('folder','[COLOR=lime]All Guides[/COLOR] Everything in one place', '', 'grab_tutorials', 'All.png','','','')
    if ADDON.getSetting('tutorial_kodi')=='true':
        o0oO('folder','[COLOR=lime]XBMC / Kodi[/COLOR] Specific', '', 'xbmc_menu', 'XBMC.png','','','')
    if ADDON.getSetting('tutorial_xbmc4xbox')=='true':
        o0oO('folder','[COLOR=lime]XBMC4Xbox[/COLOR] Specific', '&platform=XBMC4Xbox', 'xbmc_menu', 'XBMC4Xbox.png','','','')
    if ADDON.getSetting('tutorial_android')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Android', '&platform=Android', 'platform_menu', 'Android.png','','','')
    if ADDON.getSetting('tutorial_atv')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Apple TV', '&platform=ATV', 'platform_menu', 'ATV.png','','','')
    if ADDON.getSetting('tutorial_ios')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] ATV2 & iOS', '&platform=iOS', 'platform_menu', 'iOS.png','','','')
    if ADDON.getSetting('tutorial_linux')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Linux', '&platform=Linux', 'platform_menu', 'Linux.png','','','')
    if ADDON.getSetting('tutorial_pure_linux')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Pure Linux', '&platform=Custom_Linux', 'platform_menu', 'Custom_Linux.png','','','')
    if ADDON.getSetting('tutorial_openelec')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] OpenELEC', '&platform=OpenELEC', 'platform_menu', 'OpenELEC.png','','','')
    if ADDON.getSetting('tutorial_osmc')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] OSMC', '&platform=OSMC', 'platform_menu', 'OSMC.png','','','')
    if ADDON.getSetting('tutorial_osx')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] OSX', '&platform=OSX', 'platform_menu', 'OSX.png','','','')
    if ADDON.getSetting('tutorial_raspbmc')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Raspbmc', '&platform=Raspbmc', 'platform_menu', 'Raspbmc.png','','','')
    if ADDON.getSetting('tutorial_windows')=='true':
        o0oO('folder','[COLOR=orange][Platform][/COLOR] Windows', '&platform=Windows', 'platform_menu', 'Windows.png','','','')
    if ADDON.getSetting('tutorial_allwinner')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Allwinner Devices', '&hardware=Allwinner', 'platform_menu', 'Allwinner.png','','','')
    if ADDON.getSetting('tutorial_aftv')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Amazon Fire TV', '&hardware=AFTV', 'platform_menu', 'AFTV.png','','','')
    if ADDON.getSetting('tutorial_amlogic')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] AMLogic Devices', '&hardware=AMLogic', 'platform_menu', 'AMLogic.png','','','')
    if ADDON.getSetting('tutorial_boxee')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Boxee', '&hardware=Boxee', 'platform_menu', 'Boxee.png','','','')
    if ADDON.getSetting('tutorial_intel')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Intel Devices', '&hardware=Intel', 'platform_menu', 'Intel.png','','','')
    if ADDON.getSetting('tutorial_rpi')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Raspberry Pi', '&hardware=RaspberryPi', 'platform_menu', 'RaspberryPi.png','','','')
    if ADDON.getSetting('tutorial_rockchip')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Rockchip Devices', '&hardware=Rockchip', 'platform_menu', 'Rockchip.png','','','')
    if ADDON.getSetting('tutorial_xbox')=='true':
        o0oO('folder','[COLOR=dodgerblue][Hardware][/COLOR] Xbox', '&hardware=Xbox', 'platform_menu', 'Xbox_Original.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Unhide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Unhide_Passwords():
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Make Add-on Passwords Visible?", "This will make all your add-on passwords visible in the add-on settings. Are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if  'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace(' option="hidden"', '') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:
                                    pass
        dialog.ok("Passwords Are now visible", "Your passwords will now be visible in your add-on settings. If you want to undo this please use the option to hide passwords.") 
#---------------------------------------------------------------------------------------------------
# Function to update the current running build
def Update_Community(name,url,video,description,skins,guisettingslink,artpack):
    dp.create("Backing Up Important Data",'Please wait...','','')

# Get size of guisettings, based on this we will either force close or not
    guicontentsize = open(idfile, mode='r')
    guicontent     = guicontentsize.read()
    guicontentsize.close()
    
    guiorig        = re.compile('gui="(.+?)"').findall(guicontent)
    guiorigsize    = guiorig[0] if (len(guiorig) > 0) else '0'

# Store contents of favourites and sources if enabled in settings, ready for writing over top of new build
    if keepfaves=='true':
        try:
            favescontent = open(FAVS, mode='r')
            favestext = favescontent.read()
            favescontent.close()
        
        except:
            xbmc.log("### No favourites file to copy")
    
    if keepsources=='true':
        try:
            sourcescontent = open(SOURCE, mode='r')
            sourcestext = sourcescontent.read()
            sourcescontent.close()
        
        except:
            xbmc.log("### No sources file to copy")

    choice4=1
    Check_Download_Path()

# Check to see if the new guisettings file exists, if it does overwrite the main guisettings
    if os.path.exists(GUINEW):
        
        if os.path.exists(GUI):
            os.remove(GUINEW)
        
        else:
            os.rename(GUINEW,GUI)

    if os.path.exists(GUIFIX):
        os.remove(GUIFIX)

# Function for debugging, creates a file that was created in previous call and subsequently deleted when run
    if not os.path.exists(tempfile):
        localfile = open(tempfile, mode='w+')
        localfile.close() # Added this, not sure if we need it open as a hack

    dp.close()
    dp.create("Downloading Skin Fix","Downloading guisettings.xml",'', 'Please Wait')
    lib=os.path.join(USB, 'guifix.zip')

#Download guisettings from the build
    try:
        xbmc.log("### attempting to download guisettings.xml")
        downloader.download(guisettingslink, lib, dp)
        dp.close()
    except:
        dialog.ok('Problem Detected','Sorry there was a problem downloading the guisettings file. Please check your storage location, if you\'re certain that\'s ok please notify the build author on the relevant support thread.')
        xbmc.log("### FAILED to download "+guisettingslink)
# Check that gui file is a real zip and the uploader hasn't put a bad link in the db
    if zipfile.is_zipfile(lib):
        guisize = str(os.path.getsize(lib))
    
    else:
        guisize = guiorigsize

# Pull the details about the currently downloading build
    localfile = open(tempfile, mode='r')
    content   = localfile.read()
    localfile.close()

    temp         = re.compile('id="(.+?)"').findall(content)
    tempname     = re.compile('name="(.+?)"').findall(content)
    tempversion  = re.compile('version="(.+?)"').findall(content)

    tempcheck    = temp[0] if (len(temp) > 0) else ''
    namecheck    = tempname[0] if (len(tempname) > 0) else ''
    versioncheck = tempversion[0] if (len(tempversion) > 0) else ''

    if os.path.exists(guitemp):
        os.removedirs(guitemp)

# If the guisettings on server are a different size to existing do the following (no need to force close and merge data)
    if guiorigsize!=guisize:
        try:
            os.rename(GUI,GUINEW)
        
        except:
            dialog.ok("NO GUISETTINGS!",'No guisettings.xml file has been found.', 'Please exit Kodi and try again','')
            return
    
# If user chooses to create a backup do a complete backup excluding any unwanted files
    if video != 'fresh':
        choice = xbmcgui.Dialog().yesno(name, 'We highly recommend backing up your existing build before installing any community builds. Would you like to perform a backup first?', nolabel='Backup',yeslabel='Install')
        
        if choice == 0:
            mybackuppath = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds'))
            
            if not os.path.exists(mybackuppath):
                os.makedirs(mybackuppath)
            
            vq = Get_Keyboard( heading="Enter a name for this backup" )
            
            if ( not vq ):
                return False, 0
            
            title              = urllib.quote_plus(vq)
            backup_zip         = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
            exclude_dirs_full  =  ['plugin.program.totalinstaller','plugin.program.tbs']
            exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','Thumbs.db','.gitignore']
            message_header     = "Creating full backup of existing build"
            message1           = "Archiving..."
            message2           = ""
            message3           = "Please Wait"
            Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)

    writefile = open(idfile, mode='w+')
    
    if guiorigsize!=guisize:
        writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+' [COLOR=yellow](Partially installed)[/COLOR]"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
    
    else:
        writefile.write('id="'+str(tempcheck)+'"\nname="'+namecheck+'"\nversion="'+versioncheck+'"\ngui="'+guisize+'"')
    writefile.close()

# Backup library database if option selected during install process
    if video == 'libprofile' or video == 'library' or video == 'updatelibprofile' or video == 'updatelibrary':
        try:
            shutil.copytree(DATABASE, tempdbpath, symlinks=False, ignore=shutil.ignore_patterns("Textures13.db","Addons16.db","Addons15.db","saltscache.db-wal","saltscache.db-shm","saltscache.db","onechannelcache.db")) #Create temp folder for databases, give user option to overwrite existing library
        
        except:
            choice4 = xbmcgui.Dialog().yesno(name, 'There was an error trying to backup some databases. Continuing may wipe your existing library. Do you wish to continue?', nolabel='No, cancel',yeslabel='Yes, overwrite')
            
            if choice4 == 0:
                return
        
        backup_zip = xbmc.translatePath(os.path.join(USB,'Database.zip'))
        Archive_File(tempdbpath,backup_zip)
    
    if choice4 == 0:
        return
    
    time.sleep(1)

# Create a backup location outside of kodi for addon dependencies so they aren't accidentally wiped and download the build
    tempbackup = xbmc.translatePath(os.path.join(HOME,'..','koditemp.zip'))
    time.sleep(2)
    dp.create("Community Builds","Downloading "+description +" build.",'', 'Please Wait')
    filename = description.replace(' ','_').replace(':','-').replace("'",'')
    lib=os.path.join(CBPATH, filename+'.zip')
    
    if not os.path.exists(CBPATH):
        os.makedirs(CBPATH)
    
    downloader.download(url, lib, dp)

# Read the contents of profiles into memory so we can write back later
    try:
        readfile2        = open(PROFILES, mode='r')
        profile_contents = readfile2.read()
        readfile2.close()
    except:
        xbmc.log("### No profiles detected, most likely a fresh wipe performed")
    
    dp.close()
    dp.create("Community Builds","Checking ",'', 'Please Wait')

# Extract the build
    if zipfile.is_zipfile(lib):
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(lib,HOME,dp)
    
    else:
        dialog.ok('Not a valid zip file','This file is not a valid zip file, please let the build author know on their support thread so they can amend the download path. It\'s most likely just a simple typo on their behalf.')
        return

    dp.create("Restoring Dependencies","Checking ",'', 'Please Wait')
    dp.update(0,"", "Extracting Zip Please Wait")
    
    if keepfaves == 'true':
        try:
            xbmc.log("### Attempting to add back favourites ###")
            writefile = open(FAVS, mode='w+')
            writefile.write(favestext)
            writefile.close()
            dp.update(0,"", "Copying Favourites")
        except:
            xbmc.log("### Failed to copy back favourites")
    
    if keepsources == 'true':
        try:
            xbmc.log("### Attempting to add back sources ###")
            writefile = open(SOURCE, mode='w+')
            writefile.write(sourcestext)
            writefile.close()
            dp.update(0,"", "Copying Sources")
        
        except:
            xbmc.log("### Failed to copy back sources")
    
    time.sleep(1)
    if os.path.exists(tempdbpath):
        shutil.rmtree(tempdbpath)

# Update the startup.xml version number so it can check for update on next run of add-on
    if os.path.exists(startuppath):
        localfile = open(startuppath, mode='r')
        content = localfile.read()
        localfile.close()
        localversionmatch = re.compile('version="[\s\S]*?"').findall(content)
        localversioncheck  = localversionmatch[0] if (len(localversionmatch) > 0) else ''
        replacefile = content.replace(localversioncheck,'version="'+versioncheck+'"')
        writefile = open(startuppath, mode='w')
        writefile.write(str(replacefile))
        writefile.close()
    
    else:
        writefile = open(startuppath, mode='w+')
        writefile.write('date="01011001"\nversion="'+versioncheck+'"')
        writefile.close()

# Remove the downloaded build if not set to keep in add-on settings
    if localcopy == 'false':
        os.remove(lib)

# Replace the profiles content with what we stored earlier
    if 'prof' in video:
        try:
            profiletxt = open(PROFILES, mode='w+')
            profiletxt.write(profile_contents)
            profiletxt.close()
        except:
            xbmc.log("### Failed to write existing profile info back into profiles.xml")

# If the user chose to keep their library we extract it from the backup location then delete the old file
    if video == 'library' or video == 'libprofile' or video == 'updatelibprofile' or video == 'updatelibrary':
        extract.all(backup_zip,DATABASE,dp)

# If the initial database backup was successful wipe the backup
        if choice4 !=1:
            shutil.rmtree(tempdbpath)
    try:
        dp.close()
    except:
        pass

# If this is a newer (smaller version of a build) do the install process of the add-ons
    if os.path.exists(backupaddonspath):
        CB_Install_Final(description)
        
        try:
            os.remove(backupaddonspath)
        
        except:
            xbmc.log("###' Failed to remove: "+backupaddonspath)
        
        try:
            shutil.rmtree(addonstemp)

        except:
            xbmc.log("###' Failed to remove: "+addonstemp)
    
    else:
        xbmc.log("### Community Builds - using an old build")

# If the guisettings downloaded are a different size to existing we need to merge guisettings and force close
    if guiorigsize!=guisize:
        xbmc.log("### GUI SIZE DIFFERENT ATTEMPTING MERGE ###")
        newguifile = os.path.join(HOME,'newbuild')
        
        if not os.path.exists(newguifile):
            os.makedirs(newguifile)
 
        os.makedirs(guitemp)
        time.sleep(1)
        GUI_Merge(guisettingslink,video)
        time.sleep(1)
        KLL()
        dialog.ok("Force Close Required", "If you\'re seeing this message it means the force close was unsuccessful. Please close XBMC/Kodi via your operating system or pull the power.")

    if guiorigsize==guisize:
        dialog.ok('Successfully Updated','Congratulations the following build:[COLOR=dodgerblue]',description,'[/COLOR]has been successfully updated!')
#---------------------------------------------------------------------------------------------------
#Option to upload a log
def Upload_Log(): 
    if ADDON.getSetting('email')=='':
        dialog = xbmcgui.Dialog()
        dialog.ok("No Email Address Set", "A new window will Now open for you to enter your Email address. The logfile will be sent here")
        ADDON.openSettings()
    xbmc.executebuiltin('XBMC.RunScript(special://home/addons/'+AddonID+'/uploadLog.py)')
#---------------------------------------------------------------------------------------------------
# Simple function to force refresh the repo's and addons folder
def Update_Repo():
    xbmc.executebuiltin( 'UpdateLocalAddons' )
    xbmc.executebuiltin( 'UpdateAddonRepos' )    
    xbmcgui.Dialog().ok('Force Refresh Started Successfully', 'Depending on the speed of your device it could take a few minutes for the update to take effect.')
    return
#-----------------------------------------------------------------------------------------------------------------
# Check to see if we can ping google.com or google.cn
def Connectivity_Check():
    internetcheck = 1
    try:
        Open_URL('http://google.com')
    except:
        try:
            Open_URL('http://google.com')
        except:
            try:
                Open_URL('http://google.com')
            except:
                try:
                    Open_URL('http://google.cn')
                except:
                    try:
                        Open_URL('http://google.cn')
                    except:
                        dialog.ok("NO INTERNET CONNECTION",'It looks like this device isn\'t connected to the internet. Only some of the maintenance options will work until you fix the connectivity problem.')
                        Categories('','','','[COLOR=orange]NO INTERNET CONNECTION[/COLOR]')
                        internetcheck=0
    if internetcheck==1:
        Build_Check()
#-----------------------------------------------------------------------------------------------------------------
#Initial online check for new video
def Build_Check():
    xbmc.log("### Build Check Started")
    localbuildcheck   = 'None'
    localidcheck      = '0'
#Read the contents of startup.xml
    localfile           = open(startuppath, mode='r')
    content             = localfile.read()
    localfile.close()
    
    localdatecheckmatch = re.compile('date="(.+?)"').findall(content)
    localdatecheck      = localdatecheckmatch[0] if (len(localdatecheckmatch) > 0) else ''
    localversionmatch   = re.compile('version="(.+?)"').findall(content)
    localversioncheck   = localversionmatch[0] if (len(localversionmatch) > 0) else ''

    localfile2          = open(idfile, mode='r')
    content2            = localfile2.read()
    localfile2.close()
    
    localidmatch        = re.compile('id="(.+?)"').findall(content2)
    localbuildmatch     = re.compile('name="(.+?)"').findall(content2)
    localidcheck        = localidmatch[0] if (len(localidmatch) > 0) else 'None'
    localbuildcheck     = localbuildmatch[0] if (len(localbuildmatch) > 0) else ''

    Categories2(localbuildcheck,localversioncheck,localidcheck,'')
#-----------------------------------------------------------------------------------------------------------------    
def Wipe_Cache():
    PROFILE_ADDON_DATA = os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data')))

    cachelist = [
        (PROFILE_ADDON_DATA),
        (ADDON_DATA),
        (os.path.join(HOME,'cache')),
        (os.path.join(HOME,'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(ADDON_DATA,'script.module.simple.downloader')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','script.module.simple.downloader')))),
        (os.path.join(ADDON_DATA,'plugin.video.itv','Images')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','plugin.video.itv','Images'))))]

    for item in cachelist:
        if os.path.exists(item) and item != ADDON_DATA and item != PROFILE_ADDON_DATA:
            for root, dirs, files in os.walk(item):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            xbmc.log("### Successfully cleared "+str(file_count)+" files from "+os.path.join(item,d))
                        except:
                            xbmc.log("### Failed to wipe cache in: "+os.path.join(item,d))
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'Cache' in d or 'cache' in d or 'CACHE' in d:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            xbmc.log("### Successfully wiped "+os.path.join(item,d))
                        except:
                            xbmc.log("### Failed to wipe cache in: "+os.path.join(item,d))

# Genesis cache - held in database file
    try:
        genesisCache = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
        dbcon = database.connect(genesisCache)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS rel_list")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS rel_lib")
        dbcur.execute("VACUUM")
        dbcon.commit()
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
#Function to clear the addon_data
def Wipe_Kodi(mode):
    if zip == '':
        dialog.ok('Please set your backup location before proceeding','You have not set your backup storage folder.\nPlease update the addon settings and try again.')
        ADDON.openSettings(sys.argv[0])
        zip2 = ADDON.getSetting('zip')
        if zip2 == '':
            Wipe_Kodi(mode)
    mybackuppath = xbmc.translatePath(os.path.join(USB,'Community_Builds','My_Builds'))
    if not os.path.exists(mybackuppath):
        os.makedirs(mybackuppath)
    choice = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe?', '', 'All addons and settings will be completely wiped!', yeslabel='Yes',nolabel='No')
# Check Confluence is running before doing a wipe
    if choice == 1:
        if skin!= "skin.confluence":
            dialog.ok('Default Confluence Skin Required','Please switch to the default Confluence skin before performing a wipe.')
            xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
            return
        else:
#Give the option to do a full backup before wiping
            choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'This will completely wipe your install.', 'Would you like to create a backup before proceeding?', '', yeslabel='No', nolabel='Yes')
            if choice == 0:
                if not os.path.exists(mybackuppath):
                    os.makedirs(mybackuppath)
                vq = Get_Keyboard( heading="Enter a name for this backup" )
                if ( not vq ): return False, 0
                title = urllib.quote_plus(vq)
                backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                exclude_dirs_full =  ['plugin.program.totalinstaller','plugin.program.tbs']
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            Wipe_Home(EXCLUDES)
            Wipe_Userdata()
            Wipe_Addons()
            Wipe_Addon_Data()
            Wipe_Home2(EXCLUDES)
            if os.path.exists(startuppath):
                os.remove(startuppath)
            if os.path.exists(tempfile):
                os.remove(tempfile)
            if os.path.exists(idfile):
                os.remove(idfile)
        if mode != 'CB':
            KLL()
        try:
            os.remove(startuppath)
        except:
            xbmc.log("### Failed to remove startup.xml")
        try:    
            os.remove(idfile)
        except:
            xbmc.log("### Failed to remove id.xml")
    else:
        return
#-----------------------------------------------------------------------------------------------------------------
#For loop to wipe files in special://home but leave ones in EXCLUDES untouched
def Wipe_Home(excludefiles):
    dp.create("Wiping Existing Content",'','Please wait...', '')
    for root, dirs, files in os.walk(HOME,topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDES]
        for name in files:
            try:                            
                dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
                os.unlink(os.path.join(root, name))
                os.remove(os.path.join(root,name))
                os.rmdir(os.path.join(root,name))
            except:
                xbmc.log("Failed to remove file: "+name)
#-----------------------------------------------------------------------------------------------------------------
# Remove userdata folder
def Wipe_Userdata():
    userdatadirs=[name for name in os.listdir(USERDATA) if os.path.isdir(os.path.join(USERDATA, name))]
    try:
        for name in userdatadirs:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(USERDATA,name))
            except:
                xbmc.log("Failed to remove: %s" % name)
    except:
        pass

# Clean up userdata and leave items untouched that were set in addon settings
    for root, dirs, files in os.walk(USERDATA,topdown=True):
       dirs[:] = [d for d in dirs if d not in EXCLUDES]
       for name in files:
           try:                            
               dp.update(0,"Removing [COLOR=yellow]"+name+'[/COLOR]','','Please wait...')
               os.unlink(os.path.join(root, name))
               os.remove(os.path.join(root,name))
           except:
               xbmc.log("Failed to remove file: "+name)
#-----------------------------------------------------------------------------------------------------------------
# Remove addon directories
def Wipe_Addons():
    addondirs=[name for name in os.listdir(ADDONS) if os.path.isdir(os.path.join(ADDONS, name))]
    try:
        for name in addondirs:
            try:
                if keeprepos=='true':
                    if name not in EXCLUDES and not 'repo' in name:
                        dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                        shutil.rmtree(os.path.join(ADDONS,name))
                else:   
                    if name not in EXCLUDES:
                        dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                        shutil.rmtree(os.path.join(ADDONS,name))
            except:
                xbmc.log("Failed to remove: %s" % name)
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Remove addon_data
def Wipe_Addon_Data():
    addondatadirs=[name for name in os.listdir(ADDON_DATA) if os.path.isdir(os.path.join(ADDON_DATA, name))]
    try:
        for name in addondatadirs:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Removing Add-on Data: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDON_DATA,name))
            except:
                xbmc.log("Failed to remove: %s" % name)
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Clean up everything in the home path
def Wipe_Home2(excludefiles):
    homepath=[name for name in os.listdir(HOME) if os.path.isdir(os.path.join(HOME, name))]
    try:
        for name in homepath:
            try:
                if name not in excludefiles:
                    dp.update(0,"Cleaning Directory: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(HOME,name))
            except:
                xbmc.log("Failed to remove: %s" % name)
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
#XBMC/Kodi/XBMC4Xbox tutorials menu2
def XBMC_Menu(url):
    o0oO('folder','[COLOR=darkcyan]1. Install[/COLOR]', str(url)+'&tags=Install&XBMC=1', 'grab_tutorials', 'Install.png','','','')
    o0oO('folder','[COLOR=lime]2. Settings[/COLOR]', str(url)+'&tags=Settings', 'grab_tutorials', 'Settings.png','','','')
    o0oO('folder','[COLOR=orange]3. Add-ons[/COLOR]', str(url), 'tutorial_addon_menu', 'Addons.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Audio', str(url)+'&tags=Audio', 'grab_tutorials', 'Audio.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Errors', str(url)+'&tags=Errors', 'grab_tutorials', 'Errors.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Gaming', str(url)+'&tags=Gaming', 'grab_tutorials', 'gaming_portal.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  LiveTV', str(url)+'&tags=LiveTV', 'grab_tutorials', 'LiveTV.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Maintenance', str(url)+'&tags=Maintenance', 'grab_tutorials', 'Maintenance.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Pictures', str(url)+'&tags=Pictures', 'grab_tutorials', 'Pictures.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Profiles', str(url)+'&tags=Profiles', 'grab_tutorials', 'Profiles.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Skins', str(url)+'&tags=Skins', 'grab_tutorials', 'Skin.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Video', str(url)+'&tags=Video', 'grab_tutorials', 'Video.png','','','')
    o0oO('folder','[COLOR=dodgerblue][XBMC/Kodi][/COLOR]  Weather', str(url)+'&tags=Weather', 'grab_tutorials', 'Weather.png','','','')
#-----------------------------------------------------------------------------------------------------------------
#Report back with the version of Kodi installed
def XBMC_Version(url):
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        kodiorxbmc = 'You are running XBMC'
    else:
        kodiorxbmc = 'You are running Kodi'
    dialog=xbmcgui.Dialog()
    dialog.ok(kodiorxbmc, "Your version is: %s" % version)
#-----------------------------------------------------------------------------------------------------------------
# Main json query function to get response - thanks to spoyser who's code I've used for this
# def getSetting(setting):
    # try:
        # setting = '"%s"' % setting
 
        # query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (setting)
        # log(query)
        # response = xbmc.executeJSONRPC(query)
        # log(response)

        # response = simplejson.loads(response)                

        # if response.has_key('result'):
            # if response['result'].has_key('value'):
                # return response ['result']['value'] 
    # except:
        # pass

    # return None

#Addon starts here


def Launch():
    addon_id=None
    artpack=None
    audioaddons=None
    author=None
    buildname=None
    data_path=None
    description=None
    email=None
    fanart=None
    forum=None
    iconimage=None
    link=None
    local=None
    messages=None
    mode=None
    menutype=None
    name=None
    posts=None
    programaddons=None
    provider_name=None
    repo_id=None
    repo_link=None
    skins=None
    sources=None
    title=None
    updated=None
    unread=None
    url=None
    version=None
    video=None
    videoaddons=None
    welcometext=None
    zip_link=None
    direct='maintenance'
    params=Get_Params()

    try:
        addon_id=urllib.unquote_plus(params["addon_id"])
    except:
        pass
    try:
        adult=urllib.unquote_plus(params["adult"])
    except:
        pass
    try:
        artpack=urllib.unquote_plus(params["artpack"])
    except:
        pass
    try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
    except:
        pass
    try:
        author=urllib.unquote_plus(params["author"])
    except:
        pass
    try:
        buildname=urllib.unquote_plus(params["buildname"])
    except:
        pass
    try:
        data_path=urllib.unquote_plus(params["data_path"])
    except:
        pass
    try:
        description=urllib.unquote_plus(params["description"])
    except:
        pass
    try:
        email=urllib.unquote_plus(params["email"])
    except:
        pass
    try:
        fanart=urllib.unquote_plus(params["fanart"])
    except:
        pass
    try:
        forum=urllib.unquote_plus(params["forum"])
    except:
        pass
    try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
    except:
        pass
    try:
        iconimage=urllib.unquote_plus(params["iconimage"])
    except:
        pass
    try:
        link=urllib.unquote_plus(params["link"])
    except:
        pass
    try:
        local=urllib.unquote_plus(params["local"])
    except:
        pass
    try:
        url=urllib.unquote_plus(params["menutype"])
    except:
        pass
    try:
        messages=urllib.unquote_plus(params["messages"])
    except:
        pass
    try:    
        mode=str(params["mode"])
    except:
        pass
    try:
        name=urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
    except:
        pass
    try:
        posts=urllib.unquote_plus(params["posts"])
    except:
        pass
    try:
        programaddons=urllib.unquote_plus(params["programaddons"])
    except:
        pass
    try:
        provider_name=urllib.unquote_plus(params["provider_name"])
    except:
        pass
    try:
        repo_link=urllib.unquote_plus(params["repo_link"])
    except:
        pass
    try:
        repo_id=urllib.unquote_plus(params["repo_id"])
    except:
        pass
    try:
        skins=urllib.unquote_plus(params["skins"])
    except:
        pass
    try:
        sources=urllib.unquote_plus(params["sources"])
    except:
        pass
    try:
        updated=urllib.unquote_plus(params["updated"])
    except:
        pass
    try:
        unread=urllib.unquote_plus(params["unread"])
    except:
        pass
    try:
        url=urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        version=urllib.unquote_plus(params["version"])
    except:
        pass
    try:
        video=urllib.unquote_plus(params["video"])
    except:
        pass
    try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
    except:
        pass
    try:
        welcometext=urllib.unquote_plus(params["welcometext"])
    except:
        pass
    try:
        zip_link=urllib.unquote_plus(params["zip_link"])
    except:
        pass
        
    if not os.path.exists(userdatafolder):
        os.makedirs(userdatafolder)

    if not os.path.exists(MEDIA):
        os.makedirs(MEDIA)

    if not os.path.exists(startuppath):
        localfile = open(startuppath, mode='w+')
        localfile.write('date="01011001"\nversion="0.0"')
        localfile.close()

    if not os.path.exists(idfile):
        localfile = open(idfile, mode='w+')
        localfile.write('id="None"\nname="None"')
        localfile.close()

    # xmlfile = binascii.unhexlify('6164646f6e2e786d6c')
    # addonxml = xbmc.translatePath(os.path.join(ADDONS,AddonID,xmlfile))
    # localaddonversion = open(addonxml, mode='r')
    # content = file.read(localaddonversion)
    # file.close(localaddonversion)
    # localaddonvermatch = re.compile('<ref>(.+?)</ref>').findall(content)
    # addonversion  = localaddonvermatch[0] if (len(localaddonvermatch) > 0) else ''
    # localcheck = hashlib.md5(open(installfile,'rb').read()).hexdigest()
    # if addonversion != localcheck:
      # readfile = open(bakdefault, mode='r')
      # content  = file.read(readfile)
      # file.close(readfile)
    #  writefile = open(installfile, mode='w+')
    #  writefile.write(content)
    #  writefile.close()

    if mode == None : Connectivity_Check()
    if mode == 'ASCII_Check'        : ASCII_Check()
    elif mode == 'addon_final_menu'   : Addon_Final_Menu(url)
    elif mode == 'addon_categories'   : Addon_Categories(url)
    elif mode == 'addon_countries'    : Addon_Countries(url)
    elif mode == 'addon_genres'       : Addon_Genres(url)
    elif mode == 'addon_install'      : Addon_Install(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
    elif mode == 'addon_install_badzip': Addon_Install_BadZip(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
    elif mode == 'addon_install_na'   : Addon_Install_NA(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
    elif mode == 'addon_install_zero' : Addon_Install_Zero(name,zip_link,repo_link,repo_id,addon_id,provider_name,forum,data_path)
    elif mode == 'addon_loop'         : CB_Addon_Install_Loop()
    elif mode == 'addon_removal_menu' : Addon_Removal_Menu()
    elif mode == 'addonmenu'          : Addon_Menu(url)
    elif mode == 'addon_settings'     : Addon_Settings()
    elif mode == 'advanced_tools'     : Tools_Advanced()
    elif mode == 'backup'             : BACKUP()
    elif mode == 'backup_option'      : Backup_Option()
    elif mode == 'backup_restore'     : Backup_Restore()
    elif mode == 'browse_repos'       : Browse_Repos()
    elif mode == 'cb_test_loop'       : CB_Addon_Install_Loop()
    elif mode == 'CB_Menu'            : CB_Menu(url)
    elif mode == 'check_storage'      : checkPath.check(direct)
    elif mode == 'check_updates'      : Addon_Check_Updates()
    elif mode == 'clear_cache'        : Clear_Cache()
    elif mode == 'create_keyword'     : Create_Addon_Pack()
    elif mode == 'community'          : CB_Root_Menu(url)
    elif mode == 'community_backup'   : Community_Backup()
    elif mode == 'community_backup_2' : Community_Backup_OLD()
    elif mode == 'community_menu'     : Community_Menu(url,video)        
    elif mode == 'countries'          : Countries(url)
    elif mode == 'description'        : Description(name,url,buildname,author,version,description,updated,skins,videoaddons,audioaddons,programaddons,pictureaddons,sources,adult)
    elif mode == 'delete_path'        : Delete_Path(url)
    elif mode == 'delete_profile'     : Delete_Profile_Menu(url)
    elif mode == 'exec_xbmc'          : Exec_XBMC(url)
    elif mode == 'fix_special'        : Fix_Special(url)
    elif mode == 'full_backup'        : Full_Backup()
    elif mode == 'full_clean'         : Full_Clean()
    elif mode == 'genres'             : Genres(url)
    elif mode == 'gotham'             : Gotham_Confirm()
    elif mode == 'grab_addons'        : Grab_Addons(url)
    elif mode == 'grab_builds'        : Grab_Builds(url)
    elif mode == 'grab_builds_premium': Grab_Builds_Premium(url)
    elif mode == 'grab_hardware'      : Grab_Hardware(url)
    elif mode == 'grab_news'          : Grab_News(url)
    elif mode == 'grab_tutorials'     : Grab_Tutorials(url)
    elif mode == 'grab_updates'       : xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/checknews.py)')
    elif mode == 'guisettingsfix'     : GUI_Settings_Fix(url,local)
    elif mode == 'hardware_filter_menu': Hardware_Filter_Menu(url)
    elif mode == 'hardware_final_menu': Hardware_Menu(url)        
    elif mode == 'hardware_root_menu' : Hardware_Root_Menu()       
    elif mode == 'helix'              : Helix_Confirm()
    elif mode == 'hide_passwords'     : Hide_Passwords()
    elif mode == 'ipcheck'            : IP_Check()
    elif mode == 'install_venz'       : Install_Venz(url)
    elif mode == 'install_venz_menu'  : Install_Venz_Menu(url)
    elif mode == 'install_content'    : Install_Content(url)
    elif mode == 'install_menu'       : Install_Menu()
    elif mode == 'install_from_zip'   : Install_From_Zip()
    elif mode == 'instructions'       : Instructions()
    elif mode == 'instructions_1'     : Instructions_1()
    elif mode == 'instructions_2'     : Instructions_2()
    elif mode == 'instructions_3'     : Instructions_3()
    elif mode == 'instructions_4'     : Instructions_4()
    elif mode == 'instructions_5'     : Instructions_5()
    elif mode == 'instructions_6'     : Instructions_6()
    elif mode == 'keywords'           : Keyword_Search(url)
    elif mode == 'kill_xbmc'          : KLL()
    elif mode == 'kodi_settings'      : Kodi_Settings()
    elif mode == 'local_backup'       : Local_Backup()
    elif mode == 'LocalGUIDialog'     : Local_GUI_Dialog()
    elif mode == 'log'                : Log_Viewer()
    elif mode == 'main_menu_install'  : Main_Menu_Install(url)
    elif mode == 'manual_search'      : Manual_Search(url)
    elif mode == 'manual_search_builds': Manual_Search_Builds()
    elif mode == 'nan_menu'           : NaN_Menu()
    elif mode == 'news_root_menu'     : News_Root_Menu(url)
    elif mode == 'news_menu'          : News_Menu(url)
    elif mode == 'notify_msg'         : Notify_Check(url)
    elif mode == 'open_system_info'   : Open_System_Info()
    elif mode == 'open_filemanager'   : Open_Filemanager()
    elif mode == 'openelec_backup'    : OpenELEC_Backup()
    elif mode == 'openelec_settings'  : OpenELEC_Settings()
    elif mode == 'openlink'           : Open_Link(url)
    elif mode == 'play_video'         : yt.PlayVideo(url)
    elif mode == 'platform_menu'      : Platform_Menu(url)
    elif mode == 'pop'                : pop(url)
    elif mode == 'register'           : Register()
    elif mode == 'remove_addon_data'  : Remove_Addon_Data()
    elif mode == 'remove_addons'      : Remove_Addons(url)
    elif mode == 'remove_build'       : Remove_Build()
    elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
    elif mode == 'remove_packages'    : Remove_Packages()
    elif mode == 'remove_textures'    : Remove_Textures_Dialog()
    elif mode == 'restore'            : RESTORE()
    elif mode == 'restore_backup'     : Restore_Backup_XML(name,url,description)
    elif mode == 'restore_community'  : Restore_Community(name,url,video,description,skins,guisettingslink,artpack)        
    elif mode == 'restore_local_CB'   : Restore_Local_Community(url)
    elif mode == 'restore_local_gui'  : Restore_Local_GUI()
    elif mode == 'restore_local_OE'   : Restore_OpenELEC_Local()
    elif mode == 'restore_openelec'   : Restore_OpenELEC(name,url,video)
    elif mode == 'restore_option'     : Restore_Option()
    elif mode == 'restore_zip'        : Restore_Zip_File(url)         
    elif mode == 'run_addon'          : Run_Addon(url)
    elif mode == 'runtest'            : speedtest.runtest(url)
    elif mode == 'search_addons'      : Search_Addons(url)
    elif mode == 'search_builds'      : Search_Builds(url)
    elif mode == 'search_content'     : Search_Content(url)
    elif mode == 'search_content_main': Search_Content_Main(url)
    elif mode == 'search_content_sub' : Search_Content('add_sub')
    elif mode == 'Search_Private'     : Private_Search(url)
    elif mode == 'showinfo'           : Show_Info(url)
    elif mode == 'showinfo2'          : Show_Info2(url)
    elif mode == 'social_menu'        : Social_Menu()
    elif mode == 'SortBy'             : Sort_By(BuildURL,type)
    elif mode == 'speed_instructions' : Speed_Instructions()
    elif mode == 'speedtest_menu'     : Speed_Test_Menu()
    elif mode == 'startup_wizard'     : xbmc.executebuiltin('RunAddon(script.openwindow)')
    elif mode == 'testoff'            : Test_Off()
    elif mode == 'switch_profile_menu': Switch_Profile_Menu(url)
    elif mode == 'switch_profile'     : Switch_Profile(url)
    elif mode == 'text_guide'         : Text_Guide(url)
    elif mode == 'tools'              : Tools()
    elif mode == 'tutorial_final_menu': Tutorial_Menu(url)        
    elif mode == 'tutorial_addon_menu': Tutorials_Addon_Menu(url)        
    elif mode == 'tutorial_root_menu' : Tutorial_Root_Menu()        
    elif mode == 'unhide_passwords'   : Unhide_Passwords()
    elif mode == 'update'             : Update_Repo()
    elif mode == 'update_community'   : Update_Community(name,url,video,description,skins,guisettingslink,artpack)        
    elif mode == 'uploadlog'          : Upload_Log()
    elif mode == 'user_info'          : Show_User_Info()
    elif mode == 'xbmc_menu'          : XBMC_Menu(url)
    elif mode == 'xbmcversion'        : XBMC_Version(url)
    elif mode == 'wipe_xbmc'          : Wipe_Kodi(mode)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))