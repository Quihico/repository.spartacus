import sys
import os
import xbmc
import xbmcgui
import yt
import default
import threading

dialog  = xbmcgui.Dialog()
direct  = xbmc.translatePath('special://home/userdata/addon_data/script.openwindow/direct')
# If the tvguide skip file exists we can open live tv into the standard live tv SF folders
tvfile  = xbmc.translatePath('special://home/userdata/addon_data/script.trtv/skip.txt')
if os.path.exists(tvfile):
    tvgskip = 1
    readfile = open(tvfile, 'r')
    tvpath   = readfile.read().replace('\r','').replace('\n','').replace('\t','')
    readfile.close()
else:
    tvgskip = 0
    tvpath  = ''

xbmc.log('### TV PATH: %s' % tvpath)
sys.argv[1] = sys.argv[1].replace("'",'')

cleanname = sys.argv[1].replace("HOME_",'')
cleanname = cleanname.lower()

# Set the folder path to check
folderpath = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/',sys.argv[1]))


def foldercheck(path):
    directories = 0
    for dirs in os.walk(folderpath):
        directories += len(dirs[1])
    xbmc.log("### %s Dirs: %s" % (cleanname, str(directories)))
    return directories

folders = foldercheck(sys.argv[1])

# If the tvskip file IS present and the contents aren't blank we execute the command in the file
if sys.argv[1] == "HOME_LIVE_TV" and tvpath != '':
    exec(tvpath)

# If SF folder only contains one folder we open direct into the content folder
elif  folders == 1 and sys.argv[1] != "HOME_LIVE_TV":
    for dirs in os.listdir(folderpath):
        if os.path.isdir(os.path.join(folderpath, dirs)):
            xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?folder=%s/%s",return)' % (sys.argv[1], dirs))

# If no SF items are present we bring up the nocontent menu and open the +/- options
elif folders == 0 or (sys.argv[1] == "HOME_LIVE_TV" and tvgskip and folders == 0):
    default.pop('nocontent.xml')
    xbmc.executebuiltin("RunScript(special://home/addons/plugin.program.tbs/epg.py,"+cleanname+")")

# If the tvskip file isn't present we open the EPG
elif sys.argv[1] == "HOME_LIVE_TV" and (tvgskip == 0 or tvpath == "xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/addon.py)')"):
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    xbmc.executebuiltin('RunScript(special://home/addons/script.trtv/addon.py)')
    xbmc.executebuiltin("Dialog.Close(busydialog)")

# Otherwise we open the relevant root SF folder
else:
    xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?folder='+sys.argv[1]+'",return)')

