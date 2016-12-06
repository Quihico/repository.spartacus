import sys
import os
import xbmc
import xbmcgui
import yt
import default
import threading

dialog  = xbmcgui.Dialog()
runcode = ''

# If the tvguide skip file exists we can open live tv into the standard live tv SF folders
tvfile  = xbmc.translatePath('special://home/userdata/addon_data/script.trtv/skip.txt')
sys.argv[1] = sys.argv[1].replace("'",'')

redirect_file = xbmc.translatePath('special://home/userdata/addon_data/plugin.program.tbs/redirects/%s' % sys.argv[1])
xbmc.log('### REDIRECT FILE: %s' % redirect_file)

# Check the contents of the redirect file
if os.path.exists(redirect_file):
    xbmc.log('### redirect file exists, reading code')
    readfile = open(redirect_file, 'r')
    runcode  = readfile.read().replace('\r','')
    readfile.close()
    xbmc.log('### code: %s' % runcode)

if os.path.exists(tvfile):
    tvgskip = 1
    readfile = open(tvfile, 'r')
    tvpath   = readfile.read().replace('\r','').replace('\n','').replace('\t','')
    readfile.close()
else:
    tvgskip = 0
    tvpath  = ''

xbmc.log('### TV PATH: %s' % tvpath)

cleanname = sys.argv[1].replace("HOME_",'')
cleanname = cleanname.lower()

# Set the folder path to check
folderpath = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.program.super.favourites/Super Favourites/',sys.argv[1]))


def foldercheck(path):
    directories = 0
    for dirs in os.walk(folderpath):
        directories += len(dirs[1])
    return directories

folders = foldercheck(sys.argv[1])
# If the tvskip file IS present and the contents aren't blank we execute the command in the file
if sys.argv[1] == "HOME_LIVE_TV" and tvpath != '':
    exec(tvpath)

# If we're opening HOME_XXX
elif sys.argv[1] == 'HOME_XXX':
    success = default.Adult_Filter('true','menu')
    if success:
        if runcode != '':
            try:
                exec(runcode)
            except:
                dialog.ok('ERROR','It\'s not possible to open this section right now.', '', 'Please try again later.')
        else:
            xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?folder='+sys.argv[1]+'",return)')

# If the run code exists we run that
elif runcode != '':
    try:
        exec(runcode)
    except:
        dialog.ok('ERROR','It\'s not possible to open this section right now.', '', 'Please try again later.')

# If no runcode exists and the item is HOME_SYSTEM
elif sys.argv[1] == 'HOME_SYSTEM':
    xbmc.executebuiltin('ActivateWindow(settings)')

# If SF folder only contains one folder we open direct into the content folder
elif  folders == 1 and sys.argv[1] != "HOME_LIVE_TV":
    for dirs in os.listdir(folderpath):
        if os.path.isdir(os.path.join(folderpath, dirs)) and sys.argv[1] == 'HOME_MUSIC':
            xbmc.executebuiltin('ActivateWindow(10501,"plugin://plugin.program.super.favourites/?folder=%s/%s",return)' % (sys.argv[1], dirs))
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
    if sys.argv[1] == 'HOME_MUSIC':
        xbmc.log('HOME_MUSIC CHOSEN - OPENING WINDOW 10501')
        xbmc.executebuiltin('ActivateWindow(10501,"plugin://plugin.program.super.favourites/?folder='+sys.argv[1]+'",return)')
    else:
        xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.program.super.favourites/?folder='+sys.argv[1]+'",return)')

