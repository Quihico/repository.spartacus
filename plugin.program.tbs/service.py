import re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, default

######################################################
AddonID='plugin.program.tbs'
AddonName='Maintenance'
######################################################
ADDON            =  xbmcaddon.Addon(id=AddonID)
dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()
HOME             =  xbmc.translatePath('special://home/')
USERDATA         =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA       =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS           =  xbmc.translatePath(os.path.join('special://home','addons',''))
cfgfile          =  xbmc.translatePath(os.path.join(ADDON_DATA,AddonID,'cfg'))
sleeper          =  os.path.join(ADDONS,AddonID,'resources','tmr')
internetcheck    =  ADDON.getSetting('internetcheck')
cachecheck       =  ADDON.getSetting('cleancache')
cbnotifycheck    =  ADDON.getSetting('cbnotifycheck')
mynotifycheck    =  ADDON.getSetting('mynotifycheck')
flashsplash      = '/flash/oemsplash.png'
newsplash        =  xbmc.translatePath('special://home/media/branding/Splash.png')
epgdst           =  xbmc.translatePath('special://home/addons/packages/epg')
runwizard        =  os.path.join(ADDONS,'packages','RUN_WIZARD')
#---------------------------------------------------------------------------------------------------

# Make sure this doesn't interfere with startup wizard
if not os.path.exists(runwizard):
    xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')
   
if internetcheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(internetloop,XBMC.RunScript(special://home/addons/'+AddonID+'/connectivity.py,silent=true),00:01:00,silent,loop)')

if cachecheck == 'true':
    xbmc.executebuiltin('XBMC.AlarmClock(cleancacheloop,XBMC.RunScript(special://home/addons/'+AddonID+'/cleancache.py,silent=true),12:00:00,silent,loop)')

readfile = open(sleeper, 'r')
sleep = readfile.read()
readfile.close()

#get filesizes
if os.path.exists(flashsplash):
    flashsize = os.path.getsize(flashsplash)
else:
    flashsize = 0

if os.path.exists(newsplash):
    newsize = os.path.getsize(newsplash)
else:
    newsize = 0

if flashsize != newsize and newsize != 0 and flashsize != 0:
    try:
        os.system('mount -o remount,rw /flash')
        os.system('cp /storage/.kodi/media/branding/Splash.png /flash/oemsplash.png')
        os.system('cp /storage/.kodi/media/branding/Splash.png /storage/.kodi/media/Splash.png')
    except:
        pass

if sleep == '':
    localfile = open(sleeper, mode='w+')
    localfile.write('23:59:59')
    localfile.close()

xbmc.executebuiltin('RunScript(special://home/addons/'+AddonID+'/checknews.py,shares)')
xbmc.executebuiltin('XBMC.AlarmClock(Shareloop,XBMC.RunScript(special://home/addons/'+AddonID+'/checknews.py,shares),12:00:00,silent,loop)')

if sleep != '':
    xbmc.executebuiltin('XBMC.AlarmClock(Notifyloop,XBMC.RunScript(special://home/addons/'+AddonID+'/checknews.py,silent=true),'+sleep+',silent,loop)')