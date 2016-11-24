import xbmc, os

RUN_WIZARD = xbmc.translatePath('special://profile/addon_data/script.openwindow/unregistered')

while xbmc.Player().isPlaying():
    xbmc.sleep(500)

if not os.path.exists(RUN_WIZARD):
    try:
        xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/default.py,service)')
    except:
        xbmc.executebuiltin('RunScript(special://xbmc/addons/script.openwindow/default.py,service)')