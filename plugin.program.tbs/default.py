import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, time, xbmcvfs, glob, shutil, datetime, zipfile
import subprocess, threading
import yt, downloader, SF, clean, TXT, kll
import binascii
import hashlib
import speedtest
import extract
import pyxbmct

try:
    from sqlite3 import dbapi2 as database

except:
    from pysqlite2 import dbapi2 as database

AddonID          =  'plugin.program.tbs'
AddonName        =  'Maintenance'
ADDON            =  xbmcaddon.Addon(id=AddonID)
debug            =  ADDON.getSetting('debug')
USB              =  ADDON.getSetting('zip')
thirdparty       =  ADDON.getSetting('thirdparty')
enable_adult     =  ADDON.getSetting('adult')
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath('special://profile/')
ADDON_DATA       =  os.path.join(USERDATA,'addon_data')
tvguide          =  xbmc.translatePath('special://home/userdata/addon_data/script.trtv/skip.txt')
PLAYLISTS        =  os.path.join(USERDATA,'playlists')
MEDIA            =  os.path.join(HOME,'media')
DATABASE         =  os.path.join(USERDATA,'Database')
THUMBNAILS       =  os.path.join(USERDATA,'Thumbnails')
ADDONS           =  os.path.join(HOME,'addons')
KODI_ADDONS      =  xbmc.translatePath(os.path.join('special://xbmc','addons'))
BRANDART         =  os.path.join(MEDIA, 'branding','Splash.png')
ADDONXMLTEMP     =  os.path.join(ADDONS,AddonID,'resources','addonxml')
SETTINGSXML      =  os.path.join(ADDONS,AddonID,'service.py')
TBSDATA          =  os.path.join(ADDON_DATA,AddonID)
KEYWORD_FILE     =  os.path.join(HOME, 'userdata', 'addon_data', 'script.openwindow', 'keyword')
ARTPATH          =  '' #Enter URL here for artwork
defaulticon      =  os.path.join(ADDONS,AddonID,'icon_menu.png')
FAVS             =  os.path.join(USERDATA,'favourites.xml')
GUI              =  os.path.join(USERDATA,'guisettings.xml')
SOURCE           =  os.path.join(USERDATA,'sources.xml')
ADVANCED         =  os.path.join(USERDATA,'advancedsettings.xml')
PROFILES         =  os.path.join(USERDATA,'profiles.xml')
RSS              =  os.path.join(USERDATA,'RssFeeds.xml')
KEYMAPS          =  os.path.join(USERDATA,'keymaps','keyboard.xml')
progresstemp     =  os.path.join(ADDON_DATA,AddonID,'progresstemp')
sleeper          =  os.path.join(ADDONS,AddonID,'resources','tmr')
cookie           =  os.path.join(ADDON_DATA,AddonID,'temp')
ascii_results    =  os.path.join(ADDON_DATA,AddonID,'ascii_results')
ascii_results1   =  os.path.join(ADDON_DATA,AddonID,'ascii_results1')
ascii_results2   =  os.path.join(ADDON_DATA,AddonID,'ascii_results2')
successtxt       =  os.path.join(ADDON_DATA,AddonID,'successtxt.txt')
notifyart        =  os.path.join(ADDONS,AddonID,'resources/')
installfile      =  os.path.join(ADDONS,AddonID,'default.py')
skin             =  xbmc.getSkinDir()
log_path         =  xbmc.translatePath('special://logpath/')
backup_dir       =  '/storage/backup'
restore_dir      =  '/storage/.restore/'
CONFIG           =  '/storage/.config/'
STORAGE          =  '/storage/'
userdatafolder   =  os.path.join(ADDON_DATA,AddonID)
scriptfolder     =  os.path.join(ADDON_DATA,AddonID,'scripts')
packages         =  os.path.join(ADDONS,'packages')
checkicon        =  os.path.join(ADDONS,AddonID,'resources','tick.png')
codename         =  'TotalRevolution'
keywordpath      =  'http://urlshortbot.com/TotalRevolution'
artpath          =  os.path.join(ADDONS,AddonID,'resources')
checkicon        =  os.path.join(artpath,'check.png')
updateicon       =  os.path.join(artpath,'update.png')
unknown_icon     =  os.path.join(artpath,'update.png')
dialog_bg        =  os.path.join(artpath,'background.png')
black            =  os.path.join(artpath,'black.png')
EXCLUDES         =  ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml']
EXCLUDES2        =  ['firstrun','plugin.program.tbs','plugin.program.totalinstaller','addons','addon_data','userdata','sources.xml','favourites.xml','guisettings.xml','CP_Profiles','temp']
max_Bps          =  0.0
downloaded_bytes =  0.0
BACKUP_DIRS      =  ['/storage/.kodi','/storage/.cache','/storage/.config','/storage/.ssh']
xbmc_version     =  xbmc.getInfoLabel("System.BuildVersion")
AddonID2         =  'script.trtv'
#ADDON2           =  xbmcaddon.Addon(id=AddonID2)
dialog           =  xbmcgui.Dialog()
updateurl        =  'http://tlbb.me/updates/update.jpeg'
db_social        =  xbmc.translatePath('special://profile/addon_data/plugin.program.tbs/social.db')
updatedst        =  xbmc.translatePath('special://home/addons/packages/update')
remlist          =  xbmc.translatePath('special://profile/addon_data/plugin.program.tbs/remlist')
pos              =  0
listicon         =  ''
ACTION_NAV_BACK  = 92
ACTION_MOVE_UP   = 3
ACTION_MOVE_DOWN = 4

if os.path.exists(BRANDART):
    FANART = BRANDART
else:
    FANART = os.path.join(ADDONS,AddonID,'fanart.jpg')

if thirdparty == 'true':
    social_shares = 1
else:
    social_shares = 0
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
# Remove a path, whether folder or file it will be deleted
def Remove_Files():
    xbmc.log('### Attempting to Remove Files')
    if os.path.exists(remlist):
        readfile = open(remlist,'r')
        content  = readfile.read().splitlines()
        readfile.close()
        for item in content:
            rempath = xbmc.translatePath('special://home')+item
            if os.path.exists(rempath):
                try:
                    os.remove(rempath)
                    xbmc.log('### Successfully removed file: %s' % rempath)
                except:
                    try:
                        shutil.rmtree(rempath)
                        xbmc.log('### Successfully removed folder: %s' % rempath)
                    except:
                        xbmc.log("### Failed to remove: %s" %rempath)
        os.remove(remlist)
#-----------------------------------------------------------------------------------------------------------------    
# Popup class - thanks to whoever codes the help popup in TVAddons Maintenance for this section. Unfortunately there doesn't appear to be any author details in that code so unable to credit by name.
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
#---------------------------------------------------------------------------------------------------
# Main Directory function - xbmcplugin.addDirectoryItem()
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)
#-----------------------------------------------------------------------------------------------------------------  
# Add a standard directory and grab fanart and iconimage from artpath defined in global variables
def addDir(type,name,url,mode,iconimage = '',fanart = '',video = '',description = ''):
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
def Addon_Check_Updates():
    Update_Repo()
    xbmc.executebuiltin('ActivateWindow(10040,"addons://outdated/",return)')
#---------------------------------------------------------------------------------------------------
# Add-on removal menu
def Addon_Removal_Menu():
    namearray = []
    iconarray = []
    descarray = []
    patharray = []
    finalpath = []

    for file in os.listdir(ADDONS):
        if os.path.isdir(os.path.join(ADDONS,file)) and os.path.exists(os.path.join(ADDONS,file,'addon.xml')):

# Read contents of addon.xml to memory and grab REAL addon id (for those who's folder names differ)
            readfile    = open(os.path.join(ADDONS,file,'addon.xml'), 'r')
            content     = readfile.read()
            readfile.close()
            tempaddonid = re.compile('id="(.+?)"').findall(content)[0]

            Addon       = xbmcaddon.Addon(tempaddonid)
            addontype   = Addon.getAddonInfo('type').replace('xbmc.','')
            name        = Addon.getAddonInfo('name')
            iconimage   = Addon.getAddonInfo('icon')
            description = Addon.getAddonInfo('description')
            filepath    = os.path.join(ADDONS,file)

            namearray.append('[COLOR=gold]%s:[/COLOR]  %s' % (addontype,name))
            iconarray.append(iconimage)
            descarray.append(description)
            patharray.append(filepath)

    finalarray = multiselect('Add-ons To Fully Remove',namearray,iconarray,descarray)
    for item in finalarray:
        newpath = patharray[item]
        newname = namearray[item]
        finalpath.append([newname,newpath])
    if len(finalpath) > 0:
        Remove_Addons(finalpath)
#-----------------------------------------------------------------------------------------------------------------
#Function to open addon settings
def Addon_Settings():
    ADDON.openSettings(sys.argv[0])
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
# Check for the real log path, even makes exceptions for idiots who've left their old kodi logs in their builds
def Log_Check():
    finalfile = 0
    logfilepath = os.listdir(log_path)
    for item in logfilepath:
        if item.endswith('.log') and not item.endswith('.old.log'):
            mylog        = os.path.join(log_path,item)
            lastmodified = os.path.getmtime(mylog)
            if lastmodified > finalfile:
                finalfile = lastmodified
                logfile   = mylog
    
    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()
    return logtext
#-----------------------------------------------------------------------------------------------------------------
# Check for storage location on android
def Android_Path_Check():
    content = Log_Check()
    localstorage  = re.compile('External storage path = (.+?);').findall(content)
    localstorage  = localstorage[0] if (len(localstorage) > 0) else ''
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
# Create backup menu
def Backup_Option():
    addDir('','Backup Addons Only','addons','restore_zip','','','','Back Up Your Addons')
    addDir('','Backup Addon Data Only','addon_data','restore_zip','','','','Back Up Your Addon Userdata')
    addDir('','Backup Guisettings.xml',GUI,'restore_backup','','','','Back Up Your guisettings.xml')
    
    if os.path.exists(FAVS):
        addDir('','Backup Favourites.xml',FAVS,'restore_backup','Backup.png','','','Back Up Your favourites.xml')
    
    if os.path.exists(SOURCE):
        addDir('','Backup Source.xml',SOURCE,'restore_backup','Backup.png','','','Back Up Your sources.xml')
    
    if os.path.exists(ADVANCED):
        addDir('','Backup Advancedsettings.xml',ADVANCED,'restore_backup','Backup.png','','','Back Up Your advancedsettings.xml')
    
    if os.path.exists(KEYMAPS):
        addDir('','Backup Advancedsettings.xml',KEYMAPS,'restore_backup','Backup.png','','','Back Up Your keyboard.xml')
    
    if os.path.exists(RSS):
        addDir('','Backup RssFeeds.xml',RSS,'restore_backup','Backup.png','','','Back Up Your RssFeeds.xml')
#---------------------------------------------------------------------------------------------------
# Backup/Restore root menu
def Backup_Restore():
    addDir('folder','Backup My Content','none','backup_option','Backup.png','','','')
    addDir('folder','Restore My Content','none','restore_option','Restore.png','','','')
#---------------------------------------------------------------------------------------------------
# Browse pre-installed repo's via the kodi add-on browser
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
# Main category list
def Categories():
    if OpenELEC_Check():
        addDir('','[COLOR=darkcyan]Wi-Fi Settings[/COLOR]','', 'openelec_settings', 'Wi-Fi.png','','','')

    addDir('folder','[COLOR=dodgerblue]Social TV[/COLOR]','', 'social_menu', '','','','')
    addDir('folder','Install Content','','install_content', 'Search_Addons.png','','','')
    addDir('','Startup Wizard','','startup_wizard', 'Startup_Wizard.png','','','')
    addDir('folder','Maintenance','none', 'tools', 'Additional_Tools.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Function to check the download path set in settings
def Check_Download_Path():
    path = os.path.join(USB,'testCBFolder')
    
    if not os.path.exists(USB):
        dialog.ok('Download/Storage Path Check','The download location you have stored does not exist .\nPlease update the addon settings and try again.') 
        ADDON.openSettings(sys.argv[0])
#---------------------------------------------------------------------------------------------------
# Split string into arrays
def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]
#---------------------------------------------------------------------------------------------------
# Attempt to wipe the cache folder and purge addons*.db
def Clean_Addons():
    tempdir = xbmc.translatePath('special://temp')
    try:
        shutil.rmtree(tempdir)
    except:
        for item in os.listdir(tempdir):
            path = os.path.join(tempdir, item)
            try:
                os.remove(path)
            except:
                try:
                    shutil.rmtree(path)
                except:
                    xbmc.log('#### Failed to remove: %s' % path)
#---------------------------------------------------------------------------------------------------
# Function to clean HTML into plain text. Not perfect but it's better than raw html code!
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
# THIS IS A WIP, NOWHERE NEAR COMPLETE - JUST A PLACEHOLDER FOR THE REAL CODE
def Cleanup_Old_Addons(addon_ids):
    path           = xbmc.translatePath('special://home/userdata/Database')
    files          = glob.glob(os.path.join(path, 'Addons*.db'))
    ver            = 0
    dbPath         = ''

# Find the highest version number of database
    for file in files:
        dbversion = int(re.compile('Addons(.+?).db').findall(file)[0])
        if ver < dbversion:
            ver     = dbversion
            dbPath  = file

    db   = xbmc.translatePath(dbPath)
    conn = database.connect(db, timeout = 10, detect_types=database.PARSE_DECLTYPES, check_same_thread = False)
    conn.row_factory = database.Row
    c = conn.cursor()

    for id in addon_ids:
        c.execute("DELETE * FROM addons WHERE addonID = ?", (id,))
        xbmc.log('### Removed %s from addons' % id)

    c.execute("VACUUM")
    conn.commit()
    c.close()
#---------------------------------------------------------------------------------------------------
# Thanks to xunity maintenance tool for this code, this will remove old stale textures not used in past 14 days
def Cleanup_Old_Textures():
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
# Function to clear all known cache files
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Clear All Known Cache?', 'This will clear all known cache files and can help if you\'re encountering kick-outs during playback as well as other random issues. There is no harm in using this.', nolabel='Cancel',yeslabel='Delete')
    
    if choice == 1:
        Wipe_Cache()
        Remove_Textures_Dialog()
#---------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
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
# Function to delete crash logs
def Delete_Logs():  
    for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
         File   = infile
         os.remove(infile)
         dialog = xbmcgui.Dialog()
         dialog.ok("Crash Logs Deleted", "Your old crash logs have now been deleted.")
#-----------------------------------------------------------------------------------------------------------------    
# Function to delete the packages folder
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
            addDir('','[COLOR=darkcyan]DELETE[/COLOR] '+name.replace('_',' '),os.path.join(CP_PROFILE,name),'delete_path','','','','')
#---------------------------------------------------------------------------------------------------
# Function to delete the userdata/addon_data folder
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
# Function to do a full wipe.
def Destroy_Path(path):
    dp.create("Cleaning Path","Wiping...",'', 'Please Wait')
    shutil.rmtree(path, ignore_errors=True)
#---------------------------------------------------------------------------------------------------
# Enables/disables the social sharing
def Enable_Shares(mode):
    choice = 1
    if mode == 'true':
        if not dialog.yesno('SOCIAL TV SHARES', 'Due to the nature of social shares there is no way to guarantee the reliability or legality of any content provided. If you enable this option it\'s your responsibility to check the content provided is legal in your country prior to installing.'):
            choice = 0
    if choice:
        ADDON.setSetting('thirdparty', mode)
        xbmc.executebuiltin('Container.Refresh')
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
# Convert physical paths to special paths
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
# Clean up all known cache files
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

# For more accurate info we need to add a loop to only check folders with cache in the name. Actual wipe does this but getsize does not.
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
            Kill_XBMC()
        else:
            Cleanup_Old_Textures()
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
# Get params and clean up into string or integer
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
# Return mac address, not currently checked on Mac OS
def Get_Mac(protocol):
    cont    = 0
    counter = 0
    mac     = ''
    while mac == '' and counter < 5: 
        if sys.platform == 'win32': 
            mac = ''
            for line in os.popen("ipconfig /all"):
                if protocol == 'wifi':
                    if line.startswith('Wireless LAN adapter Wi'):
                        cont = 1
                    if line.lstrip().startswith('Physical Address') and cont == 1:
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

                else:
                    if line.lstrip().startswith('Physical Address'): 
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif sys.platform == 'darwin': 
            mac = ''
            if protocol == 'wifi':
                for line in os.popen("ifconfig en0 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
                for line in os.popen("ifconfig en1 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif xbmc.getCondVisibility('System.Platform.Android'):
            mac = ''
            if os.path.exists('/sys/class/net/wlan0/address') and protocol == 'wifi':
                readfile = open('/sys/class/net/wlan0/address', mode='r')
            if os.path.exists('/sys/class/net/eth0/address') and protocol != 'wifi':
                readfile = open('/sys/class/net/eth0/address', mode='r')
            mac = readfile.read()
            readfile.close()
            try:
                mac = mac.replace(' ','')
                mac = mac[:17]
            except:
                mac = ''
                counter += 1

        else:
            if protocol == 'wifi':
                for line in os.popen("/sbin/ifconfig"): 
                    if line.find('wlan0') > -1: 
                        mac = line.split()[4]
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
               for line in os.popen("/sbin/ifconfig"): 
                    if line.find('eth0') > -1: 
                        mac = line.split()[4] 
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1
    if mac == '':
        xbmc.log('#### CANNOT FIND MAC DETAILS ON YOUR DEVICE. THIS UNIT CANNOT CURRENTLY BE USED WITH OUR SERVICE')
        mac = 'Unknown'

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
#---------------------------------------------------------------------------------------------------
def Grab_Updates(url, runtype = ''):
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
        if urlparams != 'Unknown':
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
                                if runtype != 'silent':
                                    Notify('Updates Complete','No more updates to show','1000',os.path.join(ADDONS,'plugin.program.tbs','resources','tick.png'))
    #                            if not multi:
    #                                xbmc.executebuiltin( 'Container.Refresh' )
                                xbmc.executebuiltin( 'UpdateLocalAddons' )
                                xbmc.executebuiltin( 'UpdateAddonRepos' )
                                mysuccess = 1
                except Exception as e:
                    xbmc.log("### Failed with update command: "+str(e))
                    failed = 1
            try:
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            except:
                pass

            if changetimer == 1:
                xbmc.executebuiltin('StopScript(special://home/addons/plugin.program.tbs/service.py)')
                xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.tbs/service.py)')
        try:
            xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
        except:
            xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/functions.py)')
        Remove_Files()
#---------------------------------------------------------------------------------------------------
#function to grab system info
def URL_Params():
    try:
        wifimac = Get_Mac('wifi').rstrip().lstrip()
    except:
        wifimac = 'Unknown'
    try:
        ethmac  = Get_Mac('eth0').rstrip().lstrip()
    except:
        ethmac  = 'Unknown'
    try:
        cpu     = CPU_Check().rstrip().lstrip()
    except:
        cpu     = 'Unknown'
    try:
        build   = Build_Info().rstrip().lstrip()
    except:
        build   = 'Unknown'

    if ethmac == 'Unknown' and wifimac != 'Unknown':
        ethmac = wifimac
    if ethmac != 'Unknown' and wifimac == 'Unknown':
        wifimac = ethmac

    if ethmac != 'Unknown' and wifimac != 'Unknown':
        return (wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20')
        xbmc.log('### maintenance: '+(wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20'))
    else:
        return 'Unknown'
        xbmc.log("### BUILD:"+build)
#---------------------------------------------------------------------------------------------------
#Function to populate the search based on the initial first filter
def Install_Menu():
    key = SEARCH('Enter Key Phrase To Search For')
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    urlparams  = URL_Params()
    if urlparams != 'Unknown':
#    buildsURL  = 'http://tlbb.me/catmenu.php?x='+encryptme('e',urlparams)
        buildsURL  = 'http://tlbb.me/boxer/catsearch_tlbb.php?search='+encryptme('e',urlparams)+'&k='+encryptme('e',key)
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
                addDir('folder',name,url,'install_venz','','','','')
        except:
            Notify('No Response from server','Sorry Please try later','1000',os.path.join(ADDONS,'plugin.program.tbs','resources','cross.png'))     
            xbmc.executebuiltin("Dialog.Close(busydialog)")
    else:
        dialog.ok('FAULT DETECTED', 'It was not possible to obtain your MAC address details, please check your wifi and ethernet modules are enabled.')
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
            addDir('',name,link,'openlink',thumb,'','',desc)
#---------------------------------------------------------------------------------------------------
# Function to execute a command
def Exec_XBMC(command):
    xbmc.executebuiltin(command)
    xbmc.executebuiltin('Container.Refresh')
#---------------------------------------------------------------------------------------------------
# Function to enable/disable the main menu items - added due to glitch on server
def Main_Menu_Install(menumode):
    xbmc.log('MENU MODE: %s' % menumode)
    if menumode == 'add':
        if xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)'):
            addDir('','Enable Comedy','Skin.SetString(Custom6HomeItem.Disable,)','exec_xbmc','https://i.ytimg.com/vi/zZ_mFOG1H-o/maxresdefault.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)'):
            addDir('','Enable Cooking','Skin.SetString(Custom3HomeItem.Disable,)','exec_xbmc','http://videos2.healthination.com/HN_BB_05_EasyCooking_ProRes_739/HN_BB_05_EasyCooking_ProRes_739-img_1280x720.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)'):
            addDir('','Enable Fitness','Skin.SetString(Custom4HomeItem.Disable,)','exec_xbmc','http://www.fourseasons.com/content/dam/fourseasons/images/web/VGS/VGS_342_aspect16x9.jpg/jcr:content/renditions/cq5dam.web.1280.1280.jpeg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)'):
            addDir('','Enable Gaming','Skin.SetString(Custom5HomeItem.Disable,)','exec_xbmc','https://cdn2.vox-cdn.com/thumbor/ez8SzxLVWcfCqRlgOdfWsh6lfRc=/0x0:1920x1080/1280x720/cdn0.vox-cdn.com/uploads/chorus_image/image/47030516/youtube-gaming-end-screen_1920.0.0.png','','','')
        if xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)'):
            addDir('','Enable Kids','Skin.SetString(FavoritesHomeItem.Disable,)','exec_xbmc','http://b.fastcompany.net/multisite_files/fastcompany/imagecache/1280/poster/2014/04/3029893-poster-p-wearable-kid.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)'):
            addDir('','Enable Live TV','Skin.SetString(LiveTVHomeItem.Disable,)','exec_xbmc','http://www.fci-wardrobes.co.uk/site-assets/import/Presotto/dama-tv-3.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)'):
            addDir('','Enable Movies','Skin.SetString(MovieHomeItem.Disable,)','exec_xbmc','https://i.ytimg.com/vi/mohrB3ZDqu4/maxresdefault.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)'):
            addDir('','Enable Music','Skin.SetString(MusicHomeItem.Disable,)','exec_xbmc','http://cienciaetecnologias.com/wp-content/uploads/2013/07/efeito-mozart-musica-inteligencia.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)'):
            addDir('','Enable News','Skin.SetString(ProgramsHomeItem.Disable,)','exec_xbmc','http://cdn.abclocal.go.com/content/kfsn/images/cms/26184_1280x720.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)'):
            addDir('','Enable Sports','Skin.SetString(VideosHomeItem.Disable,)','exec_xbmc','http://theartmad.com/wp-content/uploads/2015/08/Different-Sports-Wallpaper-4.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)'):
            addDir('','Enable Technology','Skin.SetString(Custom2HomeItem.Disable,)','exec_xbmc','http://hpwallpaperku.com/wp-content/uploads/2016/01/Technology-Wallpaper.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)'):
            addDir('','Enable Travel','Skin.SetString(WeatherHomeItem.Disable,)','exec_xbmc','http://www.travelafghanistan.co.uk/wp-content/uploads/2015/09/jour87ix9aoikm1zpjct.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)'):
            addDir('','Enable TV Shows','Skin.SetString(TVShowHomeItem.Disable,)','exec_xbmc','http://cd8ba0b44a15c10065fd-24461f391e20b7336331d5789078af53.r23.cf1.rackcdn.com/plex.vanillacommunity.com/ipb/monthly_11_2010/post-25236-048502800%201289080759.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)'):
            addDir('','Enable World','Skin.SetString(PicturesHomeItem.Disable,)','exec_xbmc','http://cdn.bulbagarden.net/upload/6/68/PokemonWorldAnime.png','','','')
        if xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)'):
            addDir('','Enable YouTube','Skin.SetString(ShutdownHomeItem.Disable,)','exec_xbmc','https://i.ytimg.com/vi/s5y-4EpmfRQ/maxresdefault.jpg','','','')
        if xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)'):
            addDir('','Enable XXX','Skin.SetString(MusicVideoHomeItem.Disable,)','exec_xbmc','http://celebmafia.com/wp-content/uploads/2015/11/bella-thorne-photoshoot-for-glamour-magazine-mexico-december-2015-_1.jpg','','','')
    if menumode == 'remove':
        if not xbmc.getCondVisibility('Skin.String(Custom6HomeItem.Disable)'):
            addDir('','Disable Comedy','Skin.SetString(Custom6HomeItem.Disable,True)','exec_xbmc','https://i.ytimg.com/vi/zZ_mFOG1H-o/maxresdefault.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom3HomeItem.Disable)'):
            addDir('','Disable Cooking','Skin.SetString(Custom3HomeItem.Disable,True)','exec_xbmc','http://videos2.healthination.com/HN_BB_05_EasyCooking_ProRes_739/HN_BB_05_EasyCooking_ProRes_739-img_1280x720.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom4HomeItem.Disable)'):
            addDir('','Disable Fitness','Skin.SetString(Custom4HomeItem.Disable,True)','exec_xbmc','http://www.fourseasons.com/content/dam/fourseasons/images/web/VGS/VGS_342_aspect16x9.jpg/jcr:content/renditions/cq5dam.web.1280.1280.jpeg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom5HomeItem.Disable)'):
            addDir('','Disable Gaming','Skin.SetString(Custom5HomeItem.Disable,True)','exec_xbmc','https://cdn2.vox-cdn.com/thumbor/ez8SzxLVWcfCqRlgOdfWsh6lfRc=/0x0:1920x1080/1280x720/cdn0.vox-cdn.com/uploads/chorus_image/image/47030516/youtube-gaming-end-screen_1920.0.0.png','','','')
        if not xbmc.getCondVisibility('Skin.String(FavoritesHomeItem.Disable)'):
            addDir('','Disable Kids','Skin.SetString(FavoritesHomeItem.Disable,True)','exec_xbmc','http://b.fastcompany.net/multisite_files/fastcompany/imagecache/1280/poster/2014/04/3029893-poster-p-wearable-kid.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(LiveTVHomeItem.Disable)'):
            addDir('','Disable Live TV','Skin.SetString(LiveTVHomeItem.Disable,True)','exec_xbmc','http://www.fci-wardrobes.co.uk/site-assets/import/Presotto/dama-tv-3.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(MovieHomeItem.Disable)'):
            addDir('','Disable Movies','Skin.SetString(MovieHomeItem.Disable,True)','exec_xbmc','https://i.ytimg.com/vi/mohrB3ZDqu4/maxresdefault.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(MusicHomeItem.Disable)'):
            addDir('','Disable Music','Skin.SetString(MusicHomeItem.Disable,True)','exec_xbmc','http://cienciaetecnologias.com/wp-content/uploads/2013/07/efeito-mozart-musica-inteligencia.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(ProgramsHomeItem.Disable)'):
            addDir('','Disable News','Skin.SetString(ProgramsHomeItem.Disable,True)','exec_xbmc','http://cdn.abclocal.go.com/content/kfsn/images/cms/26184_1280x720.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(VideosHomeItem.Disable)'):
            addDir('','Disable Sports','Skin.SetString(VideosHomeItem.Disable,True)','exec_xbmc','http://theartmad.com/wp-content/uploads/2015/08/Different-Sports-Wallpaper-4.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(Custom2HomeItem.Disable)'):
            addDir('','Disable Technology','Skin.SetString(Custom2HomeItem.Disable,True)','exec_xbmc','http://hpwallpaperku.com/wp-content/uploads/2016/01/Technology-Wallpaper.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(WeatherHomeItem.Disable)'):
            addDir('','Disable Travel','Skin.SetString(WeatherHomeItem.Disable,True)','exec_xbmc','http://www.travelafghanistan.co.uk/wp-content/uploads/2015/09/jour87ix9aoikm1zpjct.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(TVShowHomeItem.Disable)'):
            addDir('','Disable TV Shows','Skin.SetString(TVShowHomeItem.Disable,True)','exec_xbmc','http://cd8ba0b44a15c10065fd-24461f391e20b7336331d5789078af53.r23.cf1.rackcdn.com/plex.vanillacommunity.com/ipb/monthly_11_2010/post-25236-048502800%201289080759.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(PicturesHomeItem.Disable)'):
            addDir('','Disable World','Skin.SetString(PicturesHomeItem.Disable,True)','exec_xbmc','http://cdn.bulbagarden.net/upload/6/68/PokemonWorldAnime.png','','','')
        if not xbmc.getCondVisibility('Skin.String(ShutdownHomeItem.Disable)'):
            addDir('','Disable YouTube','Skin.SetString(ShutdownHomeItem.Disable,True)','exec_xbmc','https://i.ytimg.com/vi/s5y-4EpmfRQ/maxresdefault.jpg','','','')
        if not xbmc.getCondVisibility('Skin.String(MusicVideoHomeItem.Disable)'):
            addDir('','Disable XXX','Skin.SetString(MusicVideoHomeItem.Disable,True)','exec_xbmc','http://celebmafia.com/wp-content/uploads/2015/11/bella-thorne-photoshoot-for-glamour-magazine-mexico-december-2015-_1.jpg','','','')
#---------------------------------------------------------------------------------------------------
# Function to move a directory to another location, use 1 for clean paramater if you want to remove original source.
def Move_Tree(src,dst,clean):
    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
    if clean == 1:
        try:
            shutil.rmtree(src)
        except:
            pass
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
            Background  = pyxbmct.Image(dialog_bg, aspectRatio=0) # set aspect ratio to stretch
            Background.setImage(dialog_bg)
            self.listing = pyxbmct.List(_imageWidth=15)
            self.placeControl(Background, 0, 0, rowspan=20, columnspan=20)
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
# Function to grab the main sub-categories 
def Install_Venz_Menu(function):
    menutype    = ''
    menu        = ''
    if '||' in function:
        function,menutype,menu = function.split('||')
    menu = menu.replace('_',' ').lower()

    urlparams  = URL_Params()
    if urlparams != 'Unknown':
        try:

# Inititalise the arrays for sending to multi-select window
            contentarray = []
            imagearray   = []
            descarray    = []
            contenturl   = []

# Add an item to one of the main menu categories or add a sub-menu item
            if menutype == 'add_main' or menutype == 'add_sub' or function.startswith('manualsearch'):
                categoryURL  = 'http://tlbb.me/boxer/category_search.php?&x=%s' % (encryptme('e','%s&%s&0&%s' % (urlparams, function, social_shares)))
                if debug == 'true':
                    xbmc.log(categoryURL)
                link_orig  = Open_URL2(categoryURL)
                link       = encryptme('d',link_orig)
                if debug == 'true':
                    xbmc.log('#### '+encryptme('d',link_orig))
            
                match  = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"', re.DOTALL).findall(link)
                for name, thumb, desc in match:
                    contentarray.append(name)
                    imagearray.append(thumb)
                    descarray.append(desc)

                if len(contentarray)>0:
                    choices = multiselect('Please select the categories you would like to install', contentarray, imagearray, descarray)
                    xbmc.log('Choices: %s' % choices)
                    if len(choices) > 0:
                        Install_Shares(function, menutype, menu, choices, contentarray, imagearray, descarray)
                else:
                    if thirdparty == 'true':
                        dialog.ok('NO CONTENT AVAILABLE','Sorry there\'s currently no new content available for this category.')
                    else:
                        dialog.ok('NO CONTENT AVAILABLE','Sorry there\'s currently no new content available for this category. If you\'re looking for community social shares you need to enable that feature first via Maintenance>Setup Wizard>Social Shares.')


# If this is a remove item
            else:
                Remove_Menu(function)
        except:
            Notify('No Response from server','Sorry Please try later','1000',os.path.join(ADDONS,'plugin.program.tbs','resources','cross.png'))
    else:
        dialog.ok('FAULT DETECTED', 'It was not possible to obtain your MAC address details, please check your wifi and ethernet modules are enabled.')    
#---------------------------------------------------------------------------------------------------
# Remove an item from the system
def Remove_Menu(function, menutype = ''):
    contentarray = []
    imagearray   = []
    descarray    = []
    contenturl   = []
    urlparams = URL_Params()
    if debug == 'true':
        xbmc.log('http://tlbb.me/boxer/category_search.php?&x=%s' % (encryptme('e','%s&%s&0&%s&%s' % (urlparams, function, social_shares, menutype))))
    sharelist_URL  = 'http://tlbb.me/boxer/category_search.php?&x=%s' % (encryptme('e','%s&%s&0&%s&%s' % (urlparams, function, social_shares, menutype)))
    content_list   = Open_URL2(sharelist_URL)
    clean_link     = encryptme('d',content_list)
    if debug == 'true':
        xbmc.log('#### RETURN: %s' % clean_link)
# Grab all the shares which match the master sub-category
    match = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(clean_link)
    for name, thumb, desc, link in match:
        contentarray.append(name)
        imagearray.append(thumb)
        descarray.append(desc)
        contenturl.append(link)

# Return the results and update
    if len(contentarray) > 0:
        if menutype == '':
            choices = multiselect('Select from the list below',contentarray,imagearray,descarray)
            if len(choices) > 0:
                Notify('Removing Content','Please be patient during this process','5000',os.path.join(ADDONS,'plugin.program.tbs','resources','update.png'))
                xbmc.executebuiltin('ActivateWindow(HOME)')
                for item in choices:
                    Open_URL2(contenturl[item])
        else:
            for item in contenturl:
                xbmc.log('### URL TO REMOVE: %s' % item)
                Open_URL2(item)

        Grab_Updates('http://tlbb.me/comm.php?multi&z=c&x=')
    elif menutype == '':
        dialog.ok('NOTHING TO REMOVE','You currently have no items installed on the system, please try adding shares.')
#---------------------------------------------------------------------------------------------------
# Show final results for installing (if multiple shares of same name order by popularity)
def Install_Shares(function, menutype, menu, choices, contentarray = '', imagearray = '', descarray = ''):
        shares_contentarray = []
        shares_imagearray   = []
        shares_descarray    = []
        shares_contenturl   = []
        urlparams           = URL_Params()

#    try:
        for item in choices:
            xbmc.log('CHOICE: %s' % item)
            if debug == 'true':
                xbmc.log('http://tlbb.me/boxer/category_search.php?&x=%s' % (encryptme('e','%s&%s&1&%s&%s' % (urlparams, function, social_shares, contentarray[item]))))
            sharelist_URL  = 'http://tlbb.me/boxer/category_search.php?&x=%s' % (encryptme('e','%s&%s&1&%s&%s' % (urlparams, function, social_shares, contentarray[item])))
            content_list   = Open_URL2(sharelist_URL)
            clean_link     = encryptme('d',content_list)
            if debug == 'true':
                xbmc.log('#### %s' % clean_link)

# Grab all the shares which match the master sub-category
            match = re.compile('n="(.+?)"t="(.+?)"d="(.+?)"l="(.+?)"', re.DOTALL).findall(clean_link)
            for name, thumb, desc, link in match:
                shares_contentarray.append(name)
                shares_imagearray.append(thumb)
                shares_descarray.append(desc)
                shares_contenturl.append(link)

# If we have more than one item in the list we present them so the user can select which one they want installed
            if len(shares_contentarray) > 1:
                choice = dialog.select('Select share for [COLOR=dodgerblue]%s[/COLOR]' % contentarray[item].replace('ADD ',''), shares_contentarray)
                install_share = shares_contenturl[choice]

            else:
                install_share = shares_contenturl[0]

# Remove any matching menu items previously installed from different boxes
            if len(shares_contentarray)>0:
                for item in shares_contentarray:
                    xbmc.log('### Removing any old instances of %s' % item)
                    if item.startswith('Add'):
                        item         = 'Remove'+item[3:]
                        change_text  = re.compile(' to the (.+?)Menu').findall(item)[0]
                        if change_text.endswith(' '):
                            change_text = change_text[:-1]
                        item         = item.replace(' to the %s' % change_text, '%'+' from the %s' % change_text)
                        if 'by box' in item:
                            change_text2 = re.compile('by box (.+?)from').findall(item)[0]
                            xbmc.log('by box: %s' % change_text2)
                            item         = item.replace(change_text2, '%')
                        Remove_Menu('from_the_%s_menu' % change_text.lower().replace(' ', '_'), item)
#            content_list   = Open_URL2(sharelist_URL)

                Open_URL2(install_share)

# Clean the arrays so they don't show old data
            del shares_contentarray[:]
            del shares_imagearray[:]
            del shares_descarray[:]
            del shares_contenturl[:]
            del match[:]
        xbmc.executebuiltin('ActivateWindow(HOME)')
        Grab_Updates('http://tlbb.me/comm.php?multi&z=c&x=')
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
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
        if command=="addons":
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
#-----------------------------------------------------------------------------------------------------------------          
# Hide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
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
# Menu to install content via the TR add-on
def Install_Content(url):
#    addDir('folder','Search For Content','','search_content', 'Search_Addons.png','','','')
    addDir('','[COLOR=dodgerblue]Check For Updates[/COLOR]','http://tlbb.me/comm.php?z=c&x=', 'grab_updates', '','','','')
    addDir('','Install A Keyword', '', 'keywords', 'Keywords.png','','','')
    addDir('','Install From Zip','','install_from_zip','','','','')
    addDir('','Browse My Repositories','','browse_repos','','','','')
#---------------------------------------------------------------------------------------------------
#Browse pre-installed repo's via the kodi add-on browser
def Install_From_Zip():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://install/",return)')
#-----------------------------------------------------------------------------------------------------------------
# Return details about the IP address lookup       
def IP_Check():
    ip_site = ADDON.getSetting('ip_site')
    try:
        if ip_site == "whatismyipaddress.com":
           BaseURL       = 'http://whatismyipaddress.com/'
           link          = Open_URL(BaseURL, 30).replace('\n','').replace('\r','')
           if not 'Access Denied' in link:
               ipmatch       = re.compile('whatismyipaddress.com/ip/(.+?)"').findall(link)
               ipfinal       = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
               details       = re.compile('"font-size:14px;">(.+?)</td>').findall(link)
               provider      = details[0] if (len(details) > 0) else 'Unknown'
               location      = details[2]+', '+details[3]+', '+details[4] if (len(details) > 3) else 'Unknown'
               dialog.ok('www.whatismyipaddress.com',"[B][COLOR gold]Address: [/COLOR][/B] %s" % ipfinal, '[B][COLOR gold]Provider: [/COLOR][/B] %s' % provider, '[B][COLOR gold]Location: [/COLOR][/B] %s' % location)
        else:
            BaseURL       = 'https://www.iplocation.net/find-ip-address'
            link          = Open_URL(BaseURL, 30).replace('\n','').replace('\r','')
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
def Keyword_Search():
    if not os.path.exists(packages):
        os.makedirs(packages)
    counter = 0
    success = 0
    downloadurl = ''
    title       = 'Enter Keyword'
    keyword     = SEARCH(title)
    if keyword == 'teston':
        ADDON.setSetting('debug','true')
        return
    if keyword == 'testoff':
        ADDON.setSetting('debug','false')
        return
    else:
        url='http://urlshortbot.com/venztech'
        if os.path.exists(KEYWORD_FILE):
            url  = Text_File(KEYWORD_FILE,'r')
        downloadurl = url+keyword
        lib         = os.path.join(packages, keyword+'.zip')
        urlparams   = URL_Params()
        if urlparams != 'Unknown':
            dp.create('Contacting Server','Attempt: 1', '', 'Please wait...')
            while counter <3 and success == 0:
                counter += 1
                dp.update(0,'Attempt: '+str(counter), '', 'Please wait...')
            if keyword.startswith('switchme'):
                keywordoem = keyword.replace('switchme','')
                try:
                    link = Open_URL2('http://tlbb.me/boxer/addtooem.php?x='+encryptme('e',urlparams)+'&o='+encryptme('e',keywordoem))
                except:
                    link = 'fail'
            else:
                try:
                    link = Open_URL2('http://tlbb.me/keyword.php?x='+encryptme('e',urlparams)+'k='+encryptme('e',keyword))
                except:
                    link = 'fail'
            if 'Success' in link:
                success = 1
                dp.close()
                xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
                dialog.ok('Keyword Code Success','Congratulations, your Keyword has been accepted.','Please wait for the "working" notification to finish and then click ok to continue. Any changes will have made with immediate effect.')
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
                            dp.update(0,"", "System will now reboot")
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
# Force close Kodi
def Kill_XBMC(wipedb = ''):
    os._exit(1)
#     dbfolder = xbmc.translatePath(os.path.join(USERDATA, 'Database'))
#     if not os.path.exists(scriptfolder):
#         os.makedirs(scriptfolder)
#     xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
#     version=float(xbmc_version[:4])
#     if xbmc.getCondVisibility('system.platform.windows'):
#         if version < 14:
#             try:
#                 writefile = open(os.path.join(scriptfolder,'win_xbmc.bat'), 'w+')
#                 writefile.write('@ECHO off\nTASKKILL /im XBMC.exe /f\ntskill XBMC.exe\nXBMC.exe')
#                 writefile.close()
#                 os.system(os.path.join(scriptfolder,'win_xbmc.bat'))
#             except:
#                 xbmc.log("### Failed to run win_xbmc.bat")
#         else:
#             try:
#                 writefile = open(os.path.join(scriptfolder,'win_kodi.bat'), 'w+')
#                 if wipedb == 'wipe':
#                     writefile.write('@ECHO off\nTASKKILL /im Kodi.exe /f\necho ----------------------------------------------------------\necho IN ORDER TO FULLY CLEANSE YOUR KODI INSTALL YOU NEED TO WIPE YOUR KODI DATABASE FILES.\necho IF YOU\'RE HAPPY TO PROCEED WITH THIS ACTION PRESS "Y" FOLLOWED BY "ENTER".\necho ----------------------------------------------------------\necho DELETE:\ndel %s\nKodi.exe\nclose' % (os.path.join(dbfolder,'*.*')))
#                 else:
#                     writefile.write('@ECHO off\nTASKKILL /im Kodi.exe /f\nKodi.exe\nclose')
#                 writefile.close()
#                 os.system(os.path.join(scriptfolder,'win_kodi.bat'))
#             except:
#                 xbmc.log("### Failed to run win_kodi.bat")
#     elif xbmc.getCondVisibility('system.platform.osx'):
#         if version < 14:
#             try:
#                 writefile = open(os.path.join(scriptfolder,'osx_xbmc.sh'), 'w+')
#                 writefile.write('killall -9 XBMC\nXBMC')
#                 writefile.close()
#             except:
#                 pass
#             try:
#                 os.system('chmod 755 '+os.path.join(scriptfolder,'osx_xbmc.sh'))
#             except:
#                 pass
#             try:
#                 os.system(os.path.join(scriptfolder,'osx_xbmc.sh'))
#             except:
#                 xbmc.log("### Failed to run osx_xbmc.sh")
#         else:
#             try:
#                 writefile = open(os.path.join(scriptfolder,'osx_kodi.sh'), 'w+')
#                 writefile.write('killall -9 Kodi\nKodi')
#                 writefile.close()
#             except:
#                 pass
#             try:
#                 os.system('chmod 755 '+os.path.join(scriptfolder,'osx_kodi.sh'))
#             except:
#                 pass
#             try:
#                 os.system(os.path.join(scriptfolder,'osx_kodi.sh'))
#             except:
#                 xbmc.log("### Failed to run osx_kodi.sh")
# #    else:
#     elif xbmc.getCondVisibility('system.platform.android'):
#         if os.path.exists('/data/data/com.rechild.advancedtaskkiller'):
#             dialog.ok('Attempting to force close','On the following screen please press the big button at the top which says "KILL selected apps". Kodi will restart, please be patient while your system updates the necessary files and your skin will automatically switch once fully updated.')
#             try:
#                 xbmc.executebuiltin('StartAndroidActivity(com.rechild.advancedtaskkiller)')
#             except:
#                 xbmc.log("### Failed to run Advanced Task Killer. Make sure you have it installed, you can download from https://archive.org/download/com.rechild.advancedtaskkiller/com.rechild.advancedtaskkiller.apk")
#         else:
#             dialog.ok('Advanced Task Killer Not Found',"The Advanced Task Killer app cannot be found on this system. Please make sure you actually installed it after downloading. We can't do everything for you - on Android you do have to physically click on the download to install an app.")
#         try:
#             os.system('adb shell am force-stop org.xbmc.kodi')
#         except:
#             pass
#         try:
#             os.system('adb shell am force-stop org.kodi')
#         except:
#             pass
#         try:
#             os.system('adb shell am force-stop org.xbmc.xbmc')
#         except:
#             pass
#         try:
#             os.system('adb shell am force-stop org.xbmc')
#         except:
#             pass
#         try:
#             os.system('adb shell kill org.xbmc.kodi')
#         except:
#             pass
#         try:
#             os.system('adb shell kill org.kodi')
#         except:
#             pass
#         try:
#             os.system('adb shell kill org.xbmc.xbmc')
#         except:
#             pass
#         try:
#             os.system('adb shell kill org.xbmc')
#         except:
#             pass
#         try:
#             os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
#         except:
#             pass
#         try:
#             os.system('Process.killProcess(android.os.Process.org.kodi());')
#         except:
#             pass
#         try:
#             os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
#         except:
#             pass
#         try:
#             os.system('Process.killProcess(android.os.Process.org.xbmc());')
#         except:
#             pass
#     elif xbmc.getCondVisibility('system.platform.linux'):
#         if version < 14:
#             try:
#                 writefile = open(os.path.join(scriptfolder,'linux_xbmc'), 'w+')
#                 writefile.write('killall XBMC\nkillall -9 xbmc.bin\nXBMC')
#                 writefile.close()
#             except:
#                 pass
#             try:
#                 os.system('chmod a+x '+os.path.join(scriptfolder,'linux_xbmc'))
#             except:
#                 pass
#             try:
#                 os.system(os.path.join(scriptfolder,'linux_xbmc'))
#             except:
#                 print "### Failed to run: linux_xbmc"
#         else:
#             try:
#                 writefile = open(os.path.join(scriptfolder,'linux_kodi'), 'w+')
#                 writefile.write('killall Kodi\nkillall -9 kodi.bin\nkodi')
#                 writefile.close()
#             except:
#                 pass
#             try:
#                 os.system('chmod a+x '+os.path.join(scriptfolder,'linux_kodi'))
#             except:
#                 pass
#             try:
#                 os.system(os.path.join(scriptfolder,'linux_kodi'))
#             except:
#                 print "### Failed to run: linux_kodi"
#     else: #ATV and OSMC
#         try:
#             os.system('killall AppleTV')
#         except:
#             pass
#         try:
#             os.system('sudo initctl stop kodi')
#         except:
#             pass
#         try:
#             os.system('sudo initctl stop xbmc')
#         except:
#             pass
#---------------------------------------------------------------------------------------------------
# Open Kodi Settings
def Kodi_Settings():
    xbmc.executebuiltin('ReplaceWindow(settings)')
#---------------------------------------------------------------------------------------------------
# Grab contents of the log
def Grab_Log():
    finalfile = 0
    logfilepath = os.listdir(log_path)
    for item in logfilepath:
        if item.endswith('.log') and not item.endswith('.old.log'):
            mylog        = os.path.join(log_path,item)
            lastmodified = os.path.getmtime(mylog)
            if lastmodified>finalfile:
                finalfile = lastmodified
                logfile   = mylog
    
    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()
    return logtext
#---------------------------------------------------------------------------------------------------
# View the log from within Kodi
def Log_Viewer():
    content = Grab_Log()
    Text_Boxes('Log Viewer', content)
#---------------------------------------------------------------------------------------------------
#Search in description
def Manual_Search(mode):
    vq = Get_Keyboard( heading="Search for content" )
    if ( not vq ):
        return False, 0
    title = urllib.quote_plus(vq)
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
#---------------------------------------------------------------------------------------------------
#Open Kodi File Manager
def Open_SF():
    menu_array = ['COMEDY', 'COOKING', 'FITNESS', 'GAMING', 'KIDS', 'LIVE TV', 'MOVIES', 'MUSIC', 'NEWS', 'SPORTS', 'TECHNOLOGY', 'TRAVEL', 'TV SHOWS', 'WORLD', 'XXX']
    choice = dialog.select('Choose Menu',menu_array)
    choice = menu_array[choice]
    xbmc.executebuiltin('ActivateWindow(programs,"plugin://plugin.program.super.favourites/?folder=HOME_%s",return)' % choice.replace(' ', '_'))
#-----------------------------------------------------------------------------------------------------------------
# Function to open a URL and return the contents
def Open_URL(url, t=''):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    counter = 0
    success = False
    while counter < 5 and success == False: 
        response = urllib2.urlopen(req, timeout = t)
        link     = response.read()
        response.close()
        counter += 1
        if link != '':
            success = True
    if success == True:
        return link.replace('\r','').replace('\n','').replace('\t','')
    else:
        dialog.ok('Unable to contact server','There was a problem trying to access the server, please try again later.')
        return
    return link
#-----------------------------------------------------------------------------------------------------------------
## Function to open a URL, try 3 times then respond with blank
def Open_URL2(url):
    if debug == 'true':
        xbmc.log(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req, timeout = 10)
    if response != '':
        link     = response.read()
        response.close()
        return link.replace('\r','').replace('\n','').replace('\t','')
    else:
        return response
#---------------------------------------------------------------------------------------------------
# Open URL for updating a social share
def Open_URL_Share(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
        response = urllib2.urlopen(req, timeout = 30)
    except:
        response = 'no response'
    if response != 'no response':
        link     = response.read()
        response.close()
    else:
       link = 'no response'
        
    return link.replace('\r','').replace('\n','').replace('\t','')
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
# Check if system is OE or LE
def OpenELEC_Check():
    content = Grab_Log()
    if 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:
        return True
#---------------------------------------------------------------------------------------------------
def OpenELEC_Settings():
    if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)") or xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"):
        if xbmc.getCondVisibility("System.HasAddon(service.openelec.settings)"): 
            xbmc.executebuiltin('RunAddon(service.openelec.settings)')
        elif xbmc.getCondVisibility("System.HasAddon(service.libreelec.settings)"): 
            xbmc.executebuiltin('RunAddon(service.libreelec.settings)')
        xbmc.sleep(1500)
        xbmc.executebuiltin('Control.SetFocus(1000,2)')
        xbmc.sleep(500)
        xbmc.executebuiltin('Control.SetFocus(1200,0)')
#---------------------------------------------------------------------------------------------------
# Set popup xml based on platform
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
#---------------------------------------------------------------------------------------------------
# Function to clear the addon_data
def Remove_Addon_Data():
    choice = dialog.yesno('DELETE ADD-ON DATA', 'Do you want to remove individual addon_data folders or wipe all addon_data?', yeslabel='EVERYTHING', nolabel='INDIVIDUAL ITEMS')
    
    if choice:
        choice = dialog.yesno('Are you ABSOLUTELY certain?','This will remove ALL your addon_data, there\'s no getting it back! Are you certain you want to continue?')
        if choice:
            Delete_Userdata()
            dialog.ok("Addon_Data Removed", '', 'Your addon_data folder has now been removed.','')
    else:
        namearray = []
        iconarray = []
        descarray = []
        patharray = []
        finalpath = []

        for file in os.listdir(ADDON_DATA):
            if os.path.isdir(os.path.join(ADDON_DATA,file)):
                try:
                    Addon       = xbmcaddon.Addon(file)
                    name        = Addon.getAddonInfo('name')
                    iconimage   = Addon.getAddonInfo('icon')
                    description = Addon.getAddonInfo('description')
                except:
                    name        = 'Unknown Add-on'
                    iconimage   =  unknown_icon
                    description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

            else:
                name        = 'Unknown Add-on'
                iconimage   =  unknown_icon
                description = 'No add-on has been found on your system that matches this ID. The most likely scenario for this is you\'ve previously uninstalled this add-on and left the old addon_data on the system.'

            filepath    = os.path.join(ADDON_DATA,file)
            namearray.append('%s [COLOR=gold](%s)[/COLOR]' % (file,name))
            iconarray.append(iconimage)
            descarray.append(description)
            patharray.append(filepath)

        finalarray = multiselect('Addon_Data To Remove',namearray,iconarray,descarray)
        for item in finalarray:
            newpath = patharray[item]
            newname = namearray[item]
            finalpath.append([newname,newpath])
        xbmc.log('FINAL: %s' % finalpath)
        if len(finalpath) > 0:
            Remove_Addons(finalpath)
#---------------------------------------------------------------------------------------------------
# Function to remove a list of addons including addon_data
def Remove_Addons(url):
    removed = 0
    for item in url:
        data_path = item[1].replace(ADDONS,ADDON_DATA)
        if 'addon_data' in item[1]:
            addontype = 'Addon_Data'
        else:
            addontype = 'Addon'
        if dialog.yesno("Remove %s" % addontype, "Do you want to Remove:",'[COLOR=dodgerblue]%s[/COLOR]'%item[0]):
            if not 'addon_data' in item[1]:
                removed = 1
            for root, dirs, files in os.walk(item[1]):
                
                for f in files:
                    os.unlink(os.path.join(root, f))
                
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            os.rmdir(item[1])
            if not 'addon_data' in item[1]:
                if dialog.yesno('Remove Addon_Data?','Would you also like to remove the addon_data associated with this add-on? This contains your add-on settings and can contain personal information such as username/password.'):
                    try:
                        for root, dirs, files in os.walk(data_path):
                            for f in files:
                                os.unlink(os.path.join(root, f))
                            for d in dirs:
                                shutil.rmtree(os.path.join(root, d))
                        os.rmdir(data_path)
                    except:
                        pass
    if removed:
        xbmc.executebuiltin( 'UpdateLocalAddons' )
        xbmc.executebuiltin( 'UpdateAddonRepos' )
        Remove_Packages('nodialog')
        Clean_Addons()
# Need to create function to wipe relevant bits from db
#        Cleanup_Old_Addons()
        dialog.ok('REMOVAL COMPLETE','The addons database file now needs purging, to do so we need to restart. If prompted please agree to the deletion otherwise your add-ons may still appear in Kodi even if they don\'t physically exist.')
        Kill_XBMC('wipe')
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Crash_Logs():
    if dialog.yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are log files generated when Kodi crashes and are only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete'):
        Delete_Logs()
        dialog.ok("Crash Logs Removed", '', 'Your crash log files have now been removed.','')
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Packages(url=''):
    if dialog.yesno('Delete Packages Folder', 'Do you wipe the packages folder? This will delete your old zip install files that are no longer in use. This will disable the ability to rollback but causes no harm', nolabel='Cancel',yeslabel='Delete'):
        Delete_Packages()
    if url == '':
        dialog.ok("Packages Removed", '', 'Your zip install files have now been removed.','')
#---------------------------------------------------------------------------------------------------
# Function to clear the packages folder
def Remove_Textures_Dialog():
    if dialog.yesno('Clear Cached Images?', 'This will clear your textures13.db file and remove your Thumbnails folder. These will automatically be repopulated after a restart.', nolabel='Cancel',yeslabel='Delete'):
        Remove_Textures()
        Destroy_Path(THUMBNAILS)
        
        if dialog.yesno('Quit Kodi Now?', 'Cache has been successfully deleted.', 'You must now restart Kodi, would you like to quit now?','', nolabel='I\'ll restart later',yeslabel='Yes, quit'):
            try:
                xbmc.executebuiltin("RestartApp")
            except:
                Kill_XBMC()
#---------------------------------------------------------------------------------------------------
# Function to remove textures13.db
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
# Function to restore a backup xml file (guisettings, sources, RSS)
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
# Function to restore a backup xml file (guisettings, sources, RSS)
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
# Create restore menu
def Restore_Option():
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        addDir('','Restore Your Addons','addons','restore_zip','Restore.png','','','Restore Your Addons')

    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir('','Restore Your Addon UserData','addon_data','restore_zip','Restore.png','','','Restore Your Addon UserData')           

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('','Restore Guisettings.xml',GUI,'resore_backup','Restore.png','','','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('','Restore Favourites.xml',FAVS,'resore_backup','Restore.png','','','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('','Restore Source.xml',SOURCE,'resore_backup','Restore.png','','','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('','Restore Advancedsettings.xml',ADVANCED,'resore_backup','Restore.png','','','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('','Restore Advancedsettings.xml',KEYMAPS,'resore_backup','Restore.png','','','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('','Restore RssFeeds.xml',RSS,'resore_backup','Restore.png','','','Restore Your RssFeeds.xml')    
#---------------------------------------------------------------------------------------------------
# Function to restore a previously backed up zip, this includes full backup, addons or addon_data.zip
def Restore_Zip_File(url):
    Check_Download_Path()
    if 'addons' in url:
        ZIPFILE    = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR        = ADDONS

    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

    if 'Backup' in url:
        Delete_Packages() 
        dp.create("Creating Backup","Backing Up",'', 'Please Wait')
        zipobj       = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen      = len(DIR)
        for_progress = []
        ITEM         = []

        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM = len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
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
        xbmc.sleep(500)
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")        

        if 'Backup' in url:
            dialog.ok("Install Complete", 'Kodi will now close. Just re-open Kodi and wait for all the updates to complete.')
            Kill_XBMC()

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
# Main search menu for Venz content
def Search_Content_Main(type):
    xbmc.log(type)
    if 'from_the' in type and '_menu' in type:
        Install_Venz_Menu(type+'||remove_main||'+type.replace('from_the_','').replace('_menu',''))
    elif type == 'main_menu':
        Install_Venz_Menu(type)
    elif not 'from_the' in type and type != 'main_menu' and not "submenu" in type:
        addDir('folder','Add to '+type.replace('_',' ')+' - [COLOR=dodgerblue]Browse All[/COLOR]','to_the_'+type+'_menu||add_main||'+type,'install_venz_menu','','','','')
        addDir('folder','Add to '+type.replace('_',' ')+' - [COLOR=dodgerblue]Search For Specific Shares[/COLOR]','to_the_'+type+'_menu||add_main||'+type,'search_content','Manual_Search.png','','','')
    elif "submenu" in type:
        addDir('folder','Add to '+type.replace('_submenu','').replace('_',' ').title()+' Sub-menu','to_the_'+type+'||add_sub||'+type.replace('_submenu',''),'install_venz_menu','','','','')
        addDir('folder','Remove from '+type.replace('_submenu','').replace('_',' ').title()+' Sub-menu','from_the_'+type+'||remove_sub||'+type.replace('_submenu',''),'install_venz_menu','','','','')   
#-----------------------------------------------------------------------------------------------------------------
# Search for Venz content
def Search_Content(menutype):
    vq = Get_Keyboard(heading='Type The Channel Name')
# if blank or the user cancelled the keyboard, return
    if ( not vq ): return False, 0

# we need to set the title to our query
    title = urllib.quote_plus(vq)
    Install_Venz_Menu('manualsearch'+title+'>>#'+menutype)
#---------------------------------------------------------------------------------------------------
def SetNone():
    urlparams = URL_Params()
    link = Open_URL(encryptme('d','6773736f392e2e736b61612d6c642e7264736d6e6d642d6f676f3e773c011510030A')+encryptme('e',urlparams))
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
def RMT():
    Remove_Textures()
    Wipe_Cache()
#---------------------------------------------------------------------------------------------------
# Function to pull commands and update
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
# Social TV Menu
def Social_Menu():
    if thirdparty == 'true':
        addDir('','Social Shares Status: [COLOR=lime]ENABLED[/COLOR]','false', 'enable_shares', '','','','')
    else:
        addDir('','Social Shares Status: [COLOR=red]DISABLED[/COLOR]','true', 'enable_shares', '','','','')
    addDir('','[COLOR=dodgerblue]Check For Updates[/COLOR]','http://tlbb.me/comm.php?z=c&x=', 'grab_updates', '','','','')
    addDir('','My Share Folders (Create/Share Menus)','', 'open_sf', '','','','')
    addDir('','Update My Online Shares','manual', 'check_shares', '','','','')
#    addDir('','[COLOR=grey]Friend Requests (Coming Soon)[/COLOR]', '', '', '','','','')
#    addDir('','[COLOR=grey]My Content (Coming Soon)[/COLOR]', '', '', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Instructions for the speed test
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
    addDir('','[COLOR=blue]Instructions - Read me first[/COLOR]', 'none', 'speed_instructions', 'howto.png','','','')
    addDir('','Download 16MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/16MB.txt', 'runtest', 'Download16.png','','','')
    addDir('','Download 32MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/32MB.txt', 'runtest', 'Download32.png','','','')
    addDir('','Download 64MB file   - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/64MB.txt', 'runtest', 'Download64.png','','','')
    addDir('','Download 128MB file - [COLOR=lime]Server 1[/COLOR]', 'https://totalrevolution.googlecode.com/svn/trunk/download%20files/128MB.txt', 'runtest', 'Download128.png','','','')
    addDir('','Download 10MB file   - [COLOR=darkcyan]Server 2[/COLOR]', 'http://www.wswd.net/testdownloadfiles/10MB.zip', 'runtest', 'Download10.png','','','')
#-----------------------------------------------------------------------------------------------------------------
# Show full description of build
def Test_Off():
    ADDON.setSetting('debug','false')
    xbmc.executebuiltin('Container.Refresh')
#-----------------------------------------------------------------------------------------------------------------
# Create a standard text box
def Text_Boxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try:
        f=open(anounce); text=f.read()
      except:
        text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  while xbmc.getCondVisibility('Window.IsVisible(10147)'):
      xbmc.sleep(500)

# Need to optimise the above, all that's really required is this:

# xbmc.executebuiltin("ActivateWindow(10147)")
# controller = xbmcgui.Window(10147)
# xbmc.sleep(500)
# controller.getControl(1).setLabel('TEST HEADER')
# controller.getControl(5).setText('TEST TEXT')
#-----------------------------------------------------------------------------
# Read or write to a file
def Text_File(path, mode, text = ''):
    textfile = open(path, mode)
    if mode == 'r':
        content  = textfile.read()
        textfile.close()
        return content
    if mode == 'w':
        textfile.write(text)
        textfile.close()
#-----------------------------------------------------------------------------------------------------------------
# Show full description of build
def Text_Guide(url):
    try:
        heading,text = url.split('|')
        Text_Boxes(heading, text)
    except:
        Text_Boxes('', url)
#---------------------------------------------------------------------------------------------------
# Get current timestamp in integer format
def Timestamp():
    now = time.time()
    localtime = time.localtime(now)
    return time.strftime('%Y%m%d%H%M%S', localtime)
#-----------------------------------------------------------------------------------------------------------------
# Maintenance section
def Tools():
    addDir('folder','Add-on Tools','none','tools_addons','','','','')
    addDir('folder','Backup/Restore','none','backup_restore','','','','')
    addDir('folder','Clean up my Kodi', '', 'tools_clean', '','','','')
    addDir('folder','Misc. Tools', '', 'tools_misc', '','','','')
    if OpenELEC_Check():
        addDir('','[COLOR=dodgerblue]Wi-Fi / OpenELEC Settings[/COLOR]','', 'openelec_settings', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Add-on based tools
def Tools_Addons():
    addDir('','Completely Remove An Add-on (inc. passwords)','plugin','addon_removal_menu', '','','','')
    addDir('','Delete Addon Data','url','remove_addon_data','','','','')
    addDir('','Make Old Add-ons Compatible','none','gotham', '','','','')
    addDir('','Passwords - Hide when typing in','none','hide_passwords', '','','','')
    addDir('','Passwords - Unhide when typing in','none','unhide_passwords', '','','','')
    addDir('','Update My Add-ons (Force Refresh)', 'none', 'update', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Clean Tools
def Tools_Clean():
    addDir('','[COLOR=gold]CLEAN MY KODI FOLDERS (Save Space)[/COLOR]', '', 'full_clean', '','','','')
    addDir('','Clear All Cache Folders','url','clear_cache','','','','')
    addDir('','Clear Cached Artwork (thumbnails & textures)', 'none', 'remove_textures', '','','','')
    addDir('','Clear Packages Folder','url','remove_packages','','','','')
    addDir('','Delete Old Crash Logs','url','remove_crash_logs','','','','')
    addDir('','Wipe My Install (Fresh Start)', '', 'wipe_xbmc', '','','','')
#-----------------------------------------------------------------------------------------------------------------
# Advanced Maintenance section
def Tools_Misc():
    addDir('','Check For Special Characters In Filenames','', 'ASCII_Check', '','','','')
    addDir('','Check My IP Address', 'none', 'ipcheck', '','','','')
    addDir('','Check XBMC/Kodi Version', 'none', 'xbmcversion', '','','','')
    addDir('','Convert Physical Paths To Special',HOME,'fix_special','','','','')
    addDir('','Force Close Kodi','','kill_xbmc','','','','')
    addDir('','Upload Log','none','uploadlog', '','','','')
    addDir('','View My Log','none','log', '','','','')
#-----------------------------------------------------------------------------------------------------------------
#Unhide passwords in addon settings - THANKS TO MIKEY1234 FOR THIS CODE (taken from Xunity Maintenance)
def Unhide_Passwords():
    if dialog.yesno("Make Add-on Passwords Visible?", "This will make all your add-on passwords visible in the add-on settings. Are you sure you wish to continue?"):
        for root, dirs, files in os.walk(ADDONS):
            for f in files:
                if f =='settings.xml':
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall(FILE)
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
# Thanks to Mikey1234 for some of these paths and also lambda for the clear cache option in genesis.
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
                            xbmc.log("### Successfully cleared %s files from %s" % (str(file_count), os.path.join(item,d)))
                        except:
                            xbmc.log("### Failed to wipe cache in: %s " % os.path.join(item,d))
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'CACHE' in d.upper():
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            xbmc.log("### Successfully wiped %s" % os.path.join(item,d))
                        except:
                            xbmc.log("### Failed to wipe cache in: %s" % os.path.join(item,d))

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
# Function to clear the addon_data
def Wipe_Kodi():
    stop = 0
    if dialog.yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe?', '', 'All addons and settings will be completely wiped!', yeslabel='YES, WIPE',nolabel='NO, STOP!'):
# Check Confluence is running before doing a wipe
        if skin!= "skin.confluence":
            dialog.ok('Default Confluence Skin Required','Please switch to the default Confluence skin before performing a wipe.')
            xbmc.executebuiltin("ActivateWindow(appearancesettings,return)")
            return
        else:
# Give the option to do a full backup before wiping
            if dialog.yesno("BACKUP EXISTING BUILD", 'Would you like to create a backup of your existing setup before proceeding?'):
                if USB == '':
                    dialog.ok('Please set your backup location before proceeding','You have not set your backup storage folder.\nPlease update the addon settings and try again.')
                    ADDON.openSettings(sys.argv[0])
                    if ADDON.getSetting('zip') == '' or not os.path.exists(ADDON.getSetting('zip')):
                        stop = 1
                        return
                if not stop:
                    CBPATH       = ADDON.getSetting('zip')
                    mybackuppath = os.path.join(CBPATH,'My_Builds')
                    if not os.path.exists(mybackuppath):
                        os.makedirs(mybackuppath)
                    vq = Get_Keyboard( heading="Enter a name for this backup" )
                    if ( not vq ): return False, 0
                    title = urllib.quote_plus(vq)
                    backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                    exclude_dirs_full =  ['plugin.program.nan.maintenance','plugin.program.tbs']
                    exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf','.gitignore']
                    message_header = "Creating full backup of existing build"
                    message1 = "Archiving..."
                    message2 = ""
                    message3 = "Please Wait"
                    Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            if not stop:
                keeprepos = dialog.yesno('DELETE REPOSITORIES?','Do you want to delete your repositories? Keeping bad repositories can be the cause of many problems, we recommend running Security Shield if you\'re in doubt.', yeslabel = 'KEEP REPOS', nolabel = 'DELETE REPOS')
                Wipe_Home(EXCLUDES)
                Wipe_Userdata()
                Wipe_Addons(keeprepos)
                Wipe_Addon_Data()
                Wipe_Home2(EXCLUDES)
                Kill_XBMC('wipe')
    else:
        return
#-----------------------------------------------------------------------------------------------------------------
# For loop to wipe files in special://home but leave ones in EXCLUDES untouched
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
                xbmc.log("Failed to remove file: %s" % name)
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
                print "Failed to remove: "+name
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
               xbmc.log("Failed to remove file: %s" % name)
#-----------------------------------------------------------------------------------------------------------------
# Remove addon directories
def Wipe_Addons(keeprepos):
    for name in os.listdir(ADDONS):
        if not keeprepos:
            if name not in EXCLUDES and not 'repo' in name:
                try:
                    dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDONS,name))
                except:
                    try:
                        os.remove(os.path.join(ADDONS,name))
                    except:
                        xbmc.log("Failed to remove: %s" % name)

        else:
            try:
                if name not in EXCLUDES:
                    dp.update(0,"Removing Add-on: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
                    shutil.rmtree(os.path.join(ADDONS,name))
            except:
                try:
                    os.remove(os.path.join(ADDONS,name))
                except:
                    xbmc.log("Failed to remove: %s" % name)
#-----------------------------------------------------------------------------------------------------------------
# Remove addon_data
def Wipe_Addon_Data():
    for name in os.listdir(ADDON_DATA):
        try:
            dp.update(0,"Removing Add-on Data: [COLOR=yellow]"+name+' [/COLOR]','','Please wait...')
            shutil.rmtree(os.path.join(ADDON_DATA,name))
        except:
            try:
                os.remove(os.path.join(ADDON_DATA,name))
            except:
                xbmc.log("Failed to remove: %s" % name)
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
                print "Failed to remove: "+name
    except:
        pass
#-----------------------------------------------------------------------------------------------------------------
# Report back with the version of Kodi installed
def XBMC_Version(url):
    xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
    version      = float(xbmc_version[:4])
    homearray    = HOME.split(os.sep)
    xbmc.log(str(homearray))
    arraylen     = len(homearray)
    koditype     = homearray[arraylen-1]
    if koditype == '':
        koditype = homearray[arraylen-2]
    koditype     = koditype.replace('.','').upper()
    dialog.ok('You are running: %s'%koditype, "Your version is: %s" % version)
#-----------------------------------------------------------------------------------------------------------------
# Check to see if any local shares require updating on server
def Check_My_Shares(url = ''):
    message = 0
    SF_Root = os.path.join(ADDON_DATA, 'plugin.program.super.favourites', 'Super Favourites')
    DB_Open(db_social)
    for row in cur.execute("SELECT * FROM shares;"):
        cleanpath = urllib.unquote(row[0])
        xbmc.log(cleanpath)
        localcheck = hashlib.md5(open(os.path.join(SF_Root, 'HOME_'+cleanpath, 'favourites.xml'),'rb').read()).hexdigest()
        if row[1] != localcheck:
            message = 1
            if dialog.yesno('UPDATE SHARE','The following social share has changed on your local machine:[COLOR=dodgerblue]',cleanpath,'[/COLOR]Would you like to update the online share?'):
                success = Update_Share(os.path.join(SF_Root, 'HOME_'+cleanpath))
                if success:
                    cur.execute("UPDATE shares SET stamp=? WHERE path=?", [localcheck, row[0]])
                    con.commit()
    if url == 'manual' and message == 0:
        dialog.ok('NOTHING TO UPDATE', 'You have not shared anything on the system which requires updating on the server.')
    con.close()
#-----------------------------------------------------------------------------------------------------------------
# Update a social share
def Update_Share(fullpath):
    urlparams = URL_Params()
    if urlparams != 'Unknown':
# Grab contents of the config file
        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg = cfgfile.read()
            cfg = cfg.replace('\r','').replace('\n','').replace('\t','')
            cfgfile.close()
        except:
            cfg=''

# Grab contents of the favourites.xml
        if os.path.exists(os.path.join(fullpath,'favourites.xml')):
            xmlfile  = open(os.path.join(fullpath,'favourites.xml'),'r')
            xml = xmlfile.read()
            xml = xml.replace(xbmc.translatePath('special://home'),'special://home/').replace(urllib.quote(xbmc.translatePath('special://home').encode("utf-8")),'special://home/').replace('\r','').replace('\n','').replace('\t','')
            xmlfile.close()
        else:
            xml="not a SF"

# Grab the clean part of the folder name to send
        itemname  = fullpath.split('/')
        last_item = len(itemname)-1
        fullpath  = os.path.join(itemname[last_item-1], itemname[last_item])
        if debug == 'true':
            xbmc.log('### Clean Full Path: %s' % fullpath)

# Attempt to send the share to system
        try:
            sendfaves = Open_URL_Share('http://tlbb.me/boxer/share_box.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',fullpath)))
            xbmc.log('http://tlbb.me/boxer/share_box.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',fullpath)))
            if 'success' in sendfaves:
                itemname  = itemname[last_item]
                dialog.ok('SOCIAL SHARE UPDATED', 'Thank you for sharing with the community.[COLOR=dodgerblue]',fullpath.split('/')[1], '[/COLOR]has now been updated and is publicly available.')
                return True
            elif 'no response' in sendfaves:
                dialog.ok('NOT UPDATED', 'There was an error trying to contact the server, please try again later.')
                return False
            elif 'Too Long' in sendfaves:
                dialog.ok('NOT UPDATED', 'Super Favourites contents are too large, please trim down in size and try again.')
                return False
        except:
            dialog.ok('NOT UPDATED', 'There was an error trying to add your content, please try again.')
            return False
    else:
        dialog.ok('FAULT DETECTED', 'It was not possible to obtain your MAC address details, please check your wifi and ethernet modules are enabled.')
#-----------------------------------------------------------------------------------------------------------------
# Open a database
def DB_Open(db_path):
    global cur
    global con
    con = database.connect(db_path)
    cur = con.cursor()
#-----------------------------------------------------------------------------------------------------------------
# Upload social share
def Upload_Share():
    choice         = 0
    urlparams      = URL_Params()
    item           = sys.listitem.getLabel()
    item           = item.replace('[COLOR ]','').replace('[/COLOR]','')
    path           = xbmc.getInfoLabel('ListItem.FolderPath')
    path           = urllib.unquote(path)
    if urlparams != 'Unknown':
        if debug == 'true':
            xbmc.log('### ORIG PATH: %s' % path)
            xbmc.log('### UNQUOTED PATH: %s' % path)
        try:
            scrap,fullpath = path.split('path=')
            fullpath       = xbmc.translatePath(fullpath)
            if debug == 'true':
                xbmc.log('### FULL PATH ORIG: %s' % fullpath)
        except:
            fullpath = "not a SF"
        if debug == 'true':
            xbmc.log('### FULL PATH FINAL: %s' % fullpath)
        
        if fullpath != "not a SF":
            localcheck = hashlib.md5(open(os.path.join(fullpath,'favourites.xml'),'rb').read()).hexdigest()
            mylistpath = urllib.quote(fullpath.split("HOME_",1)[1], safe='')
            if debug == 'true':
                xbmc.log('### md5: '+localcheck)
                xbmc.log('clean path: '+mylistpath)
            DB_Open(db_social)
            cur.execute("SELECT COUNT(*) from shares WHERE path = ?", [mylistpath])
            data = cur.fetchone()[0]
            if data:
                xbmc.log('### Updating Share in db: %s' % mylistpath)
                cur.execute("UPDATE shares SET stamp = ? WHERE path = ?", [localcheck, mylistpath])
            else:
                xbmc.log('### Adding Share to db: %s' % mylistpath)
                cur.execute("INSERT INTO shares (path, stamp) VALUES (?, ?)", [mylistpath, localcheck])
            con.commit()
            cur.close()
            con.close()
        else:
            dialog.ok(item.capitalize()+' Not Submitted', 'Items must be added to a valid Super Favourite folder first.')


        try:
            scrap,newpath  = path.split('Super Favourites'+os.sep)
        except:
            newpath  = "not a SF"
            newpath = newpath.replace('\\','/')

        if os.path.exists(os.path.join(fullpath,'favourites.xml')):
            xmlfile  = open(os.path.join(fullpath,'favourites.xml'),'r')
            xml = xmlfile.read()
            xml = xml.replace(xbmc.translatePath('special://home'),'special://home/').replace(urllib.quote(xbmc.translatePath('special://home').encode("utf-8")),'special://home/').replace('\r','').replace('\n','').replace('\t','')
            xmlfile.close()
        else:
            xml="not a SF"
            
        try:
            cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
            cfg = cfgfile.read()
            cfg = cfg.replace('\r','').replace('\n','').replace('\t','')
            cfgfile.close()
        except:
            cfg=''

        
        try:
            pluginname=xbmc.getInfoLabel('Container.PluginName')
            if debug == 'true':
                xbmc.log("### plugin name: %s" % str(pluginname))
        except:
            pluginname='none'

        quit = 0
        if pluginname == 'plugin.program.super.favourites':
    # Enable once we have private share options
        #        choice = dialog.select('Choose Share Type',['Share publicly','Add to my private share'])
            if xml == "not a SF" or newpath  == "not a SF":
                dialog.ok('Empty Folder','This folder doesn\'t contain any content. Please populate with content and try again.')
                quit = 1
    #        if choice == 0 and quit != 1:
            elif quit != 1:
                try:
                    sendfaves = Open_URL2('http://tlbb.me/boxer/share_box.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',newpath)))
                    if 'success' in sendfaves:
                        dialog.ok('Content Submitted', 'Thank you for sharing with the community.[COLOR=dodgerblue]',item,'[/COLOR]has now been shared and is publicly available.')
                    elif 'no response' in sendfaves:
                        dialog.ok(item.capitalize()+' Not Submitted', 'There was an error trying to contact the server, please try again later.')
                    elif 'Too Long' in sendfaves:
                        dialog.ok(item.capitalize()+' Not Submitted', 'Super Favourites contents are too large, please trim down in size and try again.')
                except:
                    dialog.ok(item.capitalize()+' Not Submitted', 'There was an error trying to add your content, please try again.')
    #        if choice == 1 and quit != 1:
    #            dialog.ok('Work In Progress','Sorry the private content section is currently a work in progress. Please check back soon.')
        if pluginname != 'plugin.program.super.favourites' and quit != 1:
            xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.super.favourites/capture.py)')
    else:
        dialog.ok('FAULT DETECTED', 'It was not possible to obtain your MAC address details, please check your wifi and ethernet modules are enabled.')
#-----------------------------------------------------------------------------------------------------------------
# Main function for launching maintenance add-on
def Launch():
    fanart      = None
    iconimage   = None
    mode        = None
    url         = None
    video       = None
    direct      = 'maintenance'
    params      = Get_Params()

    try:
        fanart=urllib.unquote_plus(params["fanart"])
    except:
        pass
    try:
        iconimage=urllib.unquote_plus(params["iconimage"])
    except:
        pass
    try:    
        mode=str(params["mode"])
    except:
        pass
    try:
        url=urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        video=urllib.unquote_plus(params["video"])
    except:
        pass
        
    if not os.path.exists(userdatafolder):
        os.makedirs(userdatafolder)

    if not os.path.exists(MEDIA):
        os.makedirs(MEDIA)


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

    if mode   == None                 : Categories()
    elif mode == 'ASCII_Check'        : ASCII_Check()
    elif mode == 'addon_removal_menu' : Addon_Removal_Menu()
    elif mode == 'backup'             : BACKUP()
    elif mode == 'backup_restore'     : Backup_Restore()
    elif mode == 'backup_option'      : Backup_Option()
    elif mode == 'browse_repos'       : Browse_Repos()
    elif mode == 'check_shares'       : Check_My_Shares(url)
    elif mode == 'check_updates'      : Addon_Check_Updates()
    elif mode == 'clear_cache'        : Clear_Cache()
    elif mode == 'delete_path'        : Delete_Path(url)
    elif mode == 'fix_special'        : Fix_Special(url)
    elif mode == 'enable_shares'      : Enable_Shares(url)
    elif mode == 'exec_xbmc'          : Exec_XBMC(url)
    elif mode == 'full_clean'         : Full_Clean()
    elif mode == 'grab_updates'       : Grab_Updates(url)
    elif mode == 'gotham'             : Gotham_Confirm()
    elif mode == 'helix'              : Helix_Confirm()
    elif mode == 'hide_passwords'     : Hide_Passwords()
    elif mode == 'install_venz'       : Install_Venz(url)
    elif mode == 'install_venz_menu'  : Install_Venz_Menu(url)
    elif mode == 'install_content'    : Install_Content(url)
    elif mode == 'install_menu'       : Install_Menu()
    elif mode == 'install_from_zip'   : Install_From_Zip()
    elif mode == 'ipcheck'            : IP_Check()
    elif mode == 'keywords'           : Keyword_Search()
    elif mode == 'kill_xbmc'          : Kill_XBMC(url)
    elif mode == 'kodi_settings'      : Kodi_Settings()
    elif mode == 'log'                : Log_Viewer()
    elif mode == 'main_menu_install'  : Main_Menu_Install(url)
    elif mode == 'manual_search'      : Manual_Search(url)
    elif mode == 'open_sf'            : Open_SF()
    elif mode == 'openlink'           : Open_Link(url)
    elif mode == 'open_system_info'   : Open_System_Info()
    elif mode == 'open_filemanager'   : Open_Filemanager()
    elif mode == 'openelec_backup'    : OpenELEC_Backup()
    elif mode == 'openelec_settings'  : OpenELEC_Settings()
    elif mode == 'play_video'         : yt.PlayVideo(url)
    elif mode == 'remove_addon_data'  : Remove_Addon_Data()
    elif mode == 'remove_addons'      : Remove_Addons(url)
    elif mode == 'remove_build'       : Remove_Build()
    elif mode == 'remove_crash_logs'  : Remove_Crash_Logs()
    elif mode == 'remove_packages'    : Remove_Packages()
    elif mode == 'remove_textures'    : Remove_Textures_Dialog()
    elif mode == 'restore_backup'     : Restore_Backup_XML(video,url,description)
    elif mode == 'restore_option'     : Restore_Option()
    elif mode == 'restore_zip'        : Restore_Zip_File(url)         
    elif mode == 'run_addon'          : Run_Addon(url)
    elif mode == 'runtest'            : speedtest.runtest(url)
    elif mode == 'search_content'     : Search_Content(url)
    elif mode == 'search_content_main': Search_Content_Main(url)
    elif mode == 'search_content_sub' : Search_Content('add_sub')
    elif mode == 'social_menu'        : Social_Menu()
    elif mode == 'speed_instructions' : Speed_Instructions()
    elif mode == 'speedtest_menu'     : Speed_Test_Menu()
    elif mode == 'start'              : Categories()
    elif mode == 'startup_wizard'     : xbmc.executebuiltin('RunAddon(script.openwindow)')
    elif mode == 'text_guide'         : Text_Guide(url)
    elif mode == 'tools'              : Tools()
    elif mode == 'tools_addons'       : Tools_Addons()
    elif mode == 'tools_clean'        : Tools_Clean()
    elif mode == 'tools_misc'         : Tools_Misc()
    elif mode == 'unhide_passwords'   : Unhide_Passwords()
    elif mode == 'update'             : Update_Repo()
    elif mode == 'uploadlog'          : Upload_Log()
    elif mode == 'xbmcversion'        : XBMC_Version(url)
    elif mode == 'wipe_xbmc'          : Wipe_Kodi()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


if not os.path.exists(TBSDATA):
    os.makedirs(TBSDATA)


if not os.path.exists(db_social):
    DB_Open(db_social)
    cur.execute('create table shares(path TEXT, stamp TEXT);')
    con.commit()
    cur.execute('create table friends(id INTEGER, name TEXT, friendgroup TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.execute('create table inbox(id INTEGER, fiendid INTEGER, message TEXT, read TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.execute('create table sent(id INTEGER, fiendid INTEGER, message TEXT, read TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.close()
    con.close()
