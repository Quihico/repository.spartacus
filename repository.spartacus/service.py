import xbmc
if not xbmc.getCondVisibility('System.HasAddon(script.python.koding.aio)'):
    try:
        xbmc.executebuiltin('InstallAddon(script.python.koding.aio)')
    except:
        pass

if not xbmc.getCondVisibility('System.HasAddon(script.openwindow)'):
    try:
        xbmc.executebuiltin('InstallAddon(script.openwindow)')
    except:
        pass